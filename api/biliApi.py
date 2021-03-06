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
        self.use_proxy = setting["proxyApi"]["enable"]
        if self.use_proxy:
            self.change_proxy()
        else:
            self.proxies = {}

    def change_proxy(self):
        '''
        更改代理
        '''
        if not self.use_proxy:
            return
        from api.proxyApi import ProxyApi
        proxy_api = ProxyApi()
        proxy = proxy_api.get_proxy()
        self.proxies = {
            "http": proxy,
            "https": proxy
        }

    def __base_get_bili_api(self, url, params):
        '''
        从Bilibili的API中获取信息
        '''
        while True:
            try:
                r = requests.get(
                    url,
                    headers=self.headers,
                    params = params,
                    proxies = self.proxies,
                    timeout=self.__timeout
                )
                r.encoding = r.apparent_encoding
                d = json.loads(r.text)
                if d["code"] == 0 or d["code"] == 22115 or d["code"] == 22007:
                    # {'code': 22007, 'message': '限制只访问前5页', 'ttl': 1}
                    # {'code': 22115, 'message': '用户已设置隐私，无法查看', 'ttl': 1}
                    break
                self.change_proxy()
                self.change_user_agent()
                logging.info(f"[BiliApi] proxy changed: {params}")
            except requests.exceptions.RequestException:
                self.change_proxy()
                self.change_user_agent()
        if d["code"] == 22115 or d["code"] == 22007:
            return None
        return d["data"]

    def get_cid_by_aid(self, input_aid: int) -> int:
        '''
        根据视频aid(即AV号)返回视频的cid
        '''
        url = "https://api.bilibili.com/x/player/pagelist"
        params = {"aid": input_aid}
        data = self.__base_get_bili_api(url, params)
        if data is None:
            return None
        return data[0]["cid"]
    
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
                self.change_proxy()
                self.change_user_agent()
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
            params = {"mid": input_mid, "pn": pn}
            data = self.__base_get_bili_api(url, params)

            if data is None:
                break
            videos = data["list"]["vlist"]
            assert isinstance(videos, list)

            for video_data in videos:
                ret.append({
                    "title": video_data["title"],
                    "aid": video_data["aid"],
                })

            video_count = data["page"]["count"]
            if pn * 30 > video_count:
                break
        return ret

    def get_user_info_by_mid(self, input_mid: int):
        '''
        获取用户基本信息
        '''
        url = "https://api.bilibili.com/x/relation/stat"
        params = {"vmid": input_mid, "jsonp": "jsonp"}
        return self.__base_get_bili_api(url, params)
    
    def get_user_level_by_mid(self, input_mid: int):
        '''
        获取用户的等级
        '''
        user_info = self.get_user_info_by_mid(input_mid)
        if user_info is None:
            return None
        return user_info["level"]

    def get_relationship_info_by_mid(self, input_mid: int):
        '''
        获取用户关注和粉丝数
        '''
        url = "https://api.bilibili.com/x/relation/stat"
        params = {"vmid": input_mid, "jsonp": "jsonp"}
        return self.__base_get_bili_api(url, params)
    
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
            params = {"vmid": input_mid, "pn": pn}
            data = self.__base_get_bili_api(url, params)
            if data is None:
                break
            followings = data["list"]
            assert isinstance(followings, list)

            for following_data in followings:
                ret.append(following_data["mid"])

            video_count = data["total"]
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
