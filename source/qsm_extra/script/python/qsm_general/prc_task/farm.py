# coding:utf-8
import lxbasic.deadline as bsc_deadline

import lxgui.core as gui_core

import lxsession.commands as ssn_commands

from .. import process as _process


class FarmSubmit:

    @classmethod
    def execute_by_hook_option(
        cls, option_hook
    ):
        c = bsc_deadline.DdlBase.generate_connection()
        groups = c.Groups.GetGroupNames()
        if isinstance(groups, list):

            session = ssn_commands.execute_option_hook_by_deadline(option_hook)
            ddl_job_id = session.get_ddl_job_id()

            if gui_core.GuiUtil.get_language() == 'chs':
                gui_core.GuiApplication.exec_message_dialog(
                    '农场任务提交成功，ID：{}。'.format(ddl_job_id),
                    status='correct'
                )
            else:
                gui_core.GuiApplication.exec_message_dialog(
                    'Farm task submit successful, ID: {}.'.format(ddl_job_id),
                    status='correct'
                )
        else:
            if gui_core.GuiUtil.get_language() == 'chs':
                gui_core.GuiApplication.exec_message_dialog(
                    '农场服务器未启动。',
                    status='warning'
                )
            else:
                gui_core.GuiApplication.exec_message_dialog(
                    'Farm server is not launched.',
                    status='warning'
                )
