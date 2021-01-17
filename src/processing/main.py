from badpackets import BadPacketsAPI
from utils.lisa import LiSaAPI
from dotenv import load_dotenv
from datetime import datetime
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
import sys
import time
import optparse

load_dotenv(dotenv_path=Path('..') / '.env', verbose=True)


# Main Methods
def create_parser_options():
    """
    Adds various command-line arguments supported by the processing script.
    """
    parser.add_option(
        "-t",
        "--threads",
        action="store",
        dest="threads",
        help="The number of worker threads to use while processing results.",
        default=4,
        type=int
    )
    parser.add_option(
        "-f",
        "--firstrun",
        action="store_true",
        dest="firstrun",
        help="Executes with 'first run' parameters (gets results from last 24h)",
        default=False
    )
    parser.add_option(
        "-m",
        "--minute",
        action="store",
        dest="hourly_min",
        help="The minute when the hourly processor executes",
        default=30,
        type=int
    )


def check_options(options):
    """
    Validates the command-line arguments provided by the user.

    Raises:
        SystemExit: If option is provided invalid value, print error and exit
    """
    threads_ok = options.threads >= 1
    hour_min_ok = 0 <= options.hourly_min <= 59

    if (threads_ok and hour_min_ok):
        return

    err_msg = "error: invalid parameter(s)"

    if not threads_ok:
        err_msg = "\n".join([err_msg, " -f, --firstrun: Number of threads must be at least 1."])
    if not hour_min_ok:
        err_msg = "\n".join([err_msg, " -m, --minute: Minute value must be between 0-59."])

    print(err_msg, file=sys.stderr)

    raise SystemExit()


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

    payloads_to_process = []
    for i, future in enumerate(as_completed(futures)):
        print(f"Processed {i+1}/{res_len} results", end="\r")
        payloads_to_process += future.result()

    try:
        print(f"\n\nInitializing malware analysis: requesting LiSa analysis for {len(payloads_to_process)} payloads (Exec time: 20s).")
        print("- Note: Some malware URLs may already be offline. These will be skipped.")

        futures = [executor.submit(lisa_api.create_file_task, payload) for payload in payloads_to_process]
        created_lisa_tasks = sum(1 for future in futures if future.result())

        if created_lisa_tasks > 0:
            print(f"\n- [LiSa] Executing malware for {created_lisa_tasks} payloads. This will run in background.")
        else:
            print("- [LiSa] No analysis tasks were created. No binaries could be retrieved from payload URLs.")

    except ConnectionError:
        print("\nNOTICE: Failed to connect to LiSa Server - Skipping payload malware analysis")

    print("\n- Completed processing BadPackets results.")

    if not first_run:
        print(f"Waiting until next cycle at: {time_until(hourly_min)} (UTC)")


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
    # Check processing script arguments
    parser = optparse.OptionParser()
    create_parser_options()
    options, args = parser.parse_args()
    check_options(options)

    clear()
    print("Initialised VisIBoT Processing Script 🤖")

    first_run = options.firstrun
    threads = options.threads
    hourly_min = options.hourly_min
    print("- Thread count:", threads, "\n- Execute minute:", hourly_min)

    print("\nSetting up URL Classifier")
    url_classifier = URLClassifier('datasets/urldata.csv')

    print("\nSetting up services:")

    connect(host=os.getenv("MONGODB_URL"))
    print("- MongoDB: Connected to VisIBoT database")

    executor = ThreadPoolExecutorStackTraced(max_workers=threads)

    bp_api = BadPacketsAPI(
        api_url=os.getenv("BADPACKETS_API_URL"),
        api_token=os.getenv("BADPACKETS_API_KEY")
    )
    bp_api.ping().raise_for_status()
    print("- BadPackets API: Authenticated token")

    lisa_api = LiSaAPI(api_url=os.getenv("LISA_API_URL"))
    t = threading.Thread(target=lisa_api.init_task_checker)
    t.start()

    time.sleep(1)

    try:
        if first_run:
            print("\nExecuting first run...\n")
            process_task(first_run)

        print(f"- Next cycle at: {time_until(hourly_min)} (UTC)\n\n", end="\r")
        init_processing_loop()
    except (KeyboardInterrupt):
        print("\n\nClosing processing script and waiting on threads to finish...\n")
    finally:
        executor.shutdown(wait=True, cancel_futures=True)
        lisa_api.stop()
