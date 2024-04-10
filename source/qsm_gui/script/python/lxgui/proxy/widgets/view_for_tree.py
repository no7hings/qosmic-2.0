# coding:utf-8
import collections

import fnmatch

import six

import lxbasic.core as bsc_core
# gui
from ... import core as gui_core
# qt
from ...qt import core as gui_qt_core
# qt widgets
from ...qt.widgets import base as gui_qt_wgt_base

from ...qt.widgets import entry as gui_qt_wgt_entry

from ...qt.widgets import view_for_tree as gui_qt_wgt_view_for_tree
# proxy abstracts
from .. import abstracts as gui_prx_abstracts
# proxy widgets
from . import utility as gui_prx_wdt_utility

from . import item as gui_prx_wgt_item

from . import container as gui_prx_wgt_container


class PrxTreeView(
    gui_prx_abstracts.AbsPrxWidget,
    gui_prx_abstracts.AbsPrxViewDef,
    #
    gui_prx_abstracts.AbsPrxViewFilterTagDef,
    gui_prx_wgt_item.AbsPrxTreeDef,
    #
    gui_prx_abstracts.AbsPrxViewVisibleConnectionDef,
):
    QT_WIDGET_CLS = gui_qt_wgt_entry.QtEntryFrame
    QT_VIEW_CLS = gui_qt_wgt_view_for_tree.QtTreeWidget
    #
    FILTER_MAXIMUM = 50

    def __init__(self, *args, **kwargs):
        super(PrxTreeView, self).__init__(*args, **kwargs)
        self._qt_layout_0 = gui_qt_wgt_base.QtVBoxLayout(self._qt_widget)
        self._qt_layout_0.setContentsMargins(4, 4, 4, 4)
        self._qt_layout_0.setSpacing(2)
        #
        self._prx_top_tool_bar = gui_prx_wgt_container.PrxHToolBar()
        self._prx_top_tool_bar.set_name('top')
        self._prx_top_tool_bar.set_left_alignment()
        self._qt_layout_0.addWidget(self._prx_top_tool_bar.widget)
        self._prx_top_tool_bar.set_border_radius(1)
        self._prx_filer_bar_0 = gui_prx_wdt_utility.PrxFilterBar()
        self._prx_top_tool_bar.add_widget(self._prx_filer_bar_0)
        #
        self._loading_index = 0
        self._loading_show_index = 0
        # add custom menu
        self._qt_view = self.QT_VIEW_CLS()
        self._qt_view.setMinimumHeight(42)
        self._qt_view.setMaximumHeight(166667)
        self._qt_view.gui_proxy = self
        self._qt_layout_0.addWidget(self._qt_view)
        # self._qt_view.setFocusProxy(
        #     self._prx_filer_bar_0._qt_widget._entry_widget
        # )
        #
        self._set_prx_tree_def_init_()
        self._qt_view.ctrl_f_key_pressed.connect(
            self.set_filter_start
        )
        self._qt_view.f_key_pressed.connect(
            self.set_scroll_to_select_item
        )
        # self._prx_filer_bar_0.set_filter_connect_to(self)
        self._gui_menu_raw = []
        self._item_dict = collections.OrderedDict()
        self._cache_expand = dict()
        self._cache_check = dict()
        self._filter_completion_cache = None
        self._loading_item_prxes = []
        self._view_keyword_filter_occurrence_index_current = 0
        #
        self._prx_filter_bar = self._prx_filer_bar_0
        self._prx_filter_bar.set_completion_gain_fnc(
            self.__keyword_filter_completion_gain_fnc
        )
        self._keyword_filter_item_prxes = []

        self._qt_view._set_view_keyword_filter_bar_(self._prx_filter_bar._qt_widget)
        self._prx_filter_bar._qt_widget.input_value_changed.connect(
            self.__keyword_filter_cbk
        )
        self._prx_filter_bar._qt_widget.input_value_change_accepted.connect(
            self._qt_view._do_keyword_filter_occurrence_
        )
        #
        self._prx_filter_bar._qt_widget.occurrence_previous_press_clicked.connect(
            self._qt_view._do_keyword_filter_occurrence_to_previous_
        )
        self._prx_filter_bar._qt_widget.occurrence_next_press_clicked.connect(
            self._qt_view._do_keyword_filter_occurrence_to_next_
        )

    def __keyword_filter_cbk(self):
        self._qt_view._set_view_keyword_filter_data_src_(
            self._prx_filter_bar.get_keywords()
        )
        self._qt_view._refresh_view_items_visible_by_any_filter_()
        self._prx_filter_bar._qt_widget._set_occurrence_buttons_enable_(self._qt_view._has_keyword_filter_results_())
        self._qt_view._refresh_viewport_showable_auto_()

    def set_resize_enable(self, boolean):
        self._qt_widget._set_resize_enable_(boolean)

    def set_resize_minimum(self, value):
        self._qt_widget._set_resize_minimum_(value)

    def set_resize_target(self, widget):
        self._qt_widget._set_resize_target_(widget)

    @property
    def view(self):
        return self._qt_view

    @property
    def filter_bar(self):
        return self._prx_filter_bar

    def set_filter_entry_tip(self, text):
        self._prx_filter_bar.set_tip(text)

    def set_loading_item_add(self, item_prx):
        if item_prx not in self._loading_item_prxes:
            self._loading_item_prxes.append(item_prx)

    def set_loading_item_remove(self, item_prx):
        if item_prx in self._loading_item_prxes:
            self._loading_item_prxes.remove(item_prx)

    def set_loading_update(self):
        self._loading_index += 1
        if self._loading_index%15 == 0:
            self._loading_show_index += 1
            for i in self._loading_item_prxes:
                i.set_name(
                    'loading {}'.format('.'*(self._loading_show_index%5))
                )
            #
            gui_qt_core.QtWidgets.QApplication.instance().processEvents(
                gui_qt_core.QtCore.QEventLoop.ExcludeUserInputEvents
            )

    def set_filter_start(self):
        self._prx_top_tool_bar.set_expanded(True)
        self._prx_filer_bar_0.set_entry_focus(True)

    def get_top_tool_bar(self):
        return self._prx_top_tool_bar

    def set_scroll_to_select_item(self):
        selection_items = self.view.selectedItems()
        if selection_items:
            self.view._scroll_view_to_item_top_(selection_items[-1])

    def set_selection_use_single(self):
        self._qt_view.setSelectionMode(gui_qt_core.QtWidgets.QAbstractItemView.SingleSelection)

    def set_selection_disable(self):
        self._qt_view.setSelectionMode(gui_qt_core.QtWidgets.QAbstractItemView.NoSelection)

    def set_size_policy_height_fixed_mode(self):
        self._qt_view._set_size_policy_height_fixed_mode_()

    def set_gui_menu_raw(self, data):
        self._qt_view._set_menu_data_(data)

    def get_gui_menu_raw(self):
        return self._qt_view._get_menu_data_()

    def _get_all_items_(self):
        return self.view._get_all_items_()

    def get_all_items(self):
        return [i.gui_proxy for i in self.view._get_all_items_() if hasattr(i, 'gui_proxy')]

    def get_all_checked_items(self):
        return [i.gui_proxy for i in self.view._get_all_checked_items_() if hasattr(i, 'gui_proxy')]

    def get_all_leaf_items(self):
        return [i.gui_proxy for i in self.view._get_all_leaf_items_()]

    def get_item_prxes_by_keyword_filter(self, keyword, match_case=False, match_word=False):
        return [i.gui_proxy for i in self.view._get_items_by_keyword_filter_(
            keyword=keyword,
            match_case=match_case,
            match_word=match_word
        )]

    # select
    def _get_selected_items_(self):
        return self.view.selectedItems()

    def get_selected_items(self):
        return [i.gui_proxy for i in self._get_selected_items_()]

    def get_selected_item_widgets(self):
        return [self._qt_view._get_item_widget_(i).gui_proxy for i in self.view.selectedItems()]

    def get_current_item(self):
        _ = self._qt_view.currentItem()
        if _:
            return _.gui_proxy

    def set_item_selected(self, item_prx, exclusive=False):
        if exclusive is True:
            self.view.setCurrentItem(item_prx.widget)
        else:
            self.view.setItemSelected(item_prx.widget, True)

    def create_item(self, *args, **kwargs):
        return self._add_item_(
            self.view.addTopLevelItem,
            *args, **kwargs
        )

    def set_clear(self):
        self.view._set_clear_()
        self._item_dict.clear()
        self._filter_completion_cache = None
        self._loading_item_prxes = []

    def restore_all(self):
        self.set_clear()

    def connect_item_select_changed_to(self, fnc):
        self.view.itemSelectionChanged.connect(fnc)

    def connect_item_check_changed_to(self, fnc):
        self.view.item_check_changed.connect(fnc)

    def connect_choose_changed_to(self, fnc):
        self.view.itemChanged.connect(fnc)

    def connect_item_expand_to(self, prx_item, fnc, time=0):
        self.view._connect_item_expand_to_(prx_item.widget, fnc, time)

    def set_all_items_expand(self):
        self.view.expandAll()

    def expand_items_by_depth(self, depth):
        qt_items = self.view._get_items_by_depth_(depth)
        for qt_item in qt_items:
            qt_item.setExpanded(True)

    def set_all_items_collapse(self):
        self.view.collapseAll()

    def set_header_view_create(self, data, max_width=0):
        self.view._set_view_header_(data, max_width)

    def set_tag_filter_all_keys_src(self, keys):
        gui_prx_abstracts.AbsPrxViewFilterTagDef.set_tag_filter_all_keys_src(
            self, keys
        )

    @classmethod
    def _generate_item_tag_filter_tgt_args_(cls, prx_item_tgt, tag_filter_all_keys_src):
        tag_filter_tgt_keys = prx_item_tgt.get_tag_filter_tgt_keys()
        tag_filter_tgt_mode = prx_item_tgt.get_tag_filter_tgt_mode()
        if tag_filter_tgt_keys:
            if tag_filter_tgt_mode == gui_core.GuiTagFilterMode.MatchAll:
                for tag_filter_tgt_key in tag_filter_tgt_keys:
                    if tag_filter_tgt_key not in tag_filter_all_keys_src:
                        return True, True
                return True, False
            elif tag_filter_tgt_mode == gui_core.GuiTagFilterMode.MatchOne:
                for tag_filter_tgt_key in tag_filter_tgt_keys:
                    if tag_filter_tgt_key in tag_filter_all_keys_src:
                        return True, False
                return True, True
            return True, False
        return False, False

    @classmethod
    def _generate_item_keyword_filter_tgt_args_(cls, item_prx, texts):
        if texts:
            keyword = texts[0]
            keyword = keyword.lower()
            keyword_filter_keys_tgt = item_prx.get_keyword_filter_keys_tgt() or []
            if keyword_filter_keys_tgt:
                context = '+'.join([i.decode('utf-8') for i in keyword_filter_keys_tgt if i])
            else:
                context = '+'.join([i.decode('utf-8') for i in item_prx.get_names() if i])
            #
            context = context.lower()
            if '*' in keyword:
                filter_key = u'*{}*'.format(keyword.lstrip('*').rstrip('*'))
                if fnmatch.filter([context], filter_key):
                    return True, False
            else:
                filter_key = u'*{}*'.format(keyword)
                if fnmatch.filter([context], filter_key):
                    return True, False
            return True, True
        return False, False

    @classmethod
    def _get_item_name_colors_(cls, prx_items, column=0):
        lis = []
        for i_prx_item in prx_items:
            item = i_prx_item.widget
            lis.append(item.textColor(column))
        return lis

    def _set_filter_bar_(self, filter_bar):
        self._prx_filter_bar = filter_bar

    def get_item_by_key(self, filter_key):
        return self._item_dict.get(filter_key)

    def get_valid_item_keys(self):
        list_ = []
        for k, v in self._item_dict.items():
            if v.get_is_enable() is True:
                list_.append(k)
        return list_

    def get_item_keys(self):
        return self._item_dict.keys()

    def select_item_by_key(self, filter_key, exclusive=False):
        prx_item = self.get_item_by_key(filter_key)
        #
        if prx_item is not None:
            if prx_item.get_is_enable() is True:
                self.set_item_selected(prx_item, exclusive=exclusive)
                self.set_scroll_to_select_item()
                prx_item.set_select()
            #
            self.set_view_update()

    def set_view_update(self):
        self.view.update()

    def connect_refresh_action_for(self, fnc):
        self._qt_view.f5_key_pressed.connect(fnc)

    def set_filter_history_key(self, key):
        self._prx_filter_bar.set_history_key(key)

    def set_completion_gain_fnc(self, fnc):
        self._prx_filter_bar.set_completion_gain_fnc(fnc)

    # noinspection PyUnusedLocal
    def __keyword_filter_completion_gain_fnc(self, *args, **kwargs):
        keyword = args[0]
        if keyword:
            if self._filter_completion_cache is None:
                # cache fist
                self._filter_completion_cache = list(
                    set(
                        map(
                            lambda x: x.lower(),
                            [
                                j for i in self._qt_view._get_all_items_()
                                for j in i._generate_keyword_filter_keys_()
                            ]
                        )
                    )
                )
            #
            _ = fnmatch.filter(
                self._filter_completion_cache, six.u('*{}*').format(keyword)
            )
            return bsc_core.RawTextsMtd.sort_by_initial(_)[:self.FILTER_MAXIMUM]
        return []

    def restore_filter(self):
        self._prx_filter_bar.restore()

    def set_draw_for_check_state_enable(self, boolean):
        self._qt_view._set_draw_for_check_state_enable_(boolean)

    def gui_bustling(self):
        return self._qt_view._gui_bustling_()


class PrxFileView(PrxTreeView):
    def __init__(self, *args, **kwargs):
        super(PrxFileView, self).__init__(*args, **kwargs)
