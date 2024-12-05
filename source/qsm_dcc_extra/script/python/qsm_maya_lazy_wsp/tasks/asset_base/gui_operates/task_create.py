# coding:utf-8
import qsm_lazy_wsp.core as lzy_wsp_core

from . import task_tool as _task_tool


class MayaAssetTaskCreateOpt(lzy_wsp_core.DccTaskCreateOpt):
    RESOURCE_BRANCH = 'asset'

    STEP = 'gnl'
    TASK = 'general'

    def __init__(self, *args, **kwargs):
        super(MayaAssetTaskCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src(self, *args, **kwargs):
        pass

    def create_groups_for(self, task):
        task_tool_opt = self._task_session.generate_opt_for(_task_tool.MayaAssetTaskToolOpt)
        if task_tool_opt:
            task_tool_opt.create_groups_for(task)
