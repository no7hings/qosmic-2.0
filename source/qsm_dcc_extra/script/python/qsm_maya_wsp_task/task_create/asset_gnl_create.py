# coding:utf-8
import qsm_wsp_task as qsm_dcc_wsp_task


class MayaAssetGnlTaskCreateOpt(qsm_dcc_wsp_task.DccTaskCreateOpt):
    def __init__(self, *args, **kwargs):
        super(MayaAssetGnlTaskCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src(self, *args, **kwargs):
        pass

    def create_groups_for(self, task):
        task_tool_opt = self._task_session.generate_task_tool_opt()
        if task_tool_opt:
            task_tool_opt.create_groups_for(task)
