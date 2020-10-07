from badpackets import BadPacketsAPI
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import json


load_dotenv(verbose=True)

last_seen_after_days = os.getenv("BADPACKETS_SEEN_AFTER_DAYS")

bp_api = BadPacketsAPI(
    api_url=os.getenv("BADPACKETS_API_URL"),
    api_token=os.getenv("BADPACKETS_API_TOKEN"),
    verbose=True
)

query_params = {
    'tags': 'Mirai',
    'limit': 1,
}

if last_seen_after_days:
    print(last_seen_after_days)
    query_params['last_seen_after'] = (
        datetime.today() - timedelta(days=last_seen_after_days)
    ).strftime('%Y-%m-%dT%H:%M:%SZ')

results = bp_api.query(query_params).json()

if "detail" in results:
    raise RuntimeError(results["detail"])

print(results)