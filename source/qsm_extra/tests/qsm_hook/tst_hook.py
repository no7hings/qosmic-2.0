# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.web as bsc_web

import qsm_task.process as qsm_tsk_process

time_tag = bsc_core.BscSystem.get_time_tag()

if qsm_tsk_process.TaskProcessClient.get_server_status():
    ts = []
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
        qsm_tsk_process.TaskProcessClient.new_entity(
            # group='[playblast][{}]'.format(time_tag),
            cmd_script=i_cmd,
            group=None,
            type='test',
            name='[playblast][1280x720][1-32]'.format(i_index),
            completed_notice=bsc_web.UrlOptions.to_string(
                dict(
                    title='通知',
                    message='拍屏结束了, 是否打开视频?',
                    ok_python_script='import os; os.startfile("Z:/temeporaries/dongchangbao/playblast/test_source.mov")',
                    status='normal'
                )
            )
        )
