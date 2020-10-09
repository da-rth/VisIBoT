from badpackets import BadPacketsAPI
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import json
import asyncio

load_dotenv(verbose=True)

last_seen_after_days = (datetime.today() - timedelta(days=int(os.getenv("BADPACKETS_DAYS_BEFORE")))).strftime('%Y-%m-%dT%H:%M:%SZ')
hourly_minute = 30
query_params = {
    'tags': 'IoT',
    'limit': 10,
    'protocol': 'tcp',
    'last_seen_after': last_seen_after_days
}


def process_badpackets():
    print("Querying Bad Packets API...")
    results = bp_api.query(query_params)
    if results.status_code == 200:
        print(json.dumps(results.json(), indent=4))


async def hourly_processing_task():
    print(f"Initialised hourly task (executes at minute {hourly_minute})\n")
    while True:
        dtnow = datetime.now()

        if dtnow.minute == hourly_minute and dtnow.second == 0:
            await process_badpackets()

        await asyncio.sleep(1)


if __name__ == "__main__":
    bp_api = BadPacketsAPI(
        api_url=os.getenv("BADPACKETS_API_URL"),
        api_token=os.getenv("BADPACKETS_API_TOKEN")
    )

    bp_api.ping().raise_for_status()

    print("BadPackets API: Authenticated token")

    try:
        loop = asyncio.get_event_loop()
        task = loop.create_task(hourly_processing_task())
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass
