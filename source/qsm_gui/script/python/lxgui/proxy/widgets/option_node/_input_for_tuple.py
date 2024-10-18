# coding:utf-8
from ....qt.widgets import utility as _qt_wgt_utility

from ....qt.widgets import input as _qt_wgt_input

import _input_base


# tuple
class AbsPrxInputForTuple(_input_base.AbsPrxInput):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = _qt_wgt_input.QtInputAsTuple

    def __init__(self, *args, **kwargs):
        super(AbsPrxInputForTuple, self).__init__(*args, **kwargs)

    def set_value_type(self, value_type):
        self._qt_input_widget._set_value_type_(value_type)

    def set_value_size(self, size):
        self._qt_input_widget._set_value_size_(size)

    def get(self):
        return self._qt_input_widget._get_value_()

    def set(self, raw=None, **kwargs):
        self._qt_input_widget._set_value_(
            raw
        )

    def set_default(self, raw, **kwargs):
        self._qt_input_widget._set_value_default_(raw)

    def get_is_default(self):
        return self._qt_input_widget._get_value_is_default_()

    def connect_input_changed_to(self, fnc):
        self._qt_input_widget._connect_input_entry_value_changed_to_(fnc)

    def set_locked(self, boolean):
        self._qt_input_widget._set_entry_enable_(
            not boolean
        )


#   integer2, 3, ...
class PrxInputForIntegerTuple(AbsPrxInputForTuple):
    def __init__(self, *args, **kwargs):
        super(PrxInputForIntegerTuple, self).__init__(*args, **kwargs)
        self._qt_input_widget._build_input_entry_(2, int)


#   float2, 3, ...
class PrxInputForFloatTuple(AbsPrxInputForTuple):
    def __init__(self, *args, **kwargs):
        super(PrxInputForFloatTuple, self).__init__(*args, **kwargs)
        self._qt_input_widget._build_input_entry_(2, float)