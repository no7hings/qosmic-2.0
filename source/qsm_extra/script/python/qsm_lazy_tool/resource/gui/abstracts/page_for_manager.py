# coding:utf-8
import collections
import functools

import six

import lxbasic.core as bsc_core

import lxbasic.pinyin as bsc_pinyin

import lxbasic.session as bsc_session

import lxgui.core as gui_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.abstracts as gui_prx_abstracts

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_lazy.screw.core as qsm_lzy_scr_core

import lxsession.commands as ssn_commands

from .... import core as _lzy_tol_core


class _GuiThreadExtra:
    def _init_gui_thread_extra_(self, window):
        self._window = window
        self._gui_thread_flag = 0

    def gui_update_thread_flag(self):
        self._gui_thread_flag += 1

    def gui_run_thread(self, cache_fnc, build_fnc, post_fnc=None):
        t = self._window._qt_widget._generate_thread_(
            cache_fnc,
            build_fnc,
            post_fnc=post_fnc
        )
        return t


class _GuiBaseOpt(
    object,
    _GuiThreadExtra
):
    GUI_NAMESPACE = None

    def __init__(self, window, page, session):
        self._init_gui_thread_extra_(window)

        self._window = window
        self._page = page
        self._session = session

        self._gui_thread_flag = 0

    def gui_update_thread_flag(self):
        self._gui_thread_flag += 1

    def gui_run_thread(self, cache_fnc, build_fnc, post_fnc=None):
        t = self._window._qt_widget._generate_thread_(
            cache_fnc,
            build_fnc,
            post_fnc=post_fnc
        )
        return t


