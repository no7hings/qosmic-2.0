# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from ...base.gui_operates import task_create as _asset_gnl_task_create


class GuiTaskCreateOpt(_asset_gnl_task_create.GuiTaskCreateOpt):
    STEP = 'cfx'
    TASK = 'cfx_rig'

    def __init__(self, *args, **kwargs):
        super(GuiTaskCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src_fnc(self, scene_src_path, upstream_scene_path=None):
        task = self._properties['task']

        if upstream_scene_path is None:
            upstream_scene_path = self._task_session.get_file_or_dir_for('asset-disorder-rig_scene-maya-file')

        if upstream_scene_path:
            if bsc_storage.StgPath.get_is_file(upstream_scene_path):
                qsm_mya_core.SceneFile.reference_file(
                    upstream_scene_path,
                    namespace='rig'
                )

        self.create_groups_for(task)

        qsm_mya_core.SceneFile.save_to(scene_src_path)
