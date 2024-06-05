# coding:utf-8
import lxbasic.core as bsc_core

import lxsession.commands as ssn_commands

user = bsc_core.BscSystem.get_user_name()

j_option_opt = bsc_core.ArgDictStringOpt(
    option=dict(
        option_hook_key='rsv-task-batchers/asset/gen-model-export-extra',
        #
        file='/l/prod/cgm/work/assets/chr/td_test/mod/modeling/maya/scenes/td_test.mod.modeling.v109.ma',
        user=bsc_core.BscSystem.get_user_name(),
        #
        choice_scheme='asset-maya-publish',
        # choice_scheme='asset-maya-output',
        #
        td_enable=True,
        # rez_beta=True,
    )
)
#
ssn_commands.execute_option_hook_by_deadline(
    option=j_option_opt.to_string()
)
