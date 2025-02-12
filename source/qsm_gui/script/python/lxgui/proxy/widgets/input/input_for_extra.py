# coding:utf-8
import six

from .... import core as _gui_core

from ....qt.widgets import utility as _qt_wgt_utility

from ....qt.widgets import button as _qt_wgt_button

from ....qt.widgets.input import input_for_extend as _qt_wgt_ipt_for_extend

from . import _input_base


#   boolean as check box
class PrxInputForBoolean(_input_base.AbsPrxInput):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = _qt_wgt_button.QtCheckButton

    def __init__(self, *args, **kwargs):
        super(PrxInputForBoolean, self).__init__(*args, **kwargs)

        self._qt_input_widget._set_check_icon_file_paths_(
            _gui_core.GuiIcon.get('tag-filter-unchecked'),
            _gui_core.GuiIcon.get('tag-filter-checked')
        )

    def get(self):
        return self._qt_input_widget._is_checked_()

    def set(self, raw=None, **kwargs):
        self._qt_input_widget._set_checked_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_input_widget._set_value_default_(raw)

    def get_default(self):
        return self._qt_input_widget._get_value_default_()

    def get_is_default(self):
        return self._qt_input_widget._get_value_is_default_()

    def connect_input_changed_to(self, fnc):
        self._qt_input_widget._set_item_check_changed_connect_to_(fnc)


#   rgba
class PrxInputForRgbaChoose(_input_base.AbsPrxInputForConstant):
    QT_INPUT_WIDGET_CLS = _qt_wgt_ipt_for_extend.QtInputForRgba

    def __init__(self, *args, **kwargs):
        super(PrxInputForRgbaChoose, self).__init__(*args, **kwargs)


# icon choose
class PrxInputForIconChoose(_input_base.AbsPrxInput):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = _qt_wgt_ipt_for_extend.QtInputForIcon

    def __init__(self, *args, **kwargs):
        super(PrxInputForIconChoose, self).__init__(*args, **kwargs)
        self.widget.setFocusProxy(self._qt_input_widget)

    def get(self):
        return self._qt_input_widget._get_value_()

    def set(self, *args, **kwargs):
        _ = args[0]
        if isinstance(_, (tuple, list)):
            self._qt_input_widget._set_choose_values_(_)
            if _:
                self.set(_[-1])
                self.set_default(_[-1])
        elif isinstance(_, six.string_types):
            self._qt_input_widget._set_value_(_)
        elif isinstance(_, (int, float)):
            self._qt_input_widget._set_choose_value_by_index_(int(_))

    def set_default(self, *args, **kwargs):
        _ = args[0]
        if isinstance(_, six.string_types):
            self._qt_input_widget._set_value_default_(_)
        elif isinstance(_, (int, float)):
            self._qt_input_widget._set_choose_value_default_by_index_(_)

    def get_default(self):
        return self._qt_input_widget._get_value_default_()

    def set_locked(self, boolean):
        self._qt_input_widget._set_entry_enable_(not boolean)
