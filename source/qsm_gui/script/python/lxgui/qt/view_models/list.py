# coding:utf-8
# qt
import collections
import functools

from ... import core as _gui_core

from ...qt.core.wrap import *

from ...qt import core as _qt_core

from . import base as _base


class ViewModelForList(object):
    SortOrder = _gui_core.GuiSortOrder

    def do_close(self):
        pass

    def do_item_tool_tip(self, event):
        item = self._widget.itemAt(event.pos())
        if item is None:
            return

        css = item._item_model.data.tool_tip_css
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

    @qt_slot()
    def _on_item_check_changed(self):
        self.refresh_info()

    def refresh_info(self):
        c = len(self.get_checked_items())
        if c:
            info = '{} item is checked ...'.format(c)
        else:
            info = ''

        if info != self._data.info:
            self._widget.info_text_accepted.emit(info)
            self._data.info = info

    def update_all_items_size_hint(self):
        [self._widget.item(x).setSizeHint(self._widget.gridSize()) for x in range(self._widget.count())]

    def set_item_frame_size(self, frm_w, frm_h):
        self._data.item.frame_width, self._data.item.frame_height = frm_w, frm_h
        grid_w, grid_h = frm_w, frm_h+self._data.item.name_height
        self._data.item.grid_size.setWidth(grid_w)
        self._data.item.grid_size.setHeight(grid_h)
        self._widget.setGridSize(self._data.item.grid_size)
        self.update_all_items_size_hint()

    def set_all_items_checked(self, boolean):
        [self._widget.item(x)._item_model._set_checked(boolean) for x in range(self._widget.count())]
        self._widget.item_check_changed.emit()

    def set_visible_items_checked(self, boolean):
        for i in range(self._widget.count()):
            i_item = self._widget.item(i)
            if i_item._item_model.is_visible():
                i_item._item_model._set_checked(boolean)
        # sent emit for check
        self._widget.item_check_changed.emit()

    def get_all_items(self):
        return [self._widget.item(x) for x in range(self._widget.count())]

    def get_checked_items(self):
        list_ = []
        for i in range(self._widget.count()):
            i_item = self._widget.item(i)
            if i_item._item_model.is_checked():
                list_.append(i_item)
        return list_

    def get_selected_items(self):
        return self._widget.selectedItems()

    def get_visible_items(self):
        list_ = []
        for i in range(self._widget.count()):
            i_item = self._widget.item(i)
            if i_item.isHidden() is False:
                list_.append(i_item)
        return list_
    
    def get_all_items_keyword_filter_keys(self):
        key_set = set()
        for i in range(self._widget.count()):
            i_key_set = self._widget.item(i)._item_model.get_keyword_filter_key_set()
            key_set.update(i_key_set)
        return list(key_set)

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
        if not isinstance(widget, QtWidgets.QListWidget):
            raise RuntimeError()

        self._widget = widget

        self._data = _base._Data(
            item=_base._Data(
                cls=None,
                frame_size=QtCore.QSize(128, 128),
                frame_width=128, frame_width_maximum=512, frame_width_minimum=16,
                frame_height=128,
                name_height=20,
                grid_size=QtCore.QSize(128, 128+20),
            ),

            info='',

            keyword_filter=_base._Data(
                key_src_set=set()
            ),
            occurrence=_base._Data(
                index=None
            ),

            item_dict=collections.OrderedDict(),

            menu=_base._Data(
                content=None,
                data=None,
                data_generate_fnc=None
            ),

            sort=_base._Data(
                keys=[],
                key_current='index',
                order=0,
            ),

            image_cache_dict=dict(),
            image_sequence_cache_dict=dict()
        )

        self._widget.item_check_changed.connect(self._on_item_check_changed)

    @property
    def data(self):
        return self._data

    def restore(self):
        for i_item in self.get_all_items():
            i_item._item_model.do_close()

        self._widget.clear()
        self._data.item_dict.clear()

        self.refresh_info()

    def _register_item(self, path, item):
        self._data.item_dict[path] = item

    def _check_item_exists(self, path):
        return self._data.item_dict.get(path) is not None

    def _get_item(self, path):
        return self._data.item_dict.get(path)

    def draw_item(self, painter, option, index):
        item = self._widget.itemFromIndex(index)
        rect = self._widget.visualItemRect(item)
        item._item_model.draw(painter, option, rect)

    def create_item(self, *args, **kwargs):
        index_cur = self._widget.count()
        item = self._data.item.cls(str(index_cur).zfill(4), self._widget)
        self._widget.addItem(item)
        # fixme: remove this?
        # if index_cur > 0:
        #     item.setHidden(True)
        #     item.setHidden(False)
        item._item_model.set_index(index_cur)
        item.setSizeHint(self.data.item.grid_size)
        return item

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

    def generate_sort_menu_data(self):
        menu_data = []
        keys = self._data.sort.keys
        order = ['ascend', 'descend'][self.get_sort_order()]
        icon_name = 'tool/sort-by-name-{}'.format(order)
        for i_key in keys+['index']:
            if i_key != self._data.sort.key_current:
                menu_data.append(
                    (i_key, icon_name, functools.partial(self.sort_by, i_key))
                )
        return menu_data

    def sort_by(self, key):
        self._data.sort.key_current = key
        [x._item_model.update_sort(key) for x in self.get_all_items()]
        self._update_sort()

    def set_sort_keys(self, keys):
        self._data.sort.keys = keys
        self._widget.setSortingEnabled(True)

    def set_sort_order(self, order):
        self._data.sort.order = order
        self._update_sort()

    def _update_sort(self):
        self._widget.sortItems(
            [QtCore.Qt.AscendingOrder, QtCore.Qt.DescendingOrder][self.get_sort_order()]
        )

    def get_sort_order(self):
        return self._data.sort.order

    def swap_sort_order(self):
        if self._data.sort.order == self.SortOrder.Ascend:
            self.set_sort_order(self.SortOrder.Descend)
        else:
            self.set_sort_order(self.SortOrder.Ascend)

    def mark_all_item_refresh_flag(self):
        for i_item in self.get_all_items():
            i_item._item_model.mark_refresh_force_flag(True)

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