# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.web as bsc_web

import qsm_task.process as qsm_tsk_process

time_tag = bsc_core.BscSystem.get_time_tag()

if qsm_tsk_process.TaskProcessClient.get_server_status():
    # qsm_tsk_process.TaskProcessClient.set_pool_maximum(5)
    # print qsm_tsk_process.TaskProcessClient.get_worker_status()
    for i_index, i_cmd_script in enumerate(
        [
            # r'rez-env python27 -- python -c "import time; time.sleep(30); print \"A\"; raise RuntimeError()"',
            r'rez-env python27 -- python -c "import time; time.sleep(10); print \"B\""',
            r'rez-env python27 -- python -c "import time; time.sleep(20); print \"C\""',
            r'rez-env python27 -- python -c "import time; time.sleep(30); print \"D\""',
            r'rez-env python27 -- python -c "import time; time.sleep(40); print \"E\""',
            r'rez-env python27 -- python -c "import time; time.sleep(50); print \"F\""',
            r'rez-env python27 -- python -c "import time; time.sleep(60); print \"G\""',
            # r'rez-env python27 -- python -c "import time; time.sleep(10); print \"H\""',
            # r'rez-env python27 -- python -c "import time; time.sleep(20); print \"I\""',
            # r'rez-env python27 -- python -c "import time; time.sleep(30); print \"J\""',
            # r'rez-env python27 -- python -c "import time; time.sleep(40); print \"K\""',
        ]
    ):
        qsm_tsk_process.TaskProcessClient.new_entity(
            cmd_script=i_cmd_script,
            group=None,
            type='test',
            name='[playblast][1280x720][1-32]'.format(i_index),
            icon_name='application/maya',
            output_file='Z:/temeporaries/dongchangbao/playblast/test_source.mov',
            completed_notice=bsc_web.UrlOptions.to_string(
                dict(
                    title='通知',
                    message='拍屏结束了, 是否打开视频?',
                    ok_python_script='import os; os.startfile("Z:/temeporaries/dongchangbao/playblast/test_source.mov")',
                    status='normal',
                )
            )
        )

