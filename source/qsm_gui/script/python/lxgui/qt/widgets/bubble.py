# coding=utf-8
import sys

import re

import lxbasic.core as bsc_core

import lxbasic.pinyin as bsc_pinyin
# gui
from ... import core as _gui_core
# qt
from ...qt.core.wrap import *
# qt process
from ...qt import core as _qt_core
# qt abstracts
from ...qt import abstracts as _qt_abstracts
# qt widgets
from . import base as _base


class QtTextBubble(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForPressDef,
):
    delete_text_accepted = qt_signal(str)

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        if self._text:
            x, y = 0, 0
            w, h = self.width(), self.height()
            dlt_w, dlt_h = h, h

            spc = 2

            txt_w, txt_h = QtGui.QFontMetrics(self._text_font).width(self._text)+16, h
            self._frame_border_radius = 2
            # fit to max size
            txt_w = min(txt_w, self._text_w_maximum)
            wgt_w = txt_w+dlt_w
            self.setFixedWidth(wgt_w)

            dlt_icon_w, dlt_icon_h = self._delete_icon_size

            self._frame_draw_rect.setRect(
                x+1, y+1, wgt_w-2, h-2
            )
            self._text_draw_rect.setRect(
                x, y, txt_w, h
            )

            self._delete_frame_rect.setRect(
                x+txt_w, y, dlt_w, dlt_h
            )
            self._delete_draw_rect.setRect(
                x+txt_w+(dlt_w-dlt_icon_w)/2, y+(dlt_h-dlt_icon_h)/2, dlt_icon_w, dlt_icon_h
            )

    def __init__(self, *args, **kwargs):
        super(QtTextBubble, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
        )
        self.setMouseTracking(True)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)

        self._frame_draw_rect = QtCore.QRect()

        self._is_hovered = False
        self._delete_is_hovered = False

        self._text_w, self._text_h = 0, 16
        self._text_w_maximum = 64
        self._side_w = 2
        self._text_spacing = 2
        self._text = None
        self._text_font = _qt_core.QtFont.generate(size=8)
        self.setFont(self._text_font)
        self._text_draw_rect = QtCore.QRect()
        self._delete_frame_rect = QtCore.QRect()
        self._delete_draw_rect = QtCore.QRect()
        self._delete_icon_size = 8, 8
        self._delete_icon_file_path_0 = _gui_core.GuiIcon.get('close')
        self._delete_icon_file_path_1 = _gui_core.GuiIcon.get('close-hover')
        
        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if not hasattr(event, 'type'):
                return False
            if event.type() == QtCore.QEvent.Close:
                self.delete_text_accepted.emit(self._get_text_())
            #
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            #
            elif event.type() == QtCore.QEvent.Enter:
                self._is_hovered = True
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.Leave:
                self._is_hovered = False
                self._delete_is_hovered = False
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseMove:
                self._do_hover_move_(event)
            #
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.Press)
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    pass
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._delete_is_hovered is True:
                        self.close()
                        self.deleteLater()
                #
                self._clear_all_action_flags_()
                #
                self._is_hovered = False
                self._refresh_widget_draw_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        if self._text is not None:
            offset = self._get_action_offset_()
            painter._draw_frame_by_rect_(
                rect=self._frame_draw_rect,
                border_color=_qt_core.QtRgba.Transparent,
                background_color=[_qt_core.QtRgba.BkgBubble, _qt_core.QtRgba.BkgBubbleHover][self._is_hovered],
                border_radius=self._frame_border_radius,
                offset=offset
            )
            painter._draw_text_by_rect_(
                rect=self._text_draw_rect,
                text=self._text,
                text_color=_qt_core.QtRgba.TxtBubble,
                font=self._text_font,
                text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                offset=offset
            )

            painter._draw_icon_file_by_rect_(
                rect=self._delete_draw_rect,
                file_path=[self._delete_icon_file_path_0, self._delete_icon_file_path_1][
                    self._delete_is_hovered],
                offset=offset
            )

    def _set_text_(self, text):
        self._text = text
        self.setToolTip(self._text)
        self._refresh_widget_all_()

    def _get_text_(self):
        return self._text

    def _do_hover_move_(self, event):
        p = event.pos()
        if self._delete_frame_rect.contains(p):
            self._delete_is_hovered = True
        else:
            self._delete_is_hovered = False
        #
        self._refresh_widget_draw_()


