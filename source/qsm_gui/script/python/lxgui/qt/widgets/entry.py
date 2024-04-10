# coding=utf-8
import six

import os

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# qt
from ..core.wrap import *

from .. import core as gui_qt_core

from .. import abstracts as gui_qt_abstracts
# qt widgets
from . import utility as gui_qt_wgt_utility

from . import resize as gui_qt_wgt_resize


# entry as constant, etc. float, integer, string, ...
class QtEntryAsConstant(
    QtWidgets.QLineEdit,

    gui_qt_abstracts.AbsQtEntryBaseDef,

    gui_qt_abstracts.AbsQtEntryFrameExtraDef,
    gui_qt_abstracts.AbsQtActionForDropBaseDef,

    gui_qt_abstracts.AbsQtEntryPopupExtra,
):
    user_entry_text_accepted = qt_signal(str)

    user_key_tab_pressed = qt_signal()

    key_backspace_extra_pressed = qt_signal()

    key_enter_pressed = qt_signal()

    focus_in = qt_signal()
    focus_out = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtEntryAsConstant, self).__init__(*args, **kwargs)
        self.setPalette(gui_qt_core.GuiQtDcc.generate_qt_palette())
        self.setFont(gui_qt_core.GuiQtFont.generate_2(size=12))
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._value_type = str

        self._value_default = None

        self._maximum = 1
        self._minimum = 0

        self.returnPressed.connect(self.user_entry_finished.emit)
        self.returnPressed.connect(self.__execute_text_change_accepted_)
        # emit send by setText
        self.textChanged.connect(self._do_entry_change_)
        # user enter
        self.textEdited.connect(self._do_user_entry_change_)

        self.setStyleSheet(
            gui_qt_core.GuiQtStyle.get('QLineEdit')
        )

        self._init_entry_base_def_(self)
        self._init_entry_frame_extra_def_(self)
        self._init_entry_popup_extra_def_(self)

        self._init_drop_base_def_(self)

        self.setAcceptDrops(self._action_drop_is_enable)

        self.installEventFilter(self)

        # self.setPlaceholderText()

        # self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def __execute_text_change_accepted_(self):
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
            if event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, QtEntryFrame):
                    entry_frame._set_focused_(True)
                self.focus_in.emit()
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, QtEntryFrame):
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
                    ('open folder', 'file/open-folder', (True, self._execute_open_in_system_, False),
                     QtGui.QKeySequence.Open)
                ]
            )
        #
        if menu_raw:
            self._qt_menu = gui_qt_wgt_utility.QtMenu(self)
            self._qt_menu._set_menu_data_(menu_raw)
            self._qt_menu._set_show_()

    def _set_drop_enable_(self, boolean):
        super(QtEntryAsConstant, self)._set_drop_enable_(boolean)
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

    def _execute_open_in_system_(self):
        _ = self.text()
        if _:
            bsc_storage.StgSystem.open(_)

    def _set_entry_use_as_storage_(self, boolean=True):
        super(QtEntryAsConstant, self)._set_entry_use_as_storage_(boolean)
        if boolean is True:
            action = QtWidgets.QAction(self)
            action.triggered.connect(
                self._execute_open_in_system_
            )
            action.setShortcut(
                QtGui.QKeySequence.Open
            )
            action.setShortcutContext(
                QtCore.Qt.WidgetShortcut
            )
            self.addAction(action)

    def _set_entry_use_as_rgba_255_(self, boolean=False):
        super(QtEntryAsConstant, self)._set_entry_use_as_rgba_255_(boolean)
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
            # if isinstance(_, six.text_type):
            #     _ = _.encode('utf-8')
            return _
        elif self._value_type == int:
            return int(_ or 0)
        elif self._value_type == float:
            return float(_ or 0)
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

    #
    def _get_is_selected_(self):
        boolean = False
        if self.selectedText():
            boolean = True
        return boolean

    def _clear_input_(self):
        self._set_value_('')

    def _set_entry_enable_(self, boolean):
        super(QtEntryAsConstant, self)._set_entry_enable_(boolean)
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

    def _set_clear_(self):
        self.clear()

    # for completion
    def _build_entry_for_completion_popup_(self, popup_widget):
        self._set_completion_popup_widget_(popup_widget)

        self.user_entry_value_changed.connect(popup_widget._do_popup_start_)
        self.user_entry_value_cleared.connect(popup_widget._do_popup_close_)


