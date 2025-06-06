# coding:utf-8
import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

from .pages import basic as _page_basic


class PrxLazyCfxTool(gui_prx_widgets.PrxBasePanel):
    CONFIGURE_KEY = None

    def __init__(self, *args, **kwargs):
        super(PrxLazyCfxTool, self).__init__(*args, **kwargs)

    def gui_close_fnc(self):
        pass

    def gui_setup_fnc(self):
        self._page_prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._page_prx_tab_tool_box)
        # main
        main_tool_prx_sca = gui_prx_widgets.PrxVScrollArea()
        self._page_prx_tab_tool_box.add_widget(
            main_tool_prx_sca,
            key='main',
            name=gui_core.GuiUtil.choice_gui_name(
                self._language, self._window._configure.get('build.main')
            ),
            icon_name_text='main',
            tool_tip=gui_core.GuiUtil.choice_gui_tool_tip(
                self._language, self._window._configure.get('build.main')
            )
        )
        self._gui_main_tool_prx_page = _page_basic.PrxPageForCfxMainTool(
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
        self.do_gui_refresh_pages(force)

    def do_gui_refresh_pages(self, force):
        key = self._page_prx_tab_tool_box.get_current_key()
        if key == 'main':
            self._gui_main_tool_prx_page.do_gui_refresh_all(force)

