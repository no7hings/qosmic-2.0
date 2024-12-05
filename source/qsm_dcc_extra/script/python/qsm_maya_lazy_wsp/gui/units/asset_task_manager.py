# coding:utf-8
from qsm_lazy_wsp.gui.abstracts import unit_for_task_manager as _abs_unit_for_task_manager

import qsm_maya_lazy_wsp.core as mya_lzy_wps_core

import qsm_maya.core as qsm_mya_core


class PrxUnitForAssetTaskManager(_abs_unit_for_task_manager.AbsPrxUnitForTaskManager):
    GUI_KEY = 'asset'

    TASK_PARSE_CLS = mya_lzy_wps_core.TaskParse

    RESOURCE_BRANCH = 'asset'

    def on_open_task_scene(self, properties):
        scene_path = properties.get('result')
        if scene_path:
            if qsm_mya_core.SceneFile.open_with_dialog(scene_path) is True:
                self.gui_load_task_scene(properties)

    def __init__(self, *args, **kwargs):
        super(PrxUnitForAssetTaskManager, self).__init__(*args, **kwargs)
