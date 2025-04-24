# coding:utf-8
import functools

import lxbasic.content as bsc_content

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_screw.scripts as lnx_scr_scripts


class AbsPrxResoraPanel(gui_prx_widgets.PrxBasePanel):
    CONFIGURE_KEY = 'resora/gui/main'

    KEY_PAGE_KEYS = 'resora.page_keys'
    KEY_PAGE_KEY_CURRENT = 'resora.page_key_current'

    def _gui_tab_add_menu_content_generate_fnc(self):
        content = bsc_content.Dict()
        data = lnx_scr_scripts.ManifestStageOpt().get_all_page_data()
        for k, v in data.items():
            i_key = k
            if i_key not in self._tag_page_key_opened:
                i_type_name = v['type']['name']
                i_node_name = v['node']['name']
                if self._window._language == 'chs':
                    i_type_gui_name = v['type']['gui_name_chs']
                    i_node_gui_name = v['node']['gui_name_chs']
                else:
                    i_type_gui_name = v['type']['gui_name']
                    i_node_gui_name = v['node']['gui_name']

                if 'type_group' in v:
                    i_type_group_name = v['type_group']['name']
                    if self._window._language == 'chs':
                        i_type_group_gui_name = v['type_group']['gui_name_chs']
                    else:
                        i_type_group_gui_name = v['type_group']['gui_name']

                    i_type_group_path = u'/{}'.format(i_type_group_name)
                    content.set(
                        u'{}.properties.type'.format(i_type_group_path), 'group'
                    )
                    content.set(
                        u'{}.properties.name'.format(i_type_group_path), i_type_group_gui_name
                    )
                    content.set(
                        u'{}.properties.icon_name'.format(i_type_group_path), 'database/group'
                    )

                i_type_path = u'/{}'.format(i_type_name)

                content.set(
                    u'{}.properties.type'.format(i_type_path), 'group'
                )
                content.set(
                    u'{}.properties.name'.format(i_type_path), i_type_gui_name
                )
                content.set(
                    u'{}.properties.icon_name'.format(i_type_path), 'database/group'
                )

                i_path = u'{}/{}'.format(i_type_path, i_node_name)

                content.set(
                    u'{}.properties.type'.format(i_path), 'action'
                )
                content.set(
                    u'{}.properties.name'.format(i_path), i_node_gui_name
                )
                content.set(
                    u'{}.properties.icon_name'.format(i_path), 'tag'
                )
                content.set(
                    u'{}.properties.execute_fnc'.format(i_path),
                    functools.partial(
                        self._gui_tab_add_page_fnc, i_key, True
                    )
                )
        return content

    def _gui_tab_add_page_fnc(self, key, switch_to):
        self._tag_page_key_opened.add(key)
        self._gui_tab_add_page(key, switch_to=switch_to)

    def _gui_page_delete_pre_fnc(self, key):
        page = self._tab_tab_widget_dict.pop(key)
        self._tag_page_key_opened.remove(key)
        return page.gui_close_fnc()

    def _gui_tab_add_page(self, key, switch_to=False):
        if key in self._tab_tab_widget_dict:
            self._prx_tab_view.set_current_by_key(key)
            return

        prx_sca = gui_prx_widgets.PrxVScrollArea()

        page_data = lnx_scr_scripts.ManifestStageOpt().get_page_data(key)

        if self._window._language == 'chs':
            name = page_data['gui_name_chs']
        else:
            name = page_data['gui_name']

        self._prx_tab_view.add_widget(
            prx_sca,
            key=key,
            name=name,
            icon_name_text=key,
            tool_tip='...',
            switch_to=switch_to
        )
        prx_page = self.gui_generate_page_for('manager')
        self._tab_tab_widget_dict[key] = prx_page
        
        self._prx_tab_view.register_page_delete_pre_fnc(key, self._gui_page_delete_pre_fnc)

        prx_page.do_gui_page_initialize(key)
        prx_sca.add_widget(prx_page)

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxResoraPanel, self).__init__(window, session, *args, **kwargs)

    def gui_close_fnc(self):
        page_keys = self._prx_tab_view.get_all_page_keys()
        gui_core.GuiHistoryStage().set_array(self.KEY_PAGE_KEYS, page_keys)
        gui_core.GuiHistoryStage().set_one(self.KEY_PAGE_KEY_CURRENT, self._prx_tab_view.get_current_key())

    def gui_setup_fnc(self):
        self.set_main_style_mode(1)

        self._prx_tab_view = gui_prx_widgets.PrxTabView()
        self.add_widget(self._prx_tab_view)

        self._prx_tab_view.set_drag_enable(True)
        self._prx_tab_view.set_add_enable(True)

        self._tag_page_key_opened = set()
        self._all_scr_stage_keys = lnx_scr_scripts.ManifestStageOpt().get_valid_database_names()

        self._tab_tab_widget_dict = {}

        self._prx_tab_view.set_add_menu_content_generate_fnc(self._gui_tab_add_menu_content_generate_fnc)
        self._prx_tab_view.set_history_key(
            [self._window.GUI_KEY, '{}.page'.format(self._gui_path)]
        )
        
        tab_keys = gui_core.GuiHistoryStage().get_array(self.KEY_PAGE_KEYS)
        tab_key_current = gui_core.GuiHistoryStage().get_one(self.KEY_PAGE_KEY_CURRENT)
        page_keys = self._all_scr_stage_keys
        if tab_keys:
            _ = [x for x in tab_keys if x in self._all_scr_stage_keys]
            if _:
                page_keys = _
        else:
            page_keys = ['resource_manifest']

        c = len(page_keys[:5])

        for i_page_key in page_keys[:5]:
            self._gui_tab_add_page_fnc(i_page_key, i_page_key==tab_key_current)

        self.connect_refresh_action_for(self.do_gui_refresh_all)
        self.register_window_close_method(self.gui_close_fnc)

    def do_gui_refresh_all(self):
        key = self._prx_tab_view.get_current_key()
        if key in self._tab_tab_widget_dict:
            self._tab_tab_widget_dict[key].do_gui_refresh_all()

    def gui_get_current_page(self):
        return self._tab_tab_widget_dict[self._prx_tab_view.get_current_key()]
