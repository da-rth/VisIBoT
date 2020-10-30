from badpackets import BadPacketsAPI
from dotenv import load_dotenv
from datetime import datetime
from utils.misc import time_until, clear
from pathlib import Path
import utils.badpackets as bp_utils
import concurrent.futures
import os
import sys
import time
import optparse

load_dotenv(dotenv_path=Path('..') / '.env', verbose=True)

# Constants
BP_URL = os.getenv("BADPACKETS_API_URL")
BP_KEY = os.getenv("BADPACKETS_API_KEY")

# Optopn Parser setup
parser = optparse.OptionParser()

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
    default=1,
    type=int
)

# Methods
def check_options():
    threads_ok = options.threads >= 1
    hour_min_ok = 0 <= options.hourly_min <= 59

    if (threads_ok and hour_min_ok): return

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

    futures = [executor.submit(bp_utils.store_result, evt, res) for evt, res in results.items()]

    for i, future in enumerate(concurrent.futures.as_completed(futures)):
        print(f"Processed {i+1}/{res_len} results", end="\r")

    print("Completed processing BadPackets results.\n")

    if not first_run:
        print(f"Waiting until next cycle at: {time_until(hourly_min)} (UTC)\n", end="\r")


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
    options, args = parser.parse_args()
    check_options()

    clear()

    print("Initialised VisIBoT BadPackets Pre-processor 🤖")

    first_run = options.firstrun
    threads = options.threads
    hourly_min = options.hourly_min

    print("- Thread count:", threads)
    print("- Execute minute:", hourly_min)

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=threads)

    bp_api = BadPacketsAPI(api_url=BP_URL, api_token=BP_KEY)
    bp_api.ping().raise_for_status()

    print("- BadPackets API: Authenticated token")

    time.sleep(1)

    try:
        if first_run:
            print("- Preparing first run...\n")
            process_task(first_run)
        print(f"- Starting processing loop.\n- Next cycle at: {time_until(hourly_min)} (UTC)\n", end="\r")
        init_processing_loop()
    except (KeyboardInterrupt):
        print("\n\nClosing processing script and waiting on threads to finish...\n")
    finally:
        executor.shutdown(wait=True, cancel_futures=True)
        print("Goodbye")
