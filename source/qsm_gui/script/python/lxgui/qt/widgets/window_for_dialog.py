# coding=utf-8
import enum

import sys

import six
# qt
from ..core.wrap import *

from .. import core as _qt_core

from .. import abstracts as _qt_abstracts

from . import base as _base

from . import utility as _utility

from . import input as _input

from . import button as _button


class _QtDialog(
    QtWidgets.QDialog,
    _qt_abstracts.AbsQtStatusBaseDef,
    _utility.QtThreadDef,
    _qt_abstracts.AbsQtMainWindowDef,
    _qt_abstracts.AbsQtShortcutBaseDef
):
    DEFAULT_SIZE = (240, 120)

    size_changed = qt_signal()

    key_escape_pressed = qt_signal()

    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_QtDialog, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        qt_palette = _qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)
        self.setAutoFillBackground(True)

        self.setFont(_qt_core.QtFonts.NameNormal)

        _qt_core.QtUtil.assign_qt_shadow(self, radius=2)

        self.installEventFilter(self)

        self._init_status_base_def_(self)
        self._init_window_base_def_(self)
        self._init_shortcut_base_def_(self)

        self._result = None

        self._verbose = False

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if not hasattr(event, 'type'):
                return False
            if event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Escape:
                    self.key_escape_pressed.emit()
            elif event.type() == QtCore.QEvent.Resize:
                self.size_changed.emit()
        return False

    def closeEvent(self, event):
        self._do_window_close_()
        event.accept()

    def _set_title_(self, text):
        self.setWindowTitle(text)

    def _do_ok_(self):
        if self._verbose is True:
            sys.stdout.write('you choose ok\n')

        self._result = True
        # todo: accept not trigger close event?
        self.accept()

    def _do_no_(self):
        if self._verbose is True:
            sys.stdout.write('you choose no\n')

        self._result = False
        self.reject()

    def _do_cancel_(self):
        if self._verbose is True:
            sys.stdout.write('you choose cancel\n')

        self._result = None
        self.reject()

    def _get_result_(self):
        return self._result

    def _connect_size_changed_to_(self, fnc):
        self.size_changed.connect(fnc)

    def _do_window_exec_(self, size=None):
        self._do_window_show_(
            size=size or self.DEFAULT_SIZE, use_exec=True
        )


class QtBaseDialog(_QtDialog):
    def __init__(self, *args, **kwargs):
        super(QtBaseDialog, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setWindowModality(QtCore.Qt.ApplicationModal)


class QtContentDialog(_QtDialog):
    class Buttons(enum.IntEnum):
        Ok = 0
        No = 1
        Cancel = 2

        All = -1

    def __init__(self, *args, **kwargs):
        super(QtContentDialog, self).__init__(*args, **kwargs)

        self._gui_build_()

        self._ok_python_script = None
        self._no_python_script = None
        self._cancel_python_script = None

    def _do_ok_(self):
        if self._verbose is True:
            sys.stdout.write('you choose Ok\n')
        self._result = True
        #
        self._execute_python_script_(self._ok_python_script)
        # mark close
        self._do_window_close_()
        # todo: accept not trigger close event?
        self.accept()

    def _do_no_(self):
        if self._verbose is True:
            sys.stdout.write('you choose no\n')
        self._result = False
        # mark close
        self._do_window_close_()
        self.reject()

    def _do_cancel_(self):
        if self._verbose is True:
            sys.stdout.write('you choose cancel\n')
        self._result = None
        # mark close
        self._do_window_close_()
        self.reject()

    def _gui_build_(self):
        self._set_icon_name_('log')

        lot = _base.QtVBoxLayout(self)
        lot.setContentsMargins(0, 0, 0, 0)
        self._central_qt_widget = _utility.QtWidget()
        lot.addWidget(self._central_qt_widget)
        self._central_qt_layout = _base.QtVBoxLayout(self._central_qt_widget)
        self._central_qt_layout.setContentsMargins(*[4]*4)

        sca = _utility.QtVScrollArea()
        self._central_qt_layout.addWidget(sca)
        self._message_input = _input.QtInputAsContent()
        sca._add_widget_(self._message_input)
        self._message_input._set_entry_enable_(False)

        self._wgt_bottom = _utility.QtWidget()
        self._wgt_bottom.setFixedHeight(24)
        sca._add_widget_(self._wgt_bottom)

        lot_bottom = _base.QtHBoxLayout(self._wgt_bottom)

        self._info_label = _utility.QtInfoLabel()
        lot_bottom.addWidget(self._info_label)

        qt_spacer_0 = _utility._QtSpacer()
        lot_bottom.addWidget(qt_spacer_0)
        #
        self._ok_button = _button.QtPressButton()
        self._ok_button._set_visible_(False)
        lot_bottom.addWidget(self._ok_button)
        self._set_ok_name_('Ok')
        self._ok_button.press_clicked.connect(self._do_ok_)
        #
        self._no_button = _button.QtPressButton()
        self._no_button._set_visible_(False)
        lot_bottom.addWidget(self._no_button)
        self._set_no_name_('No')
        self._no_button.press_clicked.connect(self._do_no_)
        #
        self._cancel_button = _button.QtPressButton()
        self._cancel_button._set_visible_(False)
        lot_bottom.addWidget(self._cancel_button)
        self._set_cancel_name_('Cancel')
        self._cancel_button.press_clicked.connect(self._do_cancel_)

        self._message_input.entry_focus_changed.connect(
            self._do_window_cancel_auto_close_
        )

    def _set_info_(self, text):
        self._info_label._set_info_(text)

    def _close_window_delay_as_fade_(self, delay_time):
        super(QtContentDialog, self)._close_window_delay_as_fade_(delay_time)
        self._do_window_auto_close_countdown_(delay_time)

    def _do_window_auto_close_countdown_(self, delay_time):
        def fnc_():
            if self._window_auto_close_flag is True:
                self._set_info_(
                    'close after {}s'.format(self._countdown_maximum)
                )
                self._countdown_maximum -= 1

                if self._countdown_maximum <= 0:
                    tmr.stop()
            else:
                self._set_info_('')
                tmr.stop()

        self._countdown_maximum = delay_time/1000
        tmr = QtCore.QTimer(self)
        tmr.timeout.connect(fnc_)
        tmr.start(1000)

    def _set_message_(self, text):
        self._message_input._set_value_(text)

    def _set_ok_visible_(self, boolean):
        self._ok_button._set_visible_(boolean)

    def _set_ok_name_(self, text):
        self._ok_button._set_name_text_(text)
        self._ok_button._fix_width_to_name_()

    def _set_ok_python_script_(self, script):
        self._ok_python_script = script

    @staticmethod
    def _execute_python_script_(script):
        if script is not None:
            # noinspection PyBroadException
            try:
                exec script
            except Exception:
                import traceback
                traceback.print_exc()

    def _set_no_visible_(self, boolean):
        self._no_button._set_visible_(boolean)

    def _set_no_name_(self, text):
        self._no_button._set_name_text_(text)
        self._no_button._fix_width_to_name_()

    def _set_no_python_script_(self, script):
        self._no_python_script = script

    def _set_cancel_visible_(self, boolean):
        self._cancel_button._set_visible_(boolean)

    def _set_cancel_name_(self, text):
        self._cancel_button._set_name_text_(text)
        self._cancel_button._fix_width_to_name_()

    def _set_cancel_python_script_(self, script):
        self._cancel_python_script = script

    def _do_show_(self):
        self._do_window_show_(
            size=self.DEFAULT_SIZE
        )

    def _set_buttons_(self, *args):
        buttons = [
            self._ok_button,
            self._no_button,
            self._cancel_button
        ]
        for i_idx, i_arg in enumerate(args):
            if i_arg:
                i_button = buttons[i_idx]
                i_button._set_visible_(True)
                if isinstance(i_arg, six.string_types):
                    i_button._set_name_text_(i_arg)
                    self._cancel_button._fix_width_to_name_()

    def _do_window_exec_(self, size=None):
        self._do_window_show_(
            size=size or self.DEFAULT_SIZE, use_exec=True
        )

    def _set_status_(self, status):
        self._central_qt_widget._set_status_(status)


class QtMessageDialog(QtContentDialog):
    def __init__(self, *args, **kwargs):
        super(QtMessageDialog, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setWindowModality(QtCore.Qt.ApplicationModal)


class QtNoticeDialog(QtContentDialog):
    def __init__(self, *args, **kwargs):
        super(QtNoticeDialog, self).__init__(*args, **kwargs)
        self.setWindowFlags(
            QtCore.Qt.Dialog | QtCore.Qt.WindowStaysOnTopHint
        )
        self._widget.setWindowModality(
            QtCore.Qt.NonModal
        )


class QtInputDialog(
    QtWidgets.QDialog,
    _qt_abstracts.AbsQtMainWindowDef,
):
    DEFAULT_SIZE = (320, 120)

    size_changed = qt_signal()
    key_escape_pressed = qt_signal()

    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtInputDialog, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        qt_palette = _qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)
        self.setAutoFillBackground(True)

        self.setFont(_qt_core.QtFonts.NameNormal)

        _qt_core.QtUtil.assign_qt_shadow(self, radius=2)

        self._init_window_base_def_(self)

        self.installEventFilter(self)

        self._result = None

        self._verbose = False

        self._gui_build_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if not hasattr(event, 'type'):
                return False
            if event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Escape:
                    self.key_escape_pressed.emit()
            elif event.type() == QtCore.QEvent.Resize:
                self.size_changed.emit()
        return False

    def closeEvent(self, event):
        self._do_window_close_()
        event.accept()

    def _set_title_(self, text):
        self.setWindowTitle(text)

    def _gui_build_(self):
        self._set_icon_name_('input')

        lot = _base.QtVBoxLayout(self)
        lot.setContentsMargins(0, 0, 0, 0)
        self._central_qt_widget = _utility.QtWidget()
        lot.addWidget(self._central_qt_widget)
        self._central_qt_layout = _base.QtVBoxLayout(self._central_qt_widget)
        self._central_qt_layout.setContentsMargins(*[2]*4)

        self._sca = _utility.QtVScrollArea()
        self._central_qt_layout.addWidget(self._sca)

        self._wgt_bottom = _utility.QtWidget()
        self._wgt_bottom.setFixedHeight(24)
        lot.addWidget(self._wgt_bottom)

        lot_bottom = _base.QtHBoxLayout(self._wgt_bottom)

        self._info_label = _utility.QtInfoLabel()
        lot_bottom.addWidget(self._info_label)

        qt_spacer_0 = _utility._QtSpacer()
        lot_bottom.addWidget(qt_spacer_0)

        self._ok_button = _button.QtPressButton()
        lot_bottom.addWidget(self._ok_button)
        self._ok_button._set_name_text_('Ok')
        self._ok_button._fix_width_to_name_()
        self._ok_button.press_clicked.connect(self._do_ok_)

        self._cancel_button = _button.QtPressButton()
        lot_bottom.addWidget(self._cancel_button)
        self._cancel_button._set_name_text_('Cancel')
        self._cancel_button._fix_width_to_name_()
        self._cancel_button.press_clicked.connect(self._do_cancel_)

    def _set_info_(self, text):
        self._info_label._set_info_(text)

    def _do_ok_(self):
        if self._verbose is True:
            sys.stdout.write('you choose ok\n')

        self._result = self._value_input._get_value_()
        # todo: accept not trigger close event?
        self.accept()

    def _do_cancel_(self):
        if self._verbose is True:
            sys.stdout.write('you choose cancel\n')

        self._result = None
        self.reject()

    def _set_value_type_(self, type_):
        if type_ in {'string', 'integer', 'float'}:
            self._value_input = _input.QtInputAsConstant()
            self._sca._add_widget_(self._value_input)
            self._value_input._set_entry_enable_(True)
            if type_ == 'integer':
                self._value_input._set_value_type_(int)
            elif type_ == 'float':
                self._value_input._set_value_type_(float)
            self._value_input._connect_input_user_entry_value_finished_to_(
                self._do_ok_
            )
        elif type_ in {'text'}:
            self._value_input = _input.QtInputAsContent()
            self._sca._add_widget_(self._value_input)
            self._value_input._set_entry_enable_(True)
            self._value_input._connect_input_user_entry_value_finished_to_(
                self._do_ok_
            )

    def _set_value_(self, value):
        self._value_input._set_value_(value)

    def _get_result_(self):
        return self._result

    def _do_window_exec_(self, size=None):
        self._value_input._entry_widget._set_focused_(True)
        self._do_window_show_(
            size=size or self.DEFAULT_SIZE, use_exec=True
        )


class QtToolDialog(
    QtWidgets.QDialog,
    _qt_abstracts.AbsQtMainWindowDef,
):
    DEFAULT_SIZE = (320, 240)

    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtToolDialog, self).__init__(*args, **kwargs)
        main_window = _qt_core.GuiQtDcc.get_qt_main_window()
        if main_window != self:
            self.setParent(
                main_window, _qt_core.QtCore.Qt.Window
            )
        # self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        qt_palette = _qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)
        self.setAutoFillBackground(True)

        self.setFont(_qt_core.QtFonts.NameNormal)

        _qt_core.QtUtil.assign_qt_shadow(self, radius=2)

        self._init_window_base_def_(self)

        self._result = None

        self._verbose = False

        self._gui_build_()

    def closeEvent(self, event):
        self._do_window_close_()
        event.accept()

    def _set_title_(self, text):
        self.setWindowTitle(text)

    def _gui_build_(self):
        self._set_icon_name_('tool/chart')

        lot = _base.QtVBoxLayout(self)
        lot.setContentsMargins(*[2]*4)
        self._central_qt_widget = _utility.QtWidget()
        lot.addWidget(self._central_qt_widget)
        self._central_qt_layout = _base.QtVBoxLayout(self._central_qt_widget)
        self._central_qt_layout.setContentsMargins(*[2]*4)

        central_wgt = _utility.QtWidget()
        lot.addWidget(central_wgt)
        self._central_lot = _base.QtVBoxLayout(central_wgt)
        self._central_lot.setContentsMargins(0, 0, 0, 0)
        self._central_lot.setSpacing(2)

        # bottom_wgt = _utility.QtWidget()
        # bottom_wgt.setFixedHeight(24)
        # lot.addWidget(bottom_wgt)
        # bottom_lot = _base.QtHBoxLayout(bottom_wgt)
        #
        # self._info_label = _utility.QtInfoLabel()
        # bottom_lot.addWidget(self._info_label)
        #
        # qt_spacer_0 = _utility._QtSpacer()
        # bottom_lot.addWidget(qt_spacer_0)
        #
        # self._close_button = _button.QtPressButton()
        # bottom_lot.addWidget(self._close_button)
        # self._close_button._set_name_text_('Close')
        # self._close_button._fix_width_to_name_()
        # self._close_button.press_clicked.connect(self._do_close_)

    def _set_info_(self, text):
        self._info_label._set_info_(text)

    def _do_close_(self):
        if self._verbose is True:
            sys.stdout.write('you choose close\n')

    def _add_widget_(self, widget):
        self._central_lot.addWidget(widget)

    def _do_window_exec_(self, size=None):
        self._do_window_show_(
            size=size or self.DEFAULT_SIZE, use_exec=True
        )

    def _get_result_(self):
        return
