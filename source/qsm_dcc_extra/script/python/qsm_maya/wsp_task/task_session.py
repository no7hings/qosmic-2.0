# coding:utf-8
import copy

import lxgui.qt.core as gui_qt_core

import qsm_maya.core as qsm_mya_core

import qsm_general.wsp_task as qsm_dcc_wsp_task

from . import task_create as _task_create

from . import task_tool as _task_tool

from . import task_release as _task_publish


class TaskSession(qsm_dcc_wsp_task.TaskSession):

    def generate_task_create_opt(self):
        task = self._properties['task']
        if 'asset' in self._properties:
            if task == 'cfx_rig':
                return _task_create.MayaAssetCfxRigCreateOpt(
                    self, self._properties
                )
            return _task_create.MayaAssetGnlTaskCreateOpt(
                self, self._properties
            )
        elif 'shot' in self._properties:
            if task == 'cfx':
                return _task_create.MayaShotCfxCreateOpt(
                    self, self._properties
                )
            return _task_create.MayaAssetGnlTaskCreateOpt(
                self, self._properties
            )
        return _task_create.MayaGnlTaskCreateOpt(
            self, self._properties
        )

    def generate_task_tool_opt(self):
        task = self._properties['task']
        if 'asset' in self._properties:
            if task == 'cfx_rig':
                return _task_tool.MayaAssetCfxRigToolOpt(
                    self, self._properties
                )
            return _task_tool.MayaAssetGnlToolOpt(
                self, self._properties
            )
        elif 'shot' in self._properties:
            if task == 'cfx':
                return _task_tool.MayaShotCfxToolOpt(
                    self, self._properties
                )
            return _task_tool.MayaShotGnlToolOpt(
                self, self._properties
            )
        return _task_tool.MayaGnlToolOpt(
            self, self._properties
        )

    def generate_task_release_opt(self):
        task = self._properties['task']
        if 'asset' in self._properties:
            if task == 'cfx_rig':
                return _task_publish.MayaAssetCfxRigReleaseOpt(
                    self, self._properties
                )
            return _task_publish.MayaAssetGnlReleaseOpt(
                self, self._properties
            )
        return _task_publish.MayaGnlReleaseOpt(
            self, self._properties
        )

    def __init__(self, *args, **kwargs):
        super(TaskSession, self).__init__(*args, **kwargs)

    def get_last_version_code(self):
        kwargs = copy.copy(self._properties)
        if 'version' in kwargs:
            kwargs.pop('version')

        pattern_opt = self._task_parse.generate_resource_source_task_scene_src_pattern_opt_for(
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

        scene_ptn_opt = self._task_parse.generate_resource_source_task_scene_src_pattern_opt_for(**kwargs)
        scene_path = scene_ptn_opt.get_value()
        if qsm_mya_core.SceneFile.save_to_with_dialog(scene_path) is True:
            kwargs['result'] = scene_path
            thumbnail_ptn_opt = self._task_parse.generate_resource_source_task_scene_src_thumbnail_pattern_opt_for(
                **kwargs
            )
            thumbnail_path = thumbnail_ptn_opt.get_value()

            gui_qt_core.QtMaya.make_snapshot(thumbnail_path)
            return kwargs

