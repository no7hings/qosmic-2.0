# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from . import shot_gnl_create as _shot_gnl


class MayaShotCfxDressingCreateOpt(_shot_gnl.MayaShotGnlTaskCreateOpt):
    def __init__(self, *args, **kwargs):
        super(MayaShotCfxDressingCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src(self, scene_src_path, upstream_scene_path=None):

        if upstream_scene_path is None:
            upstream_scene_path = self._task_session.get_file_for('shot-disorder-animation_scene_s-file')

        if upstream_scene_path:
            if bsc_storage.StgPath.get_is_file(upstream_scene_path):
                qsm_mya_core.SceneFile.open(upstream_scene_path)

        qsm_mya_core.SceneFile.save_to(scene_src_path)