class QtInfoBubble(
    QtWidgets.QWidget,
):
    class SizeMode:
        Auto = 0x00
        Fixed = 0x01

    class Style:
        Default = 0x00
        Frame = 0x01

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        if self._text:
            x, y = 0, 0
            w, h = self.width(), self.height()

            self.setFont(_qt_core.QtFont.generate_2(size=h*self._text_draw_percent))

            txt_w, txt_h = self.fontMetrics().width(self._text)+16, self.fontMetrics().height()/2
            s_t = (h-txt_h)/2

            self._frame_border_radius = 2

            w_c = txt_w+s_t*2

            if self._size_mode == self.SizeMode.Auto:
                self.setFixedWidth(w_c)
                self._frame_draw_rect.setRect(
                    x+1, y+1, w_c-1, h-1
                )
            else:
                self._frame_draw_rect.setRect(
                    x+1, y+1, w-1, h-1
                )

            x_0, y_0 = 0, 0
            w_0, h_0 = self.width(), self.height()
            w_f, h_f = w_0, h_0
            self._text_draw_rect.setRect(
                x_0, y_0, w_f, h_f
            )

    def __init__(self, *args, **kwargs):
        super(QtInfoBubble, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
        )

        self._style = self.Style.Default

        self._text = None
        self._text_font = _qt_core.QtFont.generate(size=8)
        self.setFont(self._text_font)
        self._text_draw_rect = QtCore.QRect()

        self._frame_draw_rect = QtCore.QRect()

        self._text_draw_percent = 0.5

        self._size_mode = self.SizeMode.Auto

        self._frame_border_radius = 0

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()

        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        if self._text:
            if self._style == self.Style.Default:
                painter._draw_text_by_rect_(
                    rect=self._text_draw_rect,
                    text=self._text,
                    text_color=_qt_core.QtRgba.TxtTemporary,
                    font=self._text_font,
                    text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                )
            elif self._style == self.Style.Frame:
                painter._draw_frame_by_rect_(
                    rect=self._frame_draw_rect,
                    border_color=_qt_core.QtRgba.Transparent,
                    background_color=_qt_core.QtRgba.BkgBubble,
                    border_radius=self._frame_border_radius,
                )
                painter._draw_text_by_rect_(
                    rect=self._text_draw_rect,
                    text=self._text,
                    text_color=_qt_core.QtRgba.TxtBubble,
                    font=self._text_font,
                    text_option=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                )

    def _set_size_mode_(self, mode):
        self._size_mode = mode

    def _set_text_(self, text):
        self._text = text
        self._refresh_widget_all_()

    def _set_style_(self, style):
        self._style = style


class QtMessageBubble(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForPressDef,
):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        if self._text:
            x, y = 0, 0

            mrg = 4

            txt_w, txt_h = (
                QtGui.QFontMetrics(self._text_font).width(self._text)+8, QtGui.QFontMetrics(self._text_font).height()
            )

            self._text_draw_rect.setRect(
                x+mrg, y+mrg, txt_w, txt_h
            )

            frm_w, frm_h = txt_w+mrg*2, txt_h+mrg*2
            self._frame_draw_rect.setRect(
                x, y, frm_w, frm_h
            )

            self.setFixedSize(frm_w+2, frm_h+2)

    def _do_close_(self):
        self._fade_timer.stop()

        self.parent()._bubble_message_widgets.remove(self)

        self.close()
        self.deleteLater()

    def __init__(self, *args, **kwargs):
        super(QtMessageBubble, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )

        self._text = None
        self._text_draw_rect = QtCore.QRect()
        self._text_font = _qt_core.QtFont.generate(size=10)
        self._text_color = _gui_core.GuiRgba.LightBlack

        self._frame_border_color = _gui_core.GuiRgba.LightBlack
        self._frame_background_color = _gui_core.GuiRgba.LightNeonGreen
        self._frame_draw_rect = QtCore.QRect()
        self._frame_border_radius = 3

        self._opacity = 1.0

        self._fade_timer = QtCore.QTimer(self)

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._do_close_()

        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        if self._text:
            painter._set_border_color_(*(self._frame_border_color[:3]+(self._opacity*255.0, )))
            painter._set_background_color_(*(self._frame_background_color[:3]+(self._opacity*255.0, )))
            painter.drawRoundedRect(
                self._frame_draw_rect,
                self._frame_border_radius, self._frame_border_radius,
                QtCore.Qt.AbsoluteSize
            )

            painter._set_text_color_(*(self._text_color[:3]+(self._opacity*255.0, )))
            painter._set_font_(self._text_font)
            painter.drawText(
                self._frame_draw_rect,
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                self._text
            )

    @classmethod
    def _create_for_(cls, widget, text):
        if hasattr(widget, '_bubble_message_widgets') is False:
            widget._bubble_message_widgets = []

        wgt = cls(widget)
        wgt._set_text_(text)
        wgt._popup_()
        # collection later
        widget._bubble_message_widgets.append(wgt)

    def _set_text_(self, text):
        self._text = text
        self._refresh_widget_all_()

    def _close_delay_as_fade_(self, delay_time):
        tmr = QtCore.QTimer(self)
        tmr.singleShot(delay_time, self._do_close_as_fade_)

    def _do_close_as_fade_(self):
        def fnc_():
            self._opacity -= .1
            self._refresh_widget_draw_()
            if self._opacity <= .1:
                self._do_close_()

        self._fade_timer.timeout.connect(fnc_)
        self._fade_timer.start(50)

    def _popup_(self):
        x, y = 0, 0
        widgets = self.parent()._bubble_message_widgets

        if widgets:
            y_c = y+max([(_.y()+_.height()) for _ in widgets])
        else:
            y_c = y

        p_w, p_h = self.parent().width(), self.parent().height()
        w, h = self.width(), self.height()
        self.move(x+(p_w-w)/2, y_c)
        self.show()
        self.raise_()

        self._close_delay_as_fade_(3000)


