# coding:utf-8
import lxbasic.resource as bsc_resource

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

from . import page_for_register_tool as _page_for_register_tool

from . import page_for_load_tool as _page_for_load_tool


class AbsPrxSubPanelForTool(gui_prx_widgets.PrxBaseWindow):
    PAGE_FOR_REGISTER_TOOL_CLS = _page_for_register_tool.AbsPrxPageForRegisterTool

    PAGE_FOR_LOAD_TOOL_CLS = _page_for_load_tool.AbsPrxPageForLoadTool

    class TabKeys:
        Register = 'register'
        Load = 'load'

    def do_gui_update_by_dcc_selection(self):
        if self._page_prx_tab_tool_box.get_current_key() == self.TabKeys.Register:
            self._register_prx_page.do_gui_update_by_dcc_selection()
        elif self._page_prx_tab_tool_box.get_current_key() == self.TabKeys.Load:
            self._load_prx_page.do_gui_update_by_dcc_selection()

    def _do_dcc_register_all_script_jobs(self):
        pass

    def _do_dcc_destroy_all_script_jobs(self):
        pass

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxSubPanelForTool, self).__init__(*args, **kwargs)
        if window is None:
            self._window = self
        else:
            self._window = window

        self._session = session

        self._language = gui_core.GuiUtil.get_language()

        self._configure = bsc_resource.RscExtendConfigure.get_as_content(
            'lazy-resource/gui/tool'
        )

        self.set_window_title(
            gui_core.GuiUtil.choice_name(self._language, self._configure.get('option.gui'))
        )
        self.set_window_icon_by_name(
            self._configure.get('option.gui.icon_name')
        )
        self.set_definition_window_size(
            self._configure.get('option.gui.size')
        )

        self.gui_setup_window()

    def apply_and_close_fnc(self):
        if self._page_prx_tab_tool_box.get_current_key() == self.TabKeys.Register:
            self._register_prx_page.do_apply()
        elif self._page_prx_tab_tool_box.get_current_key() == self.TabKeys.Load:
            self._load_prx_page.do_apply()

        self.do_close_window_later(500)

    def apply_fnc(self):
        if self._page_prx_tab_tool_box.get_current_key() == self.TabKeys.Register:
            self._register_prx_page.do_apply()
        elif self._page_prx_tab_tool_box.get_current_key() == self.TabKeys.Load:
            self._load_prx_page.do_apply()

    def close_fnc(self):
        self.do_close_window_later(500)

    def gui_set_buttons_enable(self, boolean):
        for i in [
            self._apply_and_close_prx_button,
            self._apply_prx_button,
            self._close_prx_button,
        ]:
            i.set_enable(boolean)

    def gui_setup_window(self):
        self._page_prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._page_prx_tab_tool_box)
        # register
        register_prx_sca = gui_prx_widgets.PrxVScrollArea()
        self._page_prx_tab_tool_box.add_widget(
            register_prx_sca,
            key='register',
            name=gui_core.GuiUtil.choice_name(
                self._language, self._window._configure.get('build.register.tab')
            ),
            icon_name_text='register',
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._language, self._window._configure.get('build.register.tab')
            )
        )
        self._register_prx_page = self.PAGE_FOR_REGISTER_TOOL_CLS(
            self._window, self._session
        )
        register_prx_sca.add_widget(self._register_prx_page)
        # load
        load_prx_sca = gui_prx_widgets.PrxVScrollArea()
        self._page_prx_tab_tool_box.add_widget(
            load_prx_sca,
            key='load',
            name=gui_core.GuiUtil.choice_name(
                self._language, self._window._configure.get('build.load.tab')
            ),
            icon_name_text='load',
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._language, self._window._configure.get('build.load.tab')
            )
        )

        self._load_prx_page = self.PAGE_FOR_LOAD_TOOL_CLS(
            self._window, self._session
        )
        load_prx_sca.add_widget(self._load_prx_page)
        # buttons
        self._bottom_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        self.add_widget(self._bottom_prx_tool_bar)
        self._bottom_prx_tool_bar.set_expanded(True)

        self._apply_and_close_prx_button = gui_prx_widgets.PrxPressButton()
        self._bottom_prx_tool_bar.add_widget(self._apply_and_close_prx_button)
        self._apply_and_close_prx_button.set_name(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._configure.get('build.register.buttons.apply_and_close')
            )
        )
        self._apply_and_close_prx_button.connect_press_clicked_to(
            self.apply_and_close_fnc
        )

        self._apply_prx_button = gui_prx_widgets.PrxPressButton()
        self._bottom_prx_tool_bar.add_widget(self._apply_prx_button)
        self._apply_prx_button.set_name(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._configure.get('build.register.buttons.apply')
            )
        )
        self._apply_prx_button.connect_press_clicked_to(
            self.apply_fnc
        )

        self._close_prx_button = gui_prx_widgets.PrxPressButton()
        self._bottom_prx_tool_bar.add_widget(self._close_prx_button)
        self._close_prx_button.set_name(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._configure.get('build.register.buttons.close')
            )
        )
        self._close_prx_button.connect_press_clicked_to(
            self.close_fnc
        )

        self.do_gui_refresh_all()

        self._page_prx_tab_tool_box.connect_current_changed_to(
            self.do_gui_refresh_all
        )
        self._page_prx_tab_tool_box.set_history_key('lazy-resource-tool.page_key_current')
        self._page_prx_tab_tool_box.load_history()
        # for load
        self._window.connect_window_activate_changed_to(self.do_gui_refresh_for_load)

        self._window.register_window_close_method(self.gui_close_fnc)

    def gui_close_fnc(self):
        self._page_prx_tab_tool_box.save_history()

    def do_gui_refresh_for_load(self):
        if self._page_prx_tab_tool_box.get_current_key() == self.TabKeys.Load:
            self._load_prx_page.do_gui_refresh_all()

    def do_gui_refresh_all(self):
        if self._page_prx_tab_tool_box.get_current_key() == self.TabKeys.Register:
            self._register_prx_page.do_gui_refresh_all()
        elif self._page_prx_tab_tool_box.get_current_key() == self.TabKeys.Load:
            self._load_prx_page.do_gui_refresh_all()

