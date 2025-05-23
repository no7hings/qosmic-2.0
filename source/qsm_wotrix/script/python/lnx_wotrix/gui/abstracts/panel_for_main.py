# coding:utf-8
import lxgui.core as gui_core

import lxgui.qt.widgets.entity as gui_qt_wgt_entity

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_parsor.swap as lnx_prs_swap


class AbsPrxWotrixTool(gui_prx_widgets.PrxBasePanel):
    CONFIGURE_KEY = 'wotrix/gui/main'

    GUI_KEY = 'wotrix'

    RESOURCE_TYPE = None

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxWotrixTool, self).__init__(window, session, *args, **kwargs)

    def gui_setup_fnc(self):
        self._prs_root = lnx_prs_swap.Swap.generate_root()

        self._page_prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()

        self.add_widget(self._page_prx_tab_tool_box)

        self._account = gui_qt_wgt_entity.QtAccountWidget()
        self.add_widget(self._account)
        self._account._model.load_entity(self._prs_root.current_user())

        self.gui_setup_pages_for(
            [
                'task_overview', 'task_manager', 'task_tracker',
                'task_tool', 'task_release'
            ]
        )

        self._page_prx_tab_tool_box.set_history_key(
            [self._window.GUI_KEY, '{}.page'.format(self._gui_path)]
        )
        self._page_prx_tab_tool_box.load_history()

        self.register_window_close_method(
            self.gui_close_fnc
        )

        self._page_prx_tab_tool_box.connect_current_changed_to(
            self.do_gui_refresh_all
        )

        self.do_gui_refresh_all()

    def gui_setup_post_fnc(self):
        for k, v in self._tab_widget_dict.items():
            v.gui_setup_post_fnc()

    def gui_close_fnc(self):
        pass

    def gui_setup_pages_for(self, page_keys):
        self._tab_widget_dict = {}

        for i_page_key in page_keys:
            if i_page_key not in self._page_class_dict:
                continue

            i_prx_sca = gui_prx_widgets.PrxVScrollArea()

            self._page_prx_tab_tool_box.add_widget(
                i_prx_sca,
                key=i_page_key,
                name=gui_core.GuiUtil.choice_gui_name(
                    self._language, self._window._configure.get('build.{}'.format(i_page_key))
                ),
                icon_name_text=i_page_key,
                tool_tip=gui_core.GuiUtil.choice_gui_tool_tip(
                    self._language, self._window._configure.get('build.{}'.format(i_page_key))
                )
            )

            i_prx_page = self._window.gui_generate_page_for(i_page_key)
            self._tab_widget_dict[i_page_key] = i_prx_page
            i_prx_sca.add_widget(i_prx_page)

    def do_gui_refresh_all(self):
        page = self.gui_find_page(self._page_prx_tab_tool_box.get_current_key())
        if page is not None:
            page.do_gui_refresh_all()

    def gui_set_current_page(self, key):
        result = self._page_prx_tab_tool_box.set_current_key(key)
        if result is True:
            return self._tab_widget_dict[key]
