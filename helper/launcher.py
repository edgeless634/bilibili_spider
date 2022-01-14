from helper.fetch import CommentFetcher, UserFollowingFetcher
from setting.settingReader import setting

def get_comment_fetchers_threads():
    thread_num = setting["launcher"]["comment_fetcher_thread_num"]
    threads = [CommentFetcher() for _ in range(thread_num)]
    return threads

def get_user_following_fetchers_threads():
    thread_num = setting["launcher"]["user_following_fetcher_thread_num"]
    threads = [UserFollowingFetcher() for _ in range(thread_num)]
    return threads

def launch():
    threads = get_comment_fetchers_threads() + get_user_following_fetchers_threads()
    for t in threads:
        t.start()
    for t in threads:
        t.join()