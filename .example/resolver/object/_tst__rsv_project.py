# coding:utf-8
import lxbasic.core as bsc_core

import lxresolver.core as rsv_core

r = rsv_core.RsvBase.generate_root()


p = r.get_rsv_project(project='nsa_dev')

print p.get_rsv_resource_groups(role=['chr', 'prp'])

print r.get_rsv_resource_by_any_file_path(
    '/production/shows/nsa_dev/assets/chr/td_test'
)
#
# print r.get_rsv_step_by_any_file_path(
#     '/production/shows/nsa_dev/assets/chr/td_test/user/work.dongchangbao/maya/scenes/modeling/td_test.mod.modeling.modeling.v000_001.ma'
# )
#
# print r.get_rsv_task_by_any_file_path(
#     '/production/shows/nsa_dev/assets/chr/td_test/user/work.dongchangbao/maya/scenes/modeling/td_test.mod.modeling.modeling.v000_001.ma'
# )
