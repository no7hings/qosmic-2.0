# coding:utf-8
from qsm_lazy_wsp.gui.abstracts import unit_for_task_manager as _abs_unit_for_task_manager

import qsm_maya_lazy_wsp.core as mya_lzy_wps_core

import qsm_maya.core as qsm_mya_core


class PrxUnitForAssetTaskManager(_abs_unit_for_task_manager.AbsPrxUnitForTaskManager):
    TASK_PARSE_CLS = mya_lzy_wps_core.TaskParse

    RESOURCE_TYPE = TASK_PARSE_CLS.ResourceTypes.Asset

    GUI_KEY = RESOURCE_TYPE

    def on_open_task_scene(self, properties):
        scene_path = properties.get('result')
        if scene_path:
            if qsm_mya_core.SceneFile.open_with_dialog(scene_path) is True:
                self.gui_load_task_unit_scene(properties)

    def dcc_set_scene_project(self, task_session):
        variants = task_session.properties
        resource_type = variants['resource_type']
        maya_dir_path = task_session.get_file_for('{}-source-maya-dir'.format(resource_type))
        qsm_mya_core.Workspace.create(maya_dir_path)

    def __init__(self, *args, **kwargs):
        super(PrxUnitForAssetTaskManager, self).__init__(*args, **kwargs)
