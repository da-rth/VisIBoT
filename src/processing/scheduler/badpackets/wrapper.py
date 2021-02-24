from badpackets.session import BadPacketsSession
from ratelimit import limits, sleep_and_retry
from requests import Response
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

""" Bad Packets API Wrapper

Description:
    A wrapper for the Bad Packets API. Various queries can be made
    directly through this wrapper. See Bad Packets API Documentation
    for more information: https://docs.badpackets.net/#operation/query

Raises:
    APIError: If provided API token is invalid, a HTTPError (status 401
              or 403) will be raised.
"""


class BadPacketsAPI():

    def __init__(self, api_url=None, api_token=None, verbose=False):
        if api_token is None:
            raise ValueError("An API key is required to use Bad Packets")

        api_url = "https://api.badpackets.net/v1/" if not api_url else api_url
        self.session = BadPacketsSession(api_url, api_token)

    @sleep_and_retry
    @limits(calls=1, period=2)
    def ping(self) -> Response:
        """
        Checks if the Bad Packets API service is online.
        Calling response.raise_for_status() will raise an exception if the request was
        unsuccessful or the provided API key could not be authenticated.

        Returns:
            Response: The response object for the given GET request indicating success of ping.
        """
        return self.session.get('ping')

    @sleep_and_retry
    @limits(calls=1, period=2)
    def query(self, params: dict) -> Response:
        """ Queries the BadPackets API using the given parameters (if supported).

        Args:
            params (dict): A dictionary of query parameter keys and values.

        Raises:
            ValueError: An un-supported query-parameter has been provided.

        Returns:
            Response: The response object for the given GET request containing Bad Packets result data.
        """
        for param in params:
            if param not in SUPPORTED_QUERY_PARAMS:
                raise ValueError(f'Unsupported query parameter: {param}')
        url_params = urllib.parse.urlencode(params)
        return self.session.get(f'query?{url_params}')

    @sleep_and_retry
    @limits(calls=1, period=2)
    def get_url(self, url: str) -> Response:
        """
        Queries the next page of Bad Packets results to be queried given the URL
        from the current response data.

        Args:
            url (str): The [next] API URL to query for additional Bad Packets results.

        Returns:
            Response: The response object for the given GET request containing Bad Packets result data.
        """
        url_params = url.split('/')[-1]
        return self.session.get(f'{url_params}')
