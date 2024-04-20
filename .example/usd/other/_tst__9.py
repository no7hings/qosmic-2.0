# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxusd.core as usd_core


def finished_fnc_(index, status, results):
    print index, status, results[-1]


t = bsc_core.TrdCommandPool

usdFilePath = '/l/prod/cgm/work/assets/vfx/efx_dissipation_grandma/srf/surfacing/katana/set/x40130/v012/x40130.usda'

stage = usd_core.Usd.Stage.Open(usdFilePath, usd_core.Usd.Stage.LoadAll)

stage_opt = usd_core.UsdStageOpt(
    stage
)

p = stage_opt.get_obj(
    '/assets/efx/efx_dissipation_grandma'
)

prim_opt = usd_core.UsdPrimOpt(
    p
)

for i_seq, i_prim in enumerate(prim_opt.get_children()):
    i_prim_opt = usd_core.UsdPrimOpt(i_prim)
    i_port = i_prim_opt.get_port('userProperties:pgOpIn:usd:opArgs:fileName')
    i_path = i_prim_opt.get_path()
    i_file_path = i_port.Get().resolvedPath

    print i_file_path

    i_file_path_m = bsc_storage.StgFileMtdForMultiply.convert_to(
        i_file_path, ['*.####.{format}']
    )
    i_file_tile_paths = bsc_storage.StgFileMtdForMultiply.get_exists_unit_paths(
        i_file_path_m
    )

    print i_file_tile_paths
    # for j_seq, j_file_path in enumerate(i_file_tile_paths):
    #     j_cmd = usd_core.UsdProcess.get_command(
    #         'method=cache-hierarchy&location={}&file={}'.format(i_path, j_file_path)
    #     )
    #
    #     bsc_core.TrdCommandPool.set_wait()
    #     #
    #     i_t = bsc_core.TrdCommandPool.set_start(j_cmd, i_seq)
    #     #
    #     i_t.finished.connect_to(finished_fnc_)

