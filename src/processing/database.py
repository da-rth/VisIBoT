import mongoengine as mongo
from mongoengine.errors import NotUniqueError
from datetime import datetime


class IpGeoData(mongo.Document):
    """
    Server/IP Address information pulled from payload data of
    BadPackets results
    """
    ip_address        = mongo.StringField(required=True, primary_key=True)
    occurrences       = mongo.IntField(default=0)
    updated_at        = mongo.DateTimeField(default=datetime.utcnow)
    data              = mongo.DictField(required=True)
    hostname          = mongo.StringField(required=False)
    tags              = mongo.DictField(required=False)
    server_type       = mongo.StringField(
        required=True,
        choices=[
            "C2 Server",
            "P2P Node",
            "Loader Server",
            "Report Server",
            "Malicious Bot",
            "Bot",
            "Unknown"
        ]
    )


class IpGeoConnection(mongo.Document):
    """
    OneToMany Document containing all connections between one IpGeoData Object and various others
    """
    source_ip         = mongo.ReferenceField(IpGeoData, required=True)
    destination_ip    = mongo.ReferenceField(IpGeoData, unique=True)


class MalwarePayload(mongo.Document):
    """
    Malware payload information retrieved from BadPackets results
    """
    url               = mongo.StringField(required=True, primary_key=True)
    occurrences       = mongo.IntField(default=0)
    lisa              = mongo.ReferenceField('LisaAnalysis', required=False)
    ip_address        = mongo.ReferenceField(IpGeoData, required=True)
    updated_at        = mongo.DateTimeField(default=datetime.utcnow)
    candidate_C2s     = mongo.ListField(mongo.ReferenceField(IpGeoData, required=False), required=False, default=[])
    candidate_P2Ps    = mongo.ListField(mongo.ReferenceField(IpGeoData, required=False), required=False, default=[])


class LisaAnalysis(mongo.DynamicDocument):
    """
    Malware binary information obtained from LiSa Sandbox
    """
    task_id           = mongo.StringField(required=True, primary_key=True)
    payload           = mongo.ReferenceField(MalwarePayload, required=True)


class CandidateC2Server(mongo.Document):
    """
    Candidate C2 Server extracted from network analysis of malware extracted from a payload
    """
    ip_address        = mongo.ReferenceField(IpGeoData, required=True)
    payloads          = mongo.ListField(mongo.ReferenceField(MalwarePayload, required=False), required=False)
    heuristics        = mongo.ListField(mongo.StringField())
    occurrences       = mongo.IntField(default=0)
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
    updated_at        = mongo.DateTimeField(default=datetime.utcnow)


def payload_create_or_update(url, ip, lisa=None, candidate_C2s=[], candidate_P2Ps=[]):
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


def result_create_or_update(event_id, result_data):
    try:
        result = BadpacketsResult(**result_data)
        result.save()
    except NotUniqueError:
        result = BadpacketsResult.objects(event_id=event_id).first()
        result.update(
            add_to_set__scanned_payloads=result_data['scanned_payloads'],
            set__updated_at=datetime.utcnow()
        )
    return result


def geodata_create_or_update(ip, hostname, server_type, geodata, tags=[]):
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
        geodata = IpGeoData(
            ip_address=ip,
            hostname=hostname,
            server_type=server_type,
            data=geodata,
            tags=flattened_tags if tags else {}
        )
        geodata.save()
    except NotUniqueError:
        geodata = IpGeoData.objects(ip_address=ip).first()

        loader_to_c2_p2p = (
            geodata.server_type == "Loader Server" and
            (server_type == "C2 Server" or server_type == "P2P Node")
        )

        report_to_loader = (
            geodata.server_type in ["Report Server", "Malicious Bot"] and
            server_type == "Loader Server"
        )

        bot_to_report = (
            geodata.server_type in ["Bot", "Unknown"] and
            server_type == "Report Server" or server_type == "Malicious Bot"
        )

        low_to_high = (
            geodata.server_type in ["Report Server", "Malicious Bot", "Bot", "Unknown"] and
            server_type in ["C2 Server", "P2P Node", "Loader Server"]
        )

        if not (loader_to_c2_p2p or report_to_loader or bot_to_report or low_to_high):
            server_type = geodata.server_type

        if 'cves' in geodata.tags:
            n_tags = geodata.tags.copy()

            for k, v in n_tags.items():
                n_tags[k] = set(v)

            n_tags['cves'].update(flattened_tags['cves'])
            n_tags['categories'].update(flattened_tags['categories'])
            n_tags['descriptions'].update(flattened_tags['descriptions'])
        else:
            n_tags = flattened_tags

        geodata.update(
            set__tags=n_tags,
            set__updated_at=datetime.utcnow(),
            set__server_type=server_type,
            inc__occurrences=1
        )
    return geodata


def candidate_cnc_create_or_update(ip_address, payload_ids, heuristics):
    try:
        c2 = CandidateC2Server(
            ip_address=ip_address,
            payloads=payload_ids,
            heuristics=heuristics
        )
        c2.save()
    except NotUniqueError:
        c2 = CandidateC2Server(ip_address=ip_address).first()
        c2.update(
            add_to_set__payloads=payload_ids,
            add_to_set__heuristics=heuristics,
            inc__occurrences=1,
            set__updated_at=datetime.utcnow(),
        )
    return c2


def candidate_p2p_create_or_update(ip_address, payload_ids, heuristics, nodes):
    try:
        p2p = CandidateP2pNode(
            ip_address=ip_address,
            payloads=payload_ids,
            heuristics=heuristics,
            nodes=nodes,
        )
        p2p.save()
    except NotUniqueError:
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
    try:
        lisa = LisaAnalysis(**lisa_analysis)
        lisa.save()
    except NotUniqueError:
        lisa = LisaAnalysis.objects(task_id=lisa_analysis['task_id']).first()
    return lisa


def geo_connections_create_or_update(source_ip, destination_ip):
    try:
        conn = IpGeoConnection(
            source_ip=source_ip,
            destination_ip=destination_ip
        )
        conn.save()
    except NotUniqueError:
        conn = IpGeoConnection.objects(source_ip=source_ip).first()
    return conn
