# coding:utf-8
import copy

import lxbasic.storage as bsc_storage

import lxgui.qt.core as gui_qt_core

from qsm_lazy_wsp.gui.abstracts import subpage_for_task_create as _sub_page_for_task_create

import qsm_maya.core as qsm_mya_core

import qsm_maya_lazy_wsp.core as mya_lzy_wps_core

from ..gui_operates import task_create as _task_create_opt


# cfx rig
class PrxSubpageForAssetCfxRigCreate(_sub_page_for_task_create.AbsPrxSubpageForTaskCreate):
    TASK_CREATE_OPT_CLS = _task_create_opt.MayaAssetCfxRigCreateOpt

    GUI_KEY = TASK_CREATE_OPT_CLS.TASK

    def __init__(self, *args, **kwargs):
        super(PrxSubpageForAssetCfxRigCreate, self).__init__(*args, **kwargs)

    def do_gui_refresh_all(self):
        resource_properties = self._sub_window._resource_properties
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
        prx_widget = self._sub_window._prx_widget
        resource_properties = self._sub_window._resource_properties
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
                resource_properties, task_parse, task_unit
            )

            if bsc_storage.StgPath.get_is_file(scene_src_path) is False:
                task_create_opt.build_scene_src(
                    scene_src_path,
                    upstream_scene_path
                )

                qsm_mya_core.SceneFile.refresh()

                with self._sub_window._window.gui_minimized():
                    gui_qt_core.QtMaya.make_snapshot(thumbnail_path)

                prx_widget.gui_load_task_scene(kwargs_new)
