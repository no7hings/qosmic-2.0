# coding=utf-8
import os
# gui
from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from ..widgets.entry import entry_for_capsule as _entry_for_capsule

from ..widgets import base as _base

from ..widgets import utility as _utility

from ..chart_models import curve as _curve_model


class QtCurveChart(QtWidgets.QWidget):
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
        super(QtCurveChart, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self._pixmap_cache = QtGui.QPixmap()
        self._chart_model = _curve_model.ChartModelForCurve()

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        painter.drawPixmap(0, 0, self._pixmap_cache)
        painter.device()

    def _set_tangent_type_(self, tangent_type):
        self._chart_model.set_tangent_type(tangent_type)
        self._refresh_widget_all_()


class QtCurveChartWidget(
    QtWidgets.QWidget
):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y, w, h = self.x(), self.y(), self.width(), self.height()

    def __init__(self, *args, **kwargs):
        super(QtCurveChartWidget, self).__init__(*args, **kwargs)

        self._lot = _base.QtHBoxLayout(self)
        self._lot.setSpacing(0)
        self._lot.setContentsMargins(*[2]*4)

        main_wgt = _utility.QtTranslucentWidget()
        self._lot.addWidget(main_wgt)
        main_lot = _base.QtVBoxLayout(main_wgt)
        main_lot.setContentsMargins(*[0]*4)
        main_lot.setSpacing(2)

        self._key_entry = _entry_for_capsule.QtEntryAsCapsule()
        main_lot.addWidget(self._key_entry)
        self._key_entry.setFixedHeight(20)

        self._sca = _utility.QtVScrollArea()
        main_lot.addWidget(self._sca)
        self._sca._set_background_color_(_gui_core.GuiRgba.Dim)

        self._curve_chart = QtCurveChart()
        self._sca._layout.addWidget(self._curve_chart)

        self._key_entry._set_value_options_(
            self._curve_chart._chart_model.TangentTypes.All
        )
        self._key_entry._set_value_(
            self._curve_chart._chart_model.TangentTypes.Default
        )

        self._key_entry.user_value_accepted.connect(self._on_tangent_type_changed_)

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        return False

    def _on_tangent_type_changed_(self, value):
        self._curve_chart._set_tangent_type_(value)

    def _set_data_(self, data):
        pass
