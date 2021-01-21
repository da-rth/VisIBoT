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
        self.all_CNCs = set()
        self.all_P2Ps = set()
        self.adding_tasks = False
        self.executor = ThreadPoolExecutorStackTraced(max_workers=4)
        self.p2p_routers = [
            "router.utorrent.com",
            "dht.transmissionbt.com",
            "router.bittorrent.com",
            "bttracker.debian.org",
        ]
        self.spreading_keywords = [
            "chmod",
            "wget",
            "curl",
            "tftp"
            "/tmp",
            "http"
        ]
        self.__is_online()

    def __is_online(self):
        try:
            r = requests.get(f"{self.api_url}/tasks?limit=1")
            r.raise_for_status()
        except Exception:
            print("- Error: LiSa Server could not be reached. Is it running?")
            self.running = False

    def __create_geo_entry(self, ip_address, geo_type):
        geodata = geoip_info(ip_address)

        if not geodata:
            return None

        hostname = get_ip_hostname(ip_address)

        return db.geodata_create_or_update(
            ip_address,
            hostname,
            geo_type,
            geodata
        )

    def __create_cnc_entry(self, geo, payload, heuristics):
        return db.candidate_cnc_create_or_update(
            ip_address=geo.id,
            payload_ids=[payload.id],
            heuristics=heuristics
        )

    def __create_p2p_entry(self, geo, payload, heuristics, nodes):
        return db.candidate_p2p_create_or_update(
            ip_address=geo.id,
            payload_ids=[payload.id],
            heuristics=heuristics,
            nodes=nodes
        )

    def __is_endpoint_spreading(self, ip_address, analysis):
        for req in analysis['network_analysis']['http_requests']:
            if 'headers' in req and ip_address in req['headers'].get('Host', ''):
                uri_has_keyword = any(s in req['uri'] for s in self.spreading_keywords)
                soap_has_keyword = any(s in req['headers'].get('SOAPAction', '') for s in self.spreading_keywords)

                if uri_has_keyword or soap_has_keyword:
                    return True

        return False

    def __is_private_ip(self, ip):
        ip_info = IP(ip)
        return ip_info.iptype() == 'PRIVATE'

    def __is_p2p(self, analysis):
        for dns_q in analysis['network_analysis']['dns_questions']:
            if dns_q.get('name', None) in self.p2p_routers:
                return True
        """
        for string in analysis['static_analysis']['strings']:
            if any(string in router for router in self.p2p_routers):
                return True
        """
        return False

    def __process_task_result(self, payload, task_id):
        ip_checker = DNSBLIpChecker(providers=providers)

        candidate_CNCs = []
        candidate_P2Ps = []

        time.sleep(1)

        self.processing_task_ids.append(task_id)

        response = requests.get(f"{self.api_url}/report/{task_id}")
        analysis = response.json() if response.json() else None
        is_p2p = self.__is_p2p(analysis)

        for endpoint in analysis['network_analysis']['endpoints']:
            heuristics = []
            ip_address = endpoint['ip']

            if self.__is_private_ip(ip_address) or self.__is_endpoint_spreading(ip_address, analysis):
                continue

            heuristics = self.__identify_heuristics(
                endpoint,
                analysis['static_analysis']['strings'],
                ip_checker
            )

            if heuristics:
                geo_type = "P2P Node" if is_p2p else "C2 Server"
                geo = self.__create_geo_entry(ip_address, geo_type)

                if geo:
                    if is_p2p:
                        candidate_P2Ps.append((geo, heuristics))
                        self.all_P2Ps.add(geo.id)
                    else:
                        candidate_CNCs.append((geo, heuristics))
                        self.all_CNCs.add(geo.id)

        for node_geo, heuristics in candidate_P2Ps:
            nodes = list(set(n.id for n, _ in candidate_P2Ps if n.id != node_geo.id))
            self.__create_p2p_entry(node_geo, payload, heuristics, nodes)

        for cnc_geo, heuristics in candidate_CNCs:
            self.__create_cnc_entry(cnc_geo, payload, heuristics)

        analysis['task_id'] = task_id
        analysis['payload'] = payload

        self.__process_payload(payload, analysis, candidate_CNCs, candidate_P2Ps)

        self.complete_task_ids.append(task_id)
        self.processing_task_ids.remove(task_id)

    def __identify_heuristics(self, endpoint, strings, ip_checker):
        heuristics = []

        blacklist_categories = ip_checker.check(endpoint['ip']).categories

        if (endpoint['data_in'] > 0) and (endpoint['data_out'] == 0):
            heuristics.append("Data in-only from IP")

        if (endpoint['data_in'] > 0) and (endpoint['data_out'] > 0):
            heuristics.append("Data in-out from IP")

        if any(endpoint['ip'] in s for s in strings):
            heuristics.append("Blacklisted C2 IP")

        if DNSBL_CATEGORY_CNC in blacklist_categories:
            heuristics.append("Connection to hard-coded IP")

        return heuristics

    def __process_payload(self, payload, analysis, candidate_CNCs, candidate_P2Ps):
        lisa_analysis = db.lisa_analysis_create_or_update(analysis)

        cnc_geos = [geo.id for geo, _ in candidate_CNCs]
        p2p_geos = [geo.id for geo, _ in candidate_P2Ps]

        payload.update(
            set__lisa=lisa_analysis,
            add_to_set__candidate_C2s=cnc_geos,
            add_to_set__candidate_P2Ps=p2p_geos,
        )

        all_ips = cnc_geos + p2p_geos

        if all_ips:
            db.geo_connections_create_or_update(payload.ip_address, all_ips)

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
                        # self.executor.submit(self.__process_task_result, payload, task_id)
                        self.__process_task_result(payload, task_id)
                    tasks_to_remove.append(task_id)

        self.pending_task_ids = [t for t in self.pending_task_ids if t[1] not in tasks_to_remove]

    def __reset(self):
        self.processing = False
        self.all_CNCs = set()
        self.all_P2Ps = set()
        self.pending_task_ids = []
        self.complete_task_ids = []
        self.processing_task_ids = []

    def init_task_checker(self):
        print("- Initialized LiSa malware sandbox task loop")

        while self.running:
            if (self.pending_task_ids or self.processing_task_ids) and not self.adding_tasks:
                self.blink = not self.blink
                print(
                    f"\r- [LiSa] Tasks pending: {len(self.pending_task_ids)} |",
                    f"processing: {len(self.processing_task_ids)} |",
                    f"complete: {len(self.complete_task_ids)} |",
                    f"possible C2s: {len(self.all_CNCs)} |",
                    f"possible P2Ps: {len(self.all_P2Ps)}",
                    f"{'...' if self.blink else '   '}",
                    end=""
                )

            if self.pending_task_ids:
                self.__check_tasks()

            elif (not self.adding_tasks) and (not self.processing_task_ids) and self.processing:
                print(
                    f"\n- [LiSa] Finished Analysis: Identified {len(self.all_CNCs)} C2 Servers",
                    f"and {len(self.all_P2Ps)} P2P Nodes from {len(self.complete_task_ids)} analysis",
                    "tasks.",
                    flush=True
                )
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
