# coding:utf-8
import qsm_general.wsp_task as qsm_dcc_wsp_task

import qsm_maya.core as qsm_mya_core

from . import task_session as _task_session


class TaskParse(qsm_dcc_wsp_task.TaskParse):
    TASK_SESSION_CLS = _task_session.TaskSession

    @classmethod
    def generate_task_session_by_resource_source_scene_src_auto(cls):
        return cls.generate_task_session_by_resource_source_scene_src(
            qsm_mya_core.SceneFile.get_current()
        )

    @classmethod
    def generate_task_session_by_asset_release_scene_src(cls, scene_path):
        task_parse = cls()

        ptn_opt = task_parse.asset_release_task_scene_src_pattern_opt
        variants = ptn_opt.get_variants(scene_path, extract=True)
        if variants:
            if 'asset' in variants:
                variants['resource_type'] = 'asset'
            return _task_session.TaskSession(task_parse, variants)

    def __init__(self):
        super(TaskParse, self).__init__()
