# coding:utf-8
import lxbasic.resource as bsc_resource

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

from . import page_for_motion_main_tool as _page_for_motion_main_tool


class PrxSubPanelForMotionTool(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForMotionTool, self).__init__(*args, **kwargs)
        if window is None:
            self._window = self
        else:
            self._window = window

        self._session = session

        self._language = gui_core.GuiUtil.get_language()

        self._configure = bsc_resource.RscExtendConfigure.get_as_content(
            'lazy-motion/gui/tool'
        )

        self.set_window_title(
            gui_core.GuiUtil.choice_name(self._language, self._configure.get('option.gui'))
        )
        self.set_window_icon_by_name(
            self._configure.get('option.gui.icon_name')
        )
        self.set_definition_window_size(
            self._configure.get('option.gui.size')
        )

        self.gui_setup_fnc()

    def gui_setup_fnc(self):
        self._prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._prx_tab_tool_box)
        # main
        self._gui_main_tool_prx_page = _page_for_motion_main_tool.PrxPageForMotionMainTool(
            self._window, self._session
        )
        self._prx_tab_tool_box.add_widget(
            self._gui_main_tool_prx_page,
            key='main',
            name=gui_core.GuiUtil.choice_name(
                self._language, self._window._configure.get('build.main.tab')
            ),
            icon_name_text='main',
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._language, self._window._configure.get('build.main.tab')
            )
        )

        self.do_gui_refresh_all()

    def do_gui_refresh_all(self):
        if self._prx_tab_tool_box.get_current_key() == 'main':
            self._gui_main_tool_prx_page.do_gui_refresh_all()

