import os
import yaml

__default_str = """
launcher:
    danmaku_fetcher_thread_num: 4
    user_following_fetcher_thread_num: 2
DanmakuFetcher:
    wait_time_each: 2
    wait_time_each_step: 1
UserFollowingFetcher:
    wait_time_each: 2
    wait_time_each_step: 1
proxyFetch:
    enable: false
    api_url: "http://127.0.0.1:5010/get/"
    proxy_for_proxyfetch: ""
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