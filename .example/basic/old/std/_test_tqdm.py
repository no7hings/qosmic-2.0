# coding:utf-8
import time

from tqdm import tqdm

for i in tqdm(range(10), desc='test', colour='#ffff00'):
    pass
    time.sleep(1)
    # print i
