# coding:utf-8
import qsm_lazy_wsp.core as lzy_wsp_core

import qsm_maya.core as qsm_mya_core

from . import task_session as _task_session


class TaskParse(lzy_wsp_core.TaskParse):
    TASK_SESSION_CLS = _task_session.TaskSession

    @classmethod
    def generate_task_session_by_resource_source_scene_src_auto(cls):
        return cls.generate_task_session_by_resource_source_scene_src(
            qsm_mya_core.SceneFile.get_current()
        )

    @classmethod
    def generate_task_session_by_asset_release_scene_src(cls, scene_path):
        task_parse = cls()

        ptn_opt = task_parse.generate_pattern_opt_for(
            'asset-release-maya-scene_src-file'
        )
        variants = ptn_opt.get_variants(scene_path, extract=True)
        if variants:
            variants['resource_branch'] = 'asset'
            return _task_session.TaskSession(task_parse, variants)

    @classmethod
    def generate_task_session_by_shot_release_scene_src(cls, scene_path):
        task_parse = cls()

        ptn_opt = task_parse.generate_pattern_opt_for(
            'shot-release-maya-scene_src-file'
        )
        variants = ptn_opt.get_variants(scene_path, extract=True)
        if variants:
            variants['resource_branch'] = 'shot'
            return _task_session.TaskSession(task_parse, variants)

    def __init__(self):
        super(TaskParse, self).__init__()
