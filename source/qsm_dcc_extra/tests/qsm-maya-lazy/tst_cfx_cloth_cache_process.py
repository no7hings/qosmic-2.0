# coding:utf-8
import lxbasic.core as bsc_core
cmd_script = r'rez-env maya-2020 mtoa qsm_dcc_main -- mayabatch -command "python(\"import lxsession.commands as ssn_commands;ssn_commands.execute_option_hook(option=\\\"option_hook_key=dcc-process/maya-cache-process&method=cfx-cloth-cache-generate&method_option=3688ACA3C103BF3736CC38D4DDE83253\\\")\")"'

bsc_core.BscProcess.execute_as_trace(
    cmd_script
)
