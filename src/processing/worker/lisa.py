# pylama:ignore=E402:ignore=E702
import sys; sys.path.append("..")
import database as db
import utils.misc as misc
import requests
import logging
import os
import validators

from utils.geodata import geoip_info
from pydnsbl import DNSBLIpChecker
from pydnsbl.providers import Provider, DNSBL_CATEGORY_CNC

logger = logging.getLogger('lisa')
providers = [
    Provider('b.barracudacentral.org'),
    Provider('combined.abuse.ch'),
    Provider('drone.abuse.ch'),
    Provider('dyna.spamrats.com'),
    Provider('noptr.spamrats.com'),
    Provider('zombie.dnsbl.sorbs.net'),
    Provider('zen.spamhaus.org'),
]

LISA_API_URL = os.getenv("LISA_API_URL", "http://localhost:4242/api")
LISA_EXEC_TIME = os.getenv("LISA_EXEC_TIME", 30)
ASCII_WEB_EXTS = [
    "html",
    ".htm",
    ".php",
    ".xml",
    ".js",
    ".css",
    ".scss",
    ".jsp",
    ".rss",
    ".asp",
    ".cfm",
    ".wss",
    ".rss",
    ".yaws",
    ".cgi",
]
SPREADING_KEYWORDS = [
    "wget",
    "curl",
    "tftp",
    "/tmp",
    "http",
]
P2P_DOMAINS = [
    ".utorrent.com",
    ".transmissionbt.com",
    ".bittorrent.com",
    ".debian.org",
]


def create_lisa_task(payload):
    try:
        r = requests.post(f"{LISA_API_URL}/tasks/create/file", {
            'url': payload.url,
            'exec_time': int(LISA_EXEC_TIME)
        })
        lisa_task_id = r.json().get('task_id', None) if r.json() else None

        if lisa_task_id:
            db.create_processing_payload_entry(payload, lisa_task_id)
        # else analysis could not be created (e.g. payload host is offline)
    except ConnectionError:
        print("[LiSa] Sandbox server is offline. Could not process payload", payload.id)


def create_geo_entry(ip_address, geo_type):
    geodata = geoip_info(ip_address)

    if not geodata:
        return None

    hostname = misc.get_ip_hostname(ip_address)

    return db.geodata_create_or_update(
        ip_address,
        hostname,
        geo_type,
        geodata
    )


def create_cnc_entry(geo, payload, heuristics):
    return db.candidate_cnc_create_or_update(
        ip_address=geo.id,
        payload_ids=[payload.id],
        heuristics=heuristics
    )


def create_p2p_entry(geo, payload, heuristics, nodes):
    return db.candidate_p2p_create_or_update(
        ip_address=geo.id,
        payload_ids=[payload.id],
        heuristics=heuristics,
        nodes=nodes
    )


def is_endpoint_spreading(ip_address, analysis):
    for req in analysis['network_analysis']['http_requests']:
        if 'headers' in req and ip_address in req['headers'].get('Host', ''):
            uri_has_keyword = any(s in req['uri'] for s in SPREADING_KEYWORDS)
            soap_has_keyword = any(s in req['headers'].get('SOAPAction', '') for s in SPREADING_KEYWORDS)
            if uri_has_keyword or soap_has_keyword:
                return True
    return False


def is_p2p(analysis):
    for dns_q in analysis['network_analysis']['dns_questions']:
        if dns_q.get('name', None) in P2P_DOMAINS:
            return True

    return False


def check_hostname_p2p(ip_address):
    hostname = misc.get_ip_hostname(ip_address)

    if not hostname:
        return False

    for p2p_domain in P2P_DOMAINS:
        if p2p_domain in hostname:
            return True

    return False


def identify_heuristics(endpoint, strings, is_blacklisted_c2):
    heuristics = []

    if (endpoint['data_in'] > 0) and (endpoint['data_out'] > 0):
        heuristics.append("Data exchange from IP address")

    if endpoint['ip'] in strings['ipv4_addresses']:
        heuristics.append("Connection to hardcoded IP address")

    if is_blacklisted_c2:
        heuristics.append("Connection to blacklisted C2 IP address")

    return heuristics


def update_payload_and_connections(payload, analysis, cnc_geos, p2p_geos):
    analysis['binary_info'] = analysis['static_analysis']['binary_info'].copy()

    # These dictionaries take up a lot of space...
    del analysis['dynamic_analysis']
    del analysis['static_analysis']

    lisa_analysis = db.lisa_analysis_create_or_update(analysis)

    payload.update(
        set__lisa=lisa_analysis,
        set__keyword=analysis.get('keyword', None),
        add_to_set__candidate_C2s=cnc_geos,
        add_to_set__candidate_P2Ps=p2p_geos,
    )

    for geo in set(cnc_geos + p2p_geos):
        if payload.ip_address != geo:
            db.geo_connections_create_or_update(payload.ip_address, geo)


def process_strings(strings):
    results = {
        "ipv4_addresses": [],
        "ipv6_addresses": [],
        "urls": [],
        "domains": [],
    }

    for string in strings:
        ipv4 = misc.ip_parser(string)
        ipv6 = misc.ipv6_parser(string)

        if ipv4 and validators.ip_address.ipv4(ipv4) and misc.is_public_ip(ipv4):
            # Ignores IPs like 1.1.1.1 and 8.8.8.8
            if len(ipv4) == 8:
                continue

            results['ipv4_addresses'].append(ipv4)

        if ipv6 and validators.ip_address.ipv6(ipv6) and misc.is_public_ip(ipv6):
            results['ipv4_addresses'].append(ipv6)

        for url in misc.extractor.find_urls(string):
            url = url.replace(")", "")
            url = url.split(":")[0] if url.count(":") == 1 else url
            ignore_url = "HNAP1" in url or "schema" in url

            if ignore_url or ipv4 in url and not misc.is_public_ip(ipv4):
                continue

            if validators.url(url):
                results['urls'].append(url)
            elif validators.domain(url) and ".sh" not in url:
                results['domains'].append(url)

    return results


def process_analysis(task_id, analysis):
    proc_payload = db.ProcessingPayloads.objects(task_id=task_id).first()
    payload = proc_payload.payload if proc_payload else None

    if not payload or 'network_analysis' not in analysis:
        return

    vt_scans = analysis['virustotal'].get('scans', None) if 'virustotal' in analysis else None
    analysis['keyword'] = misc.get_top_malware_keyword(vt_scans) if vt_scans else None
    analysis['static_strings'] = process_strings(analysis['static_analysis']['strings'])
    analysis['task_id'] = task_id
    analysis['payload'] = payload

    ip_checker = DNSBLIpChecker(providers=providers)
    candidate_CNCs = []
    candidate_P2Ps = []

    is_p2p_botnet = is_p2p(analysis)

    for endpoint in analysis['network_analysis']['endpoints']:
        ip_address = endpoint['ip']

        if not is_p2p_botnet:
            is_p2p_botnet = check_hostname_p2p(ip_address)

        if not misc.is_public_ip(ip_address) or is_endpoint_spreading(ip_address, analysis):
            continue

        blacklist_categories = ip_checker.check(endpoint['ip']).categories
        is_blacklisted_c2 = DNSBL_CATEGORY_CNC in blacklist_categories

        heuristics = identify_heuristics(endpoint, analysis['static_strings'], is_blacklisted_c2)

        if heuristics:
            geo_type = "P2P Node" if (is_p2p_botnet and not is_blacklisted_c2) else "C2 Server"
            geo = create_geo_entry(ip_address, geo_type)

            if geo:
                if is_p2p_botnet and not is_blacklisted_c2:
                    candidate_P2Ps.append((geo, heuristics))
                else:
                    candidate_CNCs.append((geo, heuristics))

    for node_geo, heuristics in candidate_P2Ps:
        nodes = list(set(n.id for n, _ in candidate_P2Ps if n.id != node_geo.id))
        create_p2p_entry(node_geo, payload, heuristics, nodes)

    for cnc_geo, heuristics in candidate_CNCs:
        create_cnc_entry(cnc_geo, payload, heuristics)

    update_payload_and_connections(
        payload,
        analysis,
        cnc_geos=[geo for geo, _ in candidate_CNCs],
        p2p_geos=[geo for geo, _ in candidate_P2Ps]
    )

    proc_payload.delete()


def process_failure(task_id, failure_data):
    exec_type = failure_data.get('exc_type', None)
    filename = failure_data.get('filename', '').lower()
    proc_payload = db.ProcessingPayloads.objects(task_id=task_id).first()

    # Only process failure for exceptions caused by attempted analysis of non-binary/ascii executable payloads
    if exec_type == 'UnicodeDecodeError' or any(s in filename for s in ASCII_WEB_EXTS):
        payload = proc_payload.payload if proc_payload else None

        if payload:
            # Delete GeoIpData if first occurrence (CASCADE will delete the payload itself)
            if payload.ip_address.occurrences == 1:
                payload.ip_address.delete()
            else:
                payload.delete()
    else:
        if proc_payload:
            proc_payload.delete()
