# coding:utf-8
import lnx_houdini.core as lnx_hou_core

from ...base.gui_operates import task_create as _asset_gnl_task_create


class GuiTaskCreateOpt(_asset_gnl_task_create.GuiTaskCreateOpt):
    STEP = 'gnl'
    TASK = 'gnl_testing'

    def __init__(self, *args, **kwargs):
        super(GuiTaskCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src_fnc(self, scene_src_path):
        lnx_hou_core.SceneFile.save_to(scene_src_path)
