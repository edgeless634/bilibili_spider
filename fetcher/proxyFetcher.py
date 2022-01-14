from setting.settingReader import setting
from utils.randomsleep import random_sleep
import requests
import logging
import json
import time

class ProxyFetcher:

    def __init__(self):
        self.api_url = setting["proxyFetch"]["api_url"]
        self.proxies = {
            "http": setting["proxyFetch"]["proxy_for_proxyfetch"],
            "https": setting["proxyFetch"]["proxy_for_proxyfetch"],
        }
        
    def get_proxy(self):
        while True:
            try:
                r = requests.get(self.api_url, params={"type": "https"}, proxies=self.proxies)
                d = json.loads(r.text)
                if "proxy" not in d:
                    logging.warning(f"No proxy for now, wait for 5s.")
                    random_sleep(5)
                    continue
                break
            except requests.exceptions.RequestException:
                pass
        print(d)
        return "http://" + d["proxy"]

if __name__ == '__main__':
    o = ProxyFetcher()
    print(o.get_proxy())