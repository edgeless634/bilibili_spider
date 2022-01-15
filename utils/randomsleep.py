import time
import random

__RANDOM_RATE = 0.1

def random_sleep(sleep_time, random_rate = __RANDOM_RATE):
    '''
    睡眠sleep_time(± random_rate * sleep_time)秒钟
    '''
    rate = random.random() * random_rate
    offset = rate * random.choice([1, -1])
    time.sleep(sleep_time * (1 + offset))

class Sleeper:
    '''
    在调用sleep时，睡眠到实例化本对象后的sleep_time秒
    '''
    def __init__(self, sleep_time) -> None:
        self.sleep_time = sleep_time
        self.start_time = time.perf_counter()
    
    def sleep(self):
        use_time = time.perf_counter() - self.start_time
        sleep_time = self.sleep_time - use_time
        if sleep_time > 0:
            random_sleep(sleep_time)