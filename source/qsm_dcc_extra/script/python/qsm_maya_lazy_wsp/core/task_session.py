# coding:utf-8
import copy

import lxgui.qt.core as gui_qt_core

import qsm_maya.core as qsm_mya_core

import qsm_lazy_wsp.core as lzy_wsp_core


class TaskSession(lzy_wsp_core.TaskSession):

    def __init__(self, *args, **kwargs):
        super(TaskSession, self).__init__(*args, **kwargs)

    def get_last_version_code(self):
        kwargs = copy.copy(self._properties)
        if 'version' in kwargs:
            kwargs.pop('version')

        pattern_opt = self._task_parse.generate_source_task_scene_src_pattern_opt_for(
            application='maya',
            **kwargs
        )
        matches = pattern_opt.find_matches(sort=True)
        if matches:
            return int(matches[-1]['version'])
        return 0
    
    def save_source_task_scene_src(self):
        pass

    def increment_and_save_source_task_scene_src(self, force=False):
        version = self.get_last_version_code()

        kwargs_new = dict(self._properties)
        kwargs_new['version'] = str(version+1).zfill(3)

        scene_ptn_opt = self._task_parse.generate_source_task_scene_src_pattern_opt_for(
            application='maya',
            **kwargs_new
        )
        scene_path = scene_ptn_opt.get_value()
        if qsm_mya_core.SceneFile.increment_and_save_with_dialog(scene_path, force) is True:
            kwargs_new['result'] = scene_path
            thumbnail_ptn_opt = self._task_parse.generate_source_task_thumbnail_pattern_opt_for(
                application='maya',
                **kwargs_new
            )
            thumbnail_path = thumbnail_ptn_opt.get_value()

            gui_qt_core.QtMaya.make_snapshot(thumbnail_path)
            return kwargs_new

    def save_source_task_scene_scr_to(self, task_unit):
        variants_new = dict(self._properties)
        task_unit_old = variants_new['task_unit']
        variants_new['task_unit'] = task_unit

        task_session = self.__class__(
            self._task_parse, variants_new
        )
        return task_session.increment_and_save_source_task_scene_src(force=task_unit != task_unit_old)
