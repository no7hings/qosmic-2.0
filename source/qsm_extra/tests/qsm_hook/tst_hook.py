# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.web as bsc_web

import qsm_hook.core as qsm_hok_core

time_tag = bsc_core.SysBaseMtd.get_time_tag()


for i_index, i_cmd in enumerate(
    [
        # r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"A\\\"\; raise RuntimeError()")"',
        r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"B\\\"\")"',
        # r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"C\\\"\")"',
        # r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"D\\\"\")"',
        # r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"E\\\"\")"',
        # r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"F\\\"\")"',
        # r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"G\\\"\")"',
        # r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"H\\\"\")"',
        # r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"I\\\"\")"',
        # r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"J\\\"\")"',
        # r'rez-env maya-2019 qsm_dcc_main -- mayabatch -command "python(\"import lxsession.commands as ssn_commands;ssn_commands.execute_option_hook(option=\\\"option_hook_key=dcc-process/maya-cache-process&method=playblast&file=Z:/temeporaries/dongchangbao/playblast/test_source.ma&camera=|persp|perspShape&start_frame=0&end_frame=32&width=1280&height=720\\\")\")"'
    ]
):
    qsm_hok_core.Hook.new_task(
        group='[playblast][{}]'.format(time_tag),
        name='[max][1-32]'.format(i_index),
        cmd_script=i_cmd,
        completion_notice=bsc_web.UrlOptions.to_string(
            dict(
                title='通知',
                message='拍屏结束了, 是否打开视频?',
                ok_python_script='import os; os.startfile("Z:/temeporaries/dongchangbao/playblast/test_source.mov")',
                status='normal'
            )
        )
    )
