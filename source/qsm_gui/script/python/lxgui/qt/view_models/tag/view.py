# coding:utf-8
import lxbasic.core as bsc_core

from .. import base as _base

from .. import view_base as _view_base


class TagViewModel(_view_base.AbsViewModel):
    def __init__(self, widget):
        super(TagViewModel, self).__init__(
            widget,
            _base._Data(
                item=_base._Data(
                    cls=None,
                    group_cls=None,
                ),
            )
        )

    def get_one(self, path):
        return self._widget._get_one_(path)

    def set_node_checked_for(self, path, boolean):
        _ = self.get_one(path)
        if _:
            _._update_check_state_(boolean)

    def expand_exclusive_for_node(self, path):
        self._widget._expand_exclusive_for_node_(path)

    def expand_all_group_items(self):
        self._widget._expand_all_group_items_()

    def collapse_all_group_items(self):
        self._widget._collapse_all_group_items_()

    def set_item_expand_below(self, path):
        self._widget._expand_for_all_from_(path)

    def uncheck_all_items(self):
        self._widget._uncheck_all_items_()

    def connect_check_paths_changed_to(self, fnc):
        self._widget.check_paths_changed.connect(fnc)

    def intersection_all_item_assign_path_set(self, path_set):
        self._widget._apply_intersection_paths_(path_set)

    def get_all_checked_node_paths(self):
        return self._widget._get_all_checked_node_paths_()

    def get_all_nodes(self):
        return self._widget._get_all_nodes_()

    def get_all_items(self):
        return self._widget._get_all_items_()

    def restore(self, clear_expand_record=False):
        if self._data.item_expand_record_enable is True:
            data = self._data.item_expand_record.data
            # keep record default
            if clear_expand_record is True:
                data.clear()

            for k, v in self._data.item_dict.items():
                if v.GROUP_FLAG is True:
                    data[k] = v._is_expanded_()

        self._widget._restore_()

    def create_item_as_group(self, path, *args, **kwargs):
        return self._widget._create_group_(path, *args, **kwargs)

    def create_group_item(self, path, *args, **kwargs):
        return self._widget._create_group_(path, *args, **kwargs)

    def create_item(self, path, *args, **kwargs):
        return self._widget._create_node_(path, *args, **kwargs)

    def create_item_(self, path, *args, **kwargs):
        if path in self._data.item_dict:
            return False, self._data.item_dict[path]

        path_opt = bsc_core.BscNodePathOpt(path)
        index_cur = len(self._data.item_dict)
        item = self._data.item.cls()

        parent_path = path_opt.get_parent_path()
        if parent_path not in self._data.item_dict:
            raise RuntimeError()
        parent_item = self._data.item_dict[parent_path]
        if isinstance(parent_item, self._data.item.group_cls) is False:
            raise RuntimeError()

        parent_item._add_node_(item)

        name = path_opt.get_name()
        item._item_model.set_path(path)
        item._item_model.set_index(index_cur)
        item._item_model.set_name(name)
        item.user_filter_checked.connect(self._widget._user_filter_check_cbk_)

        self._data.item_dict[path] = item
        return True, item

    def _remove_item_fnc(self, item):
        item._do_delete_()
