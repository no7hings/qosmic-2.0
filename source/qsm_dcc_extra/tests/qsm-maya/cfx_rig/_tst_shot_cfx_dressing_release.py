# coding:utf-8
import lxbasic.core as bsc_core

import qsm_general.process as qsm_gnl_process


cmd_script = qsm_gnl_process.MayaTaskProcess.generate_cmd_script_by_option_dict(
    'shot_cfx_dressing_release',
    dict(
        scene_src='X:/QSM_TST/QSM/release/shots/A001_001/A001_001_001/cfx.cfx_dressing/A001_001_001.cfx.cfx_dressing.v002/source/A001_001_001.ma'
    )
)


bsc_core.BscProcess.execute_as_trace(
    cmd_script
)
