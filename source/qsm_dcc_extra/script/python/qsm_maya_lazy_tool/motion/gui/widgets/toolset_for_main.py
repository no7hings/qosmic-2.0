# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_general.core as qsm_gnl_core

import qsm_gui.qt.widgets as qsm_qt_widgets

import qsm_maya.core as qsm_mya_core

import qsm_maya.animation.core as qsm_mya_anm_core

import qsm_maya.motion.core as qsm_mya_mtn_core

import qsm_maya_gui.core as qsm_mya_gui_core


class UnitForRigPicker(
    gui_prx_widgets.PrxVirtualUnit
):
    def do_gui_refresh_by_dcc_selection(self):
        if self._qt_picker._has_focus_() is False:
            namespaces = qsm_mya_core.Namespaces.extract_from_selection()
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

    def __init__(self, window, page, session, qt_picker):
        super(UnitForRigPicker, self).__init__(window, page, session)
        if not isinstance(qt_picker, qsm_qt_widgets.QtAdvCharacterPicker):
            raise RuntimeError()

        self._qt_picker = qt_picker

        self._qt_picker.user_select_control_key_accepted.connect(self.on_picker_user_select_control_key_accepted)

    def do_gui_refresh_all(self):
        self.do_gui_refresh_by_dcc_selection()


