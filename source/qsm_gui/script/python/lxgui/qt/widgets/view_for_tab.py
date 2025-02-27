# coding=utf-8
import functools
import sys

import lxbasic.core as bsc_core
# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *

from .. import core as _qt_core

from .. import abstracts as _qt_abstracts
# qt widgets
from . import utility as _qt_wgt_utility

from . import button as _qt_wgt_button

from . import layer_stack as _qt_wgt_layer_stack


class AbsQtItemsDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _init_items_base_def_(self, widget):
        self._widget = widget

        self._tab_item_stack = _qt_core.GuiQtModForTabItemStack(self)
        self._hover_tab_index = None
        self._index_press = None
        self._item_index_dragged = None

        self._index_press_tmp = None
        self._index_drag_child_polish_start = None
        self._index_drag_child_polish = None

        self._item_width_dict = {}

        self._drag_press_point = QtCore.QPoint()
        self._drag_offset_move_x, self._drag_offset_move_y = 0, 0

    def _switch_current_to_(self, index):
        pass


class QtTabView(
    QtWidgets.QWidget,
    AbsQtItemsDef,
    _qt_abstracts.AbsQtFrameBaseDef,
    _qt_abstracts.AbsQtWidgetBaseDef,
    #
    _qt_abstracts.AbsQtMenuBaseDef,
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForDragDef,
    
    _qt_abstracts.AbsQtHistoryBaseDef,
):
    current_changed = qt_signal()

    tab_delete_post_accepted = qt_signal(str)

    QT_MENU_CLS = _qt_wgt_utility.QtMenu

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_(self.rect())
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self, rect):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        #
        self._frame_draw_rect.setRect(
            x, y, w, h
        )
        m_l, m_t, m_r, m_b = self._tab_view_margins
        t_w, t_h = self._tab_w, self._tab_h
        tab_bar_x, tab_bar_y = x, y
        tab_bar_w, tab_bar_h = w, t_h

        self._tab_bar_draw_rect.setRect(
            x, y, w, t_h-1
        )
        scroll_w = w
        tab_btn_x, tab_btn_y = x, y
        #
        btn_f_w, btn_f_h = t_h, t_h
        btn_w, btn_h = 20, 20
        if self._tab_add_is_enable is True:
            self._tab_left_tool_box_rect.setRect(
                x, y, btn_f_w, t_h
            )
            self._tab_left_tool_box_draw_rect.setRect(
                x, y, btn_f_w, t_h-1
            )
            self._tab_add_button.show()
            self._tab_add_button.setGeometry(
                int(x+(btn_f_w-btn_w)/2), int(y+(btn_f_h-btn_h)/2), int(btn_w), int(btn_h)
            )
            tab_btn_x += t_h
            scroll_w -= t_h
            #
            tab_bar_x += btn_f_w
            tab_bar_w -= btn_f_w
        #
        scroll_abs_w = 0
        tab_items = self._tab_item_stack.get_all_items()
        self._item_width_dict = {}
        # compute maximum tag item width for scroll
        if tab_items:
            for i_index, i_tab_item in enumerate(tab_items):
                i_name_text = i_tab_item.get_name()
                if i_name_text is not None:
                    i_text_width = self._get_text_draw_width_(
                        i_name_text
                    )
                else:
                    i_text_width = t_w
                # compute tab width
                i_t_w = i_text_width+t_h*2
                self._item_width_dict[i_index] = i_t_w

                scroll_abs_w += i_t_w
            # update scroll model
            self._scroll_bar_model.set_w_or_h(scroll_w)
            self._scroll_bar_model.set_abs_w_or_h(scroll_abs_w+btn_f_w*3)
            self._scroll_bar_model.update()
            #
            # if self._tab_menu_is_enable is True:
            #     self._tab_menu_button.show()
            #     self._tab_menu_button.setGeometry(
            #         w-btn_f_w+(btn_f_w-btn_w)/2, tab_btn_y+(btn_f_h-btn_h)/2, btn_w, btn_h
            #     )
            # check scroll is valid
            if self._scroll_bar_model.is_valid():
                btn_w_1, btn_h_1 = btn_w/2, btn_h
                btn_f_w_r = btn_f_w*2
                tab_btn_x_1, tab_btn_y_1 = w-btn_f_w_r, y
                tab_btn_x_1 = max(tab_btn_x_1, btn_f_w_r)
                self._tab_right_tool_box_rect.setRect(
                    tab_btn_x_1, tab_btn_y_1, btn_f_w_r, btn_f_h
                )
                self._tab_right_tool_box_draw_rect.setRect(
                    tab_btn_x_1, tab_btn_y_1, btn_f_w_r, btn_f_h-1
                )
                #
                self._tab_scroll_previous_button.show()
                self._tab_scroll_previous_button.setGeometry(
                    tab_btn_x_1+(btn_f_w-btn_w)/2, tab_btn_y_1+(btn_f_h-btn_h_1)/2, btn_w_1, btn_h_1
                )

                if self._scroll_bar_model.get_is_minimum():
                    self._tab_scroll_previous_button._set_icon_file_path_(self._icons_0[1])
                else:
                    self._tab_scroll_previous_button._set_icon_file_path_(self._icons_0[0])

                self._tab_scroll_next_button.show()
                self._tab_scroll_next_button.setGeometry(
                    tab_btn_x_1+(btn_f_w-btn_w)/2+btn_w_1, tab_btn_y_1+(btn_f_h-btn_h_1)/2, btn_w_1, btn_h_1
                )

                if self._scroll_bar_model.get_is_maximum():
                    self._tab_scroll_next_button._set_icon_file_path_(self._icons_1[1])
                else:
                    self._tab_scroll_next_button._set_icon_file_path_(self._icons_1[0])

                self._tab_choose_button.show()
                self._tab_choose_button.setGeometry(
                    tab_btn_x_1+btn_f_w+(btn_f_w-btn_w)/2, tab_btn_y_1+(btn_f_h-btn_h)/2, btn_w, btn_h
                )

                tab_bar_w -= btn_f_w_r
            else:
                self._tab_scroll_previous_button.hide()
                self._tab_scroll_next_button.hide()
                self._tab_choose_button.hide()

            scroll_value = self._scroll_bar_model.get_value()
            widths = list(self._item_width_dict.values())
            if self._is_action_flag_match_(
                self.ActionFlag.DragChildPolish
            ):
                width_ = self._item_width_dict[self._index_drag_child_polish_start]
                widths_ = [_i for _seq, _i in enumerate(widths) if _seq != self._index_drag_child_polish_start]
                for i_index, i_tab_item in enumerate(tab_items):
                    i_rect = i_tab_item.get_rect()
                    i_draw_rect = i_tab_item.get_draw_rect()

                    i_x = sum(widths[:i_index])
                    i_w = self._item_width_dict[i_index]

                    i_rect.setRect(
                        tab_btn_x+i_x-scroll_value, y, i_w, t_h
                    )
                    # on drag enter right
                    if self._index_drag_child_polish_start < i_index <= self._index_drag_child_polish:
                        i_draw_x = sum(widths_[:i_index-1])
                    # on drag enter index left
                    elif self._index_drag_child_polish <= i_index < self._index_drag_child_polish_start:
                        i_draw_x = sum(widths_[:i_index])+width_
                    else:
                        i_draw_x = i_x

                    if i_index == self._index_drag_child_polish_start:
                        i_draw_x = i_x
                        i_x_cur = i_draw_x+self._drag_offset_move_x
                        i_draw_rect.setRect(
                            i_x_cur-scroll_value, y, i_w, t_h
                        )
                    else:
                        i_draw_rect.setRect(
                            tab_btn_x+i_draw_x-scroll_value, y, i_w, t_h
                        )
            else:
                for i_index, i_tab_item in enumerate(tab_items):
                    i_rect = i_tab_item.get_rect()
                    i_draw_rect = i_tab_item.get_draw_rect()

                    i_x = sum(widths[:i_index])
                    i_w = self._item_width_dict[i_index]

                    i_draw_rect.setRect(
                        tab_btn_x+i_x-scroll_value, y, i_w, t_h
                    )
                    i_rect.setRect(
                        tab_btn_x+i_x-scroll_value, y, i_w, t_h
                    )

        self._layer_stack.setGeometry(
            x+m_l, y+t_h+m_t, w-m_l-m_r, h-t_h-m_t-m_b
        )

        self._tab_bar_rect.setRect(
            tab_bar_x, tab_bar_y, tab_bar_w, tab_bar_h
        )

    def _load_history_(self):
        self._set_current_key_text_(
            self._get_history_value_()
        )

    def _save_history_(self):
        self._set_history_value_(
            self._get_current_key_text_()
        )

    def __init__(self, *args, **kwargs):
        super(QtTabView, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self._init_items_base_def_(self)

        self._init_frame_base_def_(self)
        self._init_widget_base_def_(self)
        self._init_menu_base_def_(self)

        self._init_action_base_def_(self)
        self._init_action_for_drag_def_(self)
        
        self._init_history_base_def_(self)

        self._tab_bar_rect = qt_rect()
        self._tab_bar_draw_rect = qt_rect()
        self._tab_left_tool_box_rect = qt_rect()
        self._tab_left_tool_box_draw_rect = qt_rect()
        self._tab_right_tool_box_rect = qt_rect()
        self._tab_right_tool_box_draw_rect = qt_rect()

        self._tab_add_is_enable = False
        self._tab_add_button = _qt_wgt_button.QtIconMenuButton(self)
        self._tab_add_button.hide()
        self._tab_add_button._set_icon_file_path_(
            _gui_core.GuiIcon.get('tab/tab-add')
        )

        self._icons_0 = [
            _gui_core.GuiIcon.get('window_base/scroll-left'),
            _gui_core.GuiIcon.get('window_base/scroll-left-disable')
        ]
        self._icons_1 = [
            _gui_core.GuiIcon.get('window_base/scroll-right'),
            _gui_core.GuiIcon.get('window_base/scroll-right-disable')
        ]

        self._tab_scroll_previous_button = _qt_wgt_button.QtIconPressButton(self)
        self._tab_scroll_previous_button.hide()
        self._tab_scroll_previous_button._set_icon_geometry_mode_(
            _qt_wgt_button.QtIconPressButton.IconGeometryMode.Auto
        )
        self._tab_scroll_previous_button.setFixedSize(10, 20)
        self._tab_scroll_previous_button._set_icon_file_path_(self._icons_0[0])
        self._tab_scroll_previous_button.press_clicked.connect(self._do_scroll_previous_)

        self._tab_scroll_next_button = _qt_wgt_button.QtIconPressButton(self)
        self._tab_scroll_next_button.hide()
        self._tab_scroll_next_button._set_icon_geometry_mode_(
            _qt_wgt_button.QtIconPressButton.IconGeometryMode.Auto
        )
        self._tab_scroll_next_button.setFixedSize(10, 20)
        self._tab_scroll_next_button._set_icon_file_path_(self._icons_1[0])
        self._tab_scroll_next_button.press_clicked.connect(self._do_scroll_next_)

        self._tab_choose_button = _qt_wgt_button.QtIconMenuButton(self)
        self._tab_choose_button.hide()
        self._tab_choose_button._set_icon_file_path_(
            _gui_core.GuiIcon.get('tab/tab-choose')
        )

        self._tab_menu_is_enable = False
        self._tab_menu_button = _qt_wgt_button.QtIconMenuButton(self)
        self._tab_menu_button.hide()
        self._tab_menu_button._set_icon_file_path_(
            _gui_core.GuiIcon.get('tab/tab-menu-v')
        )

        self._tab_view_margins = 2, 2, 2, 2

        self._tab_w, self._tab_h = 48, 24

        self.setFont(
            _qt_core.QtFont.generate(size=10)
        )

        self._scroll_bar_model = _qt_core.GuiQtModForScroll()
        self._scroll_bar_model.set_step(64)
        self._set_menu_data_generate_fnc_(
            self._tab_item_menu_gain_fnc_
        )

        self._layer_stack = _qt_wgt_layer_stack.QtLayerStack(self)
        self._layer_stack.installEventFilter(self)
        # use layer stack signal
        self._layer_stack.current_changed.connect(self.current_changed.emit)
        self._layer_stack.current_changed.connect(self._save_history_)

        self._delete_pre_fnc_dict = dict()

        # self._set_tool_tip_(
        #     [
        #         '"LMB-click" to show page',
        #         '"MMB-wheel" to scroll to other page',
        #         '"RMB-click" to show more actions',
        #     ]
        # )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.ToolTip:
                self._do_show_tool_tip_(event)
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                self._clear_item_hover_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self._index_press_tmp = self._compute_press_index_loc_(
                    event.pos()
                )
                self._press_point = event.pos()
                if event.button() == QtCore.Qt.LeftButton:
                    if self._index_press_tmp is not None:
                        self._set_action_flag_(self.ActionFlag.Press)
                        self._on_tab_button_press_(self._index_press_tmp)
                elif event.button() == QtCore.Qt.RightButton:
                    if self._index_press_tmp is not None:
                        self._popup_menu_()
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
            # drag and hover
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    if self._drag_is_enable is True:
                        # check "DragPress" when flag is match "Press"
                        if self._is_action_flag_match_(self.ActionFlag.Press):
                            if self._index_press_tmp is not None:
                                self._drag_press_point = self._press_point
                                self._set_action_flag_(self.ActionFlag.DragPress)
                        elif self._is_action_flag_match_(self.ActionFlag.DragPress):
                            self._do_drag_press_(event)
                        elif self._is_action_flag_match_(self.ActionFlag.DragChildPolish):
                            self._do_drag_child_polish_(event)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                elif event.button() == QtCore.Qt.NoButton:
                    self._do_hover_move_(event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    # when drag press move less than 10px, do press release also
                    if self._is_action_flag_match_(self.ActionFlag.Press, self.ActionFlag.DragPress):
                        # send signal in release action
                        self._do_mouse_press_release_(event)
                    elif self._is_action_flag_match_(self.ActionFlag.DragChildPolish):
                        self._do_drop_(event)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()

                self._index_press_tmp = None
                self._hover_tab_index = None
                self._clear_all_action_flags_()
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.Wheel:
                self._do_wheel_(event)
                return True
        elif widget == self._layer_stack:
            if event.type() == QtCore.QEvent.Enter:
                self._clear_item_hover_()
            if event.type() == QtCore.QEvent.Leave:
                self._clear_item_hover_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        painter._draw_tab_view_buttons_(
            self._tab_bar_draw_rect,
            virtual_items=self._tab_item_stack.get_all_items(),
            index_hover=self._hover_tab_index,
            index_pressed=self._index_press_tmp,
            index_current=self._get_current_index_(),
        )
        #
        if self._tab_add_is_enable:
            painter._draw_tab_left_tool_box_by_rect_(
                rect=self._tab_left_tool_box_draw_rect
            )
        #
        if self._scroll_bar_model.is_valid():
            painter._draw_tab_right_tool_box_by_rect_(
                rect=self._tab_right_tool_box_draw_rect,
                background_color=_qt_core.QtRgba.Dark
            )

    def _delete_widget_at_(self, index):
        item = self._tab_item_stack.get_item_at(index)
        # pre delete
        key = item.get_key()
        if key in self._delete_pre_fnc_dict:
            sys.stderr.write('execute page delete pre function at: {}.\n'.format(index))
            fnc = self._delete_pre_fnc_dict.pop(key)
            fnc(key)

        sys.stderr.write('delete page at: {}.\n'.format(index))
        # delete later
        self._layer_stack._delete_widget_at_(index)
        # post delete
        self.tab_delete_post_accepted.emit(item.get_key() or item.get_name())
        #
        self._tab_item_stack.delete_item(item)
        self._refresh_widget_all_()
        self.current_changed.emit()

    def _register_page_delete_pre_fnc_(self, key, fnc):
        self._delete_pre_fnc_dict[key] = fnc

    def _add_widget_(self, widget, *args, **kwargs):
        # widget.setParent(self)
        self._layer_stack._add_widget_(widget, *args, **kwargs)
        tab_item = self._tab_item_stack.create_item(widget)
        if 'key' in kwargs:
            tab_item.set_key(kwargs['key'])
        if 'name' in kwargs:
            tab_item.set_name(kwargs['name'])
        if 'icon_name_text' in kwargs:
            tab_item.set_icon_text(kwargs['icon_name_text'])
        if 'tool_tip' in kwargs:
            tab_item.set_tool_tip(kwargs['tool_tip'])

        self._refresh_widget_all_()
        return tab_item

    def _set_tab_add_enable_(self, boolean):
        self._tab_add_is_enable = boolean
        self._refresh_widget_all_()

    def _set_tab_add_menu_data_(self, data):
        self._tab_add_button._set_menu_data_(data)

    def _set_tab_add_menu_data_generate_fnc_(self, fnc):
        self._tab_add_button._set_menu_data_generate_fnc_(fnc)
    
    def _set_tab_add_menu_content_(self, content):
        self._tab_add_button._set_menu_content_(content)
    
    def _set_tab_add_menu_content_generate_fnc_(self, fnc):
        self._tab_add_button._set_menu_content_generate_fnc_(fnc)

    def _set_tab_menu_enable_(self, boolean):
        self._tab_menu_is_enable = boolean
        self._refresh_widget_all_()

    def _set_tab_menu_data_(self, data):
        self._tab_menu_button._set_menu_data_(data)

    def _set_tab_menu_data_generate_fnc_(self, fnc):
        self._tab_menu_button._set_menu_data_generate_fnc_(fnc)

    def _clear_item_hover_(self):
        self._hover_tab_index = None
        self._refresh_widget_draw_()

    def _on_tab_button_press_(self, index):
        if index != self._index_press:
            self._index_press = index

            self._refresh_widget_all_()

    def _set_item_drag_moving_at_(self, index):
        if index != self._item_index_dragged:
            self._item_index_dragged = index

            self._refresh_widget_all_()

    def _switch_current_to_(self, index):
        self._index_press = None
        self._layer_stack._switch_current_to_(index)
        self._refresh_widget_all_()

    def _update_index_current_(self, index):
        self._index_press = None
        self._layer_stack._update_index_current_(index)
        self._refresh_widget_all_()

    def _get_current_index_(self):
        return self._layer_stack._get_current_index_()

    def _set_current_name_text_(self, text):
        index = self._tab_item_stack.get_index_by_name(
            text
        )
        if index is not None:
            self._switch_current_to_(index)

    def _set_current_key_text_(self, text):
        index = self._tab_item_stack.get_index_by_key(
            text
        )
        if index is not None:
            self._switch_current_to_(index)
            return True
        return False

    def _compute_press_index_loc_(self, p):
        if self._tab_bar_rect.contains(p):
            for i_index, i_tab_item in enumerate(self._tab_item_stack.get_all_items()):
                if i_tab_item.get_rect().contains(p):
                    return i_index
    
    def _compute_press_move_index_loc_(self, p):
        rect = self._tab_bar_rect
        x = p.x()
        if rect.topLeft().x() <= x <= rect.topRight().x():
            for i_index, i_tab_item in enumerate(self._tab_item_stack.get_all_items()):
                i_rect = i_tab_item.get_rect()
                if i_rect.topLeft().x() <= x <= i_rect.topRight().x():
                    return i_index

    # noinspection PyUnusedLocal
    def _do_show_tool_tip_(self, event):
        if self._hover_tab_index is not None:
            key = self._get_page_key_at_(self._hover_tab_index)
            if key is None:
                title = self._get_page_name_text_at_(self._hover_tab_index)
                tool_tip = self._get_page_tool_tip_text_at_(self._hover_tab_index)
            else:
                title = self._get_page_name_text_at_(self._hover_tab_index)
                tool_tip = self._get_page_tool_tip_text_at_(self._hover_tab_index)

            css = _qt_core.QtUtil.generate_tool_tip_css(
                title,
                content=tool_tip,
                action_tip=[
                    '"LMB-click" to show this page',
                    '"MMB-wheel" to scroll to other page',
                    '"RMB-click" to show more actions for this page',
                ]
            )
            rect = self._get_rect_at_(self._hover_tab_index)
            p = rect.bottomRight()
            p = self.mapToGlobal(p) + QtCore.QPoint(0, -18)

            QtWidgets.QToolTip.showText(
                p, css, self
            )

    # noinspection PyUnusedLocal
    def _do_mouse_press_release_(self, event):
        if self._index_press_tmp is not None:
            self._switch_current_to_(
                self._index_press_tmp
            )

    def _do_hover_move_(self, event):
        p = event.pos()
        self._hover_tab_index = None
        if self._tab_bar_rect.contains(p):
            for i_index, i_tab_item in enumerate(self._tab_item_stack.get_all_items()):
                if i_tab_item.rect.contains(p):
                    self._hover_tab_index = i_index
                    break

        self._refresh_widget_draw_()

    def _do_drag_press_(self, event):
        p = event.pos()
        p_d = p-self._drag_press_point
        x, y = p_d.x(), p_d.y()
        # enable when mouse moved more than 10 pixel
        if abs(x) > 10:
            self._index_drag_child_polish_start = self._index_press_tmp
            self._index_drag_child_polish = self._index_press_tmp
            self._set_action_flag_(self.ActionFlag.DragChildPolish)
            # when drag is not current, set to current first
            if self._index_press_tmp != self._get_current_index_():
                self._update_index_current_(self._index_press_tmp)

    def _do_drag_child_polish_(self, event):
        p = event.pos()
        p_d = p - self._drag_press_point
        self._drag_offset_move_x, self._drag_offset_move_y = p_d.x(), p_d.y()
        index_cur = self._compute_press_move_index_loc_(p)
        if index_cur is not None:
            self._index_drag_child_polish = index_cur

        self._refresh_widget_all_()

    # noinspection PyUnusedLocal
    def _do_drop_(self, event):
        self._tab_item_stack.insert_item_between(
            self._index_drag_child_polish_start, self._index_drag_child_polish
        )
        self._layer_stack._insert_widget_between_(
            self._index_drag_child_polish_start, self._index_drag_child_polish
        )
        self._refresh_widget_all_()

    def _do_wheel_(self, event):
        p = event.pos()
        if self._tab_bar_rect.contains(p):
            delta = event.angleDelta().y()
            item_count = self._tab_item_stack.get_count()
            if item_count > 1:
                maximum, minimum = item_count-1, 0
                index_cur = self._get_current_index_()
                if delta > 0:
                    index = bsc_core.RawIndexMtd.to_previous(maximum, minimum, index_cur)
                else:
                    index = bsc_core.RawIndexMtd.to_next(maximum, minimum, index_cur)
                #
                self._do_scroll_to_(index)
                self._switch_current_to_(index)

    def _get_current_name_text_(self):
        return self._tab_item_stack.get_name_at(
            self._get_current_index_()
        )

    def _get_current_key_text_(self):
        return self._tab_item_stack.get_key_at(
            self._get_current_index_()
        )

    def _get_all_page_name_texts_(self):
        return self._tab_item_stack.get_all_names()

    def _get_all_page_key_texts_(self):
        return self._tab_item_stack.get_all_keys()

    def _get_page_key_at_(self, index):
        return self._tab_item_stack.get_key_at(
            index
        )

    def _get_page_name_text_at_(self, index):
        return self._tab_item_stack.get_name_at(index)

    def _get_rect_at_(self, index):
        return self._tab_item_stack.get_rect_at(index)

    def _get_page_tool_tip_text_at_(self, index):
        return self._tab_item_stack.get_tool_tip_at(index)

    def _tab_item_menu_gain_fnc_(self):
        if self._index_press_tmp is not None:
            if _gui_core.GuiUtil.language_is_chs():
                return [
                    (
                        '关闭页面', 'close-hover',
                        functools.partial(self._delete_widget_at_, self._index_press_tmp)
                    ),
                ]
            else:
                return [
                    (
                        'close page', 'close-hover',
                        functools.partial(self._delete_widget_at_, self._index_press_tmp)
                    ),
                ]
        return []

    def _do_scroll_to_(self, index):
        item = self._tab_item_stack.get_item_at(index)
        if item:
            x = item.get_rect().x()
            self._scroll_bar_model.accept_value(x-24)

    def _do_scroll_previous_(self):
        if self._scroll_bar_model.step_to_previous():
            self._refresh_widget_all_()

    def _do_scroll_next_(self):
        if self._scroll_bar_model.step_to_next():
            self._refresh_widget_all_()
