from badpackets import BadPacketsAPI
from dotenv import load_dotenv
from datetime import datetime
from utils.misc import time_until, clear
from pathlib import Path
from utils.threading import ThreadPoolExecutorStackTraced
from utils.virustotal import VirusTotalURLProcessor
from concurrent.futures import as_completed
from mongoengine import connect
import utils.badpackets as bp_utils
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
        default=1,
        type=int
    )


def check_options():
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

    futures = [executor.submit(bp_utils.store_result, evt, res, vt_api) for evt, res in results.items()]

    for i, future in enumerate(as_completed(futures)):
        print(f"Processed {i+1}/{res_len} results + {future.result()}", end="\r")

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
    parser = optparse.OptionParser()
    create_parser_options()

    options, args = parser.parse_args()
    check_options()

    clear()

    print("Initialised VisIBoT BadPackets Pre-processor 🤖")

    first_run = options.firstrun
    threads = options.threads
    hourly_min = options.hourly_min

    print("- Thread count:", threads)
    print("- Execute minute:", hourly_min)

    connect(host=os.getenv("MONGODB_URL"))
    print("- Connected to Database")

    executor = ThreadPoolExecutorStackTraced(max_workers=threads)
    vt_api = VirusTotalURLProcessor(
        os.getenv("VIRUSTOTAL_API_KEY")
    )
    print("- VirusTotal API: Authenticated token")
    
    bp_api = BadPacketsAPI(
        api_url=os.getenv("BADPACKETS_API_URL"),
        api_token=os.getenv("BADPACKETS_API_KEY")
    )
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
