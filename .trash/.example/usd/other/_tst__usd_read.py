# coding:utf-8
import lxusd.core as usd_core

import lxusd.dcc.operators as usd_ops


s_o = usd_core.UsdStageOpt(
    '/t/prod/cgm/output/shots/z95/z95141/efx/efx_lighthouse/z95141.efx.efx_lighthouse.v012/cache/release_ocean_mesh_geo/usd/release_ocean_mesh_geo.1180.usd'
)

print s_o.get_all_mesh_objs()

for i_p in s_o.get_all_mesh_objs():
    i_m_o = usd_ops.MeshOpt(i_p)
    print i_m_o.get_uv_map_names()
    i_m_o.get_uv_map('st')
