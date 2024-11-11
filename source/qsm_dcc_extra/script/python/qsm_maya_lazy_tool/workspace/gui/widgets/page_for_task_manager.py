# coding:utf-8
from qsm_lazy_tool.workspace.gui.abstracts import page_for_task_manager as _abs_page_for_task_manager

import qsm_maya.wsp_task as qsm_mya_wsp_task

import qsm_maya.core as qsm_mya_core


class PrxPageForAssetTaskManager(_abs_page_for_task_manager.AbsPrxPageForTaskManager):
    TASK_PARSE_CLS = qsm_mya_wsp_task.TaskParse

    RESOURCE_BRANCH = 'asset'

    def on_open_task_scene(self, properties):
        scene_path = properties.get('result')
        if scene_path:
            if qsm_mya_core.SceneFile.open_with_dialog(scene_path) is True:
                self.gui_load_task_scene(properties)

    def __init__(self, *args, **kwargs):
        super(PrxPageForAssetTaskManager, self).__init__(*args, **kwargs)


class PrxPageForShotTaskManager(_abs_page_for_task_manager.AbsPrxPageForTaskManager):
    TASK_PARSE_CLS = qsm_mya_wsp_task.TaskParse

    RESOURCE_BRANCH = 'shot'

    def on_open_task_scene(self, properties):
        scene_path = properties.get('result')
        if scene_path:
            if qsm_mya_core.SceneFile.open_with_dialog(scene_path) is True:
                self.gui_load_task_scene(properties)

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForShotTaskManager, self).__init__(window, session, *args, **kwargs)
