import logging
import mongoengine as mongo
from utils.whois import get_asn_info, get_asn_origins
from pymongo.errors import DuplicateKeyError
from mongoengine.errors import NotUniqueError
from datetime import datetime

logger = logging.getLogger('database')


class AutonomousSystem(mongo.DynamicDocument):
    """
    Document containing ASN info for ASNs associated with any ip address in IpGeoData
    """
    asn               = mongo.StringField(required=True, primary_key=True)
    asn_date          = mongo.DateTimeField(required=False, default=None)


class IpGeoData(mongo.Document):
    """
    Server/IP Address information pulled from payload data of
    BadPackets results
    """
    ip_address        = mongo.StringField(required=True, primary_key=True)
    asn               = mongo.ReferenceField(AutonomousSystem, required=False)
    prev_asns         = mongo.ListField(mongo.DictField(required=False), default=[])
    occurrences       = mongo.IntField(default=0)
    data              = mongo.DictField(required=True)
    hostname          = mongo.StringField(required=False)
    tags              = mongo.DictField(required=False)
    server_type       = mongo.StringField(
        required=True,
        choices=[
            "C2 Server",
            "P2P Node",
            "Payload Server",
            "Report Server",
            "Malicious Bot",
            "Bot",
        ]
    )
    created_at        = mongo.DateTimeField(default=datetime.utcnow)
    updated_at        = mongo.DateTimeField(default=datetime.utcnow)


class IpEvent(mongo.Document):
    """
    Server/IP Address information pulled from payload data of
    BadPackets results
    """
    ip_address        = mongo.ReferenceField(IpGeoData, required=True)
    created_at        = mongo.DateTimeField(default=datetime.utcnow)
    event_type        = mongo.StringField(
        required=True,
        choices=[
            "C2 Server",
            "P2P Node",
            "Payload Server",
            "Report Server",
            "Malicious Bot",
            "Bot",
        ]
    )


class CandidateC2AsnOrigin(mongo.DynamicDocument):
    """
    OneToMany Document containing all ASN info associated with IP Addresses stored in the IpGeoData table
    """
    ip_address        = mongo.ReferenceField(IpGeoData, required=True)
    updated_time      = mongo.DateTimeField(required=True)
    meta = {
        'indexes': [
            {'fields': ('ip_address', 'updated_time'), 'unique': True}
        ]
    }


class IpGeoConnection(mongo.Document):
    """
    Document containing all connections between one IpGeoData Object and various others
    """
    source_ip         = mongo.ReferenceField(IpGeoData, required=True)
    destination_ip    = mongo.ReferenceField(IpGeoData, required=True)
    occurrences       = mongo.IntField(default=1)
    created_at        = mongo.DateTimeField(default=datetime.utcnow)
    meta = {
        'indexes': [
            {'fields': ('source_ip', 'destination_ip'), 'unique': True}
        ]
    }


class MalwarePayload(mongo.Document):
    """
    Malware payload information retrieved from BadPackets results
    """
    url               = mongo.StringField(required=True, primary_key=True)
    occurrences       = mongo.IntField(default=1)
    lisa              = mongo.ReferenceField('LisaAnalysis', required=False)
    ip_address        = mongo.ReferenceField(IpGeoData, required=True)
    is_self_hosted    = mongo.BooleanField(required=True, default=False)
    candidate_C2s     = mongo.ListField(mongo.ReferenceField(IpGeoData, required=False), default=[])
    candidate_P2Ps    = mongo.ListField(mongo.ReferenceField(IpGeoData, required=False), default=[])
    created_at        = mongo.DateTimeField(default=datetime.utcnow)
    updated_at        = mongo.DateTimeField(default=datetime.utcnow)


class LisaAnalysis(mongo.DynamicDocument):
    """
    Malware binary information obtained from LiSa Sandbox
    """
    task_id           = mongo.StringField(required=True, primary_key=True)
    payload           = mongo.ReferenceField(MalwarePayload, required=True)
    created_at        = mongo.DateTimeField(default=datetime.utcnow)


class CandidateC2Server(mongo.Document):
    """
    Candidate C2 Server extracted from network analysis of malware extracted from a payload
    """
    ip_address        = mongo.ReferenceField(IpGeoData, required=True)
    payloads          = mongo.ListField(mongo.ReferenceField(MalwarePayload, required=False), required=False)
    heuristics        = mongo.ListField(mongo.StringField())
    occurrences       = mongo.IntField(default=1)
    created_at        = mongo.DateTimeField(default=datetime.utcnow)
    updated_at        = mongo.DateTimeField(default=datetime.utcnow)


class CandidateP2pNode(mongo.Document):
    """
    Candidate C2 Server extracted from network analysis of malware extracted from a payload
    """
    ip_address        = mongo.ReferenceField(IpGeoData, required=True)
    payloads          = mongo.ListField(mongo.ReferenceField(MalwarePayload, required=False), required=False)
    nodes             = mongo.ListField(mongo.ReferenceField('self', required=False), required=False)
    heuristics        = mongo.ListField(mongo.StringField())
    occurrences       = mongo.IntField(default=0)
    created_at        = mongo.DateTimeField(default=datetime.utcnow)
    updated_at        = mongo.DateTimeField(default=datetime.utcnow)


class BadpacketsResult(mongo.Document):
    """
    BadPackets Result JSON information
    """
    event_id          = mongo.StringField(required=True, primary_key=True)
    source_ip_address = mongo.ReferenceField(IpGeoData, required=True)
    country           = mongo.StringField(required=True, max_length=4)
    user_agent        = mongo.DictField(required=True)
    payload           = mongo.StringField(required=True)
    post_data         = mongo.StringField(required=True)
    target_port       = mongo.IntField(required=True)
    protocol          = mongo.StringField(required=True)
    event_count       = mongo.IntField(required=True)
    first_seen        = mongo.StringField(required=True)
    last_seen         = mongo.StringField(required=True)
    tags              = mongo.ListField(mongo.DictField(required=True), required=True)
    scanned_urls      = mongo.ListField(mongo.ReferenceField(MalwarePayload, required=False), required=False)
    affiliated_ips    = mongo.ListField(mongo.ReferenceField(IpGeoData, required=False), required=False)
    created_at        = mongo.DateTimeField(default=datetime.utcnow)
    updated_at        = mongo.DateTimeField(default=datetime.utcnow)


def payload_create_or_update(url, ip, lisa=None, candidate_C2s=[], candidate_P2Ps=[]):
    payload = None

    try:
        payload = MalwarePayload(
            url=url,
            ip_address=ip,
            lisa=lisa,
            candidate_C2s=candidate_C2s,
            candidate_P2Ps=candidate_P2Ps,
        )
        payload.save()
    except NotUniqueError:
        payload = MalwarePayload.objects(url=url).first()
        payload.update(
            set__updated_at=datetime.utcnow(),
            set__lisa=lisa if lisa else payload.lisa,
            add_to_set__candidate_C2s=candidate_C2s,
            add_to_set__candidate_P2Ps=candidate_P2Ps,
            inc__occurrences=1
        )

    return payload


def result_create_or_update(result_data):
    result = None

    try:
        result = BadpacketsResult(**result_data)
        result.save()
    except (NotUniqueError, DuplicateKeyError):
        result = BadpacketsResult.objects(event_id=result_data['event_id']).first()
        result.update(
            add_to_set__scanned_payloads=result_data['scanned_payloads'],
            set__updated_at=datetime.utcnow()
        )

    return result


def asn_get_or_create(asn_info):
    try:
        asn = AutonomousSystem(**asn_info)
        asn.save()
    except (NotUniqueError, DuplicateKeyError):
        asn = AutonomousSystem.objects(asn=asn_info['asn']).first()

    return asn


def c2_asn_origins_create(ip_ref, asn_origins):
    for origin in asn_origins:
        try:
            o = CandidateC2AsnOrigin(**origin, ip_address=ip_ref)
            o.save()
        except (NotUniqueError, DuplicateKeyError):
            pass


def geodata_create_or_update(ip, hostname, server_type, geodata, tags=[]):
    geo = None
    asn_info = get_asn_info(ip)
    asn_ref = asn_get_or_create(asn_info) if asn_info else None

    flattened_tags = {
        'cves': set(),
        'categories': set(),
        'descriptions': set(),
    }

    for tag in tags:
        flattened_tags['cves'].add(tag['cve'])
        flattened_tags['categories'].add(tag['category'])
        flattened_tags['descriptions'].add(tag['description'])

    try:
        geo = IpGeoData(
            ip_address=ip,
            asn=asn_ref,
            hostname=hostname,
            server_type=server_type,
            data=geodata,
            tags=flattened_tags if tags else {}
        )
        geo.save()
    except (NotUniqueError, DuplicateKeyError):
        geo = IpGeoData.objects(ip_address=ip).first()

        loader_to_c2_p2p = (
            geo.server_type == "Loader Server" and
            (server_type == "C2 Server" or server_type == "P2P Node")
        )

        report_to_loader = (
            geo.server_type in ["Report Server", "Malicious Bot"] and
            server_type == "Loader Server"
        )

        bot_to_report = (
            geo.server_type == "Bot" and
            server_type == "Report Server" or server_type == "Malicious Bot"
        )

        low_to_high = (
            geo.server_type in ["Report Server", "Malicious Bot", "Bot"] and
            server_type in ["C2 Server", "P2P Node", "Loader Server"]
        )

        if not (loader_to_c2_p2p or report_to_loader or bot_to_report or low_to_high):
            server_type = geo.server_type

        if 'cves' in geo.tags:
            n_tags = geo.tags.copy()

            for k, v in n_tags.items():
                n_tags[k] = set(v)

            n_tags['cves'].update(flattened_tags['cves'])
            n_tags['categories'].update(flattened_tags['categories'])
            n_tags['descriptions'].update(flattened_tags['descriptions'])
        else:
            n_tags = flattened_tags

        if asn_ref and asn_ref != geo.asn:
            geo.update(
                set__asn=asn_ref,
                add_to_set__prev_asns=[{
                    'asn': geo.asn,
                    'logged_at': datetime.utcnow()
                }],
            )

        geo.update(
            set__tags=n_tags,
            set__updated_at=datetime.utcnow(),
            set__server_type=server_type,
            inc__occurrences=1
        )

    if server_type == "C2 Server":
        ip_asn_origins = get_asn_origins(ip)
        c2_asn_origins_create(geo, ip_asn_origins)

    evt = IpEvent(
        ip_address=ip,
        event_type=server_type,
    )
    evt.save()

    return geo


def candidate_cnc_create_or_update(ip_address, payload_ids, heuristics):
    c2 = None

    try:
        c2 = CandidateC2Server(
            ip_address=ip_address,
            payloads=payload_ids,
            heuristics=heuristics
        )
        c2.save()
    except (NotUniqueError, DuplicateKeyError):
        c2 = CandidateC2Server(ip_address=ip_address).first()
        c2.update(
            add_to_set__payloads=payload_ids,
            add_to_set__heuristics=heuristics,
            inc__occurrences=1,
            set__updated_at=datetime.utcnow(),
        )

    return c2


def candidate_p2p_create_or_update(ip_address, payload_ids, heuristics, nodes):
    p2p = None

    try:
        p2p = CandidateP2pNode(
            ip_address=ip_address,
            payloads=payload_ids,
            heuristics=heuristics,
            nodes=nodes,
        )
        p2p.save()
    except (NotUniqueError, DuplicateKeyError):
        p2p = CandidateP2pNode(ip_address=ip_address).first()
        p2p.update(
            add_to_set__payloads=payload_ids,
            add_to_set__heuristics=heuristics,
            add_to_set__nodes=nodes,
            inc__occurrences=1,
            set__updated_at=datetime.utcnow(),
        )

    return p2p


def lisa_analysis_create_or_update(lisa_analysis):
    lisa = None

    try:
        lisa = LisaAnalysis(**lisa_analysis)
        lisa.save()
    except  (NotUniqueError, DuplicateKeyError):
        lisa = LisaAnalysis.objects(task_id=lisa_analysis['task_id']).first()

    return lisa


def geo_connections_create_or_update(source_ip, destination_ip):
    conn = None

    try:
        conn = IpGeoConnection(
            source_ip=source_ip,
            destination_ip=destination_ip
        )
        conn.save()
    except (NotUniqueError, DuplicateKeyError):
        s_ip = source_ip.ip_address if source_ip.ip_address else source_ip
        d_ip = destination_ip.ip_address if destination_ip.ip_address else destination_ip
    
        conn = IpGeoConnection.objects(
            source_ip=s_ip,
            destination_ip=d_ip
        ).first()

        conn.update(
            inc__occurrences=1
        )
    return conn
