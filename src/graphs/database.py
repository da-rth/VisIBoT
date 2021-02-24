import mongoengine as mongo
from datetime import datetime

mongo.connect(host='MONGODB_URI_HERE')

geo_hierarchy = {
    "C2 Server": 5,
    "P2P Node": 4,
    "Payload Server": 3,
    "Report Server": 2,
    "Malicious Bot": 1,
    "Bot": 0
}


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
    ip_info           = mongo.ReferenceField('IpInfo', required=False)
    asn               = mongo.ReferenceField(AutonomousSystem, required=False)
    prev_asns         = mongo.ListField(mongo.DictField(required=False), default=[])
    occurrences       = mongo.IntField(default=0)
    data              = mongo.DictField(required=True)
    hostname          = mongo.StringField(required=False)
    tags              = mongo.DictField(required=False)
    server_type       = mongo.StringField(required=True, choices=list(geo_hierarchy.keys()))
    created_at        = mongo.DateTimeField(default=datetime.utcnow)
    updated_at        = mongo.DateTimeField(default=datetime.utcnow)


class IpInfo(mongo.DynamicDocument):
    """
    API Query results from ipinfo.io
    """
    ip_address        = mongo.ReferenceField(IpGeoData, required=True, reverse_delete_rule=mongo.CASCADE)
    created_at        = mongo.DateTimeField(default=datetime.utcnow)
    updated_at        = mongo.DateTimeField(default=datetime.utcnow)


class IpGeoConnection(mongo.Document):
    """
    Document containing all connections between one IpGeoData Object and various others
    """
    source_ip         = mongo.ReferenceField(IpGeoData, required=True, reverse_delete_rule=mongo.CASCADE)
    destination_ip    = mongo.ReferenceField(IpGeoData, required=True, reverse_delete_rule=mongo.CASCADE)
    occurrences       = mongo.IntField(default=1)
    created_at        = mongo.DateTimeField(default=datetime.utcnow)
    updated_at        = mongo.DateTimeField(default=datetime.utcnow)
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
    keyword           = mongo.StringField(required=False)
    ip_address        = mongo.ReferenceField(IpGeoData, required=True, reverse_delete_rule=mongo.CASCADE)
    is_self_hosted    = mongo.BooleanField(required=True, default=False)
    candidate_C2s     = mongo.ListField(
        mongo.ReferenceField(IpGeoData, required=False, reverse_delete_rule=mongo.CASCADE),
        default=[]
    )
    candidate_P2Ps    = mongo.ListField(
        mongo.ReferenceField(IpGeoData, required=False, reverse_delete_rule=mongo.CASCADE),
        default=[]
    )
    created_at        = mongo.DateTimeField(default=datetime.utcnow)
    updated_at        = mongo.DateTimeField(default=datetime.utcnow)


class LisaAnalysis(mongo.DynamicDocument):
    """
    Malware binary information obtained from LiSa Sandbox
    """
    task_id           = mongo.StringField(required=True, primary_key=True)
    payload           = mongo.ReferenceField(MalwarePayload, required=True, reverse_delete_rule=mongo.CASCADE)
    created_at        = mongo.DateTimeField(default=datetime.utcnow)

