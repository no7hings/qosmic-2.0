# coding:utf-8
import lxbasic.core as bsc_core

cmd_script = r'rez-env maya-2024 mtoa qsm_maya_main -- mayabatch -command "python(print(1))"'

bsc_core.BscProcess.execute_as_trace(
    cmd_script
)
