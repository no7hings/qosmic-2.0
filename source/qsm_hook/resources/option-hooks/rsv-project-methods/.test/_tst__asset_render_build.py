# coding:utf-8
import lxbasic.core as bsc_core

import lxsession.commands as ssn_commands

j_option_opt = bsc_core.ArgDictStringOpt(
    option=dict(
        option_hook_key='rsv-project-methods/asset/katana/render-build',
        #
        file='/production/shows/nsa_dev/assets/chr/td_test/user/work.dongchangbao/katana/scenes/surface/td_test.srf.surface.v000_002.katana',
        #
        render_nodes=['Render', 'asset_free__default__asset_standard', 'asset_free__default__asset_standard1', 'shot_free__default__asset_standard'],
        default_render_version='new',
        default_render_frames='1001-1120:10',
        auto_convert_mov=True,
        #
        td_enable=True,
        # rez_beta=True,
    )
)
#
ssn_commands.execute_option_hook_by_deadline(
    option=j_option_opt.to_string()
)
