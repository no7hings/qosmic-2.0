# coding:utf-8
import lxbasic.core as bsc_core

import lxsession.commands as ssn_commands

bsc_core.EnvExtraMtd.set_td_enable(True)

bsc_core.EnvExtraMtd.set('QSM_TASK_ID', '202455')

ssn_commands.execute_hook('desktop-tools/general-publisher')
