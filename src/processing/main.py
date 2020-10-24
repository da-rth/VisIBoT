from badpackets import BadPacketsAPI
from dotenv import load_dotenv
from datetime import datetime, timedelta
from requests.exceptions import HTTPError
from contextlib import suppress
from tqdm import tqdm
from utils.utilities import url_parser, validate_url
from utils.geodata import geoip_info
import concurrent.futures
import dateutil.parser
import database as db
import os
import asyncio
import time

# Constants

HOURLY_AT_MIN = 30

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


executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)


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
        data=result_geodata,
        updated_at=datetime.utcnow()
    ).save()

def process_results(results):
    print(f"\nTotal BadPackets results to process: {len(results)}\n")
    results = { each['event_id'] : each for each in results }
    results_length = len(results)

    futures = []
    
    for evt, res in results.items():
        futures.append(executor.submit(store_result, evt, res))
    
    for i, future in enumerate(concurrent.futures.as_completed(futures)):
        print(f"Processed {i}/{results_length} results", end="\r")

    print(f"\nCompleted processing. Waiting until: {ceil_dt(datetime.utcnow(), timedelta(minutes=30)).strftime('%H:%M:%S')}\n\n", end="\r")


def query_badpackets(first_run=False):
    all_results = []

    after_dt = (
        datetime.utcnow() - timedelta(hours=6 if first_run else 1)
    ).strftime('%Y-%m-%dT%H:%M:%SZ')

    print(f"Querying results from BadPackets last seen after {after_dt}")

    for param, value in PROC_PARAMS:
        params = BASE_PARAMS.copy()
        params['last_seen_after'] = after_dt
        params[param] = value

        print(f" -> Querying param: {param}={value} | Last seen after: {after_dt}")

        with suppress(HTTPError, AttributeError):
            time.sleep(1)
            results_json = bp_api.query(params).json()
            all_results += results_json['results']
            page_num = 1

            while results_json['next']:
                page_num += 1
                print("    ... Querying Page", page_num)
                time.sleep(1)
                results_json = bp_api.get_url(results_json['next']).json()
                all_results += results_json['results']

    return tuple(all_results)


def background_process_task(first_run=False):
    all_bp_results = query_badpackets(first_run)
    process_results(all_bp_results)


def ceil_dt(dt, delta):
    return dt + (datetime.min - dt) % delta


if __name__ == "__main__":
    load_dotenv(verbose=True)

    bp_api = BadPacketsAPI(
        api_url=os.getenv("BADPACKETS_API_URL"),
        api_token=os.getenv("BADPACKETS_API_TOKEN")
    )
    
    bp_api.ping().raise_for_status()
    print("BadPackets API: Authenticated token")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        first_run = True
        print(f"Initialised hourly task. Executes at minute {HOURLY_AT_MIN}\n")

        while True:
            dtnow = datetime.utcnow()
            
            if (dtnow.minute == HOURLY_AT_MIN and dtnow.second == 0) or first_run:
                print("Hourly processing script triggered\n")

                executor.submit(background_process_task, (first_run))
                first_run = False
            
            time.sleep(1)

    except (asyncio.CancelledError, KeyboardInterrupt):
        print("Closing processing script...")
    finally:
        loop.close()
