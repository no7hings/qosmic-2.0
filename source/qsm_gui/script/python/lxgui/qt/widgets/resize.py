# coding=utf-8
# qt
from ..core.wrap import *

from .. import core as _qt_core

from .. import abstracts as gui_qt_abstracts


class QtHResizeHandle(
    QtWidgets.QWidget,
    #
    gui_qt_abstracts.AbsQtNameBaseDef,
    gui_qt_abstracts.AbsQtFrameBaseDef,
    gui_qt_abstracts.AbsQtResizeBaseDef,
    #
    gui_qt_abstracts.AbsQtActionBaseDef,
    gui_qt_abstracts.AbsQtActionForHoverDef,
    gui_qt_abstracts.AbsQtActionForPressDef,
):
    press_clicked = qt_signal()
    size_changed = qt_signal(int)
    resize_stated = qt_signal()
    resize_finished = qt_signal()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()

        #
        icn_w, icn_h = self._resize_icon_draw_size
        self._resize_icon_draw_rect.setRect(
            int(x+(w-icn_w)/2), int(y+(h-icn_h)/2), icn_w, icn_h
        )

    def __init__(self, *args, **kwargs):
        super(QtHResizeHandle, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        #
        self._init_frame_base_def_(self)
        self._init_name_base_def_(self)
        self._init_resize_base_def_(self)

        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)
        #
        self._hovered_frame_border_color = _qt_core.QtRgba.BdrButton
        self._hovered_frame_background_color = _qt_core.QtRgba.BkgButton

        self._actioned_frame_border_color = _qt_core.QtRgba.BorderAction
        self._actioned_frame_background_color = _qt_core.QtRgba.BackgroundAction

        self._set_name_text_('resize handle')
        self._set_tool_tip_text_(
            '"LMB-move" to resize'
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Enter:
                self._set_hovered_(True)
                self._set_action_flag_(
                    [self.ActionFlag.SplitHHover, self.ActionFlag.SplitVHover][self._resize_orientation]
                )
            elif event.type() == QtCore.QEvent.Leave:
                self._set_hovered_(False)
                self._clear_all_action_flags_()
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self._set_action_flag_(
                    [self.ActionFlag.SplitHPress, self.ActionFlag.SplitVPress][self._resize_orientation]
                )
                self._execute_action_resize_move_start_(event)
                self._set_pressed_(True)
            elif event.type() == QtCore.QEvent.MouseMove:
                self._set_action_flag_(
                    [self.ActionFlag.SplitHMove, self.ActionFlag.SplitVMove][self._resize_orientation]
                )
                self._execute_action_resize_move_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self._execute_action_resize_move_stop_(event)
                self._set_pressed_(False)
                self._clear_all_action_flags_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        painter._draw_icon_file_by_rect_(
            rect=self._resize_icon_draw_rect,
            file_path=self._resize_icon_file_path,
            is_hovered=self._is_hovered,
        )

    def _execute_action_resize_move_start_(self, event):
        self._resize_point_start = event.pos()

    def _execute_action_resize_move_(self, event):
        if self._resize_target is not None:
            p = event.pos()-self._resize_point_start
            d_w = p.x()
            w_0 = self._resize_target.minimumWidth()
            if self._resize_alignment == self.ResizeAlignment.Right:
                w_1 = w_0+d_w
            elif self._resize_alignment == self.ResizeAlignment.Left:
                w_1 = w_0-d_w
            else:
                raise RuntimeError()
            if self._resize_minimum+10 <= w_1 <= self._resize_maximum+10:
                self._resize_target.setFixedWidth(w_1)
                # self._resize_target.setMaximumWidth(w_1)
                self.size_changed.emit(w_1)

    # noinspection PyUnusedLocal
    def _execute_action_resize_move_stop_(self, event):
        self.resize_finished.emit()


class QtVResizeHandle(QtHResizeHandle):
    press_clicked = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtVResizeHandle, self).__init__(*args, **kwargs)
        self._resize_orientation = self.ResizeOrientation.Vertical

    def _execute_action_resize_move_(self, event):
        if self._resize_target is not None:
            p = event.pos()-self._resize_point_start
            d_h = p.y()
            h_0 = self._resize_target.height()
            h_1 = h_0+d_h
            if self._resize_minimum+10 <= h_1 <= self._resize_maximum+10:
                self._resize_target.setFixedHeight(h_1)
                self.size_changed.emit(h_1)
