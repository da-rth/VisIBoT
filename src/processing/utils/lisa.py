# pylama:ignore=E402:ignore=E702
import sys; sys.path.append("..")
import database as db
import requests
import threading
import time
import pydnsbl
from IPy import IP
from datetime import datetime
from utils.misc import get_ip_hostname
from utils.geodata import geoip_info


ip_checker = pydnsbl.DNSBLIpChecker()


class LiSaAPI:

    def __init__(self, api_url):
        self.running = True
        self.api_url = api_url
        self.pending_task_ids = []
        self.t = threading.Thread(name='init_task_checker', target=self.init_task_checker)
        self.t.start()

    def create_file_task(self, payload):
        r = requests.post(f"{self.api_url}/tasks/create/file", {'url': payload.url})

        if r.status_code == 200 and r.json():
            task_id = r.json()['task_id']
            self.pending_task_ids.append([payload, task_id])
            return True

    def process_task_results(self, payload, task_id):
        r = requests.get(f"{self.api_url}/report/{task_id}")
        if r.status_code == 200:
            analysis = r.json()
            # TODO: Strings analysis
            # strings = analysis['static_analysis']['strings'].copy()
            endpoints = analysis['network_analysis']['endpoints'].copy()
            candidate_servers = []

            del analysis['static_analysis']
            del analysis['network_analysis']

            payload.lisa = analysis
            payload.save()

            for endpoint in endpoints:
                ip_address = IP(endpoint['ip'])
                is_private = ip_address.iptype() == 'PRIVATE'

                if is_private:
                    continue

                is_blacklisted = endpoint['blacklisted']
                is_transaction = endpoint['data_in'] > 0 and endpoint['data_out'] > 0

                if is_blacklisted or is_transaction or ip_checker.check(str(ip_address)).blacklisted:
                    ip_address = str(ip_address)
                    geodata = geoip_info(ip_address)

                    if geodata:
                        hostname = get_ip_hostname(ip_address)
                        db.geodata_create_or_update(
                            ip_address,
                            hostname,
                            "C2 Server",
                            geodata,
                            datetime.utcnow()
                        )
                        candidate_servers.append(ip_address)

            print(f"- [LiSa] Success! Payload ID: {payload.id} | URL: {payload.url} | Total Candidate C2s: {len(candidate_servers)}")

    def stop(self):
        self.running = False

    def init_task_checker(self):
        while self.running:
            tasks_to_remove = []

            for payload, task_id in self.pending_task_ids:
                if not self.running:
                    break

                r = requests.get(f"{self.api_url}/tasks/view/{task_id}")

                if r.status_code == 500:
                    tasks_to_remove.append(task_id)
                else:
                    task_info = r.json()

                    if 'status' in task_info and task_info['status'] == "SUCCESS":
                        self.process_task_results(payload, task_id)
                        tasks_to_remove.append(task_id)

            self.pending_task_ids = [task for task in self.pending_task_ids if task[1] not in tasks_to_remove]

            time.sleep(2)

        print("Stopped LiSa task. Exiting...")
