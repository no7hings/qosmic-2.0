# coding:utf-8
import copy

import functools

import six

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.pinyin as bsc_pinyin

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.abstracts as gui_prx_abstracts

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_screw.core as qsm_scr_core


class _GuiBaseOpt(object):
    GUI_NAMESPACE = None

    def __init__(self, window, page, session, scr_stage):
        self._window = window
        self._page = page
        self._session = session

        self._scr_stage = scr_stage


class _GuiTypeOpt(
    _GuiBaseOpt,
    gui_prx_abstracts.AbsGuiPrxTreeViewOpt
):
    GUI_NAMESPACE = 'type'

    def __init__(self, window, page, session, scr_stage):
        super(_GuiTypeOpt, self).__init__(window, page, session, scr_stage)

        self._prx_tree_view = gui_prx_widgets.PrxTreeView()
        self._page._prx_v_splitter_0.add_widget(self._prx_tree_view)
        self._prx_tree_view.create_header_view(
            [('name', 4), ('count', 1)], 320-48
        )

        self._prx_tree_view.set_filter_entry_tip('filter by keyword ...')

        self._prx_tree_view.get_top_tool_bar().set_expanded(True)

        self._prx_tree_view.connect_item_select_changed_to(
            self._page.do_gui_node_refresh_by_type_selection
        )

        self._init_tree_view_opt_(self._prx_tree_view, self.GUI_NAMESPACE)

        self._index_thread_batch = 0

        self._data_cache_dict = {}

    def gui_add_entity(self, scr_entity):
        def cache_fnc_():
            # root
            if path == '/':
                _src_node_path_set = set(
                    map(
                        lambda _x: _x.path,
                        self._scr_stage.find_all(
                            entity_type=self._scr_stage.EntityTypes.Node,
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
                        self._scr_stage.find_all(
                            entity_type=self._scr_stage.EntityTypes.Node,
                            filters=[
                                ('type', 'is', 'node')
                            ]
                        )
                    )
                )

                _all_assigned_node_scr_path_set = set(
                    map(
                        lambda _x: _x.source,
                        self._scr_stage.find_all(
                            entity_type=self._scr_stage.EntityTypes.Assign,
                            filters=[
                                ('type', 'is', 'type_assign')
                            ]
                        )
                    )
                )

                _src_node_path_set = _all_scr_node_path_set-_all_assigned_node_scr_path_set
                self._data_cache_dict[path] = _src_node_path_set
                return [_src_node_path_set]

            _scr_assigns = self._scr_stage.find_all(
                entity_type=self._scr_stage.EntityTypes.Assign,
                filters=[
                    ('type', 'is', 'type_assign'),
                    ('target', 'startswith', path),
                ]
            )
            # clean duplicate
            _src_node_path_set = set([x.source for x in _scr_assigns])
            self._data_cache_dict[path] = _src_node_path_set
            return [_src_node_path_set]

        def build_fnc_(data_):
            _src_node_path_set = data_[0]
            _count = len(_src_node_path_set)
            prx_item.set_name(str(_count), 1)

            if _count > 0:
                prx_item.set_status(
                    prx_item.ValidationStatus.Normal
                )
            else:
                prx_item.set_status(
                    prx_item.ValidationStatus.Disable
                )

        path = scr_entity.path

        if self.gui_check_exists(path) is True:
            return self.gui_get_one(path)

        path_opt = bsc_core.PthNodeOpt(path)
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
        prx_item.set_tool_tip(scr_entity.to_string('user', 'gui_description_chs', 'ctime', 'mtime'))
        #
        # self._prx_tree_view.connect_item_expand_to(
        #     prx_item,
        #     functools.partial(self.refresh_by_category_expanded, prx_item),
        #     time=100
        # )
        #
        prx_item.set_expanded(True)
        prx_item.set_show_fnc(
            cache_fnc_, build_fnc_
        )
        return prx_item

    def gui_add_entities(self):
        self._index_thread_batch += 1

        t = self._window.widget._generate_thread_(
            functools.partial(
                self._gui_add_entity_cache_fnc, self._index_thread_batch
            ),
            self._gui_add_entity_build_fnc
        )

        t.do_start()

    def _gui_add_entity_cache_fnc(self, thread_stack_index):
        if thread_stack_index != self._index_thread_batch:
            return [[], 0]

        return [
            self._scr_stage.find_all(
                self._scr_stage.EntityTypes.Type,
                # filters=[
                #     ('category', 'is', 'group')
                # ]
            ),
            thread_stack_index
        ]

    def _gui_add_entity_build_fnc(self, *args):
        scr_entities, thread_stack_index = args[0]
        if thread_stack_index != self._index_thread_batch:
            return

        for i_scr_entity in scr_entities:
            self.gui_add_entity(i_scr_entity)

    def do_gui_add_all(self):
        self.restore()
        self.gui_add_entities()

    def get_selected_entities(self):
        return [x.get_gui_dcc_obj(self._namespace) for x in self._prx_tree_view.get_selected_items()]

    def get_assigned_node_paths(self, scr_type_path):
        return self._data_cache_dict[scr_type_path]

    def gui_clear_cache(self):
        self._data_cache_dict.clear()


class _GuiTagOpt(
    _GuiBaseOpt
):
    def __init__(self, window, page, session, scr_stage):
        super(_GuiTagOpt, self).__init__(window, page, session, scr_stage)

        self._prx_tag_filter_view = gui_prx_widgets.PrxTagFilterView()
        self._page._prx_v_splitter_0.add_widget(self._prx_tag_filter_view)

        self._prx_tag_filter_view.get_top_tool_bar().set_expanded(True)

        self._prx_tag_filter_view.connect_check_paths_changed_to(
            self._page.do_gui_node_refresh_by_tag_check
        )

        self._index_thread_batch = 0

        self._data_cache_dict = {}
    
    def restore(self):
        pass
    
    def gui_check_exists(self, path):
        return self._prx_tag_filter_view.check_exists(path)

    def gui_get_one(self, path):
        return self._prx_tag_filter_view.get_one(path)

    # group
    def gui_add_group(self, scr_entity):
        def cache_fnc_():
            # creation time
            if path == '/ctime':
                _src_node_path_set = set(
                    map(
                        lambda _x: _x.path,
                        self._scr_stage.find_all(
                            entity_type=self._scr_stage.EntityTypes.Node,
                            filters=[
                                ('type', 'is', 'node')
                            ]
                        )
                    )
                )
                self._data_cache_dict[path] = _src_node_path_set
                return [_src_node_path_set]
            else:
                _scr_assigns = self._scr_stage.find_all(
                    entity_type=self._scr_stage.EntityTypes.Assign,
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
            _src_node_path_set = data_[0]
            widget._assign_path_set_(_src_node_path_set)
            widget._set_tool_tip_(scr_entity.to_string('user', 'gui_description_chs', 'ctime', 'mtime'))

        path = scr_entity.path

        widget = self._prx_tag_filter_view.create_group(
            scr_entity.path, show_name=scr_entity.gui_name_chs
        )

        widget._set_expanded_(True)

        widget._run_build_extra_use_thread_(cache_fnc_, build_fnc_)
        return widget

    def gui_add_groups(self):
        self._index_thread_batch += 1

        t = self._window.widget._generate_thread_(
            functools.partial(
                self._gui_add_group_cache_fnc, self._index_thread_batch
            ),
            self._gui_add_group_build_fnc,
            post_fnc=self.gui_add_nodes
        )
        t.do_start()

    def _gui_add_group_cache_fnc(self, thread_stack_index):
        if thread_stack_index != self._index_thread_batch:
            return [[], 0]

        return [
            self._scr_stage.find_all(
                self._scr_stage.EntityTypes.Tag,
                filters=[('category', 'is', 'group')]
            ),
            thread_stack_index
        ]

    def _gui_add_group_build_fnc(self, *args):
        scr_entities, thread_stack_index = args[0]
        if thread_stack_index != self._index_thread_batch:
            return

        for i_scr_entity in scr_entities:
            self.gui_add_group(i_scr_entity)

    # node
    def gui_add_node(self, scr_entity):
        def cache_fnc_():
            if path.startswith('/ctime'):
                _src_node_path_set = set(
                    map(
                        lambda _x: _x.path,
                        self._scr_stage.find_all_by_ctime_tag(
                            self._scr_stage.EntityTypes.Node,
                            bsc_core.PthNodeOpt(path).name,
                            filters=[
                                ('type', 'is', 'node')
                            ]
                        )
                    )
                )
                self._data_cache_dict[path] = _src_node_path_set
                return [_src_node_path_set]
            else:
                _scr_assigns = self._scr_stage.find_all(
                    entity_type=self._scr_stage.EntityTypes.Assign,
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
            _src_node_path_set = data_[0]
            widget._assign_path_set_(_src_node_path_set)
            widget._set_tool_tip_(scr_entity.to_string('user', 'gui_description_chs', 'ctime', 'mtime'))

        path = scr_entity.path

        widget = self._prx_tag_filter_view.create_node(
            scr_entity.path, show_name=scr_entity.gui_name_chs
        )
        widget._run_build_extra_use_thread_(cache_fnc_, build_fnc_)
        return widget

    def gui_add_nodes(self):
        self._index_thread_batch += 1

        t = self._window.widget._generate_thread_(
            functools.partial(
                self._gui_add_node_cache_fnc, self._index_thread_batch
            ),
            self._gui_add_node_build_fnc
        )
        t.do_start()

    def _gui_add_node_cache_fnc(self, thread_stack_index):
        if thread_stack_index != self._index_thread_batch:
            return [[], 0]

        return [
            self._scr_stage.find_all(
                self._scr_stage.EntityTypes.Tag,
                filters=[('category', 'is', 'node')]
            ),
            thread_stack_index
        ]

    def _gui_add_node_build_fnc(self, *args):
        scr_entities, thread_stack_index = args[0]
        if thread_stack_index != self._index_thread_batch:
            return

        for i_scr_entity in scr_entities:
            self.gui_add_node(i_scr_entity)

    # main
    def do_gui_add_all(self):
        self.restore()
        self.gui_add_groups()

    def get_all_checked_node_paths(self):
        return self._prx_tag_filter_view.get_all_checked_node_paths()

    def apply_intersection_paths(self, path_set):
        self._prx_tag_filter_view.apply_intersection_paths(path_set)

    def get_assigned_node_paths(self, scr_tag_path):
        return self._data_cache_dict[scr_tag_path]

    def gui_clear_cache(self):
        self._data_cache_dict.clear()


class _GuiNodeOpt(
    _GuiBaseOpt,
    gui_prx_abstracts.AbsGuiPrxListViewOpt
):
    GUI_NAMESPACE = 'node'

    CHUNK_SIZE_MINIMUM = 32
    THREAD_MAXIMUM = 64

    def gui_register(self, path, qt_item):
        self._item_dict[path] = qt_item
        # prx_item.set_gui_attribute('path', path)

    def __init__(self, window, page, session, scr_stage):
        super(_GuiNodeOpt, self).__init__(window, page, session, scr_stage)

        self._item_frame_size = self._session.gui_configure.get('item_frame_size')
        self._item_icon_frame_size = self._session.gui_configure.get('item_icon_frame_size')
        self._item_icon_size = self._session.gui_configure.get('item_icon_size')

        self._prx_list_view = gui_prx_widgets.PrxListView()
        self._page._prx_h_splitter_0.add_widget(self._prx_list_view)

        self._prx_list_view.get_check_tool_box().set_visible(True)
        self._prx_list_view.get_scale_switch_tool_box().set_visible(True)
        self._prx_list_view.get_sort_switch_tool_box().set_visible(True)
        self._prx_list_view.set_filter_entry_tip('filter by keyword ...')
        self._prx_list_view.set_item_event_override_flag(True)
        #
        self._prx_list_view.get_top_tool_bar().set_expanded(True)
        self._prx_list_view.set_item_frame_size_basic(*self._item_frame_size)
        self._prx_list_view.set_item_icon_frame_size(*self._item_icon_frame_size)
        self._prx_list_view.set_item_icon_size(*self._item_icon_size)
        self._prx_list_view.set_item_frame_draw_enable(True)
        # self._prx_list_view.set_item_name_frame_draw_enable(True)
        self._prx_list_view.set_item_names_draw_range([None, 1])
        # self._prx_list_view.set_item_image_frame_draw_enable(True)

        self._init_list_view_opt_(self._prx_list_view, self.GUI_NAMESPACE)

        self._running_threads_stacks = []

        self._window.connect_window_close_to(
            self.restore_thread_stack
        )

        self._type_cache_node_paths = []
        self._tag_cache_node_paths = []

        self._data_cache_dict = {}

    def restore_cache(self):
        self._type_cache_node_paths = []
        self._tag_cache_node_paths = []

    def restore_thread_stack(self):
        if self._running_threads_stacks:
            [i.do_quit() for i in self._running_threads_stacks]

        self._running_threads_stacks = []

    # node
    def gui_add_nodes(self, scr_node_paths, thread_stack_index):
        scr_node_paths = bsc_core.RawTextsMtd.sort_by_number(scr_node_paths)

        if thread_stack_index != self._index_thread_batch:
            return

        scr_node_paths_map = bsc_core.RawListMtd.split_to(
            scr_node_paths, self.THREAD_MAXIMUM, self.CHUNK_SIZE_MINIMUM
        )

        ts = []
        for i_scr_node_paths in scr_node_paths_map:
            i_r = self._window.widget._generate_thread_(
                functools.partial(
                    self._gui_add_nodes_cache_fnc, i_scr_node_paths, thread_stack_index
                ),
                self._gui_add_nodes_build_fnc
            )
            ts.append(i_r)
        #
        [x.do_start() for x in ts]

    def _gui_add_nodes_cache_fnc(self, scr_node_paths, thread_stack_index):
        if thread_stack_index != self._index_thread_batch:
            return [[], 0]

        return [
            [self._scr_stage.get_node(x) for x in scr_node_paths],
            thread_stack_index
        ]

    def _gui_add_nodes_build_fnc(self, *args):
        scr_nodes, thread_stack_index = args[0]
        if thread_stack_index != self._index_thread_batch:
            return

        for i_scr_node in scr_nodes:
            self.gui_add_node(i_scr_node, thread_stack_index)

    def gui_add_node(self, scr_entity, thread_stack_index):
        path = scr_entity.path
        if self.gui_check_exists(path) is True:
            return self.gui_get_one(path)

        qt_item = self._prx_list_view.create_item_()
        qt_item._set_sort_name_key_(scr_entity.gui_name)
        qt_item._set_item_keyword_filter_keys_tgt_([scr_entity.gui_name, scr_entity.gui_name_chs])
        self.gui_register(path, qt_item)

        qt_item._set_item_show_fnc_(
            functools.partial(self._gui_node_show_cache_fnc, qt_item, scr_entity, thread_stack_index),
            self._gui_node_show_build_fnc
        )

    def _gui_node_show_cache_fnc(self, qt_item, scr_entity, thread_stack_index):
        if thread_stack_index != self._index_thread_batch:
            return [[], 0]

        path = scr_entity.path

        if path in self._data_cache_dict:
            data = self._data_cache_dict[path]
            return [[qt_item, scr_entity, data], thread_stack_index]

        scr_assigns = self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Assign,
            [
                ('type', 'is', 'tag_assign'),
                ('source', 'is', scr_entity.path),
            ]
        )
        tag_dict = {}
        for i_scr_assign in scr_assigns:
            i_scr_tag_path = i_scr_assign.target
            i_scr_tag = self._scr_stage.get_entity(
                self._scr_stage.EntityTypes.Tag, i_scr_tag_path
            )
            i_scr_tag_group = self._scr_stage.get_entity(
                self._scr_stage.EntityTypes.Tag, bsc_core.PthNodeMtd.get_dag_parent_path(i_scr_tag_path)
            )
            tag_dict[i_scr_tag_group.gui_name_chs] = i_scr_tag.gui_name_chs

        tag_dict[bsc_core.auto_unicode('创建时间')] = scr_entity.ctime.strftime(
            '%Y-%m-%d %H:%M:%S'
        )

        scr_properties = self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Property,
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
            [qt_item, scr_entity, [tag_dict, property_dict]], thread_stack_index
        ]

    def _gui_node_show_build_fnc(self, *args):
        build_data, thread_stack_index = args[0]
        if thread_stack_index != self._index_thread_batch:
            return

        qt_item, scr_entity, data = build_data

        qt_item_widget = gui_qt_widgets.QtItemWidgetForList()
        self._prx_list_view.assign_item_widget(qt_item, qt_item_widget)

        tag_dict, property_dict = data
        qt_item_widget._set_index_(scr_entity.id)
        qt_item_widget._set_name_text_(scr_entity.gui_name_chs or scr_entity.gui_name)
        qt_item_widget._set_name_dict_(tag_dict)

        if 'video' in property_dict:
            video_path = property_dict['video']
            if 'thumbnail' in property_dict:
                thumbnail_path = property_dict['thumbnail']
                qt_item_widget._set_video_path_(
                    video_path, thumbnail_path
                )
            else:
                qt_item_widget._set_video_path_(video_path)
            # qt_item_widget._set_video_auto_play_flag_(True)

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

        self._index_thread_batch += 1

        t = self._window.widget._generate_thread_(
            functools.partial(
                self._gui_add_nodes_by_type_cache_fnc, scr_type_paths, self._index_thread_batch
            ),
            self._gui_add_nodes_by_type_build_fnc
        )

        t.do_start()

    def _gui_add_nodes_by_type_cache_fnc(self, scr_type_paths, thread_stack_index):
        if thread_stack_index != self._index_thread_batch:
            return [[], 0]

        all_sets = []
        for i_scr_type_path in scr_type_paths:
            i_scr_node_paths = self._page._gui_type_opt.get_assigned_node_paths(i_scr_type_path)
            all_sets.append(i_scr_node_paths)

        return [
            list(set.union(*all_sets)),
            thread_stack_index
        ]

    def _gui_add_nodes_by_type_build_fnc(self, *args):
        scr_node_paths, thread_stack_index = args[0]
        if thread_stack_index != self._index_thread_batch:
            return

        self._type_cache_node_paths = scr_node_paths

        self._page._gui_tag_opt.apply_intersection_paths(set(self._type_cache_node_paths))

        if self._tag_cache_node_paths:
            scr_node_paths_ = list(set.intersection(set(self._tag_cache_node_paths), set(self._type_cache_node_paths)))
        else:
            scr_node_paths_ = scr_node_paths

        self.gui_add_nodes(scr_node_paths_, thread_stack_index)

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

                self._index_thread_batch += 1

                self.gui_add_nodes(self._type_cache_node_paths, self._index_thread_batch)

    def _gui_add_nodes_by_tag_paths(self, scr_tag_paths):
        self.restore_thread_stack()

        self._index_thread_batch += 1

        t = self._window.widget._generate_thread_(
            functools.partial(
                self._gui_add_nodes_by_tag_cache_fnc, scr_tag_paths, self._index_thread_batch
            ),
            self._gui_add_nodes_by_tag_build_fnc
        )
        t.do_start()

    def _gui_add_nodes_by_tag_cache_fnc(self, scr_tag_paths, thread_stack_index):
        if thread_stack_index != self._index_thread_batch:
            return [[], 0]

        dict_ = {}
        for i_scr_tag_path in scr_tag_paths:
            dict_.setdefault(
                bsc_core.PthNodeOpt(i_scr_tag_path).get_parent_path(),
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
            thread_stack_index
        ]

    def _gui_add_nodes_by_tag_build_fnc(self, *args):
        scr_node_paths, thread_stack_index = args[0]
        if thread_stack_index != self._index_thread_batch:
            return

        self._tag_cache_node_paths = scr_node_paths

        if self._type_cache_node_paths:
            scr_node_paths_ = list(set.intersection(set(self._tag_cache_node_paths), set(self._type_cache_node_paths)))
        else:
            scr_node_paths_ = scr_node_paths

        self.gui_add_nodes(scr_node_paths_, thread_stack_index)

    def gui_clear_cache(self):
        self._data_cache_dict.clear()


class AbsPrxPageForResource(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget

    def do_gui_node_refresh_by_type_selection(self):
        self._gui_node_opt.do_gui_add_all_by_type(
            [x.path for x in self._gui_type_opt.get_selected_entities()]
        )

    def do_gui_node_refresh_by_tag_check(self):
        self._gui_node_opt.do_gui_add_all_by_tag(
            self._gui_tag_opt.get_all_checked_node_paths()
        )

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForResource, self).__init__(*args, **kwargs)

        self._window = window
        self._session = session

        self._scr_stage = qsm_scr_core.Stage(
            'Z:/libraries/screw/.database/node.db'
            # 'Z:/libraries/media/.database/video.db'
        )
        self._scr_stage.connect()

        self._window.connect_window_close_to(self._scr_stage.close)

        self.gui_setup_page()

    def gui_setup_page(self):
        qt_v_lot_0 = gui_qt_widgets.QtVBoxLayout(self._qt_widget)
        qt_v_lot_0.setContentsMargins(*[0]*4)
        qt_v_lot_0.setSpacing(2)

        self._top_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        qt_v_lot_0.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_expanded(True)

        prx_sca = gui_prx_widgets.PrxVScrollArea()
        qt_v_lot_0.addWidget(prx_sca.widget)

        self._prx_h_splitter_0 = gui_prx_widgets.PrxHSplitter()
        prx_sca.add_widget(self._prx_h_splitter_0)

        self._prx_v_splitter_0 = gui_prx_widgets.PrxVSplitter()
        self._prx_h_splitter_0.add_widget(self._prx_v_splitter_0)
        self._gui_type_opt = _GuiTypeOpt(self._window, self, self._session, self._scr_stage)
        self._gui_tag_opt = _GuiTagOpt(self._window, self, self._session, self._scr_stage)

        self._gui_node_opt = _GuiNodeOpt(self._window, self, self._session, self._scr_stage)

        self._prx_h_splitter_0.set_fixed_size_at(0, 320)
        self._prx_v_splitter_0.set_fixed_size_at(1, 480)

        self.do_gui_refresh_all()

    def do_gui_refresh_all(self):
        self._gui_type_opt.do_gui_add_all()
        self._gui_tag_opt.do_gui_add_all()
