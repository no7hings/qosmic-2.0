# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# qt
from ....qt import core as _qt_core

from ....qt.widgets import utility as _qt_wgt_utility

from .. import view_for_tree as _wgt_view_for_tree

import _input_base


#   files
# noinspection PyUnusedLocal
class PrxInputForFiles(_input_base.AbsPrxInputExtra):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    PRX_INPUT_CLS = _wgt_view_for_tree.PrxTreeView
    NAMESPACE = 'storage'

    def __init__(self, *args, **kwargs):
        super(PrxInputForFiles, self).__init__(*args, **kwargs)
        self._qt_widget.setFixedHeight(162)
        self._prx_input.create_header_view(
            [('name', 3), ('update', 1)],
            480
        )
        self._prx_input.set_selection_use_single()
        self._prx_input.set_size_policy_height_fixed_mode()
        self._prx_input.set_resize_target(self.widget)
        self._prx_input.set_resize_enable(True)
        self._prx_input.set_resize_minimum(82)
        self._prx_input.get_check_tool_box().set_visible(True)
        #
        self._prx_input.connect_refresh_action_for(self.refresh)
        #
        self._item_dict = self._prx_input._item_dict

        self._root_location = None

        self._view_mode = 'list'

        self._paths = []

    def _add_item_component_as_tree(self, obj, scheme):
        path = obj.path
        type_name = obj.type
        if path in self._item_dict:
            prx_item = self._item_dict[path]
            return False, prx_item, None

        create_kwargs = dict(
            name='...',
            filter_key=path
        )
        parent_path = obj.get_parent_path()
        if parent_path is not None:
            prx_item_parent = self._item_dict[parent_path]
            prx_item = prx_item_parent.add_child(
                **create_kwargs
            )
        else:
            prx_item = self._prx_input.create_item(
                **create_kwargs
            )
        #
        prx_item.set_checked(True)
        prx_item.update_keyword_filter_keys_tgt([path, type_name])
        obj.set_gui(prx_item)
        prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
        self._item_dict[path] = prx_item
        #
        prx_item.set_show_build_fnc(
            lambda *args, **kwargs: self._item_show_fnc(prx_item, scheme)
        )
        return True, prx_item, None

    def _item_show_fnc(self, prx_item, scheme, use_as_tree=True):
        def rpc_lock_folder_fnc_():
            bsc_storage.StgPermissionMtd.change_mode(path, mode='555')
            prx_item.set_status(
                prx_item.ValidationStatus.Locked
            )

        def rpc_unlock_folder_fnc_():
            bsc_storage.StgPermissionMtd.change_mode(path, mode='775')
            prx_item.set_status(
                prx_item.ValidationStatus.Normal
            )

        def rpc_lock_files_fnc_():
            file_paths = bsc_storage.StgDirectoryOpt(path).get_all_file_paths()
            with bsc_log.LogProcessContext.create(maximum=len(file_paths), label='rpc unlock files (555)') as g_p:
                for i_file_path in file_paths:
                    bsc_storage.StgPermissionMtd.change_mode(i_file_path, mode='555')
                    g_p.do_update()

                prx_item.set_status(
                    prx_item.ValidationStatus.Normal
                )

        def rpc_unlock_files_fnc_():
            file_paths = bsc_storage.StgDirectoryOpt(path).get_all_file_paths()
            with bsc_log.LogProcessContext.create(maximum=len(file_paths), label='rpc unlock files (775)') as g_p:
                for i_file_path in file_paths:
                    i_file_opt = bsc_storage.StgFileOpt(i_file_path)
                    bsc_storage.StgPermissionMtd.change_mode(i_file_path, mode='775')
                    g_p.do_update()

                prx_item.set_status(
                    prx_item.ValidationStatus.Normal
                )

        obj = prx_item.get_gui_dcc_obj(namespace=self.NAMESPACE)
        path = obj.get_path()
        if obj.get_is_exists() is True:
            update = bsc_core.BscTimePrettify.to_prettify_by_timestamp(
                obj.get_mtime(),
                language=1
            )
        else:
            update = 'non-exists'
        if use_as_tree is True:
            prx_item.set_names([obj.get_name(), update])
        else:
            prx_item.set_names([obj.get_path_prettify(), update])

        if scheme == 'folder':
            prx_item.set_icon(
                _qt_core.GuiQtDcc.generate_qt_directory_icon()
            )
        else:
            prx_item.set_icon(
                _qt_core.GuiQtDcc.generate_qt_file_icon(path)
            )

        prx_item.set_tool_tip(
            (
                'type: {}\n'
                'path: {}\n'
            ).format(obj.get_type_name(), obj.get_path())
        )
        menu_raw = [
            ('open folder', 'file/folder', obj.show_in_system)
        ]
        # if use_as_tree is True:
        #     menu_raw.extend(
        #         [
        #             ('expanded',),
        #             ('expand branch', 'expand', prx_item.set_expand_branch),
        #             ('collapse branch', 'collapse', prx_item.set_collapse_branch),
        #         ]
        #     )
        if scheme == 'file':
            prx_item.set_drag_enable(True)
            prx_item.set_drag_urls([obj.get_path()])
            # for katana
            prx_item.set_drag_data(
                {
                    'nodegraph/fileref': str(obj.get_path())
                }
            )
        # elif scheme == 'folder':
        #     menu_raw.extend(
        #         [
        #             ('rpc folder permission',),
        #             ('rpc lock folder (555)', 'lock', rpc_lock_folder_fnc_),
        #             ('rpc unlock folder (775)', 'lock', rpc_unlock_folder_fnc_),
        #             ('rpc file permission',),
        #             ('rpc lock files (555)', 'lock', rpc_lock_files_fnc_),
        #             ('rpc unlock files (775)', 'lock', rpc_unlock_files_fnc_),
        #         ]
        #     )
        #
        prx_item.set_gui_menu_data(menu_raw)
        #
        if obj.get_is_exists() is False:
            prx_item.set_status(
                prx_item.ValidationStatus.Lost
            )
        elif obj.get_is_readable() is False:
            prx_item.set_status(
                prx_item.ValidationStatus.Unreadable
            )
        elif obj.get_is_writeable() is False:
            prx_item.set_status(
                prx_item.ValidationStatus.Unwritable
            )

    def _add_item_as_tree(self, obj, scheme):
        if self._root_location is not None:
            i_is_create, i_prx_item, _ = self._add_item_as_list(self._root_obj, scheme='folder')
            if i_is_create is True:
                i_prx_item.set_expanded(True)

            ancestor_paths = obj.get_ancestor_paths()
            ancestor_paths.reverse()
            if self._root_location in ancestor_paths:
                index = ancestor_paths.index(self._root_location)
                for i_path in ancestor_paths[index:]:
                    if i_path not in self._item_dict:
                        i_obj = self._root_obj.create_dag_fnc(i_path)
                        i_is_create, i_prx_item, _ = self._add_item_component_as_tree(i_obj, scheme='folder')
                        if i_is_create is True:
                            i_prx_item.set_expanded(True)
            else:
                return
        else:
            ancestor_paths = obj.get_ancestor_paths()
            if ancestor_paths:
                ancestor_paths.reverse()
                for i_path in ancestor_paths:
                    i_obj = self._root_obj.create_dag_fnc(i_path)
                    if i_path not in self._item_dict:
                        i_is_create, i_prx_item, _ = self._add_item_component_as_tree(i_obj, scheme='folder')
                        if i_is_create is True:
                            i_prx_item.set_expanded(True)
        #
        self._add_item_component_as_tree(obj, scheme)

    def _add_item_as_list(self, obj, scheme):
        path = obj.get_path()
        type_name = obj.get_type_name()
        if path in self._item_dict:
            prx_item = self._item_dict[path]
            return False, prx_item, None

        create_kwargs = dict(
            name='...',
            filter_key=path
        )
        prx_item = self._prx_input.create_item(
            **create_kwargs
        )
        #
        prx_item.set_checked(True)
        prx_item.update_keyword_filter_keys_tgt([path, type_name])
        obj.set_gui(prx_item)
        prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
        prx_item.set_tool_tip(path)
        self._item_dict[path] = prx_item
        #
        prx_item.set_show_build_fnc(
            lambda *args, **kwargs: self._item_show_fnc(prx_item, scheme, use_as_tree=False)
        )
        return True, prx_item, None

    def _set_item_selected(self, obj):
        item = obj.get_gui()
        self._prx_input.set_item_selected(
            item, exclusive=True
        )

    def restore(self):
        self._prx_input.do_clear()

    def refresh(self):
        self.set(self._paths)

    def set_view_mode(self, mode):
        self._view_mode = mode

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (tuple, list)):
            self.restore()
            self._paths = raw
            if self._paths:
                obj_cur = None
                for i_path in self._paths:
                    if bsc_storage.StgPathOpt(i_path).get_is_file():
                        i_obj = bsc_storage.StgFileOpt(i_path)
                        i_scheme = 'file'
                    else:
                        i_obj = bsc_storage.StgDirectoryOpt(i_path)
                        i_scheme = 'folder'
                    #
                    obj_cur = i_obj
                    #
                    if self._view_mode == 'list':
                        self._add_item_as_list(i_obj, i_scheme)
                    elif self._view_mode == 'tree':
                        self._add_item_as_tree(i_obj, i_scheme)
                #
                self._set_item_selected(obj_cur)
        else:
            pass

    def set_root(self, path):
        self._root_location = path
        self._root_obj = bsc_storage.StgDirectoryOpt(self._root_location)

    def set_checked_by_include_paths(self, paths):
        _ = self._prx_input.get_all_items()
        if _:
            for i in _:
                if i.get_gui_dcc_obj(namespace=self.NAMESPACE).path in paths:
                    i.set_checked(True, extra=False)

    def set_unchecked_by_include_paths(self, paths):
        _ = self._prx_input.get_all_items()
        if _:
            for i in _:
                if i.get_gui_dcc_obj(namespace=self.NAMESPACE).path not in paths:
                    i.set_checked(False, extra=False)

    def set_all_items_checked(self, boolean):
        self._prx_input._qt_view._set_all_items_checked_(boolean)

    def get(self):
        _ = self._prx_input.get_all_items()
        if _:
            return [i.get_gui_dcc_obj(namespace=self.NAMESPACE).get_path() for i in _ if i.get_is_selected()]
        return []

    def get_all(self, check_only=False):
        _ = self._prx_input.get_all_items()
        if _:
            if check_only is True:
                return [i.get_gui_dcc_obj(namespace=self.NAMESPACE).get_path() for i in _ if i.get_is_checked() is True]
            return [i.get_gui_dcc_obj(namespace=self.NAMESPACE).get_path() for i in _]
        return []

    def connect_input_changed_to(self, fnc):
        self._prx_input.connect_item_select_changed_to(
            fnc
        )

    def connect_refresh_action_for(self, fnc):
        self._prx_input.connect_refresh_action_for(fnc)
