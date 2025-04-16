# coding:utf-8
import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_general.core as qsm_gnl_core

import lnx_dcc_tool_prc.gui.proxy.widgets as lzy_gui_prx_widgets


class AbsPrxPageForTaskManager(gui_prx_widgets.PrxBasePage):
    GUI_KEY = 'task_manager'

    RESOURCE_TYPES = []

    SWAP_RESOURCE_INPUT_CLS_DICT = dict(
        project=lzy_gui_prx_widgets.PrxInputForProject,
        asset=lzy_gui_prx_widgets.PrxInputForAsset,
        episode=lzy_gui_prx_widgets.PrxInputForEpisode,
        sequence=lzy_gui_prx_widgets.PrxInputForSequence,
        shot=lzy_gui_prx_widgets.PrxInputForShot
    )

    def __init__(self, *args, **kwargs):
        super(AbsPrxPageForTaskManager, self).__init__(*args, **kwargs)

        # studio
        self._studio = qsm_gnl_core.Sync().studio.get_current()

        # artist
        self._artist_history_key = [self._window.GUI_KEY, 'artist']
        self._artist = gui_core.GuiHistoryStage().get_one(self._artist_history_key) or 'shared'

        self._resource_history_key = 'wotrix.{resource_type}-path'

        self.gui_page_setup_fnc()

    def _gui_add_user_switch_tool(self):
        self._user_switch_qt_button = gui_qt_widgets.QtIconPressButton()
        self._main_prx_tool_box.add_widget(self._user_switch_qt_button)
        self._user_switch_qt_button._set_name_text_('user switch')
        self._user_switch_qt_button._set_icon_name_('users')
        self._user_switch_qt_button.press_clicked.connect(self._on_gui_switch_user)

        self._user_qt_info_bubble = gui_qt_widgets.QtInfoBubble()
        self._main_prx_tool_box.add_widget(self._user_qt_info_bubble)
        self._user_qt_info_bubble._set_style_(
            self._user_qt_info_bubble.Style.Frame
        )
        self._user_qt_info_bubble._set_text_('{}:{}'.format(self._studio, self._artist))
        # self._user_qt_info_bubble

    def _on_gui_switch_user(self):
        options = ['shared', bsc_core.BscSystem.get_user_name()]
        result = gui_core.GuiApplication.exec_input_dialog(
            type='choose',
            options=options,
            info='Choose User...',
            value=self._artist,
            title='Switch User'
        )
        if result:
            self._gui_switch_user(result)

    def _gui_switch_user(self, artist):
        if artist != self._artist:
            self._artist = artist
            self._user_qt_info_bubble._set_text_('{}:{}'.format(self._studio, self._artist))
            gui_core.GuiHistoryStage().set_one(self._artist_history_key, self._artist)

            self.do_gui_refresh_all()
            self._window.popup_message(
                self._window.choice_gui_message(
                    self._window._configure.get('build.messages.switch_user')
                ).format(artist=self._artist)
            )

    def gui_page_setup_fnc(self):
        self._top_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_align_left()
        self._top_prx_tool_bar.set_expanded(True)

        # main tool box
        self._main_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'main'
        )
        self._gui_add_user_switch_tool()
        
        self._scan_resource_prx_input_dict = {}

        # resource
        self._resource_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'resource', size_mode=1
        )

        self._unit_prx_tab_tool_box = self.gui_create_tab_tool_box()
        self._qt_layout.addWidget(self._unit_prx_tab_tool_box.widget)

        self._task_tool_box = self._top_prx_tool_bar.create_tool_box(
            'task'
        )

        self._create_task_qt_button = gui_qt_widgets.QtPressButton()
        self._task_tool_box.add_widget(self._create_task_qt_button)
        self._create_task_qt_button._set_name_text_(
            self._window.choice_gui_name(
                self._window._configure.get('build.buttons.create_task')
            )
        )
        self._create_task_qt_button._set_icon_name_('workspace/task-create')
        self._create_task_qt_button._set_auto_width_(True)
        self._create_task_qt_button.press_clicked.connect(self._gui_show_task_create_window)

        self.gui_setup_units_for(self._unit_prx_tab_tool_box, self.RESOURCE_TYPES)

    def _gui_show_task_create_window(self):
        resource_type = self._unit_prx_tab_tool_box.get_current_key()
        unit = self._tab_widget_dict[resource_type]
        resource_properties = unit._resource_properties
        if unit._resource_properties:
            w = self._window.gui_generate_sub_panel_for('task_create')
            w.gui_setup(unit, resource_properties)
            w.do_gui_refresh_all()
            w.show_window_auto()
        else:
            self._window.exec_message_dialog(
                'entry one {} and retry.'.format(resource_type),
                title='Task Create',
                status='warning'
            )

    def gui_setup_post_fnc(self):
        for k, v in self._tab_widget_dict.items():
            v.gui_setup_post_fnc()

        self._top_prx_tool_bar.do_gui_refresh(fix_bug=True)

    def do_gui_refresh_all(self):
        self.do_gui_refresh_unit_auto(self._unit_prx_tab_tool_box)

        resource_type = self._unit_prx_tab_tool_box.get_current_key()
        self.gui_get_scan_resource_prx_input(resource_type)
        
    def gui_get_scan_resource_prx_input(self, resource_type):
        for i in self._scan_resource_prx_input_dict.values():
            i.set_hide()

        if resource_type in self._scan_resource_prx_input_dict:
            resource_prx_input = self._scan_resource_prx_input_dict[resource_type]
            resource_prx_input.set_hide(False)
            return resource_prx_input

        # create new
        resource_prx_input = self.SWAP_RESOURCE_INPUT_CLS_DICT[resource_type](
            history_key=self._resource_history_key.format(resource_type=resource_type)
        )
        unit = self._tab_widget_dict[resource_type]
        resource_prx_input.connect_input_change_accepted_to(unit._do_gui_refresh_resource_for)
        self._resource_prx_tool_box.add_widget(resource_prx_input)
        self._scan_resource_prx_input_dict[resource_type] = resource_prx_input
        return resource_prx_input

    def gui_set_current_page(self, key):
        result = self._unit_prx_tab_tool_box.set_current_key(key)
        if result is True:
            return self._tab_widget_dict[key]
