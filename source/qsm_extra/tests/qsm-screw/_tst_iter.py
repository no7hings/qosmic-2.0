# coding:utf-8
from __future__ import print_function

import time

import lxbasic.core as bsc_core

import lnx_screw.core as lnx_scr_core


def find_all(tag=0):
    stage = lnx_scr_core.Stage('motion_splice')
    return stage.find_all(entity_type='Type')


fnc = bsc_core.lru_cache()(find_all)
print(time.time())
fnc(0)
print(time.time())
fnc(1)
print(time.time())


