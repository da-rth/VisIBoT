import mongoengine as mongo
from mongoengine.errors import NotUniqueError
from datetime import datetime


high_tier_server_types = [
    "C2 Server",
    "Loader Server",
]


class GeoData(mongo.Document):
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
            "Loader Server",
            "Report Server",
            "Bot",
            "Unknown"
        ]
    )


class Payload(mongo.Document):
    """
    Malware payload information retrieved from BadPackets results
    """
    url               = mongo.StringField(required=True, primary_key=True)
    occurrences       = mongo.IntField(default=0)
    lisa              = mongo.DictField(required=False)
    ip_address        = mongo.ReferenceField(GeoData, required=True)
    updated_at        = mongo.DateTimeField(default=datetime.utcnow)
    candidate_C2s     = mongo.ListField(mongo.ReferenceField(GeoData, required=False), required=False, default=[])


class CandidateC2Server(mongo.Document):
    """
    Candidate C2 Server extracted from network analysis of malware extracted from a payload
    """
    ip_address        = mongo.ReferenceField(GeoData, required=True)
    payloads          = mongo.ListField(mongo.ReferenceField(Payload, required=False), required=False)
    heuristics        = mongo.ListField(mongo.StringField())
    occurrences       = mongo.IntField(default=0)
    updated_at        = mongo.DateTimeField(default=datetime.utcnow)


class Result(mongo.Document):
    """
    BadPackets Result JSON information
    """
    event_id          = mongo.StringField(required=True, primary_key=True)
    source_ip_address = mongo.ReferenceField(GeoData, required=True)
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
    scanned_urls      = mongo.ListField(mongo.ReferenceField(Payload, required=False), required=False)
    affiliated_ips    = mongo.ListField(mongo.ReferenceField(GeoData, required=False), required=False)
    updated_at        = mongo.DateTimeField(default=datetime.utcnow)


def payload_create_or_update(url, ip):
    try:
        payload = Payload(
            url=url,
            ip_address=ip
        )
        payload.save()
    except NotUniqueError:
        payload = Payload.objects(url=url).first()
        payload.update(
            set__updated_at=datetime.utcnow(),
            inc__occurrences=1
        )
    return payload


def result_create_or_update(event_id, result_data):
    try:
        result = Result(**result_data)
        result.save()
    except (NotUniqueError, mongo.DuplicateKeyError):
        result = Result.objects(event_id=event_id).first()
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
        geodata = GeoData(
            ip_address=ip,
            hostname=hostname,
            server_type=server_type,
            data=geodata,
            tags=flattened_tags if tags else {},
        )
        geodata.save()
    except NotUniqueError:
        geodata = GeoData.objects(ip_address=ip).first()

        loader_to_c2 = (
            geodata.server_type == "Loader Server" and
            server_type == "C2 Server"
        )

        bot_to_report_server = (
            geodata.server_type in ["Bot", "Unknown"] and
            server_type == "Report Server"
        )

        low_tier_to_high_tier = (
            geodata.server_type in ["Report Server", "Bot", "Unknown"] and
            server_type in ["C2 Server", "Loader Server"]
        )

        if not (loader_to_c2 or bot_to_report_server or low_tier_to_high_tier):
            server_type = geodata.server_type

        updated_tags = geodata.tags.copy()

        for k, v in updated_tags.items():
            updated_tags[k] = set(v)

        for tag in tags:
            updated_tags['cves'].add(tag['cve'])
            updated_tags['categories'].add(tag['category'])
            updated_tags['descriptions'].add(tag['description'])

        geodata.update(
            set__tags=updated_tags,
            set__updated_at=datetime.utcnow(),
            set__server_type=server_type,
            inc__occurrences=1
        )
    return geodata


def candidate_c2_create_or_update(ip_address, payload_ids, heuristics):
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
