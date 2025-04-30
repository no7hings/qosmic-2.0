# coding:utf-8
import os

import functools

import lxbasic.content as bsc_content

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets
# kit
from ... import core as kit_core


class _GuiPageQuery(object):
    def __init__(self, window_proxy):
        self.__window_proxy = window_proxy

        self.restore()

    def restore(self):
        self.__all_page_keys_default = kit_core.KitDesktopHook.DEFAULT_PAGE_KEYS
        self.__page_keys_default = []

        self.__all_page_keys_department = kit_core.KitDesktopHook.find_all_page_keys_at(
            kit_core.KitDesktopHook.PageKey.Departments
        )
        self.__page_keys_department = []

        self.__user_current = bsc_core.BscSystem.get_user_name()
        self.__all_page_keys_user = kit_core.KitDesktopHook.find_all_page_keys_at(
            kit_core.KitDesktopHook.PageKey.Users
        )
        if self.__user_current not in self.__all_page_keys_user:
            self.__all_page_keys_user.append(self.__user_current)
        self.__page_keys_user = []

        self.__all_page_keys = self.__all_page_keys_default+self.__all_page_keys_department+self.__all_page_keys_user

        self.__page_keys = self.__all_page_keys_default+[kit_core.KitDesktopHook.get_current_user_group_key()]

    def key_is_user(self, page_key):
        return page_key in self.__all_page_keys_user

    def push_to_using(self, page_key):
        if page_key in self.__all_page_keys_default:
            self.__page_keys_default.append(page_key)
        elif page_key in self.__all_page_keys_department:
            self.__page_keys_department.append(page_key)
        elif page_key in self.__all_page_keys_user:
            self.__page_keys_user.append(page_key)

    def pull_from_using(self, page_key):
        if page_key in self.__page_keys_default:
            self.__page_keys_default.remove(page_key)
        elif page_key in self.__page_keys_department:
            self.__page_keys_department.remove(page_key)
        elif page_key in self.__page_keys_user:
            self.__page_keys_user.remove(page_key)

    def get_defaults_waiting(self):
        return [i for i in self.__all_page_keys_default if i not in self.__page_keys_default]

    def get_departments_waiting(self):
        return [i for i in self.__all_page_keys_department if i not in self.__page_keys_department]

    def get_users_waiting(self):
        return [i for i in self.__all_page_keys_user if i not in self.__page_keys_user]

    def get_all_keys(self):
        return self.__all_page_keys

    def get_all_filterable_keys(self):
        return self.__all_page_keys_default+self.__all_page_keys_department+[kit_core.KitDesktopHook.get_current_user_group_key()]

    def get_all_using_keys(self):
        return self.__page_keys_default+self.__page_keys_department+self.__page_keys_user

    def get_placeholder_keys(self):
        return self.__page_keys

    @classmethod
    def get_current_user_key(cls):
        return kit_core.KitDesktopHook.get_current_user_group_key()


class _GuiQuery(object):
    def __init__(self, window_proxy):
        self.__window_proxy = window_proxy

        self.restore()

    def restore(self):
        self.__dict = {}
        self.__tool_name_dict = {}

    def register(self, key, value):
        self.__dict[key] = value

    def register_tool_name(self, page_name, group_sub_name, name, tool_key):
        p = u'/{}/{}/{}'.format(page_name, group_sub_name, name)
        self.__tool_name_dict.setdefault(
            p, set()
        ).add(tool_key)
        return len(self.__tool_name_dict[p])-1

    def get(self, key):
        return self.__dict[key]

    def delete(self, key):
        self.__dict.pop(key)

    def get_is_exists(self, key):
        return key in self.__dict

    def delete_all_below(self, key):
        all_keys = self.__dict.keys()
        keys = bsc_content.ContentUtil.filter(
            all_keys, '{}/*'.format(key)
        ) or []
        for i in keys:
            self.__dict.pop(i)

        all_keys = self.__tool_name_dict.keys()
        keys = bsc_content.ContentUtil.filter(
            all_keys, '{}/*'.format(key)
        )
        for i in keys:
            self.__tool_name_dict.pop(i)

    def get_tool_group_layout(self, page_name):
        return self.__dict.get(u'/{}'.format(page_name))


