# coding:utf-8
import functools

import lxbasic.core as bsc_core

import lxbasic.scan as bsc_scan

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.qt.view_widgets as gui_qt_vew_widgets


class AbsPrxPanelForWorkspace(gui_prx_widgets.PrxBasePanel):
    CONFIGURE_KEY = 'lazy-workspace/gui/main'

    GUI_KEY = 'lazy-workspace'

    RESOURCE_BRANCH = None

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPanelForWorkspace, self).__init__(window, session, *args, **kwargs)

    def gui_setup_fnc(self):
        self._page_prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._page_prx_tab_tool_box)

        self.gui_setup_pages_for(['task_manager', 'task_tool', 'task_release'])

        self._page_prx_tab_tool_box.set_history_key('lazy-workspace.{}-page'.format(self.RESOURCE_BRANCH))
        self._page_prx_tab_tool_box.load_history()

        self.register_window_close_method(
            self.gui_close_fnc
        )

        self._page_prx_tab_tool_box.connect_current_changed_to(
            self.do_gui_refresh_all
        )

        self.do_gui_refresh_all()

    def gui_setup_post_fnc(self):
        for k, v in self._page_dict.items():
            v.gui_setup_post_fnc()

    def gui_close_fnc(self):
        self._page_prx_tab_tool_box.save_history()

    def gui_setup_pages_for(self, page_keys):
        self._page_dict = {}

        for i_page_key in page_keys:
            if i_page_key not in self._page_class_dict:
                continue

            i_prx_sca = gui_prx_widgets.PrxVScrollArea()

            self._page_prx_tab_tool_box.add_widget(
                i_prx_sca,
                key=i_page_key,
                name=gui_core.GuiUtil.choice_name(
                    self._language, self._window._configure.get('build.{}'.format(i_page_key))
                ),
                icon_name_text=i_page_key,
                tool_tip=gui_core.GuiUtil.choice_tool_tip(
                    self._language, self._window._configure.get('build.{}'.format(i_page_key))
                )
            )

            i_prx_page = self._window.gui_generate_page_for(i_page_key)
            self._page_dict[i_page_key] = i_prx_page
            i_prx_sca.add_widget(i_prx_page)

    def do_gui_refresh_all(self):
        page = self.gui_find_page(self._page_prx_tab_tool_box.get_current_key())
        if page is not None:
            page.do_gui_refresh_all()
