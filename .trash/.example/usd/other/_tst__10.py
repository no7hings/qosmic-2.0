# coding:utf-8
import lxusd.startup as usd_startup

usd_startup.UsdSetup.build_environ()

import lxusd.core as usd_core

j_stage_opt = usd_core.UsdStageOpt(
    '/l/prod/cgm/publish/shots/x40/x40130/efx/efx_dissipation_grandma/x40130.efx.efx_dissipation_grandma.v008/cache/release_grandma/usd/release_grandma.1001.usd'
)

print j_stage_opt.get_all_obj_paths()
