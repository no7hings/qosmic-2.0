# coding=utf-8
from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from ...qt import abstracts as _qt_abstracts

from . import button as _qt_wgt_button


class _AbsQtHTabToolBox(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtWidgetBaseDef,
    _qt_abstracts.AbsQtFrameBaseDef,

    _qt_abstracts.AbsQtActionBaseDef,

    _qt_abstracts.AbsQtHistoryBaseDef,
):
    current_changed = qt_signal()

    QT_ORIENTATION = None

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_(self.rect())
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self, rect):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        self._frame_rect.setRect(
            x, y, w, h
        )
        m_l, m_t, m_r, m_b = self._tab_view_margins
        tab_w, tab_h = self._tab_w, self._tab_h
        btn_frm_w, btn_frm_h = tab_h, tab_h
        btn_w, btn_h = 20, 20
        if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
            tab_bar_x, tab_bar_y = x, y
            tab_bar_w, tab_bar_h = w, tab_h

            self._layout.setContentsMargins(
                m_l, m_t+tab_h, m_r, m_b
            )
            self._tab_bar_draw_rect.setRect(
                tab_bar_x, tab_bar_y, tab_bar_w, tab_bar_h-1
            )
            self._tab_bar_rect.setRect(
                tab_bar_x, tab_bar_y, tab_bar_w, tab_bar_h
            )

            scroll_abs_w = 0
            tab_items = self._tab_item_stack.get_all_items()
            if tab_items:
                for i_index, i_tab_item in enumerate(tab_items):
                    i_name_text = i_tab_item.get_name()
                    if i_name_text is not None:
                        i_text_width = QtGui.QFontMetrics(self._tab_text_font).width(i_name_text)
                    else:
                        i_text_width = tab_w
                    # compute tab width
                    i_t_w = i_text_width+16
                    if i_tab_item.icon_text:
                        i_t_w += 10
                    self._item_width_or_height_dict[i_index] = i_t_w
                    scroll_abs_w += i_t_w
                # scroll
                scroll_w = w  # use width
                # update scroll model
                self._gui_scroll.set_w_or_h(scroll_w)
                self._gui_scroll.set_abs_w_or_h(scroll_abs_w+btn_frm_w*3)
                self._gui_scroll.update()

                if self._gui_scroll.get_is_valid():
                    btn_w_1, btn_h_1 = btn_w/2, btn_h
                    btn_f_w_r = btn_frm_w*2
                    c_x_1, c_y_1 = w-btn_f_w_r, y
                    c_x_1 = max(c_x_1, btn_f_w_r)
                    self._tab_right_tool_box_rect.setRect(
                        c_x_1, c_y_1, btn_f_w_r, btn_frm_h
                    )
                    self._tab_right_tool_box_draw_rect.setRect(
                        c_x_1, c_y_1, btn_f_w_r, btn_frm_h-1
                    )
                    #
                    self._tab_scroll_previous_button.show()
                    self._tab_scroll_previous_button.setGeometry(
                        c_x_1+(btn_frm_w-btn_w)/2, c_y_1+(btn_frm_h-btn_h_1)/2, btn_w_1, btn_h_1
                    )

                    if self._gui_scroll.get_is_minimum():
                        self._tab_scroll_previous_button._set_icon_file_path_(self._icons_0[1])
                    else:
                        self._tab_scroll_previous_button._set_icon_file_path_(self._icons_0[0])

                    self._tab_scroll_next_button.show()
                    self._tab_scroll_next_button.setGeometry(
                        c_x_1+(btn_frm_w-btn_w)/2+btn_w_1, c_y_1+(btn_frm_h-btn_h_1)/2, btn_w_1, btn_h_1
                    )

                    if self._gui_scroll.get_is_maximum():
                        self._tab_scroll_next_button._set_icon_file_path_(self._icons_1[1])
                    else:
                        self._tab_scroll_next_button._set_icon_file_path_(self._icons_1[0])

                    self._tab_choose_button.show()
                    self._tab_choose_button.setGeometry(
                        c_x_1+btn_frm_w+(btn_frm_w-btn_w)/2, c_y_1+(btn_frm_h-btn_h)/2, btn_w, btn_h
                    )

                    tab_bar_w -= btn_f_w_r
                else:
                    self._tab_scroll_previous_button.hide()
                    self._tab_scroll_next_button.hide()
                    self._tab_choose_button.hide()
                # tab items
                c_x, c_y = x, y
                scroll_value = self._gui_scroll.get_value()
                widths = self._item_width_or_height_dict.values()
                for i_index, i_tab_item in enumerate(tab_items):
                    i_x = sum(widths[:i_index])
                    i_w = self._item_width_or_height_dict[i_index]

                    i_tab_item.get_rect().setRect(
                        c_x+i_x-scroll_value, c_y, i_w, tab_h
                    )
                    i_tab_item.get_draw_rect().setRect(
                        c_x+i_x-scroll_value, c_y, i_w, tab_h
                    )
                    
                    i_widget = i_tab_item.get_widget()
                    if i_index == self._index_current:
                        i_widget.show()
                    else:
                        i_widget.hide()
        elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
            tab_bar_x, tab_bar_y = x, y
            tab_bar_w, tab_bar_h = tab_w, h

            if self._direction == _gui_core.GuiDirections.LeftToRight:
                self._layout.setContentsMargins(
                    m_l+tab_w, m_t, m_r, m_b
                )
                self._tab_bar_draw_rect.setRect(
                    tab_bar_x, tab_bar_y, tab_bar_w-1, tab_bar_h
                )
                self._tab_bar_rect.setRect(
                    tab_bar_x, tab_bar_y, tab_bar_w, tab_bar_h
                )
            elif self._direction == _gui_core.GuiDirections.RightToLeft:
                self._layout.setContentsMargins(
                    m_l, m_t, m_r+tab_w, m_b
                )
                self._tab_bar_draw_rect.setRect(
                    w-tab_bar_w, tab_bar_y, tab_bar_w-1, tab_bar_h
                )
                self._tab_bar_rect.setRect(
                    w-tab_bar_w, tab_bar_y, tab_bar_w, tab_bar_h
                )
            else:
                raise RuntimeError()

            scroll_abs_w = 0
            tab_items = self._tab_item_stack.get_all_items()
            if tab_items:
                for i_index, i_tab_item in enumerate(tab_items):
                    i_name_text = i_tab_item.get_name()
                    if i_name_text is not None:
                        i_text_width = QtGui.QFontMetrics(self._tab_text_font).width(i_name_text)
                    else:
                        i_text_width = tab_w
                    # compute tab width
                    i_t_w = i_text_width+16
                    if i_tab_item.icon_text:
                        i_t_w += 10
                    self._item_width_or_height_dict[i_index] = i_t_w
                    scroll_abs_w += i_t_w
                # scroll
                scroll_w = h  # use height
                # update scroll model
                self._gui_scroll.set_w_or_h(scroll_w)
                self._gui_scroll.set_abs_w_or_h(scroll_abs_w+btn_frm_w*3)
                self._gui_scroll.update()

                if self._gui_scroll.get_is_valid():
                    btn_w_1, btn_h_1 = btn_w/2, btn_h
                    btn_f_w_r = btn_frm_w*2
                    c_x_1, c_y_1 = w-btn_f_w_r, y
                    c_x_1 = max(c_x_1, btn_f_w_r)
                    self._tab_right_tool_box_rect.setRect(
                        c_x_1, c_y_1, btn_f_w_r, btn_frm_h
                    )
                    self._tab_right_tool_box_draw_rect.setRect(
                        c_x_1, c_y_1, btn_f_w_r, btn_frm_h-1
                    )
                    #
                    self._tab_scroll_previous_button.show()
                    self._tab_scroll_previous_button.setGeometry(
                        c_x_1+(btn_frm_w-btn_w)/2, c_y_1+(btn_frm_h-btn_h_1)/2, btn_w_1, btn_h_1
                    )

                    if self._gui_scroll.get_is_minimum():
                        self._tab_scroll_previous_button._set_icon_file_path_(self._icons_0[1])
                    else:
                        self._tab_scroll_previous_button._set_icon_file_path_(self._icons_0[0])

                    self._tab_scroll_next_button.show()
                    self._tab_scroll_next_button.setGeometry(
                        c_x_1+(btn_frm_w-btn_w)/2+btn_w_1, c_y_1+(btn_frm_h-btn_h_1)/2, btn_w_1, btn_h_1
                    )

                    if self._gui_scroll.get_is_maximum():
                        self._tab_scroll_next_button._set_icon_file_path_(self._icons_1[1])
                    else:
                        self._tab_scroll_next_button._set_icon_file_path_(self._icons_1[0])

                    self._tab_choose_button.show()
                    self._tab_choose_button.setGeometry(
                        c_x_1+btn_frm_w+(btn_frm_w-btn_w)/2, c_y_1+(btn_frm_h-btn_h)/2, btn_w, btn_h
                    )

                    tab_bar_w -= btn_f_w_r
                else:
                    self._tab_scroll_previous_button.hide()
                    self._tab_scroll_next_button.hide()
                    self._tab_choose_button.hide()
                # tab items
                c_x, c_y = x, y
                scroll_value = self._gui_scroll.get_value()
                heights = self._item_width_or_height_dict.values()
                for i_index, i_tab_item in enumerate(tab_items):
                    i_y = sum(heights[:i_index])
                    i_h = self._item_width_or_height_dict[i_index]
                    if self._direction == _gui_core.GuiDirections.LeftToRight:
                        i_tab_item.get_rect().setRect(
                            c_x, c_y+i_y-scroll_value, tab_w, i_h
                        )
                        i_tab_item.get_draw_rect().setRect(
                            c_x, c_y+i_y-scroll_value, tab_w, i_h
                        )
                    elif self._direction == _gui_core.GuiDirections.RightToLeft:
                        i_tab_item.get_rect().setRect(
                            w-tab_w, c_y+i_y-scroll_value, tab_w, i_h
                        )
                        i_tab_item.get_draw_rect().setRect(
                            w-tab_w, c_y+i_y - scroll_value, tab_w, i_h
                        )
                    else:
                        raise RuntimeError()
                    
                    i_widget = i_tab_item.get_widget()
                    if i_index == self._index_current:
                        i_widget.show()
                    else:
                        i_widget.hide()

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

    def _load_history_(self):
        self._set_current_key_text_(
            self._get_history_value_()
        )

    def _save_history_(self):
        self._set_history_value_(
            self._get_current_key_text_()
        )

    def __init__(self, *args, **kwargs):
        super(_AbsQtHTabToolBox, self).__init__(*args, **kwargs)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
            self.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
            )
        elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
            self.setSizePolicy(
                QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
            )

        self._init_widget_base_def_(self)
        self._init_frame_base_def_(self)

        self._init_action_base_def_(self)

        self._init_history_base_def_(self)

        self._tab_item_stack = _qt_core.GuiQtModForTabItemStack(self)

        self._tab_view_margins = 2, 2, 2, 2
        self._tab_w, self._tab_h = 24, 24

        self._tab_text_font = _qt_core.QtFont.generate(size=10, weight=75)

        self._tab_bar_rect = QtCore.QRect()
        self._tab_bar_draw_rect = QtCore.QRect()

        self._tab_right_tool_box_rect = QtCore.QRect()
        self._tab_right_tool_box_draw_rect = QtCore.QRect()
        
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

        self._gui_scroll = _qt_core.GuiQtModForScroll()
        self._gui_scroll.set_step(64)

        self._item_width_or_height_dict = {}

        self._index_current = 0

        self._index_press_tmp = None
        self._index_press = None
        self._index_hover = None

        self._direction = _gui_core.GuiDirections.TopToBottom

        self._layout = _qt_core.QtHBoxLayout(self)

        self.installEventFilter(self)

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
                self._index_press_tmp = self._compute_press_index_loc_(
                    event.pos()
                )
                if event.button() == QtCore.Qt.LeftButton:
                    if self._index_press_tmp is not None:
                        self._set_action_flag_(self.ActionFlag.Press)
                        self._update_item_index_pressed_(self._index_press_tmp)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.button() == QtCore.Qt.NoButton:
                    self._do_hover_move_(event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    # when drag press move less than 10px, do press release also
                    if self._get_action_flag_is_match_(self.ActionFlag.Press):
                        # send signal in release action
                        self._do_mouse_press_release_(event)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()

                self._index_press_tmp = None
                self._index_hover = None
                self._clear_all_action_flags_()
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.Wheel:
                self._do_wheel_(event)
                return True
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        painter._draw_virtual_buttons_(
            bar_rect=self._tab_bar_draw_rect,
            virtual_items=self._tab_item_stack.get_all_items(),
            index_hover=self._index_hover,
            index_pressed=self._index_press,
            index_current=self._get_current_index_(),
            orientation=self.QT_ORIENTATION,
            direction=self._direction
        )

        if self._gui_scroll.get_is_valid():
            painter._draw_tab_right_tool_box_by_rect_(
                rect=self._tab_right_tool_box_draw_rect,
                background_color=_qt_core.QtBackgroundColors.Basic
            )

    def _add_widget_(self, widget, *args, **kwargs):
        # widget.setParent(self)
        # widget.setParent(self)
        self._layout.addWidget(widget)
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

    def _update_index_current_(self, index):
        if index != self._index_current:
            self._index_current = index
            self.current_changed.emit()
            self._refresh_widget_all_()

    def _get_current_index_(self):
        return self._index_current
    
    def _update_item_index_pressed_(self, index):

        if index != self._index_press:
            self._index_press = index

            self._refresh_widget_all_()
    
    def _do_mouse_press_release_(self, event):
        if self._index_press_tmp is not None:
            self._switch_current_to_(
                self._index_press_tmp
            )
    
    def _switch_current_to_(self, index):
        self._update_index_current_(index)
        self._index_press = None
        self._refresh_widget_all_()

    def _clear_item_hover_(self):
        self._index_hover = None
        self._refresh_widget_draw_()

    def _do_show_tool_tip_(self, event):
        if self._index_hover is not None:
            key = self._tab_item_stack.get_key_at(self._index_hover)
            if key is None:
                title = self._tab_item_stack.get_name_at(self._index_hover)
                tool_tip = self._tab_item_stack.get_tool_tip_at(self._index_hover)
            else:
                title = self._tab_item_stack.get_name_at(self._index_hover)
                tool_tip = self._tab_item_stack.get_tool_tip_at(self._index_hover)

            css = _qt_core.GuiQtUtil.generate_tool_tip_css(
                title,
                content=tool_tip,
                action_tip=[
                    '"LMB-click" to show this page',
                    '"MMB-wheel" to scroll to other page',
                    '"RMB-click" to show more actions for this page',
                ]
            )
            # noinspection PyArgumentList
            QtWidgets.QToolTip.showText(
                QtGui.QCursor.pos(), css, self
            )

    def _compute_press_index_loc_(self, p):
        if self._tab_bar_rect.contains(p):
            for i_index, i_tab_item in enumerate(self._tab_item_stack.get_all_items()):
                if i_tab_item.get_rect().contains(p):
                    return i_index

    def _do_hover_move_(self, event):
        p = event.pos()
        self._index_hover = None
        if self._tab_bar_rect.contains(p):
            for i_index, i_tab_item in enumerate(self._tab_item_stack.get_all_items()):
                if i_tab_item.rect.contains(p):
                    self._index_hover = i_index
                    break

        self._refresh_widget_draw_()

    def _do_wheel_(self, event):
        pass

    def _get_current_name_text_(self):
        return self._tab_item_stack.get_name_at(
            self._get_current_index_()
        )

    def _set_current_name_text_(self, text):
        index = self._tab_item_stack.get_index_by_name(
            text
        )
        if index is not None:
            self._switch_current_to_(index)

    def _get_current_key_text_(self):
        return self._tab_item_stack.get_key_at(
            self._get_current_index_()
        )

    def _set_current_key_text_(self, text):
        index = self._tab_item_stack.get_index_by_key(
            text
        )
        if index is not None:
            self._switch_current_to_(index)

    def _set_tab_direction_(self, direction):
        self._direction = direction


class QtHTabToolBox(
    _AbsQtHTabToolBox
):

    QT_ORIENTATION = QtCore.Qt.Horizontal

    def __init__(self, *args, **kwargs):
        super(QtHTabToolBox, self).__init__(*args, **kwargs)
        self._direction = _gui_core.GuiDirections.TopToBottom


class QtVTabToolBox(
    _AbsQtHTabToolBox
):
    QT_ORIENTATION = QtCore.Qt.Vertical

    def __init__(self, *args, **kwargs):
        super(QtVTabToolBox, self).__init__(*args, **kwargs)
        self._direction = _gui_core.GuiDirections.LeftToRight
