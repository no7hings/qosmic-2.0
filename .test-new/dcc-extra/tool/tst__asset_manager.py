# coding:utf-8
import lxbasic.core as bsc_core

import lxgui

lxgui.do_reload()

bsc_core.PyReloader2(
    ['qsm_maya', 'qsm_dcc', 'qsm_general', 'qsm_gui', 'qsm_tool', 'qsm_maya_tool', 'lxgui']
).do_reload()

import lxsession.commands as ssn_commands

ssn_commands.execute_hook(
    '*/*/qsm-asset-manager'
)