# noinspection PyUnusedLocal
class AbsToolKitForDesktop(gui_prx_widgets.PrxSessionWindow):
    KEY_TAB_KEYS = 'tool-desktop.page_keys'
    HST_TAB_KEY_CURRENT = 'tool-desktop.page_key_current'

    KEY_TOOL_GROUP_ORDER = 'tool-desktop.tool_group_order'
    KEY_TOOL_ORDER = 'tool-desktop.tool_order'

    LOG_KEY = 'desktop kit'

    def __init__(self, *args, **kwargs):
        super(AbsToolKitForDesktop, self).__init__(*args, **kwargs)

        kit_core.KitDesktopHook.check_is_valid(self.widget)

    @staticmethod
    def _show_environ_fnc():
        gui_core.GuiDialog.create(
            'environ',
            content='\n'.join(
                ['{} = {}'.format(k, v) for k, v in bsc_core.DictMtd.sort_key_to(os.environ).items()]
            ),
            window_size=(960, 480),
            ok_visible=False,
            no_visible=False,
            cancel_label='Close'
        )

    def __close_fnc(self):
        page_keys = self._prx_tab_view.get_all_page_keys()
        gui_core.GuiHistoryStage().set_one(self.KEY_TAB_KEYS, page_keys)

        page_key_current = self._prx_tab_view.get_current_key()
        gui_core.GuiHistoryStage().set_one(self.HST_TAB_KEY_CURRENT, page_key_current)

        tool_group_order_dict = gui_core.GuiHistoryStage().get_one(self.KEY_TOOL_GROUP_ORDER) or {}
        for i_page_key in page_keys:
            i_tool_group_layout = self.__gui_query.get_tool_group_layout(i_page_key)
            i_tool_group_names = i_tool_group_layout._get_all_widget_name_texts_()
            tool_group_order_dict[i_page_key] = i_tool_group_names

        gui_core.GuiHistoryStage().set_one(self.KEY_TOOL_GROUP_ORDER, tool_group_order_dict)

    def restore_variants(self):
        self._gui_page_query = _GuiPageQuery(self)
        self.__gui_query = _GuiQuery(self)

        self.__hook_dict = {}
        self.__option_hook_dict = {}

        self.__page_name_mapper = self._session.configure.get('build.page_name_mapper') or {}

    def gui_setup_fnc(self):
        menu = self.create_menu('extra')
        menu.set_menu_data(
            [
                ('show environ', None, self._show_environ_fnc),
            ]
        )

        self.set_main_style_mode(1)
        self._prx_tab_view = gui_prx_widgets.PrxTabView()
        self.add_widget(self._prx_tab_view)
        self._prx_tab_view.set_drag_enable(True)
        self._prx_tab_view.set_add_enable(True)
        self._prx_tab_view.set_add_menu_data_generate_fnc(self._gui_tab_add_menu_data_generate_fnc)
        self._prx_tab_view.connect_delete_post_accepted_to(self._gui_tab_page_delete_fnc)

        self.__bubbles_filter = qt_widgets.QtBubbleAsChoice(self._qt_widget)
        self.__bubbles_filter._setup_()
        self.create_window_action_for(self.__bubbles_filter._start_, 'tab')

        self.__gui_build_create_layer()
        self.__gui_build_modify_layer()
        self.__gui_build_copy_layer()
        self.gui_build_filter()

        self.do_gui_refresh_all()

        self._prx_tab_view.set_current_by_key(
            gui_core.GuiHistoryStage().get_one(self.HST_TAB_KEY_CURRENT)
        )

        self.connect_refresh_action_for(
            self.refresh_current_group
        )

        self.register_window_close_method(self.__close_fnc)

        bsc_log.Log.trace_method_result(
            self.LOG_KEY, 'is ready'
        )

    def gui_build_filter(self):
        all_tool_keys = []
        page_keys = self._gui_page_query.get_all_filterable_keys()
        for i_page_key in page_keys:
            i_tool_keys = kit_core.KitDesktopHook.find_all_tool_keys_at(i_page_key)
            all_tool_keys.extend(i_tool_keys)

        all_tool_keys.sort()

        self.__bubbles_filter._set_texts_(
            all_tool_keys
        )

        self.__bubbles_filter.choice_text_accepted.connect(self.gui_execute_tool)

    def gui_execute_tool(self, tool_key):
        args = kit_core.KitDesktopHook.get_args(tool_key)
        if args:
            _, execute_fnc = args
            self.__debug_run(execute_fnc)

    def _gui_tab_add_menu_data_generate_fnc(self):
        list_ = []
        # default

        for i_page_key in self._gui_page_query.get_defaults_waiting():
            list_.append(
                (
                    i_page_key, 'tag', functools.partial(
                        self._gui_tab_add_page_fnc, i_page_key, True
                    )
                )
            )
        if list_:
            list_.append(())
        # department
        sub_list = []
        for i_page_key in self._gui_page_query.get_departments_waiting():
            i_name = i_page_key.split('/')[-1]
            sub_list.append(
                (
                    i_name, 'tag', functools.partial(
                        self._gui_tab_add_page_fnc, i_page_key, True
                    )
                )
            )
        list_.append(
            [
                kit_core.KitDesktopHook.PageKey.Departments, 'file/folder',
                sub_list
            ]
        )
        # user
        sub_list = []
        for i_page_key in self._gui_page_query.get_users_waiting():
            i_name = i_page_key.split('/')[-1]
            sub_list.append(
                (
                    i_name, 'user', functools.partial(
                        self._gui_tab_add_page_fnc, i_page_key, True
                    )
                )
            )

        list_.append(
            [
                kit_core.KitDesktopHook.PageKey.Users, 'file/folder',
                sub_list
            ]
        )
        return list_

    def __gui_build_create_layer(self):
        layer_widget = self.create_layer_widget('create_layer', 'Create')
        s = gui_prx_widgets.PrxVScrollArea()
        layer_widget.add_widget(s)
        self._create_option_prx_node = gui_prx_widgets.PrxOptionsNode('options')
        self._create_option_prx_node.build_by_data(
            self._session.configure.get('build.node.create_options')
        )
        s.add_widget(self._create_option_prx_node.widget)

        text_browser = gui_prx_widgets.PrxTextBrowser()
        s.add_widget(text_browser)
        text_browser.set_content(
            self._session.configure.get('build.node.create_content')
        )
        text_browser.set_font_size(12)
        #
        tool_bar = gui_prx_widgets.PrxHToolbar()
        layer_widget.add_widget(tool_bar.widget)
        tool_bar.set_expanded(True)
        button = gui_prx_widgets.PrxPressButton()
        tool_bar.add_widget(button)
        button.set_name('Apply')
        button.connect_press_clicked_to(
            self.__create_layer_apply_fnc
        )

    def __gui_build_modify_layer(self):
        layer_widget = self.create_layer_widget('modify_layer', 'Modify')
        s = gui_prx_widgets.PrxVScrollArea()
        layer_widget.add_widget(s)
        self._modify_option_prx_node = gui_prx_widgets.PrxOptionsNode('options')
        self._modify_option_prx_node.build_by_data(
            self._session.configure.get('build.node.modify_options'),
        )
        s.add_widget(self._modify_option_prx_node.widget)

        text_browser = gui_prx_widgets.PrxTextBrowser()
        s.add_widget(text_browser)
        text_browser.set_content(
            self._session.configure.get('build.node.modify_content')
        )
        text_browser.set_font_size(12)
        #
        tool_bar = gui_prx_widgets.PrxHToolbar()
        layer_widget.add_widget(tool_bar.widget)
        tool_bar.set_expanded(True)
        button = gui_prx_widgets.PrxPressButton()
        tool_bar.add_widget(button)
        button.set_name('Apply')
        button.connect_press_clicked_to(
            self.__modify_layer_apply_fnc
        )

    def __gui_build_copy_layer(self):
        layer_widget = self.create_layer_widget('copy_layer', 'Copy')
        s = gui_prx_widgets.PrxVScrollArea()
        layer_widget.add_widget(s)
        self._copy_option_prx_node = gui_prx_widgets.PrxOptionsNode('options')
        self._copy_option_prx_node.build_by_data(
            self._session.configure.get('build.node.copy_options'),
        )
        s.add_widget(self._copy_option_prx_node.widget)

        text_browser = gui_prx_widgets.PrxTextBrowser()
        s.add_widget(text_browser)
        text_browser.set_content(
            self._session.configure.get('build.node.copy_content')
        )
        text_browser.set_font_size(12)
        #
        tool_bar = gui_prx_widgets.PrxHToolbar()
        layer_widget.add_widget(tool_bar.widget)
        tool_bar.set_expanded(True)
        button = gui_prx_widgets.PrxPressButton()
        tool_bar.add_widget(button)
        button.set_name('Apply')
        button.connect_press_clicked_to(
            self.__copy_layer_apply_fnc
        )

    def __create_layer_apply_fnc(self):
        options = self._create_option_prx_node.to_dict()
        kit_core.KitDesktopHookAddOpt(
            self,
            self._session,
            options
        ).accept_create(mode='create')

    def __modify_layer_apply_fnc(self):
        options = self._modify_option_prx_node.to_dict()
        kit_core.KitDesktopHookAddOpt(
            self,
            self._session,
            options
        ).accept_create(mode='modify')

    def __copy_layer_apply_fnc(self):
        options = self._copy_option_prx_node.to_dict()
        kit_core.KitDesktopHookAddOpt(
            self,
            self._session,
            options
        ).accept_create(mode='create')

    def __save_main_icon_to_file(self, page_name, group_sub_name, session):
        tool_path = u'/{}/{}/{}'.format(
            page_name, group_sub_name, bsc_core.BscUuid.generate_by_text(session.get_hook())
        )
        if self.__gui_query.get_is_exists(tool_path):
            tool = self.__gui_query.get(tool_path)
            f = gui_core.GuiStorageDialog.save_file(
                ext_filter='All File (*.png)',
                parent=self._qt_widget
            )
            if f:
                tool.save_main_icon_to_file(f)

    def do_gui_refresh_all(self):
        self.__hook_dict = {}
        self.__option_hook_dict = {}

        ms = [
            #
            (self.gui_cache, ()),
            (self.gui_build, ()),
        ]
        with self.gui_bustling():
            for i_m, i_as in ms:
                if i_as:
                    i_m(*i_as)
                else:
                    i_m()

        self.gui_sort_all_tool_group_order()

    @classmethod
    def get_group_args(cls, session, **kwargs):
        gui_configure = session.gui_configure
        page_name = gui_configure.get('group_name')
        group_sub_name = gui_configure.get('group_sub_name') or 'Tool'
        if 'gui_parent' in kwargs:
            gui_path = kwargs.get('gui_parent')
            gui_path_opts = bsc_core.BscNodePathOpt(gui_path).get_components()
            page_opt = gui_path_opts[1]
            page_name = page_opt.get_name()
            group_sub_opt = gui_path_opts[0]
            group_sub_name = group_sub_opt.get_name()
        #
        if 'page_name' in kwargs:
            page_name = kwargs['page_name']
        #
        if 'group_sub_name' in kwargs:
            group_sub_name = kwargs['group_sub_name']
        #
        gui_configure.set('group_name', page_name)
        gui_configure.set('group_sub_name', group_sub_name)
        return page_name, group_sub_name

    def gui_get_group_args(self, page_name, tool_data=None, switch_to=False):
        gui_path = u'/{}'.format(page_name)
        if self.__gui_query.get_is_exists(gui_path) is True:
            return self.__gui_query.get(gui_path)

        scroll_area = gui_prx_widgets.PrxVScrollArea()

        name = page_name.split('/')[-1]
        if name in self.__page_name_mapper:
            name = self.__page_name_mapper[page_name]

        self._prx_tab_view.add_widget(
            scroll_area,
            key=page_name,
            name=name,
            icon_name_text=name,
            switch_to=switch_to
        )

        w_0 = qt_widgets.QtWidget()
        scroll_area.add_widget(w_0)
        l_0 = qt_widgets.QtVBoxLayout(w_0)
        l_0.setContentsMargins(0, 0, 0, 0)

        top_tool_bar = gui_prx_widgets.PrxHToolbar()
        l_0.addWidget(top_tool_bar._qt_widget)
        top_tool_bar.set_expanded(True)
        top_tool_bar.set_align_left()

        if tool_data:
            tool_box = gui_prx_widgets.PrxHToolbox()
            top_tool_bar.add_widget(tool_box)
            tool_box.set_expanded(True)
            for i_data in tool_data:
                i_name, i_icon_name, i_tool_tip, i_fnc = i_data
                i_tool = gui_prx_widgets.PrxIconPressButton()
                tool_box.add_widget(i_tool)
                i_tool.set_name(i_name)
                i_tool.set_icon_name(i_icon_name)
                i_tool.set_tool_tip(i_tool_tip, action_tip='"LMB-click" to execute')
                i_tool.connect_press_clicked_to(i_fnc)

        w_1 = qt_widgets.QtWidget()
        l_0.addWidget(w_1)

        tool_group_layout_widget = qt_widgets.QtToolGroupVLayoutWidget()
        l_0.addWidget(tool_group_layout_widget)
        tool_group_layout_widget._set_drop_enable_(True)
        # tool_group_layout_widget.setContentsMargins(0, 0, 0, 0)
        self.__gui_query.register(gui_path, tool_group_layout_widget)
        return tool_group_layout_widget

    def gui_get_view_args(self, page_name=None, group_sub_name=None, tool_data=None, group_name_over=None):
        tool_group_layout_widget = self.gui_get_group_args(page_name, tool_data=tool_data)
        gui_path = u'/{}/{}'.format(page_name, group_sub_name)
        if self.__gui_query.get_is_exists(gui_path) is True:
            qt_tool_group, grid_layout_widget = self.__gui_query.get(gui_path)
        else:
            qt_tool_group = qt_widgets.QtHToolGroupStyleB()
            tool_group_layout_widget._add_widget_(qt_tool_group)
            qt_tool_group._set_name_text_(group_sub_name)
            qt_tool_group._set_expanded_(True)
            qt_tool_group._set_drag_enable_(True)

            grid_layout_widget = gui_prx_widgets.PrxToolGridLayoutWidget()
            qt_tool_group._add_widget_(grid_layout_widget._qt_widget)
            grid_layout_widget.set_drop_enable(True)
            grid_layout_widget.set_path(gui_path)
            grid_layout_widget.set_drag_and_drop_scheme('tool-desktop-tool')
            self.__gui_query.register(gui_path, (qt_tool_group, grid_layout_widget))
            grid_layout_widget.set_item_size(*self.session.gui_configure.get('item_frame_size'))
        return grid_layout_widget

    def gui_cache(self):
        pass

    def gui_cache_for_builtin(self):
        pass

    def gui_cache_hook(self, hook_args, **kwargs):
        session, _ = hook_args
        page_name, group_sub_name = self.get_group_args(
            session, **kwargs
        )
        self.__hook_dict.setdefault(
            page_name, []
        ).append(
            (hook_args, page_name, group_sub_name)
        )

    def gui_cache_option_hook(self, hook_args, **kwargs):
        session, _ = hook_args
        page_name, group_sub_name = self.get_group_args(
            session, **kwargs
        )
        self.__option_hook_dict.setdefault(
            page_name, []
        ).append(
            (hook_args, page_name, group_sub_name)
        )

    def gui_build_all_for_builtin(self):
        for _, i_v in self.__hook_dict.items():
            for j in i_v:
                j_hook_args, j_group_name, j_group_sub_name = j
                self.add_tool(
                    j_hook_args, j_group_name, j_group_sub_name
                )
        for _, i_v in self.__option_hook_dict.items():
            for j in i_v:
                j_hook_args, j_group_name, j_group_sub_name = j
                self.add_option_tool(
                    j_hook_args, j_group_name, j_group_sub_name
                )

    def gui_sort_all_tool_group_order(self):
        for i in self._prx_tab_view.get_all_page_keys():
            self.gui_sort_tool_group_order_at(i)

    def gui_sort_tool_group_order_at(self, page_name):
        names = gui_core.GuiHistoryStage().get_one(u'{}.{}'.format(self.KEY_TOOL_GROUP_ORDER, page_name)) or []
        if names:
            tool_group_layout = self.__gui_query.get_tool_group_layout(page_name)
            tool_group_layout._sort_widgets_by_name_texts_(names)

    def gui_build(self):
        # self.gui_build_all_for_builtin()
        self.gui_build_all_for_customize()

    def gui_build_all_for_customize(self):
        page_keys = self._gui_page_query.get_placeholder_keys()

        history_tag_keys = gui_core.GuiHistoryStage().get_one(self.KEY_TAB_KEYS)
        if history_tag_keys:
            page_keys = [i for i in history_tag_keys if i in self._gui_page_query.get_all_keys()]

        with self.gui_bustling():
            for i_page_key in page_keys:
                self._gui_page_query.push_to_using(i_page_key)

                self.gui_add_customize_for_page(i_page_key)

    def gui_add_customize_for_page(self, page_name, switch_to=False):
        self.gui_get_group_args(
            page_name,
            tool_data=[
                (
                    'create new', 'file/add-file', 'create new tool for "{}"'.format(page_name),
                    functools.partial(self.gui_action_create_fnc, page_name)
                ),
            ],
            switch_to=switch_to
        )

        tool_keys = kit_core.KitDesktopHook.find_all_tool_keys_at(page_name)
        for i_tool_key in tool_keys:
            self.gui_add_one_for_customize(i_tool_key, page_name)

    def gui_add_one_for_customize(self, hook_key, page_name):
        hook_args = kit_core.KitDesktopHook.get_args(hook_key)
        if hook_args:
            session, _ = hook_args
            # override page name
            page_name, group_sub_name = self.get_group_args(
                session, page_name=page_name
            )
            self.add_tool(
                hook_args,
                page_name, group_sub_name,
                menu_data=[
                    ('modify', 'file/file', functools.partial(self.gui_action_modify_fnc, session)),
                    ('copy to', 'copy', functools.partial(self.gui_action_copy_fnc, session)),
                    (),
                    ('open folder', 'file/open-folder', session.open_configure_directory),
                    (),
                    # todo: may be not useful now
                    (
                        'save main icon to file', 'file/file', functools.partial(
                            self.__save_main_icon_to_file, page_name, group_sub_name, session
                        )
                    )
                ]
            )

    def __show_no_execute_permission_dialog(self, page_name):
        gui_core.GuiDialog.create(
            self._session.gui_name,
            content='you are no permission for page "{}"'.format(page_name),
            status=gui_core.GuiDialog.ValidationStatus.Warning,
            ok_visible=False,
            no_visible=False,
        )
        return False

    def __show_no_edit_permission_dialog(self, page_name):
        gui_core.GuiDialog.create(
            self._session.gui_name,
            content='you are no editing permission (either create and modify) for page "{}"'.format(page_name),
            status=gui_core.GuiDialog.ValidationStatus.Warning,
            ok_visible=False,
            no_visible=False,
        )
        return False

    def _gui_tab_add_page_fnc(self, page_name, switch_to=False):
        self._gui_page_query.push_to_using(page_name)
        self._gui_tab_add_page(page_name, switch_to=switch_to)

    def _gui_tab_page_delete_fnc(self, page_name):
        self._gui_page_query.pull_from_using(page_name)
        self.gui_delete_group_for(page_name)

    def gui_action_create_fnc(self, page_name):
        # check had edit permission first
        if self._gui_page_query.key_is_user(page_name) is True:
            if sum(kit_core.KitPermissionQuery.get_user_args(page_name)) < 2:
                return self.__show_no_edit_permission_dialog(page_name)

        self.switch_current_layer_to('create_layer')

        self._create_option_prx_node.set('gui.group_name', page_name)
        self._create_option_prx_node.set('root', kit_core.KitDesktopHookAddOpt.get_default_root())

    def gui_action_modify_fnc(self, session):
        gui_configure = session.get_gui_configure()
        page_name = gui_configure.get('group_name')
        group_sub_name = gui_configure.get('group_sub_name')

        # check had edit permission first
        if self._gui_page_query.key_is_user(page_name) is True:
            if sum(kit_core.KitPermissionQuery.get_user_args(page_name)) < 2:
                return self.__show_no_edit_permission_dialog(page_name)

        self.switch_current_layer_to('modify_layer')

        configure_file_path = session.get_configure_yaml_file()
        configure_file_opt = bsc_storage.StgFileOpt(configure_file_path)
        self._modify_option_prx_node.set('type', session.get_type())
        self._modify_option_prx_node.set('name', session.get_name())
        self._modify_option_prx_node.set('gui.name', gui_configure.get('name'))
        self._modify_option_prx_node.set('gui.group_name', page_name)
        self._modify_option_prx_node.set('gui.group_sub_name', group_sub_name)
        self._modify_option_prx_node.set('gui.icon_name', gui_configure.get('icon_name') or '')
        self._modify_option_prx_node.set('gui.icon_style', gui_configure.get('icon_style') or '')
        self._modify_option_prx_node.set('gui.icon_sub_name', gui_configure.get('icon_sub_name') or '')
        self._modify_option_prx_node.set('gui.icon_color', gui_configure.get('icon_color') or (255, 255, 255, 255))
        self._modify_option_prx_node.set('gui.tool_tip', gui_configure.get('tool_tip'))
        python_file_path = '{}.py'.format(configure_file_opt.path_base)
        if bsc_storage.StgPath.get_is_file(python_file_path):
            self._modify_option_prx_node.set(
                'script.python', bsc_storage.StgFileOpt(python_file_path).set_read()
            )
        else:
            self._modify_option_prx_node.set(
                'script.python', ''
            )
        windows_shell_file_path = '{}.bat'.format(configure_file_opt.path_base)
        if bsc_storage.StgPath.get_is_file(windows_shell_file_path):
            self._modify_option_prx_node.set(
                'script.windows', bsc_storage.StgFileOpt(windows_shell_file_path).set_read()
            )
        else:
            self._modify_option_prx_node.set(
                'script.windows', ''
            )
        linux_shell_file_path = '{}.sh'.format(configure_file_opt.path_base)
        if bsc_storage.StgPath.get_is_file(linux_shell_file_path):
            self._modify_option_prx_node.set(
                'script.linux', bsc_storage.StgFileOpt(linux_shell_file_path).set_read()
            )
        else:
            self._modify_option_prx_node.set(
                'script.linux', ''
            )

    def gui_action_copy_fnc(self, session):
        self.switch_current_layer_to('copy_layer')
        gui_configure = session.get_gui_configure()
        group_sub_name = gui_configure.get('group_sub_name')

        configure_file_path = session.get_configure_yaml_file()
        configure_file_opt = bsc_storage.StgFileOpt(configure_file_path)
        self._copy_option_prx_node.set('type', session.get_type())
        self._copy_option_prx_node.set('name', session.get_name())
        self._copy_option_prx_node.set('gui.name', gui_configure.get('name'))
        self._copy_option_prx_node.set('gui.group_name', self._gui_page_query.get_all_keys())
        self._copy_option_prx_node.set('gui.group_name', self._gui_page_query.get_current_user_key())
        self._copy_option_prx_node.set('gui.group_sub_name', group_sub_name)
        self._copy_option_prx_node.set('gui.icon_name', gui_configure.get('icon_name') or '')
        self._copy_option_prx_node.set('gui.icon_style', gui_configure.get('icon_style') or '')
        self._copy_option_prx_node.set('gui.icon_sub_name', gui_configure.get('icon_sub_name') or '')
        self._copy_option_prx_node.set('gui.icon_color', gui_configure.get('icon_color') or (255, 255, 255, 255))
        self._copy_option_prx_node.set('gui.tool_tip', gui_configure.get('tool_tip'))
        python_file_path = '{}.py'.format(configure_file_opt.path_base)
        if bsc_storage.StgPath.get_is_file(python_file_path):
            self._copy_option_prx_node.set(
                'script.python', bsc_storage.StgFileOpt(python_file_path).set_read()
            )
        else:
            self._copy_option_prx_node.set(
                'script.python', ''
            )
        windows_shell_file_path = '{}.bat'.format(configure_file_opt.path_base)
        if bsc_storage.StgPath.get_is_file(windows_shell_file_path):
            self._copy_option_prx_node.set(
                'script.windows', bsc_storage.StgFileOpt(windows_shell_file_path).set_read()
            )
        else:
            self._copy_option_prx_node.set(
                'script.windows', ''
            )
        linux_shell_file_path = '{}.sh'.format(configure_file_opt.path_base)
        if bsc_storage.StgPath.get_is_file(linux_shell_file_path):
            self._copy_option_prx_node.set(
                'script.linux', bsc_storage.StgFileOpt(linux_shell_file_path).set_read()
            )
        else:
            self._copy_option_prx_node.set(
                'script.linux', ''
            )

    def gui_delete_group_for(self, page_name):
        self.gui_delete_tool_groups_for_page(page_name)
        gui_path = u'/{}'.format(page_name)
        self.__gui_query.delete(gui_path)

    def _gui_tab_add_page(self, page_name, switch_to=False):
        self.gui_add_customize_for_page(page_name, switch_to=switch_to)
        self.gui_add_builtin_for_page(page_name, switch_to=switch_to)

    def gui_delete_tool_groups_for_page(self, page_name):
        gui_path = u'/{}'.format(page_name)
        self.__gui_query.delete_all_below(gui_path)

        if self.__gui_query.get_is_exists(gui_path) is True:
            tool_group_layout_widget = self.__gui_query.get(gui_path)
            tool_group_layout_widget._clear_all_widgets_()

    def gui_refresh_group(self, page_name):
        self.gui_delete_tool_groups_for_page(page_name)
        self.gui_add_builtin_for_page(page_name)
        self.gui_add_customize_for_page(page_name)

    def gui_add_builtin_for_page(self, page_name, switch_to=False):
        self.gui_get_group_args(
            page_name, switch_to=switch_to
        )

        if page_name in self.__hook_dict:
            hook_data = self.__hook_dict[page_name]
            for i_hook_args, i_group_name, i_group_sub_name in hook_data:
                self.add_tool(
                    i_hook_args, i_group_name, i_group_sub_name
                )

        if page_name in self.__option_hook_dict:
            option_hook_data = self.__option_hook_dict[page_name]
            for i_hook_args, i_group_name, i_group_sub_name in option_hook_data:
                self.add_option_tool(
                    i_hook_args, i_group_name, i_group_sub_name
                )

    def refresh_current_group(self):
        self.gui_refresh_group(self._prx_tab_view.get_current_key())

    @gui_core.GuiDebug.run
    def __debug_run(self, fnc):
        fnc()

    def add_tool(self, hook_args, page_name, group_sub_name, menu_data=None):
        session, execute_fnc = hook_args
        if session.get_is_loadable() is True:
            gui_configure = session.gui_configure
            grid_layout_widget = self.gui_get_view_args(
                page_name, group_sub_name
            )

            tool_path = u'/{}/{}/{}'.format(
                page_name, group_sub_name, bsc_core.BscUuid.generate_by_text(session.get_hook())
            )

            if self.__gui_query.get_is_exists(tool_path) is True:
                prx_tool = self.__gui_query.get(tool_path)
            else:
                prx_tool = gui_prx_widgets.PrxIconPressButton()
                self.__gui_query.register(tool_path, prx_tool)
                grid_layout_widget.add_widget(prx_tool)
                session.set_gui(prx_tool._qt_widget)
                prx_tool.connect_press_dbl_clicked_to(functools.partial(self.__debug_run, execute_fnc))
                prx_tool.set_drag_enable(True)
                name = gui_configure.get('name')
                name_index = self.__gui_query.register_tool_name(page_name, group_sub_name, name, tool_path)
                if name_index > 0:
                    name = u'{}({})'.format(name, name_index)
                icon_name = gui_configure.get('icon_name')
                icon_sub_name = gui_configure.get('icon_sub_name')
                icon_style = gui_configure.get('icon_style')
                icon_color = gui_configure.get('icon_color')
                tool_tip = gui_configure.get('tool_tip')
                prx_tool.set_name(name)
                if icon_name:
                    prx_tool.set_icon_name(icon_name)
                elif icon_color:
                    if icon_style is not None:
                        prx_tool.widget._set_icon_style_(icon_style)

                    prx_tool.set_icon_color(icon_color)
                    prx_tool.set_icon_by_text(name)
                else:
                    prx_tool.set_icon_by_text(name)

                if icon_sub_name:
                    prx_tool.set_sub_icon_name(icon_sub_name)

                if menu_data is not None:
                    prx_tool.set_menu_data(menu_data)

                prx_tool.set_tool_tip(
                    tool_tip,
                    action_tip='"LMB-dbl-click" to open tool'
                )
                prx_tool.set_drag_and_drop_scheme('tool-desktop-tool')
            return prx_tool

    def add_option_tool(self, hook_args, page_name, group_sub_name, menu_data=None):
        session, execute_fnc = hook_args
        if session.get_is_loadable() is True:
            gui_configure = session.gui_configure
            grid_layout_widget = self.gui_get_view_args(
                page_name, group_sub_name
            )

            tool_path = u'/{}/{}/{}'.format(
                page_name, group_sub_name, bsc_core.BscUuid.generate_by_text(session.get_hook())
            )
            if self.__gui_query.get_is_exists(tool_path) is True:
                prx_tool = self.__gui_query.get(tool_path)
            else:
                prx_tool = gui_prx_widgets.PrxIconPressButton()
                self.__gui_query.register(tool_path, prx_tool)
                grid_layout_widget.add_widget(prx_tool)
                session.set_gui(prx_tool._qt_widget)
                prx_tool.connect_press_dbl_clicked_to(functools.partial(self.__debug_run, execute_fnc))
                prx_tool.set_drag_enable(True)
                name = gui_configure.get('name')
                prx_tool.set_name(name)
                # prx_tool.widget._set_icon_draw_percent_(1.0)

                icon_name = gui_configure.get('icon_name')
                icon_sub_name = gui_configure.get('icon_sub_name')
                tool_tip = gui_configure.get('tool_tip') or ''
                if icon_name:
                    prx_tool.set_icon_name(icon_name)
                else:
                    prx_tool.set_icon_by_text(name)

                if icon_sub_name:
                    prx_tool.set_sub_icon_name(icon_sub_name)

                prx_tool.set_tool_tip(
                    tool_tip,
                    action_tip='"LMB-dbl-click" to open tool'
                )
            return prx_tool
