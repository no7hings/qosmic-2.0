# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_general.wsp_task as qsm_dcc_wsp_task

import qsm_maya.core as qsm_mya_core

from . import task_tool as _task_tool


class DccTaskCreateOpt(qsm_dcc_wsp_task.DccTaskCreateOpt):
    def __init__(self, *args, **kwargs):
        super(DccTaskCreateOpt, self).__init__(*args, **kwargs)

    def create_groups_for(self, task):
        task_worker = _task_tool.MayaAssetGnlToolOpt(
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

        rig_scene_path = self._task_session.get_file_for('asset-release-shit_rig_scene-maya-file')
        if rig_scene_path:
            if bsc_storage.StgPath.get_is_file(rig_scene_path):
                self.create_groups_for(task)
                qsm_mya_core.SceneFile.reference_file(
                    rig_scene_path,
                    namespace='rig'
                )
                return True
        return False


class MayaShotGnlTaskCreateOpt(qsm_dcc_wsp_task.DccTaskCreateOpt):
    def __init__(self, *args, **kwargs):
        super(MayaShotGnlTaskCreateOpt, self).__init__(*args, **kwargs)

    def build_source(self):
        pass

    def create_groups_for(self, task):
        task_tool_opt = self._task_session.generate_task_tool_opt()
        if task_tool_opt:
            task_tool_opt.create_groups_for(task)


class MayaShotCfxCreateOpt(MayaShotGnlTaskCreateOpt):
    def __init__(self, *args, **kwargs):
        super(MayaShotCfxCreateOpt, self).__init__(*args, **kwargs)

    def build_source(self):
        task = self._properties['task']

        animation_scene_path = self._task_session.get_file_for('shot-release-shit_animation_scene-file')
        if animation_scene_path:
            if bsc_storage.StgPath.get_is_file(animation_scene_path):
                self.create_groups_for(task)
                qsm_mya_core.SceneFile.import_scene(animation_scene_path)
                return True
        return False
