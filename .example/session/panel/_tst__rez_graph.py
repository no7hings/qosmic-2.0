# coding:utf-8
import lxbasic.core as bsc_core

import lxsession.commands as ssn_commands

bsc_core.BscEnvironExtra.set_td_enable(True)

ssn_commands.execute_option_hook('option_hook_key=desktop-tools/rez-graph&packages=qsm_dcc_main')
