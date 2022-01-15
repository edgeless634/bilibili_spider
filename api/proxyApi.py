from setting.settingReader import setting
from utils.randomsleep import random_sleep
import requests
import logging
import json
import time

class ProxyApi:

    def __init__(self):
        self.enable = setting["proxyApi"]["enable"]
        self.api_url = setting["proxyApi"]["api_url"]
        self.proxies = {
            "http": setting["proxyApi"]["proxy_for_proxyapi"],
            "https": setting["proxyApi"]["proxy_for_proxyapi"],
        }
        
    def get_proxy(self):
        '''
        从proxy_pool项目中获取代理
        格式为http://xxx.xxx.xxx.xxx:xxxxx
        如果功能未开启则返回""
        '''
        if not self.enable:
            return ""
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
        return "http://" + d["proxy"]

if __name__ == '__main__':
    o = ProxyApi()
    print(o.get_proxy())