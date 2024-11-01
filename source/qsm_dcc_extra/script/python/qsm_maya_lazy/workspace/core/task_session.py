# coding:utf-8
import copy

import lxgui.qt.core as gui_qt_core

import qsm_maya.core as qsm_mya_core

import qsm_lazy.workspace.core as qsm_lzy_wsp_core

from . import task_worker as _asset_worker


class TaskSession(qsm_lzy_wsp_core.TaskSession):

    def generate_task_worker(self):
        task = self._properties['task']
        if task == 'cfx_rig':
            return _asset_worker.MayaAssetCfxRigWorker(
                self._task_parse, self._properties
            )
        return _asset_worker.MayaAssetTaskWorker(
            self._task_parse, self._properties
        )

    def __init__(self, *args, **kwargs):
        super(TaskSession, self).__init__(*args, **kwargs)

    def get_last_version_code(self):
        kwargs = copy.copy(self._properties)
        if 'version' in kwargs:
            kwargs.pop('version')

        pattern_opt = self._task_parse.generate_task_scene_pattern_opt_for(
            **kwargs
        )
        matches = pattern_opt.find_matches(sort=True)
        if matches:
            return int(matches[-1]['version'])
        return 0

    def save_source_task_scene(self):
        version = self.get_last_version_code()

        kwargs = copy.copy(self._properties)
        kwargs['version'] = str(version+1).zfill(3)

        scene_ptn_opt = self._task_parse.generate_task_scene_pattern_opt_for(**kwargs)
        scene_path = scene_ptn_opt.get_value()
        if qsm_mya_core.SceneFile.save_to_with_dialog(scene_path) is True:
            kwargs['result'] = scene_path
            thumbnail_ptn_opt = self._task_parse.generate_task_scene_thumbnail_pattern_opt_for(**kwargs)
            thumbnail_path = thumbnail_ptn_opt.get_value()

            gui_qt_core.QtMaya.make_snapshot(thumbnail_path)
            return kwargs

