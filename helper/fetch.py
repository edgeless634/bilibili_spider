import logging
from random import random
from threading import Thread
from fetcher.biliApi import BiliApi
from setting.settingReader import setting
from utils.datafields import datafields
import time

from utils.randomsleep import random_sleep

class BaseFetcher(Thread):
    def __init__(self):
        super().__init__()
        self.__up_field = ""
        self.__down_field = ""

    @property
    def up_field(self):
        return self.__up_field
    
    @up_field.setter
    def up_field(self, up_field):
        self.__up_field = up_field
        datafields.new_field(self.__up_field)

    @property
    def down_field(self):
        return self.__down_field
    
    @down_field.setter
    def down_field(self, down_field):
        self.__down_field = down_field
        datafields.new_field(self.__down_field)
    

class DanmakuFetcher(BaseFetcher):

    def __init__(self):
        super().__init__()
        self.up_field = "up_mid"
        self.down_field = "video_danmaku"
        self.sleep_time_each = setting["DanmakuFetcher"]["wait_time_each"]
        self.sleep_time_each_step = setting["DanmakuFetcher"]["wait_time_each_step"]
        self.found_up = set()
        self.BiliApi = BiliApi()

        self.done_mid_field = "mid_done"
        datafields.new_field(self.done_mid_field)
        self.done_mid_field_save_name = f"{str(self.name.__hash__())[:8]}.txt"
        self.load_found_up()

        self.found_aid = set()

        self.done_aid_field = "aid_done"
        datafields.new_field(self.done_aid_field)
        self.done_aid_field_save_name = f"{str(self.name.__hash__())[:8]}.txt"
        self.load_found_aid()
    
    def load_found_up(self):
        l = "\n".join(datafields.load_field_data(self.done_mid_field)).split("\n")
        self.found_up.update(set([int(i) for i in l if i != ""]))

    def load_found_aid(self):
        l = "\n".join(datafields.load_field_data(self.done_aid_field)).split("\n")
        self.found_aid.update(set([int(i) for i in l if i != ""]))

    def get_up_mid(self):
        while True:
            time.sleep(self.sleep_time_each_step)
            up_mid = datafields.get_field_data(self.up_field)
            if up_mid is None:
                return
            if up_mid not in self.found_up:
                yield up_mid
                self.found_up.add(up_mid)
    
    def save_video_danmaku(self, mid: int):
        for video in self.BiliApi.get_up_video_by_mid(mid):
            t = time.perf_counter()

            aid = video["aid"]
            if aid in self.found_aid:
                logging.info(f"[DanmakuFetcher] Ignore, as it is downloaded: {aid}")
                time.sleep(self.sleep_time_each_step)
                continue
            cid = self.BiliApi.get_cid_by_aid(aid)
            time.sleep(self.sleep_time_each_step)
            danmaku = self.BiliApi.get_danmaku_list_by_cid(cid)
            datafields.save_to_field(self.down_field, "\n".join(danmaku), filename=f"{aid}.txt")
            logging.info(f"[DanmakuFetcher] Saved: {aid}")
            datafields.save_to_field(self.done_aid_field, "\n"+str(aid), filename=self.done_aid_field_save_name, mode="a")

            use_time = time.perf_counter() - t
            sleep_time = self.sleep_time_each - use_time
            if sleep_time > 0:
                random_sleep(sleep_time)
        datafields.save_to_field(self.done_mid_field, "\n"+str(mid), filename=self.done_mid_field_save_name, mode="a")

    def run(self):
        for mid in self.get_up_mid():
            self.save_video_danmaku(mid)


class UserFollowingFetcher(BaseFetcher):
    def __init__(self):
        super().__init__()
        self.up_field = "up_mid"
        self.down_field = "up_mid"
        self.sleep_time_each = setting["UserFollowingFetcher"]["wait_time_each"]
        self.sleep_time_each_step = setting["UserFollowingFetcher"]["wait_time_each_step"]
        self.found_mid = set()
        self.biliApi = BiliApi()
    
    def get_mid(self):
        while True:
            mid = datafields.get_field_data(self.up_field)
            if mid is None:
                return
            if mid not in self.found_mid:
                yield mid
                self.found_mid.add(mid)
    
    def save_user_following(self, mid):
        logging.info(f"[UserFollowingFetcher] Start scanning: {mid}")
        followings = self.biliApi.get_following_by_mid(mid)

        followings_filtered = []

        def filter_following(mid):
            logging.info(f"[UserFollowingFetcher] Checking: {mid}")
            ret = self.biliApi.get_user_fans_num_by_mid(mid)
            if ret is None:
                return self.biliApi.get_user_level_by_mid(mid) > 4
            elif ret < 1000:
                return False
            return True

        for follow_mid in followings:
            t = time.perf_counter()

            if filter_following(follow_mid):
                followings_filtered.append(follow_mid)
                datafields.save_to_field(self.down_field, f"\n{follow_mid}", filename=f"{mid}_followings.txt", mode="a")
            
            use_time = time.perf_counter() - t
            sleep_time = self.sleep_time_each_step - use_time
            if sleep_time > 0:
                random_sleep(sleep_time)

    
    def run(self):
        for mid in self.get_mid():
            t = time.perf_counter()

            self.save_user_following(mid)

            use_time = time.perf_counter() - t
            sleep_time = self.sleep_time_each - use_time
            if sleep_time > 0:
                random_sleep(sleep_time)
