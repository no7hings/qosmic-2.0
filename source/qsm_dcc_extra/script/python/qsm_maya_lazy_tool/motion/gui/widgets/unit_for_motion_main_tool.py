# coding:utf-8
import itertools
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import qsm_maya.cfx.core as qsm_mya_cfx_core

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_general.core as qsm_gnl_core

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
                namespace_for_adv = qsm_mya_anm_core.AdvRig.filter_namespaces(namespaces)
                if namespace_for_adv:
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
        return self._prx_options_node.get('setting.frame.frame_offset')
    
    def get_control_key_excludes(self):
        return self._prx_options_node.get('setting.ignore.control_ignore')
    
    # copy
    def do_dcc_copy_character(self):
        namespace = self._page._gui_rig_picker_unit.get_dcc_namespace()
        if not namespace:
            self._window.exec_message(
                '选择一个角色（可以是任意部件）。' if self._window._language == 'chs' else 'Select one character.',
                status='warning'
            )
            return

        opt = qsm_mya_mtn_core.AdvRigMotionOpt(namespace)
        file_path = qsm_mya_gnl_core.ResourceCache.generate_character_motion_file(bsc_core.BscSystem.get_user_name())
        opt.export_to(
            file_path,
            control_set_includes=['body', 'face']
        )

        self._window.popup_bubble_message(
            '成功拷贝角色动画。' if self._window._language == 'chs'
            else 'Copy character animation successful.'
        )
    
    def do_dcc_copy_selected(self):
        args = qsm_mya_mtn_core.ControlsMotionOpt.get_args_from_selection()
        if not args:
            self._window.exec_message(
                '选择一个或多个控制器。' if self._window._language == 'chs' else 'Select one or more control.',
                status='warning'
            )
            return

        namespace, paths = args.keys()[-1], args.values()[-1]

        opt = qsm_mya_mtn_core.ControlsMotionOpt(namespace, paths)

        file_path = qsm_mya_gnl_core.ResourceCache.generate_control_motion_file(bsc_core.BscSystem.get_user_name())
        opt.export_to(
            file_path,
        )
        self._window.popup_bubble_message(
            '成功拷贝选中控制器的动画。' if self._window._language == 'chs'
            else 'Copy animation from selected control successful.'
        )

    # paste
    def do_dcc_paste_character(self):
        namespace_for_adv = []
        namespaces = qsm_mya_core.Namespaces.extract_roots_from_selection()
        if namespaces:
            namespace_for_adv = qsm_mya_anm_core.AdvRig.filter_namespaces(namespaces)

        if not namespace_for_adv:
            self._window.exec_message(
                '选择一个或者多个角色（可以是任意部件）。' if self._window._language == 'chs' else 'Select one character.',
                status='warning'
            )
            return

        control_key_excludes = self.get_control_key_excludes()
        file_path = qsm_mya_gnl_core.ResourceCache.generate_character_motion_file(bsc_core.BscSystem.get_user_name())
        for i_namespace in namespace_for_adv:
            i_opt = qsm_mya_mtn_core.AdvRigMotionOpt(i_namespace)
            i_opt.load_from(
                file_path,
                force=True,
                frame_offset=self.get_frame_offset(),
                control_key_excludes=control_key_excludes
            )

        self._window.popup_bubble_message(
            '成功粘贴动画到选中的角色，可以按“Z”撤销。' if self._window._language == 'chs'
            else 'Paste animation to selected characters successful, press "z" undo.'
        )

    def do_dcc_paste_character_to_selected(self):
        args = qsm_mya_mtn_core.ControlsMotionOpt.get_args_from_selection()
        if not args:
            self._window.exec_message(
                '选择一个或多个控制器。' if self._window._language == 'chs' else 'Select one or more control.',
                status='warning'
            )
            return

        control_key_excludes = self.get_control_key_excludes()
        file_path = qsm_mya_gnl_core.ResourceCache.generate_character_motion_file(bsc_core.BscSystem.get_user_name())
        for k, v in args.items():
            i_opt = qsm_mya_mtn_core.ControlsMotionOpt(k, v)
            i_opt.load_from(
                file_path,
                control_key_excludes=control_key_excludes
            )

        self._window.popup_bubble_message(
            '成功粘贴角色动画到选中，可以按“Z”撤销。' if self._window._language == 'chs'
            else 'Paste character animation to selected successful, press "z" undo.'
        )

    def do_dcc_paste_selected_to_character(self):
        namespace_for_adv = []
        namespaces = qsm_mya_core.Namespaces.extract_roots_from_selection()
        if namespaces:
            namespace_for_adv = qsm_mya_anm_core.AdvRig.filter_namespaces(namespaces)

        if not namespace_for_adv:
            self._window.exec_message(
                '选择一个或者多个角色（可以是任意部件）。' if self._window._language == 'chs' else 'Select one character.',
                status='warning'
            )
            return

        control_key_excludes = self.get_control_key_excludes()
        file_path = qsm_mya_gnl_core.ResourceCache.generate_control_motion_file(bsc_core.BscSystem.get_user_name())
        for i_namespace in namespace_for_adv:
            i_opt = qsm_mya_mtn_core.AdvRigMotionOpt(i_namespace)
            i_opt.load_from(
                file_path,
                force=True,
                frame_offset=self.get_frame_offset(),
                control_key_excludes=control_key_excludes
            )

        self._window.popup_bubble_message(
            '成功粘贴选中的动画到角色，可以按“Z”撤销。' if self._window._language == 'chs'
            else 'Paste selected animation to characters successful, press "z" undo.'
        )

    def do_dcc_paste_to_selected(self):
        args = qsm_mya_mtn_core.ControlsMotionOpt.get_args_from_selection()
        if not args:
            self._window.exec_message(
                '选择一个或多个控制器。' if self._window._language == 'chs' else 'Select one or more control.',
                status='warning'
            )
            return

        control_key_excludes = self.get_control_key_excludes()
        file_path = qsm_mya_gnl_core.ResourceCache.generate_control_motion_file(bsc_core.BscSystem.get_user_name())
        for k, v in args.items():
            i_opt = qsm_mya_mtn_core.ControlsMotionOpt(k, v)
            i_opt.load_from(
                file_path,
                control_key_excludes=control_key_excludes
            )

        self._window.popup_bubble_message(
            '成功粘贴动画到选中，可以按“Z”撤销。' if self._window._language == 'chs'
            else 'Paste animation to selected successful, press "z" undo.'
        )

    # mirror
    def do_dcc_mirror_selected_auto(self):
        pass

    def __init__(self, window, unit, session):
        super(ToolsetUnitForMotionCopyAndPaste, self).__init__(window, unit, session)

        self._adv_control_cfg = qsm_gnl_core.AdvControlConfigure()

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.units.copy_paste_mirror.options')
            )
        )

        self._prx_options_node.build_by_data(
            self._window._configure.get('build.main.units.copy_paste_mirror.options.parameters'),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key='copy_paste_mirror',
            name=gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.units.copy_paste_mirror')
            ),
            icon_name_text='copy_paste_mirror',
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._window._configure.get('build.main.units.copy_paste_mirror')
            )
        )
        # copy
        self._prx_options_node.set(
            'copy_motion.copy_character', self.do_dcc_copy_character
        )
        self._prx_options_node.set(
            'copy_motion.copy_selected', self.do_dcc_copy_selected
        )
        # paste
        self._prx_options_node.set(
            'paste_motion.paste_character', self.do_dcc_paste_character
        )
        self._prx_options_node.set(
            'paste_motion.paste_character_to_selected', self.do_dcc_paste_character_to_selected
        )
        
        self._prx_options_node.set(
            'paste_motion.paste_selected_to_character', self.do_dcc_paste_selected_to_character
        )
        self._prx_options_node.set(
            'paste_motion.paste_selected', self.do_dcc_paste_to_selected
        )


class ToolsetUnitForMotionMove(
    qsm_mya_gui_core.PrxUnitBaseOpt
):
    def do_dcc_create_transformation_locator(self):
        main_controls = qsm_mya_core.Selection.get_main_controls()
        if not main_controls:
            self._window.exec_message(
                '选择一个或多个主控制器（必须有移动和旋转属性，如大环）。' if self._window._language == 'chs'
                else 'Select one or more main control.',
                status='warning'
            )
            return

        qsm_mya_anm_scripts.ControlTransformationLocator(main_controls).create_transformation_locators()

    def do_dcc_remove_transformation_locator(self):
        main_controls = qsm_mya_core.Selection.get_main_controls()
        if not main_controls:
            self._window.exec_message(
                '选择一个或多个主控制器（必须有移动和旋转属性，如大环）。' if self._window._language == 'chs'
                else 'Select one or more main control.',
                status='warning'
            )
            return

        qsm_mya_anm_scripts.ControlTransformationLocator(main_controls).remove_transformation_locators()

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
