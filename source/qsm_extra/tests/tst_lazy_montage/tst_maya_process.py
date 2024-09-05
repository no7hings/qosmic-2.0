# coding:utf-8
import lxbasic.core as bsc_core

cmd_script = r'rez-env maya-2020 mtoa qsm_dcc_main studio_library -- mayabatch -command "python(\"import lxsession.commands as ssn_commands;ssn_commands.execute_option_hook(option=\\\"option_hook_key=dcc-process/maya-cache-process&method=motion_generate&method_option=A5C15C8CA8E3247B39028A5123786D28\\\")\")"'

bsc_core.BscProcess.execute_as_trace(
    cmd_script
)