class QtImageBubble(
    QtWidgets.QWidget
):
    def __init__(self, *args, **kwargs):
        super(QtImageBubble, self).__init__(*args, **kwargs)


class QtTextBubbles(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtWidgetBaseDef
):
    bubbles_value_change_accepted = qt_signal(list)
    bubbles_value_changed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtTextBubbles, self).__init__(*args, **kwargs)
        self._lot = _base.QtHBoxLayout(self)
        self._lot.setContentsMargins(*[2]*4)
        self._lot.setSpacing(1)

        self._bubble_constant_entry = None
        self._bubble_texts = []

    def _set_entry_widget_(self, widget):
        self._bubble_constant_entry = widget

    def _create_one_(self, text):
        texts = self._get_all_texts_()
        if text and text not in texts:
            self._append_value_(text)
            #
            bubble = QtTextBubble()
            self._lot.addWidget(bubble)
            bubble._set_text_(text)
            bubble.delete_text_accepted.connect(self._delete_value_)

            if self._bubble_constant_entry is not None:
                self._bubble_constant_entry._do_clear_()

    def _append_value_(self, text):
        self._bubble_texts.append(text)

        self.bubbles_value_changed.emit()
        self.bubbles_value_change_accepted.emit(self._bubble_texts)

    def _delete_value_(self, text):
        self._bubble_texts.remove(text)

        self.bubbles_value_changed.emit()
        self.bubbles_value_change_accepted.emit(self._bubble_texts)

    def _on_backspace_(self):
        # when bubble text widget delete, send emit do self._delete_value_(text)
        self._lot._delete_latest_()

        self.bubbles_value_changed.emit()
        self.bubbles_value_change_accepted.emit(self._bubble_texts)

    def _get_all_texts_(self):
        return self._bubble_texts

    def _clear_all_values_(self):
        self._bubble_texts = []
        self._lot._clear_all_widgets_()


