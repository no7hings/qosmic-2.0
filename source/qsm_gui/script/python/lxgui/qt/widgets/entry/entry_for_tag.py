# coding=utf-8
import lxbasic.core as bsc_core
# qt
from ....qt.core.wrap import *

from ....qt import core as _qt_core

from ....qt import abstracts as _qt_abstracts


# base entry as capsule, can be select one and more
class QtEntryForTag(
    QtWidgets.QWidget,

    _qt_abstracts.AbsQtNameBaseDef,

    _qt_abstracts.AbsQtEntryBaseDef,

    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForPressDef,
):
    value_changed = qt_signal()
    user_value_changed = qt_signal()
    user_value_accepted = qt_signal(object)

    H = 20

    def __init__(self, *args, **kwargs):
        super(QtEntryForTag, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )

        self._font = _qt_core.QtFont.generate_2(size=12)
        self._font_metrics = QtGui.QFontMetrics(self._font)
        self.setFont(_qt_core.QtFont.generate_2(size=12))
        self.setMouseTracking(True)

        self._init_name_base_def_(self)

        self._init_entry_base_def_(self)

        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)

        self._check_use_exclusive = True

        self._hover_index = None
        self._press_index = None
        self._current_index = None

        self._value = None

        self._values = []
        self._draw_texts = []
        self._indices = []
        #
        self._frame_rects = []
        #
        self._checked_indices = []

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
        if self._draw_texts:
            c = len(self._draw_texts)
            c_x, c_y = 0, 0
            c_w = 0
            for i_index in range(c):
                i_txt = self._draw_texts[i_index]
                i_w = self._font_metrics.width(i_txt)+16
                self._frame_rects[i_index].setRect(x+c_x, y+c_y+1, i_w, self.H-2)

                c_x += i_w
                c_w += i_w

                if i_index < c-1:
                    if c_w > w-i_w:
                        c_x = 0
                        c_w = 0
                        c_y += self.H

            fixed_h = c_y+self.H
            self.setFixedHeight(fixed_h)
        else:
            self.setFixedHeight(self.H)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                self._hover_index = None
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
                if self._is_action_flag_match_(self.ActionFlag.Press):
                    self._do_press_move_(event)
                else:
                    self._do_hover_move_(event)
            elif event.type() == QtCore.QEvent.ToolTip:
                self._do_show_tool_tip_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self._do_press_end_(event)
                self._clear_all_action_flags_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        if self._draw_texts:
            painter._draw_tag_by_rects_(
                rects=self._frame_rects,
                texts=self._draw_texts,
                value_options=self._value_options,
                checked_indices=self._checked_indices,
                index_hover=self._hover_index,
                index_pressed=self._press_index,
                use_exclusive=self._check_use_exclusive,
                is_enable=self._action_is_enable
            )

    # noinspection PyUnusedLocal
    def _do_show_tool_tip_(self, event):
        if self._hover_index is not None:
            title = self._draw_texts[self._hover_index]
            tool_tip = self._get_tool_tip_text_()

            if self._check_use_exclusive is True:
                css = _qt_core.QtUtil.generate_tool_tip_css(
                    title,
                    content=tool_tip or 'N/a',
                    action_tip=[
                        '"LMB-click" to switch to this item',
                    ]
                )
            else:
                css = _qt_core.QtUtil.generate_tool_tip_css(
                    title,
                    content=tool_tip or 'N/a',
                    action_tip=[
                        '"LMB-click" to check this item on',
                    ]
                )
            # noinspection PyArgumentList
            QtWidgets.QToolTip.showText(
                QtGui.QCursor.pos(), css, self
            )

    def _set_value_options_(self, values, names=None):
        if super(QtEntryForTag, self)._set_value_options_(values) is True:
            c = len(self._value_options)
            self._indices = range(c)
            self._draw_texts = []
            self._frame_rects = []
            self._checked_indices = []
            for i_index in self._indices:
                if names:
                    i_label = names[i_index]
                else:
                    i_label = bsc_core.BscText.to_prettify(values[i_index], capitalize=True)

                self._draw_texts.append(i_label)
                self._frame_rects.append(qt_rect())

                self._checked_indices.append(False)

            if c:
                if self._check_use_exclusive is True:
                    self._set_value_(values[0])

        self._refresh_widget_all_()

    def _set_value_(self, value):
        values_all = self._get_value_options_()
        if self._check_use_exclusive is True:
            if value not in values_all:
                return
            idx = values_all.index(value)
            self._current_index = idx
            self._checked_indices = [True if i in [idx] else False for i in self._indices]
        else:
            if isinstance(value, (tuple, list)):
                # value may be empty
                if value:
                    indices = [values_all.index(i) for i in value if i in values_all]
                    if indices:
                        self._current_index = indices[0]
                    self._checked_indices = [True if i in indices else False for i in self._indices]
                else:
                    self._current_index = None
                    self._checked_indices = [False for _ in self._indices]

        self._update_value_output_()
        self._refresh_widget_draw_()

    def _get_value_(self):
        return self._value

    def _generate_value_output_(self):
        values_all = self._get_value_options_()
        _ = [values_all[i] for i in self._indices if self._checked_indices[i] is True]
        if self._check_use_exclusive:
            if _:
                return _[0]
            return ''
        return _

    def _update_value_output_(self, user_flag=False):
        value_pre = self._value
        self._value = self._generate_value_output_()
        if value_pre != self._value:
            self.value_changed.emit()

            if user_flag is True:
                self.user_value_changed.emit()
                self.user_value_accepted.emit(self._value)

    def _set_use_exclusive_(self, boolean):
        self._check_use_exclusive = boolean

    def _get_is_use_exclusive_(self):
        return self._check_use_exclusive

    def _do_hover_move_(self, event):
        p = event.pos()

        idx = None

        if self._frame_rects:
            for i_idx in self._indices:
                i_rect = self._frame_rects[i_idx]
                if i_rect.contains(p):
                    idx = i_idx
                    break

        if idx != self._hover_index:
            self._hover_index = idx
            self._refresh_widget_draw_()

    def _do_press_start_(self, event, move_flag=False):
        if self._action_is_enable is False:
            return

        index_pre = self._current_index
        idx = self._hover_index

        if idx is None:
            return

        if idx != self._current_index:
            self._current_index = idx

            if self._check_use_exclusive is True:
                if index_pre is not None:
                    self._checked_indices[index_pre] = False
                self._checked_indices[self._current_index] = True
            else:
                self._checked_indices[self._current_index] = not self._checked_indices[self._current_index]

            self._update_value_output_(user_flag=True)
        else:
            if move_flag is False:
                if self._check_use_exclusive is False:
                    self._checked_indices[self._current_index] = not self._checked_indices[self._current_index]

        self._press_index = self._current_index

        self._refresh_widget_draw_()

    def _do_press_move_(self, event):
        if self._action_is_enable is False:
            return

        p = event.pos()

        idx = None

        if self._frame_rects:
            for i_idx in self._indices:
                i_rect = self._frame_rects[i_idx]
                if i_rect.contains(p):
                    idx = i_idx
                    break

        if idx != self._hover_index:
            self._hover_index = idx

        self._do_press_start_(event, move_flag=True)

    def _do_press_end_(self, event):
        if self._action_is_enable is False:
            return

        self._press_index = None
        event.accept()

    def _set_entry_enable_(self, boolean):
        super(QtEntryForTag, self)._set_entry_enable_(boolean)
        self._set_action_enable_(boolean)

    def _set_tool_tip_(self, text, **kwargs):
        self._tool_tip_text = text
