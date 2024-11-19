# coding=utf-8
import six

import lxbasic.storage as bsc_storage
# qt
from ....qt.core.wrap import *

from ....qt import core as _qt_core

from ....qt import abstracts as _qt_abstracts
# qt widgets
from .. import utility as _wgt_utility

from .. import entry_frame as _wgt_entry_frame


# entry as constant, etc. float, integer, string, ...
class QtEntryForConstant(
    QtWidgets.QLineEdit,

    _qt_abstracts.AbsQtEntryBaseDef,

    _qt_abstracts.AbsQtEntryFrameExtraDef,
    _qt_abstracts.AbsQtActionForDropBaseDef,

    _qt_abstracts.AbsQtEntryPopupExtra,
):
    user_entry_text_accepted = qt_signal(str)

    user_key_tab_pressed = qt_signal()

    key_backspace_extra_pressed = qt_signal()

    key_enter_pressed = qt_signal()

    focus_in = qt_signal()
    focus_out = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtEntryForConstant, self).__init__(*args, **kwargs)
        self.setPalette(_qt_core.GuiQtDcc.generate_qt_palette())
        self.setFont(_qt_core.QtFont.generate_2(size=12))
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._value_type = str

        self._value_default = None

        self._maximum = 1
        self._minimum = 0

        # noinspection PyUnresolvedReferences
        self.returnPressed.connect(self.user_entry_finished.emit)
        # noinspection PyUnresolvedReferences
        self.returnPressed.connect(self._execute_text_change_accepted_)
        # emit send by setText
        # noinspection PyUnresolvedReferences
        self.textChanged.connect(self._do_entry_change_)
        # user enter
        # noinspection PyUnresolvedReferences
        self.textEdited.connect(self._do_user_entry_change_)

        self.setStyleSheet(
            _qt_core.QtStyle.get('QLineEdit')
        )

        self._init_entry_base_def_(self)
        self._init_entry_frame_extra_def_(self)
        self._init_entry_popup_extra_def_(self)

        self._init_drop_base_def_(self)

        self.setAcceptDrops(self._action_drop_is_enable)

        self.installEventFilter(self)

        # self.setPlaceholderText()

        # self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def _execute_text_change_accepted_(self):
        self.user_entry_text_accepted.emit(self.text())
        self.entry_value_change_accepted.emit(
            self._get_value_()
        )

    def _set_entry_tip_(self, text):
        self.setPlaceholderText(text)

    def _do_wheel_(self, event):
        if self._value_type in [int, float]:
            delta = event.angleDelta().y()
            pre_value = self._get_value_()
            if delta > 0:
                self._set_value_(pre_value+1)
            else:
                self._set_value_(pre_value-1)
            #
            self._do_entry_change_()
            event.accept()
            return True
        else:
            values_all = self._get_value_options_()
            if values_all:
                delta = event.angleDelta().y()
                value_pre = self._get_value_()
                if value_pre in values_all:
                    minimum, maximum = 0, len(values_all)-1
                    idx_pre = values_all.index(value_pre)
                    if delta > 0:
                        if idx_pre == 0:
                            idx_cur = maximum
                        else:
                            idx_cur = idx_pre-1
                    else:
                        if idx_pre == maximum:
                            idx_cur = minimum
                        else:
                            idx_cur = idx_pre+1
                    idx_cur = max(min(idx_cur, maximum), 0)
                    if idx_cur != idx_pre:
                        self._set_value_(values_all[idx_cur])
                        # set value before
                        event.accept()
                        return True
        return False

    def _do_drop_(self, event):
        data = event.mimeData()
        if data.hasUrls():
            urls = event.mimeData().urls()
            if urls:
                value = urls[0].toLocalFile()
                if self._get_value_is_valid_(value):
                    self._set_value_(value)
                    return True
        return False

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if not hasattr(event, 'type'):
                return False

            if event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, _wgt_entry_frame.QtEntryFrame):
                    entry_frame._set_focused_(True)
                self.focus_in.emit()
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, _wgt_entry_frame.QtEntryFrame):
                    entry_frame._set_focused_(False)
                #
                self.focus_out.emit()
                #
                self._completion_value_auto_()
            elif event.type() == QtCore.QEvent.Wheel:
                return self._do_wheel_(event)
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Backspace:
                    if not self.text():
                        self.key_backspace_extra_pressed.emit()
                elif event.key() == QtCore.Qt.Key_Tab:
                    self.user_key_tab_pressed.emit()
                elif event.key() in {QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter}:
                    self.user_entry_finished.emit()
                    self._completion_value_auto_()
                elif event.key() == QtCore.Qt.Key_Escape:
                    self.clearFocus()
                    return True
        return False

    def dropEvent(self, event):
        if self._do_drop_(event) is True:
            event.accept()
        else:
            event.ignore()

    def contextMenuEvent(self, event):
        menu_raw = [
            ('basic',),
            ('copy', None, (True, self.copy, False), QtGui.QKeySequence.Copy),
            ('paste', None, (True, self.paste, False), QtGui.QKeySequence.Paste),
            ('cut', None, (True, self.cut, False), QtGui.QKeySequence.Cut),
            ('extend',),
            ('undo', None, (True, self.undo, False), QtGui.QKeySequence.Undo),
            ('redo', None, (True, self.redo, False), QtGui.QKeySequence.Redo),
            ('select all', None, (True, self.selectAll, False), QtGui.QKeySequence.SelectAll),
        ]
        #
        if self.isReadOnly():
            menu_raw = [
                ('basic',),
                ('copy', None, (True, self.copy, False), QtGui.QKeySequence.Copy),
                ('extend',),
                ('select all', None, (True, self.selectAll, False), QtGui.QKeySequence.SelectAll)
            ]
        #
        if self._entry_use_as_storage is True:
            menu_raw.extend(
                [
                    ('system',),
                    (
                        'open folder', 'file/open-folder', (True, self._on_open_in_system_, False),
                        QtGui.QKeySequence.Open
                    ),
                    (
                        'copy path', 'tool/copy', (True, self._on_copy_path_, False),
                        QtGui.QKeySequence.Open
                    )
                ]
            )
        #
        if menu_raw:
            self._qt_menu = _wgt_utility.QtMenu(self)
            self._qt_menu._set_menu_data_(menu_raw)
            self._qt_menu._set_show_()

    def _set_drop_enable_(self, boolean):
        super(QtEntryForConstant, self)._set_drop_enable_(boolean)
        self.setAcceptDrops(boolean)

    def _do_entry_change_(self):
        # noinspection PyUnresolvedReferences
        self.entry_value_changed.emit()
        text = self.text()
        if not text:
            self.entry_value_cleared.emit()

    def _do_user_entry_change_(self):
        # noinspection PyUnresolvedReferences
        self.user_entry_value_changed.emit()
        text = self.text()
        if not text:
            self.user_entry_value_cleared.emit()

    def _completion_value_auto_(self):
        if self._value_type in {int, float}:
            if not self.text():
                self._set_value_(0)
        elif self._entry_use_as_rgba is True:
            self._set_value_as_rgba_255_(self._get_value_as_rgba_255_())

    def _set_value_type_(self, value_type):
        self._value_type = value_type
        if self._value_type is None:
            pass
        elif self._value_type is str:
            pass
            # self._set_validator_use_as_name_()
        elif self._value_type is int:
            self._set_validator_use_as_integer_()
        elif self._value_type is float:
            self._set_validator_use_as_float_()

    def _get_value_type_(self):
        return self._value_type

    def _on_open_in_system_(self):
        _ = self.text()
        if _:
            bsc_storage.StgSystem.open(_)
    
    def _on_copy_path_(self):
        _ = self.text()
        if _:
            _qt_core.QtUtil.copy_text_to_clipboard(_)

    def _set_entry_use_as_storage_(self, boolean=True):
        super(QtEntryForConstant, self)._set_entry_use_as_storage_(boolean)
        if boolean is True:
            action = QtWidgets.QAction(self)
            # noinspection PyUnresolvedReferences
            action.triggered.connect(
                self._on_open_in_system_
            )
            action.setShortcut(
                QtGui.QKeySequence.Open
            )
            action.setShortcutContext(
                QtCore.Qt.WidgetShortcut
            )
            self.addAction(action)

    def _set_entry_use_as_rgba_255_(self, boolean=False):
        super(QtEntryForConstant, self)._set_entry_use_as_rgba_255_(boolean)
        if boolean is True:
            self._set_validator_use_as_rgba_()

    def _set_validator_use_as_rgba_(self):
        reg = QtCore.QRegExp(r'^[0-9,]+$')
        validator = QtGui.QRegExpValidator(reg, self)
        self.setValidator(validator)

    def _set_validator_use_as_name_(self):
        reg = QtCore.QRegExp(r'^[a-zA-Z][a-zA-Z0-9_]+$')
        validator = QtGui.QRegExpValidator(reg, self)
        self.setValidator(validator)

    def _set_validator_use_as_integer_(self):
        self.setValidator(QtGui.QIntValidator())
        self._completion_value_auto_()

    def _set_validator_use_as_float_(self):
        self.setValidator(QtGui.QDoubleValidator())
        self._completion_value_auto_()

    def _set_value_validator_use_as_frames_(self):
        self._set_value_type_(str)
        reg = QtCore.QRegExp(r'^[0-9-,:]+$')
        validator = QtGui.QRegExpValidator(reg, self)
        self.setValidator(validator)

    def _set_value_validator_use_as_rgba_(self):
        self._set_value_type_(str)
        reg = QtCore.QRegExp(r'^[0-9.,]+$')
        validator = QtGui.QRegExpValidator(reg, self)
        self.setValidator(validator)

    def _set_value_maximum_(self, value):
        self._maximum = value

    def _get_value_maximum_(self):
        return self._maximum

    def _set_value_minimum_(self, value):
        self._minimum = value

    def _get_value_minimum_(self):
        return self._minimum

    def _set_value_range_(self, maximum, minimum):
        self._set_value_maximum_(maximum), self._set_value_minimum_(minimum)

    def _get_value_range_(self):
        return self._get_value_maximum_(), self._get_value_minimum_()

    def _get_value_(self):
        _ = self.text()
        # do not encode output, use original data
        if self._value_type == str:
            return _
        elif self._value_type == int:
            try:
                return int(_ or 0)
            except ValueError:
                return 0
        elif self._value_type == float:
            try:
                return float(_ or 0.0)
            except ValueError:
                return 0.0
        return _

    def _set_value_(self, value):
        pre_value = self.text()
        if value is not None:
            if isinstance(value, six.text_type):
                value = value.encode('utf-8')

            if isinstance(pre_value, six.text_type):
                pre_value = pre_value.encode('utf-8')

            if self._value_type is not None:
                value = self._value_type(value)
            #
            if value != pre_value:
                self.entry_value_change_accepted.emit(value)
                self.setText(str(value))
                # self._do_entry_change_()
        else:
            self.setText('')

    def _set_value_as_rgba_255_(self, rgba):
        if isinstance(rgba, (tuple, list)):
            text = ','.join(map(lambda x: str(int(x)), rgba))
            self.setText(text)

    def _get_value_as_rgba_255_(self):
        text = self.text()
        _ = map(lambda x: max(min(int(x), 255), 0) if x else 255, map(lambda x: str(x).strip(), text.split(',')))
        c = len(_)
        if c == 4:
            return tuple(_)
        elif c > 4:
            return tuple(_[:4])
        elif c < 4:
            return tuple([_[i] if i < c else 255 for i in range(4)])
        return 255, 255, 255, 255

    def _connect_focused_to_(self, widget):
        pass

    def _is_selected_(self):
        boolean = False
        if self.selectedText():
            boolean = True
        return boolean

    def _clear_input_(self):
        self._set_value_('')

    def _set_entry_enable_(self, boolean):
        super(QtEntryForConstant, self)._set_entry_enable_(boolean)
        self.setReadOnly(not boolean)

    def _set_all_selected_(self):
        self.selectAll()

    def _get_is_focused_(self):
        return self.hasFocus()

    def _set_entry_focus_in_(self):
        # run behind "addWidget"
        self.setFocus(QtCore.Qt.MouseFocusReason)

    def _has_focus_(self):
        return self.hasFocus()

    def _do_clear_(self):
        self.clear()

    # for completion
    def _build_entry_for_completion_popup_(self, popup_widget):
        self._set_completion_popup_widget_(popup_widget)

        self.user_entry_value_changed.connect(popup_widget._do_popup_start_)
        self.user_entry_value_cleared.connect(popup_widget._do_popup_close_)