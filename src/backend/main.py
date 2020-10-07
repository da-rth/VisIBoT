from badpackets import BadPacketsAPI
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

bp_api = BadPacketsAPI(
    api_url=os.getenv("BADPACKETS_API_URL"),
    api_token=os.getenv("BADPACKETS_API_TOKEN"),
    verbose=True
)

bp_api.ok()
