# coding:utf-8
import lxbasic.core as bsc_core

bsc_core.PyReloader2(
    ['qsm_maya', 'qsm_general', 'lxbasic']
).do_reload()

import qsm_maya.handles.assembly.scripts as qsm_mya_hdl_asb_scripts

qsm_mya_hdl_asb_scripts.MeshBoxGenerate.generate_by_group(
    ''
)
