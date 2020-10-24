# pylama:ignore=E402:ignore=E702
import sys; sys.path.append("..")
from datetime import datetime, timedelta
from requests.exceptions import HTTPError
from contextlib import suppress
from utils.misc import url_parser, validate_url, useragent_parser
from utils.geodata import geoip_info
import database as db
import time


FIRST_RUN_HOURS = 12
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


def query_badpackets(api, first_run=False):
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
            results_json = api.query(params).json()
            all_results += results_json['results']
            page_num = 2

            while results_json['next']:
                print("    ... Querying Page", page_num)
                time.sleep(1)
                results_json = api.get_url(results_json['next']).json()
                all_results += results_json['results']
                page_num += 1

    return all_results


def store_result(event_id, result_data):
    if db.Result.objects(event_id=event_id):
        return

    result_geodata = geoip_info(result_data['source_ip_address'])

    if not result_geodata:
        return

    post_payload_data = result_data['post_data'] + result_data['payload']
    payload_urls = url_parser(post_payload_data)
    valid_payload_urls = []

    for url in payload_urls:

        url_existing_payload = db.Payload.objects(payload_url=url).first()

        if url_existing_payload:
            url_existing_payload.updated_at = datetime.utcnow()
            return

        valid_url_info = validate_url(url)

        if not valid_url_info:
            return

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
