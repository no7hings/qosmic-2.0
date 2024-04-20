# coding:utf-8
import lxbasic.shotgun as bsc_shotgun

import lxresolver.core as rsv_core

# task_id = 202455

task_id = 228812

# task_id = 203373

c = bsc_shotgun.StgConnector()

task_data = c.get_data_from_task_id(task_id)

r = rsv_core.RsvBase.generate_root()

rsv_project = r.get_rsv_project(project='nsa_dev')

rsv_project.auto_create_user_task_directory_by_task_data(task_data)
