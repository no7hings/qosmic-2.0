# coding:utf-8
import lxbasic.shotgun as bsc_shotgun

c = bsc_shotgun.StgConnector()

t_q = c.get_stg_task_query(
    project='nsa_dev', asset='nikki', step='cam', task='camera'
)

t_o = bsc_shotgun.StgTaskOpt(
    t_q
)

print t_o.get_notice_stg_users()
