# coding:utf-8
import lxbasic.core as bsc_core

import lxgui

lxgui.do_reload()

bsc_core.PyReloader2(
    ['qsm_maya', 'qsm_dcc', 'qsm_general']
).do_reload()


import qsm_maya.motion as qsm_motion

qsm_motion.AdvMotionOpt(
    'sam_Skin'
).transfer_motions_to(
    'sam_Skin1'
)
