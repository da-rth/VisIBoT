import re
import os
import validators
import socket
import user_agents
import tldextract
from tld import is_tld
from datetime import datetime
from urllib.parse import urlparse, unquote
from urlextract import URLExtract
from contextlib import suppress

extractor = URLExtract()

IGNORE_TLDS = ["org", "edu", "gov", "arpa", "mil", "int", "arpa", "sh"]
URL_REGEX = r'(ftp|https?):\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
IPv4_REGEX = r'[0-9]+(?:\.[0-9]+){3}'
IPv6_REGEX = r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'


def parse_wget_payload(payload_str):
    """
    Extracts URL information by working around busybox wget obfuscation method
    """
    with suppress(IndexError, ValueError):
        payload_lst = payload_str.split(" ")
        if all(arg in payload_lst for arg in ["wget", "-g", "-r"]):
            wget_idx = payload_lst.index("wget")
            end_idx = payload_lst[wget_idx:].index(";")
            wget_cmd = payload_lst[wget_idx:wget_idx+end_idx]

            host = wget_cmd[wget_cmd.index('-g')+1]
            path = wget_cmd[wget_cmd.index('-r')+1]
            return f"http://{host}{path}"


def parse_curl_payload(payload_str):
    """
    Extracts URL information by working around busybox wget obfuscation method
    """
    with suppress(IndexError):
        payload_lst = payload_str.split(" ")
        if all(arg in payload_str for arg in ["curl", "-O"]):
            url = payload_lst[payload_lst.index("-O")+1]
            return f"http://{url}" if not url.startswith("http") else url


def regex_url_parser(data):
    """Searches a string of data for a URL  using regular expression

    Args:
        s (str): A string to be parsed for any URLs

    Returns:
        list: A list of string URLs
    """
    urls = []
    for segment in data.split(";"):
        url = re.search(URL_REGEX, segment)
        if url and len(url.group()) > 4:
            urls.append(url.group())
    return urls


def remove_noise(s):
    """
    Replaces annoying substrings with space characters

    Args:
        s (str): The string to be filtered from noise

    Returns:
        str: The string with noise removed
    """
    if ";" in s:
        s = s.replace(";", " ; ")

    for x in ["${IFS}", "\"", "'", "`", "+"]:
        if x in s:
            s = s.replace(x, " ")

    return s


def valid_tld(domain_or_url):
    tlde = tldextract.extract(domain_or_url)
    top_level_domain = tlde.suffix

    if validators.ip_address.ipv4(tlde.domain):
        return True

    return is_tld(top_level_domain) and top_level_domain not in IGNORE_TLDS


def url_parser(data):
    """
    The provided string is
    - encoded and decoded to escape any unicode used for obfuscation
    - stripped of any backslashes
    - searched with urlextract
        - if no urls are found, search using regular expression

    Args:
        s (str): A string to be parsed for any URLs

    Returns:
        list: A list of string URLs
    """
    urls = set()
    data = remove_noise(unquote(data))

    extracted_urls = [url for url in extractor.find_urls(data) if valid_tld(url)]

    if extracted_urls:
        urls.update([f'http://{url}' if not url.startswith("http") else url for url in extracted_urls])
    else:
        wget_url = parse_wget_payload(data)
        curl_url = parse_curl_payload(data)

        if wget_url or curl_url:
            if wget_url and valid_tld(wget_url):
                urls.add(wget_url)
            if curl_url and valid_tld(curl_url):
                urls.add(curl_url)
        else:
            regex_urls = regex_url_parser(data)
            urls.update([url for url in regex_urls if valid_tld(url)])

    # Remove duplicate URLs and validate TLD
    return [url for url in urls if valid_tld(url)]


def ip_parser(input_str):
    """
    Parses an input string for an IPv4 address

    Args:
        input_str (str): An input string which may
            contain an IPv4 address.

    Returns:
        str: IPv4 Address
    """
    address = re.search(IPv4_REGEX, input_str)
    return address.group() if address else None


def ipv6_parser(input_str):
    """
    Parses an input string for an IPv6 address

    Args:
        input_str (str): An input string which may
        contain an IPv6 address.

    Returns:
        str: IPv6 Address
    """
    address = re.search(IPv6_REGEX, input_str)
    return address.group() if address else None


def useragent_parser(ua_str):
    """
    Given a user-agent input string, a dictionary containing
    information about the agent OS, browser and device is returned.

    If user-agent is invalid, dict will contain null results.

    Args:
        ua_str (str): The user-agent string to be parsed

    Returns:
        dict: contains organised info of user-agent in dict format
    """
    user_agent = user_agents.parse(ua_str)

    return {
        "str": ua_str,
        "browser": {
            "family": user_agent.browser.family,
            "version": user_agent.browser.version_string
        },
        "os": {
            "family": user_agent.os.family,
            "version": user_agent.os.version_string
        },
        "device": {
            "family": user_agent.device.family,
            "brand": user_agent.device.brand,
            "model": user_agent.device.model
        }
    }


def get_ip_hostname(ip):
    """
    Returns the hostname of a given IP address

    Args:
        ip (str): A string containing an IP address

    Returns:
        str: The hostname of the IP address
        None: If no hostname was found
    """
    with suppress(Exception):
        return socket.gethostbyaddr(ip)[0]


def validate_url(url):
    """
    Determines if a given URL is valid:
    - hostname in URL is legal and points to real IP
    - ip in URL is alive and points to some hostname

    Args:
        url (str): The URL to be validated

    Returns:
        None: False is returned if URL is invalid
        tuple: (ip, hostname) of URL is returned if valid
    """
    host = urlparse(url).hostname

    with suppress(Exception):
        if validators.domain(host):
            return (url, host, socket.gethostbyname(host))
        else:
            return (url, socket.gethostbyaddr(host)[0], host)


def time_until(next_mins):
    """
    Given N minutes, this function calculates the
    timestamp (in UTC) when the Nth minute next occurs.

    Example: If the time is 16:43:02 and we run time_until(15)
    the string 17:15:00 will be returned.

    Args:
        next_mins (int): The number of minutes past the hour to
            get next timestamp for.

    Returns:
        str: a string timestamp (UTC) in format HH:MM:SS
    """
    now_dt = datetime.utcnow()

    if now_dt.minute >= next_mins:
        next_dt = now_dt.replace(second=0, minute=next_mins, hour=now_dt.hour+1)
    else:
        next_dt = now_dt.replace(second=0, minute=next_mins)

    return next_dt.strftime('%H:%M:%S')


def clear():
    """
    Checks OS type and clears console accordingly
    """
    os.system('cls' if os.name == 'nt' else 'clear')
