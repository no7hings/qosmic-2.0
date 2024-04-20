# coding:utf-8
import lxbasic.storage as bsc_storage

scene_file_path = '/production/library/resource/all/3d_plant_proxy/yegrass_h008_rsc/v0001/scene/maya/yegrass_h008_rsc.ma'
geometry_abc_file_path = '/production/library/resource/all/3d_plant_proxy/yegrass_h008_rsc/v0001/geometry/abc/yegrass_h008_rsc.abc'

scene_file_opt = bsc_storage.StgFileOpt(scene_file_path)
geometry_abc_file_opt = bsc_storage.StgFileOpt(geometry_abc_file_path)

print geometry_abc_file_opt.get_is_writable()

geometry_abc_file_opt.set_modify_time(
    scene_file_opt.get_modify_timestamp()
)