class ToolsetForMotionCopyAndPaste(
    gui_prx_widgets.PrxVirtualUnit
):
    UNIT_KEY = 'copy_paste_mirror'

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
        namespaces = qsm_mya_core.Namespaces.extract_from_selection()
        if namespaces:
            results = qsm_mya_anm_core.AdvRig.filter_namespaces(namespaces)

        if not results:
            self._window.exec_message_dialog(
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
            self._window.exec_message_dialog(
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
            self._window.exec_message_dialog(
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
            file_path = qsm_gnl_core.MayaCache.generate_character_motion_file(bsc_core.BscSystem.get_user_name())
            opt.export_to(
                file_path,
                control_set_includes=['body', 'face']
            )

            self._window.popup_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.copy_character')
                )
            )
    
    def do_dcc_copy_controls(self):
        args = self.get_dcc_control_args()
        if args:
            namespace, paths = args.keys()[-1], args.values()[-1]
    
            opt = qsm_mya_mtn_core.ControlsMotionOpt(namespace, paths)
    
            file_path = qsm_gnl_core.MayaCache.generate_control_motion_file(bsc_core.BscSystem.get_user_name())
            opt.export_to(
                file_path,
            )
            self._window.popup_message(
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

            self._window.popup_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.duplicate_characters')
                )
            )

    # paste
    def do_dcc_paste_characters(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            file_path = qsm_gnl_core.MayaCache.generate_character_motion_file(
                bsc_core.BscSystem.get_user_name()
            )
            if file_path:
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

                self._window.popup_message(
                    self._window.choice_message(
                        self._window._configure.get('build.main.messages.paste_characters')
                    )
                )

    def do_dcc_paste_controls(self):
        args = self.get_dcc_control_args()
        if args:
            file_path = qsm_gnl_core.MayaCache.generate_control_motion_file(bsc_core.BscSystem.get_user_name())
            for k, v in args.items():
                i_opt = qsm_mya_mtn_core.ControlsMotionOpt(k, v)
                i_opt.load_from(
                    file_path,
                    control_key_excludes=self.get_control_key_excludes(),
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )

            self._window.popup_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.paste_controls')
                )
            )

    def do_dcc_paste_character_to_controls(self):
        args = self.get_dcc_control_args()
        if args:
            file_path = qsm_gnl_core.MayaCache.generate_character_motion_file(bsc_core.BscSystem.get_user_name())
            for k, v in args.items():
                i_opt = qsm_mya_mtn_core.ControlsMotionOpt(k, v)
                i_opt.load_from(
                    file_path,
                    control_key_excludes=self.get_control_key_excludes(),
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )
    
            self._window.popup_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.paste_controls')
                )
            )

    def do_dcc_paste_controls_to_characters(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            file_path = qsm_gnl_core.MayaCache.generate_control_motion_file(bsc_core.BscSystem.get_user_name())
            for i_namespace in namespaces:
                i_opt = qsm_mya_mtn_core.AdvCharacterMotionOpt(i_namespace)
                i_opt.load_from(
                    file_path,
                    control_key_excludes=self.get_control_key_excludes(),
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )
    
            self._window.popup_message(
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

            self._window.popup_message(
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

            self._window.popup_message(
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

            self._window.popup_message(
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

            self._window.popup_message(
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
                file_path = qsm_gnl_core.MayaCache.generate_control_motion_file(
                    bsc_core.BscSystem.get_user_name()
                )
                i_opt.load_from(
                    file_path,
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )
            
            self._window.popup_message(
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

            self._window.popup_message(
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

            self._window.popup_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.mirror_any')
                )
            )

    def __init__(self, window, page, session):
        super(ToolsetForMotionCopyAndPaste, self).__init__(window, page, session)

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


class ToolsetForMotionKeyframe(
    gui_prx_widgets.PrxVirtualUnit
):
    TOOLSET_KEY = 'keyframe'

    def _do_dcc_select_all_curves(self):
        curves = qsm_mya_core.AnimCurves.get_all(reference=False, excludes=['timewarp', 'qsm_timewarp'])
        qsm_mya_core.Selection.set(curves)

        self._window.popup_message(
            self._window.choice_message(
                self._window._configure.get('build.main.messages.select_all_curves')
            )
        )

    def _do_dcc_select_character_all_curves(self):
        results = []
        namespaces = qsm_mya_core.Namespaces.extract_from_selection()
        if namespaces:
            results = qsm_mya_anm_core.AdvRig.filter_namespaces(namespaces)

        if not results:
            self._window.exec_message_dialog(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.no_characters')
                ),
                status='warning'
            )
            return

        if results:
            curves = []
            for i_namespace in results:
                i_opt = qsm_mya_mtn_core.AdvCharacterMotionOpt(i_namespace)
                curves.extend(i_opt.find_all_anm_curves())

            qsm_mya_core.Selection.set(curves)

            self._window.popup_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.select_all_character_curves')
                )
            )

    def _do_gui_refresh_timewrap_frame_range(self):
        frame_range_src, frame_range_tgt = qsm_mya_mtn_core.TimewarpOpt.get_frame_range_args()
        self._prx_options_node.set(
            'curve_timewarp.frame_range_src', frame_range_src
        )
        self._prx_options_node.set(
            'curve_timewarp.frame_range_tgt', frame_range_tgt
        )

    def _do_dcc_refresh_timewrap_buttons(self):
        buttons = [
            self._prx_options_node.get_port('curve_timewarp.create_or_update_timewarp_preview'),
            self._prx_options_node.get_port('curve_timewarp.remove_timewarp_preview'),
            self._prx_options_node.get_port('curve_timewarp.apply_timewarp'),
        ]
        if qsm_mya_mtn_core.TimewarpOpt.check_is_valid() is True:
            for i_b in buttons:
                i_b.set_status(i_b.ValidationStatus.Enable)
            self._prx_options_node.get_port('curve_timewarp.frame_range_tgt').set_action_enable(True)
        else:
            for i_b in buttons:
                i_b.set_status(i_b.ValidationStatus.Disable)
            self._prx_options_node.get_port('curve_timewarp.frame_range_tgt').set_action_enable(False)

    def _do_dcc_create_or_update_timewrap_preview(self):
        frame_range_src = self._prx_options_node.get('curve_timewarp.frame_range_src')
        if self._prx_options_node.get('curve_timewarp.warp_scheme') == 'frame_range':
            frame_range_tgt = self._prx_options_node.get('curve_timewarp.frame_range_tgt')
            result = qsm_mya_mtn_core.TimewarpOpt.update_by_frame_range(
                frame_range_src, frame_range_tgt
            )
        elif self._prx_options_node.get('curve_timewarp.warp_scheme') == 'scale_value':
            scale_value = self._prx_options_node.get('curve_timewarp.scale_value')
            result = qsm_mya_mtn_core.TimewarpOpt.update_by_scale_value(
                frame_range_src, scale_value
            )
        else:
            raise RuntimeError()

        if result is True:
            self._window.popup_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.update_timewarp_preview')
                )
            )

        self._do_dcc_refresh_timewrap_buttons()
        
    def _do_dcc_remove_timewrap_preview(self):
        result =qsm_mya_mtn_core.TimewarpOpt.remove()
        if result is True:
            self._window.popup_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.remove_timewarp_preview')
                )
            )
        else:
            self._window.exec_message_dialog(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.no_timewarp_preview')
                ),
                status='warning'
            )
        
        self._do_dcc_refresh_timewrap_buttons()
    
    def _do_dcc_apply_timewrap(self):
        result = qsm_mya_mtn_core.TimewarpOpt.apply()
        if result is True:
            self._window.popup_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.apply_timewarp')
                )
            )
        
        self._do_dcc_refresh_timewrap_buttons()
    
    def __init__(self, window, page, session):
        super(ToolsetForMotionKeyframe, self).__init__(window, page, session)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language,
                self._window._configure.get('build.main.units.{}.options'.format(self.TOOLSET_KEY))
            )
        )

        self._prx_options_node.build_by_data(
            self._window._configure.get('build.main.units.{}.options.parameters'.format(self.TOOLSET_KEY)),
        )

        prx_sca = gui_prx_widgets.PrxVScrollArea()
        prx_sca.add_widget(self._prx_options_node)

        self._page.gui_get_tool_tab_box().add_widget(
            prx_sca,
            key=self.TOOLSET_KEY,
            name=gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.units.{}'.format(self.TOOLSET_KEY))
            ),
            icon_name_text=self.TOOLSET_KEY,
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._window._configure.get('build.main.units.{}'.format(self.TOOLSET_KEY))
            )
        )

        self._prx_options_node.set(
            'selection.select_all_curves', self._do_dcc_select_all_curves
        )
        self._prx_options_node.set(
            'selection.select_character_all_curves', self._do_dcc_select_character_all_curves
        )

        self._prx_options_node.set(
            'curve_timewarp.create_or_update_timewarp_preview', self._do_dcc_create_or_update_timewrap_preview
        )
        self._prx_options_node.set(
            'curve_timewarp.remove_timewarp_preview', self._do_dcc_remove_timewrap_preview
        )
        self._prx_options_node.set(
            'curve_timewarp.apply_timewarp', self._do_dcc_apply_timewrap
        )

    def do_gui_refresh_all(self):
        self._do_gui_refresh_timewrap_frame_range()
        self._do_dcc_refresh_timewrap_buttons()


