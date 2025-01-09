# coding:utf-8
import lxbasic.shotgun as bsc_shotgun

c = bsc_shotgun.StgConnector()

print c.find_task_id(
    project='nsa_dev',
    resource='z87',
    task='lightrig'
)
