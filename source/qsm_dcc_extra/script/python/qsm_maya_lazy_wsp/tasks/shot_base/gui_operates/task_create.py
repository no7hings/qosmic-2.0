# coding:utf-8
import qsm_lazy_wsp.core as lzy_wsp_core

from . import task_tool as _task_tool


class MayaShotTaskCreateOpt(lzy_wsp_core.DccTaskCreateOpt):
    RESOURCE_BRANCH = 'shot'

    STEP = 'gnl'
    TASK = 'general'

    def __init__(self, *args, **kwargs):
        super(MayaShotTaskCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src(self, *args, **kwargs):
        pass

    def create_groups_for(self, task):
        task_tool_opt = self._task_session.generate_opt_for(_task_tool.MayaShotTaskToolOpt)
        if task_tool_opt:
            task_tool_opt.create_groups_for(task)
