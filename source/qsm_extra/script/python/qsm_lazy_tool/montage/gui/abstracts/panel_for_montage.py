# coding:utf-8
import functools

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxPanelForMontage(gui_prx_widgets.PrxBasePanel):
    CONFIGURE_KEY = 'lazy-montage/gui/main'

    HST_TAB_KEY_CURRENT = 'lazy-montage-tool.page_key_current'

    PAGE_CLASSES = []

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPanelForMontage, self).__init__(window, session, *args, **kwargs)

    def gui_close_fnc(self):
        self._page_prx_tab_tool_box.save_history()

    def gui_setup_fnc(self):
        self._page_dict = {}

        self._page_prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._page_prx_tab_tool_box)

        for i_cls in self.PAGE_CLASSES:
            i_page_key = i_cls.GUI_KEY

            i_prx_sca = gui_prx_widgets.PrxVScrollArea()
            self._page_prx_tab_tool_box.add_widget(
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
            i_prx_page = i_cls(
                self._window, self._session
            )
            self._page_dict[i_page_key] = i_prx_page
            i_prx_sca.add_widget(i_prx_page)

        self._page_prx_tab_tool_box.set_history_key(self.HST_TAB_KEY_CURRENT)
        self._page_prx_tab_tool_box.load_history()

        self._window.connect_refresh_action_for(functools.partial(self.do_gui_refresh_all, True))

        self._page_prx_tab_tool_box.connect_current_changed_to(self.do_gui_refresh_all)

    def gui_setup_post_fnc(self):
        for k, v in self._page_dict.items():
            v.gui_setup_post_fnc()

    def do_gui_refresh_all(self, force=False):
        self._page_dict[self._page_prx_tab_tool_box.get_current_key()].do_gui_refresh_all(force=force)
