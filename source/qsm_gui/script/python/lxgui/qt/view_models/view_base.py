# coding:utf-8
import collections

import functools

from ... import core as _gui_core
# qt
from ...qt.core.wrap import *


class AbsViewModel(object):
    ItemMode = _gui_core.GuiItemMode

    ItemSortKey = _gui_core.GuiItemSortKey
    ItemSortOrder = _gui_core.GuiItemSortOrder

    ItemGroupKey = _gui_core.GuiItemGroupKey

    def do_close(self):
        self._close_flag = True

    def do_drop(self, event):
        pass

    def _on_item_check_changed(self):
        self.refresh_info()

    def __init__(self, widget, data):
        self._widget = widget

        self._data = data
        # item index
        self._data.item_index_enable = True
        # item category
        self._data.item_category_enable = False
        # item type
        self._data.item_type_enable = False
        # item name
        self._data.item_name_enable = True
        # item mtime
        self._data.item_mtime_enable = False
        # item user
        self._data.item_user_enable = False
        # item number
        self._data.item_number_enable = False
        # item lock
        self._data.item_lock_enable = False
        # item check
        self._data.item_check_enable = False
        self._data.item_color_enable = False
        # item drag
        self._data.item_drag_enable = False
        # item drop
        self._data.item_drop_enable = False
        # item sort
        self._data.item_sort_enable = False
        # item expand record
        self._data.item_expand_record_enable = False
        # menu
        self._data.menu = _gui_core.DictOpt(
            content=None,
            data=None,
            data_generate_fnc=None,
            name_dict=dict()
        )
        # keyword filter
        self._data.keyword_filter = _gui_core.DictOpt(
            key_src_set=set(),
            cache=None
        )
        # tag filter
        self._data.tag_filter = _gui_core.DictOpt(
            key_src_set=set(),
            cache=None
        )
        # occurrence
        self._data.occurrence = _gui_core.DictOpt(
            index=None
        )
        # item query
        self._data.item_dict = collections.OrderedDict()
        # information
        self._data.info = ''

        self._close_flag = False

    # item index
    def set_item_index_enable(self, boolean):
        self._data.item_index_enable = boolean

    def is_item_index_enable(self):
        return self._data.item_index_enable

    # item category
    def set_item_category_enable(self, boolean):
        self._data.item_category_enable = boolean

    def is_item_category_enable(self):
        return self._data.item_category_enable

    # item type
    def set_item_type_enable(self, boolean):
        self._data.item_type_enable = boolean

    def is_item_type_enable(self):
        return self._data.item_type_enable
    
    # item name
    def set_item_name_enable(self, boolean):
        self._data.item_name_enable = boolean

    def is_item_name_enable(self):
        return self._data.item_name_enable

    # item mtime
    def set_item_mtime_enable(self, boolean):
        self._data.item_mtime_enable = boolean

    def is_item_mtime_enable(self):
        return self._data.item_mtime_enable

    # item user
    def set_item_user_enable(self, boolean):
        self._data.item_user_enable = boolean

    def is_item_user_enable(self):
        return self._data.item_user_enable

    # item number
    def set_item_number_enable(self, boolean):
        self._data.item_number_enable = boolean

    def is_item_number_enable(self):
        return self._data.item_number_enable

    # item lock
    def set_item_lock_enable(self, boolean):
        self._data.item_lock_enable = boolean

    def is_item_lock_enable(self):
        return self._data.item_lock_enable

    # item check
    def set_item_check_enable(self, boolean):
        self._data.item_check_enable = boolean

    def is_item_check_enable(self):
        return self._data.item_check_enable

    # item color
    def set_item_color_enable(self, boolean):
        if boolean != self._data.item_color_enable:
            self._data.item_color_enable = boolean

    def is_item_color_enable(self):
        return self._data.item_color_enable

    # item sort
    def set_item_sort_enable(self, boolean):
        self._data.item_sort_enable = boolean
        if boolean is True:
            self._data.item_sort = _gui_core.DictOpt(
                keys=[],
                key_current=self.ItemSortKey.Name,
                order=0,
            )

        self._widget.setSortingEnabled(boolean)
        # sort later
        if isinstance(self._widget, QtWidgets.QListWidget):
            self._widget.sortItems(QtCore.Qt.AscendingOrder)
        elif isinstance(self._widget, QtWidgets.QTreeWidget):
            self._widget.sortByColumn(0, QtCore.Qt.AscendingOrder)

    def is_item_sort_enable(self):
        return self._data.item_sort_enable

    def set_item_sort_keys(self, keys):
        if self._data.item_sort_enable is True:
            assert isinstance(keys, list)

            self._data.item_sort.keys = keys

    def apply_item_sort_order(self, sort_order):
        if self._data.item_sort_enable is True:
            self._data.item_sort.order = sort_order

            [x._item_model.apply_sort_order(sort_order) for x in self.get_all_items()]

            self._update_item_sort()

    def get_item_sort_order(self):
        if self._data.item_sort_enable is True:
            return self._data.item_sort.order

    def get_item_sort_keys(self):
        if self._data.item_sort_enable is True:
            return self._data.item_sort.keys
        return []

    def get_item_sort_key_current(self):
        if self._data.item_sort_enable is True:
            return self._data.item_sort.key_current

    def sort_item_by(self, sort_key):
        if self._data.item_sort_enable is True:
            self._data.item_sort.key_current = sort_key

            [x._item_model.apply_sort_key(sort_key) for x in self.get_all_items()]

            self._update_item_sort()

    def _update_item_sort(self):
        if self._data.item_sort_enable is True:
            self._sort_items_fnc(
                [QtCore.Qt.AscendingOrder, QtCore.Qt.DescendingOrder][self._data.item_sort.order]
            )

    def _sort_items_fnc(self, order):
        raise NotImplementedError()

    def swap_item_sort_order(self):
        if self._data.item_sort_enable is True:
            if self._data.item_sort.order == self.ItemSortOrder.Ascending:
                self.apply_item_sort_order(self.ItemSortOrder.Descending)
            else:
                self.apply_item_sort_order(self.ItemSortOrder.Ascending)

    def generate_item_sort_menu_data(self):
        if self._data.item_sort_enable is True:
            menu_data = [
                (_gui_core.GuiName.SortByChs,) if _gui_core.GuiUtil.language_is_chs() else (_gui_core.GuiName.SortBy,)
            ]

            for i_sort_key in self.ItemSortKey.ALL:
                if i_sort_key == self._data.item_sort.key_current:
                    i_icon_name = 'radio_checked'
                else:
                    i_icon_name = 'radio_unchecked'

                if _gui_core.GuiUtil.language_is_chs():
                    i_name = self.ItemSortKey.NAME_MAP_CHS[i_sort_key]
                else:
                    i_name = self.ItemSortKey.NAME_MAP[i_sort_key]

                if i_sort_key == self.ItemSortKey.Default:
                    menu_data.append(
                        (
                            i_name,
                            i_icon_name,
                            functools.partial(self.sort_item_by, i_sort_key)
                        )
                    )
                else:
                    i_enable = self._data.get('item_{}_enable'.format(i_sort_key))
                    if i_enable is True:
                        menu_data.append(
                            (
                                i_name,
                                i_icon_name,
                                functools.partial(self.sort_item_by, i_sort_key)
                            )
                        )

            menu_data.append(
                ()
            )

            for i_sort_order in self.ItemSortOrder.ALL:
                if i_sort_order == self._data.item_sort.order:
                    i_icon_name = 'radio_checked'
                else:
                    i_icon_name = 'radio_unchecked'

                if _gui_core.GuiUtil.language_is_chs():
                    i_name = self.ItemSortOrder.NAME_MAP_CHS[i_sort_order]
                else:
                    i_name = self.ItemSortOrder.NAME_MAP[i_sort_order]

                menu_data.append(
                    (
                        i_name,
                        i_icon_name,
                        functools.partial(self.apply_item_sort_order, i_sort_order)
                    )
                )

            return menu_data
        return []

    # item drag
    def set_item_drag_enable(self, boolean):
        if boolean != self._data.item_drag_enable:
            self._data.item_drag_enable = boolean
            # fixme: may drop is enable
            self._widget.setDragDropMode(self._widget.DragOnly)

            self._update_item_drag_enable()

    def _update_item_drag_enable(self):
        self._widget.setDragEnabled(self._data.item_drag_enable)

    def get_item_drag_enable(self):
        return self._data.item_drag_enable

    # item drop
    def set_item_drop_enable(self, boolean):
        if boolean != self._data.item_drop_enable:
            self._data.item_drop_enable = boolean
            self._update_item_drop_enable()

    def _update_item_drop_enable(self):
        self._widget.setAcceptDrops(self._data.item_drop_enable)
        self._widget.setDropIndicatorShown(False)

    # keyword filter
    def set_keyword_filter_key_src(self, texts):
        self._data.keyword_filter.key_src_set = set(texts)

    def refresh_items_visible_by_any_filter(self):
        t_f_key_src_set = self._data.tag_filter.key_src_set
        k_f_key_src_set = self._data.keyword_filter.key_src_set

        items = self.get_all_items()
        for i_item in items:
            i_force_hidden_flag = i_item._item_model.get_force_hidden_flag()
            if i_force_hidden_flag is True:
                i_is_hidden = True
            else:

                # tag
                i_tag_flag = False
                if t_f_key_src_set:
                    i_enable, i_flag = i_item._item_model.generate_tag_filter_hidden_args(t_f_key_src_set)
                    if i_enable is True:
                        i_tag_flag = i_flag

                # semantic
                i_semantic_flag = False

                # keyword
                i_keyword_flag = False
                if k_f_key_src_set:
                    i_enable, i_flag = i_item._item_model.generate_keyword_filter_hidden_args(k_f_key_src_set)
                    if i_enable is True:
                        i_keyword_flag = i_flag

                # hide item when any flag is True
                if True in [i_tag_flag, i_semantic_flag, i_keyword_flag]:
                    i_is_hidden = True
                else:
                    i_is_hidden = False

            i_item.setHidden(i_is_hidden)

            # for tree
            for i in i_item._item_model.get_ancestors():
                if i_is_hidden is False:
                    i.setHidden(False)

    def generate_item_keyword_filter_keys(self):
        key_tgt_set = set()
        [key_tgt_set.update(i_item._item_model.get_keyword_filter_key_tgt_set()) for i_item in self.get_all_items()]
        return list(key_tgt_set)

    def generate_keyword_filter_completion_cache(self):
        if not self._data.keyword_filter.cache:
            self._data.keyword_filter.cache = self.generate_item_keyword_filter_keys()
        return self._data.keyword_filter.cache

    # tag filter
    def set_tag_filter_key_src(self, texts):
        self._data.tag_filter.key_src_set = set(texts)

    def get_all_items(self):
        raise NotImplementedError()

    def get_visible_items(self):
        raise NotImplementedError()

    def update_widget(self):
        # noinspection PyBroadException
        try:
            self._widget.update()
        except Exception:
            pass

    def set_all_items_checked(self, boolean):
        [x._item_model._update_check_state(boolean) for x in self.get_all_items()]
        self._widget.item_check_changed.emit()
        self.update_widget()

    def set_visible_items_checked(self, boolean):
        [x._item_model._update_check_state(boolean) for x in self.get_visible_items()]
        self._widget.item_check_changed.emit()
        self.update_widget()

    def get_checked_items(self):
        return [x for x in self.get_all_items() if x._item_model.is_checked()]

    def get_checked_item_paths(self):
        return [x._item_model.get_path() for x in self.get_checked_items()]

    def get_checked_leaf_items(self):
        return [x for x in self.get_checked_items() if not x._item_model.get_children()]

    def get_selected_items(self):
        return self._widget.selectedItems()

    def get_selected_item_paths(self):
        return [x._item_model.get_path() for x in self.get_selected_items()]

    def get_selected_leaf_items(self):
        return [x for x in self.get_selected_items() if not x._item_model.get_children()]

    def get_all_leaf_items(self):
        return [x for x in self.get_all_items() if not x._item_model.get_children()]

    def select_first_leaf_item(self):
        leaf_items = self.get_all_leaf_items()
        if leaf_items:
            leaf_items[0].setSelected(True)

    def select_last_leaf_item(self):
        leaf_items = self.get_all_leaf_items()
        if leaf_items:
            leaf_items[-1].setSelected(True)

    def clear_item_selection(self):
        self._widget.clearSelection()

    def get_current_item(self):
        return self._widget.currentItem()

    def get_all_item_paths(self):
        return self._data.item_dict.keys()

    # item status
    def clear_all_items_status(self):
        for i in self.get_all_items():
            i._item_model.clear_status()

    # item expand record
    def set_item_expand_record_enable(self, boolean):
        if boolean is True:
            self._data.item_expand_record_enable = True
            self._data.item_expand_record = _gui_core.DictOpt(
                data={}
            )

    # menu
    def set_menu_content(self, content):
        self._data.menu.content = content

    def get_menu_content(self):
        return self._data.menu.content

    def set_menu_data(self, data):
        self._data.menu.data = data

    def get_menu_data(self):
        return self._data.menu.data

    def set_menu_data_generate_fnc(self, fnc):
        self._data.menu.data_generate_fnc = fnc

    def get_menu_data_generate_fnc(self):
        return self._data.menu.data_generate_fnc

    def set_menu_name_dict(self, dict_):
        if isinstance(dict_, dict):
            self._data.menu.name_dict = dict_

    def get_menu_name_dict(self):
        return self._data.menu.name_dict

    def refresh_info(self):
        c = len(self.get_checked_items())
        if c:
            info = '{} item is checked ...'.format(c)
        else:
            info = ''

        if info != self._data.info:
            self._widget.info_text_accepted.emit(info)
            self._data.info = info

    def restore(self):
        for i_item in self.get_all_items():
            i_item._item_model.do_close()

        self._data.keyword_filter.cache = None
        self._widget.clear()
        self._data.item_dict.clear()

        self.refresh_info()

    def _register_item(self, path, item):
        self._data.item_dict[path] = item

    def _check_item_exists(self, path):
        return self._data.item_dict.get(path) is not None

    def _get_item(self, path):
        return self._data.item_dict.get(path)

    def find_item(self, path):
        return self._data.item_dict.get(path)

    def _remove_item(self, path):
        item = self._get_item(path)
        if item:
            self._remove_item_fnc(item)
            self._data.item_dict.pop(path)
            p = '{}/'.format(path)
            for i in self._data.item_dict.keys():
                if i.startswith(p):
                    self._data.item_dict.pop(i)

    def _remove_item_fnc(self, item):
        raise NotImplementedError()

    def _set_item_checked(self, path, boolean):
        item = self._get_item(path)
        if item:
            item._item_model.set_checked(boolean)

    # assign
    def intersection_all_item_assign_path_set(self, path_set):
        for i_item in self.get_all_items():
            i_item._item_model.intersection_assign_path_set(path_set)

    def generate_drag_data_for(self, items):
        list_ = []

        for i_item in items:
            i_item_model = i_item._item_model

            # ignore when is locked
            if i_item_model.is_locked():
                continue

            # ignore when daga is disabled
            if i_item_model.is_drag_enable() is False:
                continue

            i_drag_data_0 = i_item_model.get_drag_data()
            if i_drag_data_0:
                list_.append(i_drag_data_0)
            else:
                i_drag_data_1 = i_item_model.generate_drag_data()
                if i_drag_data_1:
                    list_.append(i_drag_data_1)
        return list_

    def create_group_item(self, path, *args, **kwargs):
        raise NotImplementedError()

    def create_item(self, path, *args, **kwargs):
        raise NotImplementedError()
