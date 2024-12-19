# coding:utf-8
from qsm_lazy_wsp.gui.abstracts import unit_for_task_manager as _abs_unit_for_task_manager

import qsm_maya_lazy_wsp.core as mya_lzy_wps_core

import qsm_maya.core as qsm_mya_core


class PrxUnitForShotTaskManager(_abs_unit_for_task_manager.AbsPrxUnitForTaskManager):
    GUI_KEY = 'shot'

    TASK_PARSE_CLS = mya_lzy_wps_core.TaskParse

    RESOURCE_TYPE = 'shot'

    def on_open_task_scene(self, properties):
        scene_path = properties.get('result')
        if scene_path:
            if qsm_mya_core.SceneFile.open_with_dialog(scene_path) is True:
                self.gui_load_task_scene(properties)

    def __init__(self, window, session, *args, **kwargs):
        super(PrxUnitForShotTaskManager, self).__init__(window, session, *args, **kwargs)
