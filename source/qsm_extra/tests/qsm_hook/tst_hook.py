# coding:utf-8
import lxbasic.core as bsc_core

import qsm_hook.core as qsm_hok_core

time_tag = bsc_core.SysBaseMtd.get_time_tag()


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
    qsm_hok_core.Hook.execute(
        group='[test][{}]'.format(time_tag),
        name='[max][1-32]'.format(i_index),
        cmd_script=i_cmd,
    )
