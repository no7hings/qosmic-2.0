# coding=utf-8
import sys

import re

import lxbasic.core as bsc_core
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *
# qt core
from .. import core as gui_qt_core
# qt abstracts
from .. import abstracts as gui_qt_abstracts
# qt widgets
from . import base as gui_qt_wgt_base


class QtTextBubble(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtActionBaseDef,
    gui_qt_abstracts.AbsQtActionForPressDef,
):
    delete_text_accepted = qt_signal(str)

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        if self.__text:
            x, y = 0, 0
            w, h = self.width(), self.height()
            dlt_w, dlt_h = h, h

            w_t, h_t = self.fontMetrics().width(self.__text), self.fontMetrics().height()/2
            # print h_t, h_t_
            s_t = (h-h_t)/2
            self.__radius_border = s_t
            # fit to max size
            w_t = min(w_t, self.__w_maximum_text)
            w_t_1 = w_t+s_t
            w_c = w_t_1+dlt_w
            self.setFixedWidth(w_c)

            dlt_icon_w, dlt_icon_h = self.__size_delete_icon_draw

            self.__rect_frame_draw.setRect(
                x+1, y+1, w_c-2, h-2
            )
            self.__rect_text_draw.setRect(
                x+s_t, y, w_t+2, h
            )

            self.__rect_delete.setRect(
                x+w_t_1, y, dlt_w, dlt_h
            )
            self.__rect_delete_draw.setRect(
                x+w_t_1+(dlt_w-dlt_icon_w)/2, y+(dlt_h-dlt_icon_h)/2, dlt_icon_w, dlt_icon_h
            )

    def __init__(self, *args, **kwargs):
        super(QtTextBubble, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
        )
        self.setMouseTracking(True)

        self.setFont(gui_qt_core.GuiQtFont.generate_2(size=12))

        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)

        self.__rect_frame_draw = QtCore.QRect()

        self.__is_hovered = False
        self.__delete_is_hovered = False

        self.__w_text, self.__h_text = 0, 16
        self.__w_maximum_text = 64
        self.__h_delete = 20
        self.__w_side = 2
        self.__text_spacing = 2
        self.__text = None
        self.__rect_text_draw = QtCore.QRect()
        self.__rect_delete = QtCore.QRect()
        self.__rect_delete_draw = QtCore.QRect()
        self.__size_delete = 16, 16
        self.__size_delete_icon_draw = 8, 8
        self.__icon_delete_0 = gui_core.GuiIcon.get('close')
        self.__icon_delete_1 = gui_core.GuiIcon.get('close-hover')
        
        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if hasattr(event, 'type'):
                if event.type() == QtCore.QEvent.Close:
                    self.delete_text_accepted.emit(self._get_text_())
                #
                elif event.type() == QtCore.QEvent.Resize:
                    self._refresh_widget_all_()
                #
                elif event.type() == QtCore.QEvent.Enter:
                    self.__is_hovered = True
                    self._refresh_widget_draw_()
                elif event.type() == QtCore.QEvent.Leave:
                    self.__is_hovered = False
                    self.__delete_is_hovered = False
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
                        if self.__delete_is_hovered is True:
                            self.close()
                            self.deleteLater()
                    #
                    self._clear_all_action_flags_()
                    #
                    self._is_hovered = False
                    self._refresh_widget_draw_()
        return False

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)
        if self.__text is not None:
            offset = self._get_action_offset_()
            painter._draw_frame_by_rect_(
                rect=self.__rect_frame_draw,
                border_color=gui_qt_core.QtBorderColors.Transparent,
                background_color=[gui_qt_core.QtColors.BubbleBackground, gui_qt_core.QtColors.BubbleBackgroundHover][self.__is_hovered],
                border_radius=self.__radius_border,
                offset=offset
            )
            painter._draw_text_by_rect_(
                rect=self.__rect_text_draw,
                text=self.__text,
                font_color=gui_qt_core.QtColors.ToolTipText,
                font=self.font(),
                text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                offset=offset
            )

            painter._draw_icon_file_by_rect_(
                rect=self.__rect_delete_draw,
                file_path=[self.__icon_delete_0, self.__icon_delete_1][
                    self.__delete_is_hovered],
                offset=offset
            )

    def _set_text_(self, text):
        self.__text = text
        self.setToolTip(self.__text)
        self._refresh_widget_all_()

    def _get_text_(self):
        return self.__text

    def _do_hover_move_(self, event):
        p = event.pos()
        if self.__rect_delete.contains(p):
            self.__delete_is_hovered = True
        else:
            self.__delete_is_hovered = False
        #
        self._refresh_widget_draw_()


class QtInfoBubble(
    QtWidgets.QWidget,
):
    class SizeMode(object):
        Auto = 0x00
        Fixed = 0x01

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        if self.__text:
            w, h = self.width(), self.height()

            self.setFont(gui_qt_core.GuiQtFont.generate_2(size=h*self.__text_percent))

            w_t, h_t = self.fontMetrics().width(self.__text), self.fontMetrics().height()/2
            s_t = (h-h_t)/2

            self.__radius_border = s_t

            w_c = w_t+s_t*2

            if self.__size_mode == self.SizeMode.Auto:
                self.setFixedWidth(w_c)

            x_0, y_0 = 0, 0
            w_0, h_0 = self.width(), self.height()
            w_f, h_f = w_0, h_0
            self.__rect.setRect(
                x_0, y_0, w_f, h_f
            )

    def __init__(self, *args, **kwargs):
        super(QtInfoBubble, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
        )

        self.__text = None
        self.__rect = QtCore.QRect()
        self.__margins = 2, 2, 2, 2

        self.__text_percent = 0.5

        self.__size_mode = self.SizeMode.Auto

        self.__radius_border = 0

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()

        return False

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)
        if self.__text:
            painter._draw_text_by_rect_(
                rect=self.__rect,
                text=self.__text,
                font_color=gui_qt_core.QtColors.TextTemporary,
                font=self.font(),
                text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
            )

    def _set_size_mode_(self, mode):
        self.__size_mode = mode

    def _set_text_(self, text):
        self.__text = text
        self._refresh_widget_all_()


class QtImageBubble(
    QtWidgets.QWidget
):
    def __init__(self, *args, **kwargs):
        super(QtImageBubble, self).__init__(*args, **kwargs)


class QtTextBubbles(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtWidgetBaseDef
):
    bubbles_value_change_accepted = qt_signal(list)
    bubbles_value_changed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtTextBubbles, self).__init__(*args, **kwargs)
        self.__lot = gui_qt_wgt_base.QtHBoxLayout(self)
        self.__lot.setContentsMargins(*[2]*4)
        self.__lot.setSpacing(1)

        self._bubble_constant_entry = None
        self._bubble_texts = []

    def _set_entry_widget_(self, widget):
        self._bubble_constant_entry = widget

    def _create_bubble_(self, text):
        texts = self._get_all_bubble_texts_()
        if text and text not in texts:
            self._append_value_(text)
            #
            bubble = QtTextBubble()
            self.__lot.addWidget(bubble)
            bubble._set_text_(text)
            bubble.delete_text_accepted.connect(self._delete_value_)

            if self._bubble_constant_entry is not None:
                self._bubble_constant_entry._set_clear_()

    def _append_value_(self, text):
        self._bubble_texts.append(text)

        self.bubbles_value_changed.emit()
        self.bubbles_value_change_accepted.emit(self._bubble_texts)

    def _delete_value_(self, text):
        self._bubble_texts.remove(text)

        self.bubbles_value_changed.emit()
        self.bubbles_value_change_accepted.emit(self._bubble_texts)

    def _execute_bubble_backspace_(self):
        # when bubble text widget delete, send emit do self._delete_value_(text)
        self.__lot._delete_latest_()

        self.bubbles_value_changed.emit()
        self.bubbles_value_change_accepted.emit(self._bubble_texts)

    def _get_all_bubble_texts_(self):
        return self._bubble_texts

    def _clear_all_values_(self):
        self._bubble_texts = []
        self.__lot._clear_all_widgets_()


class QtPathBubble(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtActionBaseDef,
    gui_qt_abstracts.AbsQtActionForPressDef,
):
    value_changed = qt_signal()

    next_press_clicked = qt_signal()
    component_press_clicked = qt_signal(int)
    component_press_db_clicked = qt_signal(int)

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        if self.__components:
            x, y = 0, 0
            w, h = self.width(), self.height()

            w_d = h/2
            c_x = 0
            for i_index, i_path in enumerate(self.__components):
                i_text = i_path.get_name()
                i_rect_frame = self.__rects_frame[i_index]
                i_rect_text = self.__rects_text[i_index]
                if i_index == 0:
                    i_w_c = w_d
                    i_rect_frame.setRect(
                        x+c_x, y, i_w_c, h
                    )
                    i_rect_text.setRect(
                        x+c_x, y, i_w_c, h
                    )
                else:
                    i_s_t, i_w_t, i_w_c, i_h_c = gui_qt_core.GuiQtText.generate_draw_args(
                        self, i_text
                    )
                    i_rect_frame.setRect(
                        x+c_x, y, i_w_c, i_h_c
                    )
                    i_rect_text.setRect(
                        x+c_x+i_s_t, y, i_w_t, i_h_c
                    )
                c_x += i_w_c
            # update text
            self.__rect_next.setRect(c_x, y, w_d, h)
            c_x += w_d

            self.setFixedWidth(c_x)

    def __init__(self, *args, **kwargs):
        super(QtPathBubble, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self.setFont(gui_qt_core.GuiQtFont.generate_2(size=12))
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)

        self.__path_text = None
        self.__path = None
        self.__components = None
        self.__rects_frame = []
        self.__rects_text = []
        self.__rect_next = QtCore.QRect()
        self.__w_next = 20

        self.__icon_next_enable = gui_core.GuiIcon.get('path_popup')

        self.__component_index_hovered = None
        self.__component_index_pressed = None

        self.__next_is_hovered = False
        self.__next_is_enable = False
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
                self.__component_index_hovered = None
                self.__next_is_hovered = False
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    if self.__component_index_hovered is not None:
                        self._set_action_flag_(
                            self.ActionFlag.ComponentPress
                        )
                        self.__component_index_pressed = self.__component_index_hovered
                    elif self.__next_is_hovered is True:
                        self._set_action_flag_(
                            self.ActionFlag.NextPress
                        )
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    if self.__component_index_hovered is not None:
                        self._set_action_flag_(
                            self.ActionFlag.ComponentDbClick
                        )
                        self.__component_index_pressed = self.__component_index_hovered
            elif event.type() == QtCore.QEvent.MouseMove:
                self._do_hover_move_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_is_match_(self.ActionFlag.ComponentPress):
                        self.component_press_clicked.emit(self.__component_index_pressed)
                        self.__component_index_pressed = None
                    elif self._get_action_flag_is_match_(self.ActionFlag.ComponentDbClick):
                        self.component_press_db_clicked.emit(self.__component_index_pressed)
                        self.__component_index_pressed = None
                    elif self._get_action_flag_is_match_(self.ActionFlag.NextPress):
                        self.next_press_clicked.emit()

                self._clear_all_action_flags_()
        return False

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)
        if self.__components:
            painter._set_antialiasing_(False)
            for i_index, i_path in enumerate(self.__components):
                i_text = i_path.get_name()
                i_rect_frame = self.__rects_frame[i_index]
                i_rect_text = self.__rects_text[i_index]
                painter._set_border_color_(gui_qt_core.QtColors.BubbleBorder)
                i_is_hovered = i_index == self.__component_index_hovered
                i_is_pressed = i_index == self.__component_index_pressed
                i_offset = [0, 1][i_is_pressed]
                if i_is_pressed is True:
                    painter._set_background_color_(gui_qt_core.QtColors.BubbleBackgroundActioned)
                elif i_is_hovered is True:
                    painter._set_background_color_(gui_qt_core.QtColors.BubbleBackgroundHover)
                else:
                    painter._set_background_color_(gui_qt_core.QtColors.BubbleBackground)

                if i_offset > 0:
                    i_rect_frame = QtCore.QRect(
                        i_rect_frame.x()+i_offset, i_rect_frame.y()+i_offset,
                        i_rect_frame.width()-i_offset, i_rect_frame.height()-i_offset
                    )
                    i_rect_text = QtCore.QRect(
                        i_rect_text.x()+i_offset, i_rect_text.y()+i_offset,
                        i_rect_text.width()-i_offset, i_rect_text.height()-i_offset
                    )

                painter.drawRect(i_rect_frame)

                if i_index > 0:
                    painter._set_text_color_(gui_qt_core.QtColors.BubbleText)
                    painter.drawText(
                        i_rect_text,
                        QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                        i_text
                    )
            # draw next
            r_p = self.__rect_next
            x_p, y_p = r_p.x(), r_p.y()
            w_p, h_p = r_p.width(), r_p.height()
            d_p = h_p/2
            if self.__next_is_enable is True:
                next_coords = [
                    (x_p, y_p), (x_p+d_p, y_p+d_p), (x_p, y_p+h_p),
                    (x_p, y_p)
                ]
                painter._set_border_color_(gui_qt_core.QtColors.BubbleBorder)
                if self.__next_is_hovered is True:
                    if self._get_action_flag_is_match_(self.ActionFlag.NextPress):
                        painter._set_background_color_(
                            gui_qt_core.QtColors.BubbleBackgroundActioned
                        )
                    else:
                        painter._set_background_color_(
                            gui_qt_core.QtColors.BubbleBackgroundHover
                        )
                else:
                    painter._set_background_color_(
                        gui_qt_core.QtColors.BubbleBackground
                    )
                painter._draw_path_by_coords_(
                    next_coords, False
                )
            else:
                painter._set_border_color_(gui_qt_core.QtColors.BubbleBorder)
                if self.__next_is_waiting is True:
                    painter._set_background_color_(gui_qt_core.QtColors.BubbleNextWaiting)
                else:
                    painter._set_background_color_(gui_qt_core.QtColors.BubbleNextFinished)
                painter.drawRect(
                    self.__rect_next
                )

    def _do_hover_move_(self, event):
        p = event.pos()

        self.__component_index_hovered = None
        for i_index, i_rect in enumerate(self.__rects_frame):
            if i_rect.contains(p):
                self.__component_index_hovered = i_index
        # update next
        if self.__next_is_enable is True:
            if self.__rect_next.contains(p):
                self.__next_is_hovered = True
            else:
                self.__next_is_hovered = False

        self._refresh_widget_draw_()

    def _set_next_enable_(self, boolean):
        self.__next_is_enable = boolean
        self._refresh_widget_all_()

    def _start_next_wait_(self):
        self.__next_is_waiting = True
        self._refresh_widget_draw_()

    def _end_next_wait_(self):
        self.__next_is_waiting = False
        self._refresh_widget_draw_()

    def _set_path_text_(self, text):
        if text != self.__path_text:
            self.__path_text = text
            self.__path = bsc_core.PthNodeOpt(self.__path_text)
            self.__components = self.__path.get_components()
            self.__components.reverse()
            c = len(self.__components)
            self.__rects_frame = [QtCore.QRect() for _ in range(c)]
            self.__rects_text = [QtCore.QRect() for _ in range(c)]

            self.value_changed.emit()

        self._refresh_widget_all_()

    def _get_path_text_(self):
        return self.__path_text

    def _get_path_(self):
        return self.__path

    def _get_component_at_(self, index):
        return self.__components[index]


class QtBubbleAsChoice(
    QtWidgets.QLineEdit,
    gui_qt_abstracts.AbsQtActionBaseDef,
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
        painter._set_font_(gui_qt_core.GuiQtFont.generate_2(size=h*.725))

        text_option_ = QtGui.QTextOption(
            QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter
        )
        text_option_.setUseDesignMetrics(True)
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
        if self.__texts:
            p = self.parent()
            x, y = 0, 0
            w, h = p.width(), p.height()

            self.setGeometry(
                x, y, w, h
            )

            h_i = self.__h_text_input
            self.__rect_input.setRect(
                x, y, w, h_i
            )

            self.__draw_data = []

            if self.__idx_all:
                h_y = self.__y_hover
                x_0, y_0 = 0, h_i
                w_0, h_0 = w, h-h_i
                c = len(self.__idx_all)
                c_h = max(min(int(h_0/c), self.__h_text_maximum), self.__h_text_minimum)

                v_h = c*c_h
                v_y = y_0+(h_0-v_h)/2

                for i_seq, i_index in enumerate(self.__idx_all):
                    i_text = self.__texts[i_index]
                    i_t_w, i_t_h = gui_qt_core.GuiQtFont.compute_size_2(c_h*.725, i_text)

                    i_rect = self.__rects[i_index]
                    i_x, i_y = x_0+(w_0-i_t_w)/2, y_0+(h_0-v_h)/2+c_h*i_seq

                    if self._get_action_flag_is_match_(
                        self.ActionFlag.HoverMove
                    ):
                        if i_seq == 0:
                            if x < h_y < i_y+c_h:
                                self.__index_current = i_index
                        elif i_seq == c-1:
                            if i_y < h_y < h:
                                self.__index_current = i_index
                        else:
                            if i_y < h_y < i_y+c_h:
                                self.__index_current = i_index

                    i_rect.setRect(i_x-2, i_y, i_t_w+4, c_h)
                # clamp to viewport
                if self.__y_hover < v_y:
                    self.__index_current = self.__idx_all[0]
                elif self.__y_hover > v_y+v_h:
                    self.__index_current = self.__idx_all[-1]

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
        self.__texts = []
        self.__idx_all = []

        self.__h_text_input = 20
        self.__h_text_maximum, self.__h_text_minimum = 32, 4

        self.__rect_input = QtCore.QRect()
        self.__rects = []

        self.__font_input = gui_qt_core.GuiQtFont.generate(size=12)
        self.__font_current = gui_qt_core.GuiQtFont.generate(size=24)

        self.__y_hover = -1

        self.__index_current = None
        self.__idx_maximum, self.__idx_minimum = None, 0

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
        if self.__texts:
            painter = gui_qt_core.QtPainter(self)
            painter._set_antialiasing_(False)
            x, y = 0, 0
            w, h = self.width(), self.height()

            rect = QtCore.QRect(x, y, w, h)
            painter._set_border_color_(0, 0, 0, 0)
            painter._set_background_color_(0, 0, 0, 127)
            painter.drawRect(rect)

            alpha = [63, 255][self.hasFocus()]
            if self.__idx_all:
                for i_index in self.__idx_all:
                    i_text = self.__texts[i_index]
                    i_rect = self.__rects[i_index]
                    if i_index != self.__index_current:
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

                if self.__index_current is not None:
                    text_cur = self.__texts[self.__index_current]
                    rect_cur = self.__rects[self.__index_current]

                    h_c = self.__h_text_maximum+4
                    t_w_c, t_h_c = gui_qt_core.GuiQtFont.compute_size_2(
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
                if self.__idx_all:
                    text = self.__text_input
                    painter._set_text_color_(gui_qt_core.QtColors.TextCorrect)
                else:
                    text = self.__text_input
                    painter._set_text_color_(gui_qt_core.QtColors.TextError)
            else:
                painter._set_text_color_(gui_qt_core.QtColors.TextWarning)
                text = 'type to narrow choices'

            painter.drawText(
                self.__rect_input,
                QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                text
            )

    def _do_filter_(self):
        p = gui_qt_core.GuiQtUtil.get_qt_cursor_point()
        l_p = self.mapFromGlobal(p)

        self.__y_hover = l_p.y()

        self._set_action_flag_(self.ActionFlag.HoverMove)

        self.__text_input = self.text()
        self.__pattern = r'(.*{})(.*)'.format(self.__text_input.replace('*', '.*'))
        self.__idx_all = [
            i_index for i_index, i in enumerate(self.__texts) if re.match(self.__pattern, i, re.IGNORECASE)
        ]

        if self.__idx_all:
            self.__idx_maximum = len(self.__idx_all)-1
        else:
            self.__idx_maximum = None
            self.__index_current = None

        self._refresh_widget_all_()

    def _do_hover_move_(self, event):
        l_p = event.pos()
        self.__y_hover = l_p.y()

        self._refresh_widget_all_()

    def _do_previous_key_press_(self):
        if self.__idx_maximum is not None:
            if self.__index_current is None:
                self.__index_current = self.__idx_all[-1]
            else:
                if self.__index_current not in self.__idx_all:
                    self.__index_current = self.__idx_all[-1]

                index_pre = self.__index_current
                idx = self.__idx_all.index(index_pre)
                idx -= 1
                idx = max(min(idx, self.__idx_maximum), self.__idx_minimum)
                self.__index_current = self.__idx_all[idx]

            self._refresh_widget_draw_()

    def _do_next_key_press_(self):
        if self.__idx_maximum is not None:
            if self.__index_current is None:
                self.__index_current = self.__idx_all[0]
            else:
                if self.__index_current not in self.__idx_all:
                    self.__index_current = self.__idx_all[0]

                index_pre = self.__index_current
                idx = self.__idx_all.index(index_pre)
                idx += 1
                idx = max(min(idx, self.__idx_maximum), self.__idx_minimum)
                self.__index_current = self.__idx_all[idx]

            self._refresh_widget_draw_()

    def _do_accept_(self):
        if self.__index_current is not None:
            text = self.__texts[self.__index_current]
            self.choice_index_accepted.emit(self.__index_current)
            self.choice_text_accepted.emit(text)
            self.hide()
            sys.stdout.write('you choose "{}" at {}\n'.format(text, self.__index_current))
            self.__is_active = False
        else:
            self._do_cancel_()

    def _do_cancel_(self):
        self.hide()
        self.__is_active = False

    def _set_texts_(self, texts):
        self.__texts = texts
        self.__rects = [QtCore.QRect() for _ in range(len(self.__texts))]

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
    gui_qt_abstracts.AbsQtActionBaseDef,
):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_geometry_(self):
        c_x, c_y = 0, 0
        w, h = self.width(), self.height()
        if self.__texts:
            side = 8
            t_t_w, t_t_h = gui_qt_core.GuiQtFont.compute_size_2(self.__font_size_tips, self.__tips)
            t_w, t_h = side*2+t_t_w, side*2+t_t_h
            self.__rect_tips.setRect(
                c_x+(w-t_w)/2, c_y+1, t_w, t_h-2
            )
            c_y += t_h

            for i_index, i_text in enumerate(self.__texts):
                i_rect = self.__rects[i_index]
                i_t_w, i_t_h = gui_qt_core.GuiQtFont.compute_size_2(self.__font_size_text, i_text)
                i_w, i_h = side*2+i_t_w, side*2+i_t_h
                i_rect.setRect(c_x+(w-i_w)/2, c_y+1, i_w, i_h-2)
                c_y += i_h

    def _compute_geometry_args_(self, pos):
        x_0, y_0 = pos.x(), pos.y()

        if self.__texts:
            side = 8

            t_t_w, t_t_h = gui_qt_core.GuiQtFont.compute_size_2(self.__font_size_tips, self.__tips)
            t_w, t_h = side*2+t_t_w, side*2+t_t_h
            ws = [t_w]
            hs = [t_h]
            for i_index, i_text in enumerate(self.__texts):
                i_text_draw = self.__texts_draw[i_index]

                i_t_w, i_t_h = gui_qt_core.GuiQtFont.compute_size_2(self.__font_size_text, i_text_draw)
                i_w, i_h = side*2+i_t_w, side*2+i_t_h
                ws.append(i_w)
                hs.append(i_h)

            w, h = max(ws), sum(hs)
            x, y = x_0-w/2, y_0-h/2
            return x, y, w, h

    def _refresh_widget_draw_(self):
        self.update()

    bubble_text_choose_accepted = qt_signal(str)

    def __init__(self, *args, **kwargs):
        super(QtBubbleAsChoose, self).__init__(*args, **kwargs)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed
        )

        self._init_action_base_def_(self)

        self.__tips = 'untitled'
        self.__rect_tips = QtCore.QRect()
        self.__font_size_tips = 16

        self.__texts = []
        self.__texts_draw = []
        self.__rects = []

        self.__index_current = None
        self.__idx_maximum, self.__idx_minimum = None, 0
        self.__idx_all = []

        self.__font_size_text = 24

        self.__result = None

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.FocusOut:
                self._do_popup_close_()
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()

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
                elif event.key() in {QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter}:
                    self._do_accept_()

        return False

    def paintEvent(self, event):
        if self.__texts:
            painter = gui_qt_core.QtPainter(self)
            painter._set_antialiasing_(False)

            painter._set_font_(gui_qt_core.GuiQtFont.generate(size=self.__font_size_tips*.725))
            painter._set_text_color_(gui_qt_core.QtColors.TextWarning)

            painter.drawText(
                self.__rect_tips,
                QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                self.__tips
            )

            for i_index, i_text in enumerate(self.__texts):
                i_text_draw = self.__texts_draw[i_index]
                i_rect = self.__rects[i_index]

                if i_index == self.__index_current:
                    painter._set_border_color_(gui_qt_core.QtColors.BubbleBorder)
                    painter._set_background_color_(gui_qt_core.QtColors.BubbleBackgroundHover)
                else:
                    painter._set_border_color_(gui_qt_core.QtColors.BubbleBorder)
                    painter._set_background_color_(gui_qt_core.QtColors.BubbleBackground)

                painter.drawRect(i_rect)

                painter._set_font_(gui_qt_core.GuiQtFont.generate(size=self.__font_size_text*.725))
                painter._set_text_color_(gui_qt_core.QtColors.BubbleText)
                painter.drawText(
                    i_rect,
                    QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                    i_text_draw
                )

    def _do_hover_move_(self, p):
        index_pre = self.__index_current
        self.__index_current = None
        if self.__rects:
            for i_index, i_rect in enumerate(self.__rects):
                if i_rect.contains(p):
                    self.__index_current = i_index
                    break

        if self.__index_current != index_pre:
            self._refresh_widget_draw_()

    def _do_previous_key_press_(self):
        if self.__idx_maximum is not None:
            if self.__index_current is None:
                self.__index_current = self.__idx_all[-1]
            else:
                if self.__index_current not in self.__idx_all:
                    self.__index_current = self.__idx_all[-1]

                index_pre = self.__index_current
                idx = self.__idx_all.index(index_pre)
                idx -= 1
                idx = max(min(idx, self.__idx_maximum), self.__idx_minimum)
                self.__index_current = self.__idx_all[idx]

            self._refresh_widget_draw_()

    def _do_next_key_press_(self):
        if self.__idx_maximum is not None:
            if self.__index_current is None:
                self.__index_current = self.__idx_all[0]
            else:
                if self.__index_current not in self.__idx_all:
                    self.__index_current = self.__idx_all[0]

                index_pre = self.__index_current
                idx = self.__idx_all.index(index_pre)
                idx += 1
                idx = max(min(idx, self.__idx_maximum), self.__idx_minimum)
                self.__index_current = self.__idx_all[idx]

            self._refresh_widget_draw_()

    def _do_accept_(self):
        if self.__index_current is not None:
            text = self.__texts[self.__index_current]
            self.bubble_text_choose_accepted.emit(text)
            self.__result = text
            self._do_popup_close_()

    def _do_popup_start_(self):
        press_pos = gui_qt_core.GuiQtUtil.get_qt_cursor_point()
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
        self.__tips = text

    def _set_texts_(self, texts):
        self.__texts = texts
        self.__texts_draw = map(
            bsc_core.RawTextMtd.to_prettify, self.__texts
        )
        self.__rects = [QtCore.QRect() for _ in range(len(self.__texts))]
        self.__idx_maximum = len(self.__texts)-1
        self.__idx_all = range(len(self.__texts))

    def _get_result_(self):
        return self.__result

    def get_result(self):
        return self.__result
