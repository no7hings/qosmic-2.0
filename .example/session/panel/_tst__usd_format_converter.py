# coding:utf-8
import lxbasic.core as bsc_core

import lxsession.commands as ssn_commands

bsc_core.BscEnvironExtra.set_devlop_flag(True)

ssn_commands.execute_hook('desktop-tools/usd-format-converter')
