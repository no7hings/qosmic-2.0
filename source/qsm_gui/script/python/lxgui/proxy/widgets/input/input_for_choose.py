# coding:utf-8
import six
# gui
from .... import core as _gui_core

from ....qt.widgets import utility as _qt_wgt_utility

from ....qt.widgets.input import input_for_constant as _qt_wgt_ipt_for_constant

import _input_base


# any constant choose, etc. enumerate
class PrxInputForConstantChoose(_input_base.AbsPrxInput):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = _qt_wgt_ipt_for_constant.QtInputForConstantChoose

    def __init__(self, *args, **kwargs):
        super(PrxInputForConstantChoose, self).__init__(*args, **kwargs)
        self.widget.setFocusProxy(self._qt_input_widget)
        self._qt_input_widget._set_entry_enable_(True)
        self._qt_input_widget._set_choose_index_show_enable_(True)

    def get(self):
        return self._qt_input_widget._get_value_()

    def get_enumerate_strings(self):
        return self._qt_input_widget._get_choose_values_()

    def set(self, *args, **kwargs):
        _ = args[0]
        if isinstance(_, (tuple, list)):
            self._qt_input_widget._set_choose_values_(_)
            if _:
                self.set(_[-1])
                self.set_default(_[-1])
            else:
                self.set('')
                self.set_default('')
        elif isinstance(_, six.string_types):
            self._qt_input_widget._set_value_(_)
        elif isinstance(_, (int, float)):
            self._qt_input_widget._set_choose_value_by_index_(int(_))

    def set_options(self, *args, **kwargs):
        self._qt_input_widget._set_value_options_(args[0])

    def set_icon_file_as_value(self, value, file_path):
        self._qt_input_widget._set_choose_popup_item_icon_file_path_for_(
            value, file_path
        )

    def set_default(self, *args, **kwargs):
        _ = args[0]
        if isinstance(_, six.string_types):
            self._qt_input_widget._set_value_default_(_)
        elif isinstance(_, (int, float)):
            self._qt_input_widget._set_choose_value_default_by_index_(_)

    def get_default(self):
        return self._qt_input_widget._get_value_default_()

    def get_is_default(self):
        return self._qt_input_widget._get_value_is_default_()

    def connect_input_changed_to(self, fnc):
        self._qt_input_widget.input_choose_changed.connect(fnc)

    def set_locked(self, boolean):
        self._qt_input_widget._set_entry_enable_(not boolean)


class PrxInputForSchemeChoose(_input_base.AbsPrxInput):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = _qt_wgt_ipt_for_constant.QtInputForConstantChoose
    #
    HISTORY_KEY = 'gui.schemes'

    def __init__(self, *args, **kwargs):
        super(PrxInputForSchemeChoose, self).__init__(*args, **kwargs)
        #
        self._qt_input_widget._set_entry_enable_(True)
        #
        self._scheme_key = None
        #
        self.update_history()
        #
        self._qt_input_widget._connect_input_user_entry_value_finished_to_(self.update_history)
        self._qt_input_widget.user_input_choose_changed.connect(self.update_history)

    def get(self):
        return self._qt_input_widget._get_value_()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (tuple, list)):
            self.set_history_add(raw[0])
            self.update_history()
            self.pull_history_latest()

    def set_default(self, raw, **kwargs):
        self._qt_input_widget._set_value_default_(raw)

    def get_is_default(self):
        return self._qt_input_widget._get_value_is_default_()

    def set_scheme_key(self, key):
        self._scheme_key = key

    def connect_input_changed_to(self, fnc):
        self._qt_input_widget._connect_input_entry_value_changed_to_(fnc)

    #
    def get_histories(self):
        if self._scheme_key is not None:
            return _gui_core.GuiHistory.get_all(
                self._scheme_key
            )
        return []

    def set_history_add(self, scheme):
        if self._scheme_key is not None:
            _gui_core.GuiHistory.append(
                self._scheme_key,
                scheme
            )

    #
    def update_history(self):
        if self._scheme_key is not None:
            scheme = self._qt_input_widget._get_value_()
            if scheme:
                _gui_core.GuiHistory.append(
                    self._scheme_key,
                    scheme
                )
            #
            histories = _gui_core.GuiHistory.get_all(
                self._scheme_key
            )
            if histories:
                histories = [i for i in histories if i]
                histories.reverse()
                #
                self._qt_input_widget._set_choose_values_(
                    histories
                )

    def pull_history_latest(self):
        if self._scheme_key is not None:
            _ = _gui_core.GuiHistory.get_latest(self._scheme_key)
            if _:
                self._qt_input_widget._set_value_(_)
