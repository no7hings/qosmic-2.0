# coding:utf-8
import lxgui.qt.core as gui_qt_core

import lnx_katana.core as lnx_hou_core

import lnx_wotrix.core as lnx_wtx_core


class TaskSession(lnx_wtx_core.TaskSession):

    def __init__(self, *args, **kwargs):
        super(TaskSession, self).__init__(*args, **kwargs)

    def save_source_task_scene_src(self):
        pass

    def increment_and_save_source_task_scene_src(self, force=False):
        application = 'houdini'

        version = self.get_last_version_code(application=application)

        kwargs_new = dict(self._properties)
        kwargs_new['version'] = str(version+1).zfill(3)

        scene_ptn_opt = self._task_parse.generate_source_task_scene_src_pattern_opt_for(
            application=application,
            **kwargs_new
        )
        scene_path = scene_ptn_opt.get_value()
        if lnx_hou_core.SceneFile.increment_and_save_with_dialog(scene_path, force) is True:
            kwargs_new['result'] = scene_path
            thumbnail_ptn_opt = self._task_parse.generate_source_task_thumbnail_pattern_opt_for(
                application=application,
                **kwargs_new
            )
            thumbnail_path = thumbnail_ptn_opt.get_value()

            gui_qt_core.QtMaya.make_snapshot(thumbnail_path)
            return kwargs_new
        return False

    def save_source_task_scene_scr_to(self, task_unit):
        variants_new = dict(self._properties)
        task_unit_old = variants_new['task_unit']
        variants_new['task_unit'] = task_unit

        task_session = self.__class__(
            self._task_parse, variants_new
        )
        return task_session.increment_and_save_source_task_scene_src(force=task_unit != task_unit_old)
