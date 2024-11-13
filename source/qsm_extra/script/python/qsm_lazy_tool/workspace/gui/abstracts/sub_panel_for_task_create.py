# coding:utf-8
import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxSubPanelForTaskCreate(gui_prx_widgets.PrxBaseSubPanel):
    CONFIGURE_KEY = None

    GUI_KEY = 'task_create'

    RESOURCE_BRANCH = None

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxSubPanelForTaskCreate, self).__init__(window, session, *args, **kwargs)

    def gui_setup_fnc(self):
        self._sub_page_prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._sub_page_prx_tab_tool_box)

        self.gui_setup_pages_for(self.SUB_PAGE_KEYS)

        self._sub_page_prx_tab_tool_box.set_history_key(
            'lazy-workspace.{}-toolset'.format(self.GUI_KEY)
        )
        self._sub_page_prx_tab_tool_box.load_history()

        self._sub_page_prx_tab_tool_box.connect_current_changed_to(
            self.do_gui_refresh_all
        )

    def gui_setup(self, resource_properties):
        self._resource_properties = resource_properties

    def gui_setup_pages_for(self, page_keys):
        self._page_dict = {}

        for i_page_key in page_keys:
            if i_page_key not in self.SUB_PAGE_CLASS_DICT:
                continue

            i_prx_sca = gui_prx_widgets.PrxVScrollArea()
            self._sub_page_prx_tab_tool_box.add_widget(
                i_prx_sca,
                key=i_page_key,
                name=gui_core.GuiUtil.choice_name(
                    self._language, self._sub_window._configure.get('build.{}.tab'.format(i_page_key))
                ),
                icon_name_text=i_page_key,
                tool_tip=gui_core.GuiUtil.choice_tool_tip(
                    self._language, self._sub_window._configure.get('build.{}.tab'.format(i_page_key))
                )
            )
            i_prx_page = self._sub_window.gui_generate_sub_page_for(i_page_key)
            self._page_dict[i_page_key] = i_prx_page
            i_prx_sca.add_widget(i_prx_page)

    def do_gui_refresh_all(self):
        key = self._sub_page_prx_tab_tool_box.get_current_key()
        page = self._page_dict[key]
        page.do_gui_refresh_all()
        self._sub_page_prx_tab_tool_box.save_history()
