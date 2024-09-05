# coding:utf-8
import lxbasic.storage as bsc_storage
# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *

from ..charts import histogram as _cht_histogram

from ..widgets import base as _base

from ..widgets import utility as _utility


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

        self._lot = _base.QtVBoxLayout(self)
        self._lot.setSpacing(0)
        self._lot.setContentsMargins(*[2]*4)

        self._sca = _utility.QtHScrollArea()
        self._lot.addWidget(self._sca)
        self._sca._set_background_color_(_gui_core.GuiRgba.Dim)

        self._histogram_chart = _cht_histogram.QtChartForHistogram()
        self._sca._layout.addWidget(self._histogram_chart)

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

    def _export_all_to_(self, directory_path):
        self._histogram_chart._export_all_to_(directory_path)

    def _do_export_all_(self):
        directory_path = _gui_core.GuiDialogForFile.save_directory(self)
        if directory_path:
            self._export_all_to_(directory_path)
            bsc_storage.StgDirectoryOpt(directory_path).show_in_system()

