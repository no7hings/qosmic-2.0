# coding=utf-8
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from .. import chart_models as _chart_models


class QtChartForInfo(QtWidgets.QWidget):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        self._chart_model.update(
            0, 0, self.width(), self.height()
        )

    def __init__(self, *args, **kwargs):
        super(QtChartForInfo, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self._chart_model = _chart_models.ChartModelForInfo()

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        self._chart_model.draw(painter)

    def _set_data_(self, dict_):
        self._chart_model.set_data(dict_)
        self._refresh_widget_all_()
