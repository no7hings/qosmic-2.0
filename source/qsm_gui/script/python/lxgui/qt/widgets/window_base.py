# coding=utf-8
import copy

import lxbasic.web as bsc_web

from ... import core as _gui_core
# qt
from ..core.wrap import *

from .. import core as _qt_core

from .. import abstracts as _qt_abstracts

from . import utility as _utility

from . import bubble as _bubble

from . import window_for_dialog as _window_for_dialog


class AbsWindowNoticeBaseDef(object):
    def _init_window_notice_base_def_(self, widget):
        self._widget = widget

        self._notice_widgets = []

        rect = _qt_core.QtUtil.get_qt_desktop_primary_rect()

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
        return int(x), int(y), int(self._w_i), int(self._h_i)

    def _notice_show_fnc_(self, widget):
        widget.show()
        widget.setGeometry(
            *self._get_notice_window_geometry_()
        )
        delay_time = 5000
        widget._close_window_delay_as_fade_(delay_time)

    def _do_notice_close_all_(self):
        # list maybe dynamic
        if self._notice_widgets:
            s = copy.copy(self._notice_widgets)
            for i_window in s:
                if i_window._window_close_flag is False:
                    i_window._do_window_close_()
            self._notice_widgets = []

    def _show_notice_(self, text):
        wgt = _window_for_dialog.QtNoticeDialog()
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


class AbsWindowBubbleMessageBaseDef(object):
    def _init_window_bubble_message_base_def_(self, widget):
        self._widget = widget

    def _popup_message_(self, text):
        _bubble.QtMessageBubble._create_for_(self, text)


class QtMainWindow(
    QtWidgets.QMainWindow,
    #
    _qt_abstracts.AbsQtBusyBaseDef,
    _qt_abstracts.AbsQtActionBaseDef,
    #
    _qt_abstracts.AbsQtThreadBaseDef,
    #
    _utility.QtThreadDef,
    _qt_abstracts.AbsQtMainWindowDef,
    _qt_abstracts.AbsQtShortcutBaseDef,
    AbsWindowNoticeBaseDef,
    AbsWindowBubbleMessageBaseDef,

    _qt_abstracts.AbsQtThreadWorkerExtraDef
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
        self._frame_draw_rect.setRect(
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
        #
        self.setFont(_qt_core.QtFonts.NameNormal)

        _qt_core.QtUtil.assign_qt_shadow(self, radius=2)

        self._window_system_tray_icon = None
        self._init_busy_base_def_(self)
        self._init_action_base_def_(self)
        self._init_thread_base_def_(self)
        self._init_window_base_def_(self)
        self._init_shortcut_base_def_(self)
        self._init_window_notice_base_def_(self)
        self._init_window_bubble_message_base_def_(self)

        self._init_thread_worker_extra_def_(self)

        self.setStyleSheet(
            _qt_core.QtStyle.get('QMainWindow')
        )
        self.menuBar().setStyleSheet(
            _qt_core.QtStyle.get('QMenuBar')
        )
        self._frame_draw_rect = qt_rect()
        self._menu_frame_draw_rect = qt_rect()

        self.installEventFilter(self)

        self._register_window_close_method_(
            self._do_notice_close_all_
        )

        # fixme: do not connect this method
        # self._connect_size_changed_to_(
        #     self._kill_all_thread_worker_
        # )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if not hasattr(event, 'type'):
                return False
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
            self._frame_draw_rect,
            _qt_core.QtRgba.Basic
        )
        painter.fillRect(
            self._menu_frame_draw_rect,
            _qt_core.QtRgba.Dark
        )

    def closeEvent(self, event):
        if self._window_ask_for_close is True:
            w = _window_for_dialog.QtMessageDialog(self)
            w._set_title_('Close Window')
            w._set_ok_visible_(True)
            w._set_no_visible_(True)
            w._set_message_('Are you sure you want to close the window?')
            w._do_window_exec_()
            if w._get_result_():
                self._do_window_close_()
                self._do_kill_all_thread_workers_()
                event.accept()
            else:
                event.ignore()
        else:
            self._do_window_close_()
            self._do_kill_all_thread_workers_()
            event.accept()

    def _exec_message_dialog_(self, message, *args, **kwargs):
        w = _window_for_dialog.QtMessageDialog(self)

        if 'title' in kwargs:
            w._set_title_(kwargs['title'])
        else:
            w._set_title_('Message')

        w._set_ok_visible_(True)
        if kwargs.get('show_no', False):
            w._set_no_visible_(True)
        if kwargs.get('show_cancel', False):
            w._set_cancel_visible_(True)

        w._set_message_(message)
        if 'status' in kwargs:
            status = kwargs['status']
            if status == 'warning':
                w._set_status_(
                    _gui_core.GuiValidationStatus.Warning
                )
            elif status == 'error':
                w._set_status_(
                    _gui_core.GuiValidationStatus.Error
                )
            elif status == 'correct':
                w._set_status_(
                    _gui_core.GuiValidationStatus.Correct
                )

        w._do_window_exec_(size=kwargs.get('size'))
        return w._get_result_()

    def _set_name_icon_text_(self, text):
        self.setWindowIcon(
            _qt_core.QtIcon.generate_by_text(text)
        )

    def _set_icon_name_(self, icon_name):
        self.setWindowIcon(
            _qt_core.QtIcon.generate_by_icon_name(icon_name)
        )

    def _set_window_system_tray_icon_(self, widget):
        self._window_system_tray_icon = widget

    def _connect_size_changed_to_(self, fnc):
        self.size_changed.connect(fnc)


class QtDockerWidget(QtWidgets.QDockWidget):
    def __init__(self, *args, **kwargs):
        super(QtDockerWidget, self).__init__(*args)

        self.setStyleSheet(
            _qt_core.QtStyle.get('QDockWidget')
        )


class QtDockerWindow(QtMainWindow):
    def __init__(self, *args, **kwargs):
        super(QtDockerWindow, self).__init__(*args, **kwargs)

    def _create_center_widget_(self, name, widget):
        dock = QtDockerWidget(name, self)
        dock.setWidget(widget)
        dock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
        return dock

    def _create_left_docker_(self, name, widget):
        dock = QtDockerWidget(name, self)
        dock.setWidget(widget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
        return dock

    def _create_right_docker_(self, name, widget):
        dock = QtDockerWidget(name, self)
        dock.setWidget(widget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
        return dock

    def _accept_corner_(self):
        self.setCorner(QtCore.Qt.TopLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.TopRightCorner, QtCore.Qt.RightDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomRightCorner, QtCore.Qt.RightDockWidgetArea)
