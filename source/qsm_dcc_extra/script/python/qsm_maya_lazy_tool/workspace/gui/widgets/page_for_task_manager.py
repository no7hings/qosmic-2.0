# coding:utf-8
from qsm_lazy_tool.workspace.gui.abstracts import page_for_task_manager as _abs_page_for_task_manager

import qsm_maya_lazy.workspace.core as qsm_mya_lzy_wsp_core

import qsm_maya.core as qsm_mya_core


class PrxPageForTaskManager(_abs_page_for_task_manager.AbsPrxPageForTaskManager):
    TASK_PARSE_CLS = qsm_mya_lzy_wsp_core.TaskParse

    def on_open_task_scene(self, properties):
        scene_path = properties.get('result')
        if scene_path:
            if qsm_mya_core.SceneFile.open_with_dialog(scene_path) is True:
                self.gui_load_task_scene(properties)

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskManager, self).__init__(*args, **kwargs)
