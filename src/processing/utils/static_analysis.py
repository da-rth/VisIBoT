import os
import requests
from contextlib import suppress


SA_API_URL = os.getenv("SA_API_URL")
SA_API_KEY = os.getenv("SA_API_KEY")
HEADERS = {
    "x-api-key": SA_API_KEY,
    "Accept": "application/json",
}

def retrieve_analysis(url, all_strings=False):
    params = {
        "url": url,
        "all_strings": "true" if all_strings else None,
    }
    
    with suppress(requests.exceptions.Timeout):
        response = requests.get(SA_API_URL, params=params, headers=HEADERS)

        if response.status_code == 200:
            return response.json()

if __name__ == "__main__":
    """
    TODO: Fix API response error :(
    {
        "msg": "can only concatenate str (not \"int\") to str"
    }
    """
    print(retrieve_analysis(url="http://23.254.228.212/zyxel.sh", all_strings=True))
