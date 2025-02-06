# coding:utf-8
import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_maya.core as qsm_mya_core

import qsm_maya.adv as qsm_mya_adv

import qsm_maya.handles.animation.core as qsm_mya_hdl_anm_core


class ToolsetForMotionControlAndMove(
    gui_prx_widgets.PrxVirtualBaseUnit
):
    GUI_KEY = 'control'

    @staticmethod
    def do_dcc_create_control_move_locator():
        import lxbasic.session as bsc_session
        bsc_session.OptionHook.execute(
            "option_hook_key=dcc-script/maya/qsm-control-move-create-script"
        )

    @staticmethod
    def do_dcc_remove_control_move_locator():
        import lxbasic.session as bsc_session
        bsc_session.OptionHook.execute(
            "option_hook_key=dcc-script/maya/qsm-control-move-remove-script"
        )

    @staticmethod
    def do_dcc_create_control_transform_locator():
        import lxbasic.session as bsc_session
        bsc_session.OptionHook.execute(
            "option_hook_key=dcc-script/maya/qsm-control-transform-create-script"
        )

    @staticmethod
    def do_dcc_remove_control_transform_locator():
        import lxbasic.session as bsc_session
        bsc_session.OptionHook.execute(
            "option_hook_key=dcc-script/maya/qsm-control-transform-remove-script"
        )

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

    def on_dcc_enable_control_playback_visible(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            for i_namespace in namespaces:
                i_opt = qsm_mya_adv.AdvChrOpt(i_namespace)
                i_controls = i_opt.find_all_controls()
                [qsm_mya_core.NodeAttribute.set_value(x, 'hideOnPlayback', 0) for x in i_controls]

    def on_dcc_disable_control_playback_visible(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            for i_namespace in namespaces:
                i_opt = qsm_mya_adv.AdvChrOpt(i_namespace)
                i_controls = i_opt.find_all_controls()
                [qsm_mya_core.NodeAttribute.set_value(x, 'hideOnPlayback', 1) for x in i_controls]

    def __init__(self, window, page, session):
        super(ToolsetForMotionControlAndMove, self).__init__(window, page, session)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_gui_name(
                self._window._language, self._page._configure.get('build.units.{}.options'.format(self.GUI_KEY))
            )
        )

        self._prx_options_node.build_by_data(
            self._page._configure.get('build.units.{}.options.parameters'.format(self.GUI_KEY)),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key=self.GUI_KEY,
            name=gui_core.GuiUtil.choice_gui_name(
                self._window._language, self._page._configure.get('build.units.{}'.format(self.GUI_KEY))
            ),
            icon_name_text=self.GUI_KEY,
            tool_tip=gui_core.GuiUtil.choice_gui_tool_tip(
                self._window._language, self._page._configure.get('build.units.{}'.format(self.GUI_KEY))
            )
        )
        
        # control move
        self._prx_options_node.set(
            'control_move.create_locator', self.do_dcc_create_control_move_locator
        )

        self._prx_options_node.set(
            'control_move.remove_locator', self.do_dcc_remove_control_move_locator
        )
        
        # control transform
        self._prx_options_node.set(
            'control_transform.create_locator', self.do_dcc_create_control_transform_locator
        )

        self._prx_options_node.set(
            'control_transform.remove_locator', self.do_dcc_remove_control_transform_locator
        )

        # control
        self._prx_options_node.set(
            'control.enable_playback_visible', self.on_dcc_enable_control_playback_visible
        )
        self._prx_options_node.set(
            'control.disable_playback_visible', self.on_dcc_disable_control_playback_visible
        )
