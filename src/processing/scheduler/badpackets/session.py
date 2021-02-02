from requests import Session
from urllib.parse import urljoin


class BadPacketsSession(Session):
    """
    Generates a session used for BadPackets API requests.
    - The provided api_token is inserted into the header of each request made.
    - All request url strings are prepended with the BadPackets API base url.
    """
    def __init__(self, api_url=None, api_token=None, *args, **kwargs):
        super(BadPacketsSession, self).__init__(*args, **kwargs)
        self.api_url = api_url
        self.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Token {api_token}'
        })

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.api_url, url)
        return super(BadPacketsSession, self).request(
            method, url, *args, **kwargs
        )
