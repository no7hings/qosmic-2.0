# coding:utf-8
import lxbasic.storage as bsc_storage

import lxresolver.core as rsv_core

resolver = rsv_core.RsvBase.generate_root()

for i in [
    '/l/prod/shl/publish/assets/chr/td_test/mod/modeling/td_test.mod.modeling.v001/maya/td_test.ma',
    'L:/prod/cjd/publish/assets/prp/changting_a/mod/mod_layout/changting_a.mod.mod_layout.v001/maya/changting_a.ma',
    # '/l/prod/cjd/publish/assets/prp/changting_a/mod/mod_layout/changting_a.mod.mod_layout.v001/maya/changting_a.ma',
]:
    file_path = bsc_storage.StgPathMapper.map_to_current(i)
    task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=file_path)
    print task_properties

