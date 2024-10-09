# coding=utf-8
import six

import collections

import lxbasic.core as bsc_core
# gui
from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ..widgets import base as _qt_wgt_base

from ..widgets import entry_frame as _wgt_entry_frame


class _BaseViewWidget(QtWidgets.QWidget):
    refresh = qt_signal()

    TOOL_BAR_W = 26

    def __init__(self, *args, **kwargs):
        super(_BaseViewWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self._mrg = 4
        self._grid_lot = _qt_wgt_base.QtGridLayout(self)
        self._grid_lot.setContentsMargins(*[self._mrg]*4)
        self._grid_lot.setSpacing(2)

        self._toolbar_hide_flag = False

        self.setFocusPolicy(QtCore.Qt.ClickFocus)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        mrg = self._mrg
        x, y, w, h = 0, 0, self.width(), self.height()

        f_x, f_y, f_w, f_h = x+1, y+1, w-2, h-2
        pen = QtGui.QPen(QtGui.QColor(*[(71, 71, 71, 255), (95, 95, 95, 255)][self.hasFocus()]))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QColor(*_gui_core.GuiRgba.Dim))
        painter.drawRect(f_x, f_y, f_w, f_h)

        if self._toolbar_hide_flag is False:

            tol_w = self.TOOL_BAR_W
            x_t, y_t, w_t, h_t = x+mrg, y+mrg, w-mrg*2, h-mrg*2
            polygon = QtGui.QPolygon(
                [
                    QtCore.QPoint(x_t, y_t),
                    QtCore.QPoint(x_t+w_t, y_t),
                    QtCore.QPoint(x_t+w_t, y_t+tol_w),
                    QtCore.QPoint(x_t+tol_w, y_t+tol_w),
                    QtCore.QPoint(x_t+tol_w, y_t+h_t),
                    QtCore.QPoint(x_t, y_t+h_t),
                    QtCore.QPoint(x_t, y_t)
                ]
            )
            painter.setPen(QtGui.QColor(*_gui_core.GuiRgba.Basic))
            painter.setBrush(QtGui.QColor(*_gui_core.GuiRgba.Basic))
            painter.drawPolygon(
                polygon
            )
    
    def _set_toolbar_hide_flag_(self, boolean):
        self._toolbar_hide_flag = boolean
