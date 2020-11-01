from virus_total_apis import PublicApi as VirusTotalPublicApi
from ratelimit import limits, RateLimitException
from backoff import on_exception, expo


class VirusTotalURLProcessor:

    def __init__(self, api_key):
        self.api = VirusTotalPublicApi(api_key)
        self.api_services = {
            "scan": self.api.scan_url,
            "check": self.api.get_url_report,
        }

    def store_result(self, response, processing=False):
        result = response['results']

        res = {
            "scan_url": result['permalink'],
            "scan_id": result['scan_id'],
            "scan_date": result['scan_date'],
            "processing": processing,
        }

        if not processing:
            res["positives"] = result["positives"]
            res["total"] = result["total"]

        return res

    @on_exception(expo, RateLimitException)
    @limits(calls=4, period=20)
    def api_request(self, req_type, url):
        response = self.api_services[req_type](url)

        if response['response_code'] == 204:
            raise RateLimitException("VirusTotal Rate Limit Exceeded", 60)

        return response

    def scan_url(self, url):
        response = self.api_request("scan", url)

        if 'results' in response and response['results']['response_code'] == 1:
            return self.store_result(response, processing=True)
        return False

    def process_url(self, url):
        response = self.api_request("check", url)

        if 'results' in response:
            if response['results']['response_code'] == 0:
                return self.scan_url(url)
            elif response['results']['response_code'] == 1:
                return self.store_result(response, processing=False)

        return False
