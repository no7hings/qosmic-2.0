# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.web as bsc_web

import lxgui.core as gui_core

import qsm_prc_task.process as qsm_prc_tsk_process


class BackstageSubmit:

    @classmethod
    def execute(
        cls,
        task_group, task_type, task_name,
        cmd_script, icon_name, file_path, output_file_path, completed_notice_dict,
    ):
        if qsm_prc_tsk_process.TaskProcessClient.get_server_status():
            qsm_prc_tsk_process.TaskProcessClient.new_entity(
                group=task_group,
                type=task_type,
                name=task_name,
                cmd_script=cmd_script,
                icon_name=icon_name,
                file=bsc_core.ensure_unicode(file_path),
                output_file=bsc_core.ensure_unicode(output_file_path),
                # must use string
                completed_notice=bsc_web.UrlOptions.to_string(
                    completed_notice_dict
                )
            )

            if gui_core.GuiUtil.get_language() == 'chs':
                gui_core.GuiApplication.exec_message_dialog(
                    '后台任务提交成功。',
                    status='correct'
                )
            else:
                gui_core.GuiApplication.exec_message_dialog(
                    'Backstage task submit successful.',
                    status='correct'
                )
        else:
            if gui_core.GuiUtil.get_language() == 'chs':
                gui_core.GuiApplication.exec_message_dialog(
                    '后台任务服务器未启动，启动“Y:/desktop-tools/懒人任务管理”以继续。',
                    status='warning'
                )
            else:
                gui_core.GuiApplication.exec_message_dialog(
                    'Backstage task server is not launched, launch "Y:/desktop-tools/lazy-task-manager" for continue.',
                    status='warning'
                )

