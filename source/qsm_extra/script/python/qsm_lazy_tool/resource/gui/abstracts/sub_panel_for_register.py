# coding:utf-8
import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxSubPanelForRegister(gui_prx_widgets.PrxBaseSubpanel):
    CONFIGURE_KEY = 'lazy-resource/gui/register'

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxSubPanelForRegister, self).__init__(window, session, *args, **kwargs)

    def gui_setup_fnc(self):
        self._page_prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._page_prx_tab_tool_box)
    
    def gui_setup_pages_for(self, page_keys):
        for i_page_key in page_keys:
            if i_page_key not in self._sub_page_class_dict:
                continue

            i_prx_sca = gui_prx_widgets.PrxVScrollArea()
            self._page_prx_tab_tool_box.add_widget(
                i_prx_sca,
                key=i_page_key,
                name=gui_core.GuiUtil.choice_gui_name(
                    self._language, self._sub_window._configure.get('build.{}.tab'.format(i_page_key))
                ),
                icon_name_text=i_page_key,
                tool_tip=gui_core.GuiUtil.choice_gui_tool_tip(
                    self._language, self._sub_window._configure.get('build.{}.tab'.format(i_page_key))
                )
            )
            i_prx_page = self._sub_window.gui_generate_sub_page_for(i_page_key)
            self._tab_widget_dict[i_page_key] = i_prx_page
            i_prx_sca.add_widget(i_prx_page)
