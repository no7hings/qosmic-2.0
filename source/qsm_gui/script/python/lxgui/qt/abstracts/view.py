# coding:utf-8
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import core as gui_qt_core

from . import base as gui_qt_abs_base


class AbsQtTreeWidget(
    QtWidgets.QTreeWidget,
    #
    gui_qt_abs_base.AbsQtEmptyBaseDef,
    #
    gui_qt_abs_base.AbsQtMenuBaseDef,
    #
    gui_qt_abs_base.AbsQtViewFilterExtraDef,
    #
    gui_qt_abs_base.AbsQtViewStateDef,
    gui_qt_abs_base.AbsQtViewVisibleConnectionDef,
    #
    gui_qt_abs_base.AbsQtViewScrollActionDef,
    gui_qt_abs_base.AbsQtBuildViewDef,
    gui_qt_abs_base.AbsQtShowForViewDef,
    #
    gui_qt_abs_base.AbsQtBusyBaseDef,
):
    def __init__(self, *args, **kwargs):
        super(AbsQtTreeWidget, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #
        self._init_empty_base_def_(self)
        self._init_menu_base_def_(self)
        #
        self._init_view_filter_extra_def_(self)
        #
        self._set_view_state_def_init_()
        self._set_view_visible_connection_def_init_()

        self._set_view_scroll_action_def_init_()
        # noinspection PyUnresolvedReferences
        self._get_view_v_scroll_bar_().valueChanged.connect(
            self._refresh_viewport_showable_by_scroll_
        )
        #
        self._init_view_build_extra_def_()
        self._setup_view_build_(self)

        self._init_show_for_view_def_(self)
        #
        self._init_busy_base_def_(self)
        self.setFont(gui_qt_core.QtFonts.Default)
        #
        self.customContextMenuRequested.connect(
            self._popup_menu_cbk_
        )

    def _get_all_items_(self, column=0):
        def _rcs_fnc(index_):
            if index_ is None:
                row_count = model.rowCount()
            else:
                row_count = model.rowCount(index_)
                list_.append(self.itemFromIndex(index_))
            #
            for i_row in range(row_count):
                if index_ is None:
                    _index = model.index(i_row, column)
                else:
                    _index = index_.child(i_row, index_.column())
                #
                if _index.isValid():
                    _rcs_fnc(_index)

        list_ = []
        model = self.model()

        _rcs_fnc(None)
        return list_

    def _get_all_checked_items_(self, column=0):
        def _rcs_fnc(index_):
            if index_ is None:
                row_count = model.rowCount()
            else:
                row_count = model.rowCount(index_)
            #
            for i_row in range(row_count):
                if index_ is None:
                    _i_index = model.index(i_row, column)
                else:
                    _i_index = index_.child(i_row, index_.column())
                #
                if _i_index.isValid():
                    if _i_index.data(QtCore.Qt.CheckStateRole) == QtCore.Qt.Checked:
                        list_.append(self.itemFromIndex(_i_index))
                        _rcs_fnc(_i_index)

        list_ = []
        model = self.model()

        _rcs_fnc(None)
        return list_

    def _set_view_header_(self, raw, max_width=0):
        texts, width_ps = zip(*raw)
        count = len(texts)
        #
        self.setColumnCount(count)
        self.setHeaderLabels(texts)
        set_column_enable = count > 1
        w = 0
        if set_column_enable is True:
            max_division = sum(width_ps)
            w = int(max_width/max_division)
        #
        for index in range(0, count):
            if set_column_enable is True:
                self.setColumnWidth(index, w*(width_ps[index]))
            #
            icon = QtGui.QIcon()
            p = QtGui.QPixmap(16, 16)
            p.load(gui_core.GuiIcon.get('qt-style/line-v'))
            icon.addPixmap(
                p,
                QtGui.QIcon.Normal,
                QtGui.QIcon.On
            )
            #
            self.headerItem().setBackground(index, gui_qt_core.QtBrushes.Background)
            self.headerItem().setForeground(index, QtGui.QBrush(QtGui.QColor(255, 255, 255, 255)))
            self.headerItem().setFont(index, gui_qt_core.QtFonts.NameNormal)
            # todo: in katana will make text display error, PyQt?
            if QT_LOAD_INDEX == 1:
                self.headerItem().setIcon(index, icon)

    def _get_view_h_scroll_bar_(self):
        return self.horizontalScrollBar()

    def _get_view_v_scroll_bar_(self):
        return self.verticalScrollBar()

    def _set_selection_disable_(self):
        self.setSelectionMode(
            self.NoSelection
        )

    def _set_filter_style_(self):
        pass

    # noinspection PyUnusedLocal
    def _popup_menu_cbk_(self, *args):
        indices = self.selectedIndexes()
        if indices:
            index = indices[-1]
            item = self.itemFromIndex(index)
            menu_data = item._get_menu_data_()
            menu_content = item._get_menu_content_()
        else:
            menu_data = self._get_menu_data_()
            menu_content = self._get_menu_content_()
        #
        menu = None
        #
        if menu_content:
            if menu is None:
                menu = self.QT_MENU_CLS(self)
            #
            menu._set_menu_content_(menu_content)
            menu._popup_start_()
        #
        if menu_data:
            if menu is None:
                menu = self.QT_MENU_CLS(self)
            #
            menu._set_menu_data_(menu_data)
            menu._popup_start_()


class AbsQtListWidget(
    QtWidgets.QListWidget,
    #
    gui_qt_abs_base.AbsQtEmptyBaseDef,
    #
    gui_qt_abs_base.AbsQtViewSelectActionDef,
    gui_qt_abs_base.AbsQtViewScrollActionDef,
    #
    gui_qt_abs_base.AbsQtViewFilterExtraDef,
    gui_qt_abs_base.AbsQtViewStateDef,
    gui_qt_abs_base.AbsQtViewVisibleConnectionDef,
    gui_qt_abs_base.AbsQtBuildViewDef,
    gui_qt_abs_base.AbsQtShowForViewDef,
    gui_qt_abs_base.AbsQtBusyBaseDef,
):
    SortMode = gui_core.GuiSortMode
    SortOrder = gui_core.GuiSortOrder

    item_show_changed = qt_signal()
    press_released = qt_signal()
    pressed = qt_signal()

    def _refresh_widget_draw_(self):
        self.update()
        self.viewport().update()

    def __init__(self, *args, **kwargs):
        super(AbsQtListWidget, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.viewport().installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setResizeMode(self.Adjust)
        #
        self._init_empty_base_def_(self)
        self._set_view_select_action_def_init_()
        self._set_view_scroll_action_def_init_()
        #
        self._init_view_filter_extra_def_(self)
        #
        self._set_view_state_def_init_()
        self._set_view_visible_connection_def_init_()
        #
        self.itemSelectionChanged.connect(self._view_item_select_cbk)
        self.itemSelectionChanged.connect(self._view_item_widget_select_cbk)
        # noinspection PyUnresolvedReferences
        self._get_view_v_scroll_bar_().valueChanged.connect(
            self._refresh_viewport_showable_by_scroll_
        )
        # noinspection PyUnresolvedReferences
        # self._get_view_v_scroll_bar_().rangeChanged.connect(
        #     self._refresh_all_item_widgets_
        # )
        self._viewport_rect = QtCore.QRect()
        self._item_rects = []
        #
        self.setStyleSheet(
            gui_qt_core.GuiQtStyle.get('QListView')
        )
        #
        self.verticalScrollBar().setStyleSheet(
            gui_qt_core.GuiQtStyle.get('QScrollBar')
        )
        self.horizontalScrollBar().setStyleSheet(
            gui_qt_core.GuiQtStyle.get('QScrollBar')
        )
        #
        self._init_view_build_extra_def_()
        self._setup_view_build_(self)

        self._init_show_for_view_def_(self)
        self._init_busy_base_def_(self)

        self._sort_mode = self.SortMode.Number
        self._sort_order = self.SortOrder.Ascend

        self._grid_size = 128, 128

    def _set_selection_use_multiply_(self):
        self.setSelectionMode(self.ExtendedSelection)

    def _set_selection_use_single_(self):
        self.setSelectionMode(self.SingleSelection)

    def _get_is_multiply_selection_(self):
        return self.selectionMode() == self.ExtendedSelection

    def _clear_selection_(self):
        self.clearSelection()

    def _set_sort_enable_(self, boolean):
        self.setSortingEnabled(boolean)

    def _get_sort_mode_(self):
        return self._sort_mode

    def _get_sort_order_(self):
        return self._sort_order

    def _set_item_sort_mode_(self, mode):
        self._sort_mode = mode
        self._update_sort_mode_()

    def _update_sort_mode_(self):
        if self._sort_mode == self.SortMode.Number:
            items = [self.item(i) for i in range(self.count())]
            for i_item in items:
                i_item_widget = self.itemWidget(i_item)
                i_index = str(i_item_widget._sort_number_key).zfill(4)
                i_item.setText(i_index)
            #
            self._refresh_sort_()
        elif self._sort_mode == self.SortMode.Name:
            items = [self.item(i) for i in range(self.count())]
            for i_item in items:
                i_item_widget = self.itemWidget(i_item)
                i_name = str(i_item_widget._sort_name_key).lower()
                i_item.setText(i_name)
            #
            self._refresh_sort_()

    def _swap_item_sort_order_(self):
        if self._sort_order == self.SortOrder.Ascend:
            self._sort_order = self.SortOrder.Descend
        else:
            self._sort_order = self.SortOrder.Ascend
        self._refresh_sort_()

    def _refresh_sort_(self):
        self.sortItems(
            [QtCore.Qt.AscendingOrder, QtCore.Qt.DescendingOrder][self._sort_order]
        )
        self._refresh_viewport_showable_auto_()

    def _set_drag_enable_(self, boolean):
        super(AbsQtListWidget, self)._set_drag_enable_(boolean)
        # self.acceptDrops()
        # self.setDragEnabled(True)
        self.setDragDropMode(self.InternalMove)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)

    def _get_view_h_scroll_bar_(self):
        return self.horizontalScrollBar()

    def _get_view_v_scroll_bar_(self):
        return self.verticalScrollBar()

    def _set_view_item_selected_(self, item, boolean):
        self.setItemSelected(item, boolean)

    def _get_selected_items_(self):
        return self.selectedItems()

    def _set_item_widget_selected_(self, item, boolean):
        item_widget = self.itemWidget(item)
        if item_widget:
            item_widget._set_selected_(boolean)

    # select
    def _get_selected_item_widgets_(self):
        return [self.itemWidget(i) for i in self.selectedItems()]

    def _get_selected_item_widget_(self):
        item_widgets = self._get_selected_item_widgets_()
        if item_widgets:
            return item_widgets[-1]

    def _get_checked_item_widgets_(self):
        return [i for i in self._get_all_item_widgets_() if i._get_is_checked_() is True]

    def _view_item_select_cbk(self):
        pass

    def _view_item_widget_select_cbk(self):
        if self._pre_selected_items:
            [self._set_item_widget_selected_(i, False) for i in self._pre_selected_items]
        #
        selected_items = self._get_selected_items_()
        if selected_items:
            [self._set_item_widget_selected_(i, True) for i in selected_items]
            self._pre_selected_items = selected_items

    # scroll
    def _scroll_view_to_item_top_(self, item):
        self.scrollToItem(item, self.PositionAtTop)
        self.setCurrentItem(item)

    def _set_scroll_to_selected_item_top_(self):
        selected_items = self._get_selected_items_()
        if selected_items:
            item = selected_items[-1]
            self._scroll_view_to_item_top_(item)

    # show mode
    def _set_grid_mode_(self):
        self.setViewMode(self.IconMode)
        self._update_by_item_mode_change_()

    def _set_list_mode_(self):
        self.setViewMode(self.ListMode)
        self._update_by_item_mode_change_()

    def _set_grid_size_(self, w, h):
        self._grid_size = w, h
        self._update_by_grid_size_change_()
        self._update_by_item_mode_change_()

    def _get_grid_size_(self):
        return self._grid_size

    def _general_grid_size_(self):
        pass

    def _update_by_grid_size_change_(self):
        w, h = self._get_grid_size_()
        self.setGridSize(QtCore.QSize(w, h))
        [i.setSizeHint(QtCore.QSize(w, h)) for i in self._get_all_items_()]

    def _update_by_item_mode_change_(self):
        w, h = self._get_grid_size_()
        self.verticalScrollBar().setSingleStep(h)

    def _get_viewport_size_(self):
        return self.viewport().width(), self.viewport().height()

    def _get_all_items_(self):
        return [self.item(i) for i in range(self.count())]

    def _get_all_item_count_(self):
        return self.count()

    def _get_all_item_widgets_(self):
        return [self.itemWidget(self.item(i)) for i in range(self.count())]

    def _get_all_visible_items_(self):
        return [i for i in self._get_all_items_() if i.isHidden() is False]

    def _get_all_visible_item_count_(self):
        return len(self._get_all_visible_items_())

    def _get_all_visible_item_widgets_(self):
        return [self.itemWidget(i) for i in self._get_all_visible_items_()]

    def _get_selected_visible_items_(self):
        return [i for i in self.selectedItems() if i.isHidden() is False]

    def _get_selected_visible_indices_(self):
        return [self.indexFromItem(i) for i in self._get_selected_visible_items_()]

    def _set_all_items_selected_(self, boolean):
        for i in range(self.count()):
            i_item = self.item(i)
            i_item.setSelected(boolean)
            self.itemWidget(i_item)._set_selected_(boolean)

    def _get_visible_indices_(self):
        return [self.indexFromItem(i) for i in self._get_all_visible_items_() if i.isHidden() is False]

    @staticmethod
    def _set_loading_update_():
        QtWidgets.QApplication.instance().processEvents(
            QtCore.QEventLoop.ExcludeUserInputEvents
        )

    def _set_clear_(self):
        for i in self._get_all_items_():
            i._kill_item_all_show_runnables_()
            i._stop_item_show_all_()
        #
        self._pre_selected_items = []
        #
        self.clear()

    def _scroll_to_pre_item_(self):
        # use visible indices for filter by visible
        indices = self._get_visible_indices_()
        if indices:
            selected_indices = self._get_selected_visible_indices_()
            if selected_indices:
                index_values = [i.row() for i in indices]
                selected_index_values = [i.row() for i in selected_indices]
                #
                idx = index_values.index(selected_index_values[0])
                idx_max, idx_min = len(indices)-1, 0
                #
                idx = max(min(idx, idx_max), 0)
                #
                if idx == idx_min:
                    idx = idx_max
                else:
                    idx -= 1
                #
                idx_pre = max(min(idx, idx_max), 0)
                index_pre = indices[idx_pre]
                item_pre = self.itemFromIndex(index_pre)
                item_pre.setSelected(True)
                self._scroll_view_to_item_top_(item_pre)
            else:
                item = self.itemFromIndex(indices[0])
                item.setSelected(True)
                self._scroll_view_to_item_top_(item)
                return

    def _scroll_to_next_item_(self):
        indices = self._get_visible_indices_()
        if indices:
            selected_indices = self._get_selected_visible_indices_()
            if selected_indices:
                index_values = [i.row() for i in indices]
                selected_index_values = [i.row() for i in selected_indices]
                #
                idx = index_values.index(selected_index_values[0])
                idx_max, idx_min = len(indices)-1, 0
                #
                idx = max(min(idx, idx_max), 0)
                if idx == idx_max:
                    idx = idx_min
                else:
                    idx += 1
                idx_next = max(min(idx, idx_max), 0)
                index_next = indices[idx_next]
                item_next = self.itemFromIndex(index_next)
                item_next.setSelected(True)
                self._scroll_view_to_item_top_(item_next)
            else:
                item = self.itemFromIndex(indices[0])
                item.setSelected(True)
                self._scroll_view_to_item_top_(item)
                return

    def _delete_item_widget_(self, item):
        item_widget = self.itemWidget(item)
        if item_widget:
            item_widget.close()
            item_widget.deleteLater()

    def _set_item_delete_(self, item):
        pass

    def _set_focused_(self, boolean):
        if boolean is True:
            self.setFocus(
                QtCore.Qt.MouseFocusReason
            )
        else:
            self.setFocus(
                QtCore.Qt.NoFocusReason
            )

    def _get_item_current_(self):
        return self.currentItem()

    def _refresh_all_item_widgets_(self):
        for i in self._get_all_item_widgets_():
            if i is not None:
                i._refresh_widget_all_()

    def _set_scroll_enable_(self, boolean):
        super(AbsQtListWidget, self)._set_scroll_enable_(boolean)
        if boolean is False:
            self.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff
            )
            self.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff
            )
            # self.setResizeMode(self.Fixed)
        else:
            self.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAsNeeded
            )
            self.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAsNeeded
            )

    def _set_current_item_(self, item):
        self.setCurrentItem(item)

    def _get_item_widget_(self, item):
        return self.itemWidget(item)
