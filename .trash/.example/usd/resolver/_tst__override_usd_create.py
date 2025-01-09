# coding:utf-8
import lxresolver.core as rsv_core

import lxusd.rsv.objects as rsv_objects

resolver = rsv_core.RsvBase.generate_root()


rsv_task = resolver.get_rsv_task(
    project='nsa_dev', asset='td_test', task='surface'
)


rsv_objects.RsvTaskOverrideUsdCreator(
    rsv_task
).create_all_source_geometry_uv_map_over()

