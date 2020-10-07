from requests import Session
from urllib.parse import urljoin


class BadPacketsSession(Session):
    def __init__(self, api_url=None, api_token=None, *args, **kwargs):
        super(BadPacketsSession, self).__init__(*args, **kwargs)
        self.api_url = api_url
        self.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Token {api_token}'
            #'User-Agent': f'Bad Packets Python API Wrapper/1.0'
        })

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.api_url, url)
        return super(BadPacketsSession, self).request(
            method, url, *args, **kwargs
        )
