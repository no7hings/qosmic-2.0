# coding:utf-8
import lxbasic.shotgun as bsc_shotgun

c = bsc_shotgun.StgConnector()

q = c.get_stg_resource_query(
    project='nsa_dev', asset='nikki'
)
print q.get('sg_test_thumb')

