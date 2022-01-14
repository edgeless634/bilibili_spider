import os
import yaml

__default_str = """
launcher:
    danmaku_fetcher_thread_num: 4
    user_following_fetcher_thread_num: 1
DanmakuFetcher:
    wait_time_each: 5
UserFollowingFetcher:
    wait_time_each: 5
    wait_time_each_step: 2
proxyFetch:
    enable: false
    api_url: "http://192.168.1.21:10001/get/"
    proxy_for_proxyfetch: "http://127.0.0.1:10809"
"""
setting = None


def __init():
    global setting
    file_path = os.path.dirname(__file__)
    setting = yaml.load(__default_str, Loader=yaml.CLoader)
    with open(os.path.join(file_path, "setting.yml"), "r") as f:
        new_setting = yaml.load(f.read(), Loader=yaml.CLoader)
    setting.update(new_setting)

__init()

if __name__ == "__main__":
    print(setting)