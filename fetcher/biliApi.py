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
                        logging.warning(f"[get_up_video_by_mid]网络错误: {d}, {input_mid}")
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

    def get_user_info_by_mid(self, input_mid: int):
        '''
        获取用户基本信息
        '''
        url = "https://api.bilibili.com/x/relation/stat"
        while True:
            try:
                r = requests.get(
                    url,
                    headers=self.headers,
                    params = {"vmid": input_mid, "jsonp": "jsonp"},
                    proxies = self.proxies,
                    timeout=self.__timeout
                )
                r.encoding = r.apparent_encoding
                d = json.loads(r.text)
                if d["code"] == 0 or d["code"] == 22115:
                    # {'code': 22115, 'message': '用户已设置隐私，无法查看', 'ttl': 1}
                    break
            except requests.exceptions.RequestException:
                pass
        if d["code"] == 22115:
            return None
        return d["data"]
    
    def get_user_level_by_mid(self, input_mid: int):
        '''
        获取用户的等级
        '''
        user_info = self.get_user_info_by_mid(input_mid)
        if user_info is None:
            return None
        return d["level"]

    def get_relationship_info_by_mid(self, input_mid: int):
        '''
        获取用户关注和粉丝数
        '''
        url = "https://api.bilibili.com/x/relation/stat"
        while True:
            try:
                r = requests.get(
                    url,
                    headers=self.headers,
                    params = {"vmid": input_mid, "jsonp": "jsonp"},
                    proxies = self.proxies,
                    timeout=self.__timeout
                )
                r.encoding = r.apparent_encoding
                d = json.loads(r.text)
                if d["code"] == 0 or d["code"] == 22115:
                    # {'code': 22115, 'message': '用户已设置隐私，无法查看', 'ttl': 1}
                    break
            except requests.exceptions.RequestException:
                pass
        if d["code"] == 22115:
            return None
        return d["data"]
    
    def get_user_fans_num_by_mid(self, input_mid: int) -> list:
        '''
        返回用户的粉丝数，如果没有权限则返回None
        '''
        relationship_info = self.get_user_info_by_mid(input_mid)
        if relationship_info is None:
            return None
        return relationship_info["follower"]


    def get_following_by_mid(self, input_mid: int) -> list:
        '''
        根据id返回Ta的关注
        返回格式: [mid, ]
        '''
        ret = []
        url = "https://api.bilibili.com/x/relation/followings"
        for pn in range(1, 10000000):
            while True:
                try:
                    r = requests.get(
                        url,
                        headers=self.headers,
                        params = {"vmid": input_mid, "pn": pn},
                        proxies=self.proxies,
                        timeout=self.__timeout
                    )
                    r.encoding = r.apparent_encoding
                    d = json.loads(r.text)
                    if d["code"] == 0 or d["code"] == 22115 or d["code"] == 22007:
                        # {'code': 22007, 'message': '限制只访问前5页', 'ttl': 1}
                        # {'code': 22115, 'message': '用户已设置隐私，无法查看', 'ttl': 1}
                        break
                    else:
                        logging.warning(f"[get_following_by_mid]网络错误: {d}")
                        time.sleep(1)
                except requests.exceptions.RequestException as e:
                    logging.warning(f"[get_following_by_mid]网络不稳定：{e}")
                    time.sleep(1)

            if d["code"] == 22115:
                # {'code': 22115, 'message': '用户已设置隐私，无法查看', 'ttl': 1}
                break

            if d["code"] == 22007:
                # {'code': 22007, 'message': '限制只访问前5页', 'ttl': 1}
                break

            followings = d["data"]["list"]
            assert isinstance(followings, list)

            for following_data in followings:
                ret.append(following_data["mid"])

            video_count = d["data"]["total"]
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
