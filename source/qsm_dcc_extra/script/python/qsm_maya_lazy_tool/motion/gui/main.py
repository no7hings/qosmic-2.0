# coding:utf-8
import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

from .pages import basic as _page_basic

from .pages import splicing as _page_splicing

from .pages import fix as _page_fix


class PrxLazyMotionTool(gui_prx_widgets.PrxBasePanel):
    GUI_KEY = 'lazy-motion-tool'

    CONFIGURE_KEY = None

    PAGE_CLASSES = [
        _page_basic.PrxPageForMotionMain,
        _page_splicing.PrxPageForMotionSplicing,
        _page_fix.PrxPageForMotionFix
    ]

    def __init__(self, window, session, *args, **kwargs):
        super(PrxLazyMotionTool, self).__init__(window, session, *args, **kwargs)

    def gui_setup_fnc(self):
        self._tab_widget_dict = {}

        self._page_prx_tab_tool_box = self.gui_create_tab_tool_box()
        self.add_widget(self._page_prx_tab_tool_box)

        self.gui_setup_pages_for(['main', 'splicing', 'fix'])

        self._page_prx_tab_tool_box.load_history()

        self.do_gui_refresh_all()

    def gui_setup_pages_for(self, page_keys):
        for i_page_key in page_keys:
            if i_page_key not in self._page_class_dict:
                continue

            i_prx_sca = gui_prx_widgets.PrxVScrollArea()
            i_prx_page = self._window.gui_generate_page_for(i_page_key)
            self._page_prx_tab_tool_box.add_widget(
                i_prx_sca,
                key=i_page_key,
                name=i_prx_page.get_gui_name(),
                icon_name_text=i_page_key,
                tool_tip=i_prx_page.get_gui_tool_tip()
            )
            self._tab_widget_dict[i_page_key] = i_prx_page
            i_prx_sca.add_widget(i_prx_page)

    def do_gui_refresh_all(self):
        self._page_prx_tab_tool_box.save_history()

        self._tab_widget_dict[self._page_prx_tab_tool_box.get_current_key()].do_gui_refresh_all()
