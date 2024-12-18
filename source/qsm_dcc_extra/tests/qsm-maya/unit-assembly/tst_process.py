# coding:utf-8
import lxbasic.core as bsc_core

bsc_core.PyReloader2(
    ['qsm_maya', 'qsm_general', 'lxbasic']
).do_reload()

import qsm_maya.handles.scenery.scripts as qsm_mya_hdl_scn_scripts

qsm_mya_hdl_scn_scripts.UnitAssemblyProcess(
    'X:/QSM_TST/Assets/scn/test_assembly/Maya/Final/test_assembly.ma',
).execute()
