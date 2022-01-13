import logging

def setting_test():
    from setting.settingReader import setting
    logging.info(f"Get setting: {setting}")

def proxyFetcher_test():
    from fetcher.proxyFetcher import ProxyFetcher 
    proxy_fetcher = ProxyFetcher()
    print(proxy_fetcher.get_proxy())

def biliApi_test():
    from fetcher.biliApi import BiliApi
    bili_api = BiliApi()
    print(bili_api.get_cid_by_bid("BV1Nq4y1A7Vk"))
    l = bili_api.get_up_video_by_mid(347235)
    print(l[:4])
    cid = bili_api.get_cid_by_aid(l[0]["aid"])
    print(cid)
    danmaku = bili_api.get_danmaku_list_by_cid(cid)
    print(danmaku[:8])

def CommentFetcher_test():
    from helper.fetch import CommentFetcher
    t = CommentFetcher()
    t.start()
    t.join()

if __name__ == '__main__':
    CommentFetcher_test()