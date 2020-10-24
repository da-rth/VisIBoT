from badpackets import BadPacketsAPI
from dotenv import load_dotenv
from datetime import datetime
from utils.misc import time_until
import utils.badpackets as bp_utils
import concurrent.futures
import os
import time

load_dotenv(verbose=True)

# Constants
FIRST_RUN = True
MAX_THREADS = 8
HOURLY_AT_MIN = 30
BP_URL = os.getenv("BADPACKETS_API_URL")
BP_KEY = os.getenv("BADPACKETS_API_KEY")

# Thread Execution Pool
executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS)


def background_process_task(first_run=False):
    results = {res['event_id']: res for res in bp_utils.query_badpackets(bp_api, first_run)}
    res_len = len(results)

    print(f"\nTotal BadPackets results to process: {res_len}\n")

    futures = [executor.submit(bp_utils.store_result, evt, res) for evt, res in results.items()]

    for i, future in enumerate(concurrent.futures.as_completed(futures)):
        print(f"Processed {i+1}/{res_len} results", end="\r")

    print("Completed processing BadPackets results.\n")

    if not first_run:
        print(f"Waiting until next cycle at: {time_until(HOURLY_AT_MIN)} (UTC)\n", end="\r")


def init_processing_loop():
    while True:
        dtnow = datetime.utcnow()

        if (dtnow.minute == HOURLY_AT_MIN and dtnow.second == 0):
            print("Hourly processing script triggered\n")
            executor.submit(background_process_task)

        time.sleep(1)


if __name__ == "__main__":

    bp_api = BadPacketsAPI(api_url=BP_URL, api_token=BP_KEY)
    bp_api.ping().raise_for_status()

    print("BadPackets API: Authenticated token\n")

    time.sleep(1)

    try:
        if FIRST_RUN:
            print("Preparing first run...\n")
            background_process_task(first_run=True)
        print(f"Starting processing loop. Next cycle at: {time_until(HOURLY_AT_MIN)} (UTC)\n", end="\r")
        init_processing_loop()
    except (KeyboardInterrupt):
        print("\n\nClosing processing script and waiting on threads to finish...\n")
    finally:
        executor.shutdown(wait=True, cancel_futures=True)
        print("Goodbye")
