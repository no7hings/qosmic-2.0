# coding:utf-8
import lxresource as bsc_resource

import lxbasic.core as bsc_core

import lxsession.commands as ssn_commands

bsc_core.BscEnviron.append(
    bsc_resource.ExtendResource.ENVIRON_KEY, '/data/e/myworkspace/td/lynxi/script/python/.resources'
)

user = bsc_core.BscSystem.get_user_name()

j_option_opt = bsc_core.ArgDictStringOpt(
    option=dict(
        option_hook_key='rsv-task-batchers/asset/gen-groom-export',
        #
        file='/l/prod/cgm/work/assets/chr/nn_4y_test/grm/groom/maya/scenes/nn_4y_test.grm.groom.v065.ma',
        user=bsc_core.BscSystem.get_user_name(),
        #
        choice_scheme='asset-maya-output',
        # choice_scheme='asset-maya-publish',
        #
        td_enable=True,
        # test_flag=True,
    )
)
#
ssn_commands.execute_option_hook_by_deadline(
    option=j_option_opt.to_string()
)
