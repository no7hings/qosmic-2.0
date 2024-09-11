# coding=utf-8
import os
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from .. import chart_models as _chart_models


class QtChartForBar(QtWidgets.QWidget):
    info_accepted = qt_signal(dict)

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self._generate_pixmap_cache_()
        self.update()

    def _refresh_widget_draw_geometry_(self):
        self.setMinimumSize(20, self._chart_model.compute_height())

    def _generate_pixmap_cache_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        self._pixmap_cache = self._chart_model.generate_pixmap(x, y, w, h)
        self.info_accepted.emit(self._chart_model.generate_info())

    def __init__(self, *args, **kwargs):
        super(QtChartForBar, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self._pixmap_cache = QtGui.QPixmap()
        self._chart_model = _chart_models.ChartModelForBar()

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.modifiers() == QtCore.Qt.ControlModifier:
                    self._chart_model.set_normalization_flag(True)
                    self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.KeyRelease:
                self._chart_model.set_normalization_flag(False)
                self._refresh_widget_all_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        painter.drawPixmap(0, 0, self._pixmap_cache)
        painter.device()

    def _set_data_(self, data, data_keys, active_data_keys, data_type_dict=None):
        self._chart_model.set_data(data, data_keys, active_data_keys, data_type_dict)
        self._refresh_widget_all_()
        
    def _get_data_model_(self):
        return self._chart_model
