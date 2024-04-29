# coding:utf-8
import qsm_task_pool.core as prc_task_core

c = prc_task_core.Pool.generate()

for i in range(5):
    c.new_task(
        batch_name='[dynamic-gpu-cache-generate][2024-04-28-20:00]',
        name='[dynamic-gpu-cache-generate][max][1-32]'.format(i),
        cmd_script=r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"A\\\"\")"',
    )

for i_task in c.get_tasks():
    print i_task
    # print i_task.get_status()
