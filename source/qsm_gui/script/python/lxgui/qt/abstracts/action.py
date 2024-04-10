# coding:utf-8
import enum

import lxbasic.core as bsc_core
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *


class AbsQtActionBaseDef(object):
    ActionFlag = gui_core.GuiActionFlag
    ActionState = gui_core.GuiActionState

    def _init_action_base_def_(self, widget):
        self._widget = widget
        self._action_flag = None
        #
        self._action_is_enable = True
        #
        self._action_mdf_flags = []

        self._action_state = self.ActionState.Normal
        self._action_state_rect = QtCore.QRect()

        self._action_is_busied = False

    def _get_action_is_busied_(self):
        return self._action_is_busied

    def _set_action_busied_(self, boolean):
        self._action_is_busied = boolean
        if boolean is True:
            self._widget.setCursor(QtCore.Qt.BusyCursor)
        else:
            self._widget.unsetCursor()

    def _set_action_enable_(self, boolean):
        self._action_is_enable = boolean
        if boolean is False:
            self._action_state = self.ActionState.Disable
        else:
            self._action_state = self.ActionState.Enable
        #
        self._widget._refresh_widget_draw_geometry_()
        self._widget._refresh_widget_draw_()

    def _get_action_is_enable_(self):
        return self._action_is_enable

    def _set_action_flag_(self, flag):
        if flag is not None:
            self._action_flag = flag
            self._update_action_cursor_()
        #
        self._widget.update()

    def _set_action_mdf_flags_(self, flags):
        self._action_mdf_flags = flags

    def _set_action_mdf_flag_add_(self, flag):
        if flag is not None:
            if flag not in self._action_mdf_flags:
                self._action_mdf_flags.append(flag)
        #
        self._widget.update()

    def _update_action_cursor_(self):
        if self._action_is_busied is False:
            if self._action_flag is not None:
                if self._action_flag in {
                    self.ActionFlag.Press,
                    self.ActionFlag.PressDbClick,
                    # track
                    self.ActionFlag.TrackPress,
                    #
                    self.ActionFlag.CheckPress,
                    self.ActionFlag.ExpandPress,
                    self.ActionFlag.OptionPress,
                    self.ActionFlag.ChoosePress,
                    self.ActionFlag.NextPress,
                    self.ActionFlag.ComponentPress
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtCore.Qt.PointingHandCursor
                        )
                    )
                elif self._action_flag in {
                    self.ActionFlag.HoverMove,
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtCore.Qt.ArrowCursor
                        )
                    )
                elif self._action_flag in {
                    self.ActionFlag.PressMove,
                }:
                    self._widget.setCursor(
                        QtCore.Qt.OpenHandCursor
                    )
                elif self._action_flag in {
                    self.ActionFlag.DragPress,
                }:
                    self._widget.setCursor(
                        QtCore.Qt.ClosedHandCursor
                    )
                elif self._action_flag in {
                    self.ActionFlag.TrackMove,
                    self.ActionFlag.ZoomMove,
                    self.ActionFlag.NGNodePressMove
                }:
                    p = QtGui.QPixmap(20, 20)
                    p.load(gui_core.GuiIcon.get('system/track-move'))
                    self._widget.setCursor(
                        QtGui.QCursor(
                            p,
                            10, 10
                        )
                    )
                elif self._action_flag in [
                    self.ActionFlag.TrackCircle,
                ]:
                    p = QtGui.QPixmap(20, 20)
                    p.load(gui_core.GuiIcon.get('system/track-circle'))
                    self._widget.setCursor(
                        QtGui.QCursor(
                            p,
                            10, 10
                        )
                    )
                # split
                elif self._action_flag in {
                    self.ActionFlag.SplitHHover,
                    self.ActionFlag.SplitHPress,
                    self.ActionFlag.SplitHMove,
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtGui.QPixmap(gui_core.GuiIcon.get('system/resize-h'))
                        )
                    )
                elif self._action_flag in {
                    self.ActionFlag.SplitVHover,
                    self.ActionFlag.SplitVPress,
                    self.ActionFlag.SplitVMove
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtGui.QPixmap(gui_core.GuiIcon.get('system/resize-v'))
                        )
                    )
                # resize
                elif self._action_flag in {
                    self.ActionFlag.ResizeLeft,
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtGui.QPixmap(gui_core.GuiIcon.get('system/resize-left'))
                        )
                    )
                elif self._action_flag in {
                    self.ActionFlag.ResizeRight,
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtGui.QPixmap(gui_core.GuiIcon.get('system/resize-right'))
                        )
                    )
                elif self._action_flag in {
                    self.ActionFlag.ResizeUp,
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtGui.QPixmap(gui_core.GuiIcon.get('system/resize-up'))
                        )
                    )
                elif self._action_flag in {
                    self.ActionFlag.ResizeDown,
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtGui.QPixmap(gui_core.GuiIcon.get('system/resize-down'))
                        )
                    )
                # swap
                elif self._action_flag in {
                    self.ActionFlag.SwapH,
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtGui.QPixmap(gui_core.GuiIcon.get('system/swap-h'))
                        )
                    )
                elif self._action_flag in {
                    self.ActionFlag.SwapV,
                }:
                    self._widget.setCursor(
                        QtGui.QCursor(
                            QtGui.QPixmap(gui_core.GuiIcon.get('system/swap-v'))
                        )
                    )
                #
                elif self._action_flag in {
                    self.ActionFlag.RectSelectMove,
                }:
                    p = QtGui.QPixmap(20, 20)
                    p.load(gui_core.GuiIcon.get('system/rect-select'))
                    self._widget.setCursor(
                        QtGui.QCursor(
                            p,
                            10, 10
                        )
                    )
            else:
                self._widget.unsetCursor()

    def _get_action_flag_(self):
        return self._action_flag

    def _clear_all_action_flags_(self):
        self._action_flag = None

        self._update_action_cursor_()

        self._widget.update()

    def _clear_action_modifier_flags_(self):
        self._action_mdf_flags = []
        self._widget.update()

    def _get_action_flag_is_match_(self, *args):
        if isinstance(args, int):
            return self._action_flag == args[0]
        elif isinstance(args, (tuple, list)):
            return self._action_flag in args

    def _get_action_mdf_flags_is_include_(self, flag):
        return flag in self._action_mdf_flags

    def _get_action_mdf_flags_(self):
        return self._action_mdf_flags

    def _get_is_actioned_(self):
        return self._action_flag is not None

    def _get_action_offset_(self):
        if self._action_flag is not None:
            return 2
        return 0

    def _set_action_state_(self, state):
        self._action_flag = state

    def _get_action_state_(self):
        return self._action_state

    def _create_widget_shortcut_action_(self, fnc, shortcut):
        action = QtWidgets.QAction(self._widget)
        action.triggered.connect(fnc)
        action.setShortcut(QtGui.QKeySequence(shortcut))
        action.setShortcutContext(QtCore.Qt.WidgetWithChildrenShortcut)
        self._widget.addAction(action)


