from ipwhois.net import Net
from ipwhois.asn import IPASN, ASNOrigin
from datetime import datetime


def is_valid_origin(origin):
    return origin['updated'] and not origin['description'].startswith('Temporary holder')


def parse_origin_asn(origin):
    updated = origin['updated']
    updated = updated.split('@')[1] if '@' in updated else updated

    try:
        updated_by, updated_time = updated.split(' ', 1)
    except ValueError:
        return

    updated_time_fmt = None

    if ' # ' in updated_time:
        updated_time_fmt = datetime.strptime(updated_time.split("# ")[1], '%Y-%m-%d %H:%M:%S %z')

    elif updated_time.split(' ', 1)[0].isdigit():
        if '#' in updated_time:
            updated_time_fmt = datetime.strptime(updated_time, '%Y%m%d  #%H:%M:%S%z')
        else:
            updated_time_fmt = datetime.strptime(updated_time, '%Y%m%d')

    if updated_time_fmt:
        return {
            'cidr': origin['cidr'],
            'description': origin['description'],
            'maintainer': origin['maintainer'],
            'source': origin['source'],
            'updated_by': updated_by,
            'updated_time': updated_time_fmt,
        }


def get_asn_info(ip):
    net = Net(ip)
    ip_asn = IPASN(net).lookup()

    if ip_asn['asn_date']:
        ip_asn['asn_date'] = datetime.strptime(ip_asn['asn_date'], '%Y-%m-%d')
    else:
        ip_asn['asn_date'] = None
    
    return ip_asn if ip_asn['asn'] else None


def get_asn_origins(ip):
    net = Net(ip)
    ip_asn = IPASN(net).lookup()
    asn_origin_lookup = ASNOrigin(net).lookup(asn=ip_asn['asn'])

    ip_asn_origins = [o for o in asn_origin_lookup['nets'] if is_valid_origin(o)]
    ip_asn_origins = ip_asn_origins[-10:] if len(ip_asn_origins) > 10 else ip_asn_origins
    ip_asn_origins = [parse_origin_asn(origin) for origin in ip_asn_origins if origin]

    return ip_asn_origins