# coding:utf-8
import collections

import functools

from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from . import base as _base


class AbsViewModel(object):
    ItemSortOrder = _gui_core.GuiItemSortOrder

    def do_close(self):
        self._close_flag = True

    def do_drop(self, event):
        pass

    @qt_slot()
    def _on_item_check_changed(self):
        self.refresh_info()

    def __init__(self, widget, data):
        self._widget = widget

        self._data = data
        # sort
        self._data.item_sort = _base._Data(
            enable=False,
            keys=[],
            key_current='index',
            order=0,
        )
        # item lock
        self._data.item_lock_enable = False
        # item check
        self._data.item_check_enable = False
        self._data.item_color_enable = False
        # item drag
        self._data.item_drag_enable = False
        # item drop
        self._data.item_drop_enable = False
        # menu
        self._data.menu = _base._Data(
            content=None,
            data=None,
            data_generate_fnc=None
        )
        # keyword filter
        self._data.keyword_filter = _base._Data(
            key_src_set=set(),
            cache=None
        )
        # occurrence
        self._data.occurrence = _base._Data(
            index=None
        )
        # item query
        self._data.item_dict = collections.OrderedDict()
        # information
        self._data.info = ''

        self._close_flag = False

    # sort
    def get_item_sort_order(self):
        return self._data.item_sort.order

    def set_item_sort_order(self, order):
        self._data.item_sort.order = order
        self._update_item_sort()

    def set_item_sort_keys(self, keys):
        if keys is not None:
            self._data.item_sort.enable = True
            self._data.item_sort.keys = keys
            self._widget.setSortingEnabled(True)
            if isinstance(self._widget, QtWidgets.QListWidget):
                self._widget.sortItems(QtCore.Qt.AscendingOrder)
            elif isinstance(self._widget, QtWidgets.QTreeWidget):
                self._widget.sortByColumn(0, QtCore.Qt.AscendingOrder)
            return True
        self._data.item_sort.enable = False
        return False

    def get_item_sort_keys(self):
        return self._data.item_sort.keys

    def get_item_sort_key_current(self):
        return self._data.item_sort.key_current

    def sort_item_by(self, key):
        self._data.item_sort.key_current = key
        [x._item_model.apply_sort(key) for x in self.get_all_items()]
        self._update_item_sort()

    def _update_item_sort(self):
        self._sort_items(
            [QtCore.Qt.AscendingOrder, QtCore.Qt.DescendingOrder][self.get_item_sort_order()]
        )

    def _sort_items(self, order):
        raise NotImplementedError()

    def swap_item_sort_order(self):
        if self._data.item_sort.order == self.ItemSortOrder.Ascend:
            self.set_item_sort_order(self.ItemSortOrder.Descend)
        else:
            self.set_item_sort_order(self.ItemSortOrder.Ascend)

    def generate_item_sort_menu_data(self):
        menu_data = []
        keys = self.get_item_sort_keys()
        order = ['ascend', 'descend'][self.get_item_sort_order()]
        icon_name = 'tool/sort-by-name-{}'.format(order)
        for i_key in keys+['index']:
            if i_key != self.get_item_sort_key_current():
                menu_data.append(
                    (i_key, icon_name, functools.partial(self.sort_item_by, i_key))
                )
        return menu_data

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
        key_src_set = self._data.keyword_filter.key_src_set

        items = self.get_all_items()
        for i_item in items:
            i_force_hidden_flag = i_item._item_model.get_force_hidden_flag()
            if i_force_hidden_flag is True:
                i_is_hidden = True
            else:
                i_tag_flag = False
                i_semantic_flag = False
                i_keyword_flag = False
                # keyword filter
                if key_src_set:
                    i_enable, i_flag = i_item._item_model.generate_keyword_filter_args(key_src_set)
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
        [x._item_model._update_check_state(boolean) for x in self.get_all_items()]
        self._widget.item_check_changed.emit()
        self.update_widget()

    def get_checked_items(self):
        return [x for x in self.get_all_items() if x._item_model.is_checked()]

    def get_checked_item_paths(self):
        return [x._item_model.get_path() for x in self.get_checked_items()]

    def get_selected_items(self):
        return self._widget.selectedItems()

    def get_selected_item_paths(self):
        return [x._item_model.get_path() for x in self.get_selected_items()]

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

    def _remove_item(self, path):
        item = self._get_item(path)
        if item:
            self._remove_item_fnc(item)
            self._data.item_dict.pop(path)

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

    def get_drag_data_for(self, items):
        list_ = []
        for i_item in items:
            if i_item._item_model.is_locked():
                continue

            i_drag_data = i_item._item_model.get_drag_data()
            if i_drag_data:
                list_.append(i_drag_data)
        return list_

    def create_item(self, path, *args, **kwargs):
        raise NotImplementedError()
