# coding:utf-8
import lxbasic.core as bsc_core

import qsm_general.process as qsm_gnl_process


cmd_script = qsm_gnl_process.MayaTaskProcess.generate_cmd_script_by_option_dict(
    'cfx_rig_release',
    dict(
        scene_src='X:/QSM_TST/QSM/release/assets/chr/lily/cfx.cfx_rig/lily.cfx.cfx_rig.v001/source/lily.ma'
    )
)


bsc_core.BscProcess.execute_as_trace(
    cmd_script
)
