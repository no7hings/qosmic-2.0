# coding:utf-8
import qsm_maya.core as qsm_mya_core

from ...base.gui_operates import task_create as _shot_gnl_task_create


class GuiTaskCreateOpt(_shot_gnl_task_create.GuiTaskCreateOpt):
    STEP = 'lay'
    TASK = 'layout'

    def __init__(self, *args, **kwargs):
        super(GuiTaskCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src_fnc(
        self,
        scene_src_path,
    ):
        qsm_mya_core.SceneFile.save_to(scene_src_path)
