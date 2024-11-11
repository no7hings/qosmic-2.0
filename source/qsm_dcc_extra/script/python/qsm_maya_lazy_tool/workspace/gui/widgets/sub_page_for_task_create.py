# coding:utf-8
import copy

import lxbasic.storage as bsc_storage

import lxgui.qt.core as gui_qt_core

from qsm_lazy_tool.workspace.gui.abstracts import sub_page_for_task_create as _sub_page_for_task_create

import qsm_maya.core as qsm_mya_core

import qsm_maya.wsp_task as qsm_mya_wsp_task


class PrxSubPageForAssetTaskCreate(_sub_page_for_task_create.AbsPrxSubPageForAssetTaskCreate):
    PAGE_KEY = 'asset'

    RESOURCE_BRANCH = 'asset'

    def __init__(self, *args, **kwargs):
        super(PrxSubPageForAssetTaskCreate, self).__init__(*args, **kwargs)

    def _on_apply(self):
        page = self._sub_window._window.gui_find_page('task_manager')
        if page is not None:
            if qsm_mya_core.SceneFile.new_with_dialog() is True:
                task_parse = qsm_mya_wsp_task.TaskParse()

                step_task = self._prx_options_node.get('step_task')
                task_unit = self._prx_options_node.get('task_unit')
                if not task_unit:
                    return

                step, task = step_task.split('.')
                kwargs = copy.copy(page.gui_get_entity_properties())
                kwargs['step'] = step
                kwargs['task'] = task
                kwargs['task_unit'] = task_unit
                if 'version' in kwargs:
                    kwargs.pop('version')

                task_scene_ptn_opt = task_parse.generate_resource_source_task_scene_src_pattern_opt_for(**kwargs)

                matches = task_scene_ptn_opt.find_matches(sort=True)
                if matches:
                    last_version = int(matches[-1]['version'])
                    version = last_version+1
                else:
                    version = 1

                kwargs_new = copy.copy(kwargs)

                kwargs_new['version'] = str(version).zfill(3)

                task_scene_ptn_opt_new = task_parse.generate_resource_source_task_scene_src_pattern_opt_for(
                    **kwargs_new
                )

                scene_src_path = task_scene_ptn_opt_new.get_value()

                if bsc_storage.StgPath.get_is_file(scene_src_path) is False:
                    task_session = task_parse.generate_task_session_by_resource_source_scene_src(scene_src_path)
                    
                    # create source
                    task_create_opt = task_session.generate_task_create_opt()
                    task_create_opt.build_source()
                    
                    # save source
                    qsm_mya_core.SceneFile.save_to(scene_src_path)

                    kwargs_new['result'] = scene_src_path

                    thumbnail_ptn_opt = task_parse.generate_resource_source_task_scene_src_thumbnail_pattern_opt_for(
                        **kwargs_new
                    )
                    thumbnail_path = thumbnail_ptn_opt.get_value()

                    qsm_mya_core.SceneFile.refresh()

                    with self._sub_window._window.gui_minimized():
                        gui_qt_core.QtMaya.make_snapshot(thumbnail_path)

                    page.gui_load_task_scene(kwargs_new)


class PrxSubPageForShotTaskCreate(_sub_page_for_task_create.AbsPrxSubPageForAssetTaskCreate):
    PAGE_KEY = 'shot'

    RESOURCE_BRANCH = 'shot'

    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(PrxSubPageForShotTaskCreate, self).__init__(window, session, sub_window, *args, **kwargs)

    def _on_apply(self):
        page = self._sub_window._window.gui_find_page('task_manager')
        if page is not None:
            if qsm_mya_core.SceneFile.new_with_dialog() is True:
                task_parse = qsm_mya_wsp_task.TaskParse()

                step_task = self._prx_options_node.get('step_task')
                task_unit = self._prx_options_node.get('task_unit')
                if not task_unit:
                    return

                step, task = step_task.split('.')
                kwargs = copy.copy(page.gui_get_entity_properties())
                kwargs['step'] = step
                kwargs['task'] = task
                kwargs['task_unit'] = task_unit
                if 'version' in kwargs:
                    kwargs.pop('version')

                task_scene_ptn_opt = task_parse.generate_resource_source_task_scene_src_pattern_opt_for(**kwargs)

                matches = task_scene_ptn_opt.find_matches(sort=True)
                if matches:
                    last_version = int(matches[-1]['version'])
                    version = last_version+1
                else:
                    version = 1

                kwargs_new = copy.copy(kwargs)

                kwargs_new['version'] = str(version).zfill(3)

                task_scene_ptn_opt_new = task_parse.generate_resource_source_task_scene_src_pattern_opt_for(
                    **kwargs_new
                )

                scene_src_path = task_scene_ptn_opt_new.get_value()

                if bsc_storage.StgPath.get_is_file(scene_src_path) is False:
                    task_session = task_parse.generate_task_session_by_resource_source_scene_src(scene_src_path)

                    # create source
                    task_create_opt = task_session.generate_task_create_opt()
                    task_create_opt.build_source()

                    # save source
                    qsm_mya_core.SceneFile.save_to(scene_src_path)

                    kwargs_new['result'] = scene_src_path

                    thumbnail_ptn_opt = task_parse.generate_resource_source_task_scene_src_thumbnail_pattern_opt_for(
                        **kwargs_new
                    )
                    thumbnail_path = thumbnail_ptn_opt.get_value()

                    qsm_mya_core.SceneFile.refresh()

                    with self._sub_window._window.gui_minimized():
                        gui_qt_core.QtMaya.make_snapshot(thumbnail_path)

                    page.gui_load_task_scene(kwargs_new)
