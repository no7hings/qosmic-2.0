# coding=utf-8
import functools

import lxbasic.core as bsc_core
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import core as gui_qt_core

from .. import abstracts as gui_qt_abstracts
# qt widgets
from . import utility as gui_qt_wgt_utility

from . import button as gui_qt_wgt_button

from . import layer_stack as gui_qt_wgt_layer_stack


class AbsQtItemsDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _init_items_base_def_(self, widget):
        self._widget = widget

        self._tab_item_stack = gui_qt_core.GuiQtModForTabItemStack(self)
        self._index_hover = None
        self._item_index_pressed = None
        self._item_index_dragged = None

        self._index_press = None
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
    gui_qt_abstracts.AbsQtFrameBaseDef,
    gui_qt_abstracts.AbsQtWidgetBaseDef,
    #
    gui_qt_abstracts.AbsQtMenuBaseDef,
    gui_qt_abstracts.AbsQtActionBaseDef,
    gui_qt_abstracts.AbsQtActionForDragDef,
):
    current_changed = qt_signal()

    tab_delete_accepted = qt_signal(str)

    QT_MENU_CLS = gui_qt_wgt_utility.QtMenu

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_(self.rect())
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self, rect):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        #
        self._rect_frame_draw.setRect(
            x, y, w, h
        )
        m_l, m_t, m_r, m_b = self._tab_view_margins
        t_w, t_h = self._tab_w, self._tab_h
        c_t_f_x, c_t_f_y = x, y
        c_t_f_w, c_t_f_h = w, t_h
        self._tab_bar_draw_rect.setRect(
            x, y, w, t_h-1
        )
        scroll_w = w
        c_x, c_y = x, y
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
                x+(btn_f_w-btn_w)/2, y+(btn_f_h-btn_h)/2, btn_w, btn_h
            )
            c_x += t_h
            scroll_w -= t_h
            #
            c_t_f_x += btn_f_w
            c_t_f_w -= btn_f_w
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
            self._gui_scroll.set_w_or_h(scroll_w)
            self._gui_scroll.set_abs_w_or_h(scroll_abs_w+btn_f_w*3)
            self._gui_scroll.update()
            #
            # if self._tab_menu_is_enable is True:
            #     self._tab_menu_button.show()
            #     self._tab_menu_button.setGeometry(
            #         w-btn_f_w+(btn_f_w-btn_w)/2, c_y+(btn_f_h-btn_h)/2, btn_w, btn_h
            #     )
            # check scroll is valid
            if self._gui_scroll.get_is_valid():
                btn_w_1, btn_h_1 = btn_w/2, btn_h
                btn_f_w_r = btn_f_w*2
                c_x_1, c_y_1 = w-btn_f_w_r, y
                c_x_1 = max(c_x_1, btn_f_w_r)
                self._tab_right_tool_box_rect.setRect(
                    c_x_1, c_y_1, btn_f_w_r, btn_f_h
                )
                self._tab_right_tool_box_draw_rect.setRect(
                    c_x_1, c_y_1, btn_f_w_r, btn_f_h-1
                )
                #
                self._tab_scroll_previous_button.show()
                self._tab_scroll_previous_button.setGeometry(
                    c_x_1+(btn_f_w-btn_w)/2, c_y_1+(btn_f_h-btn_h_1)/2, btn_w_1, btn_h_1
                )

                if self._gui_scroll.get_is_minimum():
                    self._tab_scroll_previous_button._set_icon_file_path_(self._icons_0[1])
                else:
                    self._tab_scroll_previous_button._set_icon_file_path_(self._icons_0[0])

                self._tab_scroll_next_button.show()
                self._tab_scroll_next_button.setGeometry(
                    c_x_1+(btn_f_w-btn_w)/2+btn_w_1, c_y_1+(btn_f_h-btn_h_1)/2, btn_w_1, btn_h_1
                )

                if self._gui_scroll.get_is_maximum():
                    self._tab_scroll_next_button._set_icon_file_path_(self._icons_1[1])
                else:
                    self._tab_scroll_next_button._set_icon_file_path_(self._icons_1[0])

                self._tab_choose_button.show()
                self._tab_choose_button.setGeometry(
                    c_x_1+btn_f_w+(btn_f_w-btn_w)/2, c_y_1+(btn_f_h-btn_h)/2, btn_w, btn_h
                )

                c_t_f_w -= btn_f_w_r
            else:
                self._tab_scroll_previous_button.hide()
                self._tab_scroll_next_button.hide()
                self._tab_choose_button.hide()

            scroll_value = self._gui_scroll.get_value()
            widths = self._item_width_dict.values()
            if self._get_action_flag_is_match_(
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
                        c_x+i_x-scroll_value, y, i_w, t_h
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
                            c_x+i_draw_x-scroll_value, y, i_w, t_h
                        )
            else:
                for i_index, i_tab_item in enumerate(tab_items):
                    i_rect = i_tab_item.get_rect()
                    i_draw_rect = i_tab_item.get_draw_rect()

                    i_x = sum(widths[:i_index])
                    i_w = self._item_width_dict[i_index]

                    i_draw_rect.setRect(
                        c_x+i_x-scroll_value, y, i_w, t_h
                    )
                    i_rect.setRect(
                        c_x+i_x-scroll_value, y, i_w, t_h
                    )

        self.__layer_stack.setGeometry(
            x+m_l, y+t_h+m_t, w-m_l-m_r, h-t_h-m_t-m_b
        )

        self._tab_bar_rect.setRect(
            c_t_f_x, c_t_f_y, c_t_f_w, c_t_f_h
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

        self._tab_bar_rect = QtCore.QRect()
        self._tab_bar_draw_rect = QtCore.QRect()
        self._tab_left_tool_box_rect = QtCore.QRect()
        self._tab_left_tool_box_draw_rect = QtCore.QRect()
        self._tab_right_tool_box_rect = QtCore.QRect()
        self._tab_right_tool_box_draw_rect = QtCore.QRect()

        self._tab_add_is_enable = False
        self._tab_add_button = gui_qt_wgt_button.QtIconMenuButton(self)
        self._tab_add_button.hide()
        self._tab_add_button._set_icon_file_path_(
            gui_core.GuiIcon.get('tab/tab-add')
        )

        self._icons_0 = [
            gui_core.GuiIcon.get('window_base/scroll-left'),
            gui_core.GuiIcon.get('window_base/scroll-left-disable')
        ]
        self._icons_1 = [
            gui_core.GuiIcon.get('window_base/scroll-right'),
            gui_core.GuiIcon.get('window_base/scroll-right-disable')
        ]

        self._tab_scroll_previous_button = gui_qt_wgt_button.QtIconPressButton(self)
        self._tab_scroll_previous_button.hide()
        self._tab_scroll_previous_button._set_icon_geometry_mode_(
            gui_qt_wgt_button.QtIconPressButton.IconGeometryMode.Auto
        )
        self._tab_scroll_previous_button.setFixedSize(10, 20)
        self._tab_scroll_previous_button._set_icon_file_path_(self._icons_0[0])
        self._tab_scroll_previous_button.press_clicked.connect(self._do_scroll_previous_)

        self._tab_scroll_next_button = gui_qt_wgt_button.QtIconPressButton(self)
        self._tab_scroll_next_button.hide()
        self._tab_scroll_next_button._set_icon_geometry_mode_(
            gui_qt_wgt_button.QtIconPressButton.IconGeometryMode.Auto
        )
        self._tab_scroll_next_button.setFixedSize(10, 20)
        self._tab_scroll_next_button._set_icon_file_path_(self._icons_1[0])
        self._tab_scroll_next_button.press_clicked.connect(self._do_scroll_next_)

        self._tab_choose_button = gui_qt_wgt_button.QtIconMenuButton(self)
        self._tab_choose_button.hide()
        self._tab_choose_button._set_icon_file_path_(
            gui_core.GuiIcon.get('tab/tab-choose')
        )

        self._tab_menu_is_enable = False
        self._tab_menu_button = gui_qt_wgt_button.QtIconMenuButton(self)
        self._tab_menu_button.hide()
        self._tab_menu_button._set_icon_file_path_(
            gui_core.GuiIcon.get('tab/tab-menu-v')
        )

        self._tab_view_margins = 2, 2, 2, 2

        self._tab_w, self._tab_h = 48, 24

        self.setFont(
            gui_qt_core.GuiQtFont.generate(size=10)
        )

        self._gui_scroll = gui_qt_core.GuiQtModForScroll()
        self._gui_scroll.set_step(64)
        self._set_menu_data_generate_fnc_(
            self._tab_item_menu_gain_fnc_
        )

        self.__layer_stack = gui_qt_wgt_layer_stack.QtLayerStack(self)
        self.__layer_stack.installEventFilter(self)
        # use layer stack signal
        self.__layer_stack.current_changed.connect(self.current_changed.emit)

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
            if event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                self._clear_item_hover_()
            elif event.type() == QtCore.QEvent.ToolTip:
                self._do_show_tool_tip_(event)
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self._index_press = self._compute_press_index_loc_(
                    event.pos()
                )
                self._press_point = event.pos()
                if event.button() == QtCore.Qt.LeftButton:
                    if self._index_press is not None:
                        self._set_action_flag_(self.ActionFlag.Press)
                        self._set_item_pressed_at_(self._index_press)
                elif event.button() == QtCore.Qt.RightButton:
                    if self._index_press is not None:
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
                        if self._get_action_flag_is_match_(self.ActionFlag.Press):
                            if self._index_press is not None:
                                self._drag_press_point = self._press_point
                                self._set_action_flag_(self.ActionFlag.DragPress)
                        elif self._get_action_flag_is_match_(self.ActionFlag.DragPress):
                            self._do_drag_press_(event)
                        elif self._get_action_flag_is_match_(self.ActionFlag.DragChildPolish):
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
                    if self._get_action_flag_is_match_(self.ActionFlag.Press, self.ActionFlag.DragPress):
                        # send signal in release action
                        self._do_press_release_(event)
                    elif self._get_action_flag_is_match_(self.ActionFlag.DragChildPolish):
                        self._do_drop_(event)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()

                self._index_press = None
                self._index_hover = None
                self._clear_all_action_flags_()
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.Wheel:
                self._do_wheel_(event)
                return True
        elif widget == self.__layer_stack:
            if event.type() == QtCore.QEvent.Enter:
                self._clear_item_hover_()
            if event.type() == QtCore.QEvent.Leave:
                self._clear_item_hover_()
        return False

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)
        painter._draw_tab_buttons_by_rects_(
            self._tab_bar_draw_rect,
            virtual_items=self._tab_item_stack.get_all_items(),
            index_hover=self._index_hover,
            index_pressed=self._index_press,
            index_current=self._get_current_index_(),
        )
        #
        if self._tab_add_is_enable:
            painter._draw_tab_left_tool_box_by_rect_(
                rect=self._tab_left_tool_box_draw_rect
            )
        #
        if self._gui_scroll.get_is_valid():
            painter._draw_tab_right_tool_box_by_rect_(
                rect=self._tab_right_tool_box_draw_rect
            )

    def _delete_widget_at_(self, index):
        item = self._tab_item_stack.get_item_at(index)
        self.__layer_stack._delete_widget_at_(index)
        self.tab_delete_accepted.emit(item.get_key() or item.get_name())
        self._tab_item_stack.delete_item(item)
        self._refresh_widget_all_()

    def _add_widget_(self, widget, *args, **kwargs):
        # widget.setParent(self)
        self.__layer_stack._add_widget_(widget, *args, **kwargs)
        tab_item = self._tab_item_stack.create_item(widget)
        if 'key' in kwargs:
            tab_item.set_key(kwargs['key'])
        if 'name' in kwargs:
            tab_item.set_name(kwargs['name'])
        if 'icon_name_text' in kwargs:
            tab_item.set_icon_text(kwargs['name'])

        self._refresh_widget_all_()

    def _set_tab_add_enable_(self, boolean):
        self._tab_add_is_enable = boolean
        self._refresh_widget_all_()

    def _set_tab_add_menu_data_(self, data):
        self._tab_add_button._set_menu_data_(data)

    def _set_tab_add_menu_gain_fnc_(self, fnc):
        self._tab_add_button._set_menu_data_generate_fnc_(fnc)

    def _set_tab_menu_enable_(self, boolean):
        self._tab_menu_is_enable = boolean
        self._refresh_widget_all_()

    def _set_tab_menu_data_(self, data):
        self._tab_menu_button._set_menu_data_(data)

    def _set_tab_menu_data_generate_fnc_(self, fnc):
        self._tab_menu_button._set_menu_data_generate_fnc_(fnc)

    def _clear_item_hover_(self):
        self._index_hover = None
        self._refresh_widget_draw_()

    def _set_item_pressed_at_(self, index):
        if index != self._item_index_pressed:
            self._item_index_pressed = index

            self._refresh_widget_all_()

    def _set_item_drag_moving_at_(self, index):
        if index != self._item_index_dragged:
            self._item_index_dragged = index

            self._refresh_widget_all_()

    def _switch_current_to_(self, index):
        self._item_index_pressed = None
        self.__layer_stack._switch_current_to_(index)
        self._refresh_widget_all_()

    def _set_current_index_(self, index):
        self._item_index_pressed = None
        self.__layer_stack._set_current_index_(index)
        self._refresh_widget_all_()

    def _get_current_index_(self):
        return self.__layer_stack._get_current_index_()

    def _set_item_current_by_name_text_(self, text):
        index = self._tab_item_stack.get_index_by_name(
            text
        )
        if index is not None:
            self._switch_current_to_(index)

    def _set_item_current_by_key_text_(self, text):
        index = self._tab_item_stack.get_index_by_key(
            text
        )
        if index is not None:
            self._switch_current_to_(index)

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
        if self._index_hover is not None:
            key = self._get_page_key_at_(self._index_hover)
            if key is None:
                title = self._get_page_name_text_at_(self._index_hover)
            else:
                title = key

            css = gui_qt_core.GuiQtUtil.generate_tool_tip_css(
                title,
                [
                    '"LMB-click" to show this page',
                    '"MMB-wheel" to scroll to other page',
                    '"RMB-click" to show more actions for this page',
                ]
            )
            QtWidgets.QToolTip.showText(
                QtGui.QCursor.pos(), css, self
            )

    # noinspection PyUnusedLocal
    def _do_press_release_(self, event):
        if self._index_press is not None:
            self._switch_current_to_(
                self._index_press
            )

    def _do_hover_move_(self, event):
        p = event.pos()
        self._index_hover = None
        if self._tab_bar_rect.contains(p):
            for i_index, i_tab_item in enumerate(self._tab_item_stack.get_all_items()):
                if i_tab_item.rect.contains(p):
                    self._index_hover = i_index
                    break

        self._refresh_widget_draw_()

    def _do_drag_press_(self, event):
        p = event.pos()
        p_d = p-self._drag_press_point
        x, y = p_d.x(), p_d.y()
        # enable when mouse moved more than 10 pixel
        if abs(x) > 10:
            self._index_drag_child_polish_start = self._index_press
            self._index_drag_child_polish = self._index_press
            self._set_action_flag_(self.ActionFlag.DragChildPolish)
            # when drag is not current, set to current first
            if self._index_press != self._get_current_index_():
                self._set_current_index_(self._index_press)

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
        self.__layer_stack._insert_widget_between_(
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

    def _tab_item_menu_gain_fnc_(self):
        if self._index_press is not None:
            return [
                ('close tab', 'cancel', functools.partial(self._delete_widget_at_, self._index_press)),
                ('close other tabs', 'cancel', None)
            ]
        return []

    def _do_scroll_to_(self, index):
        item = self._tab_item_stack.get_item_at(index)
        if item:
            x = item.get_rect().x()
            self._gui_scroll.accept_value(x-24)

    def _do_scroll_previous_(self):
        if self._gui_scroll.step_to_previous():
            self._refresh_widget_all_()

    def _do_scroll_next_(self):
        if self._gui_scroll.step_to_next():
            self._refresh_widget_all_()
