# coding:utf-8
import lxresolver.core as rsv_core

r = rsv_core.RsvBase.generate_root()

f = '/l/prod/shl/work/assets/chr/td_test/srf/surfacing/maya/scenes/td_test.srf.surfacing.v017.ma'


properties = r.get_task_properties_by_any_scene_file_path(file_path=f)

properties.set('deadline.test', 'test')

print r.get_task_properties_by_any_scene_file_path(file_path=f)