class AbsQtActionForHoverDef(object):
    def _init_action_for_hover_def_(self, widget):
        self._widget = widget
        #
        self._is_hovered = False

    def _set_action_hovered_(self, boolean):
        self._is_hovered = boolean
        #
        self._widget.update()

    def _get_is_hovered_(self):
        return self._is_hovered

    def _execute_action_hover_by_filter_(self, event):
        if event.type() == QtCore.QEvent.Enter:
            self._set_action_hovered_(True)
        elif event.type() == QtCore.QEvent.Leave:
            self._set_action_hovered_(False)

    def _clear_hover_(self):
        self._is_hovered = False
        self._widget.update()

    def _do_hover_move_(self, event):
        pass


class AbsQtActionForPressDef(object):
    pressed = qt_signal()
    press_clicked = qt_signal()
    press_db_clicked = qt_signal()
    press_toggled = qt_signal(bool)
    #
    clicked = qt_signal()
    #
    ActionFlag = gui_core.GuiActionFlag

    def _init_action_for_press_def_(self, widget):
        self._widget = widget
        #
        self._press_is_enable = True
        self._is_pressed = False
        #
        self._press_is_hovered = False
        #
        self._press_action_rect = QtCore.QRect()
        self._press_point = QtCore.QPoint()

        self._action_press_db_clicked_methods = []

    def _get_press_point_(self):
        return self._press_point

    def _get_action_is_enable_(self):
        raise NotImplementedError()

    def _get_action_flag_(self):
        raise NotImplementedError()

    def _get_action_flag_is_match_(self, flag):
        raise NotImplementedError()

    def _get_action_press_is_enable_(self):
        if self._get_action_is_enable_() is True:
            return self._press_is_enable
        return False

    def _set_pressed_(self, boolean):
        self._is_pressed = boolean
        self._widget.update()

    def _get_is_pressed_(self):
        return self._is_pressed

    def _set_action_press_db_click_emit_send_(self):
        self.press_db_clicked.emit()

    def _get_action_press_flag_is_click_(self):
        return self._get_action_flag_is_match_(
            self.ActionFlag.Press
        )

    def _set_action_press_db_clicked_method_add_(self, fnc):
        self._action_press_db_clicked_methods.append(fnc)


class AbsQtActionForCheckDef(object):
    check_clicked = qt_signal()
    check_db_clicked = qt_signal()
    check_toggled = qt_signal(bool)
    user_check_clicked = qt_signal()
    user_check_toggled = qt_signal(bool)
    #
    user_check_clicked_as_exclusive = qt_signal()
    check_changed_as_exclusive = qt_signal()
    check_swapped_as_exclusive = qt_signal()
    #
    ActionFlag = gui_core.GuiActionFlag

    def _init_action_for_check_def_(self, widget):
        self._widget = widget
        #
        self._check_action_is_enable = False
        #
        self._is_checked = False
        self._check_rect = QtCore.QRect()
        self._check_icon_frame_draw_rect = QtCore.QRect()
        self._check_icon_draw_rect = QtCore.QRect()
        self._check_is_pressed = False
        self._check_is_hovered = False
        #
        self._check_icon_frame_draw_percent = .875
        self._check_icon_frame_draw_size = 20, 20
        self._check_icon_draw_percent = .8
        self._check_icon_draw_size = 16, 16
        #
        self._check_icon_file_path_0 = gui_core.GuiIcon.get('box_unchecked')
        self._check_icon_file_path_1 = gui_core.GuiIcon.get('box_checked')
        self._check_icon_file_path_current = self._check_icon_file_path_0

        self._check_is_enable = False

        self._check_exclusive_widgets = []

        self._check_state_draw_rect = QtCore.QRect()

    def _get_action_is_enable_(self):
        raise NotImplementedError()

    def _set_check_action_enable_(self, boolean):
        self._check_action_is_enable = boolean

    def _get_check_action_is_enable_(self):
        if self._get_action_is_enable_() is True:
            return self._check_action_is_enable
        return False

    def _set_check_enable_(self, boolean):
        self._check_is_enable = boolean

    def _get_check_is_enable_(self):
        return self._check_is_enable

    def _set_checked_(self, boolean):
        self._is_checked = boolean
        self.check_clicked.emit()
        self.check_toggled.emit(boolean)
        self._refresh_check_draw_()

    def _set_exclusive_widgets_(self, widgets):
        self._check_exclusive_widgets = widgets

    def _get_is_checked_(self):
        return self._is_checked

    def _execute_check_swap_(self):
        if self._check_exclusive_widgets:
            self._update_check_exclusive_()
        else:
            self._set_checked_(not self._is_checked)
        #
        self._refresh_check_draw_()

    def _update_check_exclusive_(self):
        if self._check_exclusive_widgets:
            for i in self._check_exclusive_widgets:
                if i == self:
                    value_pre = self._get_is_checked_()
                    self._set_checked_(True)
                    if value_pre is not True:
                        self.check_changed_as_exclusive.emit()
                    else:
                        self.check_swapped_as_exclusive.emit()
                    #
                    self.user_check_clicked_as_exclusive.emit()
                else:
                    i._set_checked_(False)

    def _refresh_check_draw_(self):
        self._check_icon_file_path_current = [
            self._check_icon_file_path_0, self._check_icon_file_path_1
        ][self._is_checked]
        #
        self._widget.update()

    def _set_check_icon_frame_draw_rect_(self, x, y, w, h):
        self._check_icon_frame_draw_rect.setRect(
            x, y, w, h
        )

    def _set_check_action_rect_(self, x, y, w, h):
        self._check_rect.setRect(
            x, y, w, h
        )

    def _set_check_icon_draw_rect_(self, x, y, w, h):
        self._check_icon_draw_rect.setRect(
            x, y, w, h
        )

    def _send_check_emit_(self):
        self._execute_check_swap_()
        #
        self.user_check_clicked.emit()
        self.user_check_toggled.emit(self._is_checked)

    def _set_item_check_changed_connect_to_(self, fnc):
        self.check_clicked.connect(fnc)

    def _do_check_press_(self, event):
        self._execute_check_swap_()

    def _set_check_icon_file_paths_(self, file_path_0, file_path_1):
        self._check_icon_file_path_0 = file_path_0
        self._check_icon_file_path_1 = file_path_1
        self._refresh_check_draw_()

    def _get_action_check_is_valid_(self, event):
        if self._check_action_is_enable is True:
            p = event.pos()
            return self._check_rect.contains(p)
        return False


