# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.web as bsc_web

import lxgui.core as gui_core

import qsm_lazy_bks.worker as lzy_bks_worker


class BackstageTaskSubmit:

    @classmethod
    def execute(
        cls,
        task_group, task_type, task_name,
        cmd_script, icon_name, file_path, output_file_path, completed_notice_dict,
    ):
        lzy_bks_worker.TaskClient.new_entity(
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
                '后台任务提交成功，可在“懒人任务管理”查看任务进度。',
                status='correct'
            )
        else:
            gui_core.GuiApplication.exec_message_dialog(
                (
                    'The background task is submitted successfully, '
                    'and the task progress can be viewed in "lazy-task-manager".'
                ),
                status='correct'
            )

    @classmethod
    def check_is_valid(cls):
        if lzy_bks_worker.TaskClient.get_server_status():
            return True
        else:
            if gui_core.GuiUtil.get_language() == 'chs':
                gui_core.GuiApplication.exec_message_dialog(
                    '后台任务服务器未启动，启动“Y:/desktop-tools/懒人任务管理”以继续。',
                    status='warning'
                )
            else:
                gui_core.GuiApplication.exec_message_dialog(
                    (
                        'The backstage task server is not started. '
                        'Start "Y:/desktop-tools/Lazy Task Management" to continue.'
                    ),
                    status='warning'
                )
            return False

