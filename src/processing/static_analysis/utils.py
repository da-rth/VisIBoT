import re

unsafe_url_chars = "<>#%{}|\^~[]"

def parse_floss_output(input_strings):
    parsed_strings = []

    for i, s in enumerate(input_strings):
        string = s.s.encode('ascii','ignore')
        if string.endswith('H'):
            string = string[:-1] + " <floss-h-space>"
        parsed_strings.append(string)

    return " ".join(parsed_strings).replace(" <floss-h-space> ", "")

def ip_url_strings(string):
    ips = list(set(re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", string)))
    urls = list(set(re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)))
    urls = [url.translate(None, ''.join(unsafe_url_chars)) for url in urls]

    return {
        "ips": ips,
        "urls": urls,
    }