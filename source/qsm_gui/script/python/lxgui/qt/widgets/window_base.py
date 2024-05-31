# coding=utf-8
# qt
import copy
import enum

import sys

import six

import lxbasic.web as bsc_web

from ..core.wrap import *

from .. import core as _qt_core

from .. import abstracts as _qt_abstracts

from . import base as _base

from . import utility as _utility

from . import input as _message_input

from . import button as _button


class AbsQtShortcutBaseDef(object):
    def _init_shortcut_base_def_(self, widget):
        self._widget = widget

    def _create_window_shortcut_action_for_(self, fnc, shortcut):
        act = QtWidgets.QAction(self)
        # noinspection PyUnresolvedReferences
        act.triggered.connect(fnc)
        act.setShortcut(QtGui.QKeySequence(shortcut))
        act.setShortcutContext(QtCore.Qt.WindowShortcut)
        self._widget.addAction(act)

    def _create_widget_shortcut_action_for_(self, fnc, shortcut):
        act = QtWidgets.QAction(self)
        # noinspection PyUnresolvedReferences
        act.triggered.connect(fnc)
        act.setShortcut(QtGui.QKeySequence(shortcut))
        act.setShortcutContext(QtCore.Qt.WidgetWithChildrenShortcut)
        self._widget.addAction(act)


class AbsQtMainWindowDef(object):
    window_close_accepted = qt_signal(object)

    def _init_window_base_def_(self, widget):
        self._widget = widget
        self._window_close_fncs = []

        self._window_ask_for_close = False

        self._definition_window_size = 240, 120

        self._window_close_flag = False

        self._window_auto_close_flag = None

        self._window_opacity = 1.0

    def _do_window_close_later_(self, delay_time):
        tmr = QtCore.QTimer(self)
        tmr.timeout.connect(self._do_window_close_)
        tmr.start(delay_time)

    def _do_window_auto_close_later_(self, delay_time):
        self._window_auto_close_flag = True

        tmr = QtCore.QTimer(self)
        tmr.timeout.connect(self._do_window_close_as_fade_)
        tmr.start(delay_time)

    def _do_window_cancel_auto_close_(self):
        self._window_auto_close_flag = False

    def _do_window_close_as_fade_(self):
        if self._window_auto_close_flag is not True:
            return

        def fnc_():
            self._window_opacity -= .1
            self._widget.setWindowOpacity(self._window_opacity)
            if self._window_opacity <= .1:
                tmr.stop()
                self._do_window_close_()

        tmr = QtCore.QTimer(self)
        tmr.timeout.connect(fnc_)
        tmr.start(250)

    def _connect_window_close_to_(self, fnc):
        self._window_close_fncs.append(fnc)

    def _do_window_close_(self):
        if self._window_close_flag is False:
            if self._window_close_fncs:
                for i in self._window_close_fncs:
                    i()

            self.window_close_accepted.emit(self)

            self._widget.close()
            self._widget.deleteLater()

            self._window_close_flag = True

    def _set_window_ask_for_close_enable_(self, boolean):
        self._window_ask_for_close = boolean

    def _set_definition_window_size_(self, size):
        self._definition_window_size = size
        self._widget.setBaseSize(
            QtCore.QSize(*self._definition_window_size)
        )

    def _do_window_show_(self, pos=None, size=None, use_exec=False):
        _qt_core.GuiQtUtil.show_qt_window(
            self._widget, pos, size, use_exec
        )


    def _set_icon_name_text_(self, text):
        self._widget.setWindowIcon(
            _qt_core.GuiQtIcon.generate_by_text(text)
        )

    def _set_icon_name_(self, icon_name):
        self._widget.setWindowIcon(
            _qt_core.GuiQtIcon.create_by_icon_name(icon_name)
        )


class QtDialogBase(
    QtWidgets.QDialog,
    #
    _qt_abstracts.AbsQtStatusBaseDef,
    #
    _utility.QtThreadDef,
    AbsQtMainWindowDef,
    AbsQtShortcutBaseDef
):
    size_changed = qt_signal()

    key_escape_pressed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtDialogBase, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #
        qt_palette = _qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)
        self.setAutoFillBackground(True)
        #
        self.setFont(_qt_core.QtFonts.NameNormal)
        #
        _qt_core.GuiQtUtil.assign_qt_shadow(self, radius=2)
        #
        self.installEventFilter(self)
        #
        self._init_status_base_def_(self)
        self._init_window_base_def_(self)
        self._init_shortcut_base_def_(self)

        self._result = False

        self._verbose = False

    def _refresh_widget_draw_(self):
        self.update()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if hasattr(event, 'type'):
                if event.type() == QtCore.QEvent.KeyPress:
                    if event.key() == QtCore.Qt.Key_Escape:
                        self.key_escape_pressed.emit()
                elif event.type() == QtCore.QEvent.Resize:
                    self.size_changed.emit()
        return False

    def closeEvent(self, event):
        self._do_window_close_()
        event.accept()

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
        self._result = False
        self.reject()

    def _get_result_(self):
        return self._result

    def _connect_size_changed_to_(self, fnc):
        self.size_changed.connect(fnc)
        

