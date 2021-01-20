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


def remove_noise(s):
    """
    Replaces annoying substrings with space characters

    Args:
        s (str): The string to be filtered from noise

    Returns:
        str: The string with noise removed
    """
    for x in [";", "${IFS}", "\"", "'", "`", "+"]:
        if x in s:
            s = s.replace(x, " ")
    return s


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
        self.__is_online()

    def __is_online(self):
        try:
            r = requests.get(f"{self.api_url}/tasks?limit=1")
            r.raise_for_status()
        except Exception:
            print("- Error: LiSa Server could not be reached. Is it running?")
            self.running = False

    def __create_entry(self, ip_address, payload, heuristics):
        geodata = geoip_info(ip_address)

        if not geodata:
            return None

        hostname = get_ip_hostname(ip_address)

        geo = db.geodata_create_or_update(
            ip_address,
            hostname,
            "C2 Server",
            geodata
        )

        db.candidate_c2_create_or_update(
            ip_address=geo.id,
            payload_ids=[payload.id],
            heuristics=heuristics
        )

        return geo

    def __check_requests_chmod(self, ip_address, analysis):
        for req in analysis['network_analysis']['http_requests']:
            if 'headers' in req and ip_address in req['headers'].get('Host', ''):
                if "chmod" in req['uri'] or "chmod" in req['headers'].get('SOAPAction', ''):
                    return True

        return False

    def __is_private_ip(self, ip):
        ip_info = IP(ip)
        return ip_info.iptype() == 'PRIVATE'

    def __process_task_result(self, payload, task_id):
        candidate_C2s = []
        ip_checker = DNSBLIpChecker(providers=providers)

        time.sleep(1)

        self.processing_task_ids.append(task_id)

        response = requests.get(f"{self.api_url}/report/{task_id}")
        analysis = response.json() if response.json() else None

        for endpoint in analysis['network_analysis']['endpoints']:
            ip_address = endpoint['ip']

            if self.__is_private_ip(ip_address) or self.__check_requests_chmod(ip_address, analysis):
                continue

            heuristics = []

            is_transaction = endpoint['data_in'] > 0 and endpoint['data_out'] > 0
            is_hardcoded_s = any(ip_address in s for s in analysis['static_analysis']['strings'])
            is_blacklisted = DNSBL_CATEGORY_CNC in ip_checker.check(ip_address).categories

            if is_transaction:
                heuristics.append("Data transaction from IP")

            if is_blacklisted:
                heuristics.append("Blacklisted C2 IP")

            if is_hardcoded_s:
                heuristics.append("Hard-coded IP")

            if heuristics:
                geo = self.__create_entry(ip_address, payload, heuristics)

                if geo:
                    candidate_C2s.append(geo)
                    self.count_c2s += 1

        analysis['binary_info'] = analysis['static_analysis']['binary_info'].copy()
        analysis['task_id'] = task_id

        del analysis['static_analysis']
        del analysis['dynamic_analysis']
        del analysis['network_analysis']

        payload.update(
            set__lisa=analysis,
            set__candidate_C2s=candidate_C2s
        )

        self.complete_task_ids.append(task_id)
        self.processing_task_ids.remove(task_id)

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
                        # self.__process_task_result(payload, task_id)
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
                    f"complete: {len(self.complete_task_ids)} | "
                    f"possible C2s: {self.count_c2s} {'...' if self.blink else '   '}"
                ), end="")

            if self.pending_task_ids:
                self.__check_tasks()

            elif (not self.adding_tasks) and (not self.processing_task_ids) and self.processing:
                print(f"\n- [LiSa] Finished Analysis: Identified {self.count_c2s} candidate C2 Servers from {len(self.complete_task_ids)} analysis tasks.", flush=True)
                self.__reset()

            time.sleep(5)

        self.executor.shutdown(wait=True, cancel_futures=True)
        print("- LiSa API: Stopped task checker.", flush=True)

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

    def stop(self):
        self.running = False
