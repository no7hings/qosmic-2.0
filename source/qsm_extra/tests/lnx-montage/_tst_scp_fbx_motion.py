# coding:utf-8
import lxbasic.core as bsc_core

import lnx_montage.scripts as s

task_name, cmd_script = s.MoCapDotFbxMotionGenerateAuto(
    'Z:/resources/mixamo/Standing Arguing (1).fbx'
).generate_args()

if cmd_script:
    bsc_core.BscProcess.execute_as_trace(
        cmd_script
    )

