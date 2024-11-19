# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from . import shot_gnl_create as _shot_gnl


class MayaShotCfxClothCreateOpt(_shot_gnl.MayaShotGnlTaskCreateOpt):
    def __init__(self, *args, **kwargs):
        super(MayaShotCfxClothCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src(self, scene_src_path, upstream_scene_path=None, auto_load_cfx_rig=False, solver_start_frame=1):
        task = self._properties['task']

        if upstream_scene_path is None:
            upstream_scene_path = self._task_session.get_file_for('shot-disorder-animation_scene_s-file')

        if upstream_scene_path:
            if bsc_storage.StgPath.get_is_file(upstream_scene_path):
                # load source
                qsm_mya_core.SceneFile.open(upstream_scene_path)
                # qsm_mya_core.SceneFile.import_scene(upstream_scene_path)

        # create groups
        self.create_groups_for(task)

        if auto_load_cfx_rig is True:
            task_tool_opt = self._task_session.generate_task_tool_opt()
            task_tool_opt.load_cfx_rig_auto()

            task_tool_opt.apply_cfx_rig_solver_start_frame(solver_start_frame)

        qsm_mya_core.SceneFile.save_to(scene_src_path)

