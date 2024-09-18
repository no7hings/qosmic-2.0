# coding:utf-8
import collections

import functools

import lxbasic.core as bsc_core

from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from . import base as _base


class ListViewModel(_base.AbsViewModel):

    def do_close(self):
        pass

    def do_item_tool_tip(self, event):
        item = self._widget.itemAt(event.pos())
        if item is None:
            return

        css = item._item_model.data.tool_tip.css
        if css:
            rect = self._widget.rect()
            p = rect.topRight()
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

    def on_wheel(self, event):
        if _qt_core.QtUtil.is_ctrl_modifier():
            delta = event.angleDelta().y()

            step = 4
            frm_w_pre, frm_h_pre = self._data.item.frame_width, self._data.item.frame_height
            if delta > 0:
                frm_w = frm_w_pre+step
            else:
                frm_w = frm_w_pre-step

            frm_w = max(min(frm_w, self._data.item.frame_width_maximum), self._data.item.frame_width_minimum)
            if frm_w != frm_w_pre:
                frm_h = int(float(frm_h_pre)/float(frm_w_pre)*frm_w)
                self.set_item_frame_size(frm_w, frm_h)

    def update_all_items_size_hint(self):
        [self._widget.item(x).setSizeHint(self._widget.gridSize()) for x in range(self._widget.count())]

    def set_item_frame_size(self, frm_w, frm_h):
        self._data.item.frame_width, self._data.item.frame_height = frm_w, frm_h
        grid_w, grid_h = frm_w, frm_h+self._data.item.name_height
        self._data.item.grid_size.setWidth(grid_w)
        self._data.item.grid_size.setHeight(grid_h)
        self._widget.setGridSize(self._data.item.grid_size)
        self.update_all_items_size_hint()

    def get_all_items(self):
        return [self._widget.item(x) for x in range(self._widget.count())]

    def get_visible_items(self):
        list_ = []
        for i in range(self._widget.count()):
            i_item = self._widget.item(i)
            if i_item.isHidden() is False:
                list_.append(i_item)
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

    def __init__(self, widget):
        super(ListViewModel, self).__init__(
            widget,
            _base._Data(
                item=_base._Data(
                    cls=None,
                    frame_size=QtCore.QSize(128, 128),
                    frame_width=128, frame_width_maximum=512, frame_width_minimum=16,
                    frame_height=128,
                    name_height=20,
                    grid_size=QtCore.QSize(128, 128+20),
                ),

                info='',

                image_cache_dict=dict(),
                image_sequence_cache_dict=dict()
            )

        )

        if not isinstance(self._widget, QtWidgets.QListWidget):
            raise RuntimeError()

        self._widget.item_check_changed.connect(self._on_item_check_changed)

    @property
    def data(self):
        return self._data

    def _register_item(self, path, item):
        self._data.item_dict[path] = item

    def _check_item_exists(self, path):
        return self._data.item_dict.get(path) is not None

    def _get_item(self, path):
        return self._data.item_dict.get(path)

    def draw_item(self, painter, option, index):
        self._widget.itemFromIndex(index)._item_model.draw(painter, option, index)

    def create_item(self, path, *args, **kwargs):
        if path in self._data.item_dict:
            return False, self._data.item_dict[path]

        path_opt = bsc_core.BscPathOpt(path)
        name = path_opt.get_name()

        index_cur = len(self._data.item_dict)
        item = self._data.item.cls(name, self._widget)
        self._widget.addItem(item)

        item._item_model.set_path(path)
        item._item_model.set_name(name)
        item._item_model.set_index(index_cur)
        if self.get_item_check_enable() is True:
            item._item_model.set_check_enable(True)
        item.setSizeHint(self.data.item.grid_size)
        self._data.item_dict[path] = item
        return True, item

    def mark_all_item_refresh_flag(self):
        for i_item in self.get_all_items():
            i_item._item_model.mark_force_refresh(True)

    def check_item_showable(self, item):
        item_rect = self._widget.visualItemRect(item)
        i_w, i_h = item_rect.width(), item_rect.height()
        # check is visible
        if i_w != 0 and i_h != 0:
            view_rect = self._widget.rect()
            v_t, v_b = view_rect.top(), view_rect.bottom()
            i_t, i_b = item_rect.top(), item_rect.bottom()
            if v_b >= i_t and i_b >= v_t:
                return True
        return False

    def pull_image_cache(self, key):
        return self._data.image_cache_dict.get(key)

    def push_image_cache(self, key, data):
        self._data.image_cache_dict[key] = data

    def pull_image_sequence_cache(self, key):
        return self._data.image_sequence_cache_dict.get(key)

    def push_image_sequence_cache(self, key, data):
        self._data.image_sequence_cache_dict[key] = data
        
    def _sort_items(self, qt_order):
        self._widget.sortItems(qt_order)
