# coding=utf-8
import os
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from ..chart_models import curve as _curve_model


class QtChartForCurve(QtWidgets.QWidget):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self._generate_pixmap_cache_()
        self.update()

    def _refresh_widget_draw_geometry_(self):
        pass
        # self.setMinimumSize(
        #     self._chart_model.compute_width(), 20
        # )

    def _generate_pixmap_cache_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        self._pixmap_cache = self._chart_model.generate_pixmap(x, y, w, h)

    def __init__(self, *args, **kwargs):
        super(QtChartForCurve, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self._pixmap_cache = QtGui.QPixmap()
        self._chart_model = _curve_model.ChartModelForCurve()

        self.installEventFilter(self)
