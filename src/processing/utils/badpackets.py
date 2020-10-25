# pylama:ignore=E402:ignore=E702
import sys; sys.path.append("..")
from datetime import datetime, timedelta
from requests.exceptions import HTTPError
from contextlib import suppress
from utils.misc import url_parser, validate_url, useragent_parser
from utils.geodata import geoip_info
import database as db
import time


FIRST_RUN_HOURS = 24
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
    """
    Queries the BadPackets API for N param combinations in PROC_PARAMS
    If the initial query result contains more than 1 page, all remaining
    pages are also queried and collected.

    Args:
        api (BadPacketsAPI): The BadPackets wrapper API instance to be used.
        first_run (bool, optional): Defaults to False. Determines if FIRST_RUN_HOURS
            should be used to calculated after_dt instead of the default (1 hour).

    Returns:
        list: A list of BadPackets Results (dictionaries)
    """
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
    """
    Takes a given event_id and results dict for a BadPackets result
    and processes it:
    - ignore if result is already stored or no geodata can be found
    - extract URls in payload data and process each URL
        - validate and obtain IP and hostname for each URL
        - add new Payload & GeoData entry for each URL / IP
    - insert new Result and GeoData entry for the given result

    Args:
        event_id (str): The event_id of the given BadPackets Result
        result_data (dict): The dictionary (JSON Object) result data
    """
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
    result_data['user_agent'] = useragent_parser(result_data['user_agent'])
    result_data['payload_urls'] = valid_payload_urls
    db.Result(**result_data).save()

    # Create GeoData entry
    result_geodata = db.GeoData(
        ip_address=result_data['source_ip_address'],
        server_type="Report Server" if valid_payload_urls else "Bot",
        data=result_geodata,
        updated_at=datetime.utcnow()
    ).save()