class QtDialogWindow(QtDialogBase):
    def __init__(self, *args, **kwargs):
        super(QtDialogWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setWindowModality(QtCore.Qt.ApplicationModal)


class QtMessageBase(QtDialogBase):
    BUTTON_WIDTH = 32
    DEFAULT_SIZE = (240, 120)

    class Buttons(enum.IntEnum):
        Ok = 0
        No = 1
        Cancel = 2

        All = -1

    def __init__(self, *args, **kwargs):
        super(QtMessageBase, self).__init__(*args, **kwargs)

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
        self._result = False
        # mark close
        self._do_window_close_()
        self.reject()

    def _gui_build_(self):
        self._set_icon_name_('log')

        lot = _base.QtVBoxLayout(self)
        lot.setContentsMargins(0, 0, 0, 0)
        self._central_widget = _utility.QtWidget()
        lot.addWidget(self._central_widget)
        self._central_layout = _base.QtVBoxLayout(self._central_widget)
        self._central_layout.setContentsMargins(*[4]*4)

        sca = _utility.QtVScrollArea()
        self._central_layout.addWidget(sca)
        self._message_input = _message_input.QtInputAsContent()
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
        self._cancel_button.press_clicked.connect(self._do_no_)

        self._message_input.entry_focus_changed.connect(
            self._do_window_cancel_auto_close_
        )

    def _set_title_(self, text):
        self.setWindowTitle(text)

    def _set_info_(self, text):
        self._info_label._set_info_(text)

    def _do_window_auto_close_later_(self, delay_time):
        super(QtMessageBase, self)._do_window_auto_close_later_(delay_time)
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
                pass

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

    def _do_exec_(self):
        self._do_window_show_(
            size=self.DEFAULT_SIZE, use_exec=True
        )

    def _set_status_(self, status):
        self._central_widget._set_status_(status)


class QtMessageBox(QtMessageBase):
    def __init__(self, *args, **kwargs):
        super(QtMessageBox, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setWindowModality(QtCore.Qt.ApplicationModal)


class QtNoticeBox(QtMessageBase):
    def __init__(self, *args, **kwargs):
        super(QtNoticeBox, self).__init__(*args, **kwargs)
        self.setWindowFlags(
            QtCore.Qt.Dialog | QtCore.Qt.WindowStaysOnTopHint
        )
        self._widget.setWindowModality(
            QtCore.Qt.NonModal
        )


class AbsNoticeBaseDef(object):
    def _init_notice_base_def_(self, widget):
        self._widget = widget

        self._notice_widgets = []

        rect = _qt_core.GuiQtUtil.get_qt_desktop_primary_rect()

        self._w_i, self._h_i = 240, 120
        self._x_d, self._y_d = rect.x(), rect.y()
        self._w_d, self._h_d = rect.width(), rect.height()

        self._layout_model = _qt_core.GuiQtModForGridLayout()
        self._layout_model.set_pos(0, 0)
        self._layout_model.set_size(self._h_d, self._w_d)
        self._layout_model.set_item_size(
            self._h_i+28, self._w_i
        )

    def _notice_close_fnc_(self, widget):
        if widget in self._notice_widgets:
            self._notice_widgets.remove(widget)

    def _get_notice_window_geometry_(self):
        c = len(self._notice_widgets)
        self._layout_model.set_count(c)
        self._layout_model.update()
        x_0, y_0, w_0, h_0 = self._layout_model.get_geometry_at(c-1)
        x, y = self._w_d-self._w_i-y_0, self._h_d-self._h_i-x_0
        return x, y, self._w_i, self._h_i

    def _notice_show_fnc_(self, widget):
        widget.show()
        widget.setGeometry(
            *self._get_notice_window_geometry_()
        )
        delay_time = 5000
        widget._do_window_auto_close_later_(delay_time)

    def _do_notice_close_all_(self):
        # list maybe dynamic
        s = copy.copy(self._notice_widgets)
        for i_window in s:
            if i_window._window_close_flag is False:
                i_window._do_window_close_()

    def _show_notice_(self, text):
        wgt = QtNoticeBox()
        # append first
        self._notice_widgets.append(wgt)
        wgt._set_buttons_(True, True)

        wgt.window_close_accepted.connect(
            self._notice_close_fnc_
        )
        wgt._set_title_('Notice')
        options = bsc_web.UrlOptions.to_dict(text)
        if options:
            title = options.get('title')
            if title:
                wgt._set_title_(title)

            message = options.get('message')
            if message:
                wgt._set_message_(message)

            status = options.get('status')
            if status:
                if status == 'error':
                    wgt._set_status_(
                        wgt.ValidationStatus.Error
                    )
                elif status == 'warning':
                    wgt._set_status_(
                        wgt.ValidationStatus.Warning
                    )
            
            ok_python_script = options.get('ok_python_script')
            if ok_python_script:
                wgt._set_ok_python_script_(ok_python_script)
        else:
            wgt._set_message_(text)

        self._notice_show_fnc_(wgt)


class QtMainWindow(
    QtWidgets.QMainWindow,
    #
    _qt_abstracts.AbsQtBusyBaseDef,
    _qt_abstracts.AbsQtActionBaseDef,
    #
    _qt_abstracts.AbsQtThreadBaseDef,
    #
    _utility.QtThreadDef,
    AbsQtMainWindowDef,
    AbsQtShortcutBaseDef,
    AbsNoticeBaseDef
):
    close_clicked = qt_signal()
    key_escape_pressed = qt_signal()
    key_help_pressed = qt_signal()
    size_changed = qt_signal()
    window_activate_changed = qt_signal()

    window_loading_finished = qt_signal()

    QSM_WINDOW_FLAG = True

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        m_h = self.menuBar().height()
        self._rect_frame_draw.setRect(
            x, y, w, h
        )
        self._menu_frame_draw_rect.setRect(
            x, y, w, m_h
        )

    def __init__(self, *args, **kwargs):
        super(QtMainWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # todo: do not use WA_TranslucentBackground mode, GL bug
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self.setPalette(_qt_core.GuiQtDcc.generate_qt_palette())
        self.setAutoFillBackground(True)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self.setFont(_qt_core.QtFonts.NameNormal)
        #
        _qt_core.GuiQtUtil.assign_qt_shadow(self, radius=2)
        #
        self._window_system_tray_icon = None
        self._init_busy_base_def_(self)
        self._init_action_base_def_(self)
        self._init_thread_base_def_(self)
        self._init_window_base_def_(self)
        self._init_shortcut_base_def_(self)
        self._init_notice_base_def_(self)
        #
        self.setStyleSheet(
            _qt_core.GuiQtStyle.get('QMainWindow')
        )
        self.menuBar().setStyleSheet(
            _qt_core.GuiQtStyle.get('QMenuBar')
        )
        self._rect_frame_draw = QtCore.QRect()
        self._menu_frame_draw_rect = QtCore.QRect()

        self.installEventFilter(self)

        self._connect_window_close_to_(
            self._do_notice_close_all_
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if hasattr(event, 'type'):
                # if event.type() == QtCore.QEvent.Close:
                #     self.hide()
                #     self._do_window_close_()
                if event.type() == QtCore.QEvent.KeyPress:
                    if event.key() == QtCore.Qt.Key_Escape:
                        self.key_escape_pressed.emit()
                elif event.type() == QtCore.QEvent.Resize:
                    self.size_changed.emit()
                elif event.type() == QtCore.QEvent.WindowActivate:
                    self.window_activate_changed.emit()
                elif event.type() == QtCore.QEvent.WindowDeactivate:
                    self.window_activate_changed.emit()
                # elif event.type() == QtCore.QEvent.ShortcutOverride:
                #     if event.key() == QtCore.Qt.Key_Space:
                #         event.ignore()
        return False

    def paintEvent(self, event):
        self._refresh_widget_draw_geometry_()
        painter = _qt_core.QtPainter(self)
        painter.fillRect(
            self._rect_frame_draw,
            _qt_core.QtBackgroundColors.Basic
        )
        painter.fillRect(
            self._menu_frame_draw_rect,
            _qt_core.QtBackgroundColors.Dark
        )

    def closeEvent(self, event):
        if self._window_ask_for_close is True:
            w = QtMessageBox(self)
            w._set_title_('Close Window')
            w._set_ok_visible_(True)
            w._set_no_visible_(True)
            w._set_message_('Are you sure you want to close the window?')
            w._do_exec_()
            if w._get_result_():
                self._do_window_close_()
                event.accept()
            else:
                event.ignore()
        else:
            self._do_window_close_()
            event.accept()

    def _exec_message_(self, message):
        w = QtMessageBox(self)
        w._set_title_('Message')
        w._set_ok_visible_(True)
        w._set_no_visible_(True)
        w._set_message_(message)
        w._do_exec_()

    def _set_icon_name_text_(self, text):
        self.setWindowIcon(
            _qt_core.GuiQtIcon.generate_by_text(text)
        )

    def _set_icon_name_(self, icon_name):
        self.setWindowIcon(
            _qt_core.GuiQtIcon.create_by_icon_name(icon_name)
        )

    def _set_window_system_tray_icon_(self, widget):
        self._window_system_tray_icon = widget

    def _connect_size_changed_to_(self, fnc):
        self.size_changed.connect(fnc)
