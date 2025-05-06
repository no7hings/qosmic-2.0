# coding=utf-8
# gui
from .... import core as _gui_core
# qt
from ...core.wrap import *

from ... import abstracts as _qt_abstracts
# qt widgets
from .. import base as _wgt_base

from ..entry import entry_for_tag as _entry_for_tag


class QtInputForTag(
    QtWidgets.QWidget,

    _qt_abstracts.AbsQtInputBaseDef,
):
    QT_ENTRY_CLS = _entry_for_tag.QtEntryForTag

    def _pull_history_fnc_(self, *args, **kwargs):
        self._entry_widget._set_value_(args[0])

    def __init__(self, *args, **kwargs):
        super(QtInputForTag, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )

        self._init_input_base_def_(self)
        self._build_input_entry_(str)

    def _build_input_entry_(self, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type

        entry_layout = _wgt_base.QtHBoxLayout(self)
        entry_layout.setContentsMargins(*[1]*4)
        entry_layout.setSpacing(4)

        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)

        self.input_value_changed = self._entry_widget.value_changed
        self.user_input_value_changed = self._entry_widget.user_value_changed
        self.user_input_value_accepted = self._entry_widget.user_value_accepted

        self.user_input_value_accepted.connect(
            self._push_history_fnc_
        )

    def _set_value_options_(self, values, names=None):
        self._entry_widget._set_value_options_(values, names)

    def _set_value_by_index_(self, index):
        self._entry_widget._set_value_by_index_(index)

    def _set_value_type_(self, value_type):
        self._value_type = value_type
        if value_type == str:
            self._entry_widget._set_use_exclusive_(True)
        elif value_type == list:
            self._entry_widget._set_use_exclusive_(False)
        else:
            raise RuntimeError()

    def _set_entry_enable_(self, boolean):
        super(QtInputForTag, self)._set_entry_enable_(boolean)
        self._entry_widget._set_entry_enable_(boolean)

    def _set_tool_tip_(self, text, **kwargs):
        self._entry_widget._set_tool_tip_(text, **kwargs)