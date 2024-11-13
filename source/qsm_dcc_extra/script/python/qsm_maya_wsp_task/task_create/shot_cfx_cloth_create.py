# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from . import shot_gnl_create as _shot_gnl


class MayaShotCfxClothCreateOpt(_shot_gnl.MayaShotGnlTaskCreateOpt):
    def __init__(self, *args, **kwargs):
        super(MayaShotCfxClothCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src(self, upstream_scene_path=None):
        task = self._properties['task']

        if upstream_scene_path is None:
            upstream_scene_path = self._task_session.get_file_for('shot-disorder-animation_scene-file')

        if upstream_scene_path:
            if bsc_storage.StgPath.get_is_file(upstream_scene_path):
                # create groups
                self.create_groups_for(task)
                # load source
                qsm_mya_core.SceneFile.import_scene(upstream_scene_path)
                return True
        return False
