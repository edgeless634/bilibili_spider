from helper.fetch import CommentFetcher
from setting.settingReader import setting

def launch():
    thread_num = setting["launcher"]["comment_fetcher_thread_num"]
    threads = [CommentFetcher() for _ in range(thread_num)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()