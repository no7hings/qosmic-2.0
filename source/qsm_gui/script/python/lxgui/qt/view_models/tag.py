# coding:utf-8
import collections

from . import base as _base


class TagViewModel(object):
    def __init__(self, widget):

        self._widget = widget

        self._data = _base._Data(
            item_dict=collections.OrderedDict(),
            item=_base._Data(
                cls=None,
                group_cls=None,
            ),
        )

    def create_group(self, path, *args, **kwargs):
        return self._widget._create_group_(path, *args, **kwargs)

    def create_node(self, path, *args, **kwargs):
        return self._widget._create_node_(path, *args, **kwargs)

    def check_exists(self, path):
        return self._widget._check_exists_(path)

    def get_one(self, path):
        return self._widget._get_one_(path)

    def set_node_checked(self, path, boolean):
        _ = self.get_one(path)
        if _:
            _._apply_check_state_(boolean)

    def expand_exclusive_for_node(self, path):
        self._widget._expand_exclusive_for_node_(path)

    def expand_all_groups(self):
        self._widget._expand_all_groups_()

    def collapse_all_group_items(self):
        self._widget._collapse_all_group_items_()

    def set_item_expand_below(self, path):
        self._widget._expand_for_all_from_(path)

    def clear_all_item_check(self):
        self._widget._clear_all_checked_()

    def connect_check_paths_changed_to(self, fnc):
        self._widget.check_paths_changed.connect(fnc)

    def intersection_all_item_assign_path_set(self, path_set):
        self._widget._apply_intersection_paths_(path_set)

    def get_checked_item_paths(self):
        return self._widget._get_all_checked_node_paths_()

    def set_force_hidden_flag_for_group(self, path, boolean):
        self._widget._set_force_hidden_flag_for_group_(path, boolean)

    def restore(self):
        self._widget._restore_()