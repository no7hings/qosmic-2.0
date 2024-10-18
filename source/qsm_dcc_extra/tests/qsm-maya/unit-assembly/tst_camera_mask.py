# coding:utf-8
import lxbasic.core as bsc_core

bsc_core.PyReloader2(
    ['qsm_maya', 'qsm_general', 'lxbasic']
).do_reload()

import qsm_maya.steps.scenery.scripts as qsm_mya_stp_scn_scripts

qsm_mya_stp_scn_scripts.DynamicCameraMask(
    'perspShape1'
).execute_for_all()