# entry as content, etc. script
class QtEntryAsContent(
    QtWidgets.QTextEdit,

    gui_qt_abstracts.AbsQtEntryBaseDef,
    gui_qt_abstracts.AbsQtEntryFrameExtraDef,

    gui_qt_abstracts.AbsQtActionForDropBaseDef,
):
    focus_in = qt_signal()
    focus_out = qt_signal()
    focus_changed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtEntryAsContent, self).__init__(*args, **kwargs)
        self.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        self.installEventFilter(self)
        # self.setAcceptRichText(False)
        # self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        #
        self.setFont(gui_qt_core.QtFonts.Content)
        qt_palette = gui_qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)
        self.setAutoFillBackground(True)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #
        self._print_signals = gui_qt_core.QtPrintSignals(self)
        #
        self._print_signals.print_add_accepted.connect(self._add_value_)
        self._print_signals.print_over_accepted.connect(self._set_value_)
        #
        self.setStyleSheet(
            gui_qt_core.GuiQtStyle.get('QTextEdit')
        )
        #
        self.verticalScrollBar().setStyleSheet(
            gui_qt_core.GuiQtStyle.get('QScrollBar')
        )
        self.horizontalScrollBar().setStyleSheet(
            gui_qt_core.GuiQtStyle.get('QScrollBar')
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
                if isinstance(entry_frame, QtEntryFrame):
                    entry_frame._set_focused_(True)
                #
                self.focus_in.emit()
                self.focus_changed.emit()
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, QtEntryFrame):
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
            painter = gui_qt_core.QtPainter(self.viewport())
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

        super(QtEntryAsContent, self).paintEvent(event)

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
            self._qt_menu = gui_qt_wgt_utility.QtMenu(self)
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

    def _append_content_(self, text):
        def add_fnc_(text_):
            if isinstance(text_, six.text_type):
                text_ = text_.encode('utf-8')

            self.moveCursor(QtGui.QTextCursor.End)
            self.insertPlainText(text_+'\n')

        #
        if isinstance(text, (tuple, list)):
            [add_fnc_(i) for i in text]
        else:
            add_fnc_(text)
        #
        self.update()

    def _set_content_(self, text):
        self.setText(text)

    def _add_value_with_thread_(self, text):
        self._print_signals.print_add_accepted.emit(text)

    def _set_value_with_thread_(self, text):
        self._print_signals.print_over_accepted.emit(text)

    def _get_value_(self):
        return self.toPlainText()

    def _add_value_(self, value):
        def add_fnc_(value_):
            if isinstance(value_, six.text_type):
                value_ = value_.encode('utf-8')
            #
            self.moveCursor(QtGui.QTextCursor.End)
            self.insertPlainText(value_+'\n')

        #
        if isinstance(value, (tuple, list)):
            [add_fnc_(i) for i in value]
        else:
            add_fnc_(value)
        #
        self.update()

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
        super(QtEntryAsContent, self)._set_entry_enable_(boolean)
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
                        if bsc_storage.StgPathMtd.get_is_file(i_path) is True:
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


# entry as list
class QtEntryAsList(
    gui_qt_abstracts.AbsQtListWidget,
    gui_qt_abstracts.AbsQtHelpBaseDef,

    gui_qt_abstracts.AbsQtEntryAsArrayBaseDef,
    gui_qt_abstracts.AbsQtEntryFrameExtraDef,

    gui_qt_abstracts.AbsQtActionForDropBaseDef,
):
    entry_value_changed = qt_signal()
    entry_value_added = qt_signal()
    entry_value_removed = qt_signal()
    # for popup choose
    key_up_pressed = qt_signal()
    key_down_pressed = qt_signal()

    key_enter_pressed = qt_signal()

    user_input_method_event_changed = qt_signal(object)

    def __init__(self, *args, **kwargs):
        super(QtEntryAsList, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.viewport().installEventFilter(self)

        self.setAttribute(QtCore.Qt.WA_InputMethodEnabled)
        self.setSelectionMode(self.ExtendedSelection)

        self._item_width, self._item_height = 20, 20
        self._grid_size = 20, 20

        self._init_help_base_def_(self)

        self._init_entry_as_array_base_def_(self)
        self._init_entry_frame_extra_def_(self)

        self._init_drop_base_def_(self)

        self.setAcceptDrops(self._action_drop_is_enable)

        self._set_shortcut_register_()

        self._item_icon_file_path = None

        self._empty_icon_name = 'placeholder/default'
        self._empty_text = None

    def contextMenuEvent(self, event):
        if self._entry_is_enable is True:
            menu_raw = [
                ('basic',),
                ('copy', None, (True, self._do_action_copy_, False), QtGui.QKeySequence.Copy),
                ('paste', None, (True, self._do_action_paste_, False), QtGui.QKeySequence.Paste),
                ('cut', None, (True, self._do_action_cut_, False), QtGui.QKeySequence.Cut),
                ('extend',),
                ('select all', None, (True, self._do_action_select_all_, False), QtGui.QKeySequence.SelectAll),
            ]
        else:
            menu_raw = [
                ('basic',),
                ('copy', None, (True, self._do_action_copy_, False), QtGui.QKeySequence.Copy),
                ('extend',),
                ('select all', None, (True, self._do_action_select_all_, False), QtGui.QKeySequence.SelectAll)
            ]
        #
        items = self._get_selected_items_()
        if items:
            menu_raw.append(
                ('open folder', 'file/open-folder', (True, self._execute_open_in_system_, False),
                 QtGui.QKeySequence.Open)
            )
        #
        if menu_raw:
            self._qt_menu = gui_qt_wgt_utility.QtMenu(self)
            self._qt_menu._set_menu_data_(menu_raw)
            self._qt_menu._set_show_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Control:
                    self._action_control_flag = True
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.KeyRelease:
                if event.key() == QtCore.Qt.Key_Control:
                    self._action_control_flag = False
                elif event.key() == QtCore.Qt.Key_Delete:
                    self._execute_action_delete_(event)
            elif event.type() == QtCore.QEvent.Wheel:
                pass
            elif event.type() == QtCore.QEvent.Resize:
                pass
            elif event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, QtEntryFrame):
                    entry_frame._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                entry_frame = self._get_entry_frame_()
                if isinstance(entry_frame, QtEntryFrame):
                    entry_frame._set_focused_(False)
        #
        elif widget == self.verticalScrollBar():
            pass
        #
        elif widget == self.viewport():
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_viewport_showable_auto_()
                self._refresh_all_item_widgets_()
        return False

    def paintEvent(self, event):
        if not self.count():
            painter = gui_qt_core.QtPainter(self.viewport())
            if self._empty_text:
                painter._draw_empty_text_by_rect_(
                    rect=self.rect(),
                    text=self._empty_text,
                    text_sub=self._empty_sub_text,
                    draw_drop_icon=self._action_drop_is_enable
                )
            else:
                painter._draw_empty_image_by_rect_(
                    rect=self.rect(),
                    icon_name=self._empty_icon_name,
                )

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if self._entry_use_as_storage is True:
            if event.mimeData().hasUrls:
                # event.setDropAction(QtCore.Qt.CopyAction)
                event.accept()
                return
            event.ignore()
            return
        event.ignore()
        return

    def dropEvent(self, event):
        self._do_drop_(event)

    def _execute_open_in_system_(self):
        item = self._get_item_current_()
        if item is not None:
            item_widget = self.itemWidget(item)
            if item_widget is not None:
                value = item_widget._get_value_()
                bsc_storage.StgPathOpt(value).open_in_system()

    def _set_shortcut_register_(self):
        actions = [
            (self._do_action_copy_, 'Ctrl+C'),
            (self._do_action_paste_, 'Ctrl+V'),
            (self._do_action_cut_, 'Ctrl+X'),
            (self._do_action_select_all_, 'Ctrl+A')
        ]
        for i_fnc, i_shortcut in actions:
            i_action = QtWidgets.QAction(self)
            i_action.triggered.connect(
                i_fnc
            )
            i_action.setShortcut(
                QtGui.QKeySequence(
                    i_shortcut
                )
            )
            i_action.setShortcutContext(
                QtCore.Qt.WidgetShortcut
            )
            self.addAction(i_action)

    def _do_action_copy_(self):
        selected_item_widgets = self._get_selected_item_widgets_()
        if selected_item_widgets:
            values = [i._get_value_() for i in selected_item_widgets]
            QtWidgets.QApplication.clipboard().setText(
                '\n'.join(values)
            )

    def _do_action_cut_(self):
        selected_item_widgets = self._get_selected_item_widgets_()
        if selected_item_widgets:
            values = [i._get_value_() for i in selected_item_widgets]
            QtWidgets.QApplication.clipboard().setText(
                '\n'.join(values)
            )
            [self._delete_value_(i) for i in values]

    def _do_action_paste_(self):
        text = QtWidgets.QApplication.clipboard().text()
        if text:
            values = [i.strip() for i in text.split('\n')]
            for i_value in values:
                if self._get_value_is_valid_(i_value):
                    self._append_value_(i_value)

    def _do_action_select_all_(self):
        self._set_all_items_selected_(True)

    def _get_selected_item_widgets_(self):
        return [self.itemWidget(i) for i in self.selectedItems()]

    def _set_drop_enable_(self, boolean):
        super(QtEntryAsList, self)._set_drop_enable_(boolean)
        self.setAcceptDrops(boolean)
        # self.setDragDropMode(self.DropOnly)
        # self.setDropIndicatorShown(True)

    def _do_drop_(self, event):
        data = event.mimeData()
        if self._entry_use_as_storage is True:
            if data.hasUrls():
                urls = event.mimeData().urls()
                if urls:
                    values = []
                    #
                    for i_url in urls:
                        i_value = i_url.toLocalFile()
                        if self._get_value_is_valid_(i_value):
                            values.append(i_value)
                    #
                    if self._entry_use_as_file_multiply is True:
                        values = bsc_storage.StgFileMtdForMultiply.merge_to(
                            values,
                            ['*.<udim>.####.*', '*.####.*']
                        )
                    #
                    [self._append_value_(i) for i in values]
                    event.accept()
        else:
            event.ignore()

    # noinspection PyUnusedLocal
    def _execute_action_delete_(self, event):
        item_widgets_selected = self._get_selected_item_widgets_()
        if item_widgets_selected:
            for i in item_widgets_selected:
                i_value = i._get_value_()
                self._delete_value_(i_value, False)
            #
            self._refresh_viewport_showable_auto_()

    def _delete_values_(self, values):
        [self._delete_value_(i, False) for i in values]
        self._refresh_viewport_showable_auto_()

    def _delete_value_(self, value, auto_refresh_showable=True):
        if value:
            if self._entry_is_enable is True:
                index = self._values.index(value)
                self._values.remove(value)
                #
                item = self.item(index)
                # delete item widget
                self._delete_item_widget_(item)
                # delete item
                self.takeItem(index)
                self.entry_value_removed.emit()
        #
        if auto_refresh_showable is True:
            self._refresh_viewport_showable_auto_()

    def _append_value_(self, value):
        # use original value, do not encode
        if value and value not in self._values:
            self._values.append(value)
            self._create_bubble_(value)
            self.entry_value_added.emit()

    def _insert_value_(self, index, value):
        # use original value, do not encode
        if value and value not in self._values:
            pass

    def _extend_values_(self, values):
        if values:
            for i_value in values:
                self._append_value_(i_value)

    def _clear_all_values_(self):
        super(QtEntryAsList, self)._clear_all_values_()
        self._set_clear_()

    def __item_show_deferred_fnc(self, data):
        item_widget, text = data
        item_widget._set_name_text_(text)
        item_widget._set_tool_tip_(text)
        if self._entry_use_as_storage is True:
            if os.path.isdir(text):
                item_widget._set_icon_(
                    gui_qt_core.GuiQtDcc.get_qt_folder_icon(use_system=True)
                )
            elif os.path.isfile(text):
                item_widget._set_icon_(
                    gui_qt_core.GuiQtDcc.get_qt_file_icon(text)
                )
            else:
                item_widget._set_icon_name_text_(text)
        else:
            if self._item_icon_file_path is not None:
                item_widget._set_icon_file_path_(self._item_icon_file_path)
            else:
                item_widget._set_icon_name_text_(text)

    def _create_bubble_(self, value):
        def cache_fnc_():
            return [item_widget, value]

        def build_fnc_(data):
            self.__item_show_deferred_fnc(data)

        def delete_fnc_():
            self._delete_value_(value)

        item_widget = gui_qt_wgt_utility._QtHItem()
        item_widget._set_value_(value)
        item_widget._set_delete_enable_(True)
        item_widget.delete_press_clicked.connect(delete_fnc_)
        item = gui_qt_wgt_utility.QtListWidgetItem()
        w, h = self._grid_size
        item.setSizeHint(QtCore.QSize(w, h))
        self.addItem(item)
        item._connect_item_show_()
        self.setItemWidget(item, item_widget)
        item._set_item_show_fnc_(
            cache_fnc_, build_fnc_
        )
        item_widget._refresh_widget_all_()

    def _set_clear_(self):
        super(QtEntryAsList, self)._set_clear_()
        self._values = []

    def _set_values_(self, values):
        self._clear_all_values_()
        [self._append_value_(i) for i in values]

    def _set_item_icon_file_path_(self, file_path):
        self._item_icon_file_path = file_path

    def _set_entry_use_as_storage_(self, boolean):
        super(QtEntryAsList, self)._set_entry_use_as_storage_(boolean)
        if boolean is True:
            i_action = QtWidgets.QAction(self)
            i_action.triggered.connect(
                self._execute_open_in_system_
            )
            i_action.setShortcut(
                QtGui.QKeySequence.Open
            )
            i_action.setShortcutContext(
                QtCore.Qt.WidgetShortcut
            )
            self.addAction(i_action)


