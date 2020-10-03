from requests.exceptions import HTTPError
from badpackets.session import BadPacketsSession
from dotenv import load_dotenv
import requests
import os
import sys

""" BadPackets API Wrapper

Description:
    A wrapper for the Bad Packets API. Various queries can be made directly through this wrapper.
    See BadPackets API Documentation for more information: https://docs.badpackets.net/#operation/query

Raises:
    APIError: If provided API token is invalid, a HTTPError (status 401 or 403) will be raised.
"""
class BadPacketsAPI():

    def __init__(self, api_url=None, api_token=None, verbose=False):
        self.api_url = api_url if api_url else "https://api.badpackets.net/v1/"
        self.session = BadPacketsSession(self.api_url, api_token)
        self.verbose = verbose

        try:
            self.ping().raise_for_status()
            if self.verbose: print("BadPackets API: Successfully authenticated token")
        except requests.exceptions.HTTPError as BadPacketsInvalidApiToken:
            raise BadPacketsInvalidApiToken
    
    def ping(self):
        return self.session.get('ping')
    
    def ok(self):
        print("ok")

