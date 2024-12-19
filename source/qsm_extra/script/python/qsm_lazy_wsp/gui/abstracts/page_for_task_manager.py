# coding:utf-8
import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxPageForTaskManager(gui_prx_widgets.PrxBasePage):
    GUI_KEY = 'task_manager'

    TASK_BRANCHES = []

    def __init__(self, *args, **kwargs):
        super(AbsPrxPageForTaskManager, self).__init__(*args, **kwargs)

        self.gui_page_setup_fnc()

    def gui_page_setup_fnc(self):
        self._unit_prx_tab_tool_box = self.gui_create_tab_tool_box()
        self._qt_layout.addWidget(self._unit_prx_tab_tool_box.widget)

        self.gui_setup_units_for(self._unit_prx_tab_tool_box, self.TASK_BRANCHES)
        
    def gui_setup_post_fnc(self):
        for k, v in self._tab_widget_dict.items():
            v.gui_setup_post_fnc()

    def do_gui_refresh_all(self):
        self.do_gui_refresh_units(self._unit_prx_tab_tool_box)

    def gui_set_current_page(self, key):
        result = self._unit_prx_tab_tool_box.set_current_key(key)
        if result is True:
            return self._tab_widget_dict[key]
