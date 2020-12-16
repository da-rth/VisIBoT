import requests
import threading
import time
import pydnsbl
from IPy import IP


ip_checker = pydnsbl.DNSBLIpChecker()


class LiSaAPI:

    def __init__(self, api_url):
        self.api_url = api_url
        self.pending_task_ids = []
        t = threading.Thread(name='init_task_checker', target=self.init_task_checker)
        t.start()

    def create_file_task(self, payload):
        r = requests.post(f"{self.api_url}/tasks/create/file", {'url': payload.url})
        data = r.json()

        if "error" in data:
            payload.vt_result['processing'] = None
            payload.save()
        elif r.status_code and r.status_code == 200:
            task_id = r.json()['task_id']
            self.pending_task_ids.append([payload, task_id])
            return True

    def process_task_results(self, payload, task_id):
        print("Processing Results")
        r = requests.get(f"{self.api_url}/report/{task_id}")
        if r.statis_code == 200:
            analysis = r.json()

            strings = analysis['static_analysis']['strings']
            endpoints_out = analysis['dynamic_analysis']['endpoints']

            payload.vt_result = analysis['virustotal']
            payload.vt_result['processing'] = False
            payload.save()

            candidate_servers = []

            for endpoint in endpoints_out:
                ip_address = IP(endpoint['ip'])

                if ip_address.iptype() == 'PRIVATE':
                    continue
                elif endpoint['blacklisted']:
                    candidate_servers.append(endpoint)
                elif ip_checker.check(str(ip_address)).blacklisted:
                    candidate_servers.append(endpoint)
                elif endpoint['data_in'] > 0:
                    candidate_servers.append(endpoint)
            # get payload from db
            # Store virustotal results in payload record
            # parse endpoints
            # parse strings for IP addresses
            # print(json.dumps(virus_total, indent=1))
            print(f"success | strings: {len(strings)} | candidate servers: {len(candidate_servers)}")

    def init_task_checker(self):
        while True:
            while self.pending_task_ids:
                payload, task_id = self.pending_task_ids[0]
                r = requests.get(f"{self.api_url}/tasks/view/{task_id}")
                data = r.json()
                if 'status' in data and data['status'] == "SUCCESS":
                    self.pending_task_ids.pop()
                    self.process_task_results(payload, task_id)

                time.sleep(2)
