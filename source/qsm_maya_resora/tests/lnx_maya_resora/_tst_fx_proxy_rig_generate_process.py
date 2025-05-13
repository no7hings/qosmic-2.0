# coding:utf-8
import lxbasic.session as s

cmd_script = 'rez-env maya-2020 mtoa qsm_maya_main -- mayabatch -command "python(\\"import lxsession.commands as ssn_commands;ssn_commands.execute_option_hook(option=\\\\\\"option_hook_key=dcc-process/maya-cache-process&method=fx_proxy_rig_generate&method_option=10B2A8755BBC6B566BD454CF2CB52132\\\\\\")\\")"'

s.SsnShell.execute_script_as_trace(
    cmd_script, clear_env=True
)
