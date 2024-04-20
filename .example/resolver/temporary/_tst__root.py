# coding:utf-8
import lxresolver.core as rsv_core

r = rsv_core.RsvBase.generate_root()

rsv_project = r.get_rsv_project(project='xkt')

rsv_task = rsv_project.get_rsv_task(
    # workspace='work',
    # sequence='z88',
    shot='z88010',
    step='efx',
    task='effects'
)

print rsv_task.properties

rsv_unit = rsv_task.get_rsv_unit(
    keyword='shot-temporary-katana-render-video-mov-file'
)

result = rsv_unit.get_result(version='latest')
print result
print rsv_unit.generate_properties_by_result(result)

version_rsv_unit = rsv_task.get_rsv_unit(
    keyword='{branch}-temporary-version-dir'
)
print version_rsv_unit.get_new_version()

rsv_unit = rsv_task.get_rsv_unit(
    keyword='shot-source-houdini-scene-src-file'
)

result = rsv_unit.get_result(version='latest')
print result
print rsv_unit.generate_properties_by_result(result)

f = '/l/prod/xkt/work/shots/z88/z88010/efx/effects/houdini/z88010.efx.effects.v032.hip'

print r.get_rsv_scene_properties_by_any_scene_file_path(f)
