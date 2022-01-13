import logging
from threading import Thread
from fetcher.biliApi import BiliApi
from setting.settingReader import setting
from utils.datafields import datafields
import time

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
    

class CommentFetcher(BaseFetcher):

    def __init__(self):
        super().__init__()
        self.up_field = "up_mid"
        self.down_field = "video_comment"
        self.sleep_time_each = setting["commentFetcher"]["wait_time_each"]
        self.found_up = set()
        self.BiliApi = BiliApi()

    def get_up_mid(self):
        while True:
            up_mid = datafields.get_field_data(self.up_field)
            if up_mid is None:
                return
            if up_mid not in self.found_up:
                yield up_mid
                self.found_up.add(up_mid)
    
    def save_video_comment(self, mid: int):
        for video in self.BiliApi.get_up_video_by_mid(mid):
            t = time.perf_counter()

            aid = video["aid"]
            cid = self.BiliApi.get_cid_by_aid(aid)
            comment = self.BiliApi.get_danmaku_list_by_cid(cid)
            datafields.save_to_field(self.down_field, "\n".join(comment), filename=f"{aid}.txt")
            logging.info(f"[save_video_comment] Saved: {aid}")

            use_time = time.perf_counter() - t
            sleep_time = self.sleep_time_each - use_time
            if sleep_time > 0:
                time.sleep(sleep_time)

    def run(self):
        for mid in self.get_up_mid():
            self.save_video_comment(mid)
    
