# coding:utf-8
import lxbasic.core as bsc_core

import lxsession.commands as ssn_commands

user = bsc_core.BscSystem.get_user_name()

j_option_opt = bsc_core.ArgDictStringOpt(
    option=dict(
        option_hook_key='rsv-task-batchers/asset/gen-any-export-build',
        # choice_scheme='asset-maya-create-and-publish',
        choice_scheme='asset-maya-publish',
        #
        file='/production/shows/nsa_dev/assets/chr/td_test/shared/srf/srf_anishading/td_test.srf.srf_anishading.v014/source/td_test.ma',
        maya_scene_srcs=[
            '/production/shows/nsa_dev/assets/chr/td_test/shared/srf/srf_anishading/td_test.srf.srf_anishading.v014/source/td_test.ma'
        ],
        katana_scene_srcs=[

        ],
        #
        td_enable=True,
        # rez_beta=True,
    )
)
#
ssn_commands.execute_option_hook_by_deadline(
    option=j_option_opt.to_string()
)
