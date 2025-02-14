# coding:utf-8
from qsm_lazy_workspace.gui.abstracts import unit_for_task_manager as _abs_unit_for_task_manager

import qsm_houdini.core as qsm_hou_core

from ... import core as _lzy_wps_core


class PrxUnitForProjectTaskManager(_abs_unit_for_task_manager.AbsPrxUnitForTaskManager):
    TASK_PARSE_CLS = _lzy_wps_core.TaskParse

    RESOURCE_TYPE = TASK_PARSE_CLS.ResourceTypes.Project

    GUI_KEY = RESOURCE_TYPE

    def on_open_task_scene(self, properties):
        scene_path = properties.get('result')
        if scene_path:
            if qsm_hou_core.SceneFile.open_with_dialog(scene_path) is True:
                self.gui_load_task_unit_scene(properties)

    def dcc_set_scene_project(self, task_session):
        variants = task_session.properties
        resource_type = variants['resource_type']
        maya_dir_path = task_session.get_file_for('{}-source-maya-dir'.format(resource_type))
        qsm_hou_core.Workspace.create(maya_dir_path)

    def __init__(self, window, session, *args, **kwargs):
        super(PrxUnitForProjectTaskManager, self).__init__(window, session, *args, **kwargs)
