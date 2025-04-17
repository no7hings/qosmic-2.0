# coding:utf-8
from lnx_wotrix.gui.abstracts import unit_for_task_manager as _abs_unit_for_task_manager

import lnx_katana.core as lnx_hou_core

from ... import core as _lnx_wtx_core


class GuiTaskManagerMain(_abs_unit_for_task_manager.AbsPrxUnitForTaskManager):
    TASK_PARSE_CLS = _lnx_wtx_core.TaskParse

    RESOURCE_TYPE = TASK_PARSE_CLS.ResourceTypes.Asset

    GUI_KEY = RESOURCE_TYPE

    def on_open_task_scene(self, properties):
        scene_path = properties.get('result')
        if scene_path:
            if lnx_hou_core.SceneFile.open_with_dialog(scene_path) is True:
                self.gui_load_task_unit_scene(properties)

    def dcc_set_scene_project(self, task_session):
        variants = task_session.properties
        resource_type = variants['resource_type']
        katana_dir_path = task_session.get_file_for('{}-source-katana-dir'.format(resource_type))
        lnx_hou_core.Workspace.create(katana_dir_path)

    def __init__(self, *args, **kwargs):
        super(GuiTaskManagerMain, self).__init__(*args, **kwargs)
