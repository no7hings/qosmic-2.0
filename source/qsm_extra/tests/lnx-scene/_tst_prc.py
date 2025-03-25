# coding:utf-8
import lxbasic.core as bsc_core

cmd_script = 'rez-env maya-2020 mtoa qsm_maya_main -- mayabatch -command "python(\\"import lxsession.commands as ssn_commands;ssn_commands.execute_option_hook(option=\\\\\\"option_hook_key=dcc-process/maya-cache-process&method=shot_replace_reference&method_option=EC31A188306DBEA3EE026E103C05E894\\\\\\")\\")"'

bsc_core.BscProcess.execute_as_trace(
    cmd_script
)