class _GuiTypeOpt(
    _GuiBaseOpt,
    gui_prx_abstracts.AbsGuiPrxTreeViewOpt
):
    GUI_NAMESPACE = 'type'

    def restore_all(self):
        self.restore()
        self.gui_clear_cache()

    def __init__(self, window, page, session):
        super(_GuiTypeOpt, self).__init__(window, page, session)

        self._prx_tree_view = gui_prx_widgets.PrxTreeView()
        self._page._prx_v_splitter_0.add_widget(self._prx_tree_view)
        self._prx_tree_view.create_header_view(
            [('name', 4)], 320-48
        )

        self._prx_tree_view.set_filter_entry_tip('filter by keyword ...')

        self._prx_tree_view.get_top_tool_bar().set_expanded(True)

        self._prx_tree_view.connect_item_select_changed_to(
            self._page.do_gui_node_refresh_by_type_selection
        )

        self._init_tree_view_opt_(self._prx_tree_view, self.GUI_NAMESPACE)

        self._data_cache_dict = {}
        self._leaf_entity_path_set = set()

    def gui_add_entity(self, scr_entity, gui_thread_flag):
        def cache_fnc_():
            # root
            if path == '/':
                _src_node_path_set = set(
                    map(
                        lambda _x: _x.path,
                        self._page._scr_stage.find_all(
                            entity_type=self._page._scr_stage.EntityTypes.Node,
                            filters=[
                                ('type', 'is', 'node')
                            ]
                        )
                    )
                )
                self._data_cache_dict[path] = _src_node_path_set
                return [_src_node_path_set]
            # unspecified
            elif path == '/unspecified':
                _all_scr_node_path_set = set(
                    map(
                        lambda _x: _x.path,
                        self._page._scr_stage.find_all(
                            entity_type=self._page._scr_stage.EntityTypes.Node,
                            filters=[
                                ('type', 'is', 'node')
                            ]
                        )
                    )
                )

                _all_assigned_node_scr_path_set = set(
                    map(
                        lambda _x: _x.source,
                        self._page._scr_stage.find_all(
                            entity_type=self._page._scr_stage.EntityTypes.Assign,
                            filters=[
                                ('type', 'is', 'type_assign')
                            ]
                        )
                    )
                )

                _src_node_path_set = _all_scr_node_path_set-_all_assigned_node_scr_path_set
                self._data_cache_dict[path] = _src_node_path_set
                return [_src_node_path_set]

            if path in self._leaf_entity_path_set:
                _filters = [
                    ('type', 'is', 'type_assign'),
                    ('target', 'is', path),
                ]
            else:
                _filters = [
                    ('type', 'is', 'type_assign'),
                    ('target', 'startswith', path+'/'),
                ]

            _scr_assigns = self._page._scr_stage.find_all(
                entity_type=self._page._scr_stage.EntityTypes.Assign,
                filters=_filters
            )
            # clean duplicate
            _src_node_path_set = set([x.source for x in _scr_assigns])
            self._data_cache_dict[path] = _src_node_path_set
            return [_src_node_path_set]

        def build_fnc_(data_):
            if gui_thread_flag != self._gui_thread_flag:
                return

            _src_node_path_set = data_[0]
            _count = len(_src_node_path_set)
            _name = six.u('{}({})').format(gui_name, _count)
            prx_item.set_name(_name)
            if _count > 0:
                prx_item.set_status(
                    prx_item.ValidationStatus.Normal
                )
                prx_item.set_expanded(True)
            else:
                prx_item.set_status(
                    prx_item.ValidationStatus.Disable
                )
                prx_item.set_expanded(False)

        path = scr_entity.path

        if self.gui_check_exists(path) is True:
            return self.gui_get_one(path)

        path_opt = bsc_core.BscPathOpt(path)
        parent_gui = self.gui_get_one(path_opt.get_parent_path())

        gui_name = scr_entity.gui_name
        if self._window._language == 'chs':
            gui_name = scr_entity.gui_name_chs

        prx_item = parent_gui.add_child(
            gui_name,
            icon=gui_core.GuiIcon.get(scr_entity.gui_icon_name),
        )
        prx_item.set_gui_dcc_obj(scr_entity, namespace=self._namespace)
        self.gui_register(path, prx_item)
        prx_item.set_type(
            scr_entity.entity_type
        )
        prx_item.set_keyword_filter_keys_tgt(
            bsc_pinyin.Texts.split_any_to_words_extra([scr_entity.gui_name, scr_entity.gui_name_chs])
        )
        prx_item.set_tool_tip(scr_entity.to_description(self._window._language))

        prx_item.set_show_fnc(
            cache_fnc_, build_fnc_
        )
        return prx_item

    def gui_add_all_entities(self):
        self.gui_update_thread_flag()

        t = self.gui_run_thread(
            functools.partial(
                self._gui_add_entity_cache_fnc, self._gui_thread_flag
            ),
            self._gui_add_entity_build_fnc
        )

        t.do_start()

    def _gui_add_entity_cache_fnc(self, gui_thread_flag):
        if gui_thread_flag != self._gui_thread_flag:
            return [[], 0]

        return [
            self._page._scr_stage.find_all(
                self._page._scr_stage.EntityTypes.Type,
            ),
            gui_thread_flag
        ]

    def _gui_add_entity_build_fnc(self, *args):
        scr_entities, gui_thread_flag = args[0]
        if gui_thread_flag != self._gui_thread_flag:
            return

        # cache leaf paths
        self._leaf_entity_path_set = set(
            bsc_core.BscPath.to_leaf_paths([x.path for x in scr_entities])
        )

        for i_scr_entity in scr_entities:
            self.gui_add_entity(i_scr_entity, gui_thread_flag)

    def do_gui_add_all(self):
        self.restore()
        self.gui_add_all_entities()

    def get_selected_entities(self):
        return [x.get_gui_dcc_obj(self._namespace) for x in self._prx_tree_view.get_all_selected_items()]

    def get_assigned_node_paths(self, scr_type_path):
        return self._data_cache_dict[scr_type_path]

    def gui_clear_cache(self):
        self._data_cache_dict.clear()
        self._leaf_entity_path_set.clear()

    def gui_do_close(self):
        pass


