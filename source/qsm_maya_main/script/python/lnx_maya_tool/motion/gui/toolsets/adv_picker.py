# coding:utf-8
import lxgui.qt.core as gui_qt_core

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_dcc_tool_prc.gui.qt.widgets as lzy_gui_qt_widgets

import qsm_maya.core as qsm_mya_core

import qsm_maya.handles.animation.core as qsm_mya_hdl_anm_core

import qsm_maya.adv as qsm_mya_adv


class UnitForAdvPicker(
    gui_prx_widgets.PrxVirtualBaseUnit
):
    def do_gui_refresh_by_dcc_selection(self):
        if self._qt_picker._has_focus_() is False:
            namespaces = qsm_mya_core.Namespaces.extract_from_selection()
            if namespaces:
                namespace_for_adv = qsm_mya_hdl_anm_core.AdvRigAsset.filter_namespaces(namespaces)
                if namespace_for_adv:
                    self._qt_picker._set_namespace_(namespaces[-1])

            _ = qsm_mya_core.Selection.get()
            if not _:
                self._qt_picker._clear_all_selection_()

    @gui_qt_core.qt_slot(list)
    def on_picker_user_select_control_key_accepted(self, control_keys):
        controls = []
        namespace = self._qt_picker._get_namespace_()
        if namespace:
            resource = qsm_mya_adv.AdvChrOpt(namespace)
            for i_key in control_keys:
                if i_key == 'secondary_cloth':
                    i_controls = resource.find_all_secondary_curve_controls()
                    controls.extend(i_controls)
                else:
                    i_controls = resource.find_many_controls(i_key)
                    if i_controls:
                        controls.extend(i_controls)

            qsm_mya_core.Selection.set(controls)

    def get_dcc_namespace(self):
        return self._qt_picker._get_namespace_()

    def __init__(self, window, page, session, qt_picker):
        super(UnitForAdvPicker, self).__init__(window, page, session)
        if not isinstance(qt_picker, lzy_gui_qt_widgets.QtAdvCharacterPicker):
            raise RuntimeError()

        self._qt_picker = qt_picker

        self._qt_picker.user_select_control_key_accepted.connect(self.on_picker_user_select_control_key_accepted)

    def do_gui_refresh_all(self):
        self.do_gui_refresh_by_dcc_selection()