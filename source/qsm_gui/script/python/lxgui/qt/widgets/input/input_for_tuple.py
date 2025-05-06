# coding=utf-8
# gui
from .... import core as _gui_core
# qt
from ....qt.core.wrap import *

from ....qt import core as _qt_core

from ....qt import abstracts as _qt_abstracts
# qt widgets
from .. import base as _wgt_base

from .. import entry_frame as _wgt_entry_frame

from ..entry import entry_for_constant as _entry_for_constant


# any tuple, etc. float2, float3, ...
class QtInputForTuple(
    _wgt_entry_frame.QtEntryFrame,
    _qt_abstracts.AbsQtNameBaseDef,
    _qt_abstracts.AbsQtInputForComponentsBaseDef,
):
    def _pull_history_fnc_(self, *args, **kwargs):
        pass

    QT_ENTRY_CLS = _entry_for_constant.QtEntryForConstant

    entry_value_changed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtInputForTuple, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(_gui_core.GuiSize.InputHeight)

        self._init_name_base_def_(self)
        self._init_input_as_components_base_def_(self)
        # create entry layout first
        self._entry_layout = _wgt_base.QtHBoxLayout(self)
        self._entry_layout.setContentsMargins(2, 2, 2, 2)
        self._entry_layout.setSpacing(8)
        self._build_input_entry_(2, self._value_type)

    def _build_input_entry_(self, value_size, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type

        if self._value_entries:
            _qt_core.GuiQtLayout.clear_all_widgets(self._entry_layout)

        self._value_entries = []

        self._set_entry_count_(value_size)
        if value_size:
            for i in range(value_size):
                i_widget = self.QT_ENTRY_CLS()
                i_widget._set_value_type_(self._value_type)
                self._entry_layout.addWidget(i_widget)
                self._value_entries.append(i_widget)

    def _set_entry_enable_(self, boolean):
        for i in self._value_entries:
            i._set_entry_enable_(boolean)

        self._update_background_color_by_locked_(boolean)

        self._refresh_widget_all_()

    def _set_action_enable_(self, boolean):
        self._set_entry_enable_(boolean)
