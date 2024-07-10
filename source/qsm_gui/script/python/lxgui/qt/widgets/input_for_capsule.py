# coding=utf-8
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import abstracts as _qt_abstracts
# qt widgets
from ..widgets import base as _base

from ..widgets import entry_for_capsule as _entry_for_capsule


class QtInputAsCapsule(
    QtWidgets.QWidget,

    _qt_abstracts.AbsQtInputBaseDef,
):
    def _pull_history_(self, *args, **kwargs):
        self._entry_widget._set_value_(args[0])

    QT_ENTRY_CLS = _entry_for_capsule.QtEntryAsCapsule

    def __init__(self, *args, **kwargs):
        super(QtInputAsCapsule, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(gui_core.GuiSize.InputHeight)

        self._init_input_base_def_(self)
        self._build_input_entry_(str)

    def _build_input_entry_(self, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type
        #
        entry_layout = _base.QtHBoxLayout(self)
        entry_layout.setContentsMargins(*[1] * 4)
        entry_layout.setSpacing(4)
        #
        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)

        self.input_value_changed = self._entry_widget.value_changed
        self.user_input_value_changed = self._entry_widget.user_value_changed
        self.user_input_value_accepted = self._entry_widget.user_value_accepted
        
        self.user_input_value_accepted.connect(
            self._push_history_
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
        super(QtInputAsCapsule, self)._set_entry_enable_(boolean)
        self._entry_widget._set_entry_enable_(boolean)

    def _set_tool_tip_(self, text, **kwargs):
        self._entry_widget._set_tool_tip_(text, **kwargs)