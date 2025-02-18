# coding:utf-8
import lxgui.core as gui_core

import lnx_wotrix.core as lnx_wtx_core

import lnx_houdini.core as lnx_hou_core

from . import task_session as _task_session


class TaskParse(lnx_wtx_core.TaskParse):
    TASK_SESSION_CLS = _task_session.TaskSession

    @classmethod
    def generate_task_session_by_resource_source_scene_src_auto(cls):
        return cls.generate_task_session_by_resource_source_scene_src(
            lnx_hou_core.SceneFile.get_current()
        )

    @classmethod
    def generate_task_session_by_asset_release_scene_src(cls, scene_path):
        task_parse = cls()

        ptn_opt = task_parse.generate_pattern_opt_for(
            'asset-release-maya-scene_src-file'
        )
        variants = ptn_opt.get_variants(scene_path, extract=True)
        if variants:
            variants['resource_type'] = 'asset'
            return _task_session.TaskSession(task_parse, variants)

    @classmethod
    def generate_task_session_by_shot_release_scene_src(cls, scene_path):
        task_parse = cls()

        ptn_opt = task_parse.generate_pattern_opt_for(
            'shot-release-maya-scene_src-file'
        )
        variants = ptn_opt.get_variants(scene_path, extract=True)
        if variants:
            variants['resource_type'] = 'shot'
            return _task_session.TaskSession(task_parse, variants)

    @classmethod
    def autosave_source_scene_scr(cls):
        task_session = cls.generate_task_session_by_resource_source_scene_src_auto()
        if task_session is not None:
            variants = task_session.increment_and_save_source_task_scene_src()
            # variants is dict
            if variants:
                gui_core.GuiApplication.exec_message_dialog(
                    'Save scene successful: {}.'.format(variants['result']),
                    title='Save Scene',
                    size=(320, 120),
                    status='correct',
                )
        else:
            gui_core.GuiApplication.exec_message_dialog(
                'Save scene field, not a valid task scene: {}.'.format(lnx_hou_core.SceneFile.get_current()),
                title='Save Scene',
                size=(320, 120),
                status='warning',
            )
        return False

    def __init__(self):
        super(TaskParse, self).__init__()
