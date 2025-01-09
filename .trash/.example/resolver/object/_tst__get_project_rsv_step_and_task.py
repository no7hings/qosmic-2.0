# coding:utf-8
import lxresolver.core as rsv_core

r = rsv_core.RsvBase.generate_root()

p = r.get_rsv_project(
    project='nsa_dev'
)
# print p.properties
# project step
# print p.get_rsv_step(step='srf')
# print p.get_rsv_steps()
# print p.get_rsv_tasks()
# project task
rsv_task = p.get_rsv_task(step='srf', task='template')
print rsv_task.properties
# rsv_unit = rsv_task.get_rsv_unit(keyword='project-user-maya-scene-src-file')
# print rsv_unit.get_result(version='all')
# rsv_unit = rsv_task.get_rsv_unit(keyword='project-user-katana-scene-src-file')
# print rsv_unit.get_result(version='all')
# print p.get_rsv_tasks(step='srf')
# project steps
# print p.get_rsv_steps()
#
# print p.get_rsv_step(sequence='z87', step='lgtrig')
# print p.get_rsv_tasks(sequence='z87', step='lgtrig')
#
# print p.get_rsv_steps(sequence='z87')

# print p.get_rsv_step(asset='genariceyes', step='srf')
# print p.get_rsv_task(asset='genariceyes', step='srf', task='srf_anishading')
