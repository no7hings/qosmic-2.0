# coding:utf-8
import lxbasic.storage as bsc_storage
# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *

from ..chart_widgets import bar as _cht_wgt_bar

from ..chart_widgets import info as _cht_wgt_info

from .entry import entry_for_capsule as _entry_for_capsule

from . import base as _base

from . import utility as _utility

from . import button as _button


class QtViewForBarChart(
    QtWidgets.QWidget
):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y, w, h = self.x(), self.y(), self.width(), self.height()
        self._info_chart.setGeometry(
            x, y, w, h
        )

    def __init__(self, *args, **kwargs):
        super(QtViewForBarChart, self).__init__(*args, **kwargs)

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
        self._key_entry._set_use_exclusive_(False)

        self._sca = _utility.QtVScrollArea()
        main_lot.addWidget(self._sca)
        self._sca._set_background_color_(_gui_core.GuiRgba.Dim)

        self._bar_chart = _cht_wgt_bar.QtChartForBar()
        self._sca._layout.addWidget(self._bar_chart)

        self._key_entry.user_value_accepted.connect(self._on_active_data_keys_changed_)
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

        self._info_chart = _cht_wgt_info.QtChartForInfo(self)
        self._bar_chart.info_accepted.connect(self._info_chart._set_data_)
        
        self.installEventFilter(self)
    
    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        return False

    def _on_active_data_keys_changed_(self, values):
        self._bar_chart._chart_model.set_active_data_keys(values)
        self._bar_chart._refresh_widget_all_()

    def _set_data_(self, data, data_keys, data_key_names=None, data_type_dict=None):
        if data and data_keys:
            self._key_entry._set_value_options_(data_keys, data_key_names)
            active_data_keys = data_keys[:1]
            self._key_entry._set_value_(active_data_keys)

            self._bar_chart._set_data_(data, data_keys, active_data_keys, data_type_dict)

    def _set_name_text_(self, text):
        self._bar_chart._chart_model.set_name(text)

    def _export_all_to_(self, directory_path):
        self._bar_chart._chart_model.export(directory_path)

    def _do_export_(self):
        directory_path = _gui_core.GuiStorageDialog.save_directory(self)
        if directory_path:
            self._export_all_to_(directory_path)
            bsc_storage.StgDirectoryOpt(directory_path).show_in_system()