class QtEntryAsBubble(
    QtWidgets.QWidget,

    gui_qt_abstracts.AbsQtEntryBaseDef,

    gui_qt_abstracts.AbsQtActionBaseDef,
    gui_qt_abstracts.AbsQtActionForPressDef,
):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        if self.__text:

            if self.__texts_draw:
                cs = [len(i) for i in self.__texts_draw]
                text = self.__texts_draw[cs.index(max(cs))]
            else:
                text = self.__text

            s_t, w_t, w_c, h_c = gui_qt_core.GuiQtText.generate_draw_args(self, text, self.__w_maximum_text)
            self.setFixedWidth(w_c)

            self.__radius_border = s_t

            x, y = 0, 0

            self.__rect_frame_draw.setRect(
                x+1, y+1, w_c-2, h_c-2
            )
            self.__rect_text_draw.setRect(
                x+s_t, y, w_t, h_c
            )

    def __init__(self, *args, **kwargs):
        super(QtEntryAsBubble, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
        )

        self.setFont(gui_qt_core.GuiQtFont.generate_2(size=12))

        self._init_entry_base_def_(self)

        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)

        self.__text = None
        self.__rect_frame_draw = QtCore.QRect()
        self.__rect_text_draw = QtCore.QRect()

        self.__texts_draw = []

        self.__is_hovered = False

        self.__radius_border = 0

        self.__w_maximum_text = 96

        self.__w_mark = None

        self.setToolTip(
            gui_qt_core.GuiQtUtil.generate_tool_tip_css(
                'bubble entry',
                [
                    '"LMB-click" to show choose',
                    '"MMB-wheel" to switch value',
                ]
            )
        )

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            #
            elif event.type() == QtCore.QEvent.Enter:
                self.__is_hovered = True
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.Leave:
                self.__is_hovered = False
                self._refresh_widget_draw_()

            elif event.type() == QtCore.QEvent.Wheel:
                self._do_wheel_(event)

            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.Press)
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.PressDbClick)
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_is_match_(self.ActionFlag.Press):
                        self.press_clicked.emit()
                #
                self._clear_all_action_flags_()
                #
                self._is_hovered = False
                self._refresh_widget_draw_()

        return False

    def _do_wheel_(self, event):
        delta = event.angleDelta().y()
        return self._scroll_to_(delta)

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)
        if self.__text is not None:
            offset = self._get_action_offset_()
            color_bkg, color_txt = gui_qt_core.GuiQtColor.generate_color_args_by_text(self.__text)

            rect_frame = self.__rect_frame_draw
            rect_frame = QtCore.QRect(
                rect_frame.x()+offset, rect_frame.y()+offset, rect_frame.width()-offset, rect_frame.height()-offset
            )
            painter._set_border_color_(gui_qt_core.QtColors.BubbleBorder)
            if offset:
                painter._set_background_color_(gui_qt_core.QtColors.BubbleBackgroundActioned)
            elif self.__is_hovered:
                painter._set_background_color_(gui_qt_core.QtColors.BubbleBackgroundHover)
            else:
                painter._set_background_color_(color_bkg)

            painter.drawRoundedRect(
                rect_frame,
                self.__radius_border, self.__radius_border,
                QtCore.Qt.AbsoluteSize
            )

            rect_text = self.__rect_text_draw
            rect_text = QtCore.QRect(
                rect_text.x()+offset, rect_text.y()+offset, rect_text.width()-offset, rect_text.height()-offset
            )

            if offset:
                painter._set_text_color_(gui_qt_core.QtColors.BubbleText)
            elif self.__is_hovered:
                painter._set_text_color_(gui_qt_core.QtColors.BubbleText)
            else:
                painter._set_text_color_(color_txt)

            painter.drawText(
                rect_text,
                QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                self.__text
            )

    def _set_value_(self, value):
        if super(QtEntryAsBubble, self)._set_value_(value) is True:
            if isinstance(self._value, six.string_types):
                self.__text = self._value.capitalize()
            else:
                self.__text = str(self._value).capitalize()

            self.entry_value_changed.emit()
            self.entry_value_change_accepted.emit(value)

        self._refresh_widget_all_()

    def _get_value_(self):
        return self._value

    def _set_value_options_(self, values):
        if super(QtEntryAsBubble, self)._set_value_options_(values) is True:
            self.__texts_draw = map(
                lambda x: x.capitalize() if isinstance(x, six.string_types) else str(x).capitalize(), values
            )

        self._refresh_widget_all_()

    def _to_next_(self):
        self._scroll_to_(1)

    def _to_previous_(self):
        self._scroll_to_(-1)

    def _scroll_to_(self, delta):
        values_all = self._get_value_options_()
        if values_all:
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
                    return True
        return False

    def _get_frame_rect_(self):
        return self.__rect_frame_draw


