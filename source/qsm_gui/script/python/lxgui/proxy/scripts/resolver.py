# coding:utf-8
import functools
# gui
from ... import core as gui_core


class GuiPrxScpForRsvTask(object):
    def __init__(self, prx_list_view, namespace):
        self._prx_list_view = prx_list_view

        self._namespace = namespace

        self._prx_list_view.set_view_list_mode()

    def restore_all(self):
        self._prx_list_view.set_clear()

    def append(self, rsv_task):
        def cache_fnc_():
            return [prx_item, rsv_task]

        def build_fnc_(data_):
            self._set_show_deferred_(data_)

        prx_item = self._prx_list_view.create_item()
        prx_item.set_gui_dcc_obj(
            rsv_task, namespace=self._namespace
        )
        prx_item.set_show_fnc(
            cache_fnc_, build_fnc_
        )
        return True, prx_item

    def _set_show_deferred_(self, data):
        pass
        # prx_item, rsv_task = data


class GuiPrxScpForResolver(object):
    DCC_NAMESPACE = 'resolver'
    ROOT_NAME = 'All'

    def __init__(self, resolver, prx_tree_view, prx_tree_item_cls):
        self._resolver = resolver
        self._tree_view = prx_tree_view
        self._tree_item_cls = prx_tree_item_cls
        #
        self._item_dict = self._tree_view._item_dict
        self._keys = set()

    def gui_get_is_exists(self, path):
        return self._item_dict.get(path) is not None

    def gui_get(self, path):
        return self._item_dict[path]

    def gui_register(self, path, prx_item):
        self._item_dict[path] = prx_item
        prx_item.set_gui_attribute('path', path)

    def restore(self):
        self._tree_view.set_clear()
        self._keys.clear()

    def gui_add_root(self):
        path = '/'
        if self.gui_get_is_exists(path) is False:
            prx_item = self._tree_view.create_item(
                self.ROOT_NAME,
                icon=gui_core.GuiIcon.get('database/all'),
            )
            self.gui_register(path, prx_item)
            prx_item.set_gui_dcc_obj(self._resolver, namespace=self.DCC_NAMESPACE)
            prx_item.set_expanded(True)
            prx_item.set_checked(False)
            return True, prx_item
        return False, self.gui_get(path)

    def gui_add(self, obj, use_show_thread=False):
        name = obj.name
        path = obj.path
        type_name = obj.type
        if self.gui_get_is_exists(path) is True:
            prx_item = self.gui_get(path)
            return False, prx_item
        else:
            create_kwargs = dict(
                name=name,
                item_class=self._tree_item_cls,
                filter_key=obj.path
            )
            parent = obj.get_parent()
            if parent is not None:
                prx_item_parent = self.gui_get(parent.path)
                prx_item = prx_item_parent.add_child(
                    **create_kwargs
                )
            else:
                prx_item = self._tree_view.create_item(
                    **create_kwargs
                )
            #
            prx_item.set_type(obj.get_type_name())
            prx_item.set_checked(False)
            prx_item.update_keyword_filter_keys_tgt(
                [type_name, name]
            )
            obj.set_obj_gui(prx_item)
            prx_item.set_gui_dcc_obj(obj, namespace=self.DCC_NAMESPACE)
            self.gui_register(path, prx_item)
            #
            if use_show_thread is True:
                prx_item.set_show_build_fnc(
                    functools.partial(
                        self.gui_show_deferred_fnc, prx_item
                    )
                )
                return True, prx_item
            #
            self.gui_show_deferred_fnc(prx_item)
            return True, prx_item

    def gui_show_deferred_fnc(self, prx_item):
        def expand_by_condition_fnc_(*args):
            _prx_item = args[0]
            type_name = _prx_item.get_name(1)
            return type_name

        #
        obj = prx_item.get_gui_dcc_obj(namespace=self.DCC_NAMESPACE)
        obj_type_name = obj.type_name
        name = obj.name
        #
        menu_raw = []
        menu_raw.extend(
            obj.get_gui_menu_raw() or []
        )
        menu_raw.extend(
            obj.get_gui_extend_menu_raw() or []
        )
        #
        prx_item.set_icon_by_file(obj.icon)
        prx_item.set_name(name)
        prx_item.set_tool_tip(obj.description)
        #
        menu_raw.extend(
            [
                ('expanded',),
                ('Expand branch', None, prx_item.set_expand_branch),
                ('Collapse branch', None, prx_item.set_collapse_branch),
                # (),
                # [
                #     'Expand branch to', None,
                #     [
                #         ('Role / Sequence', None, lambda: prx_item.set_expand_branch_by_condition(expand_by_condition_fnc_, ['role', 'sequence'])),
                #         ('Asset / Shot', None, lambda: prx_item.set_expand_branch_by_condition(expand_by_condition_fnc_, ['asset', 'shot'])),
                #         ('Step', None, lambda: prx_item.set_expand_branch_by_condition(expand_by_condition_fnc_, ['step'])),
                #         ('Task', None, lambda: prx_item.set_expand_branch_by_condition(expand_by_condition_fnc_, ['task']))
                #     ]
                # ]
            ]
        )
        prx_item.set_gui_menu_raw(menu_raw)
        prx_item.set_menu_content(obj.get_gui_menu_content())

    def gui_add_as_tree(self, obj):
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            for i in ancestors:
                i_path = i.get_path()
                if self.gui_get_is_exists(i_path) is False:
                    self.gui_add(i, use_show_thread=True)
        #
        return self.gui_add(obj, use_show_thread=True)

    def gui_add_as_list(self, obj):
        pass
