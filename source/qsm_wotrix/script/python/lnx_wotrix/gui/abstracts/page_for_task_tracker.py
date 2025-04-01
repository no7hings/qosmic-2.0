# coding:utf-8
import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_dcc_tool_prc.gui.proxy.widgets as lzy_gui_prx_widgets


class AbsPrxPageForTaskTracker(gui_prx_widgets.PrxBasePage):
    GUI_KEY = 'task_tracker'

    RESOURCE_TYPES = []

    def __init__(self, *args, **kwargs):
        super(AbsPrxPageForTaskTracker, self).__init__(*args, **kwargs)

        self._resource_path = None

        self._space_key_history_key = [self._window.GUI_KEY, 'space_key']
        self._space_key = gui_core.GuiHistoryStage().get_one(self._space_key_history_key) or 'release'

        self.gui_page_setup_fnc()

    def _gui_add_space_switch_tool(self):
        self._space_switch_qt_button = gui_qt_widgets.QtIconPressButton()
        self._main_prx_tool_box.add_widget(self._space_switch_qt_button)
        self._space_switch_qt_button._set_name_text_('space switch')
        self._space_switch_qt_button._set_icon_name_('spaces')
        self._space_switch_qt_button.press_clicked.connect(self._on_gui_switch_space)

        self._space_qt_info_bubble = gui_qt_widgets.QtInfoBubble()
        self._main_prx_tool_box.add_widget(self._space_qt_info_bubble)
        self._space_qt_info_bubble._set_style_(
            self._space_qt_info_bubble.Style.Frame
        )
        self._space_qt_info_bubble._set_text_(self._space_key)

    def _on_gui_switch_space(self):
        options = ['source', 'release']
        result = gui_core.GuiApplication.exec_input_dialog(
            type='choose',
            options=options,
            info='Choose Space...',
            value=self._space_key,
            title='Switch Space'
        )
        if result:
            if result in options:
                self._gui_switch_space(result)

    def _gui_switch_space(self, space_key):
        if space_key != self._space_key:
            self._space_key = space_key
            self._space_qt_info_bubble._set_text_(self._space_key)
            gui_core.GuiHistoryStage().set_one(self._space_key_history_key, space_key)

            self.do_gui_refresh_all()

            self._window.popup_message(
                self._window.choice_gui_message(
                    self._window._configure.get('build.messages.switch_space')
                ).format(space_key=self._space_key)
            )

    def gui_page_setup_fnc(self):
        self._top_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_align_left()
        self._top_prx_tool_bar.set_expanded(True)

        # main tool box
        self._main_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'space'
        )
        self._gui_add_space_switch_tool()

        self._resource_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'resource', size_mode=1
        )
        self._scan_resource_prx_input = lzy_gui_prx_widgets.PrxInputForProject(
            history_key='wotrix.task_tracker.project-path'
        )

        self._resource_prx_tool_box.add_widget(self._scan_resource_prx_input)

        self._scan_resource_prx_input.connect_input_change_accepted_to(self._do_gui_refresh_resource_for)

        self._unit_prx_tab_tool_box = self.gui_create_tab_tool_box()
        self._qt_layout.addWidget(self._unit_prx_tab_tool_box.widget)

        self.gui_setup_units_for(self._unit_prx_tab_tool_box, self.RESOURCE_TYPES)

    def gui_setup_post_fnc(self):
        for k, v in self._tab_widget_dict.items():
            v.gui_setup_post_fnc()

    def do_gui_refresh_all(self):
        self.do_gui_refresh_units(self._unit_prx_tab_tool_box)

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

    def get_scn_entity(self):
        return self._scan_resource_prx_input.get_entity(
            self._scan_resource_prx_input.get_path()
        )
