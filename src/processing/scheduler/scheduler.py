import os
import time
from utils import time_until
from worker import celery_worker
from badpackets import BadPacketsAPI
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

# Some Constants
FIRST_RUN = os.getenv("FIRST_RUN", False) == "True"
FIRST_RUN_HOURS = int(os.getenv("FIRST_RUN_HOURS", 12))
FLOWER_URL = os.getenv("FLOWER_URL", "http://localhost:5555")
EVENT_MIN = int(os.getenv("EVENT_MINUTE", 15))
BP_API_KEY = os.getenv("BAD_PACKETS_API_KEY", None)

# Initialize BP API Wrapper
bp_api = BadPacketsAPI(api_token=BP_API_KEY)
bp_api.ping().raise_for_status()

# Setup scheduler
scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', hour='*', minute=EVENT_MIN)
def get_badpackets_results(first_run: bool = False):
    print("VisIBot collection event activated. Collecting data from BadPackets API.")

    after_dt = datetime.utcnow() - timedelta(hours=FIRST_RUN_HOURS if first_run else 1)
    after_dt = after_dt.replace(minute=0, second=0, microsecond=0).strftime('%Y-%m-%dT%H:%M:%SZ')

    print(f"Querying BadPackets (last seen after {after_dt})")

    results = []

    try:
        results_json = bp_api.query({"last_seen_after": after_dt, "limit": 1000}).json()
        results += results_json['results']
        total_results = results_json['count']

        print(f" -> Queried {len(results)}/{total_results} results")

        while results_json.get('next', False):
            results_json = bp_api.get_url(results_json['next']).json()
            results += results_json['results']

            print(f" -> Queried {len(results)}/{total_results} results")

    except Exception:
        print("Error! Failed to obtain BadPackets results for last query.")

    if results:
        print("Adding analysis tasks to worker queue...")

    for result in results:
        celery_worker.send_task('tasks.process_result', args=[result], kwargs={})

    print(f"Workers are now running tasks in the background. Visit {FLOWER_URL} to view progress.")

    if not first_run:
        print(f"The next collection event is scheduled for: {time_until(EVENT_MIN)} (UTC)")


if __name__ == "__main__":
    time.sleep(1)

    if FIRST_RUN:
        print(f"Executing first run. Obtaining BadPackets results from the last {FIRST_RUN_HOURS} hours.")
        get_badpackets_results(first_run=True)

    print(f"Started hourly scheduler. The next event will execute at: {time_until(EVENT_MIN)} (UTC).")
    scheduler.start()
