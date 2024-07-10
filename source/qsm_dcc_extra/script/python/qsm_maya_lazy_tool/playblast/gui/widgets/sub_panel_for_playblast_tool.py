# coding:utf-8
import lxbasic.resource as bsc_resource

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

from . import page_for_playblast_main_tool as _page_for_playblast_main_tool


class PrxSubPanelForLazyPlayblast(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForLazyPlayblast, self).__init__(*args, **kwargs)
        if window is None:
            self._window = self
        else:
            self._window = window

        self._session = session

        self._language = gui_core.GuiUtil.get_language()

        self._configure = bsc_resource.RscExtendConfigure.get_as_content(
            'lazy-playblast/gui/tool'
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

        self.gui_setup_window()
    
    def gui_close_fnc(self):
        self._prx_tab_tool_box.save_history()

    def gui_setup_window(self):
        self._prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._prx_tab_tool_box)
        # main
        main_tool_prx_sca = gui_prx_widgets.PrxVScrollArea()
        self._prx_tab_tool_box.add_widget(
            main_tool_prx_sca,
            key='main',
            name=gui_core.GuiUtil.choice_name(
                self._language, self._window._configure.get('build.main.tab')
            ),
            icon_name_text='main',
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._language, self._window._configure.get('build.main.tab')
            )
        )
        self._gui_main_tool_prx_page = _page_for_playblast_main_tool.PrxPageForPlayblast(
            self._window, self._session
        )
        main_tool_prx_sca.add_widget(self._gui_main_tool_prx_page)

        self._window.connect_refresh_action_for(
            lambda: self.do_gui_refresh_all(True)
        )
        self.register_window_close_method(
            self.gui_close_fnc
        )

        self.do_gui_refresh_all()

    def do_gui_refresh_all(self, force=False):
        key = self._prx_tab_tool_box.get_current_key()
        if key == 'main':
            self._gui_main_tool_prx_page.do_gui_refresh_all(force)
