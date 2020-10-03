from session import BadPacketsSession

API_URL = "https://api.badpackets.net/v1/"
API_KEY = "enter_api_key"

bps = BadPacketsSession(API_URL, API_KEY)
response = bps.get('/ping')

print(response.status_code)