# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from ...base.gui_operates import task_create as _shot_gnl_task_create


class GuiTaskCreateOpt(_shot_gnl_task_create.GuiTaskCreateOpt):
    STEP = 'ani'
    TASK = 'animation'

    def __init__(self, *args, **kwargs):
        super(GuiTaskCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src_fnc(
        self,
        scene_src_path, upstream_scene_path=None,
    ):
        if upstream_scene_path:
            if bsc_storage.StgPath.get_is_file(upstream_scene_path):
                # load source
                qsm_mya_core.SceneFile.open(upstream_scene_path)

        qsm_mya_core.SceneFile.save_to(scene_src_path)

