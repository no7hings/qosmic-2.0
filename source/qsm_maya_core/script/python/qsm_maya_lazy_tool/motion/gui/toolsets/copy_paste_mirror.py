# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_general.core as qsm_gnl_core

import qsm_maya.core as qsm_mya_core

import qsm_maya.handles.animation.core as qsm_mya_hdl_anm_core

import qsm_maya.motion as qsm_mya_motion

import qsm_maya.adv as qsm_mya_adv


class ToolsetForMotionCopyAndPasteAndMirror(
    gui_prx_widgets.PrxVirtualBaseUnit
):
    GUI_KEY = 'copy_and_paste_and_mirror'

    def do_gui_refresh_by_dcc_selection(self):
        pass

    def get_frame_offset(self):
        return self._prx_options_node.get('setting.frame.frame_offset')

    def get_control_key_excludes(self):
        return self._prx_options_node.get('setting.ignore.control_ignore')

    def get_dcc_character_args(self):
        results = []
        namespaces = qsm_mya_core.Namespaces.extract_from_selection()
        if namespaces:
            results = qsm_mya_hdl_anm_core.AdvRigAsset.filter_namespaces(namespaces)

        if not results:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.no_characters')
                ),
                status='warning'
            )
            return
        return results

    def get_dcc_control_args(self):
        args = qsm_mya_motion.ControlSetMotionOpt.get_args_from_selection()
        if not args:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.no_controls')
                ),
                status='warning'
            )
            return
        return args

    def get_dcc_control_args_for_mirror(self):
        args = qsm_mya_motion.ControlSetMotionOpt.get_args_from_selection_for_mirror()
        if not args:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.no_controls_for_mirror')
                ),
                status='warning'
            )
            return
        return args

    # duplicate
    def do_dcc_duplicate_characters(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            with self._window.gui_progressing(
                maximum=len(namespaces), label='duplicate characters'
            ) as g_p:
                for i_namespace in namespaces:
                    i_opt = qsm_mya_adv.AdvChrOpt(i_namespace)
                    i_opt.duplicate(
                        control_key_excludes=self.get_control_key_excludes(),
                        frame_offset=self.get_frame_offset(),
                    )

                    g_p.do_update()

            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.duplicate_characters')
                )
            )

    # copy
    def on_dcc_copy_character(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            namespace = namespaces[-1]
            opt = qsm_mya_adv.AdvChrOpt(namespace)

            opt.export_controls_motion_to(
                qsm_gnl_core.DccCache.generate_character_motion_file(bsc_core.BscSystem.get_user_name())
            )
            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.copy_character')
                )
            )

    def on_dcc_copy_character_pose(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            namespace = namespaces[-1]
            opt = qsm_mya_adv.AdvChrOpt(namespace)

            opt.export_controls_pose_to(
                qsm_gnl_core.DccCache.generate_character_pose_file(bsc_core.BscSystem.get_user_name())
            )
            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.copy_character_pose')
                )
            )

    def on_dcc_copy_controls(self):
        args = self.get_dcc_control_args()
        if args:
            namespace, paths = list(args.keys())[-1], list(args.values())[-1]

            opt = qsm_mya_motion.ControlSetMotionOpt(namespace, paths)

            opt.export_motion_to(
                qsm_gnl_core.DccCache.generate_control_motion_file(bsc_core.BscSystem.get_user_name())
            )
            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.copy_controls')
                )
            )

    def on_dcc_copy_controls_pose(self):
        args = self.get_dcc_control_args()
        if args:
            namespace, paths = list(args.keys())[-1], list(args.values())[-1]

            opt = qsm_mya_motion.ControlSetMotionOpt(namespace, paths)

            opt.export_pose_to(
                qsm_gnl_core.DccCache.generate_control_pose_file(bsc_core.BscSystem.get_user_name())
            )
            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.copy_controls_pose')
                )
            )

    # paste
    def do_dcc_paste_characters(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            file_path = qsm_gnl_core.DccCache.generate_character_motion_file(
                bsc_core.BscSystem.get_user_name()
            )
            if file_path:
                with self._window.gui_progressing(
                    maximum=len(namespaces), label='paste characters'
                ) as g_p:
                    for i_namespace in namespaces:
                        i_opt = qsm_mya_adv.AdvChrOpt(i_namespace)
                        i_opt.load_controls_motion_from(
                            file_path,
                            control_key_excludes=self.get_control_key_excludes(),
                            force=True,
                            frame_offset=self.get_frame_offset(),
                        )
                        g_p.do_update()

                self._window.popup_message(
                    self._window.choice_gui_message(
                        self._page._configure.get('build.messages.paste_characters')
                    )
                )

    def on_dcc_paste_character_pose(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            file_path = qsm_gnl_core.DccCache.generate_character_pose_file(
                bsc_core.BscSystem.get_user_name()
            )
            if file_path:
                with self._window.gui_progressing(
                    maximum=len(namespaces), label='paste characters'
                ) as g_p:
                    for i_namespace in namespaces:
                        i_opt = qsm_mya_adv.AdvChrOpt(i_namespace)
                        i_opt.load_controls_pose_from(
                            file_path,
                            control_key_excludes=self.get_control_key_excludes(),
                            auto_keyframe=True
                        )
                        g_p.do_update()

                self._window.popup_message(
                    self._window.choice_gui_message(
                        self._page._configure.get('build.messages.paste_characters_pose')
                    )
                )

    def on_dcc_paste_controls(self):
        args = self.get_dcc_control_args()
        if args:
            file_path = qsm_gnl_core.DccCache.generate_control_motion_file(bsc_core.BscSystem.get_user_name())
            for k, v in args.items():
                i_opt = qsm_mya_motion.ControlSetMotionOpt(k, v)
                i_opt.load_motion_from(
                    file_path,
                    control_key_excludes=self.get_control_key_excludes(),
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )

            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.paste_controls')
                )
            )

    def on_dcc_paste_controls_pose(self):
        args = self.get_dcc_control_args()
        if args:
            file_path = qsm_gnl_core.DccCache.generate_control_pose_file(bsc_core.BscSystem.get_user_name())
            for k, v in args.items():
                i_opt = qsm_mya_motion.ControlSetMotionOpt(k, v)
                i_opt.load_pose_from(
                    file_path,
                    control_key_excludes=self.get_control_key_excludes(),
                    auto_keyframe=True,
                )

            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.paste_controls_pose')
                )
            )

    def do_dcc_paste_character_to_controls(self):
        args = self.get_dcc_control_args()
        if args:
            file_path = qsm_gnl_core.DccCache.generate_character_motion_file(bsc_core.BscSystem.get_user_name())
            for k, v in args.items():
                i_opt = qsm_mya_motion.ControlSetMotionOpt(k, v)
                i_opt.load_motion_from(
                    file_path,
                    control_key_excludes=self.get_control_key_excludes(),
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )

            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.paste_controls')
                )
            )

    def do_dcc_paste_controls_to_characters(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            file_path = qsm_gnl_core.DccCache.generate_control_motion_file(bsc_core.BscSystem.get_user_name())
            for i_namespace in namespaces:
                i_opt = qsm_mya_adv.AdvChrOpt(i_namespace)
                i_opt.load_controls_motion_from(
                    file_path,
                    control_key_excludes=self.get_control_key_excludes(),
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )

            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.paste_characters')
                )
            )

    # mirror
    # mirror character
    def do_dcc_mirror_characters_right_to_left(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            for i_namespace in namespaces:
                i_opt = qsm_mya_adv.AdvChrOpt(i_namespace)
                i_opt.mirror_controls_right_to_left(
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )

            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.mirror_any')
                )
            )

    def do_dcc_mirror_characters_middle(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            for i_namespace in namespaces:
                i_opt = qsm_mya_adv.AdvChrOpt(i_namespace)
                i_opt.mirror_controls_middle(
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )

            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.mirror_any')
                )
            )

    def do_dcc_mirror_characters_left_to_right(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            for i_namespace in namespaces:
                i_opt = qsm_mya_adv.AdvChrOpt(i_namespace)
                i_opt.mirror_controls_left_to_right(
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )

            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.mirror_any')
                )
            )

    # mirror control
    def on_dcc_mirror_selected_auto(self):
        args = self.get_dcc_control_args_for_mirror()
        if args:
            for k, v in args.items():
                # generate axis vector dict
                i_adv_motion_opt = qsm_mya_adv.AdvOpt(k)
                i_controls = i_adv_motion_opt.find_all_controls()
                ir_axis_vector_dict = qsm_mya_motion.ControlSetMotionOpt(k, i_controls).generate_axis_vector_dict()

                i_opt = qsm_mya_motion.ControlSetMotionOpt(k, v)
                i_opt.mirror_all_auto(
                    force=True,
                    frame_offset=self.get_frame_offset(),
                    axis_vector_dict=ir_axis_vector_dict
                )

            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.mirror_any')
                )
            )

    # mirror and paste
    def on_dcc_mirror_and_paste_controls(self):
        args = self.get_dcc_control_args_for_mirror()
        if args:
            for k, v in args.items():
                i_opt = qsm_mya_motion.ControlMirrorPasteOpt(k)
                file_path = qsm_gnl_core.DccCache.generate_control_motion_file(
                    bsc_core.BscSystem.get_user_name()
                )
                i_opt.load_motion_from(
                    file_path,
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )

            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.mirror_any')
                )
            )

    # flip
    def on_dcc_flip_characters(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            for i_namespace in namespaces:
                i_opt = qsm_mya_adv.AdvChrOpt(i_namespace)
                i_opt.flip_controls(
                    control_key_excludes=self.get_control_key_excludes(),
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )

            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.mirror_any')
                )
            )

    def on_dcc_flip_controls(self):
        args = self.get_dcc_control_args_for_mirror()
        if args:
            for k, v in args.items():
                i_opt = qsm_mya_motion.ControlSetMotionOpt(k, v)
                i_opt.flip_all(
                    force=True,
                    frame_offset=self.get_frame_offset(),
                )

            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.mirror_any')
                )
            )

    # reset
    def on_dcc_reset_characters(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            auto_keyframe = self._prx_options_node.get('reset_motion.auto_keyframe')

            for i_namespace in namespaces:
                i_opt = qsm_mya_adv.AdvChrOpt(i_namespace)
                i_opt.rest_controls_transformation(
                    reset_scheme='transform',
                    translate=True,
                    rotate=True,
                    auto_keyframe=auto_keyframe
                )

    def on_dcc_reset_controls(self):
        args = self.get_dcc_control_args()
        if args:
            auto_keyframe = self._prx_options_node.get('reset_motion.auto_keyframe')

            for k, v in args.items():
                i_opt = qsm_mya_motion.ControlSetMotionOpt(k, v)
                i_opt.reset_transformation(
                    translate=True,
                    rotate=True,
                    auto_keyframe=auto_keyframe
                )

    def __init__(self, window, page, session):
        super(ToolsetForMotionCopyAndPasteAndMirror, self).__init__(window, page, session)

        self._adv_control_cfg = qsm_gnl_core.AdvCharacterControlConfigure()

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_gui_name(
                self._window._language, self._page._configure.get('build.units.{}.options'.format(self.GUI_KEY))
            )
        )

        self._prx_options_node.build_by_data(
            self._page._configure.get('build.units.{}.options.parameters'.format(self.GUI_KEY)),
        )

        prx_sca = gui_prx_widgets.PrxVScrollArea()
        prx_sca.add_widget(self._prx_options_node)

        self._page.gui_get_tool_tab_box().add_widget(
            prx_sca,
            key=self.GUI_KEY,
            name=gui_core.GuiUtil.choice_gui_name(
                self._window._language, self._page._configure.get('build.units.{}'.format(self.GUI_KEY))
            ),
            icon_name_text=self.GUI_KEY,
            tool_tip=gui_core.GuiUtil.choice_gui_tool_tip(
                self._window._language, self._page._configure.get('build.units.{}'.format(self.GUI_KEY))
            )
        )
        # duplicate
        self._prx_options_node.set(
            'character_motion.duplicate_characters', self.do_dcc_duplicate_characters
        )
        # copy
        self._prx_options_node.set(
            'character_motion.copy_character', self.on_dcc_copy_character
        )
        if self._window._language == 'chs':
            self._prx_options_node.get_port('character_motion.copy_character').set_menu_data(
                [
                    ('当前帧（Pose）', 'tool/copy', self.on_dcc_copy_character_pose)
                ]
            )
        else:
            self._prx_options_node.get_port('character_motion.copy_character').set_menu_data(
                [
                    ('current frame (pose)', 'tool/copy', self.on_dcc_copy_character_pose)
                ]
            )
        self._prx_options_node.set(
            'control_motion.copy_controls', self.on_dcc_copy_controls
        )
        if self._window._language == 'chs':
            self._prx_options_node.get_port('control_motion.copy_controls').set_menu_data(
                [
                    ('当前帧（Pose）', 'tool/copy', self.on_dcc_copy_controls_pose)
                ]
            )
        else:
            self._prx_options_node.get_port('control_motion.copy_controls').set_menu_data(
                [
                    ('current frame (pose)', 'tool/copy', self.on_dcc_copy_controls_pose)
                ]
            )

        # paste
        self._prx_options_node.set(
            'character_motion.paste_character', self.do_dcc_paste_characters
        )
        if self._window._language == 'chs':
            self._prx_options_node.get_port('character_motion.paste_character').set_menu_data(
                [
                    ('当前帧（Pose）', 'tool/paste', self.on_dcc_paste_character_pose)
                ]
            )
        else:
            self._prx_options_node.get_port('character_motion.paste_character').set_menu_data(
                [
                    ('current frame (pose)', 'tool/paste', self.on_dcc_paste_character_pose)
                ]
            )

        self._prx_options_node.set(
            'control_motion.paste_controls', self.on_dcc_paste_controls
        )
        if self._window._language == 'chs':
            self._prx_options_node.get_port('control_motion.paste_controls').set_menu_data(
                [
                    ('当前帧（Pose）', 'tool/paste', self.on_dcc_paste_controls_pose)
                ]
            )
        else:
            self._prx_options_node.get_port('control_motion.paste_controls').set_menu_data(
                [
                    ('current frame (pose)', 'tool/paste', self.on_dcc_paste_controls_pose)
                ]
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
            'mirror_motion.mirror_selected_auto', self.on_dcc_mirror_selected_auto
        )

        # mirror and paste
        self._prx_options_node.set(
            'mirror_and_paste_motion.mirror_and_paste_controls', self.on_dcc_mirror_and_paste_controls
        )

        # flip
        self._prx_options_node.set(
            'flip_motion.flip_characters', self.on_dcc_flip_characters
        )
        self._prx_options_node.set(
            'flip_motion.flip_controls', self.on_dcc_flip_controls
        )

        # reset
        self._prx_options_node.set(
            'reset_motion.reset_characters', self.on_dcc_reset_characters
        )
        self._prx_options_node.set(
            'reset_motion.reset_controls', self.on_dcc_reset_controls
        )