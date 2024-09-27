# coding:utf-8
import lxbasic.resource as bsc_resource

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

from . import page_for_main as _page_for_main

from . import page_for_splicing as _page_for_splicing


class PrxSubPanelForMotionTool(gui_prx_widgets.PrxBasePanel):
    CONFIGURE_KEY = 'lazy-motion/gui/tool'

    PAGE_CLASS_DICT = dict(
        main=_page_for_main.PrxPageForMotionMain,
        splicing=_page_for_splicing.PrxPageForMotionSplicing
    )

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForMotionTool, self).__init__(window, session, *args, **kwargs)

    def gui_setup_fnc(self):
        self._page_dict = {}

        self._prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._prx_tab_tool_box)

        self.gui_setup_pages_for(['main', 'splicing'])

        self.do_gui_refresh_all()

    def gui_setup_pages_for(self, page_keys):
        for i_page_key in page_keys:
            if i_page_key not in self.PAGE_CLASS_DICT:
                continue

            i_prx_sca = gui_prx_widgets.PrxVScrollArea()
            self._prx_tab_tool_box.add_widget(
                i_prx_sca,
                key=i_page_key,
                name=gui_core.GuiUtil.choice_name(
                    self._language, self._window._configure.get('build.{}.tab'.format(i_page_key))
                ),
                icon_name_text=i_page_key,
                tool_tip=gui_core.GuiUtil.choice_tool_tip(
                    self._language, self._window._configure.get('build.{}.tab'.format(i_page_key))
                )
            )
            i_prx_page = self._window.generate_page_for(i_page_key)
            self._page_dict[i_page_key] = i_prx_page
            i_prx_sca.add_widget(i_prx_page)

    def do_gui_refresh_all(self):
        self._page_dict[self._prx_tab_tool_box.get_current_key()].do_gui_refresh_all()

