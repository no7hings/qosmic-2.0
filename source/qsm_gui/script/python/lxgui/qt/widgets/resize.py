# coding=utf-8
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import core as gui_qt_core

from .. import abstracts as gui_qt_abstracts
# qt widgets
from . import utility as gui_qt_wgt_utility


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
            x+(w-icn_w)/2, y+(h-icn_h)/2, icn_w, icn_h
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
        self._hovered_frame_border_color = gui_qt_core.QtBorderColors.Button
        self._hovered_frame_background_color = gui_qt_core.QtBackgroundColors.Button

        self._actioned_frame_border_color = gui_qt_core.QtBorderColors.Actioned
        self._actioned_frame_background_color = gui_qt_core.QtBackgroundColors.Actioned

        self._set_name_text_('resize handle')
        self._set_tool_tip_text_(
            '"LMB-move" to resize'
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Enter:
                self._set_action_hovered_(True)
                self._set_action_flag_(
                    [self.ActionFlag.SplitHHover, self.ActionFlag.SplitVHover][self._resize_orientation]
                )
            elif event.type() == QtCore.QEvent.Leave:
                self._set_action_hovered_(False)
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
        painter = gui_qt_core.QtPainter(self)
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


class QtHResizeFrame(
    QtWidgets.QWidget,
):
    geometry_changed = qt_signal(int, int, int, int)

    def __init__(self, *args, **kwargs):
        super(QtHResizeFrame, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self._resize_handle = QtHResizeHandle(self)
        self._resize_handle._set_resize_icon_file_paths_(
            [
                gui_core.GuiIcon.get('resize-handle-v'), gui_core.GuiIcon.get('resize-handle-v')
            ]
        )
        self._resize_handle._resize_frame_draw_size = 10, 20
        self._resize_handle._resize_icon_draw_size = 8, 16

        self._resize_info_frame = gui_qt_wgt_utility.QtInfoBubble(self)

        self._resize_handle.size_changed.connect(self._set_resize_info_)
        self._resize_handle.resize_finished.connect(self._set_resize_reset_)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
                self.geometry_changed.emit(
                    self.x(), self.y(), self.width(), self.height()
                )
        return False

    def _set_resize_info_(self, value):
        info = str(value)
        self._resize_info_frame._set_info_text_(info)

        frm_w, frm_h = self._resize_info_frame._info_draw_size
        frm_w = self._resize_info_frame.fontMetrics().width(info)+24
        x, y = 0, 0
        w, h = self.width(), self.height()

        self._resize_info_frame.setGeometry(
            x+(w-frm_w)/2, y+(h-frm_h)/2, frm_w, frm_h
        )
        self._resize_info_frame.raise_()

    def _set_resize_reset_(self):
        self._resize_info_frame._set_info_text_('')

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        if self._resize_handle._resize_alignment == self._resize_handle.ResizeAlignment.Right:
            frm_w, frm_h = 10, 20
            r_x, r_y = x+(w-frm_w), y+(h-frm_h)
            self._resize_handle.setGeometry(
                r_x, r_y, frm_w, frm_h
            )
        elif self._resize_handle._resize_alignment == self._resize_handle.ResizeAlignment.Left:
            frm_w, frm_h = 10, 20
            r_x, r_y = x, y+(h-frm_h)
            self._resize_handle.setGeometry(
                r_x, r_y, frm_w, frm_h
            )
        self._resize_handle.raise_()

    # resize
    def _get_resize_handle_(self):
        return self._resize_handle
