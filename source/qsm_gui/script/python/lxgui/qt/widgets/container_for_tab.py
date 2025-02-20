# coding=utf-8
from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from ...qt import abstracts as _qt_abstracts

from . import utility as _utility

from . import button as _button


class _AbsQtHTabToolBox(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtWidgetBaseDef,
    _qt_abstracts.AbsQtFrameBaseDef,

    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForExpandDef,

    _qt_abstracts.AbsQtHistoryBaseDef,
):
    current_changed = qt_signal()

    QT_ORIENTATION = None

    # scroll
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

    def _check_expand_(self, point):
        if self._expand_frame_rect.contains(point):
            self._expand_hover_flag = True
        else:
            self._expand_hover_flag = False

        self._refresh_widget_draw_()

    # history
    def _load_history_(self):
        self._set_current_key_text_(
            self._get_history_value_()
        )

    def _save_history_(self):
        self._set_history_value_(
            self._get_current_key_text_()
        )

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
        icn_w, icn_h = 16, 16
        btn_w, btn_h = 20, 20
        # horizontal
        if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
            tab_bar_x, tab_bar_y = x, y
            tab_bar_w, tab_bar_h = w, tab_h

            tab_btn_x, tab_btn_y = x, y

            if self._expand_action_is_enable is True:
                tab_bar_x += btn_frm_w
                tab_btn_x += btn_frm_w
                # todo: expand button
                self._expand_frame_rect.setRect(
                    x, y, btn_frm_w, btn_frm_h
                )
                self._expand_icon_draw_rect.setRect(
                    x+(btn_frm_w-icn_w)/2, y+(btn_frm_h-icn_h)/2, icn_w, icn_h
                )

            self._layout.setContentsMargins(
                m_l, m_t+tab_h, m_r, m_b
            )

            self._viewport_rect.setRect(
                m_l, m_t+tab_h, w-(m_l+m_r), h-(m_l+m_r+tab_h)
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
                # update size
                for i_index, i_tab_item in enumerate(tab_items):
                    i_name_text = i_tab_item.get_name()
                    if i_name_text is not None:
                        i_txt_w = QtGui.QFontMetrics(self._tab_text_font).width(i_name_text)
                    else:
                        i_txt_w = tab_w
                    # compute tab width
                    i_tab_w = i_txt_w+8
                    if i_tab_item.icon_text:
                        i_tab_w += 4
                    self._item_width_or_height_dict[i_index] = i_tab_w
                    scroll_abs_w += i_tab_w
                # scroll
                scroll_w = w  # use width
                # update scroll model
                self._scroll_bar_model.set_w_or_h(scroll_w)
                self._scroll_bar_model.set_abs_w_or_h(scroll_abs_w+btn_frm_w*3)
                self._scroll_bar_model.update()

                if self._scroll_bar_model.is_valid():
                    btn_w_1, btn_h_1 = btn_w/2, btn_h
                    btn_f_w_r = btn_frm_w*2
                    c_x_1, c_y_1 = w-btn_f_w_r, y
                    c_x_1 = max(c_x_1, btn_f_w_r)
                    self._tab_scroll_tool_box_rect.setRect(
                        c_x_1, c_y_1, btn_f_w_r, btn_frm_h
                    )
                    self._tab_scroll_tool_box_draw_rect.setRect(
                        c_x_1, c_y_1, btn_f_w_r, btn_frm_h-1
                    )
                    #
                    self._tab_scroll_previous_button.show()
                    self._tab_scroll_previous_button.setGeometry(
                        c_x_1+(btn_frm_w-btn_w)/2, c_y_1+(btn_frm_h-btn_h_1)/2, btn_w_1, btn_h_1
                    )

                    if self._scroll_bar_model.get_is_minimum():
                        self._tab_scroll_previous_button._set_icon_file_path_(self._icons_0[1])
                    else:
                        self._tab_scroll_previous_button._set_icon_file_path_(self._icons_0[0])

                    self._tab_scroll_next_button.show()
                    self._tab_scroll_next_button.setGeometry(
                        c_x_1+(btn_frm_w-btn_w)/2+btn_w_1, c_y_1+(btn_frm_h-btn_h_1)/2, btn_w_1, btn_h_1
                    )

                    if self._scroll_bar_model.get_is_maximum():
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
                scroll_value = self._scroll_bar_model.get_value()
                widths = list(self._item_width_or_height_dict.values())
                for i_index, i_tab_item in enumerate(tab_items):
                    i_x = sum(widths[:i_index])
                    i_w = self._item_width_or_height_dict[i_index]

                    i_tab_item.get_rect().setRect(
                        tab_btn_x+i_x-scroll_value, tab_btn_y, i_w, tab_h
                    )
                    i_tab_item.get_draw_rect().setRect(
                        tab_btn_x+i_x-scroll_value, tab_btn_y, i_w, tab_h
                    )

                    i_widget = i_tab_item.get_widget()
                    if i_index == self._current_index:
                        i_widget.show()
                    else:
                        i_widget.hide()
        # vertical
        elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
            tab_bar_x, tab_bar_y = x, y
            tab_bar_w, tab_bar_h = tab_w, h

            tab_btn_x, tab_btn_y = x, y

            if self._direction == _gui_core.GuiDirections.LeftToRight:
                self._layout.setContentsMargins(
                    m_l+tab_w, m_t, m_r, m_b
                )
                self._viewport_rect.setRect(
                    m_l+tab_w, m_t, w-(m_l+m_r+tab_w), h-(m_l+m_r)
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
                self._viewport_rect.setRect(
                    m_l, m_t, w-(m_l+m_r+tab_w), h-(m_l+m_r)
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
                # update size
                for i_index, i_tab_item in enumerate(tab_items):
                    i_name_text = i_tab_item.get_name()
                    if i_name_text is not None:
                        i_txt_w = QtGui.QFontMetrics(self._tab_text_font).width(i_name_text)
                    else:
                        i_txt_w = tab_w
                    # compute tab width
                    i_tab_w = i_txt_w+8
                    if i_tab_item.icon_text:
                        i_tab_w += 4
                    self._item_width_or_height_dict[i_index] = i_tab_w
                    scroll_abs_w += i_tab_w
                # scroll
                scroll_w = h  # use height
                # update scroll model
                self._scroll_bar_model.set_w_or_h(scroll_w)
                self._scroll_bar_model.set_abs_w_or_h(scroll_abs_w+btn_frm_w*3)
                self._scroll_bar_model.update()

                if self._scroll_bar_model.is_valid():
                    btn_w_1, btn_h_1 = btn_w, btn_h/2
                    btn_f_w_r = btn_frm_w*2
                    c_x_1, c_y_1 = w-btn_frm_w, h-btn_f_w_r
                    c_x_1 = max(c_x_1, btn_f_w_r)
                    self._tab_scroll_tool_box_rect.setRect(
                        c_x_1, c_y_1, btn_f_w_r, btn_frm_h
                    )
                    self._tab_scroll_tool_box_draw_rect.setRect(
                        c_x_1, c_y_1, btn_frm_w-1, btn_f_w_r
                    )
                    #
                    self._tab_scroll_previous_button.show()
                    self._tab_scroll_previous_button.setGeometry(
                        c_x_1+(btn_frm_w-btn_w)/2, c_y_1+(btn_frm_h-btn_h_1)/2, btn_w_1, btn_h_1
                    )

                    if self._scroll_bar_model.get_is_minimum():
                        self._tab_scroll_previous_button._set_icon_file_path_(self._icons_0[1])
                    else:
                        self._tab_scroll_previous_button._set_icon_file_path_(self._icons_0[0])

                    self._tab_scroll_next_button.show()
                    self._tab_scroll_next_button.setGeometry(
                        c_x_1+(btn_frm_w-btn_w)/2, c_y_1+(btn_frm_h-btn_h_1)/2+btn_h_1, btn_w_1, btn_h_1
                    )

                    if self._scroll_bar_model.get_is_maximum():
                        self._tab_scroll_next_button._set_icon_file_path_(self._icons_1[1])
                    else:
                        self._tab_scroll_next_button._set_icon_file_path_(self._icons_1[0])

                    self._tab_choose_button.show()
                    self._tab_choose_button.setGeometry(
                        c_x_1+(btn_frm_w-btn_w)/2, c_y_1+btn_frm_w+(btn_frm_h-btn_h)/2, btn_w, btn_h
                    )

                    tab_bar_w -= btn_f_w_r
                else:
                    self._tab_scroll_previous_button.hide()
                    self._tab_scroll_next_button.hide()
                    self._tab_choose_button.hide()
                # tab items
                scroll_value = self._scroll_bar_model.get_value()
                heights = list(self._item_width_or_height_dict.values())
                for i_index, i_tab_item in enumerate(tab_items):
                    i_y = sum(heights[:i_index])
                    i_h = self._item_width_or_height_dict[i_index]
                    if self._direction == _gui_core.GuiDirections.LeftToRight:
                        i_tab_item.get_rect().setRect(
                            tab_btn_x, tab_btn_y+i_y-scroll_value, tab_w, i_h
                        )
                        i_tab_item.get_draw_rect().setRect(
                            tab_btn_x, tab_btn_y+i_y-scroll_value, tab_w, i_h
                        )
                    elif self._direction == _gui_core.GuiDirections.RightToLeft:
                        i_tab_item.get_rect().setRect(
                            w-tab_w, tab_btn_y+i_y-scroll_value, tab_w, i_h
                        )
                        i_tab_item.get_draw_rect().setRect(
                            w-tab_w, tab_btn_y+i_y - scroll_value, tab_w, i_h
                        )
                    else:
                        raise RuntimeError()
                    
                    i_widget = i_tab_item.get_widget()
                    if i_index == self._current_index:
                        i_widget.show()
                    else:
                        i_widget.hide()
    
    def _refresh_viewport_widget_(self, fix_size=False):
        # fixme: toolbar resize bug?
        x, y = self._viewport_rect.x(), self._viewport_rect.y()
        w, h = self._viewport_rect.width(), self._viewport_rect.height()
        if fix_size is True:
            self._viewport_widget.setGeometry(x, y, w-2, h-2)
        self._viewport_widget.setGeometry(x, y, w, h)

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
        self._init_action_for_expand_def_(self)
        # set default to True
        self._is_expanded = True
        self._expand_icon_file_path_0 = _gui_core.GuiIcon.get('tool/hide')
        self._expand_icon_file_path_1 = _gui_core.GuiIcon.get('tool/show')
        self._update_expand_icon_file_()

        self._init_history_base_def_(self)

        self._tab_item_stack = _qt_core.GuiQtModForTabItemStack(self)

        self._tab_view_margins = 2, 2, 2, 2
        self._tab_w, self._tab_h = 24, 24

        self._tab_text_font = _qt_core.QtFont.generate(size=11, weight=75)

        self._tab_bar_rect = qt_rect()
        self._tab_bar_draw_rect = qt_rect()

        self._tab_scroll_tool_box_rect = qt_rect()
        self._tab_scroll_tool_box_draw_rect = qt_rect()
        
        self._icons_0 = [
            _gui_core.GuiIcon.get('window_base/scroll-left'),
            _gui_core.GuiIcon.get('window_base/scroll-left-disable')
        ]
        self._icons_1 = [
            _gui_core.GuiIcon.get('window_base/scroll-right'),
            _gui_core.GuiIcon.get('window_base/scroll-right-disable')
        ]

        self._tab_scroll_previous_button = _button.QtIconPressButton(self)
        self._tab_scroll_previous_button.hide()
        self._tab_scroll_previous_button._set_icon_geometry_mode_(
            _button.QtIconPressButton.IconGeometryMode.Auto
        )
        self._tab_scroll_previous_button.setFixedSize(10, 20)
        self._tab_scroll_previous_button._set_icon_file_path_(self._icons_0[0])
        self._tab_scroll_previous_button.press_clicked.connect(self._do_scroll_previous_)

        self._tab_scroll_next_button = _button.QtIconPressButton(self)
        self._tab_scroll_next_button.hide()
        self._tab_scroll_next_button._set_icon_geometry_mode_(
            _button.QtIconPressButton.IconGeometryMode.Auto
        )
        self._tab_scroll_next_button.setFixedSize(10, 20)
        self._tab_scroll_next_button._set_icon_file_path_(self._icons_1[0])
        self._tab_scroll_next_button.press_clicked.connect(self._do_scroll_next_)

        self._tab_choose_button = _button.QtIconMenuButton(self)
        self._tab_choose_button.hide()
        self._tab_choose_button._set_icon_file_path_(
            _gui_core.GuiIcon.get('tab/tab-choose')
        )

        self._scroll_bar_model = _qt_core.GuiQtModForScroll()
        self._scroll_bar_model.set_step(64)

        self._item_width_or_height_dict = {}

        self._current_index = 0

        self._index_press_tmp = None
        self._index_press = None
        self._hover_tab_index = None

        self._direction = _gui_core.GuiDirections.TopToBottom

        self._layout = _qt_core.QtVBoxLayout(self)

        self._viewport_widget = _utility.QtWidget()
        self._layout.addWidget(self._viewport_widget)

        self._viewport_widget.installEventFilter(self)
        self._viewport_layout = _qt_core.QtVBoxLayout(self._viewport_widget)
        self._viewport_layout.setContentsMargins(*[0]*4)
        self._viewport_layout.setSpacing(0)

        self._viewport_rect = qt_rect()

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                self._do_leave_()
            elif event.type() == QtCore.QEvent.ToolTip:
                self._do_show_tool_tip_(event)
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
                self._refresh_viewport_widget_(fix_size=False)
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self._index_press_tmp = self._compute_press_index_loc_(
                    event.pos()
                )
                if event.button() == QtCore.Qt.LeftButton:
                    if self._index_press_tmp is not None:
                        self._set_action_flag_(self.ActionFlag.Press)
                        self._on_tab_button_press_(self._index_press_tmp)
                    else:
                        if self._expand_hover_flag is True:
                            self._set_action_flag_(self.ActionFlag.Press)
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
                    if self._is_action_flag_match_(self.ActionFlag.Press):
                        # send signal in release action
                        self._do_mouse_press_release_(event)
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
        elif widget == self._viewport_widget:
            if event.type() == QtCore.QEvent.Enter:
                self._do_leave_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        painter._draw_virtual_tab_buttons_(
            bar_rect=self._tab_bar_draw_rect,
            virtual_items=self._tab_item_stack.get_all_items(),
            index_hover=self._hover_tab_index,
            index_pressed=self._index_press,
            index_current=self._get_current_index_(),
            orientation=self.QT_ORIENTATION,
            direction=self._direction
        )

        if self._scroll_bar_model.is_valid():
            painter._draw_tab_right_tool_box_by_rect_(
                rect=self._tab_scroll_tool_box_draw_rect,
                background_color=_qt_core.QtRgba.Basic
            )

        if self._expand_action_is_enable is True:
            painter._draw_icon_file_by_rect_(
                rect=self._expand_icon_draw_rect,
                file_path=self._expand_icon_file_path_current,
                is_hovered=self._expand_hover_flag
            )

    def _add_widget_(self, widget, *args, **kwargs):
        self._viewport_layout.addWidget(widget)
        item = self._tab_item_stack.create_item(widget)
        if 'key' in kwargs:
            item.set_key(kwargs['key'])
        if 'name' in kwargs:
            item.set_name(kwargs['name'])
        if 'icon_name_text' in kwargs:
            item.set_icon_text(kwargs['icon_name_text'])
        if 'tool_tip' in kwargs:
            item.set_tool_tip(kwargs['tool_tip'])

        self._refresh_widget_all_()

    def _update_index_current_(self, index):
        if index != self._current_index:
            self._current_index = index
            self.current_changed.emit()
            self._refresh_widget_all_()
            self._refresh_viewport_widget_(fix_size=True)

            self._save_history_()

    def _get_current_index_(self):
        return self._current_index
    
    def _on_tab_button_press_(self, index):
        if index != self._index_press:
            self._index_press = index
            self._refresh_widget_all_()

    def _do_mouse_press_release_(self, event):
        if self._index_press_tmp is not None:
            self._switch_current_to_(
                self._index_press_tmp
            )
        else:
            if self._expand_hover_flag is True:
                self._execute_action_expand_()
                self._expand_hover_flag = False

    def _refresh_expand_(self):
        self._update_expand_icon_file_()
        if self._is_expanded is True:
            self._viewport_widget.show()
        else:
            self._viewport_widget.hide()

        self._refresh_widget_draw_()
    
    def _switch_current_to_(self, index):
        self._update_index_current_(index)
        self._index_press = None
        self._refresh_widget_all_()

    def _do_leave_(self):
        self._hover_tab_index = None

        self._expand_hover_flag = False

        self._refresh_widget_draw_()

    def _do_show_tool_tip_(self, event):
        if self._tab_bar_rect.contains(event.pos()):
            if self._hover_tab_index is not None:
                key = self._tab_item_stack.get_key_at(self._hover_tab_index)
                if key is None:
                    title = self._tab_item_stack.get_name_at(self._hover_tab_index)
                    tool_tip = self._tab_item_stack.get_tool_tip_at(self._hover_tab_index)
                else:
                    title = self._tab_item_stack.get_name_at(self._hover_tab_index)
                    tool_tip = self._tab_item_stack.get_tool_tip_at(self._hover_tab_index)

                css = _qt_core.QtUtil.generate_tool_tip_css(
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
        self._hover_tab_index = None
        self._expand_hover_flag = False

        if self._tab_bar_rect.contains(p):
            for i_index, i_tab_item in enumerate(self._tab_item_stack.get_all_items()):
                if i_tab_item.rect.contains(p):
                    self._hover_tab_index = i_index
                    break
        elif self._expand_frame_rect.contains(p):
            self._expand_hover_flag = True

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
            return True
        return False

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
        self._icons_0 = [
            _gui_core.GuiIcon.get('window_base/scroll-up'),
            _gui_core.GuiIcon.get('window_base/scroll-up-disable')
        ]
        self._icons_1 = [
            _gui_core.GuiIcon.get('window_base/scroll-down'),
            _gui_core.GuiIcon.get('window_base/scroll-down-disable')
        ]
        self._direction = _gui_core.GuiDirections.LeftToRight
        
        self._tab_scroll_previous_button.setFixedSize(20, 10)
        self._tab_scroll_next_button.setFixedSize(20, 10)
