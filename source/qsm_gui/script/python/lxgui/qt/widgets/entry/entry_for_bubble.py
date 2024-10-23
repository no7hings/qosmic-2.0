# coding=utf-8
import six
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
        if self.__text:

            if self.__texts_draw:
                cs = [len(i) for i in self.__texts_draw]
                text = self.__texts_draw[cs.index(max(cs))]
            else:
                text = self.__text

            s_t, w_t, w_c, h_c = _qt_core.GuiQtText.generate_draw_args(self, text, self._text_w_maximum)
            self.setFixedWidth(w_c)

            self._frame_border_radius = s_t

            x, y = 0, 0

            self.__rect_frame_draw.setRect(
                x+1, y+1, w_c-2, h_c-2
            )
            self.__rect_text_draw.setRect(
                x+s_t, y, w_t, h_c
            )

    def __init__(self, *args, **kwargs):
        super(QtEntryForTextBubble, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
        )

        self.setFont(_qt_core.QtFont.generate_2(size=12))

        self._init_entry_base_def_(self)

        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)

        self.__text = None
        self.__rect_frame_draw = QtCore.QRect()
        self.__rect_text_draw = QtCore.QRect()

        self.__texts_draw = []

        self._is_hovered = False

        self._frame_border_radius = 0

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

    def _do_wheel_(self, event):
        delta = event.angleDelta().y()
        return self._scroll_to_(delta)

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        if self.__text is not None:
            offset = self._get_action_offset_()
            color_bkg, color_txt = _qt_core.QtColor.generate_color_args_by_text(self.__text)

            rect_frame = self.__rect_frame_draw
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

            rect_text = self.__rect_text_draw
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
                self.__text
            )

    def _set_value_(self, value):
        if super(QtEntryForTextBubble, self)._set_value_(value) is True:
            if isinstance(self._value, six.string_types):
                self.__text = self._value.capitalize()
            else:
                self.__text = str(self._value).capitalize()

            self.entry_value_changed.emit()
            self.entry_value_change_accepted.emit(value)

        self._refresh_widget_all_()

    def _get_value_(self):
        return self._value

    def _set_value_options_(self, values, names=None):
        if super(QtEntryForTextBubble, self)._set_value_options_(values) is True:
            self.__texts_draw = map(
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
        return self.__rect_frame_draw
