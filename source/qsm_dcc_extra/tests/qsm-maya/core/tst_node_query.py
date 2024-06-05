# coding:utf-8
import lxbasic.core as bsc_core

import lxgui

lxgui.do_reload()

bsc_core.PyReloader2(
    ['lxbasic', 'qsm_general', 'qsm_maya', 'qsm_maya_easy_tool']
).do_reload()

import qsm_maya.core as qsm_mya_core

for i in qsm_mya_core.NodeQuery(
    'deformWave'
).get_all_port_queries():
    print i.is_writable()
