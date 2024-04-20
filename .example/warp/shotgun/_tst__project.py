# coding:utf-8
import lxbasic.shotgun as bsc_shotgun

c = bsc_shotgun.StgConnector()

print c.get_stg_project_query(project='nsa_dev').get_all_keys()

# print c.get_stg_project_query(project='nsa_dev').get('users')
