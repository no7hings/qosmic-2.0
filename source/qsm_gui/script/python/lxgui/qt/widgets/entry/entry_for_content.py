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


# entry as content, etc. script
class QtEntryForContent(
    QtWidgets.QTextEdit,

    _qt_abstracts.AbsQtEntryBaseDef,
    _qt_abstracts.AbsQtEntryFrameExtraDef,

    _qt_abstracts.AbsQtActionForDropBaseDef,
):
    focus_in = qt_signal()
    focus_out = qt_signal()
    focus_changed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtEntryForContent, self).__init__(*args, **kwargs)
        self.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        self.installEventFilter(self)
        # self.setAcceptRichText(False)
        # self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        #
        self.setFont(_qt_core.QtFonts.Content)
        qt_palette = _qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)
        self.setAutoFillBackground(True)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #
        self._print_signals = _qt_core.QtPrintSignals(self)
        #
        self._print_signals.print_add_accepted.connect(self._append_value_)
        self._print_signals.print_over_accepted.connect(self._set_value_)
        #
        self.setStyleSheet(
            _qt_core.QtStyle.get('QTextEdit')
        )
        #
        self.verticalScrollBar().setStyleSheet(
            _qt_core.QtStyle.get('QScrollBar')
        )
        self.horizontalScrollBar().setStyleSheet(
            _qt_core.QtStyle.get('QScrollBar')
        )
        self._init_entry_base_def_(self)
        self._init_entry_frame_extra_def_(self)
        self._init_drop_base_def_(self)

        self._empty_icon_name = None
        self._empty_text = None

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, _wgt_entry_frame.QtEntryFrame):
                    entry_frame._set_focused_(True)
                #
                self.focus_in.emit()
                self.focus_changed.emit()
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, _wgt_entry_frame.QtEntryFrame):
                    entry_frame._set_focused_(False)
                #
                self.focus_out.emit()
                self.focus_changed.emit()
            elif event.type() == QtCore.QEvent.Wheel:
                if event.modifiers() == QtCore.Qt.ControlModifier:
                    self._execute_font_scale_(event)
                    return True
        return False

    def paintEvent(self, event):
        if not self.toPlainText():
            painter = _qt_core.QtPainter(self.viewport())
            if self._empty_text:
                painter._draw_empty_text_by_rect_(
                    rect=self.rect(),
                    text=self._empty_text,
                    draw_drop_icon=True,
                )
            else:
                painter._draw_empty_image_by_rect_(
                    rect=self.rect(),
                    icon_name=self._empty_icon_name,
                )

        super(QtEntryForContent, self).paintEvent(event)

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
        if self.isReadOnly():
            menu_raw = [
                ('basic',),
                ('copy', None, (True, self.copy, False), QtGui.QKeySequence.Copy),
                ('extend',),
                ('select all', None, (True, self.selectAll, False), QtGui.QKeySequence.SelectAll)
            ]
        #
        if menu_raw:
            self._qt_menu = _wgt_utility.QtMenu(self)
            self._qt_menu._set_menu_data_(menu_raw)
            self._qt_menu._set_show_()

    def _execute_font_scale_(self, event):
        delta = event.angleDelta().y()
        font = self.font()
        size_pre = font.pointSize()
        if delta > 0:
            size_cur = size_pre+1
        else:
            size_cur = size_pre-1
        #
        size_cur = max(min(size_cur, 64), 6)
        font.setPointSize(size_cur)
        self.setFont(font)
        self.update()

    def _append_value_(self, text):
        def add_fnc_(value_):
            if value_ is not None:
                if isinstance(value_, six.text_type):
                    value_ = value_.encode('utf-8')

                self.moveCursor(QtGui.QTextCursor.End)
                self.insertPlainText(value_+'\n')

        #
        if isinstance(text, (tuple, list)):
            [add_fnc_(i) for i in text]
        else:
            add_fnc_(text)
        #
        self.update()

    def _set_content_(self, text):
        self.setText(text)

    def _append_value_use_signal_(self, text):
        self._print_signals.print_add_accepted.emit(text)

    def _set_value_with_thread_(self, text):
        self._print_signals.print_over_accepted.emit(text)

    def _get_value_(self):
        return self.toPlainText()

    def _set_value_(self, value):
        if value is not None:
            if isinstance(value, six.text_type):
                value = value.encode('utf-8')
            #
            self.setText(
                value
            )
        else:
            self.setText('')

    def _set_empty_text_(self, text):
        self._empty_text = text

    def _set_entry_enable_(self, boolean):
        super(QtEntryForContent, self)._set_entry_enable_(boolean)
        self.setReadOnly(not boolean)

    def dropEvent(self, event):
        self._do_drop_(event)

    def _do_drop_(self, event):
        if self._action_drop_is_enable is True:
            data = event.mimeData()
            if data.hasUrls():
                urls = event.mimeData().urls()
                if urls:
                    for i_url in urls:
                        i_path = i_url.toLocalFile()
                        if bsc_storage.StgPath.get_is_file(i_path) is True:
                            i_file_opt = bsc_storage.StgFileOpt(i_path)
                            i_data = i_file_opt.set_read()
                            self.insertPlainText(i_data)
                    event.accept()
        else:
            event.ignore()

    def insertFromMimeData(self, data):
        # add data as clear
        if data.text():
            self.insertPlainText(data.text())

    def _set_entry_focus_enable_(self, boolean):
        if boolean is False:
            self._entry_focus_policy_mark = self.focusPolicy()
            self.setFocusPolicy(
                QtCore.Qt.NoFocus
            )
        else:
            self.setFocusPolicy(
                self._entry_focus_policy_mark
            )