# coding:utf-8
from __future__ import print_function

import collections

import copy

import functools

import six

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.pinyin as bsc_pinyin

import lxbasic.session as bsc_session

import lxgui.qt.core as gui_qt_core

import lxgui.qt.view_widgets as gui_qt_vew_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_screw.core as qsm_scr_core


class _GuiThreadExtra(object):
    def _init_gui_thread_extra_(self, window):
        self._window = window
        self._gui_thread_flag = 0

    def gui_update_thread_flag(self):
        self._gui_thread_flag += 1

    def gui_generate_thread(self, cache_fnc, build_fnc, post_fnc=None):
        t = self._window._qt_widget._generate_thread_(
            cache_fnc,
            build_fnc,
            post_fnc=post_fnc
        )
        return t


class _GuiBaseOpt(
    # object,
    _GuiThreadExtra
):
    GUI_NAMESPACE = None

    def __init__(self, window, page, session):
        self._init_gui_thread_extra_(window)

        self._window = window
        self._page = page
        self._session = session

        self._gui_thread_flag = 0

    def generate_scr_entity_type_menu_content(self, scr_entity_type):
        scr_stage_type = self._page._scr_stage.type
        scr_stage_name = self._page._scr_stage.key
        options = []
        c = self._window._configure.get(
            'entity-type-actions.{}.{}.option-hooks'.format(scr_stage_type, scr_entity_type)
        )
        if c:
            for i in c:
                # update override options when var is dict
                if isinstance(i, dict):
                    i_key = list(i.keys())[0]
                    i_value = list(i.values())[0]
                else:
                    i_key = i
                    i_value = {}
                # update option from database
                i_kwargs = dict(
                    option_hook_key=i_key,
                    stage_name=scr_stage_name,
                    window_unique_id=self._window.get_window_unique_id(),
                    entity_type=scr_entity_type,
                )
                i_kwargs.update(**{k: v for k, v in i_value.items() if v})
                options.append(
                    bsc_core.ArgDictStringOpt(i_kwargs).to_string(),
                )
            return bsc_session.OptionHook.generate_menu_content(options, self._window._language)

    def generate_scr_entity_menu_content(self, scr_entity, extra_key=None):
        scr_stage_type = self._page._scr_stage.type
        scr_stage_name = self._page._scr_stage.key
        options = []

        cfg_key = 'entity-actions.{}.{}.option-hooks'.format(scr_stage_type, scr_entity.entity_type)
        if extra_key is not None:
            cfg_key = 'entity-actions.{}.{}.{}.option-hooks'.format(scr_stage_type, scr_entity.entity_type, extra_key)

        c = self._window._configure.get(cfg_key)
        if c:
            for i in c:
                if isinstance(i, dict):
                    i_key = list(i.keys())[0]
                    i_value = list(i.values())[0]
                else:
                    i_key = i
                    i_value = {}
                #
                i_kwargs = dict(
                    option_hook_key=i_key,
                    stage_name=scr_stage_name,
                    window_unique_id=self._window.get_window_unique_id(),
                    entity_type=scr_entity.entity_type,
                    entity=scr_entity.path,
                )
                i_kwargs.update(**{k: v for k, v in i_value.items() if v})
                options.append(
                    bsc_core.ArgDictStringOpt(i_kwargs).to_string(),
                )
            return bsc_session.OptionHook.generate_menu_content(options, self._window._language)

    def gui_update_thread_flag(self):
        self._gui_thread_flag += 1
        return self._gui_thread_flag

    def gui_generate_thread(self, cache_fnc, build_fnc, post_fnc=None):
        t = self._window._qt_widget._generate_thread_(
            cache_fnc,
            build_fnc,
            post_fnc=post_fnc
        )
        return t


class _GuiTypeOpt(
    _GuiBaseOpt
):
    def restore(self):
        self._qt_tree_widget._view_model.restore()

    def restore_all(self):
        self.restore()
        self.gui_clear_cache()

    def gui_clear_cache(self):
        self._leaf_entity_path_set.clear()

    def gui_do_close(self):
        pass

    def __init__(self, window, page, session):
        super(_GuiTypeOpt, self).__init__(window, page, session)

        self._qt_tree_widget = gui_qt_vew_widgets.QtTreeWidget()
        self._page._prx_v_splitter_0.add_widget(self._qt_tree_widget)

        self._qt_tree_widget._set_item_sort_enable_(True)
        # self._qt_tree_widget._set_item_check_enable_(True)
        self._qt_tree_widget._view_model.set_item_color_enable(True)
        self._qt_tree_widget._view_model.set_item_drop_enable(True)

        menu_content = self.generate_scr_entity_type_menu_content(self._page._scr_stage.EntityTypes.Type)
        if menu_content:
            self._qt_tree_widget._view_model.set_menu_content(menu_content)

        self._qt_tree_widget.refresh.connect(self.do_gui_refresh_all)
        self._qt_tree_widget._view.item_select_changed.connect(
            self._page.do_gui_node_refresh_by_type_select_or_check
        )
        self._qt_tree_widget._view.item_check_changed.connect(
            self._page.do_gui_node_refresh_by_type_select_or_check
        )

        self._leaf_entity_path_set = set()

    def gui_add_all_entities(self):
        self.gui_update_thread_flag()

        trd = self._qt_tree_widget._view._generate_thread_(
            functools.partial(
                self._gui_add_entity_cache_fnc, self._gui_thread_flag
            ),
            self._gui_add_entity_build_fnc
        )

        trd.do_start()

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
            bsc_core.BscNodePath.to_leaf_paths([x.path for x in scr_entities])
        )

        for i_scr_entity in scr_entities:
            if i_scr_entity.path in self._leaf_entity_path_set:
                if i_scr_entity.category == 'group':
                    self.gui_add_entity_as_group(i_scr_entity, gui_thread_flag)
                else:
                    self.gui_add_entity(i_scr_entity, gui_thread_flag)
            else:
                self.gui_add_entity_as_group(i_scr_entity, gui_thread_flag)

    def gui_add_entity_as_group(self, scr_entity, gui_thread_flag):
        def group_cache_fnc_():
            _menu_content = self.generate_scr_entity_menu_content(scr_entity, extra_key='group')
            return [
                _menu_content
            ]

        def group_build_fnc_(data_):
            if gui_thread_flag is not None:
                if gui_thread_flag != self._gui_thread_flag:
                    return

            if data_:
                _menu_content = data_[0]

                qt_item._item_model.set_menu_content(_menu_content)

                qt_item._item_model.refresh_force()

        path = scr_entity.path
        name = bsc_core.BscNodePath.to_dag_name(path)

        flag, qt_item = self._qt_tree_widget._view_model.create_item(path)

        qt_item._scr_entity = scr_entity

        gui_name = scr_entity.gui_name
        if self._window._language == 'chs':
            gui_name = scr_entity.gui_name_chs

        # qt_item._item_model.set_type(scr_entity.entity_type)
        qt_item._item_model.set_name(gui_name)
        qt_item._item_model.set_icon_name(scr_entity.gui_icon_name)
        qt_item._item_model.set_sort_dict(
            dict(
                gui_name=scr_entity.gui_name,
                gui_name_chs=scr_entity.gui_name_chs,
            )
        )
        qt_item._item_model.register_keyword_filter_keys(
            [scr_entity.gui_name, scr_entity.gui_name_chs]
        )
        qt_item._item_model.set_tool_tip(scr_entity.to_description(self._window._language))
        qt_item.setExpanded(True)
        trd = self._qt_tree_widget._view._generate_thread_(group_cache_fnc_, group_build_fnc_)
        trd.do_start()

    def gui_add_entity(self, scr_entity, gui_thread_flag):
        def node_cache_fnc_():
            if path == '/unspecified':
                _all_scr_node_path_set = set(
                    map(
                        lambda _x: _x.path,
                        self._page._scr_stage.find_all(
                            entity_type=self._page._scr_stage.EntityTypes.Node,
                            filters=[
                                ('type', 'is', 'node'),
                                ('lock', 'is', False)
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
                                ('type', 'is', 'type_assign'),
                                ('lock', 'is', False)
                            ]
                        )
                    )
                )

                _src_node_path_set = _all_scr_node_path_set-_all_assigned_node_scr_path_set

                _menu_content = None
            elif path == '/lock':
                _scr_nodes_lock = self._page._scr_stage.find_all(
                    entity_type=self._page._scr_stage.EntityTypes.Node,
                    filters=[
                        ('lock', 'is', True),
                    ]
                )
                _src_node_path_set = set([x.path for x in _scr_nodes_lock])

                _menu_content = None
            else:
                _scr_assigns = self._page._scr_stage.find_all(
                    entity_type=self._page._scr_stage.EntityTypes.Assign,
                    filters=[
                        ('type', 'is', 'type_assign'),
                        ('lock', 'is', False),
                        ('target', 'is', path),
                    ]
                )
                # clean duplicate
                _src_node_path_set = set([x.source for x in _scr_assigns])

                if scr_entity.kind == 'unavailable':
                    _menu_content = None
                else:
                    _menu_content = self.generate_scr_entity_menu_content(scr_entity, extra_key='node')
            return [_src_node_path_set, _menu_content]

        def node_build_fnc_(data_):
            if gui_thread_flag is not None:
                if gui_thread_flag != self._gui_thread_flag:
                    return

            if data_:
                _src_node_path_set, _menu_content = data_
                qt_item._item_model.set_assign_path_set(_src_node_path_set)
                qt_item._item_model._update_assign_path_set_to_ancestors()

                qt_item._item_model.set_menu_content(_menu_content)

                qt_item._item_model.refresh_force()

        path = scr_entity.path
        name = bsc_core.BscNodePath.to_dag_name(path)

        flag, qt_item = self._qt_tree_widget._view_model.create_item(path)

        qt_item._scr_entity = scr_entity

        gui_name = scr_entity.gui_name
        if self._window._language == 'chs':
            gui_name = scr_entity.gui_name_chs

        # qt_item._item_model.set_type(scr_entity.entity_type)
        qt_item._item_model.set_name(gui_name)
        qt_item._item_model.set_icon_name(scr_entity.gui_icon_name)
        qt_item._item_model.set_sort_dict(
            dict(
                gui_name=scr_entity.gui_name,
                gui_name_chs=scr_entity.gui_name_chs,
            )
        )
        qt_item._item_model.register_keyword_filter_keys(
            [scr_entity.gui_name, scr_entity.gui_name_chs]
        )
        qt_item._item_model.set_tool_tip(scr_entity.to_description(self._window._language))

        trd = self._qt_tree_widget._view._generate_thread_(node_cache_fnc_, node_build_fnc_)
        trd.do_start()

    def gui_create_entity_as_group(self, scr_entity):
        self.gui_add_entity_as_group(scr_entity, None)

    def gui_create_entity(self, scr_entity):
        self.gui_add_entity(scr_entity, None)

    def gui_update_entities_for(self, scr_entity_paths):

        for i_scr_entity_path in scr_entity_paths:
            i_qt_item = self._qt_tree_widget._view_model._get_item(i_scr_entity_path)
            self.gui_update_entity_for(i_qt_item)

        # update force
        for i_scr_entity_path in [
            '/unspecified',
            '/lock'
        ]:
            if i_scr_entity_path not in scr_entity_paths:
                # update for unspecified latest
                qt_item = self._qt_tree_widget._view_model._get_item(i_scr_entity_path)
                self.gui_update_entity_for(qt_item)

        self._page.do_gui_node_refresh_by_type_select_or_check()

    def gui_update_all_entities(self):
        for i_qt_item in self._qt_tree_widget._view_model.get_all_items():
            if i_qt_item._scr_entity.category == 'node':
                self.gui_update_entity_for(i_qt_item)

        self._page.do_gui_node_refresh_by_type_select_or_check()

    def gui_update_entity_for(self, qt_item):
        def cache_fnc_():
            if scr_entity.path == '/unspecified':
                _all_scr_node_path_set = set(
                    map(
                        lambda _x: _x.path,
                        self._page._scr_stage.find_all(
                            entity_type=self._page._scr_stage.EntityTypes.Node,
                            filters=[
                                ('type', 'is', 'node'),
                                ('lock', 'is', False)
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
                                ('type', 'is', 'type_assign'),
                                ('lock', 'is', False)
                            ]
                        )
                    )
                )
                _src_node_path_set = _all_scr_node_path_set-_all_assigned_node_scr_path_set
            elif scr_entity.path == '/lock':
                _scr_nodes_lock = self._page._scr_stage.find_all(
                    entity_type=self._page._scr_stage.EntityTypes.Node,
                    filters=[
                        ('lock', 'is', True),
                    ]
                )
                _src_node_path_set = set([x.path for x in _scr_nodes_lock])
            else:
                _scr_assigns = self._page._scr_stage.find_all(
                    entity_type=self._page._scr_stage.EntityTypes.Assign,
                    filters=[
                        ('type', 'is', 'type_assign'),
                        ('lock', 'is', False),
                        ('target', 'is', scr_entity.path),
                    ]
                )
                # clean duplicate
                _src_node_path_set = set([x.source for x in _scr_assigns])
            return [_src_node_path_set]

        def build_fnc_(data_):
            if data_:
                _src_node_path_set = data_[0]

                qt_item._item_model.set_assign_path_set(_src_node_path_set)
                qt_item._item_model._update_assign_path_set_to_ancestors()

                qt_item._item_model.refresh_force()

        scr_entity = qt_item._scr_entity

        build_fnc_(cache_fnc_())

    def do_gui_refresh_all(self):
        # restore resource
        self._page._gui_node_opt.restore_all()
        # restore self
        self.restore_all()
        # add all entities
        self.gui_add_all_entities()

    def get_selected_and_checked_entity_paths(self):
        return self._qt_tree_widget._view_model.get_selected_item_paths()

    def get_assign_path_set_for(self, scr_type_path):
        return self._qt_tree_widget._view_model._get_item(scr_type_path)._item_model.get_assign_path_set_for()

    def gui_reload_entity(self, scr_entity_path):
        qt_item = self._qt_tree_widget._view_model._get_item(scr_entity_path)
        if qt_item:
            scr_entity = self._page._scr_stage.get_type(scr_entity_path)
            if scr_entity is None:
                return

            gui_name = scr_entity.gui_name
            if self._window._language == 'chs':
                gui_name = scr_entity.gui_name_chs
            qt_item._item_model.set_name(gui_name)

            qt_item._item_model.refresh_force()


class _GuiTagOpt(
    _GuiBaseOpt
):
    def restore(self):
        self._qt_tag_widget._view_model.restore()

    def restore_all(self):
        self.restore()
        self.gui_clear_cache()

    def gui_clear_cache(self):
        self._leaf_entity_path_set.clear()

    def __init__(self, window, page, session):
        super(_GuiTagOpt, self).__init__(window, page, session)

        self._qt_tag_widget = gui_qt_vew_widgets.QtTagWidget()
        self._page._prx_v_splitter_0.add_widget(self._qt_tag_widget)

        self._qt_tag_widget.refresh.connect(self.do_gui_refresh_all)
        self._qt_tag_widget._view_model.set_item_color_enable(True)
        self._qt_tag_widget._view.check_paths_changed.connect(
            self._page.do_gui_node_refresh_by_tag_check
        )

        self._leaf_entity_path_set = set()

    # entity
    def gui_add_all_entities(self):
        self.gui_update_thread_flag()

        t = self.gui_generate_thread(
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
            ),
            gui_thread_flag
        ]

    def _gui_add_entity_build_fnc(self, *args):
        scr_entities, gui_thread_flag = args[0]
        if gui_thread_flag != self._gui_thread_flag:
            return

        # cache leaf paths
        self._leaf_entity_path_set = set(
            bsc_core.BscNodePath.to_leaf_paths([x.path for x in scr_entities])
        )

        for i_scr_entity in scr_entities:
            if i_scr_entity.path in self._leaf_entity_path_set:
                if i_scr_entity.category == 'group':
                    self.gui_add_entity_as_group(i_scr_entity, gui_thread_flag)
                else:
                    self.gui_add_entity(i_scr_entity, gui_thread_flag)
            else:
                self.gui_add_entity_as_group(i_scr_entity, gui_thread_flag)

    # entity
    def gui_add_entity_as_group(self, scr_entity, gui_thread_flag):
        def group_cache_fnc_():
            if scr_entity.kind == 'unavailable':
                return []

            _menu_content = self.generate_scr_entity_menu_content(scr_entity, extra_key='group')
            return [
                _menu_content
            ]

        def group_build_fnc_(data_):
            if gui_thread_flag is not None:
                if gui_thread_flag != self._gui_thread_flag:
                    return

            if data_:
                _menu_content = data_[0]
                if _menu_content:
                    qt_item._item_model.set_menu_content(_menu_content)
                    qt_item._item_model.refresh_force()

        path = scr_entity.path

        gui_name = scr_entity.gui_name
        if self._window._language == 'chs':
            gui_name = scr_entity.gui_name_chs

        flag, qt_item = self._qt_tag_widget._view_model.create_group_item(path)
        qt_item._scr_entity = scr_entity
        qt_item._item_model.set_name(gui_name)

        qt_item._set_expanded_(True)
        qt_item._set_tool_tip_(scr_entity.to_description(self._window._language))
        t = self._qt_tag_widget._view._generate_thread_(group_cache_fnc_, group_build_fnc_)
        t.do_start()
        return qt_item

    def gui_add_entity(self, scr_entity, gui_thread_flag):
        def cache_fnc_():
            # ctime branch
            if path.startswith('/ctime'):
                _src_node_path_set = set(
                    map(
                        lambda _x: _x.path,
                        self._page._scr_stage.find_all_by_ctime_tag(
                            self._page._scr_stage.EntityTypes.Node,
                            bsc_core.BscNodePathOpt(path).name,
                            filters=[
                                ('type', 'is', 'node'),
                                ('lock', 'is', False),
                            ]
                        )
                    )
                )
                return [_src_node_path_set, None]
            else:
                _scr_assigns = self._page._scr_stage.find_all(
                    entity_type=self._page._scr_stage.EntityTypes.Assign,
                    filters=[
                        ('type', 'is', 'tag_assign'),
                        ('lock', 'is', False),
                        ('target', 'is', scr_entity.path),
                    ]
                )
                # clean duplicate
                _src_node_path_set = set([x.source for x in _scr_assigns])
                # menu
                if scr_entity.kind == 'unavailable':
                    _menu_content = None
                else:
                    _menu_content = self.generate_scr_entity_menu_content(scr_entity, extra_key='node')
                return [_src_node_path_set, _menu_content]

        def build_fnc_(data_):
            if gui_thread_flag is not None:
                if gui_thread_flag != self._gui_thread_flag:
                    return

            _src_node_path_set, _menu_content = data_
            qt_item._set_assign_path_set_(_src_node_path_set)
            qt_item._update_assign_path_set_to_ancestors()
            if _menu_content:
                qt_item._item_model.set_menu_content(_menu_content)

                qt_item._item_model.refresh_force()

        path = scr_entity.path

        gui_name = scr_entity.gui_name
        if self._window._language == 'chs':
            gui_name = scr_entity.gui_name_chs

        flag, qt_item = self._qt_tag_widget._view_model.create_item(path)
        qt_item._scr_entity = scr_entity

        qt_item._item_model.set_name(gui_name)
        qt_item._set_tool_tip_(scr_entity.to_description(self._window._language))
        t = self._qt_tag_widget._view._generate_thread_(cache_fnc_, build_fnc_)
        t.do_start()
        return qt_item

    def gui_create_entity_as_group(self, scr_entity):
        self.gui_add_entity_as_group(scr_entity, None)

    def gui_create_entity(self, scr_entity):
        self.gui_add_entity(scr_entity, None)

    def gui_reload_entity(self, scr_entity_path):
        qt_item = self._qt_tag_widget._view_model._get_item(scr_entity_path)
        if qt_item:
            scr_entity = self._page._scr_stage.get_tag(scr_entity_path)
            if scr_entity is None:
                return

            gui_name = scr_entity.gui_name
            if self._window._language == 'chs':
                gui_name = scr_entity.gui_name_chs

            qt_item._item_model.set_name(gui_name)
            qt_item._item_model.refresh_force()

    def gui_update_entities_for(self, scr_entity_paths):
        for i_scr_entity_path in scr_entity_paths:
            i_qt_item = self._qt_tag_widget._view_model._get_item(i_scr_entity_path)
            self.gui_update_entity_for(i_qt_item)

        self._page.do_gui_node_refresh_by_tag_check()

    def gui_update_entity_for(self, qt_item):
        def cache_fnc_():
            _scr_assigns = self._page._scr_stage.find_all(
                entity_type=self._page._scr_stage.EntityTypes.Assign,
                filters=[
                    ('type', 'is', 'tag_assign'),
                    ('lock', 'is', False),
                    ('target', 'is', scr_entity.path),
                ]
            )
            # clean duplicate
            _src_node_path_set = set([x.source for x in _scr_assigns])
            return [_src_node_path_set]

        def build_fnc_(data_):
            if data_:
                _src_node_path_set = data_[0]

                qt_item._set_assign_path_set_(_src_node_path_set)
                qt_item._update_assign_path_set_to_ancestors()

                qt_item._item_model.refresh_force()

        scr_entity = qt_item._scr_entity
        build_fnc_(cache_fnc_())

    # main
    def do_gui_refresh_all(self):
        self._page._gui_node_opt.restore_all()

        self.restore_all()
        self.gui_add_all_entities()

    def get_check_entity_paths(self):
        return self._qt_tag_widget._view_model.get_all_checked_node_paths()

    def intersection_all_item_assign_path_set(self, path_set):
        self._qt_tag_widget._view_model.intersection_all_item_assign_path_set(path_set)

    def get_assign_path_set_for(self, scr_tag_path):
        return self._qt_tag_widget._view_model._get_item(scr_tag_path)._get_assign_path_set_()

    def gui_do_close(self):
        pass


class _GuiNodeOpt(_GuiBaseOpt):
    CHUNK_SIZE_MINIMUM = 16
    THREAD_MAXIMUM = 128

    def restore(self):
        self._qt_list_widget._view_model.restore()

    def restore_all(self):
        self.restore()
        self.gui_clear_cache()

    def gui_clear_cache(self):
        self._type_cache_node_paths = []
        self._tag_cache_node_paths = []
        self.gui_clear_node_cache()

    def gui_clear_node_cache(self):
        self._data_cache_dict.clear()

    def gui_clear_node_cache_for(self, entity_paths):
        for i_entity_path in entity_paths:
            if i_entity_path in self._data_cache_dict:
                self._data_cache_dict.pop(i_entity_path)

    def generate_menu_content(self):
        pass

    def __init__(self, window, page, session):
        super(_GuiNodeOpt, self).__init__(window, page, session)

        item_frame_size = self._page._scr_stage.configure.get('options.gui_item_frame_size')
        if item_frame_size is None:
            item_frame_size = self._window._gui_configure.get('item_frame_size')

        self._qt_list_widget = gui_qt_vew_widgets.QtListWidget()
        self._page._prx_h_splitter_0.add_widget(self._qt_list_widget)

        self._qt_list_widget._view_model.set_item_frame_size(*item_frame_size)

        self._qt_list_widget._set_item_sort_enable_(True)
        self._qt_list_widget._view_model.set_item_lock_enable(True)
        self._qt_list_widget._set_item_check_enable_(True)
        self._qt_list_widget._view_model.set_item_drag_enable(True)

        self._qt_list_widget._view.press_released.connect(self.do_save_context)
        self._qt_list_widget.refresh.connect(self.do_gui_refresh_all)

        menu_content = self.generate_scr_entity_type_menu_content(self._page._scr_stage.EntityTypes.Node)
        if menu_content:
            self._qt_list_widget._view_model.set_menu_content(menu_content)

        self._type_cache_node_paths = []
        self._tag_cache_node_paths = []

        self._type_node_path_set = set()
        self._tag_node_path_set = set()

        self._node_path_set = set()
        self._node_path_set_pre = set()

        self._node_paths = []

        self._data_cache_dict = {}

    def do_save_context(self):
        qt_items = self._qt_list_widget._view_model.get_selected_items()
        if qt_items:
            qt_item = qt_items[0]
            scr_entity = qt_item._scr_entity
            data_type = qt_item._item_model.get_property('data_type')
            if data_type is not None:
                file_path = qt_item._item_model.get_property(data_type)
                data = dict(
                    stage=self._page._scr_stage_name,
                    path=scr_entity.path,
                    gui_name_chs=scr_entity.gui_name_chs,
                    data_type=data_type,
                    file=file_path
                )
                qsm_scr_core.DataContext.save(data)

    # node
    def gui_update_entities(self, node_path_set, gui_thread_flag):
        self._node_path_set_pre = copy.copy(self._node_path_set)
        if node_path_set:
            self._node_path_set = copy.copy(node_path_set)

            node_path_set_addition = self._node_path_set.difference(self._node_path_set_pre)
            node_path_set_deletion = self._node_path_set_pre.difference(self._node_path_set)

            if node_path_set_deletion:
                for i_scr_node_path in node_path_set_deletion:
                    self._qt_list_widget._view_model._remove_item(i_scr_node_path)

            if node_path_set_addition:
                self.gui_add_entities(list(node_path_set_addition), gui_thread_flag)
        else:
            self._node_path_set.clear()
            self.restore()

    def gui_add_entities(self, scr_node_paths, gui_thread_flag):
        if gui_thread_flag is not None:
            if gui_thread_flag != self._gui_thread_flag:
                return

        self._node_paths = scr_node_paths

        scr_node_paths_map = bsc_core.BscList.split_to(
            self._node_paths, self.THREAD_MAXIMUM, self.CHUNK_SIZE_MINIMUM
        )

        ts = []
        for i_scr_node_paths in scr_node_paths_map:
            i_r = self._qt_list_widget._view._generate_thread_(
                functools.partial(
                    self._gui_add_entities_sub_cache_fnc, i_scr_node_paths, gui_thread_flag
                ),
                self._gui_add_entities_sub_build_fnc,
                post_fnc=self._qt_list_widget._view_model.update_widget
            )
            ts.append(i_r)

        [x.do_start() for x in ts]

    def _gui_add_entities_sub_cache_fnc(self, scr_node_paths, gui_thread_flag):
        if gui_thread_flag is not None:
            if gui_thread_flag != self._gui_thread_flag:
                return [[], 0]

        entity_data = []
        for i_entity_path in scr_node_paths:
            i_scr_entity = self._page._scr_stage.get_node(i_entity_path)
            if i_scr_entity:
                i_source_type = self._page._scr_stage.get_node_parameter(i_entity_path, 'source_type')
                i_is_locked = i_scr_entity.lock
                i_thumbnail_path = self._page._scr_stage.get_node_parameter(i_entity_path, 'thumbnail')
                i_scene_path = self._page._scr_stage.get_node_parameter(i_entity_path, 'scene')
                i_source_path = self._page._scr_stage.get_node_parameter(i_entity_path, 'source')
                entity_data.append(
                    (i_scr_entity, i_source_type, i_is_locked, i_thumbnail_path, i_scene_path, i_source_path)
                )
        return [
            entity_data,
            gui_thread_flag
        ]

    def _gui_add_entities_sub_build_fnc(self, *args):
        entity_data, gui_thread_flag = args[0]

        if gui_thread_flag is not None:
            if gui_thread_flag != self._gui_thread_flag:
                return

        for i_entity_data in entity_data:
            self.gui_add_entity(i_entity_data, gui_thread_flag)

    def gui_add_entity(self, entity_data, gui_thread_flag):
        scr_entity, source_type, is_locked, thumbnail_path, scene_path, source_path = entity_data

        path = scr_entity.path
        name = bsc_core.BscNodePath.to_dag_name(path)

        flag, qt_item = self._qt_list_widget._view_model.create_item(path)
        if flag is False:
            return

        qt_item._scr_entity = scr_entity
        # qt_item._item_model.set_type(scr_entity.type)
        qt_item._item_model.set_sort_dict(
            dict(
                gui_name=scr_entity.gui_name,
                gui_name_chs=scr_entity.gui_name_chs,
            )
        )
        qt_item._item_model.register_keyword_filter_keys(
            [scr_entity.gui_name, scr_entity.gui_name_chs]
        )

        gui_name = scr_entity.gui_name
        if self._window._language == 'chs':
            gui_name = scr_entity.gui_name_chs

        qt_item._item_model.set_name(gui_name)
        qt_item._item_model.set_index(scr_entity.id)
        qt_item._item_model.set_locked(is_locked)

        # add thumbnail
        if thumbnail_path:
            qt_item._item_model.set_image(thumbnail_path, source_type)

        # add drag data
        if scene_path is not None:
            qt_item._item_model.set_drag_data(
                dict(
                    file=scene_path,
                    scr_entity_path=scr_entity.path
                )
            )
        elif source_path is not None:
            qt_item._item_model.set_drag_data(
                dict(
                    file=source_path,
                    scr_entity_path=scr_entity.path
                )
            )

        qt_item._item_model.set_show_fnc(
            functools.partial(self._gui_node_show_cache_fnc, qt_item, scr_entity, gui_thread_flag),
            self._gui_node_show_build_fnc
        )

    def gui_reload_entity(self, scr_entity_path):
        qt_item = self._qt_list_widget._view_model._get_item(scr_entity_path)
        if qt_item:
            scr_entity = self._page._scr_stage.get_node(scr_entity_path)
            if scr_entity is None:
                return

            gui_name = scr_entity.gui_name
            if self._window._language == 'chs':
                gui_name = scr_entity.gui_name_chs
            qt_item._item_model.set_name(gui_name)

            is_locked = scr_entity.lock
            qt_item._item_model.set_locked(is_locked)

            qt_item._item_model.refresh_force()

    def _gui_node_show_cache_fnc(self, qt_item, scr_entity, gui_thread_flag):
        if gui_thread_flag is not None:
            if gui_thread_flag != self._gui_thread_flag:
                return [[], 0]

        path = scr_entity.path

        if path in self._data_cache_dict:
            data = self._data_cache_dict[path]
            return [[qt_item, scr_entity, data], gui_thread_flag]

        tag_dict = collections.OrderedDict()
        tag_scr_assigns = self._page._scr_stage.find_all(
            self._page._scr_stage.EntityTypes.Assign,
            [
                ('type', 'is', 'tag_assign'),
                ('lock', 'is', False),
                ('source', 'is', scr_entity.path),
            ]
        )
        for i_tag_scr_assign in tag_scr_assigns:
            i_scr_tag_path = i_tag_scr_assign.target
            i_scr_tag = self._page._scr_stage.get_entity(
                self._page._scr_stage.EntityTypes.Tag, i_scr_tag_path
            )
            # fixme: tag may be None
            if i_scr_tag is None:
                continue

            i_scr_tag_group = self._page._scr_stage.get_entity(
                self._page._scr_stage.EntityTypes.Tag, bsc_core.BscNodePath.get_dag_parent_path(i_scr_tag_path)
            )
            if self._window._language == 'chs':
                i_key = bsc_core.ensure_string(i_scr_tag_group.gui_name_chs)
                i_value = bsc_core.ensure_string(i_scr_tag.gui_name_chs)
            else:
                i_key = bsc_core.ensure_string(i_scr_tag_group.gui_name)
                i_value = bsc_core.ensure_string(i_scr_tag.gui_name)

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

        menu_content = self.generate_scr_entity_menu_content(scr_entity)
        data = [tag_dict, property_dict, menu_content]
        self._data_cache_dict[path] = data
        return [
            [qt_item, scr_entity, data], gui_thread_flag
        ]

    def _gui_node_show_build_fnc(self, *args):
        def press_dbl_click_fnc_():
            if 'source' in property_dict:
                _file_path = property_dict['source']
                bsc_storage.StgFileOpt(_file_path).start_in_system()

        build_data, gui_thread_flag = args[0]
        if gui_thread_flag is not None:
            if gui_thread_flag != self._gui_thread_flag:
                return

        qt_item, scr_entity, data = build_data
        tag_dict, property_dict, menu_content = data

        if menu_content:
            qt_item._item_model.set_menu_content(menu_content)

        tag_text = '\n'.join(['{}: {}'.format(x_k, x_v) for x_k, x_v in tag_dict.items()])
        qt_item._item_model.set_tool_tip(
            scr_entity.to_description(self._window._language)+'\n'+tag_text
        )

        if 'video' in property_dict:
            qt_item._item_model.set_video(property_dict['video'])
        elif 'audio' in property_dict:
            qt_item._item_model.set_audio(
                property_dict['audio'],
                property_dict['thumbnail']
            )
        elif 'image_sequence' in property_dict:
            fps = property_dict.get('fps')
            if fps is not None:
                # is a string, convert to int
                fps = int(fps)
            else:
                fps = 24

            qt_item._item_model.set_image_sequence(property_dict['image_sequence'], fps)

        qt_item._item_model.register_press_dbl_click_fnc(press_dbl_click_fnc_)
        qt_item._item_model.set_property_dict(property_dict)

    # by type
    def do_gui_add_all_by_type_(self, scr_type_paths):
        if scr_type_paths:
            self._type_node_path_set.clear()
            for i_scr_type_path in scr_type_paths:
                i_node_path_set = self._page._gui_type_opt.get_assign_path_set_for(i_scr_type_path)
                if i_node_path_set:
                    self._type_node_path_set.update(i_node_path_set)

            self._page._gui_tag_opt.intersection_all_item_assign_path_set(self._type_node_path_set)

            flag, self._tag_node_path_set = self.gui_get_tag_path_set()
            if flag is True:
                if self._tag_node_path_set:
                    node_path_set = set.intersection(self._type_node_path_set, self._tag_node_path_set)
                else:
                    node_path_set = set()
                self.gui_update_entities(node_path_set, self.gui_update_thread_flag())
            else:
                self.gui_update_entities(self._type_node_path_set, self.gui_update_thread_flag())

        # when type is non selected, load by tag
        else:
            self._type_node_path_set.clear()
            # restore tag intersection to default
            self._page._gui_tag_opt.intersection_all_item_assign_path_set(self._type_node_path_set)

            self.gui_update_entities(self._tag_node_path_set, self.gui_update_thread_flag())

    def gui_get_tag_path_set(self):
        scr_tag_paths = self._page._gui_tag_opt.get_check_entity_paths()
        if scr_tag_paths:
            path_set = set()
            for i_scr_tag_path in scr_tag_paths:
                i_node_path_set = self._page._gui_tag_opt.get_assign_path_set_for(i_scr_tag_path)
                if i_node_path_set:
                    path_set.update(i_node_path_set)
            return True, path_set
        return False, set()

    # by tag
    def do_gui_add_all_by_tag_(self, scr_tag_paths):
        if scr_tag_paths:
            # self.restore()

            self._tag_node_path_set.clear()
            for i_scr_tag_path in scr_tag_paths:
                i_node_path_set = self._page._gui_tag_opt.get_assign_path_set_for(i_scr_tag_path)
                if i_node_path_set:
                    self._tag_node_path_set.update(i_node_path_set)

            if self._type_node_path_set:
                node_path_set = set.intersection(self._type_node_path_set, self._tag_node_path_set)
            else:
                node_path_set = self._tag_node_path_set

            self.gui_update_entities(node_path_set, self._gui_thread_flag)
        # when tag is non checked, upload from type
        else:
            self._tag_node_path_set.clear()

            self.gui_update_entities(self._type_node_path_set, self._gui_thread_flag)

    def gui_do_close(self):
        self._qt_list_widget._view_model.do_close()

    def gui_get_checked_scr_entities(self):
        return [x._scr_entity for x in self._qt_list_widget._view_model.get_checked_items()]

    def gui_get_selected_scr_entities(self):
        return [x._scr_entity for x in self._qt_list_widget._view_model.get_selected_items()]

    def gui_get_checked_or_selected_scr_entities(self):
        return self.gui_get_checked_scr_entities() or self.gui_get_selected_scr_entities()

    def do_gui_refresh_all(self):
        self.restore()

        if self._node_path_set:
            self.gui_clear_node_cache_for(self._node_path_set)

            self.gui_add_entities(list(self._node_path_set), self.gui_update_thread_flag())


class AbsPrxPageForManager(
    gui_prx_widgets.PrxBasePage,
    _GuiThreadExtra,
):
    HISTORY_KEY = 'lazy-resource.stage_name'

    FILTER_COMPLETION_MAXIMUM = 50

    def do_gui_node_refresh_by_type_select_or_check(self):
        self._gui_node_opt.do_gui_add_all_by_type_(
            self._gui_type_opt.get_selected_and_checked_entity_paths()
        )

    def do_gui_node_refresh_by_tag_check(self):
        self._gui_node_opt.do_gui_add_all_by_tag_(
            self._gui_tag_opt.get_check_entity_paths()
        )

    def gui_close_fnc(self):
        self._scr_stage.close()
        self._gui_node_opt.gui_do_close()
        return True

    def do_gui_page_initialize(self, key):
        self._scr_stage_name = key
        self._scr_stage = qsm_scr_core.Stage(self._scr_stage_name)

        self.gui_page_setup_fnc()

    def _show_node_register_window(self):
        scr_stage_type = self._scr_stage.type
        w = self._window.gui_generate_sub_panel_for('register')
        w.gui_setup_pages_for([scr_stage_type])
        w.show_window_auto()
        register_page = w.gui_find_page(scr_stage_type)
        if register_page is not None:
            register_page.set_scr_stage_key(self._scr_stage.key)
            register_page.set_post_fnc(self.gui_on_register_finished)

    @gui_qt_core.qt_slot(list, list)
    def gui_on_register_finished(self, scr_type_paths, scr_tag_paths):
        self._gui_type_opt.gui_update_entities_for(scr_type_paths)
        if scr_tag_paths:
            self._gui_tag_opt.gui_update_entities_for(scr_tag_paths)

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
            return bsc_core.BscTexts.sort_by_initial(all_texts)[:self.FILTER_COMPLETION_MAXIMUM]
        return []

    def _gui_update_keyword_filter_path_set_fnc(self, *args, **kwargs):
        keyword = args[0]
        print(keyword)

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

        t = self.gui_generate_thread(
            functools.partial(cache_fnc_, self._gui_thread_flag),
            build_fnc_
        )

        t.do_start()

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForManager, self).__init__(window, session, *args, **kwargs)
        self._init_gui_thread_extra_(window)

        self._scr_stage_name = None
        self._scr_stage = None

        # self._window.register_window_close_method(self.gui_close_fnc)

    def _gui_add_main_tools(self):
        for i in [
            ('add', 'file/add-file', '', self._show_node_register_window)
        ]:
            i_key, i_icon_name, i_tool_tip, i_fnc = i
            i_tool = gui_prx_widgets.PrxIconPressButton()
            self._main_prx_tool_box.add_widget(i_tool)
            i_tool.set_name(i_key)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip(i_tool_tip)
            i_tool.connect_press_clicked_to(i_fnc)

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
        # self._gui_update_keyword_filter_texts()

        self._gui_type_opt.do_gui_refresh_all()
        self._gui_tag_opt.do_gui_refresh_all()
