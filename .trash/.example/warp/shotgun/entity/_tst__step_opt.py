# coding:utf-8
import lxbasic.shotgun as bsc_shotgun

c = bsc_shotgun.StgConnector()

r_q = c.get_stg_resource_query(
    project='nsa_dev', asset='nikki'
)
r_o = bsc_shotgun.StgResourceOpt(r_q)

s_q = c.get_stg_step_query(
    step='srf'
)

s_o = bsc_shotgun.StgStepOpt(s_q)

downstream_stg_steps = s_o.get_downstream_stg_steps()
print s_o.get_notice_stg_users()

print r_o.get_stg_tasks(downstream_stg_steps)

print r_o.get_stg_shots()

print r_o.get_shot_stg_tasks(downstream_stg_steps)

