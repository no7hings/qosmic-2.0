# coding:utf-8
import lxbasic.core as bsc_core

import lxsession.commands as ssn_commands

user = bsc_core.BscSystem.get_user_name()

option_opt = bsc_core.ArgDictStringOpt(
    option=dict(
        option_hook_key='rsv-task-batchers/asset/gen-model-export',
        #
        file='/l/prod/cgm/work/assets/chr/queen_white/mod/modeling/maya/scenes/queen_white.mod.modeling.v001.ma',
        user=bsc_core.BscSystem.get_user_name(),
        host=bsc_core.BscSystem.get_host(),
        #
        # choice_scheme='asset-maya-output',
        choice_scheme='asset-maya-publish',
        #
        # td_enable=True,
        # rez_beta=True,
    )
)

# s = ssn_commands.get_option_hook_session(option_opt.to_string())
#
# print s.get_executor().get_deadline_command()
#
ssn_commands.execute_option_hook_by_deadline(
    option=option_opt.to_string()
)
