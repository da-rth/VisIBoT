import re
import os
import validators
import socket
import user_agents
from datetime import datetime
from urllib.parse import urlparse

URL_REGEX = r'((ftp|https?):\/\/(www\.)?)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
IPv4_REGEX = r'[0-9]+(?:\.[0-9]+){3}'
IPv6_REGEX = r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'


def url_parser(input_str):
    """
    The provided string is
    - encoded and decoded to escape any unicode used for obfuscation
    - stripped of any backslashes
    And is searched with a URL regular expression which accepts ftp/http/https URLs

    Args:
        input_str (str): A string to be parsed for any URLs

    Returns:
        list: A list of string URLs
    """
    input_strs = input_str.replace("\\/", "/") \
        .encode() \
        .decode('unicode_escape') \
        .replace('\\', '') \
        .split(';')

    urls = []
    for s in input_strs:
        url = re.search(URL_REGEX, s)
        if url:
            if len(url.group()) > 4:
                urls.append(url.group())
    return urls


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
    try:
        return socket.gethostbyaddr(ip)[0]
    except (IndexError, socket.herror):
        return None


def validate_url(url):
    """
    Determines if a given URL is valid:
    - hostname is legal and points to real IP
    - ip is legal and points to some hostname

    Args:
        url (str): The URL to be validated

    Returns:
        None: False is returned if URL is invalid
        tuple: (ip, hostname) of URL is returned if valid
    """
    host = urlparse(url).hostname
    ip = ip_parser(url)

    if ip:
        try:
            host = socket.gethostbyaddr(ip)[0]
        except (IndexError, socket.herror):
            return None

    elif validators.domain(host):
        ip = socket.gethostbyname(host)
        print(ip)

    return (url, host, ip) if host and ip else None


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
