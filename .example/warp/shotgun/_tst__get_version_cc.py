# coding:utf-8
import lxbasic.shotgun as bsc_shotgun

c = bsc_shotgun.StgConnector()

v_q = c.get_stg_version_query(
    id='70080'
)
v_o = bsc_shotgun.StgVersionOpt(v_q)

r_o = bsc_shotgun.StgResourceOpt(v_o.get_stg_resource_query())

print r_o.get_cc_stg_users()

t_o = bsc_shotgun.StgTaskOpt(v_o.get_stg_task_query())

print t_o.get_cc_stg_users()

