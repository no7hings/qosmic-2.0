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
        option_hook_key='rsv-task-batchers/asset/gen-surface-export',
        #
        file='/production/shows/nsa_dev/assets/chr/td_test/user/work.dongchangbao/maya/scenes/surfacing/td_test.srf.surfacing.v001_001.ma',
        user=bsc_core.BscSystem.get_user_name(),
        #
        choice_scheme='asset-maya-publish',
        #
        td_enable=True,
        # rez_beta=True,
    )
)
#
ssn_commands.execute_option_hook_by_deadline(
    option=j_option_opt.to_string()
)
