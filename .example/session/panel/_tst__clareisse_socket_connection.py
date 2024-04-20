# coding:utf-8
import lxbasic.core as bsc_core

import lxsession.commands as ssn_commands

bsc_core.EnvExtraMtd.set_td_enable(True)
bsc_core.EnvBaseMtd.set('REZ_BETA', '1')

ssn_commands.execute_hook("*/clarisse/create-socket-connection")
