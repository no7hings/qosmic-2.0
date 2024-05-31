# coding=utf-8
import lxbasic.core as bsc_core
# gui
from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core


class QtChartAsPoolStatus(QtWidgets.QWidget):
    HEIGHT = 20

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        w, h = self.width(), self.height()
        c = len(self._rects)
        p_w, p_h = self._p_w, self._p_h

        m_w, m_h = (self._h-p_w)/2, (self._h-p_h)/2
        w_p_max = self._p_w*c

        x_c = w-w_p_max-m_w*2
        self._text_rect.setRect(
            0, 0, x_c-2, h
        )

        for i_rect in self._rects:
            i_rect.setRect(
                x_c+m_w, 0+m_h, p_w, p_h
            )

            x_c += self._p_w

    def __init__(self, *args, **kwargs):
        super(QtChartAsPoolStatus, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.setFixedHeight(self.HEIGHT)

        self._maximum = 1
        self._value = 0

        self._border_color = _gui_core.GuiRgba.Gray
        self._background_color = _gui_core.GuiRgba.Dim

        self._p_w, self._p_h = 12, 12
        self._h = self.HEIGHT

        self._text_rect = QtCore.QRect()
        self._rects = [QtCore.QRect()]

        self.installEventFilter(self)

    def _set_maximum_(self, value):
        self._maximum = value

        self._rects = []

        for i in range(self._maximum):
            self._rects.append(QtCore.QRect())

    def _set_value_(self, value):
        self._value = value
        self._refresh_widget_draw_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)

        for i_idx, i_rect in enumerate(self._rects):
            painter._set_border_color_(self._border_color)
            if i_idx < self._value:
                i_p = (i_idx+1)/float(self._maximum)
                i_rgb = bsc_core.RawColorMtd.hsv2rgb(
                    120-i_p*120, .75, .75
                )
                painter._set_background_color_(i_rgb)
            else:
                painter._set_background_color_(self._background_color)

            painter.drawRect(i_rect)

        painter.setFont(
            _qt_core.QtFonts.NameNormal
        )
        painter.drawText(
            self._text_rect,
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter,
            '{}/{}'.format(self._value, self._maximum)
        )
