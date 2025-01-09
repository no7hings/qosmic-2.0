# coding:utf-8
import lxusd.startup as usd_startup

usd_startup.UsdSetup.build_environ()

f = '/data/f/usd_uv_map_export_test_0/test_0.usda'

import lxusd.core as usd_core

s_opt = usd_core.UsdStageOpt(f)

p = s_opt.get_obj('/pPlane1/pPlaneShape1')

print p

m = usd_core.UsdGeom.Mesh(p)

print usd_core.UsdMeshOpt(
    m
).compute_vertex_color_map_from_uv_coord('st')


