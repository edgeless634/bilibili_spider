from setting.settingReader import setting
from utils import userAgent
from utils import bid
from bs4 import BeautifulSoup
import requests
import logging
import time
import json

class BiliApi:
    def __init__(self):
        self.headers = {
            "User-Agent": userAgent.get_user_agent()
        }
        self.__timeout = 5
        if setting["proxyFetch"]["enable"] is True:
            from fetcher.proxyFetcher import ProxyFetcher
            proxy_fetcher = ProxyFetcher()
            proxy = proxy_fetcher.get_proxy()
            self.proxies = {
                "http": proxy,
                "https": proxy
            }
        else:
            self.proxies = {}

    def get_cid_by_aid(self, input_aid: int) -> int:
        '''
        根据视频aid(即AV号)返回视频的cid
        '''
        url = "https://api.bilibili.com/x/player/pagelist"
        while True:
            try:
                r = requests.get(
                    url,
                    headers=self.headers,
                    params = {"aid": input_aid},
                    proxies = self.proxies,
                    timeout=self.__timeout
                )
                r.encoding = r.apparent_encoding
                d = json.loads(r.text)
                if d["code"] == 0:
                    break
            except requests.exceptions.RequestException:
                pass
        return d["data"][0]["cid"]
    
    def get_cid_by_bid(self, input_bid: str) -> int:
        '''
        根据视频bid(即BV号)返回视频的cid
        '''
        assert input_bid[:2] == "BV", "The starting of bid should be BV! Receive: {}".format(input_bid)
        input_aid = bid.decode(input_bid)
        return self.get_cid_by_aid(input_aid)

    def get_danmaku_list_by_cid(self, input_cid: int) -> list:
        '''
        根据视频cid返回弹幕列表，弹幕列表根据发送位置进行排序
        '''
        url = "https://comment.bilibili.com/{}.xml".format(input_cid)

        while True:
            try:
                r = requests.get(
                    url,
                    headers=self.headers,
                    timeout=self.__timeout,
                    proxies=self.proxies,
                )
                r.encoding = r.apparent_encoding
                soup = BeautifulSoup(r.text, "lxml")
                break
            except requests.exceptions.RequestException:
                pass
        l = [(i.text, float(i.attrs["p"].split(",")[0])) for i in soup.select("d")]
        l.sort(key = lambda x: x[1])
        return [i[0] for i in l]

    def get_up_video_by_mid(self, input_mid: int) -> list:
        '''
        根据up主的id返回Ta的视频
        返回格式: [{"title": title, "aid": aid}, ]
        '''
        url = "https://api.bilibili.com/x/space/arc/search"
        ret = []
        for pn in range(1, 10000000):
            while True:
                try:
                    r = requests.get(
                        url,
                        headers=self.headers,
                        params = {"mid": input_mid, "pn": pn},
                        proxies=self.proxies,
                        timeout=self.__timeout
                    )
                    r.encoding = r.apparent_encoding
                    d = json.loads(r.text)
                    if d["code"] == 0:
                        break
                    else:
                        logging.warning(f"[get_up_video_by_mid]网络错误: {d}")
                        time.sleep(1)
                except requests.exceptions.RequestException as e:
                    logging.warning(f"[get_up_video_by_mid]网络不稳定：{e}")
                    time.sleep(1)

            videos = d["data"]["list"]["vlist"]
            assert isinstance(videos, list)

            for video_data in videos:
                ret.append({
                    "title": video_data["title"],
                    "aid": video_data["aid"],
                })

            video_count = d["data"]["page"]["count"]
            if pn * 30 > video_count:
                break
        return ret

    def change_user_agent(self, user_agent = userAgent.get_user_agent()):
        self.headers["User-Agent"] = user_agent
    
    @property
    def timeout(self):
        return self.timeout
    
    @timeout.setter
    def set_timeout(self, timeout):
        self.__timeout = timeout
