from virus_total_apis import PublicApi as VirusTotalPublicApi
from ratelimit import limits, RateLimitException
from backoff import on_exception, expo

API_CALLS = 1000
API_PERIOD = 60


class VirusTotalURLProcessor:

    def __init__(self, api_key):
        self.api = VirusTotalPublicApi(api_key)
        self.api_services = {
            "scan": self.api.scan_url,
            "check": self.api.get_url_report,
        }

    def store_result(self, response, processing=False):
        """
        Given a response, return data in reduced form.
        Only add fields "positives" and "total" if result is done processing.

        Args:
            response (dict): The VT response dict to be reduced
            processing (bool, optional):
                Specifies if the result is currently being processed by VT.
                Defaults to False.

        Returns:
            dict: The response dict in reduced form
        """
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
    @limits(calls=API_CALLS, period=API_PERIOD)
    def api_request(self, req_type, url):
        """
        Allows for various VT API calls to be made while ensuring
        rate limit is respected. If rate limit occurs, try again in 30 seconds.

        Args:
            req_type (str): The type of VT request
            url (str): The URL to be checked by VirusTotal

        Raises:
            RateLimitException: When number of requests exceeds rate limit

        Returns:
            dict: The response object from the VT endpoint
        """
        response = self.api_services[req_type](url)

        if response['response_code'] == 204:
            raise RateLimitException("VirusTotal Rate Limit Exceeded", 60)

        return response

    def scan_url(self, url):
        """
        Scans a URL using rate-limited VT API endpoints and returns result.

        Args:
            url (str): The URL to be scanned by VirusTotal

        Returns:
            dict: The results from request in reduced dict form
            bool: False if no results are obtained from query
        """
        response = self.api_request("scan", url)

        if 'results' in response and response['results']['response_code'] == 1:
            return self.store_result(response, processing=True)
        return False

    def process_url(self, url):
        """
        Checks for an existing report for a URL using rate-limited VT API endpoints.
        If report exists, return result data in dict form.
        Otherwise, get report of URL and store results.

        Args:
            url (str): The URL to be scanned by VirusTotal

        Returns:
            bool: Returns False if no result is obtained (e.g. bad URL format)
            dict: Returns the results of the report or scan in reduced dict form
        """
        response = self.api_request("check", url)

        if 'results' in response:
            if response['results']['response_code'] == 0:
                return self.scan_url(url)
            elif response['results']['response_code'] == 1:
                return self.store_result(response, processing=False)

        return False

if __name__ == "__main__":
    import os
    vtapi = VirusTotalURLProcessor(os.getenv("VIRUSTOTAL_API_KEY"))
    print(vtapi.process_url("http://117.20.205.13:2779/Mozi.a;chmod"))