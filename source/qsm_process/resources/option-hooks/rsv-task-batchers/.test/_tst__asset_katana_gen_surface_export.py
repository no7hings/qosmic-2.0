# coding:utf-8
import lxbasic.core as bsc_core

import lxsession.commands as ssn_commands

user = bsc_core.SysBaseMtd.get_user_name()

j_option_opt = bsc_core.ArgDictStringOpt(
    option=dict(
        option_hook_key='rsv-task-batchers/asset/gen-surface-export',
        #
        file='/production/shows/nsa_dev/assets/chr/td_test/user/work.dongchangbao/katana/scenes/surfacing/td_test.srf.surfacing.v000_002.katana',
        user=bsc_core.SysBaseMtd.get_user_name(),
        #
        choice_scheme='asset-katana-publish',
        #
        # td_enable=True,
        # rez_beta=True,
    )
)
#
ssn_commands.execute_option_hook_by_deadline(
    option=j_option_opt.to_string()
)
