# coding:utf-8
import copy

import itertools

import functools

import six

import lxbasic.core as bsc_core

import lxbasic.web as bsc_web

import lxbasic.storage as bsc_storage

import lxbasic.pinyin as bsc_pinyin

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.abstracts as gui_prx_abstracts

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_screw.core as qsm_scr_core

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

        self._ts = []
    
    def gui_update_thread_flag(self):
        self._gui_thread_flag += 1

    def gui_run_thread(self, cache_fnc, build_fnc, post_fnc=None):
        t = self._window._qt_widget._generate_thread_(
            cache_fnc,
            build_fnc,
            post_fnc=post_fnc
        )
        return t

    def gui_quit_all_threads(self):
        for seq, i in enumerate(self._ts):
            i.do_quit()
            # del self._ts[seq]

        self._ts = []


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
            [('name', 4), ('count', 1)], 320-48
        )

        self._prx_tree_view.set_filter_entry_tip('filter by keyword ...')

        self._prx_tree_view.get_top_tool_bar().set_expanded(True)

        self._prx_tree_view.connect_item_select_changed_to(
            self._page.do_gui_node_refresh_by_type_selection
        )

        self._init_tree_view_opt_(self._prx_tree_view, self.GUI_NAMESPACE)

        self._data_cache_dict = {}

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

            _scr_assigns = self._page._scr_stage.find_all(
                entity_type=self._page._scr_stage.EntityTypes.Assign,
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
            if gui_thread_flag != self._gui_thread_flag:
                return

            _src_node_path_set = data_[0]
            _count = len(_src_node_path_set)
            prx_item.set_name(str(_count), 1)

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
        prx_item.set_tool_tip(scr_entity.to_description())

        prx_item.set_show_fnc(
            cache_fnc_, build_fnc_
        )
        return prx_item

    def gui_add_entities(self):
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
            self.gui_add_entity(i_scr_entity, gui_thread_flag)

    def do_gui_add_all(self):
        self.restore()
        self.gui_add_entities()

    def get_selected_entities(self):
        return [x.get_gui_dcc_obj(self._namespace) for x in self._prx_tree_view.get_selected_items()]

    def get_assigned_node_paths(self, scr_type_path):
        return self._data_cache_dict[scr_type_path]

    def gui_clear_cache(self):
        self._data_cache_dict.clear()

    def gui_do_close(self):
        pass


class _GuiTagOpt(
    _GuiBaseOpt
):
    def restore(self):
        pass

    def restore_all(self):
        self._prx_tag_input.restore()
        self.gui_clear_cache()

    def gui_clear_cache(self):
        self._data_cache_dict.clear()

    def __init__(self, window, page, session):
        super(_GuiTagOpt, self).__init__(window, page, session)

        self._prx_tag_input = gui_prx_widgets.PrxTagInput()
        self._page._prx_v_splitter_0.add_widget(self._prx_tag_input)

        self._prx_tag_input.get_top_tool_bar().set_expanded(True)

        self._prx_tag_input.connect_check_paths_changed_to(
            self._page.do_gui_node_refresh_by_tag_check
        )

        self._data_cache_dict = {}
    
    def gui_check_exists(self, path):
        return self._prx_tag_input.check_exists(path)

    def gui_get_one(self, path):
        return self._prx_tag_input.get_one(path)

    # entity
    def gui_add_entities(self):
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
            widget._set_tool_tip_(scr_entity.to_description())

        path = scr_entity.path

        gui_name = scr_entity.gui_name
        if self._window._language == 'chs':
            gui_name = scr_entity.gui_name_chs

        widget = self._prx_tag_input.create_group(
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
            widget._set_tool_tip_(scr_entity.to_description())

        path = scr_entity.path

        gui_name = scr_entity.gui_name
        if self._window._language == 'chs':
            gui_name = scr_entity.gui_name_chs

        widget = self._prx_tag_input.create_node(
            scr_entity.path, show_name=gui_name
        )
        t = self.gui_run_thread(cache_fnc_, build_fnc_)
        t.do_start()
        return widget

    # main
    def do_gui_add_all(self):
        self.restore()
        self.gui_add_entities()

    def get_all_checked_node_paths(self):
        return self._prx_tag_input.get_all_checked_node_paths()

    def apply_intersection_paths(self, path_set):
        self._prx_tag_input.apply_intersection_paths(path_set)

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

    def __init__(self, window, page, session):
        super(_GuiNodeOpt, self).__init__(window, page, session)

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

        self._prx_list_view.get_top_tool_bar().set_expanded(True)

        self._prx_list_view.get_filter_tool_box().set_visible(False)
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

        self._window.connect_window_close_to(
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
            data = dict(
                stage=self._page._scr_stage_key,
                path=scr_entity.path,
                gui_name_chs=scr_entity.gui_name_chs,
                file=qt_item_widget._get_property_('rebuild')
            )
            qsm_scr_core.NodeContext.save(data)

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
        path = scr_entity.path
        if self.gui_check_exists(path) is True:
            return self.gui_get_one(path)

        qt_item = self._prx_list_view.create_item_()
        qt_item._set_sort_name_key_(scr_entity.gui_name)
        qt_item._set_item_keyword_filter_keys_tgt_([scr_entity.gui_name, scr_entity.gui_name_chs])
        self.gui_register(path, qt_item)

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

        scr_assigns = self._page._scr_stage.find_all(
            self._page._scr_stage.EntityTypes.Assign,
            [
                ('type', 'is', 'tag_assign'),
                ('source', 'is', scr_entity.path),
            ]
        )
        tag_dict = {}
        for i_scr_assign in scr_assigns:
            i_scr_tag_path = i_scr_assign.target
            i_scr_tag = self._page._scr_stage.get_entity(
                self._page._scr_stage.EntityTypes.Tag, i_scr_tag_path
            )
            i_scr_tag_group = self._page._scr_stage.get_entity(
                self._page._scr_stage.EntityTypes.Tag, bsc_core.PthNodeMtd.get_dag_parent_path(i_scr_tag_path)
            )
            tag_dict[i_scr_tag_group.gui_name_chs] = i_scr_tag.gui_name_chs

        tag_dict[bsc_core.auto_unicode('创建时间')] = scr_entity.ctime.strftime(
            '%Y-%m-%d %H:%M:%S'
        )

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
        qt_item_widget._set_name_text_(scr_entity.gui_name_chs or scr_entity.gui_name)
        qt_item_widget._set_name_dict_(tag_dict)
        qt_item_widget._set_tool_tip_(
            scr_entity.to_description()
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


class AbsPrxPageForManager(
    gui_prx_abstracts.AbsPrxWidget,
    _GuiThreadExtra,
):
    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget

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

    def do_gui_close(self):
        self._scr_stage.close()

    def do_gui_initialize(self, key):
        self._scr_stage_key = key
        self._scr_stage = qsm_scr_core.Stage(self._scr_stage_key)
        self.gui_setup_page()

    def _gui_add_main_tools(self):
        self._maya_status_prx_button = gui_prx_widgets.PrxIconPressButton()
        self._main_prx_tool_box.add_widget(self._maya_status_prx_button)
        self._maya_status_prx_button.set_icon_name('application/maya')
        self._maya_status_prx_button.set_action_enable(False)

    def _gui_add_filter_tools(self):
        self._keyword_set = set()
        self._keyword_pinyin_dict = {}
        self._prx_filter_bar = gui_prx_widgets.PrxFilterBar()
        self._filter_prx_tool_box.add_widget(self._prx_filter_bar)
        
        self._prx_filter_bar._qt_widget._set_input_completion_buffer_fnc_(self._gui_keyword_filter_completion_gain_fnc)
        self._prx_filter_bar._qt_widget.input_value_change_accepted.connect(self._gui_update_keyword_filter_path_set_fnc)
    
    def _gui_keyword_filter_completion_gain_fnc(self, *args, **kwargs):
        keyword = args[0]
        if keyword:
            match_pinyin = bsc_core.PtnFnmatchMtd.filter(
                self._keyword_pinyin_dict.keys(), six.u('*{}*').format(keyword)
            )

            match_chs = [self._keyword_pinyin_dict[x] for x in match_pinyin]

            matches = bsc_core.PtnFnmatchMtd.filter(
                self._keyword_set, six.u('*{}*').format(keyword)
            )
            all_texts = match_chs + matches
            return bsc_core.RawTextsMtd.sort_by_initial(all_texts)[:self.FILTER_MAXIMUM]
        return []

    def _gui_update_keyword_filter_path_set_fnc(self, *args, **kwargs):
        keyword = args[0]
        print keyword

    def _check_maya_web_server_is_in_use(self):
        def cache_fnc_(gui_thread_flag_):
            return [
                bsc_web.WebSocket.check_is_in_use(
                    _lzy_tol_core.MayaWebServerBase.HOST,
                    _lzy_tol_core.MayaWebServerBase.PORT
                ),
                gui_thread_flag_
            ]

        def build_fnc_(data_):
            _boolean, _gui_thread_flag = data_
            if _gui_thread_flag != self._gui_thread_flag:
                return

            self._maya_status_prx_button.set_action_enable(data_[0])
            
        self.gui_update_thread_flag()

        t = self.gui_run_thread(
            functools.partial(cache_fnc_, self._gui_thread_flag),
            build_fnc_
        )

        t.do_start()

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
        super(AbsPrxPageForManager, self).__init__(*args, **kwargs)
        self._init_gui_thread_extra_(window)

        self._window = window
        self._session = session

        self._scr_stage_key = None
        self._scr_stage = None

        self._window.connect_window_close_to(self.do_gui_close)

    def gui_setup_page(self):
        v_qt_lot_0 = gui_qt_widgets.QtVBoxLayout(self._qt_widget)
        v_qt_lot_0.setContentsMargins(*[0]*4)
        v_qt_lot_0.setSpacing(2)

        self._top_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        v_qt_lot_0.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_align_left()
        self._top_prx_tool_bar.set_expanded(True)

        self._main_prx_tool_box = self._top_prx_tool_bar.create_tool_box('main')
        self._gui_add_main_tools()

        self._filter_prx_tool_box = self._top_prx_tool_bar.create_tool_box('filter', size_mode=1)
        self._gui_add_filter_tools()

        prx_sca = gui_prx_widgets.PrxVScrollArea()
        v_qt_lot_0.addWidget(prx_sca.widget)

        self._prx_h_splitter_0 = gui_prx_widgets.PrxHSplitter()
        prx_sca.add_widget(self._prx_h_splitter_0)

        self._prx_v_splitter_0 = gui_prx_widgets.PrxVSplitter()
        self._prx_h_splitter_0.add_widget(self._prx_v_splitter_0)
        self._gui_type_opt = _GuiTypeOpt(self._window, self, self._session)
        self._gui_tag_opt = _GuiTagOpt(self._window, self, self._session)

        self._gui_node_opt = _GuiNodeOpt(self._window, self, self._session)

        self._prx_h_splitter_0.set_fixed_size_at(0, 320)
        self._prx_v_splitter_0.set_fixed_size_at(1, 480)

        self.do_gui_refresh_all()

    def do_gui_refresh_all(self):
        self._gui_update_keyword_filter_texts()
        self._gui_node_opt.restore_all()
        self._gui_type_opt.restore_all()
        self._gui_tag_opt.restore_all()

        self._gui_type_opt.do_gui_add_all()
        self._gui_tag_opt.do_gui_add_all()