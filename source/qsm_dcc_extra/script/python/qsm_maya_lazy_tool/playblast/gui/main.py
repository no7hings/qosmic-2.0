# coding:utf-8
import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

from .pages import basic as _page_basic


class PrxLazyPlayblastTool(gui_prx_widgets.PrxBasePanel):
    CONFIGURE_KEY = 'lazy-playblast/gui/tool'

    def __init__(self, *args, **kwargs):
        super(PrxLazyPlayblastTool, self).__init__(*args, **kwargs)

    def gui_close_fnc(self):
        self._page_prx_tab_tool_box.save_history()

    def gui_setup_fnc(self):
        self._page_prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._page_prx_tab_tool_box)
        # main
        main_tool_prx_sca = gui_prx_widgets.PrxVScrollArea()
        self._page_prx_tab_tool_box.add_widget(
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
        self._gui_main_tool_prx_page = _page_basic.PrxPageForPlayblast(
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
        key = self._page_prx_tab_tool_box.get_current_key()
        if key == 'main':
            self._gui_main_tool_prx_page.do_gui_refresh_all(force)
