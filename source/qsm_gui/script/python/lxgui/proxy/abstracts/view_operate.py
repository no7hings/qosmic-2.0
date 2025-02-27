# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# gui
from ... import core as gui_core
# qt
from ...qt import core as gui_qt_core


class AbsGuiPrxCacheDef(object):
    CHECK_BOX_FLAG = False

    def _init_cache_def_(self, prx_tree_view):
        self._prx_tree_view = prx_tree_view

    def _push_cache(self):
        self._prx_tree_view._expand_cache_dict.clear()
        self._prx_tree_view._check_cache_dict.clear()
        for k, v in self._prx_tree_view._item_dict.items():
            self._prx_tree_view._expand_cache_dict[k] = v.get_is_expanded()

            if self.CHECK_BOX_FLAG is True:
                self._prx_tree_view._check_cache_dict[k] = v.get_is_checked()
    
    def _pull_cache(self):
        for k, v in self._prx_tree_view._item_dict.items():
            if k in self._prx_tree_view._expand_cache_dict:
                v.set_expanded(self._prx_tree_view._expand_cache_dict[k])

            if self.CHECK_BOX_FLAG is True:
                if k in self._prx_tree_view._check_cache_dict:
                    v.set_checked(self._prx_tree_view._check_cache_dict[k])


class AbsGuiPrxTreeViewOpt(object):
    ROOT_NAME = 'All'

    def _init_tree_view_opt_(self, prx_tree_view, namespace):
        self._prx_tree_view = prx_tree_view
        self._item_dict = self._prx_tree_view._item_dict
        self._keys = set()

        self._gui_thread_flag = 0

        self._namespace = namespace

    def register_occurrence(self, key, path):
        prx_item = self.gui_get_one(path)
        self._prx_tree_view._qt_view._register_keyword_filter_occurrence_(
            key, prx_item.get_item()
        )

    def register_completion(self, key):
        self._keys.add(key)

    def get_completion_keys(self):
        return self._keys

    def restore(self):
        self._prx_tree_view.do_clear()
        self._keys.clear()

    def gui_check_exists(self, path):
        return self._item_dict.get(path) is not None

    def gui_get_one(self, path):
        if path:
            return self._item_dict[path]
        return self._prx_tree_view

    def gui_register(self, path, prx_item):
        self._item_dict[path] = prx_item
        prx_item.set_gui_attribute('path', path)

    def get_current_obj(self):
        _ = self._prx_tree_view.get_selected_items()
        if _:
            return _[-1].get_gui_dcc_obj(self._namespace)


class AbsGuiPrxTreeViewAsDirectoryOpt(AbsGuiPrxTreeViewOpt):
    def _init_tree_view_as_directory_opt_(self, prx_tree_view, namespace):
        self._init_tree_view_opt_(prx_tree_view, namespace)

        self._gui_thread_flag = 0
        self._root = None

        self._cache_expand_all = dict()
        self._cache_expand_current = dict()

    def restore(self):
        self.__push_expand_cache()

        self._prx_tree_view.do_clear()
        self._keys.clear()

    def __push_expand_cache(self):
        if self._root is not None:
            if self._root not in self._cache_expand_all:
                expand_dict = dict()
                self._cache_expand_all[self._root] = expand_dict
            else:
                expand_dict = self._cache_expand_all[self._root]

            for k, v in self._item_dict.items():
                expand_dict[k] = v.get_is_expanded()

    def __pull_expand_cache(self):
        # load expand cache
        if self._root in self._cache_expand_all:
            self._cache_expand_current = self._cache_expand_all[self._root]

    def gui_add_root(self, directory_opt):
        directory_path = directory_opt.get_path()
        self._root = directory_opt.get_parent_path()

        self.__pull_expand_cache()

        path = directory_path[len(self._root):]
        if self.gui_check_exists(path) is False:
            path_opt = bsc_core.BscNodePathOpt(path)
            prx_item = self._prx_tree_view.create_item(
                path_opt.get_name(),
                icon=gui_core.GuiIcon.get('database/all'),
            )
            self.gui_register(path, prx_item)

            prx_item.set_gui_dcc_obj(
                directory_opt, self._namespace
            )

            prx_item.set_expanded(True)
            prx_item.set_checked(False)
            prx_item.set_gui_menu_data(
                [
                    ('system',),
                    ('open folder', 'file/open-folder', directory_opt.show_in_system)
                ]
            )
            return True, prx_item
        return False, self.gui_get_one(path)

    def gui_add_one(self, directory_opt):
        directory_path = directory_opt.get_path()
        path = directory_path[len(self._root):]
        if self.gui_check_exists(path) is False:
            path_opt = bsc_core.BscNodePathOpt(path)
            #
            parent_gui = self.gui_get_one(path_opt.get_parent_path())
            #
            prx_item = parent_gui.add_child(
                path_opt.name,
                icon=gui_core.GuiIcon.get_directory(),
            )
            self.gui_register(path, prx_item)
            prx_item.set_tool_tip(path)
            if path in self._cache_expand_current:
                prx_item.set_expanded(self._cache_expand_current[path])

            prx_item.set_gui_dcc_obj(
                directory_opt, self._namespace
            )

            prx_item.set_checked(False)
            prx_item.set_gui_menu_data(
                [
                    ('system',),
                    ('open folder', 'file/open-folder', directory_opt.show_in_system)
                ]
            )
            if directory_opt.get_is_readable() is False:
                prx_item.set_status(
                    prx_item.ValidationStatus.Unreadable
                )
            elif directory_opt.get_is_writeable() is False:
                prx_item.set_status(
                    prx_item.ValidationStatus.Unwritable
                )
            return prx_item
        return self.gui_get_one(path)

    def gui_add_all(self, directory_path):
        directory_opt = bsc_storage.StgDirectoryOpt(directory_path)
        # add root first
        self.gui_add_root(
            directory_opt
        )
        all_directories = directory_opt.get_all_directories()
        for i_directory_opt in all_directories:
            self.gui_add_one(i_directory_opt)

    def gui_add_all_use_thread(self, directory_path):
        def cache_fnc_():
            return [
                self._gui_thread_flag,
                directory_opt.get_all_directories()
            ]

        def build_fnc_(*args):
            _index_thread_batch_current, _all_directories = args[0]
            with self._prx_tree_view.gui_bustling():
                for _i_directory_opt in _all_directories:
                    if _index_thread_batch_current != self._gui_thread_flag:
                        break
                    self.gui_add_one(_i_directory_opt)

        def post_fnc_():
            pass

        self._gui_thread_flag += 1

        directory_opt = bsc_storage.StgDirectoryOpt(directory_path)
        self.gui_add_root(
            directory_opt
        )

        t = gui_qt_core.QtBuildThread(self._prx_tree_view.get_widget())
        t.set_cache_fnc(cache_fnc_)
        t.cache_value_accepted.connect(build_fnc_)
        t.run_finished.connect(post_fnc_)
        #
        t.start()


class AbsGuiPrxTreeViewAsStorageOpt(AbsGuiPrxTreeViewOpt):
    def _init_tree_view_as_storage_opt_(self, prx_tree_view, namespace):
        self._init_tree_view_opt_(prx_tree_view, namespace)

        self._gui_thread_flag = 0
        self._root = None

        self._cache_expand_all = dict()
        self._cache_expand_current = dict()

    def restore(self):
        self.__push_expand_cache()

        self._prx_tree_view.do_clear()
        self._keys.clear()

    def __push_expand_cache(self):
        if self._root is not None:
            if self._root not in self._cache_expand_all:
                expand_dict = dict()
                self._cache_expand_all[self._root] = expand_dict
            else:
                expand_dict = self._cache_expand_all[self._root]

            for k, v in self._item_dict.items():
                expand_dict[k] = v.get_is_expanded()

    def __pull_expand_cache(self):
        # load expand cache
        if self._root in self._cache_expand_all:
            self._cache_expand_current = self._cache_expand_all[self._root]

    def gui_add_root(self, directory_opt):
        directory_path = directory_opt.get_path()
        self._root = directory_opt.get_parent_path()

        self.__pull_expand_cache()

        path = directory_path[len(self._root):]
        if self.gui_check_exists(path) is False:
            path_opt = bsc_core.BscNodePathOpt(path)

            prx_item = self._prx_tree_view.create_item(
                path_opt.get_name(),
                icon=gui_qt_core.GuiQtDcc.generate_qt_directory_icon(use_system=True),
            )
            self.gui_register(path, prx_item)

            prx_item.set_gui_dcc_obj(
                directory_opt, self._namespace
            )

            prx_item.set_expanded(True)
            prx_item.set_checked(False)
            prx_item.set_gui_menu_data(
                [
                    ('system',),
                    ('open folder', 'file/open-folder', directory_opt.show_in_system)
                ]
            )
            return True, prx_item
        return False, self.gui_get_one(path)

    def gui_add_one(self, stg_opt):
        stg_path = stg_opt.get_path()
        path = stg_path[len(self._root):]
        if self.gui_check_exists(path) is False:
            path_opt = bsc_core.BscNodePathOpt(path)
            #
            parent_gui = self.gui_get_one(path_opt.get_parent_path())

            time_txt = bsc_core.ensure_string(
                bsc_core.BscTimePrettify.to_prettify_by_timestamp(
                    stg_opt.get_mtime(), language=1
                )
            )
            #
            if stg_opt.get_is_file():
                icon = gui_qt_core.GuiQtDcc.generate_qt_file_icon(stg_path)
            else:
                icon = gui_qt_core.GuiQtDcc.generate_qt_directory_icon(use_system=True)

            prx_item = parent_gui.add_child(
                path_opt.name,
                icon=icon,
            )
            prx_item.set_name(time_txt, 1)
            self.gui_register(path, prx_item)
            prx_item.set_tool_tip(path)
            if path in self._cache_expand_current:
                prx_item.set_expanded(self._cache_expand_current[path])

            prx_item.set_gui_dcc_obj(
                stg_opt, self._namespace
            )

            prx_item.set_checked(False)
            prx_item.set_gui_menu_data(
                [
                    ('system',),
                    ('open folder', 'file/open-folder', stg_opt.show_in_system)
                ]
            )
            if stg_opt.get_is_readable() is False:
                prx_item.set_status(
                    prx_item.ValidationStatus.Unreadable
                )
            elif stg_opt.get_is_writeable() is False:
                prx_item.set_status(
                    prx_item.ValidationStatus.Unwritable
                )
            return prx_item
        return self.gui_get_one(path)

    def gui_add_all(self, root):
        directory_opt = bsc_storage.StgDirectoryOpt(root)
        # add root first
        self.gui_add_root(
            directory_opt
        )
        all_directories = directory_opt.get_all_directories()
        for i_directory_opt in all_directories:
            self.gui_add_one(i_directory_opt)

    def gui_add_all_use_thread(self, root):
        def cache_fnc_():
            return [
                self._gui_thread_flag,
                directory_opt.get_all()
            ]

        def build_fnc_(*args):
            _index_thread_batch_current, _all_opts = args[0]
            with self._prx_tree_view.gui_bustling():
                for _i_opt in _all_opts:
                    if _index_thread_batch_current != self._gui_thread_flag:
                        break
                    self.gui_add_one(_i_opt)

        def post_fnc_():
            pass

        self._gui_thread_flag += 1

        directory_opt = bsc_storage.StgDirectoryOpt(root)
        self.gui_add_root(
            directory_opt
        )

        t = gui_qt_core.QtBuildThread(self._prx_tree_view.get_widget())
        t.set_cache_fnc(cache_fnc_)
        t.cache_value_accepted.connect(build_fnc_)
        t.run_finished.connect(post_fnc_)
        #
        t.start()


class AbsGuiTreeViewAsTagOpt(AbsGuiPrxTreeViewOpt):
    ROOT_NAME = 'All'

    class GroupScheme(object):
        Disable = 0x01
        Hide = 0x02

    GROUP_SCHEME = GroupScheme.Disable

    def _init_tree_view_as_tag_opt_(self, prx_tree_view, namespace):
        self._init_tree_view_opt_(prx_tree_view, namespace)

        self._group_item_dict = {}
        self._tag_item_dict = {}

        self._count_tag_dict = {}

        self._check_cache_dict = {}

    def __push_check_cache(self):
        pass

    def __pull_check_cache(self):
        for k, v in self._item_dict.items():
            pass

    def restore(self):
        # self.__pull_check_cache()

        self._prx_tree_view.do_clear()
        self._group_item_dict.clear()
        self._tag_item_dict.clear()

        self._count_tag_dict.clear()

    def reset(self):
        self._count_tag_dict.clear()
        self._tag_item_dict.clear()
        for i_k, i_prx_item in self._group_item_dict.items():
            if i_k != '/':
                i_prx_item.clear_children()
                i_prx_item.set_checked(False)
                if self.GROUP_SCHEME == self.GroupScheme.Disable:
                    i_prx_item.set_enable(False)
                    i_prx_item.set_status(
                        i_prx_item.ValidationStatus.Disable
                    )

                elif self.GROUP_SCHEME == self.GroupScheme.Hide:
                    i_prx_item.set_visible(False)

    def gui_get_group_is_exists(self, path):
        return path in self._group_item_dict

    def gui_get_group(self, path):
        return self._group_item_dict[path]

    def gui_get_tag(self, path):
        return self._tag_item_dict[path]

    def gui_check_exists(self, path):
        return path in self._tag_item_dict

    def gui_register_group(self, path, prx_item):
        # self.gui_register(path, prx_item)
        self._group_item_dict[path] = prx_item

    def gui_register_tag(self, path, prx_item):
        # self.gui_register(path, prx_item)
        self._tag_item_dict[path] = prx_item

    def gui_get_one(self, path):
        return self._tag_item_dict[path]

    def gui_add_root(self):
        path = '/'
        if self.gui_get_group_is_exists(path) is False:
            prx_item = self._prx_tree_view.create_item(
                self.ROOT_NAME,
                icon=gui_core.GuiIcon.get('database/all'),
            )

            self.gui_register_group(path, prx_item)

            prx_item.set_expanded(True)
            prx_item.set_checked(False)
            prx_item.set_emit_send_enable(True)
            return True, prx_item
        return False, self.gui_get_group(path)

    def gui_add_group_by_path(self, path):
        if self.gui_get_group_is_exists(path) is False:
            path_opt = bsc_core.BscNodePathOpt(path)
            parent_gui = self.gui_get_group(path_opt.get_parent_path())
            gui_name = bsc_core.RawStrUnderlineOpt(path_opt.get_name()).to_prettify()
            prx_item = parent_gui.add_child(
                gui_name,
                icon=gui_core.GuiIcon.get('database/group'),
            )

            self.gui_register_group(path, prx_item)

            prx_item.set_tool_tip(path)
            prx_item.set_checked(False)
            prx_item.set_expanded(True)
            if self.GROUP_SCHEME == self.GroupScheme.Disable:
                prx_item.set_enable(False)
                prx_item.set_status(prx_item.ValidationStatus.Disable)
            elif self.GROUP_SCHEME == self.GroupScheme.Hide:
                prx_item.set_visible(False)
            prx_item.set_emit_send_enable(True)
            return prx_item
        return self.gui_get_group(path)

    def gui_add_tag_by_path(self, path):
        if self.gui_check_exists(path) is False:
            path_opt = bsc_core.BscNodePathOpt(path)
            parent_path = path_opt.get_parent_path()
            parent_prx_item = self.gui_get_group(parent_path)
            if self.GROUP_SCHEME == self.GroupScheme.Disable:
                parent_prx_item.set_enable(True)
                parent_prx_item.set_status(parent_prx_item.ValidationStatus.Normal)
            elif self.GROUP_SCHEME == self.GroupScheme.Hide:
                parent_prx_item.set_visible(True)

            gui_name = bsc_core.RawStrUnderlineOpt(path_opt.get_name()).to_prettify()
            prx_item = parent_prx_item.add_child(
                gui_name,
                icon=gui_core.GuiIcon.get('database/tag'),
            )

            self.gui_register_tag(path, prx_item)

            prx_item.set_checked(False)
            prx_item.set_emit_send_enable(True)

            prx_item.set_name('0', 1)
            return prx_item
        return self.gui_get_tag(path)

    def gui_register_tag_by_path(self, tag_path, path, auto_create_ancestors=False):
        if auto_create_ancestors is True:
            path_opt = bsc_core.BscNodePathOpt(tag_path)
            ancestors = path_opt.get_ancestors()
            ancestors.reverse()
            for i_path_opt in ancestors:
                i_path = i_path_opt.path
                if self.gui_get_group_is_exists(i_path) is False:
                    self.gui_add_group_by_path(i_path)

        prx_item = self.gui_add_tag_by_path(tag_path)

        self._count_tag_dict.setdefault(tag_path, set()).add(path)

        if tag_path in self._count_tag_dict:
            prx_item.set_name(
                str(len(self._count_tag_dict[tag_path])),
                1
            )

    def generate_tag_filter_data_src(self):
        set_ = set()
        for i_tag_path, i_prx_item in self._tag_item_dict.items():
            if i_prx_item.get_is_checked() is True:
                set_.add(i_tag_path)
        return set_

    def generate_tag_filter_data_tgt(self, *args, **kwargs):
        pass

    def generate_semantic_tag_filter_data_src(self):
        dict_ = {}
        for i_tag_path, i_prx_item in self._tag_item_dict.items():
            if i_prx_item.get_is_checked() is True:
                i_group_path = bsc_core.BscNodePathOpt(i_tag_path).get_parent_path()
                dict_.setdefault(i_group_path, set()).add(i_tag_path)
        return dict_

    def generate_semantic_tag_filter_data_tgt(self, *args, **kwargs):
        pass


