# coding:utf-8
import lxbasic.core as bsc_core

p = bsc_core.PyReloader(
    [
        'lxuniverse', 'lxresolver',
        'lxarnold',
        'lxutil',
        'lxkatana', 'lxkatana_gui'
    ]
)
p.set_reload()

import lxkatana.dcc.operators as ktn_dcc_operators

geometry_file_path, hair_file_path, look_file_path, katana_look_file_path, source_katana_file_path = [
    '/l/prod/shl/work/assets/chr/nn_gongshifu/srf/surfacing/geometry/scene/v009/hi.abc',
    None,
    '/l/prod/shl/work/assets/chr/nn_gongshifu/srf/surfacing/look/scene/v009/all.ass',
    None,
    None
]
