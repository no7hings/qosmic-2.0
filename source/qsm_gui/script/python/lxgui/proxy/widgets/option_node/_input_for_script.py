# coding:utf-8
from ....qt.widgets import utility as _qt_wgt_utility

from ....qt.widgets import input as _qt_wgt_input

import _base

import _input_base


#   script
class PrxInputForScript(_input_base.AbsPrxInput):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = _qt_wgt_input.QtInputAsContent

    def __init__(self, *args, **kwargs):
        super(PrxInputForScript, self).__init__(*args, **kwargs)
        self.widget.setFixedHeight(_base.OptionNodeBase.PortHeightA)
        #
        self._qt_input_widget._get_resize_handle_()._set_resize_target_(self.widget)
        self._qt_input_widget._set_resize_enable_(True)
        self._qt_input_widget._set_input_entry_drop_enable_(True)
        self._qt_input_widget._set_item_value_entry_enable_(True)
        self._qt_input_widget._set_size_policy_height_fixed_mode_()

    def get(self):
        return self._qt_input_widget._get_value_()

    def set(self, raw=None, **kwargs):
        self._qt_input_widget._set_value_(raw)

    def set_external_editor_ext(self, ext):
        self._qt_input_widget._set_external_editor_ext_(ext)

    def set_default(self, raw, **kwargs):
        self._qt_input_widget._set_value_default_(raw)

    def get_is_default(self):
        return self._qt_input_widget._get_value_is_default_()

    def set_locked(self, boolean):
        self._qt_input_widget._set_entry_enable_(not boolean)