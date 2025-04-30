# coding:utf-8
import lnx_wotrix.core as lnx_wtx_core

from . import task_tool as _task_tool


class GuiTaskCreateOpt(lnx_wtx_core.DccTaskCreateOpt):
    RESOURCE_TYPE = 'asset'

    STEP = 'gnl'
    TASK = 'general'

    def __init__(self, *args, **kwargs):
        super(GuiTaskCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src_fnc(self, *args, **kwargs):
        pass

    def create_groups_for(self, task):
        task_tool_opt = self._task_session.generate_opt_for(_task_tool.GuiTaskToolOpt)
        if task_tool_opt:
            task_tool_opt.create_groups_for(task)
