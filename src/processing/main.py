from badpackets import BadPacketsAPI
from dotenv import load_dotenv
from datetime import datetime, timedelta
from requests.exceptions import HTTPError
from contextlib import suppress
import os
import json
import asyncio

load_dotenv(verbose=True)

last_seen_after_days = (datetime.today() - timedelta(days=int(os.getenv("BADPACKETS_DAYS_BEFORE")))).strftime('%Y-%m-%dT%H:%M:%SZ')
hourly_minute = 15
base_params = {
    'limit': 1000,
    'protocol': 'tcp',
    'last_seen_after': last_seen_after_days,
}
params_to_process = {
    'payload': 'chmod',
    'post_data': 'chmod',
    'tags': 'IoT',
    'tags': 'Mirai',
}

def process_results(results_json):
    #print(json.dumps(results_json, indent=4))
    print("Results:", len(results_json['results']))
    #print(results_json['next'])

async def process_badpackets():
    
    await asyncio.sleep(1)

    for param, value in params_to_process.items():
        params = base_params.copy()
        params[param] = value

        try:
            results = bp_api.query(params)
            results.raise_for_status()
            print(f"\nQuerying param: {param}={value}")
            results_json = results.json()
            process_results(results_json)
            await asyncio.sleep(1)

            while results_json['next']:
                print(" - Getting Next Page...")
                # TODO bp_api.get() method
                results = bp_api.get(url=results_json['next'])
                results_json = results.json()
                process_results(results_json)
                await asyncio.sleep(1)
        except (HTTPError, AttributeError) as e:
            raise e

async def hourly_processing_task():
    print(f"Initialised hourly task (executes at minute {hourly_minute})\n")
    while True:
        dtnow = datetime.now()

        if dtnow.minute == hourly_minute and dtnow.second == 0:
            # Run processor in a thread
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
    asyncio.run(process_badpackets())
    """
    try:
        loop = asyncio.get_event_loop()
        task = loop.create_task(hourly_processing_task())
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass
    """
