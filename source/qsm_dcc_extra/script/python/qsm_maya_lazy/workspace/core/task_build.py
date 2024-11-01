# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_lazy.workspace.core as qsm_lzy_wsp_core

import qsm_maya.core as qsm_mya_core

from . import task_worker as _asset_make


class TaskBuild(qsm_lzy_wsp_core.TaskBuild):
    def __init__(self, *args, **kwargs):
        super(TaskBuild, self).__init__(*args, **kwargs)

    def execute(self):
        task = self._properties['task']
        if 'asset' in self._properties:
            if task == 'cfx_rig':
                # reference rig
                rig_scene_ptn_opt = self._task_parse.generate_pattern_opt_for(
                    'asset-release-rig-scene-file', **self._properties
                )

                rig_scene_path = rig_scene_ptn_opt.get_value()
                if bsc_storage.StgPath.get_is_file(rig_scene_path):
                    self.create_groups_for(task)

                    qsm_mya_core.SceneFile.reference_file(
                        rig_scene_path,
                        namespace='rig'
                    )

    def create_groups_for(self, task):
        task_worker = _asset_make.MayaAssetTaskWorker(
            self._task_parse, self._properties
        )
        task_worker.create_groups_for(task)
