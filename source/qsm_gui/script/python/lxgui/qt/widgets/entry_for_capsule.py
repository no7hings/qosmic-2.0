# coding=utf-8
import six

import lxbasic.core as bsc_core
# qt
from ..core.wrap import *

from .. import core as gui_qt_core

from .. import abstracts as gui_qt_abstracts


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

    def _set_value_options_(self, values, labels=None):
        if super(QtEntryAsCapsule, self)._set_value_options_(values) is True:
            c = len(values)
            self.__indices = range(c)
            self.__texts_draw = []
            self.__rects_frame = []
            self.__indices_checked = []
            for i_index in self.__indices:
                if labels:
                    i_label = labels[i_index]
                else:
                    i_label = bsc_core.RawTextMtd.to_prettify(values[i_index], capitalize=True)
                self.__texts_draw.append(i_label)
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