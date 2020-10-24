from badpackets import BadPacketsAPI
from dotenv import load_dotenv
from datetime import datetime, timedelta
from requests.exceptions import HTTPError
from contextlib import suppress
from utils.utilities import url_parser, validate_url, useragent_parser, time_until
from utils.geodata import geoip_info
import concurrent.futures
import database as db
import os
import time

load_dotenv(verbose=True)

# Constants
FIRST_RUN = True
FIRST_RUN_HOURS = 24

MAX_THREADS = 8
HOURLY_AT_MIN = 30

BP_URL = os.getenv("BADPACKETS_API_URL")
BP_KEY = os.getenv("BADPACKETS_API_KEY")

BASE_PARAMS = {
    'limit': 1000,
    'protocol': 'tcp',
}
PROC_PARAMS = [
    ('payload', 'chmod'),
    ('post_data', 'chmod'),
    ('tags', 'IoT'),
    ('tags', 'Mirai'),
]


executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS)


def store_result(event_id, result_data):
    if db.Result.objects(event_id=event_id): return

    result_geodata = geoip_info(result_data['source_ip_address'])

    if not result_geodata: return

    post_payload_data = result_data['post_data'] + result_data['payload']
    payload_urls = url_parser(post_payload_data)
    valid_payload_urls = []
    
    for url in payload_urls:

        url_existing_payload = db.Payload.objects(payload_url=url).first()

        if url_existing_payload:
            url_existing_payload.updated_at = datetime.utcnow()
            return

        valid_url_info = validate_url(url)

        if not valid_url_info: return

        url_hostname, url_ip = valid_url_info
        url_ip_geodata = geoip_info(url_ip)
        url_existing_geodata = db.GeoData.objects(ip_address=url_ip).first()

        if (not url_ip_geodata):
            return

        if url_existing_geodata:
            url_existing_geodata.updated_at = datetime.utcnow()
            return

        db.GeoData(
            ip_address=url_ip,
            data=url_ip_geodata,
            server_type="Loader Server",
            updated_at=datetime.utcnow()
        ).save()

        db.Payload(
            payload_url=url,
            ip_address=url_ip,
            vt_scan_url="http://virustotal.com/TODO",
            updated_at=datetime.utcnow()
        ).save()

        valid_payload_urls.append(url)
    
    # Create Result entry
    result_data['payload_urls'] = valid_payload_urls
    db.Result(**result_data).save()

    # Create GeoData entry
    result_geodata = db.GeoData(
        ip_address=result_data['source_ip_address'],
        server_type="Report Server" if valid_payload_urls else "Bot",
        user_agent=useragent_parser(result_data['user_agent']),
        data=result_geodata,
        updated_at=datetime.utcnow()
    ).save()


def query_badpackets(first_run=False):
    all_results = []

    after_dt = (
        datetime.utcnow() - timedelta(hours=FIRST_RUN_HOURS if first_run else 1)
    ).strftime('%Y-%m-%dT%H:%M:%SZ')

    print(f"Querying results from BadPackets last seen after {after_dt}")

    for param, value in PROC_PARAMS:
        params = BASE_PARAMS.copy()
        params['last_seen_after'] = after_dt
        params[param] = value

        print(f" -> Querying param: {param}={value}")

        with suppress(HTTPError, AttributeError):
            time.sleep(1)
            results_json = bp_api.query(params).json()
            all_results += results_json['results']
            page_num = 2

            while results_json['next']:
                print("    ... Querying Page", page_num)
                time.sleep(1)
                results_json = bp_api.get_url(results_json['next']).json()
                all_results += results_json['results']
                page_num += 1

    return all_results


def background_process_task(first_run=False):
    results = { each['event_id'] : each for each in query_badpackets(first_run) }
    res_len = len(results)

    print(f"\nTotal BadPackets results to process: {res_len}\n")

    futures = [executor.submit(store_result, evt, res) for evt, res in results.items()]
    
    for i, future in enumerate(concurrent.futures.as_completed(futures)):
        print(f"Processed {i+1}/{res_len} results", end="\r")

    print(f"Completed processing. Waiting until next cycle at: {time_until(HOURLY_AT_MIN)} (UTC)\n", end="\r")


def init_processing_loop():
    while True:
        dtnow = datetime.utcnow()
        
        if (dtnow.minute == HOURLY_AT_MIN and dtnow.second == 0):
            print("Hourly processing script triggered\n")
            executor.submit(background_process_task)
        
        time.sleep(1)


if __name__ == "__main__":

    bp_api = BadPacketsAPI(api_url=BP_URL, api_token=BP_KEY)
    bp_api.ping().raise_for_status()

    print("BadPackets API: Authenticated token\n")

    time.sleep(1)

    try:
        if FIRST_RUN:
            print("Preparing first run...\n")
            background_process_task(first_run=True)

        print(f"Waiting until next cycle at: {time_until(HOURLY_AT_MIN)} (UTC)\n", end="\r")
        init_processing_loop()

    except (KeyboardInterrupt):
        print("\nClosing processing script. Waiting on Threads to finish...")
        executor.shutdown(wait=True)

