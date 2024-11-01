# coding:utf-8
import qsm_lazy.workspace.core as qsm_lzy_wsp_core

import qsm_maya.core as qsm_mya_core

from . import task_session as _task_session


class TaskParse(qsm_lzy_wsp_core.TaskParse):
    @classmethod
    def generate_session_for_auto(cls):
        task_parse = cls()

        scene_path = qsm_mya_core.SceneFile.get_current()

        scene_ptn_opt = task_parse.task_scene_pattern_opt
        variants = scene_ptn_opt.get_variants(scene_path, extract=True)
        if variants:
            if 'asset' in variants:
                variants['resource_type'] = 'asset'
            return _task_session.TaskSession(task_parse, variants)

    @classmethod
    def generate_session_for_scene(cls, scene_path):
        task_parse = cls()

        scene_ptn_opt = task_parse.task_scene_pattern_opt
        variants = scene_ptn_opt.get_variants(scene_path, extract=True)
        if variants:
            if 'asset' in variants:
                variants['resource_type'] = 'asset'
            return _task_session.TaskSession(task_parse, variants)

    def __init__(self):
        super(TaskParse, self).__init__()
