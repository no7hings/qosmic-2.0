# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.content as bsc_content
# qt
from ...core.wrap import *

from ... import core as _qt_core

from .. import bubble as _wgt_bubble
# qt widgets
from . import entry_for_constant as _entry_for_constant


# entry as path
#   command for undo
class _PathAcceptCmd(QtWidgets.QUndoCommand):
    def __init__(self, widget, path_old, path_new):
        super(_PathAcceptCmd, self).__init__()
        self._widget = widget
        self.__path_old = path_old
        self.__path_new = path_new

    def undo(self):
        self._widget._accept_auto_(self.__path_old, self.__path_new)

    def redo(self):
        self._widget._accept_auto_(self.__path_new, self.__path_old)


#   widget
class QtEtdEntryForPath(QtWidgets.QWidget):
    entry_value_changed = qt_signal()

    entry_value_change_accepted = qt_signal(str)
    user_entry_value_change_accepted = qt_signal(str)

    next_press_clicked = qt_signal()
    next_index_accepted = qt_signal(object)

    BUBBLE_CLS = _wgt_bubble.QtPathBubble

    def _build_undo_stack(self):
        # undo
        self._undo_stack = QtWidgets.QUndoStack()

    def __init__(self, *args, **kwargs):
        super(QtEtdEntryForPath, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self._lot = QtWidgets.QHBoxLayout(self)
        self._lot.setContentsMargins(*[0]*4)
        self._lot.setSpacing(2)
        self._lot.setAlignment(QtCore.Qt.AlignLeft)

        self._path_bubble = self.BUBBLE_CLS()
        self._lot.addWidget(self._path_bubble)
        self.next_press_clicked = self._path_bubble.next_press_clicked

        self._path_bubble.component_press_clicked.connect(self._choose_at_)
        self._path_bubble.component_press_dbl_clicked.connect(self._enter_at_)

        self._entry_widget = _entry_for_constant.QtEntryForConstant()
        self._lot.addWidget(self._entry_widget)

        self._entry_widget.setFocusPolicy(QtCore.Qt.ClickFocus)
        self._entry_widget.setFont(_qt_core.QtFont.generate_2(size=12))

        # todo: hss chinese word?
        # reg = QtCore.QRegExp(r'^[a-zA-Z0-9_]+$')
        # validator = QtGui.QRegExpValidator(reg, self._entry_widget)
        # self._entry_widget.setValidator(validator)

        self.setFocusProxy(self._entry_widget)

        self._build_undo_stack()

        self._next_name_texts = []

        self._entry_widget.setToolTip(
            _qt_core.QtUtil.generate_tool_tip_css(
                'constant entry',
                [
                    '"LMB-click" to start entry',
                    '   press any key to show completion',
                    '   press "Alt+Down" to show choose'
                ]
            )
        )

        self._entry_widget.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self._entry_widget:
            if event.type() == QtCore.QEvent.KeyPress:
                if event.key() in {QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter}:
                    # send emit first for completion
                    return self._do_key_enter_press_()
                elif event.key() == QtCore.Qt.Key_Backspace:
                    return self._do_key_backspace_press_()
                # undo and redo
                elif event.key() == QtCore.Qt.Key_Z and event.modifiers() == QtCore.Qt.ControlModifier:
                    self._undo_stack.undo()
                    return True
                elif event.key() == QtCore.Qt.Key_Z and event.modifiers() == (
                    QtCore.Qt.ControlModifier|QtCore.Qt.ShiftModifier
                ):
                    self._undo_stack.redo()
                    return True
            elif event.type() == QtCore.QEvent.ContextMenu:
                # disable menu context
                return True
        return False

    def _get_entry_widget_(self):
        return self._entry_widget
    
    def _set_entry_tip_(self, text):
        self._entry_widget._set_entry_tip_(text)

    def _enter_next_(self, name_text):
        if name_text:
            if self._check_name_text_is_valid_(name_text) is True:
                path_old = self._path_bubble._get_path_()
                path_new = path_old.generate_child(name_text)
                self._undo_stack.push(_PathAcceptCmd(self, path_old, path_new))
                return True
        return False

    def _enter_at_(self, index):
        path = self._path_bubble._get_component_at_(index)
        if path.get_is_root() is False:
            path_old = self._get_path_()
            path_new = path.get_parent()
            self._undo_stack.push(_PathAcceptCmd(self, path_old, path_new))

    def _choose_at_(self, index):
        path = self._path_bubble._get_component_at_(index)
        if path.get_is_root() is False:
            pass

    def _do_key_enter_press_(self):
        return self._enter_next_(self._entry_widget.text())

    def _do_key_backspace_press_(self):
        _ = self._entry_widget.text()
        if not _:
            path_old = self._path_bubble._get_path_()
            if path_old.get_is_root() is False:
                path_new = path_old.get_parent()
                self._undo_stack.push(_PathAcceptCmd(self, path_old, path_new))
                return True
        return False

    def _check_name_text_is_valid_(self, name_text):
        name_texts = self._get_next_name_texts_()
        if name_texts:
            name_text = bsc_core.ensure_unicode(name_text)
            return name_text in name_texts
        return False

    def _get_matched_next_name_texts_(self, keyword):
        name_texts = self._get_next_name_texts_()
        if name_texts:
            return bsc_content.ContentUtil.filter(
                name_texts, u'*{}*'.format(keyword)
            )
        return []

    def _get_next_name_texts_(self):
        return self._next_name_texts

    def _set_next_name_texts_(self, texts):
        self._next_name_texts = texts
        self._update_next_enable_()

    def _do_next_wait_start_(self):
        self._next_name_texts = []
        self._path_bubble._start_next_wait_()
        # self._update_next_enable_()

    def _do_next_wait_end_(self):
        self._update_next_enable_()
        self._path_bubble._end_next_wait_()

    def _accept_auto_(self, path_0, path_1):
        path_text_0, path_text_1 = path_0.to_string(), path_1.to_string()
        c_0, c_1 = path_0.get_depth(), path_1.get_depth()
        # send emit
        self.entry_value_changed.emit()
        self.entry_value_change_accepted.emit(path_text_0)
        # update bubble
        self._path_bubble._set_path_text_(path_text_0)
        # send user emit
        self.user_entry_value_change_accepted.emit(path_text_0)
        # update entry
        #   when backward
        if c_0 < c_1:
            # 0 is "/A" and 1 is "/A/B/C"
            if c_1-c_0 > 1:
                self._entry_widget.setText(path_text_1[len(path_text_0):].split(path_0.pathsep)[0])
            # 0 is "/A" and 1 is "/A/B"
            else:
                self._entry_widget.setText(path_1.get_name())
            self._entry_widget.selectAll()
        #   when forward
        else:
            self._entry_widget.clear()
        # update next
        self._update_next_()

    def _update_next_(self):
        self.next_index_accepted.emit(self._get_path_())
        self._update_next_enable_()

    def _update_next_enable_(self):
        self._path_bubble._set_next_enable_(bool(self._get_next_name_texts_()))

    def _set_root_text_(self, text):
        self._path_bubble._set_root_text_(text)

    def _set_path_text_(self, path_text):
        if path_text:
            if path_text != self._get_path_text_():
                self.entry_value_changed.emit()
                self.entry_value_change_accepted.emit(path_text)
                # update bubble
                self._path_bubble._set_path_text_(path_text)
                # update entry
                self._entry_widget.clear()
                # update next what ever value is changed
                self._update_next_()

    def _get_path_text_(self):
        return self._path_bubble._get_path_text_()

    def _get_path_(self):
        return self._path_bubble._get_path_()

    def _backward_(self):
        self.__component_texts.remove(self.__component_texts[-1])

    def _set_focused_(self, boolean):
        if boolean is True:
            self.setFocus(
                QtCore.Qt.MouseFocusReason
            )
        else:
            self.setFocus(
                QtCore.Qt.NoFocusReason
            )
