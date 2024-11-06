# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_general.wsp_task as qsm_dcc_wsp_task

import qsm_maya.core as qsm_mya_core

import qsm_maya.steps.cfx_rig.core as qsm_mya_stp_cfx_rig_core

from . import task_tool as _asset_make


class DccTaskCreateOpt(qsm_dcc_wsp_task.DccTaskCreateOpt):
    def __init__(self, *args, **kwargs):
        super(DccTaskCreateOpt, self).__init__(*args, **kwargs)

    def execute(self):
        task = self._properties['task']
        if 'asset' in self._properties:
            if task == 'cfx_rig':
                # reference rig
                rig_scene_ptn_opt = self._task_session._task_parse.generate_pattern_opt_for(
                    'asset-release-shit-rig-scene-file', **self._properties
                )

                rig_scene_path = rig_scene_ptn_opt.get_value()
                if bsc_storage.StgPath.get_is_file(rig_scene_path):
                    self.create_groups_for(task)

                    qsm_mya_stp_cfx_rig_core.RigOpt.load_rig(rig_scene_path)

    def create_groups_for(self, task):
        task_worker = _asset_make.MayaAssetGnlToolOpt(
            self._task_session._task_parse, self._properties
        )
        task_worker.create_groups_for(task)


class MayaGnlTaskCreateOpt(qsm_dcc_wsp_task.DccTaskCreateOpt):
    def __init__(self, *args, **kwargs):
        super(MayaGnlTaskCreateOpt, self).__init__(*args, **kwargs)

    def build_source(self):
        pass


class MayaAssetGnlTaskCreateOpt(qsm_dcc_wsp_task.DccTaskCreateOpt):
    def __init__(self, *args, **kwargs):
        super(MayaAssetGnlTaskCreateOpt, self).__init__(*args, **kwargs)

    def build_source(self):
        pass

    def create_groups_for(self, task):
        task_tool_opt = self._task_session.generate_task_tool_opt()
        if task_tool_opt:
            task_tool_opt.create_groups_for(task)
        

class MayaAssetCfxRigCreateOpt(MayaAssetGnlTaskCreateOpt):
    def __init__(self, *args, **kwargs):
        super(MayaAssetCfxRigCreateOpt, self).__init__(*args, **kwargs)

    def build_source(self):
        task = self._properties['task']

        rig_scene_ptn_opt = self._task_session._task_parse.generate_pattern_opt_for(
            'asset-release-shit-rig-scene-file', **self._properties
        )
        rig_scene_path = rig_scene_ptn_opt.get_value()
        if bsc_storage.StgPath.get_is_file(rig_scene_path):
            self.create_groups_for(task)

            qsm_mya_core.SceneFile.reference_file(
                rig_scene_path,
                namespace='rig'
            )
