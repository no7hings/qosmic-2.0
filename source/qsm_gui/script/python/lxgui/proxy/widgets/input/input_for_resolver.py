# coding:utf-8

import functools

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage
# gui
from .... import core as _gui_core
# qt
from ....qt.widgets import utility as _qt_wgt_utility

from ....qt.widgets.input import input_for_constant as _qt_wgt_ipt_for_constant

from .. import view_for_tree as _wgt_view_for_tree

from . import _input_base


# entity
class PrxInputForRsvEntity(_input_base.AbsPrxInputExtra):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    PRX_INPUT_CLS = _wgt_view_for_tree.PrxTreeView
    NAMESPACE = 'resolver'

    def __init__(self, *args, **kwargs):
        super(PrxInputForRsvEntity, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(160)
        self.widget.setMinimumHeight(160)
        self._prx_input.create_header_view(
            [('name', 2), ('update', 1)],
            320
        )
        self._prx_input.set_selection_use_single()
        self._prx_input.set_size_policy_height_fixed_mode()
        # resize
        self._prx_input.set_resize_target(self.widget)
        self._prx_input.set_resize_enable(True)
        self._prx_input.set_resize_minimum(82)
        self._item_dict = {}

    def __set_item_comp_add_as_tree_(self, obj, use_show_thread=False):
        obj_path = obj.path
        obj_type = obj.type
        if obj_path in self._item_dict:
            prx_item = self._item_dict[obj_path]
            return False, prx_item, None
        else:
            create_kwargs = dict(
                name='loading ...',
                icon_name_text=obj_type,
                filter_key=obj_path
            )
            parent = obj.get_parent()
            if parent is not None:
                prx_item_parent = self._item_dict[parent.path]
                prx_item = prx_item_parent.add_child(
                    **create_kwargs
                )
            else:
                prx_item = self._prx_input.create_item(
                    **create_kwargs
                )
            # prx_item.set_checked(True)
            prx_item.update_keyword_filter_keys_tgt([obj_path, obj_type])
            obj.set_obj_gui(prx_item)
            prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
            self._item_dict[obj_path] = prx_item
            #
            if use_show_thread is True:
                prx_item.set_show_build_fnc(
                    lambda *args, **kwargs: self._item_show_fnc(prx_item)
                )
                return True, prx_item, None
            else:
                self._item_show_fnc(prx_item)
                return True, prx_item, None

    def _item_show_fnc(self, prx_item, use_as_tree=True):
        obj = prx_item.get_gui_dcc_obj(namespace=self.NAMESPACE)
        obj_type_name = obj.type_name
        obj_name = obj.name
        _obj_path = obj.path
        menu_raw = []
        menu_raw.extend(
            obj.get_gui_menu_raw() or []
        )
        menu_raw.extend(
            obj.get_gui_extend_menu_raw() or []
        )
        #
        if use_as_tree is True:
            menu_raw.extend(
                [
                    ('expanded',),
                    ('expand branch', 'expand', prx_item.set_expand_branch),
                    ('collapse branch', 'collapse', prx_item.set_collapse_branch),
                ]
            )
        #
        result = obj.get('result')
        update = obj.get('update')
        prx_item.set_icon_by_text(obj_type_name)
        prx_item.set_names([obj_name, update])
        prx_item.set_tool_tip(obj.description)
        if result:
            if bsc_storage.StgPathOpt(result).get_is_file():
                prx_item.set_icon_by_file(_gui_core.GuiIcon.get_by_file(result))
        #
        prx_item.set_gui_menu_data(menu_raw)
        prx_item.set_menu_content(obj.get_gui_menu_content())

    def _add_item_as_tree(self, obj):
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            for i_rsv_obj in ancestors:
                ancestor_path = i_rsv_obj.path
                if ancestor_path not in self._item_dict:
                    self.__set_item_comp_add_as_tree_(i_rsv_obj, use_show_thread=True)
        #
        self.__set_item_comp_add_as_tree_(obj, use_show_thread=True)

    def _add_item_as_list(self, obj):
        obj_path = obj.path
        obj_type = obj.type
        #
        create_kwargs = dict(
            name='...',
            filter_key=obj_path
        )
        prx_item = self._prx_input.create_item(
            **create_kwargs
        )
        # prx_item.set_checked(True)
        prx_item.update_keyword_filter_keys_tgt([obj_path, obj_type])
        obj.set_obj_gui(prx_item)
        prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
        self._item_dict[obj_path] = prx_item
        #
        prx_item.set_show_build_fnc(
            functools.partial(
                self._item_show_fnc, prx_item, False
            )
        )

    def _set_item_selected(self, obj):
        item = obj.get_obj_gui()
        self._prx_input.set_item_selected(
            item, exclusive=True
        )

    def __clear_items_(self):
        self._prx_input.do_clear()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (tuple, list)):
            self.__clear_items_()
            objs = raw
            if objs:
                with bsc_log.LogProcessContext.create(maximum=len(objs), label='gui-add for resolver object') as g_p:
                    for i in objs:
                        g_p.do_update()
                        #
                        self._add_item_as_list(i)
                    #
                    self._set_item_selected(
                        objs[-1]
                    )
        else:
            pass

    def get(self):
        _ = self._prx_input.get_current_item()
        if _:
            return _.get_gui_dcc_obj(namespace=self.NAMESPACE)

    def connect_input_changed_to(self, fnc):
        self._prx_input.connect_item_select_changed_to(
            fnc
        )


# project
class PrxInputForRsvProject(_input_base.AbsPrxInput):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = _qt_wgt_ipt_for_constant.QtInputForConstantChoose
    #
    HISTORY_KEY = 'gui.projects'

    def __init__(self, *args, **kwargs):
        super(PrxInputForRsvProject, self).__init__(*args, **kwargs)
        #
        self._qt_input_widget._set_entry_enable_(True)
        #
        self.update_history()
        #
        self._qt_input_widget._connect_input_user_entry_value_finished_to_(self.update_history)
        self._qt_input_widget.user_input_choose_changed.connect(self.update_history)

    def get(self):
        return self._qt_input_widget._get_value_()

    def set(self, raw=None, **kwargs):
        self._qt_input_widget._set_value_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_input_widget._set_value_default_(raw)

    def get_is_default(self):
        return self._qt_input_widget._get_value_is_default_()

    def connect_input_changed_to(self, fnc):
        self._qt_input_widget._connect_input_entry_value_changed_to_(fnc)

    #
    def update_history(self):
        project = self._qt_input_widget._get_value_()
        if project:
            import lxresolver.core as rsv_core

            resolver = rsv_core.RsvBase.generate_root()
            #
            rsv_project = resolver.get_rsv_project(project=project)
            project_directory_path = rsv_project.get_directory_path()
            work_directory_path = '{}/work'.format(project_directory_path)
            if bsc_storage.StgPathOpt(work_directory_path).get_is_exists() is True:
                _gui_core.GuiHistory.append(
                    self.HISTORY_KEY,
                    project
                )
        #
        histories = _gui_core.GuiHistory.get_all(
            self.HISTORY_KEY
        )
        if histories:
            histories = [i for i in histories if i]
            histories.reverse()
            #
            self._qt_input_widget._set_choose_values_(
                histories
            )

    def pull_history_latest(self):
        _ = _gui_core.GuiHistory.get_latest(self.HISTORY_KEY)
        if _:
            self._qt_input_widget._set_value_(_)

    def get_histories(self):
        return _gui_core.GuiHistory.get_all(
            self.HISTORY_KEY
        )
