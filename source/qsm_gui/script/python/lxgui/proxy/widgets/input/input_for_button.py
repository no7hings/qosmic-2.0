# coding:utf-8
import six

import functools

import types
# gui
from .... import core as _gui_core

from ....qt.widgets import utility as _qt_wgt_utility

from ....qt.widgets import button as _qt_wgt_button
# proxy widgets
from .. import utility as _utility

import _input_base


# press button
class PrxInputForPressButton(_input_base.AbsPrxInput):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = _qt_wgt_button.QtPressButton

    def __init__(self, *args, **kwargs):
        super(PrxInputForPressButton, self).__init__(*args, **kwargs)

    def get(self):
        return None

    @_gui_core.GuiModifier.run_with_exception_catch
    def __exec_fnc(self, fnc):
        fnc()

    @staticmethod
    @_gui_core.GuiModifier.run_with_exception_catch
    def __exec_scp(script):
        exec script

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (types.MethodType, types.FunctionType, functools.partial, types.LambdaType)):
            self._qt_input_widget.press_clicked.connect(
                functools.partial(self.__exec_fnc, raw)
            )
        elif isinstance(raw, six.string_types):
            self._qt_input_widget.press_clicked.connect(
                functools.partial(self.__exec_scp, raw)
            )

    def set_menu_enable(self, boolean):
        self._qt_input_widget._set_menu_enable_(boolean)

    def set_menu_data(self, data):
        self._qt_input_widget._set_menu_data_(data)

    def set_menu_content(self, content):
        self._qt_input_widget._set_menu_content_(content)

    def set_name_icon_text(self, text):
        self._qt_input_widget._set_name_icon_text_(text)

    def set_option_enable(self, boolean):
        self._qt_input_widget._set_option_click_enable_(boolean)

    def set_icon_by_file(self, file_path):
        self._qt_input_widget._set_icon_file_path_(file_path)


# sub process button
class PrxInputForSpcButton(_input_base.AbsPrxInput):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = _qt_wgt_button.QtPressButton

    def __init__(self, *args, **kwargs):
        super(PrxInputForSpcButton, self).__init__(*args, **kwargs)
        self._stop_button = _utility.PrxIconPressButton()
        self.add_button(self._stop_button)
        self._stop_button.set_name('Stop Process')
        self._stop_button.set_icon_by_text('Stop Process')
        self._stop_button.set_tool_tip('press to stop process')

    def get(self):
        return None

    @_gui_core.GuiModifier.run_with_exception_catch
    def __exec_fnc(self, fnc):
        fnc()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (types.MethodType, types.FunctionType)):
            self._qt_input_widget.press_clicked.connect(
                functools.partial(self.__exec_fnc, raw)
            )

    def set_menu_data(self, raw):
        self._qt_input_widget._set_menu_data_(raw)

    def set_stop(self, raw):
        if isinstance(raw, (types.MethodType, types.FunctionType)):
            self._stop_button.widget.press_clicked.connect(
                functools.partial(self.__exec_fnc, raw)
            )

    def set_stop_connect_to(self, fnc):
        self._stop_button.widget.press_clicked.connect(
            functools.partial(self.__exec_fnc, fnc)
        )

    def set_icon_by_file(self, file_path):
        self._qt_input_widget._set_icon_file_path_(file_path)


# validation button
class PrxInputForValidateButton(_input_base.AbsPrxInput):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = _qt_wgt_button.QtPressButton

    def __init__(self, *args, **kwargs):
        super(PrxInputForValidateButton, self).__init__(*args, **kwargs)

    def get(self):
        return None

    @_gui_core.GuiModifier.run_with_exception_catch
    def __exec_fnc(self, fnc):
        fnc()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (types.MethodType, types.FunctionType)):
            self._qt_input_widget.press_clicked.connect(
                functools.partial(self.__exec_fnc, raw)
            )

    def set_menu_data(self, raw):
        self._qt_input_widget._set_menu_data_(raw)
