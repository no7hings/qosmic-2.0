# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import qsm_maya.cfx.core as qsm_mya_cfx_core

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_gui.qt.widgets as qsm_qt_widgets

import qsm_maya.core as qsm_mya_core

import qsm_maya.general.core as qsm_mya_gnl_core

import qsm_maya.animation.core as qsm_mya_anm_core

import qsm_maya.animation.scripts as qsm_mya_anm_scripts

import qsm_maya.motion.core as qsm_mya_mtn_core

import qsm_maya_gui.core as qsm_mya_gui_core


class UnitForRigPicker(
    qsm_mya_gui_core.PrxUnitBaseOpt
):
    def do_gui_refresh_by_dcc_selection(self):
        if self._qt_picker._has_focus_() is False:
            namespaces = qsm_mya_core.Namespaces.extract_roots_from_selection()
            if namespaces:
                results = qsm_mya_anm_core.AdvRig.filter_namespaces(namespaces)
                if results:
                    self._qt_picker._set_namespace_(namespaces[-1])

    @gui_qt_core.qt_slot(list)
    def on_picker_user_select_control_key_accepted(self, control_keys):
        controls = []
        namespace = self._qt_picker._get_namespace_()
        if namespace:
            resource = qsm_mya_anm_core.AdvRig(namespace)
            for i_key in control_keys:
                i_controls = resource.find_all_controls(i_key)
                if i_controls:
                    controls.extend(i_controls)

        qsm_mya_core.Selection.set(controls)

    def get_dcc_namespace(self):
        return self._qt_picker._get_namespace_()

    def __init__(self, window, unit, session, qt_picker):
        super(UnitForRigPicker, self).__init__(window, unit, session)
        if not isinstance(qt_picker, qsm_qt_widgets.QtAdvPicker):
            raise RuntimeError()

        self._qt_picker = qt_picker

        self._qt_picker.user_select_control_key_accepted.connect(self.on_picker_user_select_control_key_accepted)

    def do_gui_refresh_all(self):
        self.do_gui_refresh_by_dcc_selection()


class ToolsetUnitForMotionCopyAndPaste(
    qsm_mya_gui_core.PrxUnitBaseOpt
):
    def do_gui_refresh_by_dcc_selection(self):
        pass

    def get_frame_offset(self):
        return self._prx_options_node.get('setting.frame_offset')

    def do_dcc_copy_all(self):
        namespace = self._page._gui_rig_picker_unit.get_dcc_namespace()
        opt = qsm_mya_mtn_core.AdvMotionOpt(namespace)
        file_path = qsm_mya_gnl_core.ResourceCache.generate_animation_file(bsc_core.BscSystem.get_user_name())
        opt.export_data_to(file_path, part_includes=['body', 'face'])

        self._window.popup_bubble_message(
            '成功拷贝所有' if self._window._language == 'chs' else 'Copy All Successful'
        )

    def do_dcc_paste_all(self):
        namespace = self._page._gui_rig_picker_unit.get_dcc_namespace()
        opt = qsm_mya_mtn_core.AdvMotionOpt(namespace)
        file_path = qsm_mya_gnl_core.ResourceCache.generate_animation_file(bsc_core.BscSystem.get_user_name())
        opt.import_data_from(file_path, force=True, frame_offset=self.get_frame_offset())

        self._window.popup_bubble_message(
            '成功粘贴所有' if self._window._language == 'chs' else 'Paste All Successful'
        )

    def __init__(self, window, unit, session):
        super(ToolsetUnitForMotionCopyAndPaste, self).__init__(window, unit, session)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.units.copy_and_paste.options')
            )
        )

        self._prx_options_node.build_by_data(
            self._window._configure.get('build.main.units.copy_and_paste.options.parameters'),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key='copy_and_paste',
            name=gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.units.copy_and_paste')
            ),
            icon_name_text='copy_and_paste',
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._window._configure.get('build.main.units.copy_and_paste')
            )
        )

        self._prx_options_node.set(
            'copy_keyframe.copy_all', self.do_dcc_copy_all
        )
        self._prx_options_node.set(
            'paste_keyframe.paste_to_all', self.do_dcc_paste_all
        )


class ToolsetUnitForMotionMove(
    qsm_mya_gui_core.PrxUnitBaseOpt
):
    def do_dcc_create_transformation_locator(self):
        main_controls = qsm_mya_core.Selection.get_main_controls()
        if main_controls:
            qsm_mya_anm_scripts.ControlTransformationLocator(main_controls).create_transformation_locators()
        else:
            self._window.exec_message(
                '没有控制器被选中',
                status='warning'
            )

    def do_dcc_remove_transformation_locator(self):
        main_controls = qsm_mya_core.Selection.get_main_controls()
        if main_controls:
            qsm_mya_anm_scripts.ControlTransformationLocator(main_controls).remove_transformation_locators()
        else:
            self._window.exec_message(
                '没有控制器被选中',
                status='warning'
            )

    def __init__(self, window, unit, session):
        super(ToolsetUnitForMotionMove, self).__init__(window, unit, session)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.units.move.options')
            )
        )

        self._prx_options_node.build_by_data(
            self._window._configure.get('build.main.units.move.options.parameters'),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key='move',
            name=gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.units.move')
            ),
            icon_name_text='move',
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._window._configure.get('build.main.units.move')
            )
        )
        
        self._prx_options_node.set(
            'transformation.create_transformation_locator', self.do_dcc_create_transformation_locator
        )

        self._prx_options_node.set(
            'transformation.remove_transformation_locator', self.do_dcc_remove_transformation_locator
        )
