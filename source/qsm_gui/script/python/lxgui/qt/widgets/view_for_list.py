# coding=utf-8
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from ...qt import abstracts as _qt_abstracts
# qt widgets
from . import utility as _utility

from . import item_for_list as _item_for_list

from . import entry_frame as _entry_frame


class QtListWidget(
    _qt_abstracts.AbsQtListWidget,
    _qt_abstracts.AbsQtMenuBaseDef,
):
    ctrl_f_key_pressed = qt_signal()
    f5_key_pressed = qt_signal()
    item_checked = qt_signal(object, int)
    #
    focus_changed = qt_signal()
    #
    info_text_accepted = qt_signal(str)
    QT_MENU_CLS = _utility.QtMenu

    def __init__(self, *args, **kwargs):
        super(QtListWidget, self).__init__(*args, **kwargs)
        self._init_menu_base_def_(self)
        qt_palette = _qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)

        self.setSelectionMode(self.SingleSelection)

        self.setResizeMode(self.Adjust)
        self.setVerticalScrollMode(self.ScrollPerItem)

        self._item_frame_icon_width, self._item_frame_icon_height = 40, 128
        self._item_frame_image_width, self._item_frame_image_height = 128, 128
        self._item_frame_name_width, self._item_frame_name_height = 128, 40

        self._grid_size = 128, 128

        self._item_side = 4
        self._item_spacing = 2

        self._item_frame_size = 128, 128
        self._item_frame_size_basic = 128, 128
        self._item_frame_draw_enable = False

        self._item_icon_frame_size = 20, 20
        self._item_icon_size = 16, 16
        self._item_icon_frame_draw_enable = False

        self._item_list_mode_auto_size = False
        self._item_image_frame_size = 108, 124
        self._item_image_size = 112, 128

        self._item_name_frame_size = 16, 16
        self._item_name_size = 12, 12
        self._item_name_frame_draw_enable = False
        self._item_names_draw_range = None

        self._item_scale_percent = 1.0

        self._item_image_frame_draw_enable = False

        self._item_image_draw_as_full = False

        self._set_grid_mode_()

        self._action_control_flag = False

        self.item_checked.connect(
            self._refresh_info_
        )

        self._info = ''

        self._drag_action_flag = False

        self._selection_mode_mark = None

    def _do_wheel_(self, event):
        if self._action_control_flag is True:
            delta = event.angleDelta().y()
            step = 4
            w_pre, h_pre = self._item_frame_size
            if delta > 0:
                w_cur = w_pre+step
            else:
                w_cur = w_pre-step
            #
            w_cur = max(min(w_cur, 480), 28)
            if w_cur != w_pre:
                h_cur = int(float(h_pre)/float(w_pre)*w_cur)
                self._set_item_frame_size_(w_cur, h_cur)
                self._set_all_item_widgets_update_()

    def _set_item_scale_percent_(self, scale):
        self._item_scale_percent = scale
        #
        w_pre, h_pre = self._item_frame_size
        w_bsc, h_bsc = self._item_frame_size_basic
        #
        w_cur = w_bsc*scale
        w_cur = max(min(w_cur, 480), 48)
        w_cur = w_cur+w_cur%2
        #
        if w_cur != w_pre:
            h_cur = int(float(h_bsc)/float(w_bsc)*w_cur)
            self._set_item_frame_size_(w_cur, h_cur)
            self._set_all_item_widgets_update_()
            #
            self._refresh_viewport_showable_auto_()

    def contextMenuEvent(self, event):
        menu_data = []
        #
        view_menu_data = self._get_menu_data_()
        if view_menu_data:
            menu_data.extend(view_menu_data)
            menu_data.append(
                ()
            )
        #
        item = self._get_item_current_()
        if item:
            item_menu_data = item._get_menu_data_()
            menu_data.extend(
                item_menu_data
            )
        #
        if menu_data:
            menu = self.QT_MENU_CLS(self)
            #
            menu._set_menu_data_(menu_data)
            menu._popup_start_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_F and event.modifiers() == QtCore.Qt.ControlModifier:
                    self.ctrl_f_key_pressed.emit()
                elif event.key() == QtCore.Qt.Key_F5:
                    self.f5_key_pressed.emit()
                elif event.key() == QtCore.Qt.Key_Control:
                    self._action_control_flag = True
            elif event.type() == QtCore.QEvent.KeyRelease:
                if event.key() == QtCore.Qt.Key_Control:
                    self._action_control_flag = False
            elif event.type() == QtCore.QEvent.Wheel:
                self._do_wheel_(event)
                return True
            elif event.type() == QtCore.QEvent.Resize:
                # self._refresh_size_()
                self._refresh_view_all_items_viewport_showable_()
            elif event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                parent = self.parent()
                if isinstance(parent, _entry_frame.QtEntryFrame):
                    parent._set_focused_(True)
                self.focus_changed.emit()
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                parent = self.parent()
                if isinstance(parent, _entry_frame.QtEntryFrame):
                    parent._set_focused_(False)
                self.focus_changed.emit()
        # view port
        elif widget == self.viewport():
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.buttons() == QtCore.Qt.LeftButton:
                    # todo: to fix error rect selection when item is drag
                    # when is drag set to single selection mode
                    # when not press at item reset selection mode
                    if self.itemAt(event.pos()) is None:
                        if self._selection_mode_mark is not None:
                            self.setSelectionMode(self._selection_mode_mark)

                    self.pressed.emit()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    pass
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self.press_released.emit()
        if widget == self.verticalScrollBar():
            pass
        return False

    def paintEvent(self, event):
        if not self.count():
            painter = _qt_core.QtPainter(self.viewport())
            painter._draw_empty_image_by_rect_(
                self.rect(),
                self._empty_icon_name
            )
        # super(QtListWidget, self).paintEvent(event)

    def _update_drag_action_(self):
        # when is drag set to single selection mode
        if self._selection_mode_mark is None:
            self._selection_mode_mark = self.selectionMode()
        self.setSelectionMode(self.SingleSelection)

    def _set_drag_action_flag_(self, boolean):
        self._drag_action_flag = True

    # noinspection PyUnusedLocal
    def _refresh_size_(self):
        if self._scroll_is_enable is False:
            w, h = self.viewport().width(), self.viewport().height()
            # self.adjustSize()
            h_add = self.verticalScrollBar().maximum()
            # print h+h_add
            # self.adjustSize()

    # noinspection PyUnusedLocal
    def _refresh_info_(self, *args, **kwargs):
        c = sum([self.item(i)._get_is_checked_() for i in range(self.count())])
        if c:
            info = '{} item is checked ...'.format(c)
        else:
            info = ''
        #
        if info != self._info:
            self.info_text_accepted.emit(info)
            self._info = info

    def _get_item_frame_size_(self):
        if self._get_is_grid_mode_():
            w, h = (
                self._item_frame_icon_width+self._item_spacing+self._item_frame_image_width+self._item_side*2,
                self._item_frame_image_height+self._item_spacing+self._item_frame_name_height+self._item_side*2
            )
            return w, h
        else:
            w, h = (
                self._item_frame_image_width+self._item_spacing+self._item_frame_image_width+self._item_side*2,
                self._item_frame_image_height+self._item_side*2
            )
            return w, h

    def _set_item_frame_size_(self, w, h):
        self._item_frame_size = w, h
        self._update_grid_size_(w, h)

    def _update_grid_size_(self, w, h):
        _w, _h = w+self._item_side*2, h+self._item_side*2
        self._set_grid_size_(_w, _h)

    def _set_grid_mode_(self):
        self.setViewMode(self.IconMode)
        self._update_grid_size_(*self._item_frame_size)
        self._update_by_item_mode_change_()

    def _set_list_mode_(self):
        self.setViewMode(self.ListMode)
        if self._item_list_mode_auto_size is True:
            self._update_grid_size_(*self._item_image_frame_size)
        self._update_by_item_mode_change_()

    def _set_item_size_basic_(self, w, h):
        self._item_frame_size_basic = w, h
        self._set_item_frame_size_(w, h)

    def _set_item_frame_draw_enable_(self, boolean):
        self._item_frame_draw_enable = boolean

    def _set_item_icon_frame_size_(self, w, h):
        self._item_icon_frame_size = w, h

    def _set_item_icon_size_(self, w, h):
        self._item_icon_size = w, h

    def _set_item_icon_frame_draw_enable_(self, boolean):
        self._item_icon_frame_draw_enable = boolean

    def _set_item_image_frame_size_(self, w, h):
        self._item_list_mode_auto_size = True
        self._item_image_frame_size = w, h

    def _get_item_image_frame_size_(self):
        return self._item_image_frame_size

    def _get_item_list_mode_auto_size_(self):
        return self._item_list_mode_auto_size

    def _set_item_image_size_(self, w, h):
        self._item_image_size = w, h

    def _set_item_name_frame_size_(self, w, h):
        self._item_name_frame_size = w, h

    def _set_item_name_size_(self, w, h):
        self._item_name_size = w, h

    def _set_item_name_frame_draw_enable_(self, boolean):
        self._item_name_frame_draw_enable = boolean

    def _set_item_names_draw_range_(self, range_):
        self._item_names_draw_range = range_

    def _set_item_image_frame_draw_enable_(self, boolean):
        self._item_image_frame_draw_enable = boolean

    def _set_item_image_draw_as_full_(self, boolean):
        self._item_image_draw_as_full = boolean

    def _get_item_count_(self):
        return self.count()

    def _set_all_item_widgets_update_(self):
        [
            (i._set_frame_size_(*self._item_frame_size), i._refresh_widget_draw_geometry_())
            for i in self._get_all_item_widgets_()
        ]

    def _set_all_item_widgets_checked_(self, boolean):
        [
            i._set_checked_(boolean)
            for i in self._get_all_item_widgets_()
        ]
        [
            i._set_checked_(boolean)
            for i in self._get_all_items_()
        ]
        self.item_checked.emit(self, 0)

    def _set_all_visible_item_widgets_checked_(self, boolean):
        [
            i._set_checked_(boolean)
            for i in self._get_all_visible_item_widgets_()
        ]
        [
            i._set_checked_(boolean)
            for i in self._get_all_visible_items_()
        ]
        self.item_checked.emit(self, 0)

    def _swap_view_mode_(self):
        if self._get_is_grid_mode_() is True:
            self._set_list_mode_()
        else:
            self._set_grid_mode_()

        self._refresh_viewport_showable_auto_()

    def _get_is_grid_mode_(self):
        return self.viewMode() == self.IconMode

    # noinspection PyUnusedLocal
    def _add_item_widget_(self, item_widget, *args, **kwargs):
        view = self
        #
        index_cur = view._get_item_count_()
        item = _item_for_list.QtListWidgetItem('', view)
        view.addItem(item)
        # debug for position error
        index = self.row(item)
        if index > 0:
            item.setHidden(True)
            item.setHidden(False)
        #
        item.setSizeHint(QtCore.QSize(*self._grid_size))
        view.setItemWidget(item, item_widget)
        item.gui_proxy = item_widget.gui_proxy
        #
        item_widget.user_check_toggled.connect(
            item._update_checked_from_user_
        )
        item._initialize_item_show_()
        item.setText(str(index_cur).zfill(4))
        # set view and item first
        item_widget._set_view_(view)
        item_widget._set_item_(item)
        # and set other below
        item_widget._set_sort_number_key_(index_cur)
        item_widget._set_index_(index_cur)
        #
        item_widget._set_frame_size_(
            *self._item_frame_size
        )
        item_widget._set_frame_draw_enable_(
            self._item_frame_draw_enable
        )
        #
        item_widget._set_icon_frame_draw_size_(
            *self._item_icon_frame_size
        )
        item_widget._set_icon_size_(
            *self._item_icon_size
        )
        item_widget._set_icon_frame_draw_enable_(
            self._item_icon_frame_draw_enable
        )
        #
        item_widget._set_name_frame_size_(
            *self._item_name_frame_size
        )
        item_widget._set_names_draw_range_(
            self._item_names_draw_range
        )
        item_widget._set_name_size_(
            *self._item_name_size
        )
        item_widget._set_name_frame_draw_enable_(
            self._item_name_frame_draw_enable
        )
        item_widget._set_image_draw_as_full_(
            self._item_image_draw_as_full
        )
        #
        item_widget._set_image_frame_draw_enable_(
            self._item_image_frame_draw_enable
        )

    def _create_item_(self, *args, **kwargs):
        view = self
        #
        index_cur = view._get_item_count_()
        item = _item_for_list.QtListWidgetItem('', view)
        view.addItem(item)
        # debug for position error
        index = self.row(item)
        if index > 0:
            item.setHidden(True)
            item.setHidden(False)

        item.setSizeHint(QtCore.QSize(*self._grid_size))
        item.setText(str(index_cur).zfill(4))

        item._set_sort_number_key_(index)
        item._initialize_item_show_()
        return item

    def _connect_item_widget_(self, item, item_widget, *args, **kwargs):
        view = self

        index = self.row(item)

        view.setItemWidget(item, item_widget)
        item.gui_proxy = item_widget.gui_proxy

        item_widget.user_check_toggled.connect(item._update_checked_from_user_)
        # set view and item first
        item_widget._set_view_(view)
        item_widget._set_item_(item)
        # and set other below
        item_widget._set_index_(index)
        #
        item_widget._set_frame_size_(
            *self._item_frame_size
        )
        item_widget._set_frame_draw_enable_(self._item_frame_draw_enable)
        item_widget._set_icon_frame_draw_size_(*self._item_icon_frame_size)
        item_widget._set_icon_size_(*self._item_icon_size)
        item_widget._set_icon_frame_draw_enable_(self._item_icon_frame_draw_enable)
        item_widget._set_name_frame_size_(*self._item_name_frame_size)
        item_widget._set_names_draw_range_(self._item_names_draw_range)
        item_widget._set_name_size_(*self._item_name_size)
        item_widget._set_name_frame_draw_enable_(self._item_name_frame_draw_enable)
        item_widget._set_image_draw_as_full_(self._item_image_draw_as_full)
        item_widget._set_image_frame_draw_enable_(self._item_image_frame_draw_enable)

    def _set_clear_(self):
        for i in self._get_all_items_():
            i._kill_item_all_show_runnables_()
            i._stop_item_show_all_()
        #
        self._pre_selected_items = []
        #
        self.clear()
