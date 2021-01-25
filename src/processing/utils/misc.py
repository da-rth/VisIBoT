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
from utils.tor_session import session

extractor = URLExtract()
VALID_SCHEMAS = ["tftp", "ftp", "http", "https", "sftp"]
IGNORE_TLDS = ["edu", "gov", "mil", "int", "arpa", "sh"]
URL_REGEX = r'(ftp|https?):\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
IPv4_REGEX = r'[0-9]+(?:\.[0-9]+){3}'
IPv6_REGEX = r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'


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
        hour = now_dt.hour+1
        hour = hour if hour < 23 else 0
        next_dt = now_dt.replace(second=0, minute=next_mins, hour=hour)
    else:
        next_dt = now_dt.replace(second=0, minute=next_mins)

    return next_dt.strftime('%H:%M:%S')


def clear():
    """
    Checks OS type and clears console accordingly
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def url_builder(host, port=None, path=None):
    if any(host.startswith(s) for s in VALID_SCHEMAS):
        url = host
    else:
        url = f"http://{host}"

    if port and ":" not in host:
        if host.endswith("/"):
            url += f":{port}/"
        else:
            url += f":{port}"

    if path:
        if url.endswith("/") or path.startswith("/"):
            url += path
        else:
            url += f"/{path}"

    return url


def is_host_valid(host):
    return validators.ip_address.ipv4(host) or validators.domain(host) or validators.url(host)


def build_command_urls(payload_str):
    """
    Extracts URL information by working around busybox wget obfuscation method
    """
    urls = set()
    cmds = ['wget', 'curl', 'tftp']
    commands = [ln for ln in payload_str.split(";") if any(ln.startswith(cmd) for cmd in cmds)]

    for cmd in commands:
        args = cmd.lstrip(" ").split(" ")
        host, port, path = '', None, None

        with suppress(IndexError, ValueError, StopIteration):
            host = next(arg for arg in args if is_host_valid(arg))

            if cmd.startswith("wget"):
                host = args[args.index('-g')+1]
                path = args[args.index('-r')+1]

            elif cmd.startswith("curl"):
                host = args[args.index("-O")+1]

            elif cmd.startswith("tftp"):
                with suppress(StopIteration):
                    port = next(arg for arg in args[args.index(host):] if arg.isdigit())

                with suppress(IndexError):
                    if "-g" in args:
                        host = args[args.index('-g')+1]
                    if "-r" in args:
                        path = args[args.index("-r")+1]
                    elif "get" in args:
                        path = args[args.index("get")+1]

            if is_host_valid(host):
                url = url_builder(host, port, path)
                urls.add(url)

    return list(urls)


def parse_regex_urls(data):
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
    if "\\/" in s:
        s = s.replace("\\/", "/")

    for x in ["nohup", "(", ")"]:
        if x in s:
            s = s.replace(x, '')

    for x in ["${IFS}", "\"", "'", "`", "+"]:
        if x in s:
            s = s.replace(x, " ")

    for x in ["||", "&&", "&"]:
        if x in s:
            s = s.replace(x, ";")

    return s


def valid_tld(domain_or_url):
    tlde = tldextract.extract(domain_or_url)

    if validators.ip_address.ipv4(tlde.domain):
        return True

    return is_tld(tlde.suffix) and tlde.suffix not in IGNORE_TLDS


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
    - domain in URL is legitimate and points to real IP
    - IP address in URL is alive and points to some hostname

    Args:
        url (str): The URL to be validated

    Returns:
        None: False is returned if URL is invalid
        tuple: (url, ip, hostname) is returned if URL is valid
    """
    ignore_exts = [".png", ".jpg", ".jpeg", ".html", ".xml"]

    if any(url.lower().endswith(s) for s in ignore_exts):
        return None

    host = urlparse(url).hostname

    if not host:
        return None

    hostname, address = None, None

    if validators.ip_address.ipv4(host):
        with suppress(Exception):
            hostname = socket.gethostbyaddr(host)[0]
        return (url, host, hostname)

    elif validators.domain(host):
        with suppress(Exception):
            address = socket.gethostbyname(host)

        if address:
            return (url, address, host)

    else:
        return None


def extract_urls(data):
    data = remove_noise(unquote(data))
    urls_set = set()
    urls_list = []

    urls_set.update(extractor.find_urls(data))
    urls_set.update(build_command_urls(data))
    urls_set.update(parse_regex_urls(data))

    for url in urls_set:
        if url and valid_tld(url):
            is_invalid_schema = not any(url.startswith(s) for s in VALID_SCHEMAS)
            urls_list.append(f'http://{url}' if is_invalid_schema else url)

    return [url for url in urls_list if valid_tld(url)]


def scrape_binary_urls(url, visited_urls=[], stop=False):
    binary_urls = []
    visited_urls.append(url)

    try:
        r = session.get(url, timeout=3)
        content_type = r.headers.get('content-type', None)

        if content_type:
            if content_type.startswith('application/'):
                return [url]
            if not content_type.startswith('text/'):
                return []

        if r.content and 'ELF' in r.content[:10].decode('utf-8'):
            return [url]

        # print(r.text)
        has_shebang = '#!' in r.text
        has_get_cmd = any(cmd in r.text for cmd in ['wget', 'curl', 'tftp'])

        if not stop and has_shebang or has_get_cmd:
            text = r.text.replace("\n", ";")
            # Remove tabs
            text = " ".join(text.split())

            for url in extract_urls(text):
                if url not in visited_urls:
                    binary_urls += scrape_binary_urls(url, visited_urls, stop=True)

        return binary_urls
    except Exception:
        return []


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
    urls.update(extract_urls(data))
    urls.update([bin_url for url in urls for bin_url in scrape_binary_urls(url)])
    return [validate_url(url) for url in urls if url]
