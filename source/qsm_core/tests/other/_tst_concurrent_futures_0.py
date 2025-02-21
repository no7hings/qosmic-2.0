# coding:utf-8
from concurrent.futures import ThreadPoolExecutor

# 创建一个全局线程池
executor = ThreadPoolExecutor(max_workers=5)

depth_max = 5

lst = []


def rcs_fnc(lst_, depth_):

    if depth_ == depth_max:
        return False

    _depth = depth_+1
    for _i in range(5):
        lst_.append((depth_, _i))
        executor.submit(rcs_fnc, lst_, _depth)
    return True


future = executor.submit(rcs_fnc, lst, 0)
if future.result():
    print lst
