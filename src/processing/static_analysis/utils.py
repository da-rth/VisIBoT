import re
import validators
import tldextract
from tld import is_tld

def parse_floss_output(input_strings):
    parsed_strings = []

    for i, s in enumerate(input_strings):
        string = s.s.encode('ascii', 'ignore')
        parsed_strings.append(string)

    return " ".join(parsed_strings).replace(" <floss-h-space> ", "")


def valid_tld(domain_or_url):
    top_level_domain = tldextract.extract(domain_or_url).suffix
    return is_tld(top_level_domain)


def ip_url_strings(string):
    ipv4s, ipv6s, urls, domains = set(), set(), set(), set()

    for s in string.split(" "):
        if validators.ip_address.ipv6(s) and s != ":":
            ipv6s.add(s)
        elif validators.ip_address.ipv4(s):
            ipv4s.add(s)
        elif validators.url(s):
            urls.add(s)
        elif validators.domain(s) and valid_tld(s):
            domains.add(s)

    return {
        "ipv4": list(ipv4s),
        "ipv6": list(ipv6s),
        "urls": list(urls),
        "domains": list(domains)
    }
