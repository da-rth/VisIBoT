from virus_total_apis import PublicApi as VirusTotalPublicApi
import os
import json

"""
VirusTotal Public API

Rate Limit: 4 requests/min

TODO: Look into: https://pypi.org/project/ratelimit/
"""

API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

MALWARE_URL = 'http://205.185.115.72/c'

vt = VirusTotalPublicApi(API_KEY)

# response = vt.scan_url(MALWARE_URL)
# response = vt.get_url_report(MALWARE_URL)
# print(json.dumps(response, sort_keys=False, indent=4))