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

            _ = qsm_mya_core.Selection.get()
            if not _:
                self._qt_picker._clear_all_selection_()

    @gui_qt_core.qt_slot(list)
    def on_picker_user_select_control_key_accepted(self, control_keys):
        controls = []
        namespace = self._qt_picker._get_namespace_()
        if namespace:
            resource = qsm_mya_anm_core.AdvRig(namespace)
            for i_key in control_keys:
                i_controls = resource.find_many_controls(i_key)
                if i_controls:
                    controls.extend(i_controls)

        qsm_mya_core.Selection.set(controls)

    def get_dcc_namespace(self):
        return self._qt_picker._get_namespace_()

    def __init__(self, window, unit, session, qt_picker):
        super(UnitForRigPicker, self).__init__(window, unit, session)
        if not isinstance(qt_picker, qsm_qt_widgets.QtAdvCharacterPicker):
            raise RuntimeError()

        self._qt_picker = qt_picker

        self._qt_picker.user_select_control_key_accepted.connect(self.on_picker_user_select_control_key_accepted)

    def do_gui_refresh_all(self):
        self.do_gui_refresh_by_dcc_selection()


class ToolsetForMotionCopyAndPaste(
    qsm_mya_gui_core.PrxUnitBaseOpt
):
    def do_gui_refresh_by_dcc_selection(self):
        pass

    def get_frame_offset(self):
        return self._prx_options_node.get('setting.frame.frame_offset')
    
    def get_control_key_excludes(self):
        return self._prx_options_node.get('setting.ignore.control_ignore')

    def get_control_set_includes(self):
        return self._prx_options_node.get('setting.includes.control_set_includes')
    
    def get_dcc_character_args(self):
        results = []
        namespaces = qsm_mya_core.Namespaces.extract_roots_from_selection()
        if namespaces:
            results = qsm_mya_anm_core.AdvRig.filter_namespaces(namespaces)

        if not results:
            self._window.exec_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.no_characters')
                ),
                status='warning'
            )
            return
        return results
    
    def get_dcc_control_args(self):
        args = qsm_mya_mtn_core.ControlsMotionOpt.get_args_from_selection()
        if not args:
            self._window.exec_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.no_controls')
                ),
                status='warning'
            )
            return
        return args

    def get_dcc_control_args_for_mirror(self):
        args = qsm_mya_mtn_core.ControlsMotionOpt.get_args_from_selection_for_mirror()
        if not args:
            self._window.exec_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.no_controls_for_mirror')
                ),
                status='warning'
            )
            return
        return args
    
    # copy
    def do_dcc_copy_character(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            namespace = namespaces[-1]
            opt = qsm_mya_mtn_core.AdvCharacterMotionOpt(namespace)
            file_path = qsm_mya_gnl_core.ResourceCache.generate_character_motion_file(bsc_core.BscSystem.get_user_name())
            opt.export_to(
                file_path,
                control_set_includes=['body', 'face']
            )

            self._window.popup_bubble_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.copy_character')
                )
            )
    
    def do_dcc_copy_controls(self):
        args = self.get_dcc_control_args()
        if args:
            namespace, paths = args.keys()[-1], args.values()[-1]
    
            opt = qsm_mya_mtn_core.ControlsMotionOpt(namespace, paths)
    
            file_path = qsm_mya_gnl_core.ResourceCache.generate_control_motion_file(bsc_core.BscSystem.get_user_name())
            opt.export_to(
                file_path,
            )
            self._window.popup_bubble_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.copy_controls')
                )
            )

    def do_dcc_duplicate_characters(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            with self._window.gui_progressing(
                maximum=len(namespaces), label='duplicate characters'
            ) as g_p:
                for i_namespace in namespaces:
                    i_opt = qsm_mya_mtn_core.AdvCharacterMotionOpt(i_namespace)
                    i_opt.duplicate(
                        control_key_excludes=self.get_control_key_excludes(),
                        frame_offset=self.get_frame_offset(),
                    )

                    g_p.do_update()

            self._window.popup_bubble_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.duplicate_characters')
                )
            )

    # paste
    def do_dcc_paste_characters(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            file_path = qsm_mya_gnl_core.ResourceCache.generate_character_motion_file(
                bsc_core.BscSystem.get_user_name()
            )
            with self._window.gui_progressing(
                maximum=len(namespaces), label='paste characters'
            ) as g_p:
                for i_namespace in namespaces:
                    i_opt = qsm_mya_mtn_core.AdvCharacterMotionOpt(i_namespace)
                    i_opt.load_from(
                        file_path,
                        control_key_excludes=self.get_control_key_excludes(),
                        force=True,
                        frame_offset=self.get_frame_offset(),
                    )
                    g_p.do_update()
    
            self._window.popup_bubble_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.paste_characters')
                )
            )

    def do_dcc_paste_controls(self):
        args = self.get_dcc_control_args()
        if args:
            file_path = qsm_mya_gnl_core.ResourceCache.generate_control_motion_file(bsc_core.BscSystem.get_user_name())
            for k, v in args.items():
                i_opt = qsm_mya_mtn_core.ControlsMotionOpt(k, v)
                i_opt.load_from(
                    file_path,
                    control_key_excludes=self.get_control_key_excludes(),
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )

            self._window.popup_bubble_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.paste_controls')
                )
            )

    def do_dcc_paste_character_to_controls(self):
        args = self.get_dcc_control_args()
        if args:
            file_path = qsm_mya_gnl_core.ResourceCache.generate_character_motion_file(bsc_core.BscSystem.get_user_name())
            for k, v in args.items():
                i_opt = qsm_mya_mtn_core.ControlsMotionOpt(k, v)
                i_opt.load_from(
                    file_path,
                    control_key_excludes=self.get_control_key_excludes(),
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )
    
            self._window.popup_bubble_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.paste_controls')
                )
            )

    def do_dcc_paste_controls_to_characters(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            file_path = qsm_mya_gnl_core.ResourceCache.generate_control_motion_file(bsc_core.BscSystem.get_user_name())
            for i_namespace in namespaces:
                i_opt = qsm_mya_mtn_core.AdvCharacterMotionOpt(i_namespace)
                i_opt.load_from(
                    file_path,
                    control_key_excludes=self.get_control_key_excludes(),
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )
    
            self._window.popup_bubble_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.paste_characters')
                )
            )

    # mirror
    def do_dcc_mirror_characters_right_to_left(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            control_set_includes = self.get_control_set_includes()
            for i_namespace in namespaces:
                i_opt = qsm_mya_mtn_core.AdvCharacterMotionOpt(i_namespace)
                i_opt.mirror_right_to_left(
                    control_set_includes=control_set_includes,
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )

            self._window.popup_bubble_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.mirror_any')
                )
            )

    def do_dcc_mirror_characters_middle(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            control_set_includes = self.get_control_set_includes()
            for i_namespace in namespaces:
                i_opt = qsm_mya_mtn_core.AdvCharacterMotionOpt(i_namespace)
                i_opt.mirror_middle(
                    control_set_includes=control_set_includes,
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )

            self._window.popup_bubble_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.mirror_any')
                )
            )

    def do_dcc_mirror_characters_left_to_right(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            control_set_includes = self.get_control_set_includes()
            for i_namespace in namespaces:
                i_opt = qsm_mya_mtn_core.AdvCharacterMotionOpt(i_namespace)
                i_opt.mirror_left_to_right(
                    control_set_includes=control_set_includes,
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )

            self._window.popup_bubble_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.mirror_any')
                )
            )

    def do_dcc_mirror_selected_auto(self):
        args = self.get_dcc_control_args_for_mirror()
        if args:
            for k, v in args.items():
                i_opt = qsm_mya_mtn_core.ControlsMotionOpt(k, v)
                i_opt.mirror_auto(
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )

            self._window.popup_bubble_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.mirror_any')
                )
            )

    # mirror and paste
    def do_dcc_mirror_and_paste_controls(self):
        args = self.get_dcc_control_args_for_mirror()
        if args:
            for k, v in args.items():
                i_opt = qsm_mya_mtn_core.MirrorPasteOpt(k)
                file_path = qsm_mya_gnl_core.ResourceCache.generate_control_motion_file(
                    bsc_core.BscSystem.get_user_name()
                )
                i_opt.load_from(
                    file_path,
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )
            
            self._window.popup_bubble_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.mirror_any')
                )
            )
    
    # flip
    def do_dcc_flip_characters(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            control_set_includes = self.get_control_set_includes()
            for i_namespace in namespaces:
                i_opt = qsm_mya_mtn_core.AdvCharacterMotionOpt(i_namespace)
                i_opt.flip(
                    control_set_includes=control_set_includes,
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )

            self._window.popup_bubble_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.mirror_any')
                )
            )
    
    def do_dcc_flip_controls(self):
        args = self.get_dcc_control_args_for_mirror()
        if args:
            for k, v in args.items():
                i_opt = qsm_mya_mtn_core.ControlsMotionOpt(k, v)
                i_opt.flip(
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )

            self._window.popup_bubble_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.mirror_any')
                )
            )

    def __init__(self, window, unit, session):
        super(ToolsetForMotionCopyAndPaste, self).__init__(window, unit, session)

        self._adv_control_cfg = qsm_gnl_core.AdvCharacterControlConfigure()

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.units.copy_paste_mirror.options')
            )
        )

        self._prx_options_node.build_by_data(
            self._window._configure.get('build.main.units.copy_paste_mirror.options.parameters'),
        )

        prx_sca = gui_prx_widgets.PrxVScrollArea()
        prx_sca.add_widget(self._prx_options_node)

        self._page.gui_get_tool_tab_box().add_widget(
            prx_sca,
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
            'character_motion.copy_character', self.do_dcc_copy_character
        )
        self._prx_options_node.set(
            'control_motion.copy_controls', self.do_dcc_copy_controls
        )
        self._prx_options_node.set(
            'character_motion.duplicate_characters', self.do_dcc_duplicate_characters
        )
        # paste
        self._prx_options_node.set(
            'character_motion.paste_character', self.do_dcc_paste_characters
        )
        self._prx_options_node.set(
            'control_motion.paste_controls', self.do_dcc_paste_controls
        )
        self._prx_options_node.set(
            'character_motion.paste_character_to_controls', self.do_dcc_paste_character_to_controls
        )
        
        self._prx_options_node.set(
            'control_motion.paste_controls_to_characters', self.do_dcc_paste_controls_to_characters
        )
        # mirror
        self._prx_options_node.set(
            'mirror_motion.mirror_characters_right_to_left', self.do_dcc_mirror_characters_right_to_left
        )

        self._prx_options_node.set(
            'mirror_motion.mirror_characters_middle', self.do_dcc_mirror_characters_middle
        )

        self._prx_options_node.set(
            'mirror_motion.mirror_characters_left_to_right', self.do_dcc_mirror_characters_left_to_right
        )

        self._prx_options_node.set(
            'mirror_motion.mirror_selected_auto', self.do_dcc_mirror_selected_auto
        )
        # mirror and paste
        self._prx_options_node.set(
            'mirror_and_paste_motion.mirror_and_paste_controls', self.do_dcc_mirror_and_paste_controls
        )
        # flip
        self._prx_options_node.set(
            'flip_motion.flip_characters', self.do_dcc_flip_characters
        )
        self._prx_options_node.set(
            'flip_motion.flip_controls', self.do_dcc_flip_controls
        )


