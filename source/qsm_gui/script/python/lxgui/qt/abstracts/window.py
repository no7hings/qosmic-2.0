# coding=utf-8
# qt
from ..core.wrap import *

from .. import core as _qt_core


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
    window_closed = qt_signal()

    def _init_window_base_def_(self, widget):
        self._widget = widget
        self._window_close_fncs = []

        self._window_ask_for_close = False

        self._definition_window_size = 240, 120

        self._window_close_flag = False

        self._window_auto_close_flag = None

        self._window_opacity = 1.0

    def _close_window_delay_(self, delay_time):
        tmr = QtCore.QTimer(self)
        tmr.singleShot(delay_time, self._do_window_close_)

    def _run_fnc_delay_(self, fnc, delay_time):
        tmr = QtCore.QTimer(self)
        tmr.singleShot(delay_time, fnc)

    def _close_window_delay_as_fade_(self, delay_time):
        self._window_auto_close_flag = True

        tmr = QtCore.QTimer(self)
        tmr.singleShot(delay_time, self._do_window_close_as_fade_)

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

    def _register_window_close_method_(self, fnc):
        self._window_close_fncs.append(fnc)

    def _do_window_close_(self):
        if self._window_close_flag is False:
            # run close fnc first
            if self._window_close_fncs:
                for i in self._window_close_fncs:
                    i()

            self.window_close_accepted.emit(self)
            self.window_closed.emit()

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
        _qt_core.QtUtil.show_qt_window(
            self._widget, pos, size, use_exec
        )

    def _set_icon_by_text_(self, text):
        self._widget.setWindowIcon(
            _qt_core.QtIcon.generate_by_text(text)
        )

    def _set_icon_name_(self, icon_name):
        self._widget.setWindowIcon(
            _qt_core.QtIcon.generate_by_icon_name(icon_name)
        )
