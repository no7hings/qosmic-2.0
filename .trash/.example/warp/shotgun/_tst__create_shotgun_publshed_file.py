# coding:utf-8
import lxresolver.core as rsv_core

import lxbasic.shotgun as bsc_shotgun

c = bsc_shotgun.StgConnector()

r = rsv_core.RsvBase.generate_root()

file_paths = [
    '/l/prod/cgm/work/assets/chr/ext_andy/rig/rigging/maya/scenes/ext_andy.rig.rigging.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_ben/rig/rigging/maya/scenes/ext_ben.rig.rigging.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_burk/rig/rigging/maya/scenes/ext_burk.rig.rigging.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_erzi/rig/rigging/maya/scenes/ext_erzi.rig.rigging.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_fuzzy/rig/rigging/maya/scenes/ext_fuzzy.rig.rigging.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_johnny/rig/rigging/maya/scenes/ext_johnny.rig.rigging.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_luo/rig/rigging/maya/scenes/ext_luo.rig.rigging.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_mannequin/rig/rigging/maya/scenes/ext_mannequin.rig.rigging.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_mike/rig/rigging/maya/scenes/ext_mike.rig.rigging.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_owl_a/rig/rigging/maya/scenes/ext_owl_a.rig.rigging.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_proketeriat/rig/rigging/maya/scenes/ext_proketeriat.rig.rigging.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_suraj/rig/rigging/maya/scenes/ext_suraj.rig.rigging.v001.ma',
    '/l/prod/cgm/work/assets/chr/ext_woodpecker/rig/rigging/maya/scenes/ext_woodpecker.rig.rigging.v001.ma'
]

for i_file_path in file_paths:
    i_rsv_scene_properties = r.get_rsv_scene_properties_by_any_scene_file_path(
        i_file_path
    )
    i_rsv_task = r.get_rsv_task(**i_rsv_scene_properties.value)
    i_rsv_unit = i_rsv_task.get_rsv_unit(
        keyword='asset-maya-scene-file'
    )
    i_file_path_ = i_rsv_unit.get_result(version=i_rsv_scene_properties.get('version'))
    i_rsv_properties = i_rsv_unit.generate_properties_by_result(i_file_path_)

    print c.set_stg_published_file_create(
        file=i_file_path_, **i_rsv_properties.value
    )
