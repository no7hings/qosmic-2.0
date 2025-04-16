# coding:utf-8
import copy

import lxbasic.storage as bsc_storage

import lxgui.qt.core as gui_qt_core

from lnx_wotrix.gui.abstracts import subpage_for_task_create as _sub_page_for_task_create

import qsm_maya.core as qsm_mya_core

import lnx_maya_wotrix.core as mya_lzy_wps_core

from ..gui_operates import task_create as _task_create_opt


# cfx rig
class GuiTaskCreateMain(_sub_page_for_task_create.AbsPrxSubpageForTaskCreate):
    TASK_CREATE_OPT_CLS = _task_create_opt.MayaAssetCfxRigCreateOpt

    GUI_KEY = '{}/{}'.format(TASK_CREATE_OPT_CLS.RESOURCE_TYPE, TASK_CREATE_OPT_CLS.TASK)

    def __init__(self, *args, **kwargs):
        super(GuiTaskCreateMain, self).__init__(*args, **kwargs)

    def do_gui_refresh_all(self):
        resource_properties = self._subwindow._resource_properties
        if not resource_properties:
            return

        kwargs_new = copy.copy(resource_properties)
        kwargs_new['step'] = 'rig'
        kwargs_new['task'] = 'rigging'
        task_parse = mya_lzy_wps_core.TaskParse()
        rig_scene_ptn_opt = task_parse.generate_pattern_opt_for(
            'asset-disorder-rig_scene-maya-file', **kwargs_new
        )
        matches = rig_scene_ptn_opt.find_matches()
        if matches:
            rig_scene_path = matches[-1]['result']
            self._prx_options_node.set('upstream.scene', rig_scene_path)
            modify_time = bsc_storage.StgFileOpt(rig_scene_path).get_modify_time()
            self._prx_options_node.set('upstream.scene_modify_time', modify_time)

    def _on_apply(self):
        prx_widget = self._subwindow._prx_widget
        resource_properties = self._subwindow._resource_properties
        if not resource_properties:
            return

        if qsm_mya_core.SceneFile.new_with_dialog() is True:
            task_parse = mya_lzy_wps_core.TaskParse()

            task_unit = self._prx_options_node.get('task_unit')
            if not task_unit:
                return

            upstream_scene_path = self._prx_options_node.get('upstream.scene')
            if upstream_scene_path is None:
                return

            (
                task_create_opt, kwargs_new, scene_src_path, thumbnail_path
            ) = self.TASK_CREATE_OPT_CLS.generate_scene_src_args(
                resource_properties, task_parse, task_unit, 'maya'
            )

            if bsc_storage.StgPath.get_is_file(scene_src_path) is False:
                task_create_opt.build_scene_src_fnc(
                    scene_src_path,
                    upstream_scene_path
                )

                qsm_mya_core.SceneFile.refresh()

                with self._subwindow._window.gui_minimized():
                    gui_qt_core.QtMaya.make_snapshot(thumbnail_path)

                prx_widget.gui_load_task_unit_scene(kwargs_new)
