# coding:utf-8
from concurrent.futures import ThreadPoolExecutor

# 创建一个全局线程池
executor = ThreadPoolExecutor(max_workers=5)

depth_max = 5

lst = []


def rcs_fnc(lst_, depth_):

    if depth_ == depth_max:
        return

    _depth = depth_+1
    for _i in range(5):
        lst_.append((depth_, _i))
        # rcs_fnc(lst_, _depth)
        executor.submit(rcs_fnc, lst_, _depth)


executor.submit(rcs_fnc, lst, 0)

# rcs_fnc(lst, 0)
print lst
