import logging

from api.biliApi import BiliApi

logging.basicConfig(level=logging.INFO)

def setting_test():
    from setting.settingReader import setting
    logging.info(f"Get setting: {setting}")

def proxyApi_test():
    from api.proxyApi import ProxyApi
    proxy_api = ProxyApi()
    print(proxy_api.get_proxy())

def biliApi_test():
    from api.biliApi import BiliApi
    bili_api = BiliApi()
    print(bili_api.get_cid_by_bid("BV1Nq4y1A7Vk"))
    l = bili_api.get_up_video_by_mid(347235)
    print(l[:4])
    cid = bili_api.get_cid_by_aid(l[0]["aid"])
    print(cid)
    danmaku = bili_api.get_danmaku_list_by_cid(cid)
    print(danmaku[:8])
    followings = bili_api.get_following_by_mid(385842994)
    print(followings[:10])
    relations = bili_api.get_relationship_info_by_mid(385842994)
    print(relations)

def DanmakuFetcher_test():
    from helper.fetch import DanmakuFetcher
    t = DanmakuFetcher()
    t.start()
    t.join()

def UserFollowingFetcher_test():
    from helper.fetch import UserFollowingFetcher
    t = UserFollowingFetcher()
    t.start()
    t.join()

if __name__ == '__main__':
    DanmakuFetcher_test()