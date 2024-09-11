# coding:utf-8
import lxbasic.storage as bsc_storage
# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *

from ..chart_widgets import histogram as _cht_wgt_histogram

from ..widgets import base as _base

from ..widgets import utility as _utility

from ..widgets import button as _button

from ..widgets import container as _container


class QtViewForHistogramChart(
    QtWidgets.QWidget
):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        pass

    def __init__(self, *args, **kwargs):
        super(QtViewForHistogramChart, self).__init__(*args, **kwargs)

        self._lot = _base.QtHBoxLayout(self)
        self._lot.setSpacing(0)
        self._lot.setContentsMargins(*[2]*4)

        self._sca = _utility.QtHScrollArea()
        self._lot.addWidget(self._sca)
        self._sca._set_background_color_(_gui_core.GuiRgba.Dim)

        self._histogram_chart = _cht_wgt_histogram.QtChartForHistogram()
        self._sca._layout.addWidget(self._histogram_chart)

        right_wgt = _utility.QtVLine()
        # right_wgt.hide()
        right_wgt.setFixedWidth(24)
        right_wgt._set_line_draw_enable_(True)
        self._lot.addWidget(right_wgt)
        right_lot = _base.QtVBoxLayout(right_wgt)
        right_lot.setContentsMargins(*[0]*4)
        right_lot.setSpacing(2)
        right_lot._set_align_as_top_()

        self._export_button = _button.QtIconPressButton()
        right_lot.addWidget(self._export_button)
        self._export_button.setFixedSize(24, 24)
        self._export_button._set_icon_name_('tool/export')
        self._export_button.press_clicked.connect(self._do_export_)

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        return False

    def _set_data_(self, data):
        self._histogram_chart._chart_model.set_data(data)

    def _set_name_text_(self, text):
        self._histogram_chart._chart_model.set_name(text)

    def _export_to_(self, file_path):
        self._histogram_chart._chart_model.export(file_path)

    def _do_export_(self):
        file_path = _gui_core.GuiStorageDialog.save_file(ext_filter='All File (*.png)', parent=self)
        if file_path:
            self._export_to_(file_path)
            bsc_storage.StgDirectoryOpt(file_path).show_in_system()

