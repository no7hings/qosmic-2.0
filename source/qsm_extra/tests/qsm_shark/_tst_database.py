# coding:utf-8
import lnx_shark.database as dtb

stage = dtb.Stage()

print(stage.find_all_projects())

# project = stage.get_project(name='QSM_TST')

# print dict(project)

# stage.create_project(name='QSM_TST')
