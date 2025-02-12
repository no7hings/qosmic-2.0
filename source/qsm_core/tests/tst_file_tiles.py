# coding:utf-8
from __future__ import print_function

import lxbasic.core as bsc_core


print(bsc_core.BscFileTiles.is_valid(
    'test.<udim>.jpg'
))

print(bsc_core.BscFileTiles.is_valid(
    'test.<f>.jpg'
))

print(bsc_core.BscFileTiles.is_valid(
    'test.jpg'
))
