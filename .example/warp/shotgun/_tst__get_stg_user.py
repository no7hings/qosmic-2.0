# coding:utf-8
import lxbasic.shotgun as bsc_shotgun

c = bsc_shotgun.StgConnector()

us = c.get_stg_users(name=['笔帽'])

print us

# print urllib.urlopen(i).read()

for i in us:
    print c.to_query(i).get('email')
    print c.to_query(i).get('login')