class _GuiTagOpt(
    _GuiBaseOpt
):
    def restore(self):
        pass

    def restore_all(self):
        self._prx_tag_view.restore()
        self.gui_clear_cache()

    def gui_clear_cache(self):
        self._data_cache_dict.clear()

    def __init__(self, window, page, session):
        super(_GuiTagOpt, self).__init__(window, page, session)

        self._prx_tag_view = gui_prx_widgets.PrxTagView()
        self._page._prx_v_splitter_0.add_widget(self._prx_tag_view)

        self._prx_tag_view.get_top_tool_bar().set_expanded(True)

        self._prx_tag_view.connect_check_paths_changed_to(
            self._page.do_gui_node_refresh_by_tag_check
        )

        self._data_cache_dict = {}
    
    def gui_check_exists(self, path):
        return self._prx_tag_view.check_exists(path)

    def gui_get_one(self, path):
        return self._prx_tag_view.get_one(path)

    # entity
    def gui_add_all_entities(self):
        self.gui_update_thread_flag()

        t = self.gui_run_thread(
            functools.partial(
                self._gui_add_entity_cache_fnc, self._gui_thread_flag
            ),
            self._gui_add_entity_build_fnc,
        )
        t.do_start()

    def _gui_add_entity_cache_fnc(self, gui_thread_flag):
        if gui_thread_flag != self._gui_thread_flag:
            return [[], 0]

        return [
            self._page._scr_stage.find_all(
                self._page._scr_stage.EntityTypes.Tag,
                # filters=[
                #     ('category', 'is', 'group')
                # ]
            ),
            gui_thread_flag
        ]

    def _gui_add_entity_build_fnc(self, *args):
        scr_entities, gui_thread_flag = args[0]
        if gui_thread_flag != self._gui_thread_flag:
            return

        for i_scr_entity in scr_entities:
            if i_scr_entity.category == 'group':
                self.gui_add_group(i_scr_entity, gui_thread_flag)
            elif i_scr_entity.category == 'node':
                self.gui_add_node(i_scr_entity, gui_thread_flag)

    # group
    def gui_add_group(self, scr_entity, gui_thread_flag):
        def cache_fnc_():
            # creation time
            if path == '/':
                _src_node_path_set = set(
                    map(
                        lambda _x: _x.path,
                        self._page._scr_stage.find_all(
                            entity_type=self._page._scr_stage.EntityTypes.Node,
                            filters=[
                                ('type', 'is', 'node')
                            ]
                        )
                    )
                )
                self._data_cache_dict[path] = _src_node_path_set
                return [_src_node_path_set]
            elif path == '/ctime':
                _src_node_path_set = set(
                    map(
                        lambda _x: _x.path,
                        self._page._scr_stage.find_all(
                            entity_type=self._page._scr_stage.EntityTypes.Node,
                            filters=[
                                ('type', 'is', 'node')
                            ]
                        )
                    )
                )
                self._data_cache_dict[path] = _src_node_path_set
                return [_src_node_path_set]
            else:
                _scr_assigns = self._page._scr_stage.find_all(
                    entity_type=self._page._scr_stage.EntityTypes.Assign,
                    filters=[
                        ('type', 'is', 'tag_assign'),
                        ('target', 'startswith', scr_entity.path),
                    ]
                )
                # clean duplicate
                _src_node_path_set = set([x.source for x in _scr_assigns])
                self._data_cache_dict[path] = _src_node_path_set
                return [_src_node_path_set]

        def build_fnc_(data_):
            if gui_thread_flag != self._gui_thread_flag:
                return

            _src_node_path_set = data_[0]
            widget._assign_path_set_(_src_node_path_set)
            widget._set_tool_tip_(scr_entity.to_description(self._window._language))

        path = scr_entity.path

        gui_name = scr_entity.gui_name
        if self._window._language == 'chs':
            gui_name = scr_entity.gui_name_chs

        widget = self._prx_tag_view.create_group(
            scr_entity.path, show_name=gui_name
        )

        widget._set_expanded_(True)

        t = self.gui_run_thread(cache_fnc_, build_fnc_)
        t.do_start()
        return widget

    # node
    def gui_add_node(self, scr_entity, gui_thread_flag):
        def cache_fnc_():
            if path.startswith('/ctime'):
                _src_node_path_set = set(
                    map(
                        lambda _x: _x.path,
                        self._page._scr_stage.find_all_by_ctime_tag(
                            self._page._scr_stage.EntityTypes.Node,
                            bsc_core.BscPathOpt(path).name,
                            filters=[
                                ('type', 'is', 'node')
                            ]
                        )
                    )
                )
                self._data_cache_dict[path] = _src_node_path_set
                return [_src_node_path_set]
            else:
                _scr_assigns = self._page._scr_stage.find_all(
                    entity_type=self._page._scr_stage.EntityTypes.Assign,
                    filters=[
                        ('type', 'is', 'tag_assign'),
                        ('target', 'startswith', scr_entity.path),
                    ]
                )
                # clean duplicate
                _src_node_path_set = set([x.source for x in _scr_assigns])
                self._data_cache_dict[path] = _src_node_path_set
                return [_src_node_path_set]

        def build_fnc_(data_):
            if gui_thread_flag != self._gui_thread_flag:
                return

            _src_node_path_set = data_[0]
            widget._assign_path_set_(_src_node_path_set)
            widget._set_tool_tip_(scr_entity.to_description(self._window._language))

        path = scr_entity.path

        gui_name = scr_entity.gui_name
        if self._window._language == 'chs':
            gui_name = scr_entity.gui_name_chs

        widget = self._prx_tag_view.create_node(
            scr_entity.path, show_name=gui_name
        )
        t = self.gui_run_thread(cache_fnc_, build_fnc_)
        t.do_start()
        return widget

    # main
    def do_gui_add_all(self):
        self.restore()
        self.gui_add_all_entities()

    def get_all_checked_node_paths(self):
        return self._prx_tag_view.get_all_checked_node_paths()

    def apply_intersection_paths(self, path_set):
        self._prx_tag_view.apply_intersection_paths(path_set)

    def get_assigned_node_paths(self, scr_tag_path):
        return self._data_cache_dict[scr_tag_path]

    def gui_do_close(self):
        pass


class _GuiNodeOpt(
    _GuiBaseOpt,
    gui_prx_abstracts.AbsGuiPrxListViewOpt
):
    GUI_NAMESPACE = 'node'

    CHUNK_SIZE_MINIMUM = 16
    THREAD_MAXIMUM = 64

    def gui_register(self, path, qt_item):
        self._item_dict[path] = qt_item
        # prx_item.set_gui_attribute('path', path)

    def restore_all(self):
        super(_GuiNodeOpt, self).restore()
        self.gui_clear_cache()

    def get_dtb_entity_menu_content(self, scr_entity):
        scr_stage_key = self._page._scr_stage.key
        options = []
        c = self._window._configure.get(
            'entity-actions.{}.{}.option-hooks'.format(scr_stage_key, scr_entity.entity_type)
        )
        if c:
            for i in c:
                if isinstance(i, dict):
                    i_key = i.keys()[0]
                    i_value = i.values()[0]
                else:
                    i_key = i
                    i_value = {}
                #
                i_kwargs = dict(
                    option_hook_key=i_key,
                    stage_key=scr_stage_key,
                    window_unique_id=self._window.get_window_unique_id(),
                    entity_type=scr_entity.entity_type,
                    entity=scr_entity.path,
                )
                i_kwargs.update(**{k: v for k, v in i_value.items() if v})
                options.append(
                    bsc_core.ArgDictStringOpt(i_kwargs).to_string(),
                )
            return bsc_session.OptionHook.generate_menu_contents(options, self._window._language)

    def generate_menu_content(self):
        pass

    def __init__(self, window, page, session):
        super(_GuiNodeOpt, self).__init__(window, page, session)

        self._item_frame_size = self._window._gui_configure.get('item_frame_size')
        self._item_icon_frame_size = self._window._gui_configure.get('item_icon_frame_size')
        self._item_icon_size = self._window._gui_configure.get('item_icon_size')

        self._prx_list_view = gui_prx_widgets.PrxListView()
        self._page._prx_h_splitter_0.add_widget(self._prx_list_view)

        self._prx_list_view.get_check_tool_box().set_visible(True)
        self._prx_list_view.get_scale_switch_tool_box().set_visible(True)
        self._prx_list_view.get_sort_switch_tool_box().set_visible(True)
        self._prx_list_view.set_filter_entry_tip('filter by keyword ...')
        self._prx_list_view.set_item_event_override_flag(True)

        self._prx_list_view.get_top_tool_bar().set_expanded(True)

        # self._prx_list_view.get_filter_tool_box().set_visible(False)
        self._prx_list_view.set_item_frame_size_basic(*self._item_frame_size)
        self._prx_list_view.set_item_icon_frame_size(*self._item_icon_frame_size)
        self._prx_list_view.set_item_icon_size(*self._item_icon_size)
        self._prx_list_view.set_item_frame_draw_enable(True)
        # self._prx_list_view.set_item_name_frame_draw_enable(True)
        self._prx_list_view.set_item_names_draw_range([None, 1])
        # self._prx_list_view.set_item_image_frame_draw_enable(True)

        self._prx_list_view.connect_press_released_to(self.do_save_context)

        self._init_list_view_opt_(self._prx_list_view, self.GUI_NAMESPACE)

        self._running_threads_stacks = []

        self._window.register_window_close_method(
            self.restore_thread_stack
        )

        self._type_cache_node_paths = []
        self._tag_cache_node_paths = []

        self._data_cache_dict = {}

        self._node_path_set = set()

    def gui_clear_cache(self):
        self._type_cache_node_paths = []
        self._tag_cache_node_paths = []
        self._data_cache_dict.clear()

    def restore_thread_stack(self):
        if self._running_threads_stacks:
            [i.do_quit() for i in self._running_threads_stacks]

        self._running_threads_stacks = []

    def do_save_context(self):
        selected_qt_item_widgets = self._prx_list_view.get_selected_qt_item_widgets()
        if selected_qt_item_widgets:
            qt_item_widget = selected_qt_item_widgets[0]
            scr_entity = qt_item_widget._get_entity_()
            data_type = qt_item_widget._get_property_('data_type')
            file_path = qt_item_widget._get_property_(data_type)
            data = dict(
                stage=self._page._scr_stage_key,
                path=scr_entity.path,
                gui_name_chs=scr_entity.gui_name_chs,
                data_type=data_type,
                file=file_path
            )
            qsm_lzy_scr_core.DataContext.save(data)

    # node
    def gui_add_nodes(self, scr_node_paths, gui_thread_flag):
        if gui_thread_flag != self._gui_thread_flag:
            return

        scr_node_paths = bsc_core.RawTextsMtd.sort_by_number(scr_node_paths)

        scr_node_paths_map = bsc_core.RawListMtd.split_to(
            scr_node_paths, self.THREAD_MAXIMUM, self.CHUNK_SIZE_MINIMUM
        )

        ts = []
        for i_scr_node_paths in scr_node_paths_map:
            i_r = self._window.widget._generate_thread_(
                functools.partial(
                    self._gui_add_nodes_cache_fnc, i_scr_node_paths, gui_thread_flag
                ),
                self._gui_add_nodes_build_fnc
            )
            ts.append(i_r)
        #
        [x.do_start() for x in ts]

    def _gui_add_nodes_cache_fnc(self, scr_node_paths, gui_thread_flag):
        if gui_thread_flag != self._gui_thread_flag:
            return [[], 0]

        return [
            [self._page._scr_stage.get_node(x) for x in scr_node_paths],
            gui_thread_flag
        ]

    def _gui_add_nodes_build_fnc(self, *args):
        scr_nodes, gui_thread_flag = args[0]
        if gui_thread_flag != self._gui_thread_flag:
            return

        for i_scr_node in scr_nodes:
            self.gui_add_node(i_scr_node, gui_thread_flag)

    def gui_add_node(self, scr_entity, gui_thread_flag):
        if scr_entity is None:
            return

        path = scr_entity.path
        if self.gui_check_exists(path) is True:
            return self.gui_get_one(path)

        qt_item = self._prx_list_view.create_item_()
        qt_item._set_sort_name_key_(scr_entity.gui_name)
        qt_item._set_item_keyword_filter_keys_tgt_(
            [scr_entity.path, scr_entity.gui_name, scr_entity.gui_name_chs]
        )
        self.gui_register(path, qt_item)
        qt_item._scr_entity = scr_entity

        qt_item._set_item_show_fnc_(
            functools.partial(self._gui_node_show_cache_fnc, qt_item, scr_entity, gui_thread_flag),
            self._gui_node_show_build_fnc
        )

    def _gui_node_show_cache_fnc(self, qt_item, scr_entity, gui_thread_flag):
        if gui_thread_flag != self._gui_thread_flag:
            return [[], 0]

        path = scr_entity.path

        if path in self._data_cache_dict:
            data = self._data_cache_dict[path]
            return [[qt_item, scr_entity, data], gui_thread_flag]

        tag_scr_assigns = self._page._scr_stage.find_all(
            self._page._scr_stage.EntityTypes.Assign,
            [
                ('type', 'is', 'tag_assign'),
                ('source', 'is', scr_entity.path),
            ]
        )
        tag_dict = collections.OrderedDict()
        for i_tag_scr_assign in tag_scr_assigns:
            i_scr_tag_path = i_tag_scr_assign.target
            i_scr_tag = self._page._scr_stage.get_entity(
                self._page._scr_stage.EntityTypes.Tag, i_scr_tag_path
            )
            i_scr_tag_group = self._page._scr_stage.get_entity(
                self._page._scr_stage.EntityTypes.Tag, bsc_core.BscPath.get_dag_parent_path(i_scr_tag_path)
            )
            if self._window._language == 'chs':
                i_key = i_scr_tag_group.gui_name_chs
                i_value = bsc_core.auto_string(i_scr_tag.gui_name_chs)
            else:
                i_key = i_scr_tag_group.gui_name
                i_value = bsc_core.auto_string(i_scr_tag.gui_name)

            if i_key in tag_dict:
                i_value_all = tag_dict[i_key]
                i_value_all += ', {}'.format(i_value)
            else:
                i_value_all = i_value

            tag_dict[i_key] = i_value_all

        scr_properties = self._page._scr_stage.find_all(
            self._page._scr_stage.EntityTypes.Property,
            [
                ('type', 'is', 'parameter'),
                ('node', 'is', scr_entity.path),
            ]
        )
        property_dict = {}
        for i_scr_property in scr_properties:
            property_dict[i_scr_property.port] = i_scr_property.value

        self._data_cache_dict[path] = [tag_dict, property_dict]
        return [
            [qt_item, scr_entity, [tag_dict, property_dict]], gui_thread_flag
        ]

    def _gui_node_show_build_fnc(self, *args):
        build_data, gui_thread_flag = args[0]
        if gui_thread_flag != self._gui_thread_flag:
            return

        qt_item, scr_entity, data = build_data

        qt_item_widget = gui_qt_widgets.QtItemWidgetForList()
        self._prx_list_view.assign_item_widget(qt_item, qt_item_widget)

        tag_dict, property_dict = data
        qt_item_widget._set_entity_(scr_entity)
        qt_item_widget._set_path_text_(scr_entity.path)
        qt_item_widget._set_index_(scr_entity.id)

        gui_name = scr_entity.gui_name
        if self._window._language == 'chs':
            gui_name = scr_entity.gui_name_chs

        menu_content = self.get_dtb_entity_menu_content(scr_entity)
        if menu_content:
            qt_item._set_menu_content_(menu_content)

        qt_item_widget._set_name_text_(gui_name)
        qt_item_widget._set_name_dict_(tag_dict)
        qt_item_widget._set_tool_tip_(
            scr_entity.to_description(self._window._language)
        )
        if 'video' in property_dict:
            if 'thumbnail' in property_dict:
                qt_item_widget._set_image_path_(
                    property_dict['thumbnail']
                )

            qt_item_widget._set_video_path_(property_dict['video'])
        elif 'image' in property_dict:
            if 'thumbnail' in property_dict:
                qt_item_widget._set_image_path_(
                    property_dict['thumbnail']
                )
        elif 'image_sequence' in property_dict:
            if 'thumbnail' in property_dict:
                qt_item_widget._set_image_path_(
                    property_dict['thumbnail']
                )

            qt_item_widget._set_image_sequence_path_(property_dict['image_sequence'])

        qt_item_widget._set_property_dict_(property_dict)

        qt_item_widget._refresh_widget_all_()

    # by type
    def do_gui_add_all_by_type(self, scr_type_paths):
        if scr_type_paths:
            self.restore()
            self._gui_add_nodes_by_type_paths(scr_type_paths)
        else:
            self._type_cache_node_paths = []
            self._page._gui_tag_opt.apply_intersection_paths(set(self._type_cache_node_paths))
            #
            self._page.do_gui_node_refresh_by_tag_check()

    def _gui_add_nodes_by_type_paths(self, scr_type_paths):
        self.restore_thread_stack()

        self.gui_update_thread_flag()

        t = self.gui_run_thread(
            functools.partial(
                self._gui_add_nodes_by_type_cache_fnc, scr_type_paths, self._gui_thread_flag
            ),
            self._gui_add_nodes_by_type_build_fnc
        )

        t.do_start()

    def _gui_add_nodes_by_type_cache_fnc(self, scr_type_paths, gui_thread_flag):
        if gui_thread_flag != self._gui_thread_flag:
            return [[], 0]

        all_sets = []
        for i_scr_type_path in scr_type_paths:
            i_scr_node_paths = self._page._gui_type_opt.get_assigned_node_paths(i_scr_type_path)
            all_sets.append(i_scr_node_paths)

        return [
            list(set.union(*all_sets)),
            gui_thread_flag
        ]

    def _gui_add_nodes_by_type_build_fnc(self, *args):
        scr_node_paths, gui_thread_flag = args[0]
        if gui_thread_flag != self._gui_thread_flag:
            return

        self._type_cache_node_paths = scr_node_paths

        self._page._gui_tag_opt.apply_intersection_paths(set(self._type_cache_node_paths))

        if self._tag_cache_node_paths:
            scr_node_paths_ = list(set.intersection(set(self._tag_cache_node_paths), set(self._type_cache_node_paths)))
        else:
            scr_node_paths_ = scr_node_paths

        self.gui_add_nodes(scr_node_paths_, gui_thread_flag)

    # by tag
    def do_gui_add_all_by_tag(self, scr_tag_paths):
        if scr_tag_paths:
            self.restore()
            self._gui_add_nodes_by_tag_paths(scr_tag_paths)
        else:
            self._tag_cache_node_paths = []

            self.restore()
            if self._type_cache_node_paths:
                self.restore_thread_stack()

                self.gui_update_thread_flag()

                self.gui_add_nodes(self._type_cache_node_paths, self._gui_thread_flag)

    def _gui_add_nodes_by_tag_paths(self, scr_tag_paths):
        self.restore_thread_stack()

        self.gui_update_thread_flag()

        t = self.gui_run_thread(
            functools.partial(
                self._gui_add_nodes_by_tag_cache_fnc, scr_tag_paths, self._gui_thread_flag
            ),
            self._gui_add_nodes_by_tag_build_fnc
        )
        t.do_start()

    def _gui_add_nodes_by_tag_cache_fnc(self, scr_tag_paths, gui_thread_flag):
        if gui_thread_flag != self._gui_thread_flag:
            return [[], 0]

        dict_ = {}
        for i_scr_tag_path in scr_tag_paths:
            dict_.setdefault(
                bsc_core.BscPathOpt(i_scr_tag_path).get_parent_path(),
                set()
            ).add(i_scr_tag_path)

        all_sets = []
        for i_k, i_v in dict_.items():
            i_scr_node_paths = set()
            for j_scr_tag_path in i_v:
                j_scr_node_paths = self._page._gui_tag_opt.get_assigned_node_paths(j_scr_tag_path)
                i_scr_node_paths.update(j_scr_node_paths)

            all_sets.append(i_scr_node_paths)

        return [
            list(set.intersection(*all_sets)),
            gui_thread_flag
        ]

    def _gui_add_nodes_by_tag_build_fnc(self, *args):
        scr_node_paths, gui_thread_flag = args[0]
        if gui_thread_flag != self._gui_thread_flag:
            return

        self._tag_cache_node_paths = scr_node_paths

        if self._type_cache_node_paths:
            scr_node_paths_ = list(set.intersection(set(self._tag_cache_node_paths), set(self._type_cache_node_paths)))
        else:
            scr_node_paths_ = scr_node_paths

        self.gui_add_nodes(scr_node_paths_, gui_thread_flag)

    def gui_do_close(self):
        pass

    def gui_get_checked_scr_entities(self):
        return [x._scr_entity for x in self._prx_list_view.get_checked_items()]
    
    def gui_get_selected_scr_entities(self):
        return [x._scr_entity for x in self._prx_list_view.get_selected_items()]

    def gui_get_checked_or_selected_scr_entities(self):
        return self.gui_get_checked_scr_entities() or self.gui_get_selected_scr_entities()


