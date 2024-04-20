# coding:utf-8
import lxmaya.ssn.objects as mya_ssn_objects

app = mya_ssn_objects.SsnRsvApplication()

rsp = app.get_rsv_scene_properties()

print rsp

print rsp.get('project')
print rsp.get('step')
print rsp.get(rsp.get('branch'))
print rsp.get('task')
#
sc = app.get_stg_connector()

si = sc.shotgun

print sc.get_stg_project(**rsp.value)
print sc.get_stg_resource(**rsp.value)
print sc.get_stg_step(**rsp.value)
print sc.get_stg_task(**rsp.value)
