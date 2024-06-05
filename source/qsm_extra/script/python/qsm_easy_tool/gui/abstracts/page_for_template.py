# coding:utf-8
import copy
import functools

import six

import lxbasic.core as bsc_core

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
        self._prx_tree_view.connect_item_select_changed_to(
            self._page.do_gui_node_refresh_by_type_selection
        )

        self._init_tree_view_opt_(self._prx_tree_view, self.GUI_NAMESPACE)

        self._index_thread_batch = 0

    def gui_add_group(self, scr_entity):
        def cache_fnc_():
            _scr_assigns = self._scr_stage.find_all(
                entity_type=self._scr_stage.EntityTypes.Assign,
                filters=[
                    ('target', 'startswith', path),
                ]
            )
            # clean duplicate
            _scr_assigns = {i.source: i for i in _scr_assigns}.values()

            return [_scr_assigns]

        def build_fnc_(data_):
            _scr_assigns = data_[0]
            _count = len(_scr_assigns)
            prx_item.set_name(str(_count), 1)

            if _count > 0:
                prx_item.set_enable(True)
            else:
                prx_item.set_checked(False)
                prx_item.set_enable(False)
                prx_item.set_status(
                    prx_item.ValidationStatus.Disable
                )

        path = scr_entity.path

        if self.gui_is_exists(path) is True:
            return self.gui_get(path)

        path_opt = bsc_core.PthNodeOpt(path)
        parent_gui = self.gui_get(path_opt.get_parent_path())

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
            [scr_entity.gui_name, scr_entity.gui_name_chs]
        )
        prx_item.set_tool_tip(scr_entity.to_string())
        #
        # self._prx_tree_view.connect_item_expand_to(
        #     prx_item,
        #     functools.partial(self.refresh_by_category_expanded, prx_item),
        #     time=100
        # )
        #
        prx_item.set_checked(False)
        prx_item.set_expanded(True)
        prx_item.set_show_fnc(
            cache_fnc_, build_fnc_
        )
        return prx_item

    def gui_add_groups(self):
        self._index_thread_batch += 1

        t = gui_qt_core.QtBuildThread(self._prx_tree_view.get_widget())
        t.set_cache_fnc(
            functools.partial(
                self._gui_add_group_cache_fnc, self._index_thread_batch
            )
        )
        t.cache_value_accepted.connect(self._gui_add_group_build_fnc)
        t.run_finished.connect(self.gui_add_nodes)
        #
        t.start()

    def _gui_add_group_cache_fnc(self, thread_stack_index):
        if thread_stack_index != self._index_thread_batch:
            return [[], 0]

        return [
            self._scr_stage.find_all(
                self._scr_stage.EntityTypes.Type,
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

    def gui_add_node(self, scr_entity):
        def cache_fnc_():
            _scr_assigns = self._scr_stage.find_all(
                entity_type=self._scr_stage.EntityTypes.Assign,
                filters=[
                    ('target', 'startswith', path),
                ]
            )
            # clean duplicate
            _scr_assigns = {i.source: i for i in _scr_assigns}.values()

            return [_scr_assigns]

        def build_fnc_(data_):
            _scr_assigns = data_[0]
            _count = len(_scr_assigns)
            prx_item.set_name(str(_count), 1)

        path = scr_entity.path

        if self.gui_is_exists(path) is True:
            return self.gui_get(path)

        path_opt = bsc_core.PthNodeOpt(path)
        parent_gui = self.gui_get(path_opt.get_parent_path())

        gui_name = scr_entity.gui_name
        if self._window._language == 'chs':
            gui_name = scr_entity.gui_name_chs
            # gui_name = six.u('{}({})').format(scr_entity.gui_name_chs, scr_entity.gui_name)

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
            [scr_entity.gui_name, scr_entity.gui_name_chs]
        )
        prx_item.set_tool_tip(scr_entity.to_string())
        #
        # self._prx_tree_view.connect_item_expand_to(
        #     prx_item,
        #     functools.partial(self.refresh_by_category_expanded, prx_item),
        #     time=100
        # )
        #
        prx_item.set_checked(False)
        prx_item.set_show_fnc(
            cache_fnc_, build_fnc_
        )
        return prx_item

    def gui_add_nodes(self):
        self._index_thread_batch += 1

        t = gui_qt_core.QtBuildThread(self._prx_tree_view.get_widget())
        t.set_cache_fnc(
            functools.partial(
                self._gui_add_node_cache_fnc, self._index_thread_batch
            )
        )
        t.cache_value_accepted.connect(self._gui_add_node_build_fnc)
        #
        t.start()

    def _gui_add_node_cache_fnc(self, thread_stack_index):
        if thread_stack_index != self._index_thread_batch:
            return [[], 0]

        return [
            self._scr_stage.find_all(
                self._scr_stage.EntityTypes.Type,
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

    def do_gui_add_all(self):
        self.restore()
        self.gui_add_groups()

    def get_selected_entities(self):
        return [x.get_gui_dcc_obj(self._namespace) for x in self._prx_tree_view.get_selected_items()]


class _GuiTagOpt(
    _GuiBaseOpt,
    gui_prx_abstracts.AbsGuiPrxTreeViewOpt
):
    def __init__(self, window, page, session, scr_stage):
        super(_GuiTagOpt, self).__init__(window, page, session, scr_stage)

        self._prx_tree_view = gui_prx_widgets.PrxTreeView()
        self._page._prx_v_splitter_0.add_widget(self._prx_tree_view)
        self._prx_tree_view.create_header_view(
            [('name', 4), ('count', 1)], 240-48
        )
        self._prx_tree_view.set_selection_disable()

        self._init_tree_view_opt_(self._prx_tree_view, self.GUI_NAMESPACE)

        self._index_thread_batch = 0

    def gui_add_group(self, scr_entity):
        path = scr_entity.path

        if self.gui_is_exists(path) is True:
            return self.gui_get(path)

        path_opt = bsc_core.PthNodeOpt(path)
        parent_gui = self.gui_get(path_opt.get_parent_path())

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
            [scr_entity.gui_name, scr_entity.gui_name_chs]
        )
        prx_item.set_tool_tip(scr_entity.to_string())
        #
        # self._prx_tree_view.connect_item_expand_to(
        #     prx_item,
        #     functools.partial(self.refresh_by_category_expanded, prx_item),
        #     time=100
        # )
        #
        prx_item.set_checked(False)
        prx_item.set_expanded(True)
        return prx_item

    def gui_add_groups(self):
        self._index_thread_batch += 1

        t = gui_qt_core.QtBuildThread(self._prx_tree_view.get_widget())
        t.set_cache_fnc(
            functools.partial(
                self._gui_add_group_cache_fnc, self._index_thread_batch
            )
        )
        t.cache_value_accepted.connect(self._gui_add_group_build_fnc)
        t.run_finished.connect(self.gui_add_nodes)
        #
        t.start()

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

    def gui_add_node(self, scr_entity):
        path = scr_entity.path

        if self.gui_is_exists(path) is True:
            return self.gui_get(path)

        path_opt = bsc_core.PthNodeOpt(path)
        parent_gui = self.gui_get(path_opt.get_parent_path())

        gui_name = scr_entity.gui_name
        if self._window._language == 'chs':
            gui_name = scr_entity.gui_name_chs
            # gui_name = six.u('{}({})').format(scr_entity.gui_name_chs, scr_entity.gui_name)

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
            [scr_entity.gui_name, scr_entity.gui_name_chs]
        )
        prx_item.set_tool_tip(scr_entity.to_string())
        #
        # self._prx_tree_view.connect_item_expand_to(
        #     prx_item,
        #     functools.partial(self.refresh_by_category_expanded, prx_item),
        #     time=100
        # )
        #
        prx_item.set_checked(False)
        return prx_item

    def gui_add_nodes(self):
        self._index_thread_batch += 1

        t = gui_qt_core.QtBuildThread(self._prx_tree_view.get_widget())
        t.set_cache_fnc(
            functools.partial(
                self._gui_add_node_cache_fnc, self._index_thread_batch
            )
        )
        t.cache_value_accepted.connect(self._gui_add_node_build_fnc)
        #
        t.start()

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

    def do_gui_add_all(self):
        self.restore()
        self.gui_add_groups()


class _GuiNodeOpt(
    _GuiBaseOpt,
    gui_prx_abstracts.AbsGuiPrxListViewOpt
):
    GUI_NAMESPACE = 'node'

    THREAD_STEP = 32

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

        # self._prx_list_view.get_check_tool_box().set_visible(True)
        self._prx_list_view.get_scale_switch_tool_box().set_visible(True)
        self._prx_list_view.get_sort_switch_tool_box().set_visible(True)
        self._prx_list_view.set_filter_entry_tip('filter by keyword ...')
        #
        self._prx_list_view.get_top_tool_bar().set_expanded(True)
        self._prx_list_view.set_item_frame_size_basic(*self._item_frame_size)
        self._prx_list_view.set_item_icon_frame_size(*self._item_icon_frame_size)
        self._prx_list_view.set_item_icon_size(*self._item_icon_size)
        self._prx_list_view.set_item_frame_draw_enable(True)
        # self._prx_list_view.set_item_icon_frame_draw_enable(True)
        # self._prx_list_view.set_item_name_frame_draw_enable(True)
        self._prx_list_view.set_item_names_draw_range([None, 1])
        # self._prx_list_view.set_item_image_frame_draw_enable(True)

        self._init_list_view_opt_(self._prx_list_view, self.GUI_NAMESPACE)

        self._scr_type_paths = []

        self._running_threads_stacks = []

        self._window.connect_window_close_to(
            self.restore_thread_stack
        )

    def do_gui_add_all(self, scr_entities):
        self._gui_add_nodes_auto(scr_entities)

    def restore_thread_stack(self):
        if self._running_threads_stacks:
            [i.do_quit() for i in self._running_threads_stacks]
        #
        self._running_threads_stacks = []

    def _gui_add_nodes_auto(self, scr_entities):
        scr_types = []
        for i_scr_entity in scr_entities:
            i_path = i_scr_entity.path
            i_scr_types = self._scr_stage.find_all(
                self._scr_stage.EntityTypes.Type,
                filters=[
                    ('path', 'startswith', i_path),
                    ('type', 'is', 'node')
                ]
            )
            scr_types.extend(i_scr_types)
        # clean duplicate
        scr_types = {i.path: i for i in scr_types}.values()
        self._gui_add_nodes_by_types(scr_types)

    def _gui_add_nodes_by_types(self, scr_types):
        self.restore_thread_stack()

        self._index_thread_batch += 1

        scr_type_paths_pre = set(self._scr_type_paths)
        self._scr_type_paths = set([x.path for x in scr_types])
        if self._scr_type_paths != scr_type_paths_pre:
            path_added = self._scr_type_paths-scr_type_paths_pre
            path_deleted = scr_type_paths_pre-self._scr_type_paths
            if path_deleted:
                path_added = self._scr_type_paths
                self.restore()

            if path_added:
                ts = gui_qt_core.QtBuildThreadStack(self._window.widget)
                self._running_threads_stacks.append(ts)
                for i_scr_type_path in path_added:
                    ts.register(
                        cache_fnc=functools.partial(
                            self._gui_add_nodes_by_type_cache_fnc, i_scr_type_path, self._index_thread_batch
                        ),
                        build_fnc=self._gui_add_nodes_by_type_build_fnc
                    )

                ts.do_start()

                # self._window.connect_window_close_to(quit_fnc_)

    def _gui_add_nodes_by_type_cache_fnc(self, scr_type_path, thread_stack_index):
        if thread_stack_index != self._index_thread_batch:
            return [[], 0]

        scr_assigns = self._scr_stage.find_all(
            entity_type=self._scr_stage.EntityTypes.Assign,
            filters=[
                ('target', 'is', scr_type_path),
            ]
        )

        return [
            scr_assigns,
            thread_stack_index
        ]

    def _gui_add_nodes_by_type_build_fnc(self, *args):
        scr_assigns, thread_stack_index = args[0]
        if thread_stack_index != self._index_thread_batch:
            return

        self.gui_add_nodes(scr_assigns, thread_stack_index)
        # for i_scr_assign in scr_assigns:
        #     i_scr_node = self._scr_stage.get_node(
        #         i_scr_assign.source
        #     )
        #     self.gui_add_node(i_scr_node)

    def gui_add_nodes(self, scr_assigns, thread_stack_index):
        if thread_stack_index != self._index_thread_batch:
            return

        scr_assigns_map = bsc_core.RawListMtd.grid_to(
            scr_assigns, self.THREAD_STEP
        )

        ts = gui_qt_core.QtBuildThreadStack(self._window.widget)
        self._running_threads_stacks.append(ts)
        for i_scr_assigns in scr_assigns_map:
            ts.register(
                cache_fnc=functools.partial(
                    self._gui_add_nodes_cache_fnc, i_scr_assigns, thread_stack_index
                ),
                build_fnc=self._gui_add_nodes_build_fnc
            )
        #
        ts.do_start()

    def _gui_add_nodes_cache_fnc(self, scr_assigns, thread_stack_index):
        if thread_stack_index != self._index_thread_batch:
            return [[], 0]

        return [
            [self._scr_stage.get_node(x.source) for x in scr_assigns],
            thread_stack_index
        ]

    def _gui_add_nodes_build_fnc(self, *args):
        scr_nodes, thread_stack_index = args[0]
        if thread_stack_index != self._index_thread_batch:
            return

        for i_scr_node in scr_nodes:
            self.gui_add_node(i_scr_node)

    def gui_add_node(self, scr_entity):
        path = scr_entity.path
        if self.gui_is_exists(path) is True:
            return self.gui_get(path)

        qt_item = self._prx_list_view.create_item_()
        qt_item._set_sort_name_key_(scr_entity.gui_name)
        self.gui_register(path, qt_item)

        qt_item._set_item_show_fnc_(
            functools.partial(self._gui_node_show_cache_fnc, qt_item, scr_entity),
            self._gui_node_show_build_fnc
        )

    def _gui_node_show_cache_fnc(self, qt_item, scr_entity):
        return [
            qt_item, scr_entity
        ]

    def _gui_node_show_build_fnc(self, *args):
        qt_item, scr_entity = args[0]
        prx_item_widget = self._prx_list_view.create_item_widget_(qt_item)

        prx_item_widget.set_name(scr_entity.gui_name)
        prx_item_widget.set_gui_attribute('path', scr_entity.path)

        # prx_item_widget.set_check_enable(True)
        prx_item_widget.set_index_draw_enable(True)

        name_dict = dict(
            name=scr_entity.gui_name
        )
        prx_item_widget.set_name_dict(name_dict)

        prx_item_widget.set_image(
            'Z:/projects/QSM_TST/workarea/user.nothings/dev.developing/resource_manager/.snapshot/QSM_TST.dev.developing.resource_manager.v003.jpg'
        )

        prx_item_widget.refresh_widget_force()


class AbsPrxPageForTemplate(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget

    def do_gui_node_refresh_by_type_selection(self):
        scr_entities = self._gui_type_opt.get_selected_entities()
        if scr_entities:
            self._gui_node_opt.do_gui_add_all(scr_entities)

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForTemplate, self).__init__(*args, **kwargs)

        self._window = window
        self._session = session

        self._scr_stage = qsm_scr_core.Stage(
            'Z:/libraries/screw/.database/easy-template.db'
        )
        self._scr_stage.connect()

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
        self._prx_v_splitter_0.set_fixed_size_at(1, 240)

        self.do_gui_refresh_all()

    def do_gui_refresh_all(self):
        self._gui_type_opt.do_gui_add_all()
        self._gui_tag_opt.do_gui_add_all()
