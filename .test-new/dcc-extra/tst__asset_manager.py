# coding:utf-8
import lxbasic.core as bsc_core

bsc_core.PyReloader2(
    ['qsm_maya']
).do_reload()

import lxsession.commands as ssn_commands

ssn_commands.execute_hook(
    '*/*/qsm-asset-manager'
)
