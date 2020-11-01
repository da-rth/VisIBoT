from mongoengine import Document, StringField, ListField
from mongoengine import IntField, DateTimeField, DictField
from mongoengine import ReferenceField
from datetime import datetime
import os


class GeoData(Document):
    """
    Server/IP Address information pulled from payload data of
    BadPackets results
    """
    ip_address = StringField(required=True, primary_key=True)
    updated_at = DateTimeField(default=datetime.utcnow)
    data = DictField(required=True)
    hostname = StringField(required=False)
    server_type = StringField(required=True, choices=[
        "C2 Server",
        "Loader Server",
        "Report Server",
        "Bot",
        "Unknown"
    ])


class Payload(Document):
    """
    Malware payload information retrieved from BadPackets results
    """
    url = StringField(required=True, unique=True)
    scan_url = StringField(required=True)
    ip_address = ReferenceField(GeoData, required=True)
    updated_at = DateTimeField(default=datetime.utcnow)


class Result(Document):
    """
    BadPackets Result JSON information
    """
    event_id = StringField(required=True, primary_key=True)
    source_ip_address = ReferenceField(GeoData, required=True)
    country = StringField(required=True, max_length=4)
    user_agent = DictField(required=True)
    payload = StringField(required=True)
    post_data = StringField(required=True)
    target_port = IntField(required=True)
    protocol = StringField(required=True)
    event_count = IntField(required=True)
    first_seen = StringField(required=True)
    last_seen = StringField(required=True)
    tags = ListField(DictField(required=True), required=True)
    scanned_payloads = ListField(ReferenceField(Payload, required=False), required=False)
    updated_at = DateTimeField(default=datetime.utcnow)


def payload_create_or_update(url, vt_result, ip, now):
    try:
        payload = Payload(
            url=url,
            vt_result=vt_result,
            ip_address=ip,
            updated_at=now
        )
        payload.save()
    except NotUniqueError:
        payload_geodata = Payload.objects(url=url).first()
        payload_geodata.updated_at = now
        payload_data.save()

    return payload


def result_create_or_update(event_id, result_data, now):
    try:
        result = Result(**result_data)
        result.save()
    except (NotUniqueError, DuplicateKeyError):
        result = Result.objects(event_id=event_id).first()
        result.updated_at = now
        result.save()

    return result


def geodata_create_or_update(ip, hostname, server_type, geodata):
    try:
        geodata = GeoData(
            ip_address=ip,
            hostname=hostname,
            server_type=server_type,
            data=geodata,
        )
        geodata.save()
    except NotUniqueError:
        geodata = GeoData.objects(ip_address=ip).first()
        geodata.updated_at = now
        geodata.save()

    return geodata
