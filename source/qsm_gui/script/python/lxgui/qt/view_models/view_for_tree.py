# coding:utf-8
import collections

import functools

import lxbasic.core as bsc_core

from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from . import base as _base

from . import view_base as _view_base


class TreeViewModel(_view_base.AbsViewModel):
    ItemSortOrder = _gui_core.GuiItemSortOrder

    def do_close(self):
        pass

    def do_drop(self, event):
        data = event.mimeData()
        print data

    def refresh_info(self):
        c = len(self.get_checked_leaf_items())
        if c:
            info = '{} leaf item is checked ...'.format(c)
        else:
            info = ''

        if info != self._data.info:
            self._widget.info_text_accepted.emit(info)
            self._data.info = info

    def _update_item_drop_enable(self):
        self._widget.setAcceptDrops(self._data.item_drop_enable)
        self._widget.setDropIndicatorShown(False)

    def do_item_popup_tool_tip(self, event):
        item = self._widget.itemAt(event.pos())
        if item is None:
            return

        css = item._item_model.data.tool_tip.css
        if css:
            rect = self._widget.visualItemRect(item)
            p = rect.bottomLeft()
            p = self._widget.mapToGlobal(p)+QtCore.QPoint(0, -15)
            # noinspection PyArgumentList
            QtWidgets.QToolTip.showText(
                p, css, self._widget
            )

    def do_item_press_click(self, event):
        item = self._widget.itemAt(event.pos())
        if item is None:
            return

        item._item_model.do_press_click(event.pos())

    def do_item_press_dbl_click(self, event):
        item = self._widget.itemAt(event.pos())
        if item is None:
            return

        item._item_model.do_press_dbl_click(event.pos())

    def do_item_hover_move(self, event):
        item = self._widget.itemAt(event.pos())
        if item is None:
            return

        item._item_model.do_hover_move(event.pos())

    def on_item_expand_at(self, index):
        def fnc_():
            method()
            timer.stop()

        if _qt_core.QtApplication.is_shift_modifier():
            self.set_item_extend_expanded_at(index, True)

        item = self._widget.itemFromIndex(index)

        path = item._item_model.get_path()
        if path in self._data.expand_method_dict:
            method, time = self._data.expand_method_dict[path]
            if time == 0:
                method()
            else:
                timer = QtCore.QTimer(self)
                timer.timeout.connect(fnc_)
                timer.start(time)

    def on_item_collapse_at(self, index):
        if _qt_core.QtApplication.is_shift_modifier():
            self.set_item_extend_expanded_at(index, False)

    def set_item_extend_expanded_at(self, index, boolean):
        for i in range(0, index.model().rowCount(index)):
            i_child_index = index.child(i, 0)
            # ignore non children item
            if i_child_index.model().rowCount(i_child_index):
                self._widget.setExpanded(i_child_index, boolean)
                self.set_item_extend_expanded_at(i_child_index, boolean)

    def __init__(self, widget):
        super(TreeViewModel, self).__init__(
            widget,
            _base._Data(
                item=_base._Data(
                    cls=None,
                    grid_size=QtCore.QSize(128, 20),
                ),
                expand_method_dict=dict(),
            )
        )

        if not isinstance(widget, QtWidgets.QTreeWidget):
            raise RuntimeError()

        self._widget = widget

        self._widget.item_check_changed.connect(self._on_item_check_changed)

    def get_all_items(self, column=0):
        def rcs_fnc_(index_):
            # top level
            if index_ is None:
                _row_count = model.rowCount()
            else:
                _row_count = model.rowCount(index_)
                list_.append(self._widget.itemFromIndex(index_))
            #
            for _i_row in range(_row_count):
                # top level
                if index_ is None:
                    _index = model.index(_i_row, column)
                else:
                    _index = index_.child(_i_row, index_.column())

                if _index.isValid():
                    rcs_fnc_(_index)

        list_ = []
        model = self._widget.model()

        rcs_fnc_(None)
        return list_

    def get_visible_items(self, column=0):
        def rcs_fnc_(index_):
            # top level
            if index_ is None:
                _row_count = model.rowCount()
            else:
                _row_count = model.rowCount(index_)
                _item = self._widget.itemFromIndex(index_)
                if _item.isHidden():
                    return
                else:
                    list_.append(_item)

            for _i_row in range(_row_count):
                # top level
                if index_ is None:
                    _index = model.index(_i_row, column)
                else:
                    _index = index_.child(_i_row, index_.column())

                if _index.isValid():
                    rcs_fnc_(_index)

        list_ = []
        model = self._widget.model()

        rcs_fnc_(None)
        return list_

    def scroll_to_item_top(self, item):
        self._widget.scrollToItem(item, self._widget.PositionAtTop)
        self._widget.setCurrentItem(item)

    def occurrence_item_previous(self):
        items = self.get_visible_items()
        maximum = len(items)-1
        if items:
            idx_max, idx_min = maximum, 0
            if self._data.occurrence.index is None:
                self._data.occurrence.index = idx_max
                self.scroll_to_item_top(items[idx_max])
            else:
                idx = self._data.occurrence.index
                idx = max(min(idx, idx_max), 0)
                if idx == idx_min:
                    idx = idx_max
                else:
                    idx -= 1
                idx_pre = max(min(idx, idx_max), 0)
                item_pre = items[idx_pre]
                self.scroll_to_item_top(item_pre)
                self._data.occurrence.index = idx_pre
        else:
            self._data.occurrence.index = None

        return maximum, self._data.occurrence.index

    def occurrence_item_next(self):
        items = self.get_visible_items()
        maximum = len(items)-1
        if items:
            idx_max, idx_min = maximum, 0
            if self._data.occurrence.index is None:
                self._data.occurrence.index = idx_min
                self.scroll_to_item_top(items[idx_min])
            else:
                idx = self._data.occurrence.index

                idx = max(min(idx, idx_max), 0)

                if idx == idx_max:
                    idx = idx_min
                else:
                    idx += 1
                idx_nxt = max(min(idx, idx_max), 0)
                item_nxt = items[idx_nxt]
                self.scroll_to_item_top(item_nxt)
                self._data.occurrence.index = idx_nxt
        else:
            self._data.occurrence.index = None
        return maximum, self._data.occurrence.index

    @property
    def data(self):
        return self._data

    def create_root(self):
        _ = self.create_item('/')
        if _[0] is True:
            _[1].setExpanded(True)
        return _

    def create_item(self, path, *args, **kwargs):
        if path in self._data.item_dict:
            return False, self._data.item_dict[path]

        path_opt = bsc_core.BscNodePathOpt(path)
        index_cur = len(self._data.item_dict)
        item = self._data.item.cls()
        if path_opt.get_is_root():
            self._widget.addTopLevelItem(item)
        else:
            parent_path = path_opt.get_parent_path()
            if parent_path not in self._data.item_dict:
                raise RuntimeError()
            parent_item = self._data.item_dict[parent_path]
            if isinstance(parent_item, QtWidgets.QTreeWidgetItem) is False:
                raise RuntimeError()
            parent_item.addChild(item)

        name = path_opt.get_name()
        item.setText(0, str(index_cur).zfill(4))

        item_model = item._item_model
        item_model.set_path(path)
        item_model.set_index(index_cur)
        item_model.set_name(name)
        if self.is_item_check_enable() is True:
            item_model.set_check_enable(True)
        if self.is_item_color_enable() is True:
            item_model.set_color_rgb(bsc_core.BscTextOpt(name).to_hash_rgb(s_p=(35, 50), v_p=(75, 95)))
        item.setSizeHint(0, self.data.item.grid_size)

        self._data.item_dict[path] = item
        return True, item

    def draw_item(self, painter, option, index):
        self._widget.itemFromIndex(index)._item_model.draw(painter, option, index)
    
    def _sort_items(self, qt_order):
        self._widget.sortItems(0, qt_order)

    def generate_chart_data(self):
        paths = self._data.item_dict.keys()
        leaf_paths = bsc_core.BscNodePath.to_leaf_paths(paths)

        dict_ = {}
        for i_path in leaf_paths:
            i_item = self._get_item(i_path)
            i_item_model = i_item._item_model
            i_parent = i_item_model.get_parent()
            i_key = i_item_model.get_name()
            i_group_key = i_parent._item_model.get_name()
            i_value = i_item_model.get_number()
            if i_value:
                dict_.setdefault(i_group_key, {})[i_key] = i_value

        return dict_

    def generate_item_sort_menu_data(self):
        menu_data = []
        keys = self.get_item_sort_keys()
        order = ['ascend', 'descend'][self.get_item_sort_order()]
        icon_name = 'tool/sort-by-name-{}'.format(order)
        for i_key in keys+['index', 'number']:
            if i_key != self.get_item_sort_key_current():
                menu_data.append(
                    (i_key, icon_name, functools.partial(self.sort_item_by, i_key))
                )
        return menu_data

    def set_head_data(self, raw, max_width=0):
        self._widget.setHeaderHidden(False)

        texts, width_ps = zip(*raw)
        count = len(texts)

        self._widget.setColumnCount(count)
        self._widget.setHeaderLabels(texts)
        set_column_enable = count > 1
        w = 0
        if set_column_enable is True:
            max_division = sum(width_ps)
            w = int(max_width/max_division)

        for i_idx in range(0, count):
            if set_column_enable is True:
                self._widget.setColumnWidth(i_idx, w*(width_ps[i_idx]))

            icon = QtGui.QIcon()
            p = QtGui.QPixmap(16, 16)
            p.load(_gui_core.GuiIcon.get('qt-style/line-v'))
            icon.addPixmap(
                p,
                QtGui.QIcon.Normal,
                QtGui.QIcon.On
            )
            #
            self._widget.headerItem().setBackground(i_idx, _qt_core.QtRgba.Background)
            self._widget.headerItem().setForeground(i_idx, _qt_core.QtRgba.Text)
            self._widget.headerItem().setFont(i_idx, _qt_core.QtFonts.NameNormal)
            # todo: in katana will make text display error, PyQt?
            # if QT_LOAD_INDEX == 1:
            self._widget.headerItem().setIcon(i_idx, icon)
