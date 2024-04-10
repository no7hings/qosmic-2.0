# coding:utf-8
import six

import collections

import lxcontent.core as ctt_core

import lxbasic.core as bsc_core
# gui
from ... import core as gui_core
# proxy
from .. import abstracts as gui_prx_abstracts


class GuiPrxScpForTreeSelection(object):
    def __init__(self, prx_tree_view, dcc_selection_cls, dcc_namespace, dcc_geometry_location=None, dcc_pathsep=None):
        self._prx_tree_view = prx_tree_view
        self._dcc_selection_cls = dcc_selection_cls
        self._dcc_geometry_location = dcc_geometry_location
        self._dcc_pathsep = dcc_pathsep
        #
        self._dcc_namespace = dcc_namespace

    @classmethod
    def select_fnc(cls, prx_tree_view, dcc_selection_cls, dcc_namespace, dcc_geometry_location=None, dcc_pathsep=None):
        if dcc_selection_cls is not None:
            obj_paths = []
            gui_items = prx_tree_view._get_selected_items_()
            for i_gui_item in gui_items:
                i_prx_item = i_gui_item.gui_proxy
                i_dcc_obj = i_prx_item.get_gui_dcc_obj(namespace=dcc_namespace)
                if i_dcc_obj is not None:
                    if dcc_geometry_location is not None:
                        i_path = dcc_geometry_location+i_dcc_obj.path
                    else:
                        i_path = i_dcc_obj.path
                    #
                    if dcc_pathsep is not None:
                        i_path = bsc_core.PthNodeOpt(i_path).translate_to(
                            dcc_pathsep
                        ).get_value()
                    #
                    obj_paths.append(i_path)
            #
            if obj_paths:
                dcc_selection_cls(obj_paths).select_all()
            else:
                dcc_selection_cls.set_clear()

    def set_select(self):
        self.select_fnc(
            prx_tree_view=self._prx_tree_view,
            dcc_selection_cls=self._dcc_selection_cls,
            dcc_namespace=self._dcc_namespace,
            dcc_geometry_location=self._dcc_geometry_location,
            dcc_pathsep=self._dcc_pathsep
        )


class GuiPrxScpForTreeGain(object):
    def __init__(self, prx_tree_view, dcc_namespace):
        self._prx_tree_view = prx_tree_view
        self._dcc_namespace = dcc_namespace

    def get_checked_args(self):
        lis = []
        for i_prx_item in self._prx_tree_view.get_all_items():
            if i_prx_item.get_is_checked() is True:
                obj = i_prx_item.get_gui_dcc_obj(namespace=self._dcc_namespace)
                if obj is not None:
                    lis.append((i_prx_item, obj))
        return lis


class GuiPrxScpForTreeTagFilter(object):
    COUNT_COLUMN = 1

    def __init__(self, prx_tree_view_src, prx_tree_view_tgt, prx_tree_item_cls):
        self._prx_tree_view_src = prx_tree_view_src
        self._prx_tree_view_tgt = prx_tree_view_tgt
        #
        self._prx_tree_item_cls = prx_tree_item_cls
        #
        self._filter_content = ctt_core.Content(
            value=collections.OrderedDict()
        )
        #
        self._dcc_obj_dict = {}
        self._dcc_selection_cls = None
        self._dcc_namespace = None

        self._namespace_src = 'filter'

        self._item_dict = self._prx_tree_view_src._item_dict
        #
        self._prx_tree_view_src.connect_item_check_changed_to(
            self.set_filter
        )

    def set_dcc_selection_args(self, dcc_selection_cls, dcc_namespace):
        self._dcc_selection_cls = dcc_selection_cls
        self._dcc_namespace = dcc_namespace

    def set_select(self):
        GuiPrxScpForTreeSelection.select_fnc(
            prx_tree_view=self._prx_tree_view_src,
            dcc_selection_cls=self._dcc_selection_cls,
            dcc_namespace=self._dcc_namespace
        )

    def restore_all(self):
        self._prx_tree_view_src.restore_all()
        #
        self._filter_content = ctt_core.Content(
            value=collections.OrderedDict()
        )
        self._dcc_obj_dict = {}

    def set_tgt_item_tag_update(self, key, prx_item_tgt, dcc_obj=None):
        self.register(
            prx_item_tgt,
            [key],
            dcc_obj=dcc_obj
        )

    def _set_item_src_show_deferred_(self, prx_item):
        path_dag_opt = prx_item.get_gui_dcc_obj(namespace=self._namespace_src)
        name = bsc_core.SPathMtd.set_unquote_to(path_dag_opt.name)
        path = bsc_core.SPathMtd.set_unquote_to(path_dag_opt.path)
        prx_item.set_name(name)
        prx_item.set_icon_by_name(path, 0)
        prx_item.set_tool_tip(path)

    def _add_prx_item_src_(self, path):
        path_dag_opt = bsc_core.PthNodeOpt(path)
        key = path_dag_opt.path
        if key in self._item_dict:
            return False, self._item_dict[key]
        #
        _kwargs = dict(
            name='...',
            item_class=self._prx_tree_item_cls,
            filter_key=key
        )
        #
        parent_path = bsc_core.PthNodeOpt(path).get_parent_path()
        if parent_path in self._item_dict:
            prx_item_parent = self._item_dict[parent_path]
            prx_item = prx_item_parent.add_child(
                **_kwargs
            )
        else:
            prx_item = self._prx_tree_view_src.create_item(
                **_kwargs
            )
        #
        prx_item.set_checked(False)
        prx_item.set_emit_send_enable(True)
        prx_item.set_gui_dcc_obj(path_dag_opt, self._namespace_src)
        #
        prx_item.set_show_build_fnc(
            self._set_item_src_show_deferred_(
                prx_item
            )
        )
        return True, prx_item

    def set_src_items_refresh(self, expand_depth=None):
        self._prx_tree_view_src.set_clear()
        #
        leaf_paths = self._filter_content.get_all_leaf_key_as_dag_paths()
        all_paths = ['/'] + self._filter_content.get_all_key_as_dag_paths()
        all_paths.sort()
        all_paths = bsc_core.RawTextsOpt(all_paths).sort_by_number()
        for path in all_paths:
            i_is_create, i_prx_item_src = self._add_prx_item_src_(path)
            if path in leaf_paths:
                tag_filter_key = path
                i_prx_item_src.set_tag_filter_src_key_add(tag_filter_key)
            #
            if path in self._dcc_obj_dict:
                dcc_obj = self._dcc_obj_dict[path]
                if self._dcc_namespace is not None:
                    i_prx_item_src.set_gui_dcc_obj(dcc_obj, namespace=self._dcc_namespace)
        #
        if isinstance(expand_depth, int):
            self._prx_tree_view_src.expand_items_by_depth(expand_depth)
        else:
            self._prx_tree_view_src.set_all_items_expand()

    def set_filter_statistic(self):
        target_filter_tag_item_prx_dict = self._prx_tree_view_tgt.get_tag_filter_tgt_statistic_raw()
        for i_prx_item_src in self._prx_tree_view_src._item_dict.values():
            tag_filter_src_keys = i_prx_item_src.get_tag_filter_src_keys()
            if tag_filter_src_keys:
                for tag_filter_src_key in tag_filter_src_keys:
                    if tag_filter_src_key in target_filter_tag_item_prx_dict:
                        tgt_item_prxes = target_filter_tag_item_prx_dict[tag_filter_src_key]
                        if tgt_item_prxes:
                            states = self._prx_tree_view_tgt.get_item_states(tgt_item_prxes)
                            if i_prx_item_src.get_check_enable() is True:
                                if gui_core.GuiState.ERROR in states:
                                    i_prx_item_src.set_error_state()
                                elif gui_core.GuiState.WARNING in states:
                                    i_prx_item_src.set_warning_state()
                                # else:
                                #     i_prx_item_src.set_adopt_state()
                                #
                                i_prx_item_src.set_name(str(len(tgt_item_prxes)), self.COUNT_COLUMN)
                                #
                                brushes = self._prx_tree_view_tgt.get_item_state_colors(tgt_item_prxes)
                                i_prx_item_src.set_foregrounds_raw(brushes)
                                #
                                i_prx_item_src.set_states_raw(states)
                            else:
                                i_prx_item_src.set_name('N/a', self.COUNT_COLUMN)
                                #
                                i_prx_item_src.set_foregrounds_raw([])
                                #
                                i_prx_item_src.set_states_raw([])
                            #
                            i_prx_item_src.set_hidden(boolean=False, ancestors=True)
                        else:
                            i_prx_item_src.set_hidden(boolean=True, ancestors=True)
                    else:
                        i_prx_item_src.set_hidden(boolean=True, ancestors=True)

    def set_filter(self):
        tag_filter_all_keys_src = []
        for i_prx_item_src in self._prx_tree_view_src._item_dict.values():
            tag_filter_src_keys = i_prx_item_src.get_tag_filter_src_keys()
            for tag_filter_src_key in tag_filter_src_keys:
                if i_prx_item_src.get_is_checked() is True:
                    if tag_filter_src_key not in tag_filter_all_keys_src:
                        tag_filter_all_keys_src.append(tag_filter_src_key)
        #
        self._prx_tree_view_tgt.set_tag_filter_all_keys_src(tag_filter_all_keys_src)

    def get_filter_dict(self):
        dic = collections.OrderedDict()
        for i_prx_item_src in self._prx_tree_view_src._item_dict.values():
            i_key = i_prx_item_src.get_path()
            i_value = i_prx_item_src.get_is_checked()
            dic[i_key] = i_value
        return dic

    def set_filter_by_dict(self, dic):
        prx_items = self._prx_tree_view_src.get_all_leaf_items()
        for i_prx_item in prx_items:
            i_path = i_prx_item.get_path()
            if i_path in dic:
                i_prx_item.set_checked(dic[i_path])
            else:
                i_prx_item.set_checked(False)

        self.set_filter()

    def register(self, prx_item_tgt, keys, dcc_obj=None, expand_depth=1):
        for i_key in keys:
            i_path = ctt_core.ContentUtil.key_path_to_dag_path(i_key)
            #
            prx_item_tgt.set_tag_filter_tgt_mode(gui_core.GuiTagFilterMode.MatchAll)
            prx_item_tgt.set_tag_filter_tgt_key_add(
                i_path, ancestors=True
            )
            prx_item_tgt.set_tag_filter_tgt_statistic_enable(True)
            self._filter_content.add_element(
                i_key,
                prx_item_tgt
            )
            count = len(self._filter_content.get(i_key))
            #
            prx_item_src = self._get_item_src_(
                i_path, dcc_obj, expand_depth
            )

            prx_item_src.set_name(str(count), 1)

    def _get_item_src_(self, path, dcc_obj=None, expand_depth=1):
        if path in self._item_dict:
            return self._item_dict[path]
        #
        path_dag_opt = bsc_core.PthNodeOpt(path)
        ancestor_paths = path_dag_opt.get_ancestor_paths()
        if ancestor_paths:
            ancestor_paths.reverse()
            #
            for seq, i_ancestor_path in enumerate(ancestor_paths):
                if i_ancestor_path not in self._item_dict:
                    i_is_create, i_ancestor_prx_item_src = self._add_prx_item_src_(i_ancestor_path)
                    if i_is_create is True:
                        if seq+1 <= expand_depth:
                            i_ancestor_prx_item_src.set_expanded(True)
        #
        is_create, prx_item_src = self._add_prx_item_src_(path)
        prx_item_src.set_tag_filter_src_key_add(path)
        if is_create is True:
            if self._dcc_namespace is not None:
                if dcc_obj is not None:
                    prx_item_src.set_gui_dcc_obj(
                        dcc_obj,
                        namespace=self._dcc_namespace
                    )
        return prx_item_src


class GuiPrxScpForTreeAdd(gui_prx_abstracts.AbsGuiPrxCacheDef):
    def __init__(self, prx_tree_view, prx_tree_item_cls, dcc_namespace):
        self._prx_tree_view = prx_tree_view
        self._prx_tree_item_cls = prx_tree_item_cls
        #
        self._dcc_namespace = dcc_namespace
        self._item_dict = self._prx_tree_view._item_dict

        self._init_cache_def_(self._prx_tree_view)

    def restore_all(self):
        self._generate_cache(self._item_dict)
        self._prx_tree_view.set_clear()

    def _set_dag_dcc_obj_gui_add_(self, obj):
        obj_path = obj.path
        if obj_path in self._item_dict:
            return self._item_dict[obj_path]
        else:
            kwargs = dict(
                name=(obj.name, obj.type),
                item_class=self._prx_tree_item_cls,
                icon=obj.icon,
                tool_tip=obj.path
            )
            parent = obj.get_parent()
            if parent is not None:
                prx_item_parent = self._item_dict[parent.path]
                prx_item = prx_item_parent.add_child(
                    **kwargs
                )
            else:
                prx_item = self._prx_tree_view.create_item(
                    **kwargs
                )
            #
            prx_item.set_gui_dcc_obj(obj, namespace=self._dcc_namespace)
            prx_item.set_expanded(True)
            prx_item.set_checked(False)
            prx_item.set_icon_by_name(obj.type_name, 1)
            self._item_dict[obj_path] = prx_item
            return prx_item

    def gui_add(self, obj, prx_item_parent, name_use_path_prettify):
        key = obj.path
        tool_tips = [
            'type: {}'.format(obj.type_name),
            'path: {}'.format(obj.path)
        ]
        tool_tip = '\n'.join(tool_tips)
        if name_use_path_prettify is True:
            kwargs = dict(
                name=obj.get_path_prettify_(),
                item_class=self._prx_tree_item_cls,
                icon=obj.icon,
                tool_tip=tool_tip,
                menu=obj.get_gui_menu_raw()
            )
        else:
            kwargs = dict(
                name=obj.name,
                item_class=self._prx_tree_item_cls,
                icon=obj.icon,
                tool_tip=tool_tip,
                menu=obj.get_gui_menu_raw()
            )
        if prx_item_parent is not None:
            prx_item = prx_item_parent.add_child(
                **kwargs
            )
        else:
            prx_item = self._prx_tree_view.create_item(
                **kwargs
            )
        prx_item.set_gui_dcc_obj(obj, namespace=self._dcc_namespace)
        self._item_dict[key] = prx_item

        if key in self._cache_expand:
            prx_item.set_expanded(self._cache_expand[key])
        else:
            prx_item.set_expanded(False)
        if key in self._cache_check:
            prx_item.set_checked(self._cache_check[key])
        else:
            prx_item.set_checked(False)
        return prx_item

    def _set_prx_item_add_2_(self, obj, prx_item_parent):
        obj_key = obj.path
        if obj_key in self._item_dict:
            return self._item_dict[obj_key]
        else:
            return self.gui_add(
                obj,
                prx_item_parent,
                name_use_path_prettify=False
            )

    def _set_prx_item_add_0_(self, obj, parent=None):
        obj_key = obj.path
        if obj_key in self._item_dict:
            return self._item_dict[obj_key]
        else:
            if parent is not None:
                parent_key = parent.path
                prx_item_parent = self._item_dict[parent_key]
            else:
                prx_item_parent = None
            return self.gui_add(obj, prx_item_parent, name_use_path_prettify=False)

    def _set_prx_item_add_1_(self, obj, parent=None):
        obj_key = obj.path
        if obj_key in self._item_dict:
            return self._item_dict[obj_key]
        else:
            if parent is not None:
                parent_key = parent.path
                prx_item_parent = self._item_dict[parent_key]
            else:
                prx_item_parent = None
            return self.gui_add(obj, prx_item_parent, name_use_path_prettify=True)

    def gui_add_as(self, obj, mode='tree'):
        if mode == 'tree':
            return self.gui_add_as_tree(obj)
        elif mode == 'list':
            return self.gui_add_as_list(obj)

    def gui_add_as_list(self, obj):
        root = obj.get_root()
        self._set_prx_item_add_0_(root)
        parent = obj.get_parent()
        self._set_prx_item_add_1_(parent, root)
        #
        return self._set_prx_item_add_0_(obj, parent)

    def gui_add_as_tree(self, obj):
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            #
            for ancestor in ancestors:
                ancestor_path = ancestor.path
                if ancestor_path not in self._item_dict:
                    self._set_dag_dcc_obj_gui_add_(ancestor)
        #
        return self._set_dag_dcc_obj_gui_add_(obj)

    def get_checked_dcc_objs(self):
        list_ = []
        for k, v in self._prx_tree_view._item_dict.items():
            i_texture = v.get_gui_dcc_obj(namespace=self._dcc_namespace)
            if i_texture is not None:
                if v.get_is_checked() is True:
                    list_.append(i_texture)
        return list_


# noinspection PyUnusedLocal
class GuiPrxScpForStorageTreeAdd(gui_prx_abstracts.AbsGuiPrxCacheDef):
    def __init__(self, prx_tree_view, prx_tree_item_cls):
        self._prx_tree_view = prx_tree_view
        self._prx_tree_item_cls = prx_tree_item_cls
        self._item_dict = self._prx_tree_view._item_dict

        self._init_cache_def_(self._prx_tree_view)

        self._dcc_namespace = 'storage'

    def restore_all(self):
        self._generate_cache(self._item_dict)
        self._prx_tree_view.set_clear()

    def _set_dag_dcc_obj_gui_add_(self, obj):
        obj_path = obj.path
        obj_key = obj.normcase_path
        if obj_path in self._item_dict:
            return False, self._item_dict[obj_path]
        else:
            kwargs = self._generate_add_kwargs(obj, False)
            parent = obj.get_parent()
            if parent is not None:
                prx_item_parent = self._item_dict[parent.path]
                prx_item = prx_item_parent.add_child(
                    **kwargs
                )
            else:
                prx_item = self._prx_tree_view.create_item(
                    **kwargs
                )
            #
            prx_item.set_checked(False)
            prx_item.set_icon_by_color(bsc_core.RawTextOpt(obj.type).to_rgb(), 1)
            self._item_dict[obj_key] = prx_item
            return True, prx_item

    def _generate_add_kwargs(self, obj, name_use_path_prettify):
        obj_name = obj.name
        type_name = 'directory'
        if obj.get_is_file():
            type_name = 'file({})'.format(obj.ext)
        #
        if name_use_path_prettify is True:
            kwargs = dict(
                name='...',
                item_class=self._prx_tree_item_cls,
                # icon=obj.icon,
                icon_name_text=type_name,
            )
        else:
            kwargs = dict(
                name='...',
                item_class=self._prx_tree_item_cls,
                # icon=obj.icon,
                icon_name_text=type_name,
            )
        return kwargs

    def gui_add(self, obj, parent=None, use_show_thread=False, name_use_path_prettify=False):
        key = obj.normcase_path
        if key in self._item_dict:
            return False, self._item_dict[key]
        else:
            if parent is not None:
                parent_key = parent.normcase_path
                prx_item_parent = self._item_dict[parent_key]
            else:
                prx_item_parent = None
            #
            create_kwargs = dict(
                name='loading ...',
                item_class=self._prx_tree_item_cls,
                filter_key=obj.path
            )
            #
            if prx_item_parent is not None:
                prx_item = prx_item_parent.add_child(
                    **create_kwargs
                )
            else:
                prx_item = self._prx_tree_view.create_item(
                    **create_kwargs
                )

            self._item_dict[key] = prx_item
            if key in self._cache_expand:
                prx_item.set_expanded(self._cache_expand[key])
            else:
                prx_item.set_expanded(False)
            if key in self._cache_check:
                prx_item.set_checked(self._cache_check[key])
            else:
                prx_item.set_checked(False)
            #
            prx_item.update_keyword_filter_keys_tgt([obj.path, obj.type])
            obj.set_obj_gui(prx_item)
            prx_item.set_gui_dcc_obj(obj, namespace=self._dcc_namespace)
            if obj.get_is_file() is True:
                prx_item.set_gui_dcc_obj(obj, namespace='storage-file')
            else:
                prx_item.set_gui_dcc_obj(obj, namespace='storage-directory')
            #
            if use_show_thread is True:
                prx_item.set_show_build_fnc(
                    lambda *args, **kwargs: self._set_prx_item_show_deferred_(prx_item, name_use_path_prettify)
                )
                return True, prx_item
            else:
                self._set_prx_item_show_deferred_(prx_item, name_use_path_prettify)
                return True, prx_item

    def gui_add_as(self, obj, mode='tree', use_show_thread=False):
        if mode == 'tree':
            return self.gui_add_as_tree(obj)
        elif mode == 'list':
            return self.gui_add_as_list(obj, use_show_thread=use_show_thread)

    def gui_add_as_list(self, obj, use_show_thread=False):
        obj_key = obj.normcase_path
        if obj_key in self._item_dict:
            return False, self._item_dict[obj_key]

        if obj.PATHSEP in obj.path:
            root = obj.get_root()
            if root is not None:
                # add root
                self.gui_add(
                    obj=root,
                    use_show_thread=use_show_thread
                )
                # add directory
                directory = obj.get_parent()
                self.gui_add(
                    obj=directory,
                    parent=root,
                    use_show_thread=use_show_thread,
                    name_use_path_prettify=True
                )
                # add file
                return self.gui_add(
                    obj=obj,
                    parent=directory,
                    use_show_thread=use_show_thread
                )
        #
        return False, None

    def gui_add_as_tree(self, obj):
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            for i_ancestor in ancestors:
                i_ancestor_path = i_ancestor.path
                if i_ancestor_path not in self._item_dict:
                    self._set_dag_dcc_obj_gui_add_(i_ancestor)
        #
        return self._set_dag_dcc_obj_gui_add_(obj)

    def _set_prx_item_show_deferred_(self, prx_item, name_use_path_prettify):
        obj = prx_item.get_gui_dcc_obj(namespace=self._dcc_namespace)
        name_orig = obj.name
        obj_name = obj.name
        obj_path = obj.path
        obj_type = obj.type
        #
        if name_use_path_prettify is True:
            name = obj.get_path_prettify_()
        else:
            name = obj_name
        #
        descriptions = [
            u'path="{}"'.format(obj_path)
        ]
        if obj.get_is_file():
            file_tiles = obj.get_exists_units()
            if file_tiles:
                tool_tip_ = []
                if len(file_tiles) > 10:
                    _ = file_tiles[:8]+['...']+file_tiles[-1:]
                else:
                    _ = file_tiles
                #
                for i_file_tile in _:
                    if isinstance(i_file_tile, six.string_types):
                        tool_tip_.append(i_file_tile)
                    else:
                        readable = i_file_tile.get_is_readable()
                        writable = i_file_tile.get_is_writable()
                        tool_tip_.append(
                            u'path="{}"; readable={}; writable={}'.format(
                                i_file_tile.path, readable, writable
                            )
                        )
                #
                name = '{} ({})'.format(bsc_core.auto_encode(name), len(file_tiles))
                descriptions = [tool_tip_]
        #
        menu_raw = []
        menu_raw.extend(
            obj.get_gui_menu_raw() or []
        )
        menu_raw.extend(
            obj.get_gui_extend_menu_raw() or []
        )
        #
        prx_item.set_name_orig(name_orig)
        prx_item.set_name(name)
        prx_item.set_icon_by_file(obj.icon)
        #
        menu_raw.extend(
            [
                ('expanded',),
                ('expand branch', None, prx_item.set_expand_branch),
                ('collapse branch', None, prx_item.set_collapse_branch),
                ('permission',),
                ('unlock', None, None),
            ]
        )
        prx_item.set_gui_menu_raw(menu_raw)
        prx_item.set_menu_content(obj.get_gui_menu_content())
        #
        if obj.get_is_root() is False:
            if obj.get_is_exists() is False:
                prx_item.set_status(prx_item.ValidationStatus.Lost)
            elif obj.get_is_readable() is False:
                prx_item.set_status(prx_item.ValidationStatus.Unreadable)
            elif obj.get_is_writable() is False:
                prx_item.set_status(prx_item.ValidationStatus.Unwritable)
            else:
                prx_item.set_status(prx_item.ValidationStatus.Normal)
                if obj.get_is_directory() is True:
                    prx_item.set_expanded(True)
        else:
            prx_item.set_expanded(True)

        prx_item.set_tool_tips(descriptions)

    def get_files(self):
        list_ = []
        for k, v in self._prx_tree_view._item_dict.items():
            i_texture = v.get_gui_dcc_obj(namespace='storage-file')
            if i_texture is not None:
                if v.get_is_visible() is True:
                    list_.append(i_texture)
        return list_

    def get_checked_files(self):
        list_ = []
        for k, v in self._prx_tree_view._item_dict.items():
            i_texture = v.get_gui_dcc_obj(namespace='storage-file')
            if i_texture is not None:
                if v.get_is_visible() is True and v.get_is_checked() is True:
                    list_.append(i_texture)
        return list_

    @staticmethod
    def get_file(item):
        return item.gui_proxy.get_gui_dcc_obj(namespace='storage-file')


# noinspection PyUnusedLocal
class GuiPrxScpForTextureTreeAdd(GuiPrxScpForStorageTreeAdd):
    def __init__(self, *args, **kwargs):
        super(GuiPrxScpForTextureTreeAdd, self).__init__(*args, **kwargs)

        self._output_directory_path = None

    def set_output_directory(self, directory_path):
        self._output_directory_path = directory_path

    def _set_prx_item_show_deferred_(self, prx_item, name_use_path_prettify):
        obj = prx_item.get_gui_dcc_obj(namespace=self._dcc_namespace)
        obj_name = obj.name
        obj_path = obj.path
        obj_type = obj.type
        #
        if name_use_path_prettify is True:
            name = obj.get_path_prettify_()
        else:
            name = obj_name
        #
        descriptions = [
            u'path="{}"'.format(obj_path)
        ]
        if obj.get_is_file():
            file_tiles = obj.get_exists_units()
            if file_tiles:
                tool_tip_ = []
                if len(file_tiles) > 10:
                    _ = file_tiles[:8]+['...']+file_tiles[-1:]
                else:
                    _ = file_tiles
                #
                for i_file_tile in _:
                    if isinstance(i_file_tile, six.string_types):
                        tool_tip_.append(i_file_tile)
                    else:
                        st_mode = i_file_tile.get_permission()
                        tool_tip_.append(
                            u'path="{}"; st-mode="{}"'.format(
                                i_file_tile.path, st_mode
                            )
                        )
                #
                name = '{} ({})'.format(name, len(file_tiles))
                descriptions = [tool_tip_]
        #
        menu_raw = []
        menu_raw.extend(
            obj.get_gui_menu_raw() or []
        )
        menu_raw.extend(
            obj.get_gui_extend_menu_raw() or []
        )
        #
        prx_item.set_name(name)
        prx_item.set_icon_by_file(obj.icon)
        prx_item.set_tool_tips(descriptions)
        #
        menu_raw.extend(
            [
                ('expanded',),
                ('Expand branch', None, prx_item.set_expand_branch),
                ('Collapse branch', None, prx_item.set_collapse_branch),
            ]
        )
        prx_item.set_gui_menu_raw(menu_raw)
        prx_item.set_menu_content(obj.get_gui_menu_content())
        #
        if obj.get_is_exists() is False:
            prx_item.set_status(prx_item.ValidationStatus.Disable)
        else:
            prx_item.set_status(prx_item.ValidationStatus.Normal)
            if obj.get_is_directory() is True:
                prx_item.set_expanded(True)
            else:
                i_tx_exists = obj._get_is_exists_as_tgt_ext_(
                    obj.path, obj.TX_EXT, self._output_directory_path
                )
                if i_tx_exists is True:
                    prx_item.set_status(prx_item.ValidationStatus.Normal)
                else:
                    prx_item.set_status(prx_item.ValidationStatus.Warning)
        #
        # self._prx_tree_view.set_loading_update()


# noinspection PyUnusedLocal
class GuiPrxScpForTreeAdd1(object):
    def __init__(self, prx_tree_view, prx_tree_item_cls, dcc_namespace):
        self._prx_tree_view = prx_tree_view
        self._prx_tree_item_cls = prx_tree_item_cls
        #
        self._dcc_namespace = dcc_namespace
        self._item_dict = self._prx_tree_view._item_dict

    def restore_all(self):
        self._prx_tree_view.set_clear()

    def _set_dag_dcc_obj_gui_add_(self, obj):
        obj_path = obj.path
        if obj_path in self._item_dict:
            return self._item_dict[obj_path]
        else:
            kwargs = dict(
                name=(obj.name, obj.type.name),
                item_class=self._prx_tree_item_cls,
                icon=obj.icon,
                tool_tip=obj.path,
                menu=obj.get_gui_menu_raw()
            )
            parent = obj.get_parent()
            if parent is not None:
                prx_item_parent = self._item_dict[parent.path]
                prx_item = prx_item_parent.add_child(
                    **kwargs
                )
            else:
                prx_item = self._prx_tree_view.create_item(
                    **kwargs
                )
            #
            obj.set_obj_gui(prx_item)
            prx_item.set_gui_dcc_obj(obj, namespace=self._dcc_namespace)
            prx_item.set_expanded(True)
            prx_item.set_checked(False)
            prx_item.set_icon_by_color(bsc_core.RawTextOpt(obj.type.name).to_rgb(), 1)
            self._item_dict[obj_path] = prx_item
            return prx_item

    def _set_prx_item_show_deferred_(self, prx_item, name_use_path_prettify):
        obj = prx_item.get_gui_dcc_obj(namespace=self._dcc_namespace)

        icon = obj.icon
        obj_type_name = obj.type_name
        obj_name = obj.name
        obj_path = obj.path

        menu_raw = obj.get_gui_menu_raw()

        prx_item.set_icon_by_file(icon)
        prx_item.set_icon_by_name(obj_type_name, 1)
        prx_item.set_name(obj_name)
        prx_item.set_tool_tip(obj_path)

        prx_item.set_gui_menu_raw(menu_raw)

    def gui_add(self, obj, prx_item_parent, name_use_path_prettify):
        if name_use_path_prettify is True:
            kwargs = dict(
                name=(obj.get_path_prettify_(), obj.type_path),
                item_class=self._prx_tree_item_cls,
                icon=obj.icon,
                tool_tip=obj.path,
                menu=obj.get_gui_menu_raw()
            )
        else:
            kwargs = dict(
                name=(obj.name, obj.type_path),
                item_class=self._prx_tree_item_cls,
                icon=obj.icon,
                tool_tip=obj.path,
                menu=obj.get_gui_menu_raw()
            )
        if prx_item_parent is not None:
            prx_item = prx_item_parent.add_child(
                **kwargs
            )
        else:
            prx_item = self._prx_tree_view.create_item(
                **kwargs
            )
        #
        obj.set_obj_gui(prx_item)
        prx_item.set_gui_dcc_obj(obj, namespace=self._dcc_namespace)
        prx_item.set_expanded(True)
        prx_item.set_checked(True)
        #
        self._item_dict[obj.path] = prx_item
        # prx_item.set_show_build_fnc(
        #     functools.partial(
        #         self._set_prx_item_show_deferred_, prx_item, name_use_path_prettify
        #     )
        # )
        return prx_item

    def _set_prx_item_add_0_(self, obj, parent=None):
        obj_key = obj.path
        if obj_key in self._item_dict:
            return self._item_dict[obj_key]
        else:
            if parent is not None:
                parent_key = parent.path
                prx_item_parent = self._item_dict[parent_key]
            else:
                prx_item_parent = None
            return self.gui_add(
                obj,
                prx_item_parent,
                name_use_path_prettify=False
            )

    def _set_prx_item_add_1_(self, obj, parent=None):
        obj_key = obj.path
        if obj_key in self._item_dict:
            return self._item_dict[obj_key]
        else:
            if parent is not None:
                parent_key = parent.path
                prx_item_parent = self._item_dict[parent_key]
            else:
                prx_item_parent = None
            return self.gui_add(
                obj,
                prx_item_parent,
                name_use_path_prettify=True
            )

    def gui_add_as(self, obj, mode='tree'):
        if mode == 'tree':
            return self.gui_add_as_tree(obj)
        elif mode == 'list':
            return self.gui_add_as_list(obj)

    def gui_add_as_list(self, obj):
        root = obj.get_root()
        self._set_prx_item_add_0_(root)
        #
        parent = obj.get_parent()
        self._set_prx_item_add_1_(parent, root)
        #
        return self._set_prx_item_add_0_(obj, parent)

    def gui_add_as_tree(self, obj):
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            #
            for i_ancestor in ancestors:
                i_ancestor_path = i_ancestor.path
                if i_ancestor_path not in self._item_dict:
                    self._set_dag_dcc_obj_gui_add_(i_ancestor)
        #
        return self._set_dag_dcc_obj_gui_add_(obj)


class GuiPrxScpForUsdTreeAdd(GuiPrxScpForTreeAdd1):
    def __init__(
        self, prx_tree_view, prx_tree_item_cls, dcc_namespace, dcc_pathsep, dcc_node_class,
        dcc_geometry_location=None
    ):
        super(GuiPrxScpForUsdTreeAdd, self).__init__(prx_tree_view, prx_tree_item_cls, dcc_namespace='usd')
        self._dcc_namespace = dcc_namespace
        self._dcc_pathsep = dcc_pathsep
        self._dcc_node_class = dcc_node_class
        self._dcc_geometry_location = dcc_geometry_location

    def gui_add_as_list(self, obj):
        root = obj.get_root()
        self._set_prx_item_add_0_(root)
        transform = obj.get_parent()
        group = transform.get_parent()
        self._set_prx_item_add_1_(group, root)
        # self._set_prx_item_add_0_(transform, group)
        #
        return self._set_prx_item_add_0_(obj, group)

    def set_item_prx_update(self, src_mesh):
        src_transform = src_mesh.get_parent()
        src_group = src_transform.get_parent()
        self._set_tgt_update_(src_group)
        self._set_tgt_update_(src_transform)
        self._set_tgt_update_(src_mesh)

    def _set_tgt_update_(self, src_obj):
        path_src = src_obj.path
        prx_item = src_obj.get_obj_gui()
        if prx_item is not None:
            path_opt_src = bsc_core.PthNodeOpt(path_src)
            path_opt_tgt = path_opt_src.translate_to(self._dcc_pathsep)
            dcc_node = self._dcc_node_class(path_opt_tgt.get_value())
            if dcc_node.get_is_exists() is True:
                prx_item.set_icon_by_file(dcc_node.icon)
                prx_item.set_gui_dcc_obj(dcc_node, namespace=self._dcc_namespace)
            else:
                prx_item.set_temporary_state()