class QtPathBubble(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForPressDef,
):
    value_changed = qt_signal()

    next_press_clicked = qt_signal()
    component_press_clicked = qt_signal(int)
    component_press_dbl_clicked = qt_signal(int)

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        if self._components:
            x, y = 0, 0
            w, h = self.width(), self.height()

            w_d = h/2
            c_x = 0
            for i_index, i_path in enumerate(self._components):
                i_text = i_path.get_name()
                i_frame_rect = self._frame_rects[i_index]
                i_text_rect = self._text_rects[i_index]
                # root
                if i_index == 0:
                    if self._root_text is not None:
                        i_text = self._root_text

                i_text_w = QtGui.QFontMetrics(self._text_font).width(i_text)+16
                i_text_w = min(i_text_w, self._text_w_maximum)

                i_frame_rect.setRect(
                    x+c_x, y, i_text_w, h
                )
                i_text_rect.setRect(
                    x+c_x, y, i_text_w, h
                )
                c_x += i_text_w

            # update text
            self._next_rect.setRect(c_x, y, w_d, h)

            c_x += w_d

            self.setFixedWidth(c_x)

    def __init__(self, *args, **kwargs):
        super(QtPathBubble, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)
        
        self._text_font = _qt_core.QtFont.generate_2(size=12)
        self.setFont(self._text_font)
        
        self.__path_text = None
        # path is instance of BscNodePathOpt
        self._path = None

        self._components = None
        self._frame_rects = []
        self._text_rects = []
        self._next_rect = QtCore.QRect()
        self._next_text_rect = QtCore.QRect()

        self._text_w_maximum = 120

        self._root_text = None

        self._component_hovered_index = None
        self._component_pressed_index = None

        self._next_hover_flag = False
        self._next_is_enable = False
        self.__next_is_waiting = False

        self.installEventFilter(self)
    
    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.Enter:
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.Leave:
                self._component_hovered_index = None
                self._next_hover_flag = False
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.ToolTip:
                self._do_show_tool_tip_(event)
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._component_hovered_index is not None:
                        self._set_action_flag_(
                            self.ActionFlag.ComponentPress
                        )
                        self._component_pressed_index = self._component_hovered_index
                    elif self._next_hover_flag is True:
                        self._set_action_flag_(
                            self.ActionFlag.NextPress
                        )
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._component_hovered_index is not None:
                        self._set_action_flag_(
                            self.ActionFlag.ComponentDbClick
                        )
                        self._component_pressed_index = self._component_hovered_index
            elif event.type() == QtCore.QEvent.MouseMove:
                self._do_hover_move_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._is_action_flag_match_(self.ActionFlag.ComponentPress):
                        self.component_press_clicked.emit(self._component_pressed_index)
                        self._component_pressed_index = None
                    elif self._is_action_flag_match_(self.ActionFlag.ComponentDbClick):
                        self.component_press_dbl_clicked.emit(self._component_pressed_index)
                        self._component_pressed_index = None
                    elif self._is_action_flag_match_(self.ActionFlag.NextPress):
                        self.next_press_clicked.emit()

                self._clear_all_action_flags_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        if self._components:
            painter._set_antialiasing_(False)
            for i_index, i_path in enumerate(self._components):
                i_text = i_path.get_name()
                if i_index == 0:
                    if self._root_text is not None:
                        i_text = self._root_text

                i_frame_rect = self._frame_rects[i_index]
                i_text_rect = self._text_rects[i_index]
                painter._set_border_color_(_qt_core.QtRgba.BdrBubble)
                i_is_hovered = i_index == self._component_hovered_index
                i_is_pressed = i_index == self._component_pressed_index
                i_offset = [0, 1][i_is_pressed]
                if i_is_pressed is True:
                    painter._set_background_color_(_qt_core.QtRgba.BkgBubbleAction)
                elif i_is_hovered is True:
                    painter._set_background_color_(_qt_core.QtRgba.BkgBubbleHover)
                else:
                    painter._set_background_color_(_qt_core.QtRgba.BkgBubble)

                if i_offset > 0:
                    i_frame_rect = QtCore.QRect(
                        i_frame_rect.x()+i_offset, i_frame_rect.y()+i_offset,
                        i_frame_rect.width()-i_offset, i_frame_rect.height()-i_offset
                    )
                    i_text_rect = QtCore.QRect(
                        i_text_rect.x()+i_offset, i_text_rect.y()+i_offset,
                        i_text_rect.width()-i_offset, i_text_rect.height()-i_offset
                    )

                painter.drawRect(i_frame_rect)

                i_text_elided = self.fontMetrics().elidedText(
                    i_text,
                    QtCore.Qt.ElideMiddle,
                    i_text_rect.width()-4,
                    QtCore.Qt.TextShowMnemonic
                )

                painter._set_text_color_(_qt_core.QtRgba.TxtBubble)
                painter.drawText(
                    i_text_rect,
                    QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                    i_text_elided
                )
            # draw next
            nxt_p = self._next_rect
            nxt_x, nxt_y = nxt_p.x(), nxt_p.y()
            nxt_w, nxt_h = nxt_p.width(), nxt_p.height()
            nxt_r = nxt_h/2
            if self._next_is_enable is True:
                next_coords = [
                    (nxt_x, nxt_y),
                    (nxt_x+nxt_w, nxt_y+nxt_r),
                    (nxt_x, nxt_y+nxt_h),
                    # repeat start
                    (nxt_x, nxt_y)
                ]
                painter._set_border_color_(_qt_core.QtRgba.BdrBubble)
                if self._next_hover_flag is True:
                    if self._is_action_flag_match_(self.ActionFlag.NextPress):
                        painter._set_background_color_(
                            _qt_core.QtRgba.BkgBubbleAction
                        )
                    else:
                        painter._set_background_color_(
                            _qt_core.QtRgba.BkgBubbleHover
                        )
                else:
                    painter._set_background_color_(
                        _qt_core.QtRgba.BkgBubble
                    )

                painter._draw_path_by_coords_(
                    next_coords, False
                )
            else:
                painter._set_border_color_(_qt_core.QtRgba.BdrBubble)
                if self.__next_is_waiting is True:
                    painter._set_background_color_(_qt_core.QtRgba.BkgBubbleNextWait)
                else:
                    painter._set_background_color_(_qt_core.QtRgba.BkgBubbleNextFinish)

                painter.drawRect(
                    self._next_rect
                )

    def _do_hover_move_(self, event):
        p = event.pos()

        self._component_hovered_index = None
        for i_index, i_rect in enumerate(self._frame_rects):
            if i_rect.contains(p):
                self._component_hovered_index = i_index
        # update next
        if self._next_is_enable is True:
            if self._next_rect.contains(p):
                self._next_hover_flag = True
            else:
                self._next_hover_flag = False

        self._refresh_widget_draw_()

    def _do_show_tool_tip_(self, event):
        if self._component_hovered_index:
            component = self._components[self._component_hovered_index]

            css = _qt_core.QtUtil.generate_tool_tip_css(
                'path', component.to_string()
            )
            # noinspection PyArgumentList
            QtWidgets.QToolTip.showText(
                QtGui.QCursor.pos(), css, self
            )

    def _set_next_enable_(self, boolean):
        self._next_is_enable = boolean
        self._refresh_widget_all_()

    def _start_next_wait_(self):
        self.__next_is_waiting = True
        self._refresh_widget_draw_()

    def _end_next_wait_(self):
        self.__next_is_waiting = False
        self._refresh_widget_draw_()

    def _set_root_text_(self, text):
        self._root_text = text

    def _set_path_text_(self, text):
        if text != self.__path_text:
            self.__path_text = text
            self._path = bsc_core.BscNodePathOpt(self.__path_text)
            self._components = self._path.get_components()
            self._components.reverse()
            c = len(self._components)
            self._frame_rects = [QtCore.QRect() for _ in range(c)]
            self._text_rects = [QtCore.QRect() for _ in range(c)]

            self.value_changed.emit()

        self._refresh_widget_all_()

    def _get_path_text_(self):
        return self.__path_text

    def _get_path_(self):
        return self._path

    def _get_component_at_(self, index):
        return self._components[index]


