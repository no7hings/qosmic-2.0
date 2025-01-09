# coding:utf-8
import lxusd.startup as usd_startup

import lxusd.core as usd_core

usd_startup.UsdSetup.build_environ()

import lxusd.fnc.objects as usd_fnc_exporter

color_scheme = 'asset_color'

f_src = '/l/prod/cgm/publish/assets/chr/td_test/mod/modeling/td_test.mod.modeling.v056/cache/usd/geo/hi.usd'

f_tgt = '/l/prod/cgm/publish/assets/chr/td_test/mod/modeling/td_test.mod.modeling.v056/cache/usd/geo_extra/user_property.usd'

s = usd_core.UsdStageOpt._open_file_(f_src)

usd_fnc_exporter.GeometryLookPropertyExporter(
    option=dict(
        file=f_tgt,
        location='/master',
        #
        stage_src=s,
        #
        asset_name='nn_4y',
        #
        color_seed=5,
        #
        color_scheme=color_scheme,
        #
        with_object_color=True,
        with_group_color=True,
        with_asset_color=True,
        with_shell_color=True,
        #
        # with_uv_map=True,
        #
        # with_display_color=True
    )
).set_run()