class AbsQtActionForExpandDef(object):
    class ExpandDirection(enum.IntEnum):
        TopToBottom = 0
        BottomToTop = 1

    class CollapseDirection(enum.IntEnum):
        RightToLeft = 0
        LeftToRight = 1

    #
    expand_clicked = qt_signal()
    expand_toggled = qt_signal(bool)
    #
    EXPAND_TOP_TO_BOTTOM = 0
    EXPAND_BOTTOM_TO_TOP = 1
    #
    ActionFlag = gui_core.GuiActionFlag

    def _init_action_for_expand_def_(self, widget):
        self._widget = widget
        #
        self._is_expand_enable = False
        #
        self._expand_icon_file_path = None
        self._expand_icon_file_path_0 = gui_core.GuiIcon.get('box_checked')
        self._expand_icon_file_path_1 = gui_core.GuiIcon.get('box_unchecked')
        self._is_expanded = False
        #
        self._expand_frame_rect = QtCore.QRect()
        self._expand_icon_draw_rect = QtCore.QRect()
        #
        self._expand_direction = self.ExpandDirection.TopToBottom

    def _set_expanded_(self, boolean):
        self._is_expanded = boolean
        self._refresh_expand_()

    def _get_is_expanded_(self):
        return self._is_expanded

    def _swap_expand_(self):
        self._is_expanded = not self._is_expanded
        self._refresh_expand_()

    def _refresh_expand_(self):
        pass

    def _set_expand_direction_(self, direction):
        self._expand_direction = direction
        self._refresh_expand_()

    def _execute_action_expand_(self):
        self._swap_expand_()
        # noinspection PyUnresolvedReferences
        self.expand_clicked.emit()
        self.expand_toggled.emit(self._is_expanded)


