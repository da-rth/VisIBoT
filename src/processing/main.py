from badpackets import BadPacketsAPI
from utils.lisa import LiSaAPI
from dotenv import load_dotenv
from datetime import datetime
from utils.args import check_options
from utils.misc import time_until, clear
from utils.url_classifier import URLClassifier
from pathlib import Path
from utils.stack_thread import ThreadPoolExecutorStackTraced
from concurrent.futures import as_completed
from mongoengine import connect
from requests.exceptions import ConnectionError
import utils.badpackets as bp_utils
import threading
import os
import time


load_dotenv(dotenv_path=Path('..') / '.env', verbose=True)


# Main Methods
def process_task(first_run=False):
    """
    The main processing task which runs in a background thread

    Args:
        first_run (bool, optional): Defaults to False.
            Specifies if the process is the first run. If so,
            collect results last seen from current time - FIRST_RUN_HOURS
            instead of 1 hour.
    """
    results = {res['event_id']: res for res in bp_utils.query_badpackets(bp_api, first_run)}
    res_len = len(results)

    print(f"\nTotal BadPackets results to process: {res_len}\n")

    futures = [executor.submit(bp_utils.store_result, evt, res, url_classifier) for evt, res in results.items()]

    payloads_to_process = set()
    for i, future in enumerate(as_completed(futures)):
        print(f"Processed {i+1}/{res_len} results", end="\r")
        payloads_to_process.update(future.result())

    print(f"\nCompleted processing BadPackets results. Next cycle at: {time_until(hourly_min)} (UTC).\n")

    try:
        lisa_api.create_file_tasks(payloads_to_process)
    except ConnectionError:
        print("\nNOTICE: Failed to connect to LiSa Server - Skipping payload malware analysis")


def init_processing_loop():
    """
    The main processing loop which runs continually until
    a KeyboardInterrupt is detected. Each loop sleeps for 1 second
    and the processing task executes once per hour at: HH::hourly_min:00
    """
    while True:
        dtnow = datetime.utcnow()

        if (dtnow.minute == hourly_min and dtnow.second == 0):
            print("Hourly processing script triggered\n")
            executor.submit(process_task)

        time.sleep(1)


if __name__ == "__main__":
    # Parse command-line arguments
    options = check_options()
    first_run = options.firstrun
    threads = options.threads
    hourly_min = options.hourly_min
    executor = ThreadPoolExecutorStackTraced(max_workers=threads)

    # API Instances
    bp_api = BadPacketsAPI(
        api_url=os.getenv("BADPACKETS_API_URL"),
        api_token=os.getenv("BADPACKETS_API_KEY")
    )

    lisa_api = LiSaAPI(
        api_url=os.getenv("LISA_API_URL")
    )

    # Clear console and launch script
    clear()
    print(
        "Initialized VisIBoT Processing Script 🤖",
        f"- Thread count {threads}",
        f"- Execute at {hourly_min} min\n",
        "Setting up services:", sep="\n"
    )

    connect(host=os.getenv("MONGODB_URL"))
    print("- Connected to VisIBoT MongoDB database")

    bp_api.ping().raise_for_status()
    print("- Authenticated BadPackets token")

    t = threading.Thread(target=lisa_api.init_task_checker)
    t.start()

    print("\nSetting up URL Classifier")
    url_classifier = URLClassifier('datasets/urldata.csv')

    try:
        if first_run:
            print("\nExecuting first run...\n")
            process_task(first_run)
        else:
            print(f"\nNext cycle at: {time_until(hourly_min)} (UTC)\n")

        init_processing_loop()
    except (KeyboardInterrupt):
        print("\n\nClosing processing script and waiting on threads to finish...\n")
    finally:
        executor.shutdown(wait=True, cancel_futures=True)
        lisa_api.stop()
