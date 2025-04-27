# coding:utf-8
import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxSubPanelForAssign(gui_prx_widgets.PrxBaseSubpanel):
    # CONFIGURE_KEY = 'resora/gui/assign'

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxSubPanelForAssign, self).__init__(window, session, *args, **kwargs)

    def gui_setup_fnc(self):
        self._page_prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._page_prx_tab_tool_box)

    def gui_setup_pages_for(self, page_keys):
        for i_page_key in page_keys:
            if i_page_key not in self._subpage_class_dict:
                continue

            i_prx_sca = gui_prx_widgets.PrxVScrollArea()
            i_prx_page = self._subwindow.gui_generate_subpage_for(i_page_key)
            i_prx_sca.add_widget(i_prx_page)

            self._page_prx_tab_tool_box.add_widget(
                i_prx_sca,
                key=i_page_key,
                name=i_prx_page.get_gui_name(),
                icon_name_text=i_page_key,
                tool_tip=i_prx_page.get_gui_tool_tip()
            )
            self._tab_widget_dict[i_page_key] = i_prx_page
