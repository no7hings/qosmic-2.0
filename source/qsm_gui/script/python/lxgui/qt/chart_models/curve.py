# coding:utf-8
import lxbasic.core as bsc_core

from ... import core as _gui_core

from ..core.wrap import *

from .. import core as _qt_core

from . import base as _base


class ChartModelForCurve(object):
    def __init__(self):
        self._data = [
            _base._Data(
                coord=(0, 0)
            ),
            _base._Data(
                coord=(1, 1)
            )
        ]

    def generate_pixmap(self, x, y, w, h):
        self.update(x, y, w, h)

        size = QtCore.QSize(w, h)
        pixmap = QtGui.QPixmap(size)
        pixmap.fill(QtGui.QColor(63, 63, 63, 255))
        painter = _qt_core.QtPainter(pixmap)
        painter._set_antialiasing_(False)
        self._draw_curve(painter)
        painter.end()
        return pixmap

    def update(self, x, y, w, h):
        pass

    def _draw_curve(self, painter):
        for i in self._data:
            pass
