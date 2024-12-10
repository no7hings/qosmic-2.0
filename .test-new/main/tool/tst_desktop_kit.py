# coding:utf-8
import lxbasic.core as bsc_core

bsc_core.BscEnvironExtra.set_devlop_flag(True)

import lxsession.commands as ssn_commands; ssn_commands.execute_hook('desktop-tools/desktop-tool-kit')
