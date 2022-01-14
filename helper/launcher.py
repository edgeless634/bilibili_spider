from helper.fetch import DanmakuFetcher, UserFollowingFetcher
from setting.settingReader import setting

def get_danmaku_fetchers_threads():
    thread_num = setting["launcher"]["danmaku_fetcher_thread_num"]
    threads = [DanmakuFetcher() for _ in range(thread_num)]
    return threads

def get_user_following_fetchers_threads():
    thread_num = setting["launcher"]["user_following_fetcher_thread_num"]
    threads = [UserFollowingFetcher() for _ in range(thread_num)]
    return threads

def launch():
    threads = get_danmaku_fetchers_threads() + get_user_following_fetchers_threads()
    for t in threads:
        t.start()
    for t in threads:
        t.join()