# coding:utf-8
import lxbasic.core as bsc_core

bsc_core.BscProcess.execute_as_trace(
    r'rez-env maya-2020 mtoa qsm_maya_main -- mayabatch -command "python(\"import lxsession.commands as ssn_commands;ssn_commands.execute_option_hook(option=\\\"option_hook_key=dcc-process/maya-task-process&method=asset_cfx_rig_release&method_option=F00CFA7FBC2F87A4A38E21605A894FD9\\\")\")"'
)
