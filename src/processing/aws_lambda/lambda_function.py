import re
import json
import requests
import validators
import tldextract
from tld import is_tld
from urllib.parse import unquote
from contextlib import suppress

# pylama:ignore=W605

"""

https://github.com/fireeye/stringsifter/blob/master/stringsifter/flarestrings.py

"""

ASCII_BYTE = b" !\"#\$%&\'\(\)\*\+,-\./0123456789:;<=>\?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^_`abcdefghijklmnopqrstuvwxyz\{\|\}\\\~\t"

IGNORE_TLDS = ["org", "edu", "gov", "arpa", "mil", "int", "arpa", "sh"]


def remove_noise(s):
    """
    Replaces annoying substrings with space characters

    Args:
        s (str): The string to be filtered from noise

    Returns:
        str: The string with noise removed
    """
    for x in [";", "${IFS}", "\"", "'", "`", "+"]:
        if x in s:
            s = s.replace(x, " ")
    return s


def get_strings(b, min_len=8):
    """[summary]

    Args:
        filename ([type]): [description]
        min_len (int, optional): [description]. Defaults to 8.

    Returns:
        [type]: [description]
    """
    re_narrow = re.compile(b'([%s]{%d,})' % (ASCII_BYTE, min_len))
    re_wide = re.compile(b'((?:[%s]\x00){%d,})' % (ASCII_BYTE, min_len))

    strings = []

    for match in re_narrow.finditer(b):
        string = match.group().decode('ascii')
        strings.append(unquote(string))

    for match in re_wide.finditer(b):
        with suppress(UnicodeDecodeError):
            string = match.group().decode('utf-16')
            strings.append(unquote(string))

    return strings


def valid_tld(domain_or_url):
    tlde = tldextract.extract(domain_or_url)
    top_level_domain = tlde.suffix

    if validators.ip_address.ipv4(tlde.domain):
        return True

    return is_tld(top_level_domain) and top_level_domain not in IGNORE_TLDS


def get_hosts(strings):
    strings = remove_noise(" ".join(strings))
    ips, urls, domains = [], [], []

    for s in strings.split(" "):
        if validators.ip_address.ipv4(s):
            ips.append(s)
        elif validators.url(s) and valid_tld(s):
            urls.append(s)
        elif validators.domain(s) and valid_tld(s):
            domains.append(s)

    return {
        "ips": list(set(ips)),
        "urls": list(set(urls)),
        "domains": list(set(domains))
    }


def response(code, body):
    """
    Creates a dictionary JSON response of given message and http code
    """
    return {
        'statusCode': 400,
        'body': json.dumps(body)
    }


def perform_analysis(url, get_all_strings=False):
    if not url:
        return response(400, {"msg": "Requst is missing the 'url' query parameter."})
    try:
        with requests.get(url, timeout=1) as r:
            if r.status_code == 200:
                strings = get_strings(r.content)
                body = strings if get_all_strings else get_hosts(strings)
                return response(200, body)
            else:
                return response(400, {"msg": "Website responded with code: "+r.status_code})
    except requests.exceptions.MissingSchema:
        return response(400, {"msg": "No URL Schema supplied e.g. http://"})
    except Exception as e:
        return response(400, {"msg": str(e)})


def lambda_handler(event=None, context=None):
    query_params = event.get('queryStringParameters', None)
    if query_params:
        url = query_params.get("url", None)
        get_all_strings = query_params.get("all_strings", False) == "true"
        return perform_analysis(url, get_all_strings)
    else:
        return response(400, {"msg": "Please include the 'url' query parameter in the request."})
