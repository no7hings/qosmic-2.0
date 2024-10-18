# coding:utf-8
import lxbasic.core as bsc_core

import qsm_prc_task.core as qsm_tsk_core

p = qsm_tsk_core.TaskPool.generate()
p.do_update()

time_tag = bsc_core.BscSystem.get_time_tag()

tasks = []

for i_index, i_cmd in enumerate(
    [
        # r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"A\\\"\; raise RuntimeError()")"',
        r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"B\\\"\")"',
        r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"C\\\"\")"',
        r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"D\\\"\")"',
        r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"E\\\"\")"',
        r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"F\\\"\")"',
        # r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"G\\\"\")"',
        # r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"H\\\"\")"',
        # r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"I\\\"\")"',
        # r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"J\\\"\")"',
    ]
):
    i_task = p.new_task(
        group='[dynamic-gpu-cache-generate][{}]'.format(time_tag),
        name='[dynamic-gpu-cache-generate][max][1-32]'.format(i_index),
        cmd_script=i_cmd,
    )
    tasks.append(i_task)

[i.do_wait_for_start() for i in tasks]