class AbsPrxPageForManager(
    gui_prx_widgets.PrxBasePage,
    _GuiThreadExtra,
):
    HISTORY_KEY = 'lazy-resource.stage_key'

    FILTER_MAXIMUM = 50

    def do_gui_node_refresh_by_type_selection(self):
        self._gui_node_opt.do_gui_add_all_by_type(
            [x.path for x in self._gui_type_opt.get_selected_entities()]
        )

    def do_gui_node_refresh_by_tag_check(self):
        self._gui_node_opt.do_gui_add_all_by_tag(
            self._gui_tag_opt.get_all_checked_node_paths()
        )

    def gui_close_fnc(self):
        self._scr_stage.close()

    def do_gui_page_initialize(self, key):
        self._scr_stage_key = key
        self._scr_stage = qsm_lzy_scr_core.Stage(self._scr_stage_key)

        self.gui_page_setup_fnc()

    def _gui_add_main_tools(self):
        for i in [
            ('add', 'file/add-file', '', self._add_resource)
        ]:
            i_key, i_icon_name, i_tool_tip, i_fnc = i
            i_tool = gui_prx_widgets.PrxIconPressButton()
            self._main_prx_tool_box.add_widget(i_tool)
            i_tool.set_name(i_key)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip(i_tool_tip)
            i_tool.connect_press_clicked_to(i_fnc)

    def _add_resource(self):
        w = self._window.generate_sub_panel_for('register')
        w.gui_setup_pages_for(['motion'])
        w.show_window_auto()

    def _gui_add_filter_tools(self):
        self._keyword_set = set()
        self._keyword_pinyin_dict = {}
        self._prx_filter_bar = gui_prx_widgets.PrxFilterBar()
        self._filter_prx_tool_box.add_widget(self._prx_filter_bar)
        
        self._prx_filter_bar._qt_widget._set_input_completion_buffer_fnc_(self._gui_keyword_filter_completion_gain_fnc)
        self._prx_filter_bar._qt_widget.input_value_accepted.connect(self._gui_update_keyword_filter_path_set_fnc)
    
    def _gui_keyword_filter_completion_gain_fnc(self, *args, **kwargs):
        keyword = args[0]
        if keyword:
            match_pinyin = bsc_core.BscFnmatch.filter(
                self._keyword_pinyin_dict.keys(), six.u('*{}*').format(keyword)
            )

            match_chs = [self._keyword_pinyin_dict[x] for x in match_pinyin]

            matches = bsc_core.BscFnmatch.filter(
                self._keyword_set, six.u('*{}*').format(keyword)
            )
            all_texts = match_chs + matches
            return bsc_core.RawTextsMtd.sort_by_initial(all_texts)[:self.FILTER_MAXIMUM]
        return []

    def _gui_update_keyword_filter_path_set_fnc(self, *args, **kwargs):
        keyword = args[0]
        print keyword

    def _gui_update_keyword_filter_texts(self):
        def cache_fnc_(gui_thread_flag_):
            self._keyword_set = set()
            self._keyword_pinyin_dict = {}

            _all_scr_nodes = self._scr_stage.find_all(
                self._scr_stage.EntityTypes.Node,
                [
                    ('type', 'is', 'node'),
                ]
            )

            for _i in _all_scr_nodes:
                _i_list, _i_dict = bsc_pinyin.Text.to_pinyin_map(_i.gui_name_chs)
                self._keyword_set.update(_i_list)
                self._keyword_pinyin_dict.update(_i_dict)

            return []

        def build_fnc_(data_):
            pass

        t = self.gui_run_thread(
            functools.partial(cache_fnc_, self._gui_thread_flag),
            build_fnc_
        )

        t.do_start()

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForManager, self).__init__(window, session, *args, **kwargs)
        self._init_gui_thread_extra_(window)

        self._scr_stage_key = None
        self._scr_stage = None

        self._window.register_window_close_method(self.gui_close_fnc)

    def gui_page_setup_fnc(self):
        self._top_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_align_left()
        self._top_prx_tool_bar.set_expanded(True)

        self._main_prx_tool_box = self._top_prx_tool_bar.create_tool_box('main')
        self._gui_add_main_tools()

        self._filter_prx_tool_box = self._top_prx_tool_bar.create_tool_box('filter', size_mode=1)
        # self._gui_add_filter_tools()

        prx_sca = gui_prx_widgets.PrxVScrollArea()
        self._qt_layout.addWidget(prx_sca.widget)

        self._prx_h_splitter_0 = gui_prx_widgets.PrxHSplitter()
        prx_sca.add_widget(self._prx_h_splitter_0)

        self._prx_v_splitter_0 = gui_prx_widgets.PrxVSplitter()
        self._prx_h_splitter_0.add_widget(self._prx_v_splitter_0)
        self._gui_type_opt = _GuiTypeOpt(self._window, self, self._session)
        self._gui_tag_opt = _GuiTagOpt(self._window, self, self._session)

        self._gui_node_opt = _GuiNodeOpt(self._window, self, self._session)

        self._prx_v_splitter_1 = gui_prx_widgets.PrxVSplitter()
        self._prx_h_splitter_0.add_widget(self._prx_v_splitter_1)
        self._prx_h_splitter_0.swap_contract_right_or_bottom_at(2)

        self._prx_h_splitter_0.set_fixed_size_at(0, 320)
        self._prx_h_splitter_0.set_fixed_size_at(2, 320)
        self._prx_v_splitter_0.set_fixed_size_at(1, 480)

        self.do_gui_refresh_all()

    def do_gui_refresh_all(self):
        self._gui_update_keyword_filter_texts()
        self._gui_node_opt.restore_all()
        self._gui_type_opt.restore_all()
        self._gui_tag_opt.restore_all()

        self._gui_type_opt.do_gui_add_all()
        self._gui_tag_opt.do_gui_add_all()
