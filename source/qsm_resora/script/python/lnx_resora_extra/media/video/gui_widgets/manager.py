# coding:utf-8
import functools

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_resora.core.drop_action as lnx_rsr_cor_drag

import lnx_resora.gui.abstracts as lnx_rsr_gui_abstracts


class GuiResourceManagerMain(lnx_rsr_gui_abstracts.AbsPrxPageForManager):
    class DragMode:
        Default = 'default'
        MayaFxProxyRig = 'maya_fx_proxy_rig'

    def __init__(self, window, session, *args, **kwargs):
        super(GuiResourceManagerMain, self).__init__(window, session, *args, **kwargs)

    def gui_page_setup_sup_fnc(self):
        self._drag_mode = gui_core.GuiHistoryStage().get_one(self._gui_history_group+['drag_mode']) or 'default'

        self._drag_mode_switch_prx_tool_box = self.gui_add_top_tool_box('drag mode switch')
        self._gui_add_drag_mode_switch_tools()

    def _gui_add_drag_mode_switch_tools(self):
        cfg = [
            (self.DragMode.Default, 'file/file'),
            (self.DragMode.MayaFxProxyRig, 'application/maya'),
        ]
        tools = []
        for i_drag_mode, i_icon_name in cfg:
            i_tool = gui_prx_widgets.PrxIconToggleButton()
            self._drag_mode_switch_prx_tool_box.add_widget(i_tool)

            i_tool._qt_widget._set_exclusive_widgets_(tools)
            i_tool.set_name(i_drag_mode)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip('"LMB-click" for switch to drag mode to "{}".'.format(i_drag_mode))

            if i_drag_mode == self._drag_mode:
                i_tool.set_checked(True)

            tools.append(i_tool._qt_widget)
            i_tool.connect_check_changed_as_exclusive_to(
                functools.partial(self._gui_switch_drag_mode, i_drag_mode)
            )

    def _gui_switch_drag_mode(self, drag_mode):
        pass