# base entry as capsule, can be select one and more
class QtEntryAsCapsule(
    QtWidgets.QWidget,

    gui_qt_abstracts.AbsQtNameBaseDef,

    gui_qt_abstracts.AbsQtEntryBaseDef,

    gui_qt_abstracts.AbsQtActionBaseDef,
    gui_qt_abstracts.AbsQtActionForHoverDef,
    gui_qt_abstracts.AbsQtActionForPressDef,
):
    value_changed = qt_signal()
    user_value_changed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtEntryAsCapsule, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        self.setFont(gui_qt_core.GuiQtFont.generate_2(size=12))
        self.setMouseTracking(True)

        self._init_name_base_def_(self)

        self._init_entry_base_def_(self)

        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)

        self._capsule_per_width = 0

        self.__check_use_exclusive = True

        self.__index_hover = None
        self.__index_pressed = None
        self.__index_current = None

        self.__value_output = None

        self.__values = []
        self.__texts_draw = []
        self.__indices = []
        #
        self.__rects_frame = []
        #
        self.__indices_checked = []

        self._capsule_height = 18
        self.installEventFilter(self)

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        if self.__texts_draw:
            h_t = self.fontMetrics().height()
            s_t = (h-h_t)/2
            w_t = int(max([self.fontMetrics().width(i) for i in self.__texts_draw]))
            c = len(self.__texts_draw)
            self._capsule_per_width = w_t+(w_t%2)+s_t*2
            for i_index in range(c):
                i_x, i_y = x+i_index*self._capsule_per_width, y
                i_w, i_h = self._capsule_per_width, h
                self.__rects_frame[i_index].setRect(
                    x+i_x, y+1, i_w, h-2
                )

            _w_maximum = c*self._capsule_per_width

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                self.__index_hover = None
                self._refresh_widget_all_()
            # press
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._do_press_start_(event)
                    self._set_action_flag_(
                        self.ActionFlag.Press
                    )
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    self._do_press_start_(event)
                    self._set_action_flag_(
                        self.ActionFlag.Press
                    )
            elif event.type() == QtCore.QEvent.MouseMove:
                if self._get_action_flag_is_match_(self.ActionFlag.Press):
                    self._do_press_move_(event)
                #
                self._do_hover_move_(event)
            elif event.type() == QtCore.QEvent.ToolTip:
                self._do_show_tool_tip_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self._do_press_end_(event)
                self._clear_all_action_flags_()
        return False

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)
        if self.__texts_draw:
            painter._draw_capsule_by_rects_(
                rects=self.__rects_frame,
                texts=self.__texts_draw,
                checked_indices=self.__indices_checked,
                index_hover=self.__index_hover,
                index_pressed=self.__index_pressed,
                use_exclusive=self.__check_use_exclusive,
                is_enable=self._action_is_enable
            )

    # noinspection PyUnusedLocal
    def _do_show_tool_tip_(self, event):
        if self.__index_hover is not None:
            value = self._get_value_options_()[self.__index_hover]
            if not isinstance(value, six.string_types):
                title = str(value)
            else:
                title = value

            if self.__check_use_exclusive is True:
                css = gui_qt_core.GuiQtUtil.generate_tool_tip_css(
                    title,
                    [
                        '"LMB-click" to switch to this item',
                    ]
                )
            else:
                css = gui_qt_core.GuiQtUtil.generate_tool_tip_css(
                    title,
                    [
                        '"LMB-click" to check this item on',
                    ]
                )
            QtWidgets.QToolTip.showText(
                QtGui.QCursor.pos(), css, self
            )

    def _set_value_options_(self, values):
        if super(QtEntryAsCapsule, self)._set_value_options_(values) is True:
            c = len(values)
            self.__indices = range(c)
            self.__texts_draw = []
            self.__rects_frame = []
            self.__indices_checked = []
            for i_index in self.__indices:
                self.__texts_draw.append(
                    bsc_core.RawTextMtd.to_prettify(values[i_index], capitalize=True)
                )
                self.__rects_frame.append(QtCore.QRect())

                self.__indices_checked.append(False)

            if c:
                if self.__check_use_exclusive is True:
                    self._set_value_(values[0])

        self._refresh_widget_draw_()

    def _set_value_(self, value):
        values_all = self._get_value_options_()
        if self.__check_use_exclusive is True:
            idx = values_all.index(value)
            self.__index_current = idx
            self.__indices_checked = [True if i in [idx] else False for i in self.__indices]
        else:
            if value:
                indices = [values_all.index(i) for i in value if i in values_all]
                self.__index_current = indices[0]
                self.__indices_checked = [True if i in indices else False for i in self.__indices]

        self._update_value_output_()
        self._refresh_widget_draw_()

    def _get_value_(self):
        return self.__value_output

    def _generate_value_output_(self):
        values_all = self._get_value_options_()
        _ = [values_all[i] for i in self.__indices if self.__indices_checked[i] is True]
        if self.__check_use_exclusive:
            if _:
                return _[0]
            return ''
        return _

    def _update_value_output_(self):
        value_pre = self.__value_output
        self.__value_output = self._generate_value_output_()
        if value_pre != self.__value_output:
            self.value_changed.emit()

    def _set_use_exclusive_(self, boolean):
        self.__check_use_exclusive = boolean

    def _get_is_use_exclusive_(self):
        return self.__check_use_exclusive

    def _do_hover_move_(self, event):
        if self._action_is_enable is False:
            return
        if not self._capsule_per_width:
            return
        p = event.pos()
        x, y = p.x(), p.y()
        self.__index_hover = None
        c = len(self._value_options)
        if c:
            index = int(x/self._capsule_per_width)
            if index < c:
                self.__index_hover = index
                self._refresh_widget_draw_()

    def _do_press_start_(self, event):
        if self._action_is_enable is False:
            return
        if not self._capsule_per_width:
            return
        p = event.pos()
        x, y = p.x(), p.y()
        index_pre = self.__index_current
        index = int(x/self._capsule_per_width)
        if index in self.__indices:
            self.__index_current = index
            self.__index_pressed = self.__index_current
            if self.__check_use_exclusive is True:
                if index_pre is not None:
                    self.__indices_checked[index_pre] = False
                self.__indices_checked[self.__index_current] = True
            else:
                self.__indices_checked[self.__index_current] = not self.__indices_checked[
                    self.__index_current]

            self._capsule_press_state = self.__indices_checked[self.__index_current]

            self._update_value_output_()

    def _do_press_move_(self, event):
        if self._action_is_enable is False:
            return
        if not self._capsule_per_width:
            return
        p = event.pos()
        x, y = p.x(), p.y()
        index_pre = self.__index_current
        index = int(x/self._capsule_per_width)
        if index in self.__indices:
            self.__index_current = index
            self.__index_pressed = self.__index_current
            if index_pre != self.__index_current:
                if self.__check_use_exclusive is True:
                    if index_pre is not None:
                        self.__indices_checked[index_pre] = False
                    self.__indices_checked[self.__index_current] = True
                else:
                    self.__indices_checked[self.__index_current] = self._capsule_press_state
                #
                self._update_value_output_()

    def _do_press_end_(self, event):
        if self._action_is_enable is False:
            return
        self.__index_pressed = None
        event.accept()

    def _set_entry_enable_(self, boolean):
        super(QtEntryAsCapsule, self)._set_entry_enable_(boolean)
        self._set_action_enable_(boolean)


# base entry frame
class QtEntryFrame(
    QtWidgets.QWidget,

    gui_qt_abstracts.AbsQtNameBaseDef,
    gui_qt_abstracts.AbsQtFrameBaseDef,
    gui_qt_abstracts.AbsQtStatusBaseDef,

    gui_qt_abstracts.AbsQtActionBaseDef,
    gui_qt_abstracts.AbsQtThreadBaseDef,
):
    geometry_changed = qt_signal(int, int, int, int)
    entry_focus_in = qt_signal()
    entry_focus_out = qt_signal()
    entry_focus_changed = qt_signal()

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        # int left， int top， int right， int bottom
        m_l, m_t, m_r, m_b = self._frame_draw_margins
        #
        c = self._entry_count
        #
        frm_x, frm_y = x+m_l+1, y+m_t+1
        frm_w, frm_h = w-m_l-m_r-2, h-m_t-m_b-2
        #
        self._rect_frame_draw.setRect(
            frm_x, frm_y, frm_w, frm_h
        )
        if c > 1:
            for i in range(c):
                i_widget = self._value_entries[i]
                i_p = i_widget.pos()
                i_r = i_widget.rect()
                i_x, i_y = i_p.x(), i_p.y()
                i_w, i_h = i_r.width(), i_r.height()
                self._frame_draw_rects[i].setRect(
                    i_x, frm_y, i_w, frm_h
                )
        else:
            self._frame_draw_rects[0].setRect(
                frm_x, frm_y, frm_w, frm_h
            )
        #
        if self._tip_draw_enable is True:
            self._tip_draw_rect.setRect(
                x, y, w, h
            )
        #
        if self._resize_handle is not None:
            frm_w, frm_h = 24, 24
            r_x, r_y = x+(w-frm_w), y+(h-frm_h)
            self._resize_handle.setGeometry(
                r_x, r_y, frm_w, frm_h
            )

    def __init__(self, *args, **kwargs):
        super(QtEntryFrame, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._is_hovered = False
        self._is_focused = False
        self._entry_count = 1
        #
        self._entry_widget = None
        self._value_entries = []
        #
        self._init_name_base_def_(self)
        self._init_frame_base_def_(self)
        self._init_status_base_def_(self)
        self._init_action_base_def_(self)
        self._init_thread_base_def_(self)
        #
        self._frame_border_color = gui_qt_core.QtBorderColors.Light
        self._hovered_frame_border_color = gui_qt_core.QtBorderColors.Hovered
        self._selected_frame_border_color = gui_qt_core.QtBorderColors.Selected
        self._frame_background_color = gui_qt_core.QtBackgroundColors.Dim

        self._resize_handle = gui_qt_wgt_resize.QtVResizeHandle(self)
        self._resize_handle.hide()

        self._tip_draw_enable = False
        self._tip_text = None
        self._tip_draw_rect = QtCore.QRect()
        # self._resize_handle._set_resize_target_(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
                self.geometry_changed.emit(
                    self.x(), self.y(), self.width(), self.height()
                )
        return False

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)

        is_selected = self._is_focused

        color_bkg = self._frame_background_color
        color_bdr = [gui_qt_core.QtBorderColors.Basic, gui_qt_core.QtBorderColors.HighLight][is_selected]
        w_bdr = [self._frame_border_draw_width, self._frame_border_draw_width+1][is_selected]
        painter._set_border_color_(
            gui_qt_core.QtColors.Transparent
        )
        painter._set_background_color_(
            color_bkg
        )
        for i_rect in self._frame_draw_rects:
            painter.drawRect(i_rect)

        if self._tip_draw_enable is True:
            if self._tip_text is not None:
                painter._draw_text_by_rect_(
                    rect=self._tip_draw_rect,
                    text=self._tip_text,
                    font_color=gui_qt_core.QtColors.TextDisable,
                    font=gui_qt_core.QtFonts.DefaultItalic,
                    text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                )

        if self._thread_draw_flag is True:
            for i_rect in self._frame_draw_rects:
                painter._draw_alternating_colors_by_rect_(
                    rect=i_rect,
                    colors=((0, 0, 0, 63), (0, 0, 0, 0)),
                    running=True
                )

        painter._set_border_color_(
            color_bdr
        )
        painter._set_background_color_(
            gui_qt_core.QtColors.Transparent
        )
        painter._set_border_width_(w_bdr)
        for i_rect in self._frame_draw_rects:
            painter.drawRect(i_rect)

    # resize
    def _get_resize_handle_(self):
        return self._resize_handle

    def _set_resize_enable_(self, boolean):
        self._resize_handle.setVisible(boolean)

    def _set_resize_minimum_(self, value):
        self._resize_handle._set_resize_minimum_(value)

    def _set_resize_target_(self, widget):
        self._resize_handle._set_resize_target_(widget)

    def _update_background_color_by_locked_(self, boolean):
        self._frame_background_color = [
            gui_qt_core.QtBackgroundColors.Basic, gui_qt_core.QtBackgroundColors.Dim
        ][boolean]

    def _set_focused_(self, boolean):
        self._is_focused = boolean
        self._refresh_widget_draw_()
        self.entry_focus_changed.emit()

    def _set_focus_in_(self):
        self._set_focused_(True)
        self.entry_focus_in.emit()

    def set_focus_out_(self):
        self._set_focused_(False)
        self.entry_focus_out.emit()

    def _set_entry_count_(self, size):
        self._entry_count = size
        self._frame_draw_rects = [QtCore.QRect() for _ in range(size)]

    def _set_size_policy_height_fixed_mode_(self):
        self._entry_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )

    def _set_tip_text_(self, text):
        self._tip_text = text

    def _set_tip_draw_enable_(self, boolean):
        self._tip_draw_enable = boolean