class ToolsetForMove(
    gui_prx_widgets.PrxVirtualUnit
):
    UNIT_KEY = 'move'

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

    def __init__(self, window, page, session):
        super(ToolsetForMove, self).__init__(window, page, session)

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


class ToolsetForConstrainAndDeform(
    gui_prx_widgets.PrxVirtualUnit
):
    UNIT_KEY = 'constrain_and_deform'

    def do_dcc_replace_motion_path_object(self):
        paths = cmds.ls(selection=1, type='transform', long=1) or []
        if len(paths) < 2:
            self._window.exec_message_dialog(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.less_transforms')
                ),
                status='warning'
            )
            return

        qsm_mya_core.MotionPath.replace_all(paths)

    def do_dcc_curve_warp_path_object(self):
        paths = cmds.ls(selection=1, type='transform', long=1) or []
        if len(paths) < 2:
            self._window.exec_message_dialog(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.less_transforms')
                ),
                status='warning'
            )
            return

        qsm_mya_core.CurveWarp.replace_all(paths)

    def __init__(self, window, page, session):
        super(ToolsetForConstrainAndDeform, self).__init__(window, page, session)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.units.{}.options'.format(self.UNIT_KEY))
            )
        )

        self._prx_options_node.build_by_data(
            self._window._configure.get('build.main.units.{}.options.parameters'.format(self.UNIT_KEY)),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key=self.UNIT_KEY,
            name=gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.units.{}'.format(self.UNIT_KEY))
            ),
            icon_name_text=self.UNIT_KEY,
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._window._configure.get('build.main.units.{}'.format(self.UNIT_KEY))
            )
        )

        self._prx_options_node.set(
            'motion_path.replace_object', self.do_dcc_replace_motion_path_object
        )

        self._prx_options_node.set(
            'curve_warp.replace_object', self.do_dcc_curve_warp_path_object
        )
