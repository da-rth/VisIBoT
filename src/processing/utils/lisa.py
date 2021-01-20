# pylama:ignore=E402:ignore=E702
import sys; sys.path.append("..")
import database as db
import requests
import time
from .stack_thread import ThreadPoolExecutorStackTraced
from IPy import IP
from utils.misc import get_ip_hostname
from utils.geodata import geoip_info
from pydnsbl import DNSBLIpChecker
from pydnsbl.providers import Provider, DNSBL_CATEGORY_CNC


providers = [
    Provider('b.barracudacentral.org'),
    Provider('combined.abuse.ch'),
    Provider('drone.abuse.ch'),
    Provider('dyna.spamrats.com'),
    Provider('noptr.spamrats.com'),
    Provider('zombie.dnsbl.sorbs.net'),
    Provider('zen.spamhaus.org'),
]


class LiSaAPI:

    def __init__(self, api_url, exec_time=30):
        self.exec_time = exec_time
        self.blink = False
        self.running = True
        self.processing = False
        self.api_url = api_url
        self.processing_task_ids = []
        self.complete_task_ids = []
        self.pending_task_ids = []
        self.count_c2s = 0
        self.adding_tasks = False
        self.executor = ThreadPoolExecutorStackTraced(max_workers=4)
        self.__ping()

    def __ping(self):
        try:
            r = requests.get(f"{self.api_url}/tasks?limit=1")
            r.raise_for_status()
        except Exception:
            print("- Error: LiSa Server could not be reached. Is it running?")
            self.running = False

    def create_file_tasks(self, payloads):
        if self.running and payloads:
            self.processing = True
            self.adding_tasks = True
            created_tasks = 0
            failed_tasks = 0

            for i, payload in enumerate(payloads):
                try:
                    r = requests.post(f"{self.api_url}/tasks/create/file", {'url': payload.url, 'exec_time': self.exec_time})
                    task_id = r.json().get('task_id', None) if r.json() else None

                    if task_id:
                        self.pending_task_ids.append([payload, task_id])
                        created_tasks += 1
                    else:
                        failed_tasks += 1
                except Exception:
                    failed_tasks += 1

                print(f"\r- [LiSa] Creating tasks: {i+1}/{len(payloads)} | Created: {created_tasks} | Failed: {failed_tasks}", end="")

            self.adding_tasks = False

            if created_tasks > 0:
                print(f"\n- [LiSa] Monitoring malware analysis tasks (task exec time: {self.exec_time}s)")
            else:
                print("\n- [LiSa] No analysis tasks were created. All of the provided payload URLs are offline.")

    def __process_task_result(self, payload, task_id):
        time.sleep(1)
        ip_checker = DNSBLIpChecker(providers=providers)
        self.processing_task_ids.append(task_id)

        candidate_C2s = []
        response = requests.get(f"{self.api_url}/report/{task_id}")
        analysis = response.json() if response.json() else None

        strings = "".join(analysis['static_analysis']['strings'])
        endpoints = analysis['network_analysis']['endpoints'].copy()
        analysis['binary_info'] = analysis['static_analysis']['binary_info'].copy()

        del analysis['static_analysis']
        del analysis['dynamic_analysis']
        del analysis['network_analysis']

        for endpoint in endpoints:
            ip_str = endpoint['ip']
            ip_address = IP(ip_str)

            if ip_address.iptype() == 'PRIVATE':
                continue

            is_receive_only = endpoint['data_in'] > 0 and endpoint['data_out'] == 0
            is_hardcoded_s = endpoint['ip'] in strings
            is_blacklisted = DNSBL_CATEGORY_CNC in ip_checker.check(ip_str).categories

            heuristics = []

            if is_receive_only:
                heuristics.append("Received data from IP without exchange.")

            if is_blacklisted:
                heuristics.append("Blacklisted C2 IP")

            if is_hardcoded_s:
                heuristics.append("Hard-coded IP")

            if heuristics:
                ip_address = ip_str
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

                db.candidate_c2_create_or_update(
                    ip_address=c2_geo.id,
                    payload_ids=[payload.id],
                    heuristics=heuristics
                )

                candidate_C2s.append(c2_geo)
                self.count_c2s += 1

        payload.update(
            set__lisa=analysis,
            set__candidate_C2s=candidate_C2s
        )

        self.complete_task_ids.append(task_id)
        self.processing_task_ids.remove(task_id)

    def stop(self):
        self.running = False

    def __check_tasks(self):
        tasks_to_remove = []
        complete_tasks_list = {}
        r = requests.get(f"{self.api_url}/tasks?limit=20")
        tasks_list = r.json() if r.json() else []
        tasks_list = [task for task in tasks_list if isinstance(task, dict)]
        complete_tasks_list = {task['task_id']: task['status'] for task in tasks_list}

        for (payload, task_id) in self.pending_task_ids:
            if not self.running:
                break

            if task_id in complete_tasks_list:
                status = complete_tasks_list[task_id]

                if status:
                    if status == 'SUCCESS':
                        self.executor.submit(self.__process_task_result, payload, task_id)

                    tasks_to_remove.append(task_id)

        self.pending_task_ids = [t for t in self.pending_task_ids if t[1] not in tasks_to_remove]

    def __reset(self):
        self.processing = False
        self.count_c2s = 0
        self.pending_task_ids = []
        self.complete_task_ids = []
        self.processing_task_ids = []

    def init_task_checker(self):
        print("- Initialized LiSa malware sandbox task loop")

        while self.running:
            if (self.pending_task_ids or self.processing_task_ids) and not self.adding_tasks:
                self.blink = not self.blink
                print((
                    f"\r- [LiSa] Tasks pending: {len(self.pending_task_ids)} | "
                    f"processing: {len(self.processing_task_ids)} | "
                    f"complete: {len(self.complete_task_ids)} {'...' if self.blink else '   '}"
                ), end="")

            if self.pending_task_ids:
                self.__check_tasks()

            elif (not self.adding_tasks) and (not self.processing_task_ids) and self.processing:
                print(f"\n- [LiSa] Finished Analysis: Identified {self.count_c2s} candidate C2 Servers from {len(self.complete_task_ids)} analysis tasks.", flush=True)
                self.__reset()

            time.sleep(5)

        self.executor.shutdown(wait=True, cancel_futures=True)
        print("- LiSa API: Stopped task checker.", flush=True)