class QtBubbleAsChoice(
    QtWidgets.QLineEdit,
    _qt_abstracts.AbsQtActionBaseDef,
):
    choice_text_accepted = qt_signal(str)
    choice_index_accepted = qt_signal(int)

    def __draw_text(self, painter, rect, rect_draw, text, text_color, highlight_color):
        # noinspection PyUnusedLocal
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()

        x_d, y_d = rect_draw.x(), rect_draw.y()
        w_d, h_d = rect_draw.width(), rect_draw.height()
        # update font
        painter._set_font_(_qt_core.QtFont.generate_2(size=h*.725))

        text_option_ = QtGui.QTextOption(
            QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter
        )
        # fixme: text width error
        # text_option_.setUseDesignMetrics(True)
        text_option_.setWrapMode(text_option_.NoWrap)

        text_ = painter.fontMetrics().elidedText(
            text,
            QtCore.Qt.ElideLeft,
            w_d,
            QtCore.Qt.TextShowMnemonic
        )
        rect_f_ = QtCore.QRectF(
            x_d, y_d,
            w_d, h_d
        )
        if self.__text_input:
            ms = re.search(self.__pattern, text, re.IGNORECASE)
            if ms:
                a = ms.group(1)
                a_t_w = painter.fontMetrics().width(a)
                # t_w = float(a_t_w+b_t_w)
                # a_w, b_w = a_t_w/t_w*w, b_t_w/t_w*w

                t_w = painter.fontMetrics().width(text)
                a_w = (w-t_w)/2+a_t_w

                a_rect = QtCore.QRect(x_d, y_d, a_w, h_d)

                painter._set_border_color_(0, 0, 0, 0)
                painter._set_background_color_(highlight_color)
                painter.drawRect(a_rect)

                painter._set_text_color_(text_color)
                painter.drawText(
                    rect_f_,
                    text_,
                    text_option_,
                )
                # painter.drawText(
                #     rect_draw,
                #     QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                #     text
                # )
        else:
            painter._set_text_color_(text_color)
            painter.drawText(
                rect_f_,
                text_,
                text_option_,
            )
            # painter.drawText(
            #     rect_draw,
            #     QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
            #     text
            # )

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        if self._texts:
            p = self.parent()
            x, y = 0, 0
            w, h = p.width(), p.height()

            self.setGeometry(
                x, y, w, h
            )

            h_i = self._text_h_input
            self.__rect_input.setRect(
                x, y, w, h_i
            )

            self.__draw_data = []

            if self._idx_all:
                h_y = self.__y_hover
                x_0, y_0 = 0, h_i
                w_0, h_0 = w, h-h_i
                c = len(self._idx_all)
                c_h = max(min(int(h_0/c), self._text_h_maximum), self._text_h_minimum)

                v_h = c*c_h
                v_y = y_0+(h_0-v_h)/2

                for i_seq, i_index in enumerate(self._idx_all):
                    i_text = self._texts[i_index]
                    i_t_w, i_t_h = _qt_core.QtFont.compute_size_2(c_h*.725, i_text)

                    i_rect = self._rects[i_index]
                    i_x, i_y = x_0+(w_0-i_t_w)/2, y_0+(h_0-v_h)/2+c_h*i_seq

                    if self._is_action_flag_match_(
                        self.ActionFlag.HoverMove
                    ):
                        if i_seq == 0:
                            if x < h_y < i_y+c_h:
                                self._index_current = i_index
                        elif i_seq == c-1:
                            if i_y < h_y < h:
                                self._index_current = i_index
                        else:
                            if i_y < h_y < i_y+c_h:
                                self._index_current = i_index

                    i_rect.setRect(i_x-2, i_y, i_t_w+4, c_h)
                # clamp to viewport
                if self.__y_hover < v_y:
                    self._index_current = self._idx_all[0]
                elif self.__y_hover > v_y+v_h:
                    self._index_current = self._idx_all[-1]

    def __init__(self, *args, **kwargs):
        super(QtBubbleAsChoice, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        self._init_action_base_def_(self)

        self.__is_active = False

        self.__text_input = ''
        self.__pattern = None
        self._texts = []
        self._idx_all = []

        self._text_h_input = 20
        self._text_h_maximum, self._text_h_minimum = 32, 4

        self.__rect_input = QtCore.QRect()
        self._rects = []

        self.__font_input = _qt_core.QtFont.generate(size=12)
        self.__font_current = _qt_core.QtFont.generate(size=24)

        self.__y_hover = -1

        self._index_current = None
        self._idx_maximum, self.__idx_minimum = None, 0

        self.__draw_data = []

        reg = QtCore.QRegExp(r'^[a-zA-Z0-9_ \*\/]+$')
        validator = QtGui.QRegExpValidator(reg, self)
        self.setValidator(validator)

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if self.__is_active is True:
            if widget == self:
                if event.type() == QtCore.QEvent.Enter:
                    pass
                    # self.setFocus()
                elif event.type() == QtCore.QEvent.FocusIn:
                    self._refresh_widget_draw_()
                elif event.type() == QtCore.QEvent.FocusOut:
                    self._refresh_widget_draw_()
                elif event.type() == QtCore.QEvent.MouseButtonPress:
                    if event.button() == QtCore.Qt.LeftButton:
                        self._set_action_flag_(self.ActionFlag.Press)
                elif event.type() == QtCore.QEvent.MouseMove:
                    if event.buttons() == QtCore.Qt.NoButton:
                        self._set_action_flag_(
                            self.ActionFlag.HoverMove
                        )
                        self._do_hover_move_(event)
                elif event.type() == QtCore.QEvent.MouseButtonRelease:
                    if event.button() == QtCore.Qt.LeftButton:
                        self._do_accept_()

                    self._clear_all_action_flags_()
                elif event.type() == QtCore.QEvent.KeyRelease:
                    if event.key() == QtCore.Qt.Key_Up:
                        self._set_action_flag_(
                            self.ActionFlag.KeyPress
                        )
                        self._do_previous_key_press_()
                    elif event.key() == QtCore.Qt.Key_Down:
                        self._set_action_flag_(
                            self.ActionFlag.KeyPress
                        )
                        self._do_next_key_press_()
                    elif event.key() in {QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter}:
                        self._do_accept_()
                    elif event.key() == QtCore.Qt.Key_Escape:
                        self._do_cancel_()
                    else:
                        pre_text = self.__text_input
                        if self.text() != pre_text:
                            self._do_filter_()
            elif widget == self.parent():
                if event.type() == QtCore.QEvent.Resize:
                    self._set_action_flag_(
                        self.ActionFlag.Resize
                    )
                    self._refresh_widget_all_()
        return False

    def paintEvent(self, event):
        if self._texts:
            painter = _qt_core.QtPainter(self)
            painter._set_antialiasing_(False)
            x, y = 0, 0
            w, h = self.width(), self.height()

            rect = QtCore.QRect(x, y, w, h)
            painter._set_border_color_(0, 0, 0, 0)
            painter._set_background_color_(0, 0, 0, 127)
            painter.drawRect(rect)

            alpha = [63, 255][self.hasFocus()]
            if self._idx_all:
                for i_index in self._idx_all:
                    i_text = self._texts[i_index]
                    i_rect = self._rects[i_index]
                    if i_index != self._index_current:
                        i_x, i_y = i_rect.x(), i_rect.y()
                        i_w, i_h = i_rect.width(), i_rect.height()
                        painter._set_border_color_(127, 127, 127, alpha)
                        painter._set_background_color_(63, 63, 63, alpha)

                        if i_w > w:
                            i_rect_draw = QtCore.QRect(x+3, i_y+1, w-7, i_h-2)
                        else:
                            i_rect_draw = QtCore.QRect(i_x, i_y+1, i_w, i_h-2)

                        painter.drawRect(i_rect_draw)

                        self.__draw_text(
                            painter, i_rect, i_rect_draw, i_text,
                            (239, 239, 239, alpha), (31, 63, 31, 127)
                        )

                if self._index_current is not None:
                    text_cur = self._texts[self._index_current]
                    rect_cur = self._rects[self._index_current]

                    h_c = self._text_h_maximum+4
                    t_w_c, t_h_c = _qt_core.QtFont.compute_size_2(
                        h_c*.725, text_cur
                    )

                    p_c_c = rect_cur.center()

                    x_cc, y_cc = p_c_c.x(), p_c_c.y()
                    w_c = t_w_c+4
                    x_c, y_c = x_cc-t_w_c/2-2, y_cc-h_c/2+1

                    rect_cur_0 = QtCore.QRect(
                        x_c, y_cc-h_c/2, w_c, h_c
                    )
                    if w_c > w:
                        rect_draw_cur = QtCore.QRect(
                            x+3, y_cc-h_c/2+1, w-7, h_c-2
                        )
                    else:
                        rect_draw_cur = QtCore.QRect(
                            x_c, y_cc-h_c/2+1, w_c, h_c-2
                        )

                    painter._set_border_color_(127, 127, 127, 255)
                    painter._set_background_color_(207, 207, 207, 255)
                    painter.drawRect(rect_draw_cur)

                    self.__draw_text(
                        painter, rect_cur_0, rect_draw_cur, text_cur,
                        (31, 31, 31, 255), (255, 127, 63, 127)
                    )

            painter._set_font_(self.__font_input)
            if self.__text_input:
                if self._idx_all:
                    text = self.__text_input
                    painter._set_text_color_(_qt_core.QtRgba.TxtCorrect)
                else:
                    text = self.__text_input
                    painter._set_text_color_(_qt_core.QtRgba.TxtError)
            else:
                painter._set_text_color_(_qt_core.QtRgba.TxtWarning)
                text = 'type to narrow choices'

            painter.drawText(
                self.__rect_input,
                QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                text
            )

    def _do_filter_(self):
        p = _qt_core.QtUtil.get_qt_cursor_point()
        l_p = self.mapFromGlobal(p)

        self.__y_hover = l_p.y()

        self._set_action_flag_(self.ActionFlag.HoverMove)

        self.__text_input = self.text()
        self.__pattern = r'(.*{})(.*)'.format(self.__text_input.replace('*', '.*'))
        self._idx_all = [
            i_index for i_index, i in enumerate(self._texts) if re.match(self.__pattern, i, re.IGNORECASE)
        ]

        if self._idx_all:
            self._idx_maximum = len(self._idx_all)-1
        else:
            self._idx_maximum = None
            self._index_current = None

        self._refresh_widget_all_()

    def _do_hover_move_(self, event):
        l_p = event.pos()
        self.__y_hover = l_p.y()

        self._refresh_widget_all_()

    def _do_previous_key_press_(self):
        if self._idx_maximum is not None:
            if self._index_current is None:
                self._index_current = self._idx_all[-1]
            else:
                if self._index_current not in self._idx_all:
                    self._index_current = self._idx_all[-1]

                index_pre = self._index_current
                idx = self._idx_all.index(index_pre)
                idx -= 1
                idx = max(min(idx, self._idx_maximum), self.__idx_minimum)
                self._index_current = self._idx_all[idx]

            self._refresh_widget_draw_()

    def _do_next_key_press_(self):
        if self._idx_maximum is not None:
            if self._index_current is None:
                self._index_current = self._idx_all[0]
            else:
                if self._index_current not in self._idx_all:
                    self._index_current = self._idx_all[0]

                index_pre = self._index_current
                idx = self._idx_all.index(index_pre)
                idx += 1
                idx = max(min(idx, self._idx_maximum), self.__idx_minimum)
                self._index_current = self._idx_all[idx]

            self._refresh_widget_draw_()

    def _do_accept_(self):
        if self._index_current is not None:
            text = self._texts[self._index_current]
            self.choice_index_accepted.emit(self._index_current)
            self.choice_text_accepted.emit(text)
            self.hide()
            sys.stdout.write('you choose "{}" at {}\n'.format(text, self._index_current))
            self.__is_active = False
        else:
            self._do_cancel_()

    def _do_cancel_(self):
        self.hide()
        self.__is_active = False

    def _set_texts_(self, texts):
        self._texts = texts
        self._rects = [QtCore.QRect() for _ in range(len(self._texts))]

    def _start_(self):
        if self.__is_active is True:
            if not self.__text_input:
                self._do_cancel_()
        else:
            self.clear()
            self.show()
            self.setFocus()

            self._do_filter_()

            self.__is_active = True

    def _setup_(self):
        self.hide()
        self.parent().installEventFilter(self)


class QtBubbleAsChoose(
    QtWidgets.QDialog,
    _qt_abstracts.AbsQtActionBaseDef,
):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_geometry_(self):
        mrg = self._margin
        c_x, c_y = mrg, mrg
        w, h = self.width(), self.height()
        if self._texts:
            side = 8
            t_t_w, t_t_h = _qt_core.QtFont.compute_size_2(self._tips_font_siz, self._tips)
            t_w, t_h = side*2+t_t_w, side*2+t_t_h
            self._tips_draw_rect.setRect(
                c_x+(w-t_w)/2, c_y+1, t_w, t_h-2
            )
            c_y += t_h

            for i_index, i_text in enumerate(self._texts):
                i_rect = self._rects[i_index]
                i_t_w, i_t_h = _qt_core.QtFont.compute_size_2(self._text_font_size, i_text)
                i_w, i_h = side*2+i_t_w, side*2+i_t_h
                i_rect.setRect(c_x+(w-i_w)/2, c_y+1, i_w, i_h-2)
                c_y += i_h

    def _compute_geometry_args_(self, pos):
        x_0, y_0 = pos.x(), pos.y()

        if self._texts:
            mrg = self._margin
            side = 8

            t_t_w, t_t_h = _qt_core.QtFont.compute_size_2(self._tips_font_siz, self._tips)
            t_w, t_h = side*2+t_t_w, side*2+t_t_h
            ws = [t_w]
            hs = [t_h]
            for i_index, i_text in enumerate(self._texts):
                i_text_draw = self._texts_draw[i_index]

                i_t_w, i_t_h = _qt_core.QtFont.compute_size_2(self._text_font_size, i_text_draw)
                i_w, i_h = side*2+i_t_w, side*2+i_t_h
                ws.append(i_w)
                hs.append(i_h)

            w, h = max(ws)+mrg*2, sum(hs)+mrg*2
            x, y = x_0-w/2-mrg, y_0-h/2-mrg
            return x, y, w, h

    def _refresh_widget_draw_(self):
        self.update()

    bubble_text_choose_accepted = qt_signal(str)

    def _do_cancel_(self):
        self._do_popup_close_()

    def __init__(self, *args, **kwargs):
        super(QtBubbleAsChoose, self).__init__(*args, **kwargs)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowDoesNotAcceptFocus)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        # self.setGraphicsEffect()
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed
        )

        self._init_action_base_def_(self)

        self._margin = 16

        self._tips = 'untitled'
        self._tips_draw_rect = QtCore.QRect()
        self._tips_font_siz = 16

        self._texts = []
        self._texts_draw = []
        self._rects = []

        self._index_current = None
        self._idx_maximum, self.__idx_minimum = None, 0
        self._idx_all = []

        self._text_font_size = 16

        self._result = None
        
        self._close_draw_rect = QtCore.QRect()

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.FocusOut:
                self._do_popup_close_()
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type == QtCore.QEvent.WindowDeactivate:
                print 'AAA'

            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.Press)
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.NoButton:
                    self._set_action_flag_(
                        self.ActionFlag.HoverMove
                    )
                    self._do_hover_move_(event.pos())
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self._do_accept_()

                self._clear_all_action_flags_()
            elif event.type() == QtCore.QEvent.KeyRelease:
                if event.key() == QtCore.Qt.Key_Up:
                    self._set_action_flag_(
                        self.ActionFlag.KeyPress
                    )
                    self._do_previous_key_press_()
                elif event.key() == QtCore.Qt.Key_Down:
                    self._set_action_flag_(
                        self.ActionFlag.KeyPress
                    )
                    self._do_next_key_press_()
                elif event.key() == QtCore.Qt.Key_Escape:
                    self._do_cancel_()
                elif event.key() in {QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter}:
                    self._do_accept_()

        return False

    def paintEvent(self, event):
        if self._texts:
            painter = _qt_core.QtPainter(self)
            painter._set_antialiasing_(False)

            painter.fillRect(
                self.rect(), QtGui.QColor(0, 0, 0, 1)
            )

            painter._set_font_(_qt_core.QtFont.generate(size=self._tips_font_siz*.725))
            painter._set_text_color_(_qt_core.QtRgba.TxtWarning)

            painter.drawText(
                self._tips_draw_rect,
                QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                self._tips
            )

            for i_index, i_text in enumerate(self._texts):
                i_text_draw = self._texts_draw[i_index]
                i_rect = self._rects[i_index]

                if i_index == self._index_current:
                    painter._set_border_color_(_qt_core.QtRgba.BdrBubble)
                    painter._set_background_color_(_qt_core.QtRgba.BkgBubbleHover)
                else:
                    painter._set_border_color_(_qt_core.QtRgba.BdrBubble)
                    painter._set_background_color_(_qt_core.QtRgba.BkgBubble)

                painter.drawRect(i_rect)

                painter._set_font_(_qt_core.QtFont.generate(size=self._text_font_size*.725))
                painter._set_text_color_(_qt_core.QtRgba.TxtBubble)
                painter.drawText(
                    i_rect,
                    QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                    i_text_draw
                )

    def _do_hover_move_(self, p):
        index_pre = self._index_current
        self._index_current = None
        if self._rects:
            for i_index, i_rect in enumerate(self._rects):
                if i_rect.contains(p):
                    self._index_current = i_index
                    break

        if self._index_current != index_pre:
            self._refresh_widget_draw_()

    def _do_previous_key_press_(self):
        if self._idx_maximum is not None:
            if self._index_current is None:
                self._index_current = self._idx_all[-1]
            else:
                if self._index_current not in self._idx_all:
                    self._index_current = self._idx_all[-1]

                index_pre = self._index_current
                idx = self._idx_all.index(index_pre)
                idx -= 1
                idx = max(min(idx, self._idx_maximum), self.__idx_minimum)
                self._index_current = self._idx_all[idx]

            self._refresh_widget_draw_()

    def _do_next_key_press_(self):
        if self._idx_maximum is not None:
            if self._index_current is None:
                self._index_current = self._idx_all[0]
            else:
                if self._index_current not in self._idx_all:
                    self._index_current = self._idx_all[0]

                index_pre = self._index_current
                idx = self._idx_all.index(index_pre)
                idx += 1
                idx = max(min(idx, self._idx_maximum), self.__idx_minimum)
                self._index_current = self._idx_all[idx]

            self._refresh_widget_draw_()

    def _do_accept_(self):
        if self._index_current is not None:
            text = self._texts[self._index_current]
            self.bubble_text_choose_accepted.emit(text)
            self._result = text
            self._do_popup_close_()
        else:
            self._do_popup_close_()

    def _do_popup_start_(self):
        press_pos = _qt_core.QtUtil.get_qt_cursor_point()
        geometry_args = self._compute_geometry_args_(press_pos)
        if geometry_args:
            self.setGeometry(*geometry_args)
            self.setFocus(QtCore.Qt.MouseFocusReason)
            p = self.mapFromGlobal(press_pos)
            self._refresh_widget_draw_geometry_()
            self._do_hover_move_(p)
            self.exec_()

    def _do_popup_close_(self):
        self.deleteLater()
        self.close()

    def _set_tips_(self, text):
        self._tips = text

    def _set_texts_(self, texts, texts_draw=None):
        self._texts = texts
        self._texts_draw = map(
            bsc_pinyin.Text.to_prettify, self._texts
        )
        self._rects = [QtCore.QRect() for _ in range(len(self._texts))]
        self._idx_maximum = len(self._texts)-1
        self._idx_all = range(len(self._texts))

    def _get_result_(self):
        return self._result

    def get_result(self):
        return self._result
