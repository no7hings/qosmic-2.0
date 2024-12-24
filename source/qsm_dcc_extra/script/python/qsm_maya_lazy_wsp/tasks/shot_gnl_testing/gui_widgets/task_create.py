# coding:utf-8
import lxbasic.storage as bsc_storage

import lxgui.qt.core as gui_qt_core

from qsm_lazy_wsp.gui.abstracts import subpage_for_task_create as _sub_page_for_task_create

import qsm_maya.core as qsm_mya_core

import qsm_maya_lazy_wsp.core as mya_lzy_wps_core

from ..gui_operates import task_create as _task_create_opt


class PrxSubpageForShotGnlTestingCreate(_sub_page_for_task_create.AbsPrxSubpageForTaskCreate):
    TASK_CREATE_OPT_CLS = _task_create_opt.MayaShotGnlTestingCreateOpt

    GUI_KEY = '{}/{}'.format(TASK_CREATE_OPT_CLS.RESOURCE_TYPE, TASK_CREATE_OPT_CLS.TASK)

    def __init__(self, *args, **kwargs):
        super(PrxSubpageForShotGnlTestingCreate, self).__init__(*args, **kwargs)

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

            (
                task_create_opt, kwargs_new, scene_src_path, thumbnail_path
            ) = self.TASK_CREATE_OPT_CLS.generate_scene_src_args(
                resource_properties, task_parse, task_unit, 'maya'
            )

            if bsc_storage.StgPath.get_is_file(scene_src_path) is False:
                task_create_opt.build_scene_src_fnc(scene_src_path)

                qsm_mya_core.SceneFile.refresh()

                with self._subwindow._window.gui_minimized():
                    gui_qt_core.QtMaya.make_snapshot(thumbnail_path)

                prx_widget.gui_load_task_unit_scene(kwargs_new)
