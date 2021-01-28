import os
import time
import logging
import threading
import utils.collect as collection_utils
import utils.tor_session as tor_session
from badpackets import BadPacketsAPI
from utils.lisa import LiSaAPI
from dotenv import load_dotenv
from datetime import datetime
from utils.args import check_options
from utils.misc import time_until, clear
from pathlib import Path
from utils.stack_thread import ThreadPoolExecutorStackTraced
from concurrent.futures import as_completed
from mongoengine import connect
from requests.exceptions import ConnectionError
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-25s %(levelname)-8s %(message)s",
    datefmt="%d-%m-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            filename='visibot.log',
            maxBytes=5*1024*1024,
        ),
    ]
)
logging.getLogger("filelock").setLevel(logging.ERROR)
logger = logging.getLogger('main')


def process_task(first_run=False):
    """
    The main processing task which runs in a background thread

    Args:
        first_run (bool, optional): Defaults to False.
            Specifies if the process is the first run. If so,
            collect results last seen from current time - FIRST_RUN_HOURS
            instead of 1 hour.
    """
    results = collection_utils.query_badpackets(bp_api, first_run)
    res_len = len(results)

    print(f"\nTotal BadPackets results to process: {res_len}\n")

    futures = [executor.submit(collection_utils.store_result, result) for result in results]

    payloads_to_process = set()
    for i, future in enumerate(as_completed(futures)):
        print(f"\rProcessed {i+1}/{res_len} results | potential payloads: {len(payloads_to_process)}", end="")
        result_payloads = future.result()
        payloads_to_process.update(result_payloads)

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
        dt_now = datetime.utcnow()

        if (dt_now.minute == hourly_min and dt_now.second == 0):
            clear()
            print("Hourly collection cycle triggered!\n")
            executor.submit(process_task)

        time.sleep(1)


if __name__ == "__main__":
    load_dotenv(dotenv_path=Path('..') / '.env', verbose=True)

    clear()

    options = check_options()
    first_run = options.firstrun
    threads = options.threads
    hourly_min = options.hourly_min
    drop_db = options.drop_db

    executor = ThreadPoolExecutorStackTraced(max_workers=threads)

    # Validate tor session
    tor_session.check_session()

    # Init and check LiSa
    lisa_api = LiSaAPI(
        api_url=os.getenv("LISA_API_URL"),
        exec_time=int(os.getenv("LISA_EXEC_TIME_SEC"))
    )

    # Validate BadPackets API Token
    try:
        bp_api = BadPacketsAPI(
            api_url=os.getenv("BADPACKETS_API_URL"),
            api_token=os.getenv("BADPACKETS_API_KEY")
        )
    except Exception:
        msg = "Failed to authorize BadPackets API with provided API key"
        print("\nError:", msg)
        logger.exception(msg)
        raise SystemExit(1)

    print(
        "\nInitialized VisIBoT Processing Script 🤖",
        f"- Thread count {threads}",
        f"- Execute at {hourly_min} min\n",
        "Setting up services:", sep="\n"
    )

    db = connect(host=os.getenv("MONGODB_DB_URL"))
    print("- Connected to VisIBoT MongoDB database")

    if drop_db:
        db_name = os.getenv("MONGODB_DB_NAME")
        confirm = input(f"- DROP {db_name}: This cannot be undone. Are you sure? (y/n): ")

        if confirm == "y":
            db.drop_database(db_name)
            print(f"- MongoDB database {db_name} has been dropped.")
            logger.info(f"User dropped {db_name} database")
        else:
            print("- You cancelled the database drop request.")

    bp_api.ping().raise_for_status()
    print("- Authenticated BadPackets token")

    threading.Thread(target=lisa_api.init_task_checker).start()

    try:
        if first_run:
            print("\nExecuting first run...\n")
            process_task(first_run)
        else:
            print(f"\nNext cycle at: {time_until(hourly_min)} (UTC)\n")

        init_processing_loop()
    except (KeyboardInterrupt):
        print("\n\nClosing processing script and waiting on threads to finish...\n")
        logger.info('KeyBoard Interrupt raised by user.')

    logger.info('Shutting down main.py executor and cancelling futures.')
    executor.shutdown(wait=True, cancel_futures=True)
    lisa_api.stop()
    logger.info('Exiting VisIBoT Processing Script.')
