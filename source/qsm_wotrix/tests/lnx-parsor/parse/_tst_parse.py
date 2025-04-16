# coding:utf-8
import lnx_parsor.parse as c

stage = c.Stage()

project = stage.project('QSM_TST', space_key='source')

for i in project.roles():
    print(i.assets())
