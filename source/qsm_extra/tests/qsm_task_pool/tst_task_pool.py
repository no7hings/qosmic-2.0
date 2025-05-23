# coding:utf-8
from __future__ import print_function

import lnx_backstage.core as lzy_bks_core

p = lzy_bks_core.TaskPool.generate()

for i in range(5):
    p.new_entity(
        group='[dynamic-gpu-cache-generate][2024-04-28-20:00]',
        name='[dynamic-gpu-cache-generate][max][1-32]'.format(i),
        cmd_script=r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"A\\\"\")"',
    )

for i_task in p.get_tasks():
    print(i_task)
    # print(i_task.get_status())
