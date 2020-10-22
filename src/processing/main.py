from badpackets import BadPacketsAPI
from dotenv import load_dotenv
from datetime import datetime, timedelta
from requests.exceptions import HTTPError
from contextlib import suppress
import os
import json
import asyncio

load_dotenv(verbose=True)


hourly_minute = 15
base_params = {
    'limit': 1000,
    'protocol': 'tcp',
}
params_to_process = {
    'payload': 'chmod',
    'post_data': 'chmod',
    'tags': 'IoT',
    'tags': 'Mirai',
}

def process_results(results_json):
    print(f"Total results: {results_json['count']} | Current results: {len(results_json['results'])} | has next: {results_json['next'] != None}")

async def process_badpackets(first_run=False):
    if first_run:
        print(f"Performing first run. Querying last 24h of results from BadPackets.")
    
    for param, value in params_to_process.items():

        after_dt = (
            datetime.today() - timedelta(hours=24 if first_run else 1)
        ).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        params = base_params.copy()
        params['last_seen_after'] = after_dt
        params[param] = value
        
        print(f"\nQuerying param: {param}={value} | Last seen after: {after_dt}")
    
        with suppress(HTTPError, AttributeError):
            await asyncio.sleep(1)
            results_json = bp_api.query(params).json()
            process_results(results_json)
            
            while results_json['next']:
                await asyncio.sleep(1)
                results_json = bp_api.get_url(results_json['next']).json()
                process_results(results_json)

async def hourly_processing_task():
    print(f"Initialised hourly task. Executes at minute {hourly_minute}\n")
    while True:
        dtnow = datetime.now()
        if dtnow.minute == hourly_minute and dtnow.second == 0:
            await asyncio.gather(
                asyncio.to_thread(process_badpackets),
                asyncio.sleep(1)
            )


if __name__ == "__main__":
    bp_api = BadPacketsAPI(
        api_url=os.getenv("BADPACKETS_API_URL"),
        api_token=os.getenv("BADPACKETS_API_TOKEN")
    )

    bp_api.ping().raise_for_status()

    print("BadPackets API: Authenticated token")

    try:
        asyncio.run(process_badpackets(first_run=True))

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        task = loop.create_task(hourly_processing_task())
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass
