# coding:utf-8
from ....qt.widgets import utility as _qt_wgt_utility

from ....qt.widgets import input_for_capsule as _qt_wgt_input_for_capsule

import _input_base


#   capsule
class PrxInputForCapsule(_input_base.AbsPrxInput):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = _qt_wgt_input_for_capsule.QtInputAsCapsule

    def __init__(self, *args, **kwargs):
        super(PrxInputForCapsule, self).__init__(*args, **kwargs)

    def get(self):
        return self._qt_input_widget._get_value_()

    def set(self, *args, **kwargs):
        self._qt_input_widget._set_value_(
            args[0]
        )

    def set_locked(self, boolean):
        self._qt_input_widget._set_entry_enable_(not boolean)

    def set_default(self, *args, **kwargs):
        self._qt_input_widget._set_value_default_(
            args[0]
        )

    def get_default(self):
        return self._qt_input_widget._get_value_default_()

    def get_is_default(self):
        return self._qt_input_widget._get_value_is_default_()

    def set_options(self, *args, **kwargs):
        self._qt_input_widget._set_value_options_(
            *args, **kwargs
        )

    def connect_input_changed_to(self, fnc):
        self._qt_input_widget.input_value_changed.connect(fnc)

    def connect_user_input_changed_to(self, fnc):
        self._qt_input_widget.user_input_value_changed.connect(fnc)
