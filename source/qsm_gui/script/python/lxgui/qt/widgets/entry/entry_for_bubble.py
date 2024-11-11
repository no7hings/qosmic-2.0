# coding=utf-8
import six

from .... import core as _gui_core
# qt
from ....qt.core.wrap import *

from ....qt import core as _qt_core

from ....qt import abstracts as _qt_abstracts


class QtEntryForTextBubble(
    QtWidgets.QWidget,

    _qt_abstracts.AbsQtEntryBaseDef,

    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForPressDef,
):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        if self._value:
            x, y = 0, 0
            w, h = self.width(), self.height()
            w_c = max([QtGui.QFontMetrics(self._text_font).width(_x)+16 for _x in self._draw_texts])

            self.setFixedWidth(w_c)

            self._frame_draw_rect.setRect(
                x+1, y+1, w_c-1, h-1
            )
            self._text_draw_rect.setRect(
                x, y, w_c, h
            )

            self._popup_icon_rect.setRect(
                x+w_c-8, y+h-8, 8, 8
            )

    def _do_wheel_(self, event):
        delta = event.angleDelta().y()
        return self._scroll_to_(delta)

    def __init__(self, *args, **kwargs):
        super(QtEntryForTextBubble, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
        )

        self._text_font = _qt_core.QtFont.generate_2(size=12)

        self.setFont(self._text_font)

        self._init_entry_base_def_(self)

        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)

        self._frame_draw_rect = QtCore.QRect()
        self._text_draw_rect = QtCore.QRect()

        self._draw_texts = []

        self._is_hovered = False

        self._frame_border_radius = 2

        self._text_w_maximum = 96

        self.__w_mark = None

        self.setToolTip(
            _qt_core.QtUtil.generate_tool_tip_css(
                'bubble entry',
                [
                    '"LMB-click" to show choose',
                    '"MMB-wheel" to switch value',
                ]
            )
        )

        self._popup_icon_rect = QtCore.QRect()
        self._popup_icon_file = _gui_core.GuiIcon.get('state/popup')

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            #
            elif event.type() == QtCore.QEvent.Enter:
                self._is_hovered = True
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.Leave:
                self._is_hovered = False
                self._refresh_widget_draw_()

            elif event.type() == QtCore.QEvent.Wheel:
                self._do_wheel_(event)

            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.Press)
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.PressDblClick)
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._is_action_flag_match_(self.ActionFlag.Press):
                        self.press_clicked.emit()
                #
                self._clear_all_action_flags_()
                #
                self._is_hovered = False
                self._refresh_widget_draw_()

        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        if self._value is not None:
            offset = self._get_action_offset_()

            draw_text = self._draw_texts[self._value_options.index(self._value)]

            color_bkg, color_txt = _qt_core.QtColor.generate_color_args_by_text(draw_text)

            rect_frame = self._frame_draw_rect
            rect_frame = QtCore.QRect(
                rect_frame.x()+offset, rect_frame.y()+offset, rect_frame.width()-offset, rect_frame.height()-offset
            )
            painter._set_border_color_(_qt_core.QtRgba.BdrBubble)
            if offset:
                painter._set_background_color_(_qt_core.QtRgba.BkgBubbleAction)
            elif self._is_hovered:
                painter._set_background_color_(_qt_core.QtRgba.BkgBubbleHover)
            else:
                painter._set_background_color_(color_bkg)

            painter.drawRoundedRect(
                rect_frame,
                self._frame_border_radius, self._frame_border_radius,
                QtCore.Qt.AbsoluteSize
            )

            rect_text = self._text_draw_rect
            rect_text = QtCore.QRect(
                rect_text.x()+offset, rect_text.y()+offset, rect_text.width()-offset, rect_text.height()-offset
            )

            if offset:
                painter._set_text_color_(_qt_core.QtRgba.TxtBubble)
            elif self._is_hovered:
                painter._set_text_color_(_qt_core.QtRgba.TxtBubble)
            else:
                painter._set_text_color_(color_txt)

            painter.drawText(
                rect_text,
                QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                draw_text
            )

            painter._draw_icon_file_by_rect_(
                self._popup_icon_rect, self._popup_icon_file, offset
            )

    def _set_value_(self, value):
        if super(QtEntryForTextBubble, self)._set_value_(value) is True:

            self.entry_value_changed.emit()
            self.entry_value_change_accepted.emit(value)

        self._refresh_widget_all_()

    def _set_value_by_index_(self, index):
        value = super(QtEntryForTextBubble, self)._set_value_by_index_(index)
        if value:
            self.entry_value_changed.emit()
            self.entry_value_change_accepted.emit(value)

        self._refresh_widget_all_()

    def _get_value_(self):
        return self._value

    def _set_value_options_(self, values, names=None):
        if super(QtEntryForTextBubble, self)._set_value_options_(values) is True:
            if names:
                self._draw_texts = names
            else:
                self._draw_texts = map(
                    lambda x: x.capitalize() if isinstance(x, six.string_types) else str(x).capitalize(), values
                )

        self._refresh_widget_all_()

    def _to_next_(self):
        self._scroll_to_(1)

    def _to_previous_(self):
        self._scroll_to_(-1)

    def _scroll_to_(self, delta):
        values_all = self._get_value_options_()
        if values_all:
            value_pre = self._get_value_()
            if value_pre in values_all:
                minimum, maximum = 0, len(values_all)-1
                idx_pre = values_all.index(value_pre)
                if delta > 0:
                    if idx_pre == 0:
                        idx_cur = maximum
                    else:
                        idx_cur = idx_pre-1
                else:
                    if idx_pre == maximum:
                        idx_cur = minimum
                    else:
                        idx_cur = idx_pre+1
                idx_cur = max(min(idx_cur, maximum), 0)
                if idx_cur != idx_pre:
                    self._set_value_(values_all[idx_cur])
                    # set value before
                    return True
        return False

    def _get_frame_rect_(self):
        return self._frame_draw_rect
