# coding:utf-8
import functools

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_lazy.screw.core as qsm_lzy_scr_core


class AbsPrxPanelForResourceManager(gui_prx_widgets.PrxBasePanel):
    CONFIGURE_KEY = 'lazy-resource/gui/manager'

    KEY_TAB_KEYS = 'lazy-resource-manager.page_keys'
    HST_TAB_KEY_CURRENT = 'lazy-resource-manager.page_key_current'
    
    def _gui_tab_add_menu_gain_fnc(self):
        lst = []
        for i_key in qsm_lzy_scr_core.Stage.get_all_keys():
            if i_key not in self._tag_page_key_opened:
                i_configure = qsm_lzy_scr_core.Stage.get_configure(i_key)
                if self._window._language == 'chs':
                    i_name = i_configure.get('options.gui_name_chs')
                else:
                    i_name = i_configure.get('options.gui_name')

                lst.append(
                    (
                        i_name,
                        'tag',
                        functools.partial(
                            self._gui_tab_add_page_fnc, i_key, True
                        )
                    )
                )
        return lst
    
    def _gui_tab_add_page_fnc(self, key, switch_to):
        self._tag_page_key_opened.add(key)
        self._gui_tab_add_page(key, switch_to=switch_to)

    def _gui_page_delete_pre_fnc(self, key):
        page = self._tab_page_dict.pop(key)
        self._tag_page_key_opened.remove(key)
        return page.gui_close_fnc()

    def _gui_tab_add_page(self, key, switch_to=False):
        prx_sca = gui_prx_widgets.PrxVScrollArea()
        configure = qsm_lzy_scr_core.Stage.get_configure(key)
        if self._window._language == 'chs':
            name = configure.get('options.gui_name_chs')
        else:
            name = configure.get('options.gui_name')

        self._prx_tab_view.add_widget(
            prx_sca,
            key=key,
            name=name,
            icon_name_text=key,
            tool_tip='...',
            switch_to=switch_to
        )
        prx_page = self.generate_page_for('manager')
        self._tab_page_dict[key] = prx_page
        
        self._prx_tab_view.register_page_delete_pre_fnc(key, self._gui_page_delete_pre_fnc)

        prx_page.do_gui_page_initialize(key)
        prx_sca.add_widget(prx_page)

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPanelForResourceManager, self).__init__(window, session, *args, **kwargs)

    def gui_close_fnc(self):
        page_keys = self._prx_tab_view.get_all_page_keys()
        gui_core.GuiHistory.set_one(self.KEY_TAB_KEYS, page_keys)

        page_key_current = self._prx_tab_view.get_current_key()
        gui_core.GuiHistory.set_one(self.HST_TAB_KEY_CURRENT, page_key_current)

    def gui_setup_fnc(self):
        self.set_main_style_mode(1)

        self._prx_tab_view = gui_prx_widgets.PrxTabView()
        self.add_widget(self._prx_tab_view)
        self._prx_tab_view.set_drag_enable(True)
        self._prx_tab_view.set_add_enable(True)

        self._tag_page_key_opened = set()
        self._all_scr_stage_keys = qsm_lzy_scr_core.Stage.get_all_keys()

        self._tab_page_dict = {}

        self._prx_tab_view.set_add_menu_data_gain_fnc(self._gui_tab_add_menu_gain_fnc)

        history_tag_keys = gui_core.GuiHistory.get_one(self.KEY_TAB_KEYS)
        page_keys = self._all_scr_stage_keys
        if history_tag_keys:
            _ = [x for x in history_tag_keys if x in self._all_scr_stage_keys]
            if _:
                page_keys = _

        self._gui_tab_add_page_fnc(page_keys[0], False)

        self.connect_refresh_action_for(self.do_gui_refresh_all)
        self.register_window_close_method(self.gui_close_fnc)

    def do_gui_refresh_all(self):
        key = self._prx_tab_view.get_current_key()
        if key in self._tab_page_dict:
            self._tab_page_dict[key].do_gui_refresh_all()

    def gui_get_current_page(self):
        return self._tab_page_dict[self._prx_tab_view.get_current_key()]
