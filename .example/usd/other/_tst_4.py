# coding:utf-8
import lxbasic.core as bsc_core
p = bsc_core.PyReloader(
    [
        'lxuniverse',
        'lxarnold', 'lxusd',
        'lxutil', 'lxmaya',
    ]
)
p.set_reload()

import lxusd.fnc.objects as usd_fnc_objects

file_path = '/l/prod/shl/publish/assets/chr/nn_gongshifu/srf/td_test/nn_gongshifu.srf.td_test.v019/cache/usd/uv_map.usd'

geometry_file_path = '/l/prod/shl/publish/assets/chr/nn_gongshifu/mod/modeling/nn_gongshifu.mod.modeling.v007/cache/usd/geo/hi.usd'

surface_geometry_file_path = '/l/prod/shl/work/assets/chr/nn_gongshifu/srf/td_test/geometry/scene/v010/hi.usd'

g_f = usd_fnc_objects.GeometryUvMapExporter(
    file_path=file_path,
    root='/master',
    option=dict(
        path_lstrip=True,
        file_0=geometry_file_path,
        file_1=surface_geometry_file_path
    )
)

g_f.set_run()
