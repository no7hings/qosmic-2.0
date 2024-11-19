# coding:utf-8
import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxPageForTaskManager(gui_prx_widgets.PrxBasePage):
    GUI_KEY = 'task_manager'

    def __init__(self, *args, **kwargs):
        super(AbsPrxPageForTaskManager, self).__init__(*args, **kwargs)

        self.gui_page_setup_fnc()

    def gui_page_setup_fnc(self):
        self._unit_prx_tab_tool_box = self.gui_create_v_tab_tool_box()
        self.gui_setup_units_for(self._unit_prx_tab_tool_box, ['asset', 'shot'])
        
    def gui_setup_post_fnc(self):
        for k, v in self._page_dict.items():
            v.gui_setup_post_fnc()

    def do_gui_refresh_all(self):
        self.do_gui_refresh_units(self._unit_prx_tab_tool_box)
