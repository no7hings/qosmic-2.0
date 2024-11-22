# coding:utf-8
import copy

import lxbasic.storage as bsc_storage

import lxgui.qt.core as gui_qt_core

from qsm_lazy_tool.workspace.gui.abstracts import sub_page_for_task_create as _sub_page_for_task_create

import qsm_maya.core as qsm_mya_core

import qsm_maya_wsp_task as qsm_mya_wsp_task


# cfx dressing
class PrxSubPageForShotCfxDressingCreate(_sub_page_for_task_create.AbsPrxSubPageForTaskCreate):
    GUI_KEY = 'cfx_dressing'

    RESOURCE_BRANCH = 'shot'

    STEP = 'cfx'

    TASK = 'cfx_dressing'

    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(PrxSubPageForShotCfxDressingCreate, self).__init__(window, session, sub_window, *args, **kwargs)

        self._prx_options_node.set(
            'play_preview', self.on_play_preview
        )

    def on_play_preview(self):
        preview_path = self._prx_options_node.get('upstream.preview')
        if preview_path:
            if bsc_storage.StgPath.get_is_file(preview_path):
                bsc_storage.StgFileOpt(preview_path).start_in_system()

    def do_gui_refresh_all(self):
        resource_properties = self._sub_window._resource_properties
        if not resource_properties:
            return

        kwargs_new = copy.copy(resource_properties)
        kwargs_new['step'] = 'ani'
        kwargs_new['task'] = 'animation'
        task_parse = qsm_mya_wsp_task.TaskParse()

        # scene
        animation_scene_ptn_opt = task_parse.generate_pattern_opt_for(
            'shot-disorder-animation_scene_s-file', **kwargs_new
        )
        matches = animation_scene_ptn_opt.find_matches()
        if matches:
            rig_scene_path = matches[-1]['result']
            self._prx_options_node.set('upstream.scene', rig_scene_path)

        # preview
        animation_preview_pth_opt = task_parse.generate_pattern_opt_for(
            'shot-disorder-animation_preview_s-file', **kwargs_new
        )
        matches = animation_preview_pth_opt.find_matches()
        if matches:
            preview_path = matches[-1]['result']
            self._prx_options_node.set('upstream.preview', preview_path)

    def _on_apply(self):
        prx_widget = self._sub_window._prx_widget
        resource_properties = self._sub_window._resource_properties
        if not resource_properties:
            return

        if qsm_mya_core.SceneFile.new_with_dialog() is True:
            task_parse = qsm_mya_wsp_task.TaskParse()

            task_unit = self._prx_options_node.get('task_unit')
            if not task_unit:
                return

            upstream_scene_path = self._prx_options_node.get('upstream.scene')
            if upstream_scene_path is None:
                return

            step, task = self.STEP, self.TASK
            kwargs = copy.copy(resource_properties)
            kwargs['step'] = step
            kwargs['task'] = task
            kwargs['task_unit'] = task_unit
            if 'version' in kwargs:
                kwargs.pop('version')

            task_scene_ptn_opt = task_parse.generate_source_task_scene_src_pattern_opt_for(**kwargs)

            matches = task_scene_ptn_opt.find_matches(sort=True)
            if matches:
                last_version = int(matches[-1]['version'])
                version = last_version+1
            else:
                version = 1

            kwargs_new = copy.copy(kwargs)

            kwargs_new['version'] = str(version).zfill(3)

            task_scene_ptn_opt_new = task_parse.generate_source_task_scene_src_pattern_opt_for(
                **kwargs_new
            )

            scene_src_path = task_scene_ptn_opt_new.get_value()

            if bsc_storage.StgPath.get_is_file(scene_src_path) is False:
                task_session = task_parse.generate_task_session_by_resource_source_scene_src(scene_src_path)

                # create source
                task_create_opt = task_session.generate_task_create_opt()
                if task_create_opt is None:
                    return

                task_create_opt.build_scene_src(
                    scene_src_path,
                    upstream_scene_path
                )

                kwargs_new['result'] = scene_src_path

                thumbnail_ptn_opt = task_parse.generate_resource_source_task_scene_src_thumbnail_pattern_opt_for(
                    **kwargs_new
                )
                thumbnail_path = thumbnail_ptn_opt.get_value()

                qsm_mya_core.SceneFile.refresh()

                with self._sub_window._window.gui_minimized():
                    gui_qt_core.QtMaya.make_snapshot(thumbnail_path)

                prx_widget.gui_load_task_scene(kwargs_new)
