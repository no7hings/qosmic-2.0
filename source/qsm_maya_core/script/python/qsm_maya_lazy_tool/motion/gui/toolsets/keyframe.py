# coding:utf-8
import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_maya.core as qsm_mya_core

import qsm_maya.handles.animation.core as qsm_mya_hdl_anm_core

import qsm_maya.motion.core as qsm_mya_mtn_core

import qsm_maya.adv as qsm_mya_adv


class ToolsetForMotionKeyframe(
    gui_prx_widgets.PrxVirtualBaseUnit
):
    GUI_KEY = 'keyframe'

    def _do_dcc_select_all_curves(self):
        curves = qsm_mya_core.AnmCurveNodes.get_all(reference=False, excludes=['timewarp', 'qsm_timewarp'])
        qsm_mya_core.Selection.set(curves)

        self._window.popup_message(
            self._window.choice_gui_message(
                self._page._configure.get('build.messages.select_all_curves')
            )
        )

    def _do_dcc_select_character_all_curves(self):
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

        if results:
            curves = []
            for i_namespace in results:
                i_opt = qsm_mya_adv.AdvChrOpt(i_namespace)
                curves.extend(i_opt.find_all_anm_curves())

            qsm_mya_core.Selection.set(curves)

            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.select_all_character_curves')
                )
            )

    def _on_dcc_euler_filter(self):
        anm_curves = qsm_mya_core.Selection.get_all_anm_curves()
        if anm_curves:
            qsm_mya_core.AnmCurveNodes.euler_filter(anm_curves)

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
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.update_timewarp_preview')
                )
            )

        self._do_dcc_refresh_timewrap_buttons()

    def _do_dcc_remove_timewrap_preview(self):
        result = qsm_mya_mtn_core.TimewarpOpt.remove()
        if result is True:
            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.remove_timewarp_preview')
                )
            )
        else:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.no_timewarp_preview')
                ),
                status='warning'
            )

        self._do_dcc_refresh_timewrap_buttons()

    def _do_dcc_apply_timewrap(self):
        result = qsm_mya_mtn_core.TimewarpOpt.apply()
        if result is True:
            self._window.popup_message(
                self._window.choice_gui_message(
                    self._page._configure.get('build.messages.apply_timewarp')
                )
            )

        self._do_dcc_refresh_timewrap_buttons()

    def __init__(self, window, page, session):
        super(ToolsetForMotionKeyframe, self).__init__(window, page, session)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_gui_name(
                self._window._language,
                self._page._configure.get('build.units.{}.options'.format(self.GUI_KEY))
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

        self._prx_options_node.set(
            'selection.select_all_curves', self._do_dcc_select_all_curves
        )
        self._prx_options_node.set(
            'selection.select_character_all_curves', self._do_dcc_select_character_all_curves
        )

        self._prx_options_node.set(
            'curve_filter.euler_filter', self._on_dcc_euler_filter
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