class AbsGuiPrxListViewOpt(object):
    def _init_list_view_opt_(self, prx_list_view, namespace):
        self._prx_list_view = prx_list_view
        self._item_dict = self._prx_list_view._item_dict
        self._keys = set()

        self._gui_thread_flag = 0

        self._namespace = namespace

    def register_occurrence(self, key, path):
        prx_item = self.gui_get_one(path)
        self._prx_list_view._qt_view._register_keyword_filter_occurrence_(key, prx_item.get_item())

    def restore(self):
        self._prx_list_view.do_clear()
        self._keys.clear()
        self._prx_list_view.refresh_check_info()

    def gui_check_exists(self, path):
        return self._item_dict.get(path) is not None

    def gui_get_one(self, path):
        return self._item_dict[path]

    def gui_register(self, path, prx_item):
        self._item_dict[path] = prx_item
        prx_item.set_gui_attribute('path', path)

    def get_current_obj(self):
        _ = self._prx_list_view.get_selected_items()
        if _:
            return _[-1].get_gui_dcc_obj(self._namespace)


class AbsGuiQtListWidgetOpt(object):
    def _init_list_view_opt_(self, qt_list_widget, namespace):
        self._qt_list_widget = qt_list_widget
        self._gui_thread_flag = 0

    def restore(self):
        self._qt_list_widget._view_model.restore()

    def gui_check_exists(self, path):
        return self._qt_list_widget._view_model._check_item_exists(path)

    def gui_get_one(self, path):
        return self._qt_list_widget._view_model._get_item(path)

    def gui_register(self, path, qt_item):
        self._qt_list_widget._view_model._register_item(path, qt_item)


class AbsGuiPrxListViewAsFileOpt(AbsGuiPrxListViewOpt):
    def _init_list_view_as_file_opt_(self, prx_list_view, namespace):
        self._init_list_view_opt_(prx_list_view, namespace)
