# coding:utf-8
import lxresolver.core as rsv_core

r = rsv_core.RsvBase.generate_root()

# rsv_project = r.get_rsv_project(project='cjd')
#
# rsv_shot = rsv_project.get_rsv_resource(
#     shot='e10060'
# )
#
# print rsv_shot
#
# rsv_tasks = rsv_shot.get_rsv_tasks(step='efx*')
#
# for i_rsv_task in rsv_tasks:
#     print i_rsv_task.name


print r.get_rsv_resources(
    project='cjd', branch='shot'
)
