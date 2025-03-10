# coding:utf-8
import lxbasic.resource as bsc_resource

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxPanelForValidation(gui_prx_widgets.PrxBasePanel):

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPanelForValidation, self).__init__(window, session, *args, **kwargs)

    def gui_setup_fnc(self):
        self._tab_widget_dict = {}

        self._page_prx_tab_tool_box = self.gui_create_tab_tool_box()
        self.add_widget(self._page_prx_tab_tool_box)

        self.gui_setup_pages_for(['rig', 'rig_batch', 'scenery', 'scenery_batch'])

        self._page_prx_tab_tool_box.load_history()
        self.register_window_close_method(
            self.gui_close_fnc
        )

    def gui_close_fnc(self):
        pass

    def gui_setup_pages_for(self, page_keys):
        for i_page_key in page_keys:
            if i_page_key not in self._page_class_dict:
                continue

            i_prx_sca = gui_prx_widgets.PrxVScrollArea()

            self._page_prx_tab_tool_box.add_widget(
                i_prx_sca,
                key=i_page_key,
                name=gui_core.GuiUtil.choice_gui_name(
                    self._language, self._window._configure.get('build.{}'.format(i_page_key))
                ),
                icon_name_text=i_page_key,
                tool_tip=gui_core.GuiUtil.choice_gui_tool_tip(
                    self._language, self._window._configure.get('build.{}'.format(i_page_key))
                )
            )

            i_prx_page = self._window.gui_generate_page_for(i_page_key)
            self._tab_widget_dict[i_page_key] = i_prx_page
            i_prx_sca.add_widget(i_prx_page)

    def do_gui_refresh_all(self):
        pass
