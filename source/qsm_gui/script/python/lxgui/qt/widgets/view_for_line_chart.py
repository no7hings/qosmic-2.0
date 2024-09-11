# coding:utf-8
import lxbasic.storage as bsc_storage
# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *

from ..chart_widgets import line as _cht_wgt_line

from ..widgets import base as _base

from ..widgets import utility as _utility

from ..widgets import entry_for_capsule as _entry_for_capsule


class QtViewForLineChart(
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
        super(QtViewForLineChart, self).__init__(*args, **kwargs)

        self._lot = _base.QtVBoxLayout(self)
        self._lot.setSpacing(0)
        self._lot.setContentsMargins(*[2]*4)

        top_wgt = _utility.QtTranslucentWidget()
        top_wgt.setFixedHeight(20)
        self._lot.addWidget(top_wgt)
        top_lot = _base.QtHBoxLayout(top_wgt)
        top_lot.setContentsMargins(*[0]*4)
        top_lot.setSpacing(2)

        self._key_entry = _entry_for_capsule.QtEntryAsCapsule()
        top_lot.addWidget(self._key_entry)
        self._key_entry._set_use_exclusive_(False)

        self._sca = _utility.QtHScrollArea()
        self._lot.addWidget(self._sca)
        self._sca._set_background_color_(_gui_core.GuiRgba.Dim)

        self._line_chart = _cht_wgt_line.QtChartForLine()
        self._sca._layout.addWidget(self._line_chart)

        self._key_entry.user_value_accepted.connect(self._on_active_data_keys_changed_)

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        return False

    def _on_active_data_keys_changed_(self, values):
        self._line_chart._chart_model.set_active_data_keys(values)
        self._line_chart._chart_model.sort_branch_by_active()
        self._line_chart._refresh_widget_all_()

    def _set_data_(self, data, data_keys, data_type_dict=None):
        if data and data_keys:
            self._key_entry._set_value_options_(data_keys)
            active_data_keys = data_keys
            self._key_entry._set_value_(active_data_keys)

            self._line_chart._chart_model.set_data(data, data_keys, active_data_keys, data_type_dict)

    def _set_name_text_(self, text):
        self._line_chart._chart_model.set_name(text)

    def _export_all_to_(self, directory_path):
        self._line_chart._export_all_to_(directory_path)

    def _do_export_all_(self):
        directory_path = _gui_core.GuiStorageDialog.save_directory(self)
        if directory_path:
            self._export_all_to_(directory_path)
            bsc_storage.StgDirectoryOpt(directory_path).show_in_system()