class AbsQtActionForOptionPressDef(object):
    checked = qt_signal()

    def _get_action_is_enable_(self):
        raise NotImplementedError()

    def _init_action_for_option_press_def_(self, widget):
        self._widget = widget
        #
        self._option_click_is_enable = False
        self._option_icon_file_path = gui_core.GuiIcon.get('option')
        #
        self._option_click_rect = QtCore.QRect()
        self._option_click_icon_rect = QtCore.QRect()

    def _set_option_click_enable_(self, boolean):
        self._option_click_is_enable = boolean
        #
        self._widget.update()

    def _get_option_click_is_enable_(self):
        if self._get_action_is_enable_() is True:
            return self._option_click_is_enable
        return False


class AbsQtActionForTrackDef(object):
    def _init_action_for_track_def_(self, widget):
        self._widget = widget
        #
        self._track_offset_flag = False
        #
        self._track_offset_start_point = QtCore.QPoint(0, 0)
        #
        self._tmp_track_offset_x, self._tmp_track_offset_y = 0, 0
        self._track_offset_x, self._track_offset_y = 0, 0
        #
        self._track_offset_minimum_x, self._track_offset_minimum_y = -1000, -1000
        self._track_offset_maximum_x, self._track_offset_maximum_y = 1000, 1000
        #
        self._track_limit_x, self._track_limit_x = 0, 0
        self._track_offset_direction_x, self._track_offset_direction_y = 1, 1
        #
        self._track_offset_radix_x, self._track_offset_radix_y = 2, 2

    def _refresh_widget_draw_(self):
        self._widget.update()

    def _set_tack_offset_action_start_(self, event):
        self._track_offset_flag = True
        self._track_offset_start_point = event.globalPos()

    def _execute_action_track_offset_(self, event):
        track_point = event.globalPos()-self._track_offset_start_point
        track_offset_x, track_offset_y = self._tmp_track_offset_x, self._tmp_track_offset_y
        track_d_offset_x, track_d_offset_y = track_point.x(), track_point.y()
        #
        self._track_offset_x = bsc_core.RawValueMtd.set_offset_range_to(
            value=track_offset_x,
            d_value=track_d_offset_x,
            radix=self._track_offset_radix_x,
            value_range=(self._track_offset_minimum_x, self._track_offset_maximum_x),
            direction=self._track_offset_direction_x
        )
        #
        self._track_offset_y = bsc_core.RawValueMtd.set_offset_range_to(
            value=track_offset_y,
            d_value=track_d_offset_y,
            radix=self._track_offset_radix_y,
            value_range=(self._track_offset_minimum_y, self._track_offset_maximum_y),
            direction=self._track_offset_direction_y
        )
        self._refresh_widget_draw_()

    def _set_track_offset_action_end_(self, event):
        self._tmp_track_offset_x, self._tmp_track_offset_y = self._track_offset_x, self._track_offset_y
        self._track_offset_flag = False


class AbsQtActionForZoomDef(object):
    def _init_action_for_zoom_def_(self, widget):
        self._widget = widget
        #
        self._zoom_scale_flag = True
        #
        self._zoom_scale_x, self._zoom_scale_y = 1.0, 1.0
        self._zoom_scale_minimum_x, self._zoom_scale_minimum_y = 0.1, 0.1
        self._zoom_scale_maximum_x, self._zoom_scale_maximum_y = 100.0, 100.0

        self._zoom_scale_radix_x, self._zoom_scale_radix_y = 5.0, 5.0

    def _refresh_widget_draw_(self):
        self._widget.update()

    def _execute_action_zoom_scale_(self, event):
        delta = event.angleDelta().y()
        self._zoom_scale_x = bsc_core.RawValueMtd.step_to(
            value=self._zoom_scale_x,
            delta=delta,
            step=self._zoom_scale_radix_x,
            value_range=(self._zoom_scale_minimum_x, self._zoom_scale_maximum_x),
            direction=1
        )

        self._zoom_scale_y = bsc_core.RawValueMtd.step_to(
            value=self._zoom_scale_y,
            delta=delta,
            step=self._zoom_scale_radix_y,
            value_range=(self._zoom_scale_minimum_y, self._zoom_scale_maximum_y),
            direction=1
        )
        #
        self._refresh_widget_draw_()