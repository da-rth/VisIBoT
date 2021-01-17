# pylama:ignore=E402:ignore=E702
import sys; sys.path.append("..")
import database as db
import requests
import threading
import time
import pydnsbl
from .stack_thread import ThreadPoolExecutorStackTraced
from IPy import IP
from datetime import datetime
from utils.misc import get_ip_hostname
from utils.geodata import geoip_info
from contextlib import suppress

ip_checker = pydnsbl.DNSBLIpChecker()


class LiSaAPI:

    def __init__(self, api_url):
        self.running = True
        self.api_url = api_url
        self.pending_task_ids = []
        self.successful_tasks_count = 0
        self.failed_tasks_count = 0
        self.processing_tasks_count = 0
        self.blink = False
        self.can_clear = False
        self.executor = ThreadPoolExecutorStackTraced(max_workers=4)

        try:
            requests.get(self.api_url)
            print("- LiSa API: LiSa server is online.")
        except Exception:
            print("- LiSa API: Error! LiSa Server could not be reached. Is it running?")

    def create_file_task(self, payload):
        r = requests.post(f"{self.api_url}/tasks/create/file", {'url': payload.url})

        if r.status_code == 200 and r.json():
            task_id = r.json()['task_id']
            self.pending_task_ids.append([payload, task_id])
            return True

    def process_task_result(self, payload, task_id):
        candidate_C2s = []

        r = requests.get(f"{self.api_url}/report/{task_id}")

        if r.status_code != 200 or not r.json():
            return

        analysis = r.json()
        strings = "".join(analysis['static_analysis']['strings'])
        endpoints = analysis['network_analysis']['endpoints'].copy()

        del analysis['static_analysis']
        del analysis['dynamic_analysis']
        del analysis['network_analysis']

        for endpoint in endpoints:
            ip_address = IP(endpoint['ip'])

            if ip_address.iptype() == 'PRIVATE':
                continue

            is_hardcoded_s = endpoint['ip'] in strings
            is_blacklisted = endpoint['blacklisted']
            is_transaction = endpoint['data_in'] > 0 and endpoint['data_out'] > 0

            # ip_checker.check(str(ip_address)).blacklisted

            if is_blacklisted or is_transaction or is_hardcoded_s:
                ip_address = str(ip_address)
                geodata = geoip_info(ip_address)

                if not geodata:
                    continue

                hostname = get_ip_hostname(ip_address)

                c2_geo = db.geodata_create_or_update(
                    ip_address,
                    hostname,
                    "C2 Server",
                    geodata
                )
                
                c2 = db.candidate_c2_create_or_update(
                    ip_address=c2_geo.id,
                    payload_ids=[payload.id]
                )

                candidate_C2s.append(c2_geo)

        payload.update(
            set__lisa=analysis,
            set__candidate_C2s=candidate_C2s
        )

        self.successful_tasks_count += 1
        self.processing_tasks_count -= 1

    def stop(self):
        self.running = False
    
    def print_output(self):
        self.blink = not self.blink
        print((
            f"\r- [LiSa] Malware Analysis - Pending: {len(self.pending_task_ids)} | " \
            f"Processing: {self.processing_tasks_count} | " \
            f"Successful: {self.successful_tasks_count} | " \
            f"Failed: {self.failed_tasks_count}" \
            f"{' ...' if self.blink else '    '}"
        ), end="", flush=True)

    def init_task_checker(self):
        api_retries = 3
        print("- LiSa API: Initialized LiSa Task Checker Loop")
        while self.running:

            if self.pending_task_ids:
                tasks_to_remove = []

                self.can_clear = True

                r = requests.get(f"{self.api_url}/tasks?limit=20")

                if not r.json():
                    api_retries -= 1

                    if api_retries == 0:
                        print("- [LiSa] Could not reach LiSa task list endpoint after 3 retries... cancelling pending tasks.", flush=True)
                        self.pending_task_ids = []
                        continue

                with suppress(TypeError):
                    complete_tasks_list = {r['task_id']: r['status'] for r in r.json()}

                    for (payload, task_id) in self.pending_task_ids:
                        if not self.running:
                            break

                        if task_id in complete_tasks_list:
                            status = complete_tasks_list[task_id]

                            if status:
                                if status == 'SUCCESS':
                                    self.processing_tasks_count += 1
                                    self.executor.submit(self.process_task_result, payload, task_id)

                                if status == 'FAILURE':
                                    self.failed_tasks_count += 1

                                tasks_to_remove.append(task_id)

                    self.pending_task_ids = [t for t in self.pending_task_ids if t[1] not in tasks_to_remove]

            else:
                self.successful_tasks_count = 0
                self.failed_tasks_count = 0
                self.processing_tasks_count = 0
                api_retries = 3

            if self.processing_tasks_count > 0 or len(self.pending_task_ids) > 0:
                self.print_output()

            elif self.can_clear:
                print("\r- [LiSa] Finished Analysis: task queue empty." + (" " * 64), end="\n", flush=True)
                self.can_clear = False

            time.sleep(1)

        self.executor.shutdown(wait=True, cancel_futures=True)
        print("- LiSa API: Stopped LiSa task loop. Running tasks may take a while to finish.", flush=True)
