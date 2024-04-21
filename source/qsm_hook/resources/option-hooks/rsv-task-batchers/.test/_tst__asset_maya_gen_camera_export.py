# coding:utf-8
import lxbasic.core as bsc_core

import lxsession.commands as ssn_commands

user = bsc_core.SysBaseMtd.get_user_name()

j_option_opt = bsc_core.ArgDictStringOpt(
    option=dict(
        option_hook_key='rsv-task-batchers/asset/gen-camera-export',
        # choice_scheme='asset-maya-create-and-publish',
        choice_scheme='asset-maya-publish',
        #
        file='/production/shows/nsa_dev/assets/chr/momo/user/work.dongchangbao/maya/scenes/camera/momo.cam.camera.v000_001.ma',
        #
        # td_enable=True,
        # rez_beta=True,
    )
)
#
ssn_commands.execute_option_hook_by_deadline(
    option=j_option_opt.to_string()
)
