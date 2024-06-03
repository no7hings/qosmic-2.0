# coding:utf-8
import lxbasic.core as bsc_core

import lxgui

lxgui.do_reload()

bsc_core.PyReloader2(
    ['lxbasic', 'qsm_general', 'qsm_maya', 'qsm_maya_easy_tool']
).do_reload()

import qsm_maya.rig.scripts as qsm_mya_rig_scripts

qsm_mya_rig_scripts.TransformationLocatorOpt(
    ['sam_Skin', 'sam_Skin1']
).create_transformation_locators()
