# coding:utf-8
import functools

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

from .pages import compose as _compose


class PrxPanelForMosaic(gui_prx_widgets.PrxBasePanel):
    CONFIGURE_KEY = 'mosaic/gui/main'

    HST_TAB_KEY_CURRENT = 'mosaic.page_key_current'

    PAGE_CLASSES = [
        _compose.AbsPrxPageForCompose
    ]

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPanelForMosaic, self).__init__(window, session, *args, **kwargs)

    def gui_close_fnc(self):
        self._page_prx_tab_tool_box.save_history()

    def gui_setup_fnc(self):
        self._tab_widget_dict = {}

        self._page_prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._page_prx_tab_tool_box)

        for i_cls in self.PAGE_CLASSES:
            i_page_key = i_cls.GUI_KEY

            i_prx_sca = gui_prx_widgets.PrxVScrollArea()
            self._page_prx_tab_tool_box.add_widget(
                i_prx_sca,
                key=i_page_key,
                name=gui_core.GuiUtil.choice_gui_name(
                    self._language, self._window._configure.get('build.{}.tab'.format(i_page_key))
                ),
                icon_name_text=i_page_key,
                tool_tip=gui_core.GuiUtil.choice_gui_tool_tip(
                    self._language, self._window._configure.get('build.{}.tab'.format(i_page_key))
                )
            )
            i_prx_page = i_cls(
                self._window, self._session
            )
            self._tab_widget_dict[i_page_key] = i_prx_page
            i_prx_sca.add_widget(i_prx_page)

        self._page_prx_tab_tool_box.set_history_key(self.HST_TAB_KEY_CURRENT)
        self._page_prx_tab_tool_box.load_history()

        self._window.connect_refresh_action_for(functools.partial(self.do_gui_refresh_all, True))

        self._page_prx_tab_tool_box.connect_current_changed_to(self.do_gui_refresh_all)

    def gui_setup_post_fnc(self):
        for k, v in self._tab_widget_dict.items():
            v.gui_setup_post_fnc()

    def do_gui_refresh_all(self, force=False):
        self._tab_widget_dict[self._page_prx_tab_tool_box.get_current_key()].do_gui_refresh_all(force=force)
