# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from ...base.gui_operates import task_create as _asset_gnl_task_create


class MayaAssetRigTestingCreateOpt(_asset_gnl_task_create.MayaAssetTaskCreateOpt):
    STEP = 'rig'
    TASK = 'rig_testing'

    def __init__(self, *args, **kwargs):
        super(MayaAssetRigTestingCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src_fnc(self, scene_src_path, upstream_scene_path=None):

        if upstream_scene_path is None:
            upstream_scene_path = self._task_session.get_file_for('asset-disorder-rig_scene-maya-file')

        if upstream_scene_path:
            if bsc_storage.StgPath.get_is_file(upstream_scene_path):
                qsm_mya_core.SceneFile.reference_file(
                    upstream_scene_path,
                    namespace='rig'
                )

        qsm_mya_core.SceneFile.save_to(scene_src_path)
