# coding:utf-8
import functools

import lxbasic.core as bsc_core

from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from . import base as _base

from . import view_base as _view_base


class ListViewModel(_view_base.AbsViewModel):

    def do_close(self):
        self._close_flag = True
        self._widget._do_kill_all_thread_worker_()
        # for i in self.get_all_items():
        #     i._item_model.do_close()

    def do_item_popup_tool_tip(self, event):
        item = self._widget.itemAt(event.pos())
        if item is None:
            return

        # tool tip
        if item.GROUP_FLAG is False:
            item_model_data = item._item_model._data
            if item_model_data.play_enable is True:
                if item_model_data.play.flag is True:
                    return

            css = item_model_data.tool_tip.css
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

        # hover play
        if item.GROUP_FLAG is False:
            item_model_data = item._item_model._data
            if item_model_data.play_enable is True:
                if item_model_data.play.flag is True:
                    # noinspection PyArgumentList
                    QtWidgets.QToolTip.hideText()

            item._item_model.do_hover_move(event.pos())

    def on_wheel(self, event):
        if _qt_core.QtUtil.is_ctrl_modifier():
            delta = event.angleDelta().y()

            step = 4
            frm_w_pre, frm_h_pre = self._data.item.frame_width, self._data.item.frame_height
            if delta > 0:
                frm_h = frm_h_pre+step
            else:
                frm_h = frm_h_pre-step
            # width match to height
            frm_h = max(min(frm_h, self._data.item.frame_height_maximum), self._data.item.frame_height_minimum)
            if frm_h != frm_h_pre:
                frm_w = int(float(frm_w_pre)/float(frm_h_pre)*frm_h)
                self.set_item_frame_size(frm_w, frm_h)

    def update_all_items_size_hint(self):
        for i in range(self._widget.count()):
            i_item = self._widget.item(i)
            i_item.setSizeHint(self._data.item.grid_size)
            i_item._item_model._data.text.height = self._data.item.text_height

    def set_item_frame_size(self, frm_w, frm_h):
        self._data.item.frame_width, self._data.item.frame_height = frm_w, frm_h

        # grid h add name height
        txt_h = 0
        if self.is_item_name_enable() is True:
            txt_h += _gui_core.GuiSize.ItemHeightDefault
        if self.is_item_mtime_enable() is True:
            txt_h += _gui_core.GuiSize.ItemHeightDefault
        if self.is_item_user_enable() is True:
            txt_h += _gui_core.GuiSize.ItemHeightDefault

        self._data.item.text_height = txt_h

        grid_w, grid_h = frm_w, frm_h+txt_h

        self._data.item.grid_size.setWidth(grid_w)
        self._data.item.grid_size.setHeight(grid_h)
        # set grid size to -1 for disable grid size and update item
        self._widget.setGridSize(QtCore.QSize(-1, -1))
        self.update_all_items_size_hint()

    def get_all_items(self):
        return [self._widget.item(x) for x in range(self._widget.count())]

    def get_all_group_items(self):
        return [x for x in self.get_all_items() if x.GROUP_FLAG is True]

    def remove_all_group_items(self):
        [self._remove_item_fnc(x) for x in self.get_all_group_items()]

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
                # about item
                item=_base._Data(
                    cls=None,
                    group_cls=None,
                    # frame
                    frame_width=128, frame_height=128,
                    frame_width_maximum=512, frame_height_maximum=512,
                    frame_width_minimum=24, frame_height_minimum=24,
                    text_height=0,
                    grid_size=QtCore.QSize(128, 128),
                    #
                    mode=0,
                ),
                item_group_enable=False,
                item_group=None,
                info='',
                # media cache
                image_cache_dict=bsc_core.LRUCache(maximum=1024),
                image_sequence_cache_dict=bsc_core.LRUCache(maximum=4096),
                video_cache_dict=bsc_core.LRUCache(maximum=1024),
                audio_cache_dict=bsc_core.LRUCache(maximum=1024),
            )

        )

        assert isinstance(widget, QtWidgets.QListWidget)
        
        self._widget = widget

        self._widget.item_check_changed.connect(self._on_item_check_changed)

    @property
    def data(self):
        return self._data

    # item mode
    def set_item_mode(self, mode):
        self._data.item.mode = mode
        self._update_item_mode()
    
    def _update_item_mode(self):
        if self._data.item.mode == self.ItemMode.Icon:
            self._widget.setViewMode(self._widget.IconMode)
        else:
            self._widget.setViewMode(self._widget.ListMode)
        # fixme: when mode is change, must update drag flag
        self._update_item_drag_enable()

    def swap_item_mode(self):
        if self._data.item.mode == self.ItemMode.Icon:
            self.set_item_mode(self.ItemMode.List)
        else:
            self.set_item_mode(self.ItemMode.Icon)

    def get_item_mode(self):
        return self._data.item.mode

    def draw_item(self, painter, option, index):
        self._widget.itemFromIndex(index)._item_model.draw(painter, option, index)

    def create_group_item(self, name, *args, **kwargs):
        item = self._data.item.group_cls('', self._widget)
        item_model = item._item_model
        item_model.set_name(name)
        group_text = u'{}:'.format(
            bsc_core.ensure_unicode(name)
        )
        item_model._update_name(group_text)
        sort_order = kwargs.get('sort_order')
        if sort_order is not None:
            item_model.apply_sort_order(sort_order)
        self._widget.addItem(item)

    def create_item(self, path, *args, **kwargs):
        if path in self._data.item_dict:
            return False, self._data.item_dict[path]

        path_opt = bsc_core.BscNodePathOpt(path)
        name = path_opt.get_name()

        index_cur = len(self._data.item_dict)
        item = self._data.item.cls('', self._widget)
        self._widget.addItem(item)

        item_model = item._item_model

        item_model.set_path(path)
        item_model.set_name(name)
        item_model.set_index(index_cur)
        if self.is_item_sort_enable() is True:
            item_model.set_sort_enable(True)
        if self.is_item_group_enable() is True:
            item_model.set_group_enable(True)
        # item mtime
        if self.is_item_mtime_enable() is True:
            item_model.set_mtime_enable(True)
        # item user
        if self.is_item_user_enable() is True:
            item_model.set_user_enable(True)
        # lock and check
        if self.is_item_lock_enable() is True:
            item_model.set_lock_enable(True)
        if self.is_item_check_enable() is True:
            item_model.set_check_enable(True)

        item.setSizeHint(self.data.item.grid_size)
        item_model._data.text.height = self._data.item.text_height
        self._data.item_dict[path] = item
        return True, item

    def _remove_item_fnc(self, item):
        item._item_model.do_close()
        self._widget.takeItem(self._widget.row(item))

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

    # media cache
    def pull_image_cache(self, key):
        return self._data.image_cache_dict.get(key)

    def push_image_cache(self, key, data):
        self._data.image_cache_dict[key] = data

    def pull_image_sequence_cache(self, key):
        return self._data.image_sequence_cache_dict.get(key)

    def push_image_sequence_cache(self, key, data):
        self._data.image_sequence_cache_dict[key] = data

    def pull_video_cache(self, key):
        return self._data.video_cache_dict.get(key)

    def push_video_cache(self, key, data):
        self._data.video_cache_dict[key] = data

    def pull_audio_cache(self, key):
        return self._data.audio_cache_dict.get(key)

    def push_audio_cache(self, key, data):
        self._data.audio_cache_dict[key] = data

    # item sort
    def _sort_items_fnc(self, qt_order):
        self._widget.sortItems(qt_order)

    def apply_item_sort_order(self, order):
        if self._data.item_sort_enable is True:
            self._data.item_sort.order = order
            for i_group_item in self.get_all_group_items():
                i_group_item._item_model.apply_sort_order(order)
            self._update_item_sort()

    # item group
    def set_item_group_enable(self, boolean):
        self._data.item_group_enable = boolean
        if boolean is True:
            self._data.item_group = _base._Data(
                keys=[],
                key_current=self.ItemGroupKey.Null,
            )

    def is_item_group_enable(self):
        return self._data.item_group_enable

    def set_item_group_keys(self, keys):
        if self._data.item_group_enable is True:
            self._data.item_group.keys = keys

    def get_item_group_key_current(self):
        if self._data.item_group_enable is True:
            return self._data.item_group.key_current

    def group_item_by(self, key):
        if self._data.item_group_enable is True:
            self._data.item_group.key_current = key
            # remove group items first
            self.remove_all_group_items()

            [x._item_model.apply_group_key(key) for x in self.get_all_items()]

            self._update_item_groups()

    def _update_item_groups(self):
        group_names = self._generate_item_current_group_names()
        for i_group_name in group_names:
            self.create_group_item(i_group_name, sort_order=self._data.item_sort.order)

    def generate_item_group_menu_data(self):
        if self._data.item_group_enable is True:
            menu_data = [
                (_gui_core.GuiName.GroupByChs,) if _gui_core.GuiUtil.language_is_chs() else (_gui_core.GuiName.GroupBy,)
            ]

            for i_group_key in self.ItemGroupKey.ALL:
                if i_group_key == self._data.item_group.key_current:
                    i_icon_name = 'radio_checked'
                else:
                    i_icon_name = 'radio_unchecked'

                if _gui_core.GuiUtil.language_is_chs():
                    i_name = self.ItemGroupKey.NAME_MAP_CHS[i_group_key]
                else:
                    i_name = self.ItemGroupKey.NAME_MAP[i_group_key]

                if i_group_key == self.ItemGroupKey.Null:
                    menu_data.append(
                        (i_name, i_icon_name, functools.partial(self.group_item_by, i_group_key))
                    )
                else:
                    i_enable = self._data.get('item_{}_enable'.format(i_group_key))
                    if i_enable is True:
                        menu_data.append(
                            (i_name, i_icon_name, functools.partial(self.group_item_by, i_group_key))
                        )
            return menu_data
        return []

    def _generate_item_current_group_names(self):
        if self._data.item_group_enable is True:
            dict_ = {}
            for i_item in self.get_all_items():
                # only add for non-group
                if i_item.GROUP_FLAG is False:
                    dict_.setdefault(
                        i_item._item_model._generate_current_group_name(), []
                    ).append(i_item)

            group_names = dict_.keys()
            group_names = filter(None, group_names)

            sort_order = self.get_item_sort_order()
            if sort_order is not None:
                group_names.sort(reverse=sort_order)
            return group_names
        return []
