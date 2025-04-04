# coding:utf-8
# gui
from .... import core as _gui_core

from ....qt.widgets import utility as _qt_wgt_utility

from .. import view_for_tree as _wgt_view_for_tree

from . import _input_base


# array
#   nodes
class PrxInputForNodes(_input_base.AbsPrxInputExtra):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    PRX_INPUT_CLS = _wgt_view_for_tree.PrxTreeView
    NAMESPACE = 'dcc'

    def __init__(self, *args, **kwargs):
        super(PrxInputForNodes, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(162)
        self.widget.setMinimumHeight(162)
        self._prx_input.create_header_view(
            [('name', 1)],
            320
        )
        self._prx_input.set_selection_use_single()
        self._prx_input.set_size_policy_height_fixed_mode()
        self._prx_input.set_resize_target(self.widget)
        self._prx_input.set_resize_enable(True)
        self._prx_input.set_resize_minimum(82)
        #
        self._item_dict = self._prx_input._item_dict

        self._view_mode = 'list'

    def _add_item_component_as_tree(self, obj, as_group=False):
        path = obj.path
        # obj_type = obj.type
        if path in self._item_dict:
            prx_item = self._item_dict[path]
            return False, prx_item, None
        else:
            icon_name = obj.get('icon_name')
            if as_group is True:
                if not icon_name:
                    icon_name = 'database/group'
                create_kwargs = dict(
                    name='loading ...',
                    icon=_gui_core.GuiIcon.get(icon_name),
                    filter_key=path
                )
            else:
                if not icon_name:
                    icon_name = 'database/object'
                create_kwargs = dict(
                    name='loading ...',
                    icon=_gui_core.GuiIcon.get(icon_name),
                    filter_key=path
                )

            parent = obj.get_parent()
            if parent is not None:
                prx_item_parent = self._item_dict[parent.path]
                prx_item = prx_item_parent.add_child(
                    **create_kwargs
                )
                prx_item_parent.set_expanded(True)
            else:
                prx_item = self._prx_input.create_item(
                    **create_kwargs
                )

            if path == obj.pathsep:
                prx_item.set_expanded(True)

            prx_item.set_checked(True)
            prx_item.update_keyword_filter_keys_tgt([obj.name])
            prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
            self._item_dict[path] = prx_item

            prx_item.set_show_build_fnc(
                lambda *args, **kwargs: self._item_show_fnc(prx_item)
            )
            return True, prx_item, None

    # noinspection PyUnusedLocal
    def _item_show_fnc(self, prx_item, use_as_tree=True):
        obj = prx_item.get_gui_dcc_obj(namespace=self.NAMESPACE)
        prx_item.set_name(
            obj.get_name()
        )
        prx_item.set_tool_tip(
            (
                'path: {}\n'
            ).format(
                obj.get_path()
            )
        )

    def _add_item_as_tree(self, obj):
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            for i_obj in ancestors:
                ancestor_path = i_obj.path
                if ancestor_path not in self._item_dict:
                    i_is_create, i_prx_item, _ = self._add_item_component_as_tree(i_obj, as_group=True)
                    if i_is_create is True:
                        i_prx_item.set_expanded(True)

        self._add_item_component_as_tree(obj)

    def _add_item_as_list(self, obj):
        path = obj.path
        type_name = obj.type_name
        #
        create_kwargs = dict(
            name='loading ...',
            icon_name_text=type_name,
            filter_key=path
        )
        prx_item = self._prx_input.create_item(
            **create_kwargs
        )
        #
        prx_item.set_checked(True)
        prx_item.update_keyword_filter_keys_tgt([path, type_name])
        prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
        prx_item.set_tool_tip(path)
        self._item_dict[path] = prx_item
        #
        self._item_show_fnc(prx_item, use_as_tree=False)

    def _set_item_selected(self, obj):
        path = obj.path
        if path in self._item_dict:
            item = self._item_dict[path]
            self._prx_input.set_item_selected(
                item, exclusive=True
            )

    def __clear_items_(self):
        self._prx_input.do_clear()

    def set_view_mode(self, mode):
        self._view_mode = mode

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (tuple, list)):
            self.__clear_items_()
            objs = raw
            if objs:
                for i in objs:
                    if self._view_mode == 'list':
                        self._add_item_as_list(i)
                    elif self._view_mode == 'tree':
                        self._add_item_as_tree(i)

                # self._set_item_selected(
                #     objs[-1]
                # )
        else:
            pass

    def update_checked_by_paths(self, paths, extra=False):
        _ = self._prx_input.get_all_items()
        if _:
            for i in _:
                if i.get_gui_dcc_obj(namespace=self.NAMESPACE).path in paths:
                    i.set_checked(True, extra=extra)

    def update_unchecked_by_paths(self, paths, extra=False):
        _ = self._prx_input.get_all_items()
        if _:
            for i in _:
                if i.get_gui_dcc_obj(namespace=self.NAMESPACE).path not in paths:
                    i.set_checked(False, extra=extra)

    def set_all_items_checked(self, boolean):
        self._prx_input._qt_view._set_all_items_checked_(boolean)

    def update_check_by_dict(self, dict_):
        for k, v in dict_.items():
            i_item = self._item_dict[k]
            i_item.set_checked(v, extra=True)

    def get(self):
        _ = self._prx_input.get_all_items()
        if _:
            return [i.get_gui_dcc_obj(namespace=self.NAMESPACE) for i in _ if i.get_is_checked()]
        return []

    def get_all(self):
        _ = self._prx_input.get_all_items()
        if _:
            return [i.get_gui_dcc_obj(namespace=self.NAMESPACE) for i in _]
        return []

    def connect_input_changed_to(self, fnc):
        self._prx_input.connect_item_select_changed_to(
            fnc
        )
