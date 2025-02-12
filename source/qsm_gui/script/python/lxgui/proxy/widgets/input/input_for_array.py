# coding:utf-8
# gui
from .... import core as _gui_core

from ....qt.widgets import utility as _qt_wgt_utility

from ....qt.widgets.input import input_for_array as _qt_wgt_ipt_for_array
# proxy widgets
from .. import utility as _wgt_utility

from . import _input_base


# any array
class PrxInputForArray(_input_base.AbsPrxInput):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = _qt_wgt_ipt_for_array.QtInputForArray

    def __init__(self, *args, **kwargs):
        super(PrxInputForArray, self).__init__(*args, **kwargs)
        self._history_key = 'gui.values'
        #
        self._qt_input_widget._set_entry_enable_(True)
        self._qt_input_widget._get_resize_handle_()._set_resize_target_(self.widget)
        self._qt_input_widget._set_resize_enable_(True)
        self._qt_input_widget._get_resize_handle_()._set_resize_minimum_(42)
        self._qt_input_widget._set_size_policy_height_fixed_mode_()
        self._qt_input_widget._set_value_choose_button_icon_file_path_(
            _gui_core.GuiIcon.get('attribute')
        )

        self.widget.setFixedHeight(_gui_core.GuiSize.InputHeightA)

        self._add_button = _wgt_utility.PrxIconPressButton()
        self._qt_input_widget._add_input_button_(self._add_button.widget)
        self._add_button.connect_press_clicked_to(self._set_add_)
        self._add_button.set_name('add')
        self._add_button.set_icon_name('add')
        self._add_button.set_icon_frame_size(18, 18)
        self._add_button.set_tool_tip(
            [
                '"LMB-click" add a value'
            ]
        )

    def _set_add_(self):
        pass

    def get(self):
        return self._qt_input_widget._get_values_()

    def set(self, raw=None, **kwargs):
        pass

    def append(self, value):
        self._qt_input_widget._append_value_(
            value
        )

    def remove(self, value):
        self._qt_input_widget._remove_value_(
            value
        )


# any array choose
# noinspection PyUnusedLocal
class PrxInputForArrayChoose(_input_base.AbsPrxInput):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = _qt_wgt_ipt_for_array.QtInputForArrayChoose

    def __init__(self, *args, **kwargs):
        super(PrxInputForArrayChoose, self).__init__(*args, **kwargs)
        self._history_key = 'gui.values_choose'
        #
        self._qt_input_widget._set_entry_enable_(True)
        self._qt_input_widget._get_resize_handle_()._set_resize_target_(self.widget)
        self._qt_input_widget._set_resize_enable_(True)
        self._qt_input_widget._get_resize_handle_()._set_resize_minimum_(42)
        self._qt_input_widget._set_size_policy_height_fixed_mode_()
        self._qt_input_widget._set_value_choose_button_icon_file_path_(
            _gui_core.GuiIcon.get('attribute')
        )

        self.widget.setFixedHeight(_gui_core.GuiSize.InputHeightA)

    def _set_add_(self):
        pass

    def get(self):
        pass

    def set(self, *args, **kwargs):
        pass

    def set_choose_values(self, *args, **kwargs):
        self._qt_input_widget._clear_choose_values_()
        self._qt_input_widget._restore_choose_popup_()
        self._qt_input_widget._set_choose_values_(args[0])

    def append(self, value):
        pass
