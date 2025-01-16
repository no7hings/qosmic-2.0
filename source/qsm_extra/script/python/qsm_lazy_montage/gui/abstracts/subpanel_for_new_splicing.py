# coding:utf-8
import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxSubpanelForNewSplicing(gui_prx_widgets.PrxBaseSubpanel):
    CONFIGURE_KEY = 'lazy-montage/gui/new_splicing'

    GUI_KEY = 'new_splicing'

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxSubpanelForNewSplicing, self).__init__(window, session, *args, **kwargs)

    def gui_setup_fnc(self):
        self._sub_page_prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._sub_page_prx_tab_tool_box)

        self.gui_setup_pages_for(['general'])

        self._sub_page_prx_tab_tool_box.set_history_key('lazy-montage.{}-page'.format(self.GUI_KEY))
        self._sub_page_prx_tab_tool_box.load_history()
        
        self._sub_page_prx_tab_tool_box.connect_current_changed_to(
            self.do_gui_refresh_all
        )

    def gui_setup_pages_for(self, page_keys):
        self._tab_widget_dict = {}

        for i_gui_key in page_keys:
            if i_gui_key not in self._sub_page_class_dict:
                continue

            i_prx_sca = gui_prx_widgets.PrxVScrollArea()
            i_prx_page = self._subwindow.gui_generate_sub_page_for(i_gui_key)
            i_prx_sca.add_widget(i_prx_page)

            self._sub_page_prx_tab_tool_box.add_widget(
                i_prx_sca,
                key=i_gui_key,
                name=i_prx_page.get_gui_name(),
                icon_name_text=i_gui_key,
                tool_tip=i_prx_page.get_gui_tool_tip()
            )

            self._tab_widget_dict[i_gui_key] = i_prx_page
    
    def do_gui_refresh_all(self):
        key = self._sub_page_prx_tab_tool_box.get_current_key()
        page = self._tab_widget_dict.get(key)
        if page:
            page.do_gui_refresh_all()
            self._sub_page_prx_tab_tool_box.save_history()
