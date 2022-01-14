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