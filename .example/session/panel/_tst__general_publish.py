# coding:utf-8
import lxbasic.core as bsc_core

import lxsession.commands as ssn_commands

bsc_core.BscEnvironExtra.set_devlop_flag(True)

bsc_core.BscEnvironExtra.set('QSM_TASK_ID', '202455')

ssn_commands.execute_hook('desktop-tools/general-publisher')
