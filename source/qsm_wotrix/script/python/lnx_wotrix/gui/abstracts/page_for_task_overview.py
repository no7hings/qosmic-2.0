# coding:utf-8
import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_dcc_tool_prc.gui.proxy.widgets as lzy_gui_prx_widgets

from . import unit_base as _unit_base


class AbsPrxPageForTaskOverview(gui_prx_widgets.PrxBasePage):
    GUI_KEY = 'task_overview'

    RESOURCE_TYPES = []

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForTaskOverview, self).__init__(window, session, *args, **kwargs)

        self._resource_path = None

        self.gui_page_setup_fnc()

    def gui_page_setup_fnc(self):
        self._top_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_align_left()
        self._top_prx_tool_bar.set_expanded(True)

        self._resource_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'resource', size_mode=1
        )
        self._scan_resource_prx_input = lzy_gui_prx_widgets.PrxInputForProject(
            history_key='wotrix.task_overview.project-path'
        )

        self._resource_prx_tool_box.add_widget(self._scan_resource_prx_input)

        self._scan_resource_prx_input.connect_input_change_accepted_to(self._do_gui_refresh_resource_for)

        self._unit_prx_tab_tool_box = self.gui_create_tab_tool_box()
        self._qt_layout.addWidget(self._unit_prx_tab_tool_box.widget)

        self.gui_setup_units_for(self._unit_prx_tab_tool_box, self.RESOURCE_TYPES)

    def _do_gui_refresh_resource_for(self, path):
        self._resource_path = path

        scn_entity = self._scan_resource_prx_input.get_entity(
            path
        )
        if scn_entity:
            key = self._unit_prx_tab_tool_box.get_current_key()
            gui = self._tab_widget_dict.get(key)
            if gui:
                gui.do_gui_load_project(scn_entity)
