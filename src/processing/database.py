from mongoengine import connect, Document, StringField
from mongoengine import IntField, URLField, DateTimeField, DictField
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv(verbose=True)

connect(host=os.getenv("MONGODB_URL"))


class BadPacketsResult(Document):
    """
    BadPackets Result JSON information
    """
    event_id = StringField(required=True, primary_key=True, unique=True)
    source_ip_address = StringField(required=True)
    country = StringField(required=True, max_length=4)
    user_agent = StringField(required=True)
    payload = StringField(required=True)
    post_data = StringField(required=True)
    target_port = IntField(required=True)
    protocol = StringField(required=True)
    event_count = IntField(required=True)
    first_seen = DateTimeField(required=True)
    last_seen = DateTimeField(required=True)

    meta = {
        "indexes": ["event_id"],
    }


class BadPacketsIPAddress(Document):
    """
    Server/IP Address information pulled from payload data of
    BadPackets results
    """
    ip_address = StringField(required=True, primary_key=True, unique=True)
    ip_geodata = DictField(required=True)
    vt_ip_url = URLField()
    domain = StringField()
    last_seen = DateTimeField(default=datetime.utcnow)
    server_type = StringField(required=True, choices=[
        "C2",
        "Loader",
        "Report",
        "Bot"
    ])

    meta = {
        "indexes": ["ip_address", "server_type"],
    }


class BadPacketsPayload(Document):
    """
    Malware payload information retrieved from BadPackets results
    """
    bp_event_id = StringField(required=True, primary_key=True, unique=True)
    ip_address = StringField(required=True)
    payload_url = URLField(required=True)
    virustotal_url = URLField(required=True)

    meta = {
        "indexes": ["bp_event_id", "ip_address"],
    }


class BadPacketsTag(Document):
    """
    BadPackets tag for a given API result
    """
    bp_event_id = StringField(required=True, primary_key=True, unique=True)
    cve = StringField()
    category = StringField()
    description = StringField()