class ToolsetForMotionOffset(
    qsm_mya_gui_core.PrxUnitBaseOpt
):
    def __init__(self, window, unit, session):
        super(ToolsetForMotionOffset, self).__init__(window, unit, session)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.units.offset.options')
            )
        )

        self._prx_options_node.build_by_data(
            self._window._configure.get('build.main.units.offset.options.parameters'),
        )

        prx_sca = gui_prx_widgets.PrxVScrollArea()
        prx_sca.add_widget(self._prx_options_node)

        self._page.gui_get_tool_tab_box().add_widget(
            prx_sca,
            key='offset',
            name=gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.units.offset')
            ),
            icon_name_text='offset',
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._window._configure.get('build.main.units.offset')
            )
        )


class ToolsetForMove(
    qsm_mya_gui_core.PrxUnitBaseOpt
):

    @staticmethod
    def do_dcc_create_transformation_locator():
        import lxbasic.session as bsc_session
        bsc_session.OptionHook.execute(
            "option_hook_key=dcc-script/maya/qsm-control-move-create-script"
        )

    @staticmethod
    def do_dcc_remove_transformation_locator():
        import lxbasic.session as bsc_session
        bsc_session.OptionHook.execute(
            "option_hook_key=dcc-script/maya/qsm-control-move-remove-script"
        )

    def __init__(self, window, unit, session):
        super(ToolsetForMove, self).__init__(window, unit, session)

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
            'transformation.create_control_move_locator', self.do_dcc_create_transformation_locator
        )

        self._prx_options_node.set(
            'transformation.remove_control_move_locator', self.do_dcc_remove_transformation_locator
        )
