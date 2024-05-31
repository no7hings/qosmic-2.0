# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.web as bsc_web

import qsm_task.process as qsm_tsk_process

time_tag = bsc_core.SysBaseMtd.get_time_tag()

bsc_core.SysBaseMtd.get_time_tag()

print qsm_tsk_process.TaskProcessClient.get_server_status()

# if qsm_tsk_process.TaskProcessClient.get_server_status():
#     for i_index, i_cmd in enumerate(
#         [
#             r'rez-env maya-2019 qsm_dcc_main -- mayabatch -command "python(\"import lxsession.commands as ssn_commands;ssn_commands.execute_option_hook(option=\\\"option_hook_key=dcc-process/maya-cache-process&method=playblast&file=Z:/temeporaries/dongchangbao/playblast/test_source.ma&camera=|persp|perspShape&start_frame=0&end_frame=32&width=1280&height=720\\\")\")"'
#         ]
#     ):
#         qsm_tsk_process.TaskProcessClient.new_entity(
#             # group='[playblast][{}]'.format(time_tag),
#             group=None,
#             name='[playblast][test_source.ma][1280x720][1-32]',
#             cmd_script=i_cmd,
#             icon_name='application/maya',
#             output_file='Z:/temeporaries/dongchangbao/playblast/test_source.mov',
#             completed_notice=bsc_web.UrlOptions.to_string(
#                 dict(
#                     title='通知',
#                     message='拍屏结束了, 是否打开视频?',
#                     ok_python_script='import os; os.startfile("Z:/temeporaries/dongchangbao/playblast/test_source.mov")',
#                     status='normal'
#                 )
#             )
#         )
