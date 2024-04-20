# coding:utf-8
import lxresolver.core as rsv_core

r = rsv_core.RsvBase.generate_root()

rsv_project = r.get_rsv_project(project='cjd')

rsv_shots = rsv_project.get_rsv_resources(branch='shot', sequence='e10')

task_args_lis = [
    ('rlo', 'rough_layout'),
    ('ani', 'blocking'),
    ('ani', 'animation'),
    ('flo', 'final_layout'),
]

task_args_lis.reverse()

lis = []

for i_rsv_shot in rsv_shots:
    i_rsv_tasks = i_rsv_shot.get_rsv_tasks()
    for j_task_args in task_args_lis:
        j_step, j_task = j_task_args
        j_rsv_task = i_rsv_shot.get_rsv_task(step=j_step, task=j_task)
        if j_rsv_task is not None:
            j_rsv_unit = j_rsv_task.get_rsv_unit(
                keyword='shot-component-usd-file'
            )
            j_file_path = j_rsv_unit.get_result()
            if j_file_path is not None:
                # print j_file_path
                lis.append(j_file_path)
                break


for i in lis:
    print i
