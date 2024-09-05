# coding:utf-8

import lxbasic.core as bsc_core
cmd_script = r'rez-env maya-2020 mtoa qsm_dcc_main -- mayabatch -command "python(\"import lxsession.commands as ssn_commands;ssn_commands.execute_option_hook(option=\\\"option_hook_key=dcc-process/maya-cache-process&method=rig-validation&method_option=E7D7D5AC32CA03E8C3A85E30CF6AAA1B\\\")\")"'

bsc_core.BscProcess.execute_as_trace(
    cmd_script
)
