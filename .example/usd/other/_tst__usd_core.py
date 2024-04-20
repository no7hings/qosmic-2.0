# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import lxusd.startup as usd_startup

usd_startup.UsdSetup.build_environ()

import lxusd.core as usd_core

file_path_src = '/l/prod/cgm/work/assets/vfx/efx_dissipation_grandma/srf/surfacing/katana/set/x40130/v012/x40130.usda'

file_path_tgt = '/data/f/test_usd_export/test_1.usda'

location = '/assets/efx/efx_dissipation_grandma'

stage_opt = usd_core.UsdStageOpt(
    file_path_src
)

p = stage_opt.get_obj(
    location
)

prim_opt = usd_core.UsdPrimOpt(
    p
)

list_ = []
cs = prim_opt.get_children()
with bsc_log.LogProcessContext.create_as_bar(maximum=len(cs), label='usd combine') as l_p:
    for i_prim in cs:
        l_p.do_update()
        #
        i_prim_opt = usd_core.UsdPrimOpt(i_prim)
        i_port = i_prim_opt.get_port('userProperties:pgOpIn:usd:opArgs:fileName')
        i_path = i_prim_opt.get_path()
        list_.append(
            i_path
        )
        i_file_path = i_port.Get().resolvedPath

        i_yaml_file_path = bsc_storage.StgTmpYamlMtd.get_file_path(
            i_file_path, 'usd-hierarchy-cacher'
        )
        i_yaml_file_opt = bsc_storage.StgFileOpt(i_yaml_file_path)
        if i_yaml_file_opt.get_is_exists() is True:
            i_list = i_yaml_file_opt.set_read()
            list_.extend([i_path + j for j in i_list])
        else:
            i_file_path_ = bsc_storage.StgFileMtdForMultiply.convert_to(
                i_file_path, ['*.####.{format}']
            )
            i_file_tile_paths = bsc_storage.StgFileMtdForMultiply.get_exists_unit_paths(
                i_file_path_
            )
            i_list = []
            for j_file_path in i_file_tile_paths:
                j_stage_opt = usd_core.UsdStageOpt(j_file_path)
                j_rls_paths = j_stage_opt.get_all_obj_paths()
                i_list.extend(j_rls_paths)
            #
            i_list_ = list(set(i_list))
            i_list_.sort(key=i_list.index)
            #
            bsc_storage.StgFileOpt(i_yaml_file_path).set_write(
                i_list_
            )
            #
            list_.extend([i_path+j for j in i_list_])

output_file_opt = usd_core.UsdFileWriteOpt(
    file_path_tgt
)

output_file_opt.set_location_add(location)

with bsc_log.LogProcessContext.create_as_bar(maximum=len(list_), label='usd create') as l_p:
    for i in list_:
        l_p.do_update()
        output_file_opt.set_obj_add(i)

output_file_opt.set_save()



