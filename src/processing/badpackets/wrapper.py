from badpackets.session import BadPacketsSession
import urllib

SUPPORTED_QUERY_PARAMS = [
    "event_id",
    "source_ip_address",
    "target_port",
    "protocol",
    "user_agent",
    "payload",
    "post_data",
    "country",
    "first_seen_before",
    "first_seen_after",
    "last_seen_before",
    "last_seen_after",
    "tags",
    "event_count",
    "limit",
    "offset",
    "ordering"
]

""" BadPackets API Wrapper

Description:
    A wrapper for the Bad Packets API. Various queries can be made
    directly through this wrapper. See BadPackets API Documentation
    for more information: https://docs.badpackets.net/#operation/query

Raises:
    APIError: If provided API token is invalid, a HTTPError (status 401
              or 403) will be raised.
"""


class BadPacketsAPI():

    def __init__(self, api_url=None, api_token=None, verbose=False):
        if api_token is None:
            raise ValueError("An API key is required to use BadPackets")

        api_url = "https://api.badpackets.net/v1/" if not api_url else api_url
        self.session = BadPacketsSession(api_url, api_token)

    def ping(self):
        return self.session.get('ping')

    def query(self, params):
        for param in params:
            if param not in SUPPORTED_QUERY_PARAMS:
                raise ValueError(f'Unsupported query parameter: {param}')
        url_params = urllib.parse.urlencode(params)
        return self.session.get(f'query?{url_params}')
