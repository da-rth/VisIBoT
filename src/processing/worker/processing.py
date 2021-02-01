# pylama:ignore=E402:ignore=E702
import sys; sys.path.append("..")
import database as db
import logging
import time
import validators
import os
from datetime import datetime, timedelta
from urllib.parse import urlparse
from utils.misc import url_parser, useragent_parser, get_ip_hostname
from utils.geodata import geoip_info

logger = logging.getLogger('collection')


def store_result_geodata(result_data, scanned_payloads, connections):
    ip = result_data['source_ip_address']
    geodata = geoip_info(ip)

    if not geodata:
        return

    hostname = get_ip_hostname(ip)

    has_botnet_tag = any(tag['category'] in ["Botnet Activity"] for tag in result_data.get('tags', []))
    is_self_hosting = ip in result_data['payload'] + result_data['post_data']

    if scanned_payloads:
        if has_botnet_tag or is_self_hosting:
            server_type = "Malicious Bot"
        else:
            server_type = "Report Server"
    elif has_botnet_tag:
        server_type = "Bot"
    else:
        return

    geo = db.geodata_create_or_update(
        ip,
        hostname,
        server_type,
        geodata,
        result_data['tags']
    )

    for conn in connections:
        if geo.ip_address != conn.ip_address:
            db.geo_connections_create_or_update(geo, conn)

    result_data['source_ip_address'] = geo.id
    result_data['user_agent'] = useragent_parser(result_data['user_agent'])
    result_data['scanned_urls'] = [payload.url for payload in scanned_payloads]
    result_data['affiliated_ips'] = [payload.ip_address for payload in scanned_payloads]
    db.result_create_or_update(result_data)


def store_result_payload(url_info, source_ip_address):
    url, ip, hostname = url_info

    existing_geo = db.IpGeoData.objects(ip_address=ip).first()
    existing_payload = db.MalwarePayload.objects(url=url).first()

    if existing_payload and existing_geo:
        existing_payload.update(
            set__updated_at=datetime.utcnow()
        )

        return (existing_payload, existing_geo, True)
    else:
        is_self_hosted = source_ip_address == ip
        server_type = "Malicious Bot" if is_self_hosted else "Payload Server"
        geodata = geoip_info(ip)
        if geodata:
            geo = db.geodata_create_or_update(ip, hostname, server_type, geodata)

            if existing_payload:
                return (existing_payload, geo, True)
            else:
                payload = db.payload_create_or_update(url, ip)
                return (payload, geo, False)
        else:
            return (None, None, False)


def store_result(result_data):
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
    connections = []
    scanned_payloads = []
    existing_result = db.BadpacketsResult.objects(event_id=result_data['event_id']).first()

    if existing_result:
        existing_result.update(
            set__updated_at=datetime.utcnow(),
        )

        existing_result.source_ip_address.update(
            set__updated_at=datetime.utcnow()
        )
        return []

    payload_data = result_data['post_data'] + result_data['payload']
    malicious_urls = [url for url in url_parser(payload_data) if url]

    for url_info in malicious_urls:
        payload, geo, already_exists = store_result_payload(url_info, result_data['source_ip_address'])

        if payload and geo and not already_exists:
            scanned_payloads.append(payload)
            connections.append(geo)

    store_result_geodata(result_data, scanned_payloads, connections)

    return scanned_payloads
