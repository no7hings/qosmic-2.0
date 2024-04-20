# coding:utf-8
import multiprocessing

import random

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxusd.core as usd_core

bsc_log.Log.TEST = True

random.seed(1)

points = [
    (random.choice(range(1, 10)), random.choice(range(1, 10)), random.choice(range(1, 10))) for _ in range(100000)
]


def perform_query(data):
    _points, _check_points = data
    _kd_tree = usd_core.NpKDTree(_points)
    # return kd_tree.compute_closed_indexes(_check_points)
    return _kd_tree.compute_closed_indexes(_check_points)


p = multiprocessing.Pool(processes=4)

bsc_log.Log.test_start('check')

results = p.map(
    perform_query, [(points, i) for i in [points, points, points, points]]
)

p.close()
p.join()

print results

bsc_log.Log.test_end('check')

# kd_tree = usd_core.NpKDTree(points)
# bsc_log.Log.test_start('check')
# for i in [points, points, points, points]:
#     print kd_tree.compute_closed_indexes(i)
# bsc_log.Log.test_end('check')
