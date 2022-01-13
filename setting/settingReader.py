import os
import yaml

__default_str = """
spider:
    wait_time: 0.2
proxyFetch:
    enable: false
    proxy_for_proxyfetch: "http://127.0.0.1:1080"
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