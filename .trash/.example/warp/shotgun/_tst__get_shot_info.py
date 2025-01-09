# coding:utf-8
import lxbasic.shotgun as bsc_shotgun

c = bsc_shotgun.StgConnector()

print c.get_stg_resource_queries(
    project='lib', branch='shot'
)
