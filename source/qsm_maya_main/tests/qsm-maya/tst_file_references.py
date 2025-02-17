# coding:utf-8
from __future__ import print_function

import lxbasic.core as bsc_core

bsc_core.PyReloader2(
    ['qsm_maya', 'qsm_general', 'lxbasic']
).do_reload()

import qsm_maya.core as qsm_mya_core

print(qsm_mya_core.FileReferences.search_all_from(
    ['X:/QSM_TST/Assets/prp/test_gpu_assembly/Maya/Final']
))
