from badpackets.session import BadPacketsSession
import requests
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
        api_url if api_url else "https://api.badpackets.net/v1/"
        self.session = BadPacketsSession(api_url, api_token)
        self.verbose = verbose

        try:
            self.ping().raise_for_status()
            if self.verbose:
                print("BadPackets API: Authenticated token")
        except requests.exceptions.HTTPError as BadPacketsInvalidApiToken:
            raise BadPacketsInvalidApiToken

    def ping(self):
        return self.session.get('ping')

    def query(self, params):
        for param in params:
            if param not in SUPPORTED_QUERY_PARAMS:
                raise ValueError(f'Unsupported query parameter: {param}')
        url_params = urllib.parse.urlencode(params)
        return self.session.get(f'query?{url_params}')
