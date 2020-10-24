from mongoengine import connect, Document, StringField, ListField
from mongoengine import IntField, URLField, DateTimeField, DictField
from mongoengine import ReferenceField
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv(verbose=True)

database = connect(host=os.getenv("MONGODB_URL"))

class GeoData(Document):
    """
    Server/IP Address information pulled from payload data of
    BadPackets results
    """
    ip_address = StringField(required=True, primary_key=True)
    updated_at = DateTimeField(default=datetime.utcnow)
    data = DictField(required=True)
    server_type = StringField(required=True, choices=[
        "C2 Server",
        "Loader Server",
        "Report Server",
        "Bot"
    ])


class Payload(Document):
    """
    Malware payload information retrieved from BadPackets results
    """
    payload_url = URLField(required=True, primary_key=True)
    vt_scan_url = URLField(required=True)
    ip_address = StringField(required=True)
    updated_at = DateTimeField(default=datetime.utcnow)


class Result(Document):
    """
    BadPackets Result JSON information
    """
    event_id = StringField(required=True, primary_key=True)
    source_ip_address = StringField(required=True)
    country = StringField(required=True, max_length=4)
    user_agent = StringField(required=True)
    payload = StringField(required=True)
    post_data = StringField(required=True)
    target_port = IntField(required=True)
    protocol = StringField(required=True)
    event_count = IntField(required=True)
    first_seen = StringField(required=True)
    last_seen = StringField(required=True)
    tags = ListField(DictField(required=True), required=True)
    payload_urls = ListField(ReferenceField(Payload))
    updated_at = DateTimeField(default=datetime.utcnow)
    


