# coding:utf-8
import lxbasic.shotgun as shotgun_core

c = shotgun_core.StgConnector()

p = c.get_stg_project_query(project='nsa_dev')

print shotgun_core.StgProjectOpt(p).get_color_space()
