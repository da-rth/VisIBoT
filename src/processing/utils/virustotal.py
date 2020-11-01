from virus_total_apis import PublicApi as VirusTotalPublicApi
import time

class VirusTotalURLProcessor:

    def __init__(self, api_key):
        self.api = VirusTotalPublicApi(api_key)#
        self.queue = []
        self.current_url = None
        self.running = True


    def init(self):
        print("Starting VT URL Processor...")
        while self.running:
            if self.queue:
                self.current_url = self.queue.pop()
                print("Processing:", self.current_url)
                self.process_url()

            time.sleep(0.5)


    def stop(self):
        self.runing = False
        print("Stopping VT URL Processor...")


    def add_job(self, url):
        self.queue.append(url)


    def hit_rate_limit(self, response):
        limit_reached = response['response_code'] == 204

        if limit_reached:
            print("Hit rate limit... Sleeping 15 seconds")
            time.sleep(15)

        return limit_reached


    def store_result(self, response):
        # result = response['results']
        print("TODO: Store data")


    def handle_invalid_url(self):
        print("TODO: Handle Invalid URL")


    def scan_url(self):
        response = self.api.scan_url(self.current_url)

        if not self.hit_rate_limit(response):
            if 'results' in response and response['results']['response_code'] == 1:
                self.store_result(response)
            else:
                self.handle_invalid_url()
        else:
            self.scan_url()


    def process_url(self):
        response = self.api.get_url_report(self.current_url)

        if not self.hit_rate_limit(response):
            if 'results' in response:
                if response['results']['response_code'] == 0:
                    return self.scan_url()
                elif response['results']['response_code'] == 1:
                    return self.store_result(response)
            self.handle_invalid_url()
        else:
            self.process_url()


