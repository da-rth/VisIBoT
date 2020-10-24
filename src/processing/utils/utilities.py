import re
import validators
from urllib.parse import urlparse
import socket


BAD_IPS = ['0.0.0.0', socket.gethostbyname('some.bad.ip')]
URL_REGEX = r'(ftp|https?):\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
IPv4_REGEX = r'[0-9]+(?:\.[0-9]+){3}'
IPv6_REGEX = r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'


def url_parser(input_str):
    """The provided string is
    - encoded and decoded to escape any unicode used for obfuscation
    - stripped of any backslashes
    And is searched with a URL regular expression which accepts ftp/http/https URLs

    Args:
        input_str (String): A string to be parsed for any URLs

    Returns:
        list : A list of string URLs
    """
    input_strs = input_str.replace("\\/", "/").encode().decode('unicode_escape').replace('\\','').split(';')
    urls = []
    for s in input_strs:
        url = re.search(URL_REGEX, s)
        if url:
            urls.append(url.group())
    return urls


def ip_parser(input_str):
    address = re.search(IPv4_REGEX, input_str)
    return address.group() if address else None


def ipv6_parser(input_str):
    address = re.search(IPv6_REGEX, input_str)
    return address.group() if address else None


def validate_url(url):
    """Determines if a given URL is valid:
    - hostname is legal and points to real IP
    - ip is legal and points to some hostname

    Args:
        url (String): The URL to be validated

    Returns:
        Bool: False is returned if URL is invalid
        Tuple: (ip, hostname) of URL is returned if valid
    """
    host = urlparse(url).hostname
    ip = ip_parser(url)

    if ip:
        try:
            host = socket.gethostbyaddr(ip)[0]
        except (IndexError, socket.herror):
            return False
    
    elif validators.domain(host):
        ip = socket.gethostbyname(host)
        if ip in BAD_IPS:
            return False
    
    return (host, ip) if host and ip else False



