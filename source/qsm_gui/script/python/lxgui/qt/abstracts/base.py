# coding=utf-8
import os

import collections

import enum

import fnmatch

import urllib

import six

from contextlib import contextmanager

import lxcontent.core as ctt_core

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import core as gui_qt_core


class AbsQtWidgetBaseDef(object):
    def _init_widget_base_def_(self, widget):
        self._widget = widget
        self._basic_rect = QtCore.QRect()
        self._w, self._h = 0, 0

    def _get_text_draw_width_(self, text=None):
        return self._widget.fontMetrics().width(text)

    def _set_size_(self, w, h):
        self._widget.setFixedSize(QtCore.QSize(w, h))


class AbsQtBusyBaseDef(object):
    def _init_busy_base_def_(self, widget):
        self._widget = widget

    @contextmanager
    def _gui_bustling_(self):
        self._widget.setCursor(QtCore.Qt.BusyCursor)
        yield self
        self._widget.unsetCursor()


class AbsQtFocusDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _refresh_focus_draw_geometry_(self):
        raise NotImplementedError()

    def _init_focus_def_(self, widget):
        self._widget = widget
        self._is_focused = False
        self._focus_rect = QtCore.QRect()

    def _set_focused_(self, boolean):
        self._is_focused = boolean
        if boolean is True:
            self._widget.setFocus(
                QtCore.Qt.MouseFocusReason
            )
        else:
            self._widget.setFocus(
                QtCore.Qt.NoFocusReason
            )
        self._refresh_focus_draw_geometry_()
        self._refresh_widget_draw_()

    def _get_is_focused_(self):
        return self._is_focused

    def _set_focused_rect_(self, x, y, w, h):
        self._focus_rect.setRect(
            x, y, w, h
        )

    def _get_focus_rect_(self):
        return self._focus_rect


class AbsQtEmptyBaseDef(object):
    def _init_empty_base_def_(self, widget):
        self._widget = widget

        self._empty_icon_name = 'placeholder/default'
        self._empty_text = None
        self._empty_sub_text = None

    def _set_empty_icon_name_(self, text):
        self._empty_icon_name = text
        self._widget.update()

    def _set_empty_text_(self, text):
        self._empty_text = text
        self._widget.update()

    def _set_empty_sub_text_(self, text):
        self._empty_sub_text = text
        self._widget.update()


class AbsQtMenuBaseDef(object):
    QT_MENU_CLS = None

    def _init_menu_base_def_(self, widget):
        self._widget = widget
        self._menu_title_text = None
        self._menu_data = []
        self._menu_data_generate_fnc = None
        self._menu_content = None
        self._menu_content_generate_fnc = None

    def _set_menu_title_text_(self, text):
        self._menu_title_text = text

    def _set_menu_data_(self, data):
        """
        :param data: list, etc.
        [
            ('VBO Info (Quads/Tris)', None, None),
            () # sep,
            ('VBO Info', None, None),
            ('Camera/Complexity', None, None),
            ('Performance', None, None),
            ('GPU stats', None, None),
        ]
        :return:
        """
        self._menu_data = data

    def _add_menu_data_(self, data):
        if isinstance(data, list):
            self._menu_data.extend(data)
        elif isinstance(data, tuple):
            self._menu_data.append(data)

    def _extend_menu_data_(self, raw):
        self._menu_data.extend(raw)

    def _get_menu_data_(self):
        return self._menu_data

    def _set_menu_data_generate_fnc_(self, fnc):
        self._menu_data_generate_fnc = fnc

    def _set_menu_content_generate_fnc_(self, fnc):
        self._menu_content_generate_fnc = fnc

    def _auto_generate_menu_(self, qt_menu):
        if qt_menu is None:
            qt_menu = self.QT_MENU_CLS(self)
            if self._menu_title_text is not None:
                qt_menu._set_title_text_(self._menu_title_text)
        return qt_menu

    def _popup_menu_(self):
        qt_menu = None
        # add menu content first, menu content operate always clear all
        # when generate function is defining, use generate data
        if self._menu_content_generate_fnc is not None:
            menu_content = self._menu_content_generate_fnc()
            if menu_content:
                if menu_content.get_is_empty() is False:
                    qt_menu = self._auto_generate_menu_(qt_menu)
                    qt_menu._set_menu_content_(menu_content)
                    qt_menu._set_show_()
        else:
            menu_content = self._get_menu_content_()
            if menu_content:
                if menu_content.get_is_empty() is False:
                    qt_menu = self._auto_generate_menu_(qt_menu)
                    qt_menu._set_menu_content_(menu_content)
                    qt_menu._set_show_()
        if self._menu_data_generate_fnc is not None:
            qt_menu = self._auto_generate_menu_(qt_menu)
            menu_data = self._menu_data_generate_fnc()
            if menu_data:
                qt_menu._set_menu_data_(menu_data)
                qt_menu._set_show_()
        else:
            menu_data = self._get_menu_data_()
            if menu_data:
                qt_menu = self._auto_generate_menu_(qt_menu)
                qt_menu._set_menu_data_(menu_data)
                qt_menu._set_show_()

    def _set_menu_content_(self, content):
        self._menu_content = content

    def _get_menu_content_(self):
        return self._menu_content


class AbsQtStatusBaseDef(object):
    Status = gui_core.GuiStatus
    ShowStatus = gui_core.GuiShowStatus
    ValidationStatus = gui_core.GuiValidationStatus
    Rgba = gui_core.GuiRgba

    @classmethod
    def _get_rgb_args_(cls, r, g, b, a):
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        r_, g_, b_ = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        return (r_, g_, b_, a), (r, g, b, a)

    @classmethod
    def _get_background_rgba_args_by_status_(cls, status):
        if status in {cls.Status.Started}:
            return cls._get_rgb_args_(*cls.Rgba.Transparent)
        elif status in {cls.Status.Failed, cls.Status.Error, cls.Status.Killed}:
            return cls._get_rgb_args_(*cls.Rgba.Red)
        elif status in {cls.Status.Waiting}:
            return cls._get_rgb_args_(*cls.Rgba.Orange)
        elif status in {cls.Status.Suspended}:
            return cls._get_rgb_args_(*cls.Rgba.Yellow)
        elif status in {cls.Status.Running}:
            return cls._get_rgb_args_(*cls.Rgba.Blue)
        elif status in {cls.Status.Completed}:
            return cls._get_rgb_args_(*cls.Rgba.Green)
        return cls._get_rgb_args_(*cls.Rgba.Transparent)

    @classmethod
    def _get_rgba_args_by_status_(cls, status):
        if status in {cls.Status.Waiting}:
            return cls._get_rgb_args_(*cls.Rgba.Orange)
        elif status in {cls.Status.Started}:
            return cls._get_rgb_args_(*cls.Rgba.Blue)
        elif status in {cls.Status.Killed}:
            return cls._get_rgb_args_(*cls.Rgba.Yellow)
        elif status in {cls.Status.Failed}:
            return cls._get_rgb_args_(*cls.Rgba.Red)
        elif status in {cls.Status.Completed}:
            return cls._get_rgb_args_(*cls.Rgba.Green)
        return cls._get_rgb_args_(*cls.Rgba.Orange)

    @classmethod
    def _get_text_rgba_args_by_validator_status_(cls, status):
        if status in {cls.ValidationStatus.Warning}:
            return cls._get_rgb_args_(*cls.Rgba.Yellow)
        elif status in {cls.ValidationStatus.Disable, cls.ValidationStatus.Lost}:
            return cls._get_rgb_args_(*cls.Rgba.DarkGray)
        elif status in {cls.ValidationStatus.Error, cls.ValidationStatus.Unreadable}:
            return cls._get_rgb_args_(*cls.Rgba.Red)
        elif status in {cls.ValidationStatus.Locked, cls.ValidationStatus.Unwritable}:
            return cls._get_rgb_args_(*cls.Rgba.Purple)
        elif status in {cls.ValidationStatus.Active}:
            return cls._get_rgb_args_(*cls.Rgba.Blue)
        elif status in {cls.ValidationStatus.Correct, cls.ValidationStatus.New}:
            return cls._get_rgb_args_(*cls.Rgba.Green)
        return cls._get_rgb_args_(*cls.Rgba.White)

    @classmethod
    def _get_rgba_args_by_validator_status_(cls, status):
        if status in [cls.ValidationStatus.Warning]:
            return cls._get_rgb_args_(*cls.Rgba.Yellow)
        elif status in {cls.ValidationStatus.Disable, cls.ValidationStatus.Lost}:
            return cls._get_rgb_args_(*cls.Rgba.DarkGray)
        elif status in {cls.ValidationStatus.Error, cls.ValidationStatus.Unreadable}:
            return cls._get_rgb_args_(*cls.Rgba.Red)
        elif status in {cls.ValidationStatus.Locked, cls.ValidationStatus.Unwritable}:
            return cls._get_rgb_args_(*cls.Rgba.Purple)
        elif status in {cls.ValidationStatus.Active}:
            return cls._get_rgb_args_(*cls.Rgba.Blue)
        elif status in {cls.ValidationStatus.Correct, cls.ValidationStatus.New}:
            return cls._get_rgb_args_(*cls.Rgba.Green)
        return cls._get_rgb_args_(*cls.Rgba.Transparent)

    def _init_status_base_def_(self, widget):
        self._widget = widget
        #
        self._is_status_enable = False
        #
        self._status = gui_core.GuiStatus.Stopped
        #
        self._status_color = gui_qt_core.QtBackgroundColors.Transparent
        self._hover_status_color = gui_qt_core.QtBackgroundColors.Transparent
        #
        self._status_rect = QtCore.QRect()

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _set_status_(self, status):
        self._is_status_enable = True
        #
        self._status = status
        #
        if status in {gui_core.GuiStatus.Running}:
            self._widget.setCursor(QtCore.Qt.BusyCursor)
        else:
            self._widget.unsetCursor()
        #
        self._status_color, self._hover_status_color = self._get_background_rgba_args_by_status_(
            self._status
        )
        self._refresh_widget_draw_()

    def _get_status_(self):
        return self._status

    def _get_status_is_enable_(self):
        return self._is_status_enable


class AbsQtSubProcessBaseDef(object):
    def _init_sub_process_base_def_(self):
        self._sub_process_is_enable = False
        #
        self._sub_process_statuses = []

        self._sub_process_status_text = ''
        #
        self._sub_process_status_colors = []
        self._hover_sub_process_status_colors = []
        #
        self._sub_process_status_rect = QtCore.QRect()

        self._sub_process_finished_results = []

        self._sub_process_timestamp_started = 0
        self._sub_process_timestamp_costed = 0
        #
        self._sub_process_finished_timestamp_estimated = 0

        self._sub_process_finished_value = 0
        self._sub_process_finished_maximum = 0

        self._sub_process_status_text_format_0 = '[{costed_time}]'
        self._sub_process_status_text_format_1 = '[{value}/{maximum}][{costed_time}]'
        self._sub_process_status_text_format_2 = '[{value}/{maximum}][{costed_time}/{estimated_time}]'

        # self._sub_process_timer = QtCore.QTimer(self)

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _initialization_sub_process_(self, count, status):
        if count > 0:
            self._sub_process_is_enable = True
            self._sub_process_statuses = [status]*count
            color, hover_color = AbsQtStatusBaseDef._get_background_rgba_args_by_status_(status)
            self._sub_process_status_colors = [color]*count
            self._hover_sub_process_status_colors = [hover_color]*count
            self._sub_process_finished_results = [False]*count
            self._sub_process_finished_maximum = len(self._sub_process_finished_results)
            self._sub_process_timestamp_started = bsc_core.SysBaseMtd.get_timestamp()
        else:
            self._restore_sub_process_()

        self._refresh_widget_draw_()

    def _set_sub_process_statuses_(self, statuses):
        if statuses:
            count = len(statuses)
            self._sub_process_is_enable = True
            self._sub_process_statuses = statuses
            self._sub_process_status_colors = []
            self._hover_sub_process_status_colors = []
            for i_status in statuses:
                i_color, i_hover_color = AbsQtStatusBaseDef._get_background_rgba_args_by_status_(i_status)
                self._sub_process_status_colors.append(i_color)
                self._hover_sub_process_status_colors.append(i_hover_color)

            self._sub_process_finished_results = [False]*count
            self._sub_process_timestamp_started = bsc_core.SysBaseMtd.get_timestamp()
        else:
            self._restore_sub_process_()
        #
        self._refresh_widget_draw_()

    def _set_sub_process_status_at_(self, index, status):
        self._sub_process_statuses[index] = status
        #
        color, hover_color = AbsQtStatusBaseDef._get_background_rgba_args_by_status_(status)
        self._sub_process_status_colors[index] = color
        self._hover_sub_process_status_colors[index] = hover_color
        #
        self._refresh_widget_draw_()

    def _restore_sub_process_(self):
        self._sub_process_is_enable = False
        self._sub_process_statuses = []
        self._sub_process_status_colors = []
        self._hover_sub_process_status_colors = []
        self._sub_process_finished_results = []

        self._sub_process_status_text = ''

    def _set_sub_process_finished_at_(self, index, status):
        self._sub_process_finished_results[index] = True
        #
        self._update_sub_process_finished_()
        #
        self._refresh_widget_draw_()

    def _update_sub_process_finished_(self):
        self._sub_process_finished_value = sum(self._sub_process_finished_results)
        self._sub_process_finished_maximum = len(self._sub_process_finished_results)
        #
        self._sub_process_timestamp_costed = bsc_core.SysBaseMtd.get_timestamp()-self._sub_process_timestamp_started
        if self._sub_process_finished_value > 1:
            self._sub_process_finished_timestamp_estimated = (
                self._sub_process_timestamp_costed/self._sub_process_finished_value
            )*self._sub_process_finished_maximum
        else:
            self._sub_process_finished_timestamp_estimated = 0

    def _refresh_sub_process_draw_(self):
        self._sub_process_timestamp_costed = bsc_core.SysBaseMtd.get_timestamp()-self._sub_process_timestamp_started
        self._refresh_widget_draw_()

    def _get_sub_process_status_text_(self):
        if self._sub_process_is_enable is True:
            kwargs = dict(
                value=self._sub_process_finished_value,
                maximum=self._sub_process_finished_maximum,
                costed_time=bsc_core.RawIntegerMtd.second_to_time_prettify(
                    self._sub_process_timestamp_costed,
                    mode=1
                ),
                estimated_time=bsc_core.RawIntegerMtd.second_to_time_prettify(
                    self._sub_process_finished_timestamp_estimated,
                    mode=1
                ),
            )
            if int(self._sub_process_finished_timestamp_estimated) > 0:
                return self._sub_process_status_text_format_2.format(
                    **kwargs
                )
            else:
                return self._sub_process_status_text_format_1.format(
                    **kwargs
                )
        return ''

    def _get_sub_process_is_finished_(self):
        # completed is True
        return sum(self._sub_process_finished_results) == len(self._sub_process_finished_results)

    def _set_sub_process_enable_(self, boolean):
        self._sub_process_is_enable = boolean

    def _get_sub_process_is_enable_(self):
        return self._sub_process_is_enable


class AbsQtValidatorBaseDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _init_validator_base_def_(self, widget):
        self._widget = widget

        self._validator_is_enable = False
        self._validator_statuses = []
        self._validator_status_colors = []
        self._hover_validator_status_colors = []

        self._validator_status_rect = QtCore.QRect()

    def _set_validator_status_at_(self, index, status):
        self._validator_statuses[index] = status
        color, hover_color = AbsQtStatusBaseDef._get_rgba_args_by_validator_status_(status)
        self._validator_status_colors[index] = color
        self._hover_validator_status_colors[index] = hover_color
        #
        self._refresh_widget_draw_()

    def _restore_validator_(self):
        self._validator_is_enable = False
        self._validator_statuses = []
        self._validator_status_colors = []
        self._hover_validator_status_colors = []

    def _set_validator_statuses_(self, statuses):
        if statuses:
            self._validator_is_enable = True
            self._validator_statuses = statuses
            self._validator_status_colors = []
            self._hover_validator_status_colors = []
            for i_status in statuses:
                i_color, i_hover_color = AbsQtStatusBaseDef._get_rgba_args_by_validator_status_(
                    i_status
                    )
                self._validator_status_colors.append(i_color)
                self._hover_validator_status_colors.append(i_hover_color)
        else:
            self._restore_validator_()

        self._refresh_widget_draw_()

    def _get_validator_is_enable_(self):
        return self._validator_is_enable


class AbsQtFrameBaseDef(object):

    def _refresh_widget_all_(self):
        raise NotImplementedError()

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _init_frame_base_def_(self, widget):
        self._widget = widget
        self._frame_border_color = gui_qt_core.QtBackgroundColors.Transparent
        self._hovered_frame_border_color = gui_qt_core.QtBackgroundColors.Transparent
        self._selected_frame_border_color = gui_qt_core.QtBackgroundColors.Transparent
        self._actioned_frame_border_color = gui_qt_core.QtBackgroundColors.Transparent
        #
        self._frame_background_color = gui_qt_core.QtBackgroundColors.Transparent
        self._hovered_frame_background_color = gui_qt_core.QtBackgroundColors.Transparent
        self._selected_frame_background_color = gui_qt_core.QtBackgroundColors.Transparent
        self._actioned_frame_background_color = gui_qt_core.QtBackgroundColors.Transparent
        #
        self._frame_border_radius = 0
        #
        self._frame_draw_is_enable = False
        self._rect_frame_draw = QtCore.QRect()
        self._frame_draw_margins = 0, 0, 0, 0
        self._frame_size = 20, 20
        self._frame_border_draw_style = QtCore.Qt.SolidLine
        self._frame_border_draw_width = 1

        self._margins_offset_frame = 0, 0, 0, 0

        self._frame_draw_rects = [QtCore.QRect()]

    def _set_frame_margins_(self, m_l, m_t, m_r, m_b):
        self._margins_offset_frame = m_l, m_t, m_r, m_b
        self._refresh_widget_all_()

    def _set_border_color_(self, color):
        self._frame_border_color = gui_qt_core.GuiQtColor.to_qt_color(color)
        self._refresh_widget_draw_()

    def _set_background_color_(self, color):
        self._frame_background_color = gui_qt_core.GuiQtColor.to_qt_color(color)
        self._refresh_widget_draw_()

    def _get_border_color_(self):
        return self._frame_border_color

    def _get_background_color_(self):
        return self._frame_background_color

    def _set_frame_draw_rect_(self, x, y, w, h):
        self._rect_frame_draw.setRect(
            x, y, w, h
        )

    def _get_frame_rect_(self):
        return self._rect_frame_draw

    def _set_frame_size_(self, w, h):
        self._frame_size = w, h

    def _set_frame_draw_enable_(self, boolean):
        self._frame_draw_is_enable = boolean
        self._refresh_widget_draw_()

    def _set_frame_border_radius_(self, radius):
        self._frame_border_radius = radius


class AbsQtResizeBaseDef(object):
    ResizeOrientation = gui_core.GuiOrientation
    ResizeAlignment = gui_core.GuiAlignment

    def _init_resize_base_def_(self, widget):
        self._widget = widget

        self._resize_orientation = self.ResizeOrientation.Horizontal
        self._resize_alignment = self.ResizeAlignment.Right

        self._resize_is_enable = False
        self._resize_draw_rect = QtCore.QRect()
        self._resize_action_rect = QtCore.QRect()

        self._resize_icon_file_paths = [
            gui_core.GuiIcon.get('resize-left'), gui_core.GuiIcon.get('resize-right')
        ]
        self._resize_icon_file_path = self._resize_icon_file_paths[self._resize_alignment]
        #
        self._resize_frame_draw_size = 20, 20
        self._resize_icon_draw_size = 16, 16
        self._resize_icon_draw_rect = QtCore.QRect()

        self._resize_point_start = QtCore.QPoint()
        self._resize_value_temp = 0

        self._resize_target = None
        self._resize_minimum = 20
        self._resize_maximum = 960

    def _set_resize_enable_(self, boolean):
        self._resize_is_enable = boolean

    def _set_resize_target_(self, widget):
        self._resize_target = widget

    def _set_resize_minimum_(self, value):
        self._resize_minimum = value

    def _set_resize_maximum_(self, value):
        self._resize_maximum = value

    def _set_resize_orientation_(self, value):
        self._resize_orientation = value

    def _set_resize_alignment_(self, value):
        self._resize_alignment = value
        self._resize_icon_file_path = self._resize_icon_file_paths[self._resize_alignment]

    def _set_resize_icon_file_paths_(self, file_paths):
        self._resize_icon_file_paths = file_paths
        self._resize_icon_file_path = self._resize_icon_file_paths[self._resize_alignment]


class AbsQtPopupBaseDef(object):
    class PopupStyle(object):
        FromFrame = 0x01
        FromMouse = 0x02

    user_popup_finished = qt_signal()
    user_popup_value_accepted = qt_signal(str)
    user_popup_values_accepted = qt_signal(list)

    def _init_popup_base_def_(self, widget):
        self._widget = widget
        self._popup_region = 0
        self._popup_side = 2
        self._popup_margin = 8
        self._popup_shadow_radius = 4
        self._popup_offset = 0, 0

        self._entry_widget = None
        self._entry_frame_widget = None

        self._popup_is_activated = False

        self._popup_width_minimum = 160

        self._h_popup_top_toolbar = 20

        self._rect_popup_top_toolbar = QtCore.QRect()
        self._rect_popup_top_toolbar_tool_tip = QtCore.QRect()

        self._rect_popup_bottom_toolbar = QtCore.QRect()

        self._popup_auto_resize_is_enable = False

        self._popup_style = self.PopupStyle.FromFrame

        self._popup_press_rect = QtCore.QRect()

        self._use_as_storage = False

    def _set_popup_press_rect_(self, rect):
        self._popup_press_rect = rect

    def _get_popup_press_rect_(self):
        return self._popup_press_rect

    @classmethod
    def _compute_popup_press_point_(cls, widget, rect=None):
        if rect is None:
            rect = widget.rect()
        # p = QtCore.QPoint(rect.right(), rect.center().y())
        return widget.mapToGlobal(rect.center())

    def _get_popup_pos_from_(self, widget):
        rect = widget.rect()
        # p = QtCore.QPoint(rect.right(), rect.center().y())
        p = widget.mapToGlobal(rect.topLeft())
        o_x, o_y = self._popup_offset
        return p.x()+o_x, p.y()+o_y

    def _set_popup_style_(self, style):
        self._popup_style = style

    @classmethod
    def _get_popup_pos_0_(cls, widget):
        rect = widget.rect()
        # p = QtCore.QPoint(rect.right(), rect.center().y())
        p = widget.mapToGlobal(rect.bottomLeft())
        return p.x(), p.y()+1

    @classmethod
    def _get_popup_size_from_(cls, widget):
        rect = widget.rect()
        return rect.width(), rect.height()

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _refresh_widget_draw_geometry_(self):
        raise NotImplementedError()

    def _do_popup_start_(self, *args, **kwargs):
        raise NotImplementedError()

    def _do_popup_end_(self, *args, **kwargs):
        raise NotImplementedError()

    def _do_popup_close_(self, *args, **kwargs):
        self._widget.close()
        self._widget.deleteLater()

    def _set_popup_activated_(self, boolean):
        self._popup_is_activated = boolean
        if boolean is True:
            self._widget.show()
        else:
            self._widget.hide()

    def _get_popup_is_activated_(self):
        return self._popup_is_activated

    def _show_popup_as_style_0_(self, press_point, press_rect, desktop_rect, view_width, view_height):
        press_x, press_y = press_point.x(), press_point.y()
        press_w, press_h = press_rect.width(), press_rect.height()
        #
        width_maximum = desktop_rect.width()
        height_maximum = desktop_rect.height()
        #
        side = self._popup_side
        margin = self._popup_margin
        shadow_radius = self._popup_shadow_radius
        #
        o_x = 0
        o_y = 0
        #
        width_ = view_width+margin*2+side*2+shadow_radius
        height_ = view_height+margin*2+side*2+shadow_radius
        #
        r_x, r_y, region = bsc_core.RawCoordMtd.set_region_to(
            position=(press_x, press_y),
            size=(width_, height_),
            maximum_size=(width_maximum, height_maximum),
            offset=(o_x, o_y)
        )
        self._popup_region = region
        #
        if region in [0, 1]:
            y_ = r_y-side+press_h/2
        else:
            y_ = r_y+side+shadow_radius-press_h/2
        #
        if region in [0, 2]:
            x_ = r_x-margin*3
        else:
            x_ = r_x+margin*3+side+shadow_radius
        #
        self._widget.setGeometry(
            x_, y_,
            width_, height_
        )
        #
        self._refresh_widget_draw_geometry_()
        #
        self._widget.show()
        self._refresh_widget_draw_()

    def _show_popup_(self, pos, size):
        x, y = pos
        w, h = size
        # desktop_rect = get_qt_desktop_rect()
        self._widget.setGeometry(
            x, y,
            w, h
        )
        self._refresh_widget_draw_geometry_()
        #
        self._widget.show()
        #
        self._widget.update()

    def _set_entry_widget_(self, widget):
        self._entry_widget = widget
        self._entry_widget.installEventFilter(self._widget)

    def _get_entry_widget_(self):
        return self._entry_frame_widget

    def _set_entry_frame_widget_(self, widget):
        self._entry_frame_widget = widget

    def _get_entry_frame_widget_(self):
        return self._entry_frame_widget

    def _set_popup_use_as_storage_(self, boolean):
        self._use_as_storage = boolean

    def _set_popup_offset_(self, x, y):
        self._popup_offset = x, y

    def _do_popup_view_scroll_to_pre_(self):
        pass

    def _do_popup_view_scroll_to_next_(self):
        pass

    def _set_popup_auto_resize_enable_(self, boolean):
        self._popup_auto_resize_is_enable = boolean

    @classmethod
    def _compute_height_maximum_fnc_(cls, popup_view, row_maximum):
        rects = [popup_view.visualItemRect(popup_view.item(i)) for i in range(popup_view.count())[:row_maximum]]
        if rects:
            rect = rects[-1]
            y = rect.y()
            h = rect.height()
            return y+h+1+4
        return 0


class AbsQtValueDefaultExtraDef(object):
    def _init_value_default_extra_def_(self, widget):
        self._widget = widget
        self._value_default = None

    def _get_value_(self):
        raise NotImplementedError()

    def _set_value_default_(self, value):
        self._value_default = value

    def _get_value_default_(self):
        return self._value_default

    def _get_value_is_default_(self):
        return self._get_value_() == self._get_value_default_()


class AbsQtValueArrayBaseDef(object):
    def _init_value_array_base_def_(self, widget):
        self._widget = widget
        self._values = []

    def _clear_all_values_(self):
        self._values = []

    def _append_value_(self, value):
        if value not in self._values:
            self._values.append(value)
            return True
        return False

    def _insert_value_(self, index, value):
        self._values.insert(index, value)

    def _delete_value_(self, value):
        if value in self._values:
            self._values.remove(value)
            return True
        return False

    def _extend_values_(self, values):
        self._values.extend(values)

    def _set_values_(self, values):
        self._values = values

    def _get_values_(self):
        return self._values


class AbsQtActionForDropBaseDef(object):
    def _init_drop_base_def_(self, widget):
        self._widget = widget
        self._action_drop_is_enable = False

    def _set_drop_enable_(self, boolean):
        self._action_drop_is_enable = boolean


class AbsQtActionForDragDef(object):
    def _init_action_for_drag_def_(self, widget):
        self._widget = widget
        self._drag_is_enable = False

        self._drag_point_offset = QtCore.QPoint(0, 0)

        self._drag_press_point = QtCore.QPoint(0, 0)

        self._drag_urls = []
        self._drag_data = {}

        self._drag_and_drop_scheme = 'unknown'

        self._drag_mime_data = QtCore.QMimeData()

    def _set_drag_and_drop_scheme_(self, text):
        self._drag_and_drop_scheme = text

    def _get_drag_and_drop_scheme_(self):
        return self._drag_and_drop_scheme

    def _set_drag_enable_(self, boolean):
        self._drag_is_enable = boolean

    def _set_drag_urls_(self, urls):
        self._drag_urls = urls

    def _get_drag_urls_(self):
        return self._drag_urls

    def _set_drag_data_(self, data):
        if isinstance(data, dict):
            self._drag_data = data

    def _generate_drag_mime_data_(self):
        self._drag_mime_data = QtCore.QMimeData()
        for k, v in self._drag_data.items():
            self._drag_mime_data.setData(
                bsc_core.auto_encode(k), bsc_core.auto_encode(v)
            )
        #
        if self._drag_urls:
            self._drag_mime_data.setUrls(
                [QtCore.QUrl.fromLocalFile(i) for i in self._drag_urls]
            )
        return self._drag_mime_data

    def _get_drag_data_(self):
        return self._drag_data

    def _get_drag_mime_data_(self):
        return self._drag_mime_data


class AbsQtActionForDropDef(object):
    def _init_action_for_drop_def_(self, widget):
        self._widget = widget

        self._index_drag_child_polish_start = None
        self._index_drag_child_polish = None
        self._drag_rect_child_polish = QtCore.QRect()

        self._index_drag_child_add_start = None
        self._index_drag_child_add = None
        self._drag_rect_child_add = QtCore.QRect()

        self._drag_and_drop_scheme = 'unknown'

        self._drag_and_drop_key = None

    def _set_drag_and_drop_scheme_(self, text):
        self._drag_and_drop_scheme = text

    def _get_drag_and_drop_scheme_(self):
        return self._drag_and_drop_scheme

    def _get_drag_and_drop_key_(self):
        return self._drag_and_drop_key


class AbsQtIconBaseDef(object):
    class IconGeometryMode(object):
        Square = 0
        Auto = 1

    def _init_icon_base_def_(self, widget):
        self._widget = widget
        #
        self._icon_geometry_mode = self.IconGeometryMode.Square
        #
        self._icon_is_enable = False
        #
        self._icon_file_path = None
        self._icon_sub_file_path = None
        self._icon_file_is_enable = False
        self._hover_icon_file_path = None
        #
        self._icon_color_rgb = None
        self._icon_text = None
        self._icon_name_rgba = None
        self._icon_sub_text = None
        self._icon_name_is_enable = False
        #
        self._icon_name_auto_color = True
        #
        self._icon = None
        #
        self._icon_frame_draw_rect = QtCore.QRect()
        self._icon_draw_rect = QtCore.QRect()
        self._icon_sub_draw_rect = QtCore.QRect()
        #
        self._icon_color_draw_rect = QtCore.QRect()
        self._icon_text_draw_rect = QtCore.QRect()
        #
        self._icon_hover_color = None
        #
        self._icon_frame_draw_size = 20, 20
        #
        self._icon_draw_size = 16, 16
        self._icon_draw_percent = .75
        self._sub_icon_draw_size = 10, 10
        self._icon_sub_draw_percent = .5
        #
        self._icon_color_draw_size = 12, 12
        self._icon_name_draw_size = 12, 12
        self._icon_text_draw_percent = .675
        #
        self._icon_state_draw_is_enable = False
        self._icon_state_draw_rect = QtCore.QRect()
        self._icon_state_rect = QtCore.QRect()
        self._icon_state_file_path = None
        self._icon_state_draw_percent = .25
        self._icon_state_draw_rgb = 72, 72, 72

    def _set_icon_geometry_mode_(self, mode):
        self._icon_geometry_mode = mode

    def _set_icon_enable_(self, boolean):
        self._icon_is_enable = boolean

    def _set_icon_state_draw_enable_(self, boolean):
        self._icon_state_draw_is_enable = boolean

    def _set_icon_state_rgb_(self, color):
        pass

    def _set_icon_hover_color_(self, qt_color):
        self._icon_hover_color = qt_color

    def _set_icon_(self, icon):
        self._icon_is_enable = True
        self._icon = icon
        self._widget.update()

    def _set_icon_name_enable_(self, boolean):
        self._icon_name_is_enable = boolean

    def _set_icon_file_path_(self, file_path):
        self._icon_is_enable = True
        self._icon_file_path = file_path
        self._widget.update()

    def _set_icon_name_(self, icon_name):
        self._set_icon_file_path_(
            gui_core.GuiIcon.get(icon_name)
        )

    def _set_icon_sub_file_path_(self, file_path):
        self._icon_sub_file_path = file_path
        self._widget.update()

    def _set_icon_sub_text_(self, text):
        self._icon_sub_text = text
        self._widget.update()

    def _set_icon_sub_name_(self, icon_name):
        self._set_icon_sub_file_path_(
            gui_core.GuiIcon.get(icon_name)
        )

    def _set_icon_state_name_(self, icon_name):
        self._set_icon_state_file_path_(
            gui_core.GuiIcon.get(icon_name)
        )

    def _set_icon_state_file_path_(self, file_path):
        self._set_icon_state_draw_enable_(True)
        self._icon_state_file_path = file_path

    def _set_hover_icon_file_path_(self, file_path):
        self._hover_icon_file_path = file_path

    def _set_icon_frame_draw_size_(self, w, h):
        self._icon_frame_draw_size = w, h

    def _set_icon_file_draw_size_(self, w, h):
        self._icon_draw_size = w, h

    def _set_icon_file_draw_percent_(self, p):
        self._icon_draw_percent = p

    def _get_icon_file_path_(self):
        if self._icon_is_enable is True:
            return self._icon_file_path

    def _set_icon_color_rgb_(self, rgb):
        self._icon_is_enable = True
        self._icon_color_rgb = rgb
        self._widget.update()

    def _set_icon_name_text_(self, text):
        self._icon_is_enable = True
        self._icon_text = text
        self._widget.update()

    def _set_icon_name_auto_color_(self, boolean):
        self._icon_name_auto_color = boolean

    def _set_icon_name_rgba_(self, rgba):
        self._icon_name_rgba = rgba
        self._widget.update()

    def _set_color_icon_rect_(self, x, y, w, h):
        self._icon_color_draw_rect.setRect(
            x, y, w, h
        )

    def _set_icon_text_draw_rect_(self, x, y, w, h):
        self._icon_text_draw_rect.setRect(
            x, y, w, h
        )

    def _get_icon_name_text_(self):
        if self._icon_is_enable is True:
            return self._icon_text

    def _set_icon_frame_draw_rect_(self, x, y, w, h):
        self._icon_frame_draw_rect.setRect(
            x, y, w, h
        )

    def _set_icon_file_draw_rect_(self, x, y, w, h):
        self._icon_draw_rect.setRect(
            x, y, w, h
        )

    def _set_sub_icon_file_draw_rect_(self, x, y, w, h):
        self._icon_sub_draw_rect.setRect(
            x, y, w, h
        )

    def _get_file_icon_rect_(self):
        return self._icon_draw_rect

    def _set_icon_draw_percent_(self, p):
        self._icon_draw_percent = p


class AbsQtIconsBaseDef(object):
    def _init_icons_base_def_(self, widget):
        self._widget = widget
        #
        self._icons_enable = False
        self._icon_pixmaps = []
        self._icon_file_paths = []
        self._icon_name_texts = []
        self._icon_indices = []
        self._icon_rects = []
        #
        self._icon_frame_draw_size = 20, 20
        self._icon_draw_size = 16, 16
        self._icon_frame_draw_enable = False
        #
        self._icon_frame_draw_rect = QtCore.QRect()

    def _set_icon_file_path_(self, file_path):
        self._set_icon_file_paths_(
            [file_path]
        )

    def _set_icon_file_path_at_(self, file_path, index=0):
        self._icon_file_paths[index] = file_path

    def _get_icon_file_path_at_(self, index=0):
        if index in self._get_icon_indices_():
            return self._icon_file_paths[index]

    def _set_icon_rect_at_(self, x, y, w, h, index=0):
        self._icon_rects[index].setRect(
            x, y, w, h
        )

    def _get_icon_rect_at_(self, index=0):
        if index in self._get_icon_indices_():
            return self._icon_rects[index]

    def _set_icon_pixmaps_(self, pixmaps):
        self._icon_pixmaps = pixmaps
        self._icon_indices = range(len(pixmaps))
        self._icon_rects = []
        for _ in self._get_icon_indices_():
            self._icon_rects.append(
                QtCore.QRect()
            )

    def _get_icon_as_pixmap_at_(self, index):
        if index in self._get_icon_indices_():
            return self._icon_pixmaps[index]

    def _get_icons_as_pixmap_(self):
        return self._icon_pixmaps

    def _set_icon_file_paths_(self, file_paths):
        self._icon_file_paths = file_paths
        self._icon_indices = range(len(self._icon_file_paths))
        self._icon_rects = []
        for _ in self._get_icon_indices_():
            self._icon_rects.append(
                QtCore.QRect()
            )

    def _set_icons_by_name_text_(self, texts):
        self._icon_name_texts = texts
        self._icon_indices = range(len(self._icon_name_texts))
        self._icon_rects = []
        for _ in self._get_icon_indices_():
            self._icon_rects.append(
                QtCore.QRect()
            )

    def _get_icon_name_text_at_(self, index=0):
        return self._icon_name_texts[index]

    def _set_icon_name_rect_at_(self, index, name_text):
        self._icon_name_texts[index] = name_text

    def _set_icon_file_path_add_(self, file_path):
        self._icon_file_paths.append(file_path)
        self._icon_rects.append(QtCore.QRect())

    def _get_icon_file_paths_(self):
        return self._icon_file_paths

    def _get_icon_indices_(self):
        return self._icon_indices

    def _get_has_icons_(self):
        return self._icon_indices != []

    def _get_icon_count_(self):
        return len(self._icon_indices)

    def _set_icon_frame_draw_size_(self, w, h):
        self._icon_frame_draw_size = w, h

    def _set_icon_size_(self, w, h):
        self._icon_draw_size = w, h

    def _set_icon_frame_draw_enable_(self, boolean):
        self._icon_frame_draw_enable = boolean


class AbsQtIndexBaseDef(object):
    def _init_index_base_def_(self, widget):
        self._widget = widget
        self._index_draw_enable = False
        self._index = 0
        self._index_text = None
        self._index_text_color = gui_qt_core.QtFontColors.Dark
        self._index_text_font = gui_qt_core.QtFonts.Index
        self._index_text_option = QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter
        #
        self._index_frame_rect = QtCore.QRect()
        self._index_rect = QtCore.QRect()
        #
        self._index_frame_draw_enable = False
        self._index_draw_enable = False

    def _set_index_draw_enable_(self, boolean):
        self._index_draw_enable = boolean

    def _set_index_(self, index):
        self._index = index
        self._index_text = str(index+1)

    def _get_index_(self):
        return self._index

    def _get_index_text_(self):
        return self._index_text

    def _set_index_draw_rect_(self, x, y, w, h):
        self._index_rect.setRect(
            x, y, w, h
        )

    def _get_index_rect_(self):
        return self._index_rect


class AbsQtTypeDef(object):
    def _init_type_base_def_(self, widget):
        self._widget = widget
        #
        self._type_text = None
        self._type_rect = QtCore.QRect()
        self._type_color = QtGui.QColor(127, 127, 127, 255)

    def _set_type_text_(self, text):
        self._type_text = text or ''
        self._type_color = bsc_core.RawTextOpt(
            self._type_text
        ).to_rgb()

    def _set_type_draw_rect_(self, x, y, w, h):
        self._type_rect.setRect(
            x, y, w, h
        )


class AbsQtPathBaseDef(object):
    def _init_path_base_def_(self, widget):
        self._widget = widget
        self._path_text = None

    def _set_path_text_(self, text):
        self._path_text = text
        self._widget.update()

    def _get_path_text_(self):
        return self._path_text


class AbsQtValueBaseDef(object):
    def _init_value_base_def_(self, widget):
        self._widget = widget

        self._value_type = None

        self._value = None

        self._value_options = []

    def _set_value_type_(self, value_type):
        self._value_type = value_type

    def _get_value_type_(self):
        return self._value_type

    def _set_value_(self, value):
        if value != self._value:
            self._value = value
            return True
        return False

    def _get_value_(self):
        return self._value

    # value for choose
    def _set_value_options_(self, values):
        if values != self._value_options:
            self._value_options = values
            return True
        return False

    def _set_value_by_index_(self, index):
        if self._value_options:
            value = self._value_options[index]
            self._set_value_(value)

    def _get_value_options_(self):
        return self._value_options


class AbsQtValueValidationExtraDef(object):
    def _init_value_validation_extra_def_(self, widget):
        self._widget = widget
        # default is True
        self._value_validation_fnc = lambda x: True

        self._value_type = None
        self._value = None

    def _set_value_validation_fnc_(self, fnc):
        self._value_validation_fnc = fnc

    def _get_value_is_valid_(self, value):
        return self._value_validation_fnc(value)


class AbsQtValueHistoryExtraDef(object):
    def _get_value_is_valid_(self, *args, **kwargs):
        raise NotImplementedError()

    def _init_value_history_base_def_(self, widget):
        self._widget = widget

        self._history_key = None

        self.__history_values = []

    def _set_history_values_(self, texts):
        self.__history_values = texts

    def _get_history_values_(self):
        return self.__history_values

    def _clear_history_values_(self):
        self.__history_values = []

    def _set_history_key_(self, key):
        self._history_key = key
        self._refresh_history_()

    def _get_history_key_(self):
        return self._history_key

    def _get_history_latest_(self):
        if self._history_key is not None:
            return gui_core.GuiHistory.get_latest(self._history_key)

    def _pull_history_(self, *args, **kwargs):
        raise NotImplementedError()

    def _push_history_(self, value):
        if self._history_key is not None:
            if value:
                if self._get_value_is_valid_(value) is True:
                    gui_core.GuiHistory.append(
                        self._history_key,
                        value
                    )
            #
            self._refresh_history_()

    def _pull_history_latest_(self):
        if self._history_key is not None:
            value = gui_core.GuiHistory.get_latest(self._history_key)
            if value is not None:
                self._pull_history_(value)
                return True
        return False

    def _refresh_history_(self):
        if self._history_key is not None:
            values = gui_core.GuiHistory.get_all(
                self._history_key
            )
            if values:
                # latest show on top
                values.reverse()
                # value validation
                values = [i for i in values if self._get_value_is_valid_(i) is True]
                self._set_history_values_(values)
            else:
                self._clear_history_values_()

        self._refresh_history_extend_()

    def _refresh_history_extend_(self):
        pass


class AbsQtNameBaseDef(object):
    AlignRegion = gui_core.GuiAlignRegion

    def _init_name_base_def_(self, widget):
        self._widget = widget
        #
        self._name_enable = False
        self._name_text = None
        self._name_text_orig = None
        self._name_draw_font = gui_qt_core.QtFonts.NameNormal
        #
        self._name_align = self.AlignRegion.Center
        #
        self._name_color = gui_qt_core.QtFontColors.Basic
        self._hover_name_color = gui_qt_core.QtFontColors.Light
        self._name_text_option = QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter
        #
        self._name_word_warp = True
        #
        self._name_width = 160
        #
        self._name_frame_size = 20, 20
        self._name_draw_size = 16, 16
        self._name_frame_draw_rect = QtCore.QRect()
        self._name_draw_rect = QtCore.QRect()

        self._tool_tip_text = None

    def _set_name_align_(self, align):
        self._name_align = align

    def _set_name_color_(self, color):
        self._name_color = color

    def _get_name_text_draw_width_(self, text=None):
        if text is None:
            text = self._name_text
        # print self._widget.fontMetrics().width(text), text
        return self._widget.fontMetrics().width(text)

    def _set_name_text_(self, text):
        self._name_enable = True
        self._name_text = text
        #
        if self._tool_tip_text is not None:
            self._set_tool_tip_text_(self._tool_tip_text)
        #
        self._widget.update()

    def _get_name_text_(self):
        if self._name_enable is True:
            return self._name_text

    def _get_name_text_option_(self):
        return self._name_text_option

    def _set_name_text_option_(self, option):
        self._name_text_option = option

    def _set_name_text_option_to_align_center_(self):
        self._name_text_option = QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter
        self._widget.update()

    def _set_name_text_option_to_align_center_top_(self):
        self._name_text_option = QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop
        self._widget.update()

    def _set_name_width_(self, w):
        self._name_width = w

    def _set_name_frame_rect_(self, x, y, w, h):
        self._name_frame_draw_rect.setRect(
            x, y, w, h
        )

    def _set_name_draw_rect_(self, x, y, w, h):
        self._name_draw_rect.setRect(
            x, y, w, h
        )

    def _get_name_rect_(self):
        return self._name_draw_rect

    def _set_tool_tip_(self, raw, **kwargs):
        if raw is not None:
            if isinstance(raw, (tuple, list)):
                _ = '\n'.join(raw)
            elif isinstance(raw, six.string_types):
                _ = raw
            else:
                raise TypeError()
            #
            self._set_tool_tip_text_(_, **kwargs)

    def _set_tool_tip_text_(self, text, **kwargs):
        self._tool_tip_text = text
        if hasattr(self, 'setToolTip'):
            css = (
                '<html>\n'
                '<body>\n'
                '<style>.no_wrap{white-space:nowrap;}</style>\n'
                '<style>.no_warp_and_center{white-space:nowrap;text-align: center;}</style>\n'
            )
            name_text = self._name_text
            if 'name' in kwargs:
                name_text = kwargs['name']
            #
            if name_text:
                name_text = bsc_core.auto_encode(name_text)
                name_text = name_text.replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;')
                css += '<h3><p class="no_warp_and_center">{}</p></h3>\n'.format(name_text)

            if text:
                # add split line
                css += '<p><hr></p>\n'
                text = bsc_core.auto_encode(text)
                if isinstance(text, six.string_types):
                    texts = text.split('\n')
                elif isinstance(text, (tuple, list)):
                    texts = text
                else:
                    raise RuntimeError()
                #
                for i_text in texts:
                    i_text = bsc_core.auto_encode(i_text)
                    i_text = i_text.replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;')
                    i_text = gui_qt_core.GuiQtUtil.generate_tool_tip_action_css(i_text)
                    css += '<p class="no_wrap">{}</p>\n'.format(i_text)

            if 'action_tip' in kwargs:
                action_tip = kwargs['action_tip']
                css += '<p><hr></p>\n'
                action_tip = action_tip.replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;')
                action_tip = gui_qt_core.GuiQtUtil.generate_tool_tip_action_css(action_tip)
                css += '<p class="no_wrap">{}</p>\n'.format(action_tip)

            css += '</body>\n</html>'
            # noinspection PyCallingNonCallable
            # self._tool_tip_text = css
            self.setToolTip(css)

    def _set_name_font_size_(self, size):
        font = self._widget.font()
        font.setPointSize(size)
        self._name_draw_font = font
        self._widget.setFont(self._name_draw_font)

    def _set_name_draw_font_(self, font):
        self._name_draw_font = font
        self._widget.setFont(self._name_draw_font)

    def _set_name_text_orig_(self, text):
        self._name_text_orig = text

    def _get_name_text_orig_(self):
        return self._name_text_orig


class AbsQtNamesBaseDef(AbsQtNameBaseDef):
    def _refresh_widget_all_(self):
        pass

    def _init_names_base_def_(self, widget):
        self._init_name_base_def_(widget)
        #
        self._widget = widget
        #
        self._names_enable = False
        self._name_texts = []
        self._name_indices = []
        self._name_draw_rects = []
        #
        self._name_text_dict = collections.OrderedDict()
        self._name_key_rect = []
        self._name_value_rect = []
        #
        self._name_frame_size = 20, 20
        self._name_size = 16, 16
        self._name_frame_draw_enable = False
        #
        self._name_word_warp = True
        #
        self._name_frame_border_color = 0, 0, 0, 0
        self._name_frame_background_color = 95, 95, 95, 127
        #
        self._names_draw_range = None
        #
        self._name_frame_draw_rect = QtCore.QRect(0, 0, 0, 0)

    def _set_name_text_at_(self, text, index=0):
        self._name_texts[index] = text

    def _get_name_text_at_(self, index=0):
        if index in self._get_name_indices_():
            return self._name_texts[index]

    def _set_name_text_draw_rect_at_(self, x, y, w, h, index=0):
        self._name_draw_rects[index].setRect(
            x, y, w, h
        )

    def _set_name_text_(self, text):
        if not isinstance(text, six.text_type):
            text = str(text)

        self._name_text = text

    def _get_name_text_(self):
        if self._name_text:
            return self._name_text
        if self._name_texts:
            return self._name_texts[0]

    def _set_name_texts_(self, texts):
        self._name_texts = texts
        self._name_indices = range(len(texts))
        self._name_draw_rects = []
        for _ in self._get_name_indices_():
            self._name_draw_rects.append(
                QtCore.QRect()
            )
        #
        self._refresh_widget_all_()

    def _get_name_texts_(self):
        return self._name_texts

    def _set_name_text_dict_(self, text_dict):
        self._name_text_dict = text_dict
        self._set_name_texts_(
            [v if seq == 0 else '{}: {}'.format(k, v) for seq, (k, v) in enumerate(self._name_text_dict.items())]
        )
        self._refresh_widget_all_()

    def _get_show_name_texts_(self):
        if self._name_text_dict:
            return ['{}: {}'.format(k, v) for seq, (k, v) in enumerate(self._name_text_dict.items())]
        return self._get_name_texts_()

    def _get_name_text_dict_(self):
        return self._name_text_dict

    def _set_names_draw_range_(self, range_):
        self._names_draw_range = range_

    def _set_name_frame_border_color_(self, color):
        self._name_frame_border_color = color

    def _get_name_frame_border_color_(self):
        return self._name_frame_border_color

    def _set_name_frame_background_color_(self, color):
        self._name_frame_background_color = color

    def _get_name_frame_background_color_(self):
        return self._name_frame_background_color

    def _get_name_rect_at_(self, index=0):
        return self._name_draw_rects[index]

    def _get_name_indices_(self):
        return self._name_indices

    def _get_has_names_(self):
        return self._name_indices != []

    def _set_name_frame_size_(self, w, h):
        self._name_frame_size = w, h

    def _set_name_size_(self, w, h):
        self._name_size = w, h

    def _set_name_frame_draw_enable_(self, boolean):
        self._name_frame_draw_enable = boolean

    def _set_tool_tip_text_(self, text, **kwargs):
        if hasattr(self, 'setToolTip'):
            css = (
                '<html>\n'
                '<body>\n'
                '<style>.no_wrap{white-space:nowrap;float:right;}</style>\n'
                '<style>.no_warp_and_center{white-space:nowrap;text-align:center;}</style>\n'
            )
            #
            name_text = self._name_text
            if name_text:
                name_text = bsc_core.auto_encode(name_text)
                name_text = name_text.replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;')
                css += '<h2><p class="no_warp_and_center">{}</p></h2>\n'.format(name_text)
            #
            name_texts = self._get_show_name_texts_()
            if name_texts:
                css += '<p><hr></p>\n'
                for i_text in name_texts:
                    i_text = bsc_core.auto_encode(i_text)
                    i_text = i_text.replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;')
                    css += '<p class="no_wrap">{}</p>\n'.format(i_text)
            #
            if text:
                text = bsc_core.auto_encode(text)
                css += '<p><hr></p>\n'
                if isinstance(text, six.string_types):
                    texts_extend = text.split('\n')
                elif isinstance(text, (tuple, list)):
                    texts_extend = text
                else:
                    raise RuntimeError()
                #
                for i_text in texts_extend:
                    i_text = bsc_core.auto_encode(i_text)
                    i_text = i_text.replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;')
                    i_text = gui_qt_core.GuiQtUtil.generate_tool_tip_action_css(i_text)
                    css += '<p class="no_wrap">{}</p>\n'.format(i_text)

            css += '</body>\n</html>'
            self.setToolTip(css)


class AbsQtItemLayoutBaseDef(object):
    def _init_item_layout_base_def_(self, widget):
        self._widget = widget
        self._layout_item = None

    def _set_layout_item_(self, widget):
        self._layout_item = widget

    def _get_layout_item_(self):
        return self._layout_item


class AbsQtProgressBaseDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _refresh_widget_draw_geometry_(self):
        pass

    def _init_progress_base_def_(self):
        self._progress_height = 2
        #
        self._progress_maximum = 0
        self._progress_value = 0
        #
        self._progress_map_maximum = 10
        self._progress_map_value = 0
        #
        self._progress_rect = QtCore.QRect()
        #
        self._progress_raw = []

    def _set_progress_height_(self, value):
        self._progress_height = value

    def _set_progress_run_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()
        #
        QtWidgets.QApplication.instance().processEvents(
            QtCore.QEventLoop.ExcludeUserInputEvents
        )

    def _set_progress_maximum_(self, value):
        self._progress_maximum = value

    def _set_progress_map_maximum_(self, value):
        self._progress_map_maximum = value

    def _set_progress_value_(self, value):
        self._progress_value = value
        #
        if self._progress_map_maximum > 1:
            map_value = int(
                bsc_core.RawValueRangeMtd.set_map_to(
                    (1, self._progress_maximum), (1, self._progress_map_maximum),
                    self._progress_value
                )
            )
            self._set_progress_map_value_(map_value)

    def _set_progress_map_value_(self, map_value):
        if map_value != self._progress_map_value:
            self._progress_map_value = map_value
            #
            self._set_progress_run_()

    def _set_progress_update_(self):
        self._set_progress_value_(self._progress_value+1)

    def _stop_progress_(self):
        self._set_progress_value_(0)
        self._progress_raw = []
        #
        self._refresh_widget_draw_()

    def _get_progress_percent_(self):
        return float(self._progress_map_value)/float(self._progress_map_maximum)

    def _set_progress_raw_(self, raw):
        self._progress_raw = raw

    def _get_progress_is_enable_(self):
        return self._progress_map_value != 0


class AbsQtImageBaseDef(object):
    def _init_image_base_def_(self):
        self._image_enable = False
        self._image_draw_is_enable = False
        #
        self._image_file_path = None
        self._image_sub_file_path = None
        self._image_text = None
        self._image_data = None
        self._image_pixmap = None
        #
        self._image_frame_size = 32, 32
        self._image_draw_size = 30, 30
        self._image_draw_percent = .75
        self._image_frame_draw_enable = False
        #
        self._image_frame_rect = QtCore.QRect(0, 0, 0, 0)
        self._image_draw_rect = QtCore.QRect(0, 0, 0, 0)
        self._image_sub_draw_rect = QtCore.QRect(0, 0, 0, 0)

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _set_image_file_path_(self, arg):
        self._image_enable = True
        self._image_draw_is_enable = True
        if isinstance(arg, six.string_types):
            self._image_file_path = arg
        elif isinstance(arg, QtGui.QPixmap):
            self._image_pixmap = arg
        self._refresh_widget_draw_()

    def _set_image_sub_file_path_(self, file_path):
        self._image_sub_file_path = file_path
        self._refresh_widget_draw_()

    def _set_image_text_(self, text):
        self._image_text = text
        self._refresh_widget_draw_()

    def _set_image_url_(self, url):
        self._image_draw_is_enable = True
        # noinspection PyBroadException
        try:
            self._image_data = urllib.urlopen(url).read()
        except Exception:
            pass

        self._refresh_widget_draw_()

    def _set_image_draw_enable_(self, boolean):
        self._image_draw_is_enable = boolean

    def _get_image_data(self):
        if self._image_enable is True:
            return self._image_data

    def _set_image_draw_size_(self, w, h):
        self._image_draw_size = w, h

    def _get_image_draw_size_(self):
        return self._image_draw_size

    def _get_image_size_(self):
        if self._image_file_path is not None:
            if os.path.isfile(self._image_file_path):
                ext = os.path.splitext(self._image_file_path)[-1]
                if ext in ['.jpg', '.png']:
                    image = QtGui.QImage(self._image_file_path)
                    if image.isNull() is False:
                        # image.save(self._image_file_path, 'PNG')
                        s = image.size()
                        return s.width(), s.height()
                elif ext in ['.mov']:
                    pass
        return self._image_draw_size

    def _get_image_file_path_(self):
        if self._image_enable is True:
            return self._image_file_path

    def _set_image_rect_(self, x, y, w, h):
        self._image_draw_rect.setRect(
            x, y, w, h
        )

    def _get_image_rect_(self):
        return self._image_draw_rect

    def _get_has_image_(self):
        return (
                self._image_file_path is not None or
                self._image_sub_file_path is not None or
                self._image_text is not None or
                self._image_pixmap is not None
        )

    def _set_image_frame_draw_enable_(self, boolean):
        self._image_frame_draw_enable = boolean

    def _get_image_frame_rect_(self):
        return self._image_frame_rect


class AbsQtMovieBaseDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _init_movie_base_def_(self):
        self._play_draw_enable = False
        self._movie_rect = QtCore.QRect()

    def _get_play_draw_is_enable_(self):
        return self._play_draw_enable

    def _set_play_draw_enable_(self, boolean):
        self._play_draw_enable = boolean

    def _set_movie_rect_(self, x, y, w, h):
        self._movie_rect.setRect(x, y, w, h)


class AbsQtChartBaseDef(object):
    def _init_chart_base_def_(self, widget):
        self._widget = widget
        self._chart_data = None
        self._chart_draw_data = None
        self._chart_mode = gui_core.GuiSectorChartMode.Completion
        #
        self._hover_flag = False
        self._hover_point = QtCore.QPoint()
        #
        r, g, b = 143, 143, 143
        h, s, v = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        color = bsc_core.RawColorMtd.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        #
        self._chart_border_color = color
        self._hover_chart_border_color = hover_color
        self._chart_background_color = 39, 39, 39, 255
        #
        self._chart_text_color = 0, 0, 0, 255

    def _set_chart_data_(self, data, mode):
        self._chart_data = data
        self._chart_mode = mode
        #
        self._refresh_chart_data_()
        #
        self._set_chart_data_post_run_()
        #
        self._widget.update()

    def _set_chart_data_post_run_(self):
        pass

    def _refresh_chart_data_(self):
        raise NotImplementedError()

    def _set_height_(self, h):
        # noinspection PyUnresolvedReferences
        self.setMaximumHeight(h)
        # noinspection PyUnresolvedReferences
        self.setMinimumHeight(h)


class AbsQtThreadBaseDef(object):
    def _init_thread_base_def_(self, widget):
        self._widget = widget

        self._qt_thread_enable = bsc_core.EnvBaseMtd.get_qt_thread_enable()

        self._thread_draw_flag = False
        self._thread_load_index = 0

        self._thread_running_timer = QtCore.QTimer()
        self._thread_running_timer.timeout.connect(self._refresh_thread_draw_)

        self.__thread_exists = None

    def _set_action_busied_(self, *args, **kwargs):
        raise NotImplementedError()

    def _start_thread_draw_(self):
        self._set_action_busied_(True)
        self._thread_draw_flag = True
        self._thread_load_index = 0
        self._thread_running_timer.start(100)
        self._refresh_thread_draw_()

    def _stop_thread_draw_(self):
        self._set_action_busied_(False)
        self._thread_draw_flag = False
        self._thread_running_timer.stop()
        self._thread_load_index = 0
        self._refresh_thread_draw_()

    def _thread_start_accept_fnc_(self, thread):
        if self.__thread_exists:
            if thread.isFinished() is False:
                thread.do_quit()
            self.__thread_exists = None

        self.__thread_exists = thread
        if self._thread_draw_flag is False:
            self._start_thread_draw_()

    def _thread_finish_accept_fnc_(self, thread):
        if thread.isFinished() is False:
            thread.do_quit()
        self.__thread_exists = None
        self._stop_thread_draw_()

    def _refresh_thread_draw_(self):
        self._thread_load_index += 1
        self._widget.update()

    def _run_build_use_thread_(self, cache_fnc, build_fnc, post_fnc):
        if self._qt_thread_enable is True:
            t = gui_qt_core.QtBuildThreadExtra(self._widget)
            t.set_cache_fnc(cache_fnc)
            t.cache_value_accepted.connect(build_fnc)
            t.run_finished.connect(post_fnc)
            t.start_accepted.connect(self._thread_start_accept_fnc_)
            t.finish_accepted.connect(self._thread_finish_accept_fnc_)
            t.start()
        else:
            build_fnc(cache_fnc())
            post_fnc()

    def _run_fnc_use_thread_(self, fnc):
        if self._qt_thread_enable is True:
            t = gui_qt_core.QtMethodThread(self._widget)
            t.append_method(fnc)
            t.start_accepted.connect(self._thread_start_accept_fnc_)
            t.finish_accepted.connect(self._thread_finish_accept_fnc_)
            t.start()


class AbsQtChooseExtraDef(object):
    input_choose_changed = qt_signal()
    user_input_choose_changed = qt_signal()
    # when popup item choose, send choose text form this emit
    user_input_choose_value_accepted = qt_signal(str)
    user_input_choose_values_accepted = qt_signal(list)

    def _init_choose_extra_def_(self, widget):
        self._widget = widget

        self._choose_expand_icon_file_path = gui_core.GuiIcon.get('choose_expand')
        self._choose_collapse_icon_file_path = gui_core.GuiIcon.get('choose_collapse')
        #
        self._choose_is_activated = False

        self._choose_values = []
        self._choose_values_current = []

        self._choose_index_show_enable = False

    def _get_choose_is_activated_(self):
        return self._choose_is_activated

    def _set_choose_activated_(self, boolean):
        self._choose_is_activated = boolean

    def _set_item_choose_content_raw_(self, raw):
        if isinstance(raw, (tuple, list)):
            self._choose_values = list(raw)

    def _set_choose_values_(self, values, *args, **kwargs):
        self._choose_values = values

    def _clear_choose_values_(self):
        self._choose_values = []
        self._choose_values_current = []

    def _get_choose_values_(self):
        return self._choose_values

    def _get_choose_value_at_(self, index):
        return self._choose_values[index]

    def _get_choose_current_values_append_(self, value):
        self._choose_values_current.append(value)

    def _extend_choose_values_current_(self, values):
        pass

    # noinspection PyUnusedLocal
    def _choose_value_completion_gain_fnc_(self, *args, **kwargs):
        return ctt_core.ContentUtil.filter(
            self._choose_values, '*{}*'.format(
                bsc_core.auto_encode((args[0]))
            )
        )

    def _refresh_choose_index_(self):
        raise NotImplementedError()

    def _set_choose_index_show_enable_(self, boolean):
        self._choose_index_show_enable = boolean
        self._refresh_choose_index_()


class AbsQtActionForEntryDef(object):
    entry_value_changed = qt_signal()
    entry_value_cleared = qt_signal()
    # change
    user_entry_value_changed = qt_signal()
    # clear
    user_entry_value_cleared = qt_signal()

    def _init_action_for_entry_def_(self, widget):
        pass


class AbsQtGuideBaseDef(object):
    guide_press_clicked = qt_signal()
    guide_press_db_clicked = qt_signal()
    #
    guide_text_accepted = qt_signal(str)
    guide_text_choose_accepted = qt_signal(str)
    guide_text_press_accepted = qt_signal(str)
    #
    QT_GUIDE_RECT_CLS = None

    def _init_guide_base_def_(self, widget):
        self._widget = widget
        #
        self._guide_items = []
        self._guide_index_current = None

        self._guide_type_texts = []
        self._guide_dict = {}
        #
        self._guide_item_extend = None

    def _set_guide_type_texts_(self, texts):
        self._guide_type_texts = texts

    def _set_guide_dict_(self, dict_):
        self._guide_dict = dict_

    def _create_guide_item_(self):
        item = self.QT_GUIDE_RECT_CLS()
        self._guide_items.append(item)
        return item

    def _get_guide_items_(self):
        return self._guide_items

    def _get_guide_item_indices_(self):
        return range(len(self._get_guide_items_()))

    def _get_guide_item_at_(self, index=0):
        if self._guide_items:
            if index < len(self._guide_items):
                return self._guide_items[index]

    def _restore_guide_(self):
        self._guide_items = []
        self._guide_index_current = None

    def _clear_all_guide_items_(self):
        self._guide_items = []

    def _set_guide_current_index_(self, index):
        self._guide_index_current = index

    def _clear_guide_current_(self):
        self._guide_index_current = None

    def _set_guide_name_text_at_(self, name_text, index=0):
        item = self._get_guide_item_at_(index)
        path_text = item._path_text
        child_path_text = bsc_core.PthNodeMtd.get_dag_child_path(path_text, name_text)
        #
        self._set_guide_path_text_(child_path_text)
        return child_path_text

    def _set_guide_path_text_(self, path_text):
        pass

    def _get_guide_name_text_at_(self, index=0):
        return self._get_guide_item_at_(index)._get_name_text_()

    def _get_guide_path_text_at_(self, index=0):
        return self._get_guide_item_at_(index)._path_text


class AbsQtGuideEntryDef(AbsQtGuideBaseDef):
    QT_POPUP_GUIDE_CHOOSE_CLS = None

    def _init_guide_entry_def_(self, widget):
        self._init_guide_base_def_(widget)
        #
        self._popup_guide_choose_widget = None
        #
        self._guide_choose_index_current = None

    def _get_action_flag_(self):
        raise NotImplementedError()

    def _get_action_flag_is_match_(self, flag):
        raise NotImplementedError()

    def _get_guide_choose_point_at_(self, index=0):
        item = self._get_guide_item_at_(index)
        rect = item._icon_frame_draw_rect
        return self._widget.mapToGlobal(rect.center())

    def _get_guide_choose_rect_at_(self, index=0):
        item = self._get_guide_item_at_(index)
        rect = item._icon_frame_draw_rect
        return rect

    def _set_guide_choose_item_current_at_(self, text, index=0):
        item = self._get_guide_item_at_(index)
        if item is not None:
            item._set_name_text_(text)

    def _get_guide_choose_item_current_at_(self, index=0):
        item = self._get_guide_item_at_(index)
        if item is not None:
            return item._name_text

    #
    def _set_guide_choose_item_content_at_(self, raw, index=0):
        item = self._get_guide_item_at_(index)
        if item is not None:
            item._set_item_choose_content_raw_(raw)

    #
    def _get_guide_child_name_texts_at_(self, index=0):
        item = self._get_guide_item_at_(index)
        if item is not None:
            return self._get_guide_child_name_texts_from_(item)

    def _get_guide_sibling_name_texts_at_(self, index=0):
        item = self._get_guide_item_at_(index)
        if item is not None:
            return self._get_guide_sibling_name_texts_from_(item)

    def _get_guide_child_name_texts_from_(self, item):
        return bsc_core.PthNodeMtd.find_dag_child_names(
            item._path_text, self._get_guide_valid_path_texts_()
        )

    def _get_guide_sibling_name_texts_from_(self, item):
        return bsc_core.PthNodeMtd.find_dag_sibling_names(
            item._path_text, self._get_guide_valid_path_texts_()
        )

    def _get_guide_valid_path_texts_(self):
        # todo, fnc "get_is_enable" is from proxy
        return [k for k, v in self._guide_dict.items() if v is None or v.get_is_enable() is True]

    def _start_guide_choose_item_popup_at_(self, index=0):
        self._popup_guide_choose_widget = self.QT_POPUP_GUIDE_CHOOSE_CLS(self)
        self._popup_guide_choose_widget._set_entry_widget_(self._widget)
        self._popup_guide_choose_widget._set_entry_frame_widget_(self._widget)
        self._popup_guide_choose_widget._do_popup_start_(index)

    def _set_guide_choose_item_expanded_at_(self, boolean, index=0):
        item = self._get_guide_item_at_(index)
        if item is not None:
            item._set_choose_activated_(boolean)

    def _get_guide_choose_item_is_expanded_at_(self, index=0):
        item = self._get_guide_item_at_(index)
        if item is not None:
            return item._get_choose_is_activated_()

    def _set_guide_choose_item_expand_at_(self, index=0):
        self._set_guide_choose_item_expanded_at_(True, index)

    def _set_guide_choose_item_collapse_at_(self, index=0):
        self._set_guide_choose_item_expanded_at_(False, index)
        self._widget.update()

    def _get_is_guide_choose_flag_(self):
        return self._get_action_flag_is_match_(
            gui_core.GuiActionFlag.ChoosePress
        )

    def _restore_guide_(self):
        self._guide_items = []
        self._guide_choose_index_current = None
        self._guide_index_current = None

    def _set_guide_choose_current_index_(self, index):
        self._guide_choose_index_current = index

    def _clear_guide_choose_current_(self):
        self._guide_choose_index_current = None

    def _restore_guide_choose_(self):
        widget_pre = self._popup_guide_choose_widget
        if widget_pre is not None:
            widget_pre._do_popup_close_()


class AbsQtPressSelectExtraDef(object):
    user_press_select_accepted = qt_signal(bool)

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    #
    def _init_press_select_extra_def_(self, widget):
        self._widget = widget
        #
        self._is_selected = False

    def _get_action_flag_(self):
        raise NotImplementedError()

    def _set_selected_(self, boolean):
        self._is_selected = boolean
        self._refresh_widget_draw_()

    def _get_is_selected_(self):
        return self._is_selected


class AbsQtItemMovieActionDef(object):
    movie_play_press_clicked = qt_signal()

    def _set_item_movie_action_def_init_(self):
        self._item_movie_play_rect = QtCore.QRect()

    def _set_item_movie_play_rect_(self, x, y, w, h):
        self._item_movie_play_rect.setRect(x, y, w, h)

    def _set_item_movie_play_press_clicked_connect_to_(self, fnc):
        pass

    def _set_item_movie_pay_press_clicked_emit_send_(self):
        self.movie_play_press_clicked.emit()


class AbsQtItemWidgetExtra(object):
    def _init_item_widget_extra_(self, widget):
        self._widget = widget
        self._item = None

    def _set_item_(self, item):
        self._item = item

    def _get_item_(self):
        return self._item


class AbsQtBuildViewDef(object):
    def _init_view_build_extra_def_(self):
        pass

    def _setup_view_build_(self, view):
        self._build_runnable_stack = gui_qt_core.QtBuildRunnableStack(
            view
        )


class AbsQtViewSelectActionDef(object):
    def _set_view_select_action_def_init_(self):
        self._pre_selected_items = []

    def _set_view_item_selected_(self, item, boolean):
        raise NotImplementedError()

    def _set_item_widget_selected_(self, item, boolean):
        raise NotImplementedError()

    def _get_selected_items_(self):
        raise NotImplementedError()

    def _get_selected_item_widgets_(self):
        raise NotImplementedError()

    def _view_item_select_cbk(self):
        raise NotImplementedError()

    def _set_selection_use_multiply_(self):
        pass

    def _set_selection_use_single_(self):
        pass

    def _get_is_multiply_selection_(self):
        pass

    def _clear_selection_(self):
        pass


class AbsQtViewScrollActionDef(object):
    def _set_view_scroll_action_def_init_(self):
        self._scroll_is_enable = True

    def _set_scroll_enable_(self, boolean):
        self._scroll_is_enable = boolean

    def _get_view_h_scroll_bar_(self):
        raise NotImplementedError()

    def _get_view_v_scroll_bar_(self):
        raise NotImplementedError()

    def _get_view_v_scroll_value_(self):
        return self._get_view_v_scroll_bar_().value()

    def _get_v_minimum_scroll_value_(self):
        return self._get_view_v_scroll_bar_().minimum()

    def _get_v_maximum_scroll_value_(self):
        return self._get_view_v_scroll_bar_().maximum()

    def _get_v_scroll_percent_(self):
        v = self._get_view_v_scroll_value_()
        v_min, v_max = self._get_v_minimum_scroll_value_(), self._get_v_maximum_scroll_value_()
        if v_max > 0:
            return float(v)/float(v_max)
        return 0


class AbsQtItemFilterDef(object):
    TagFilterMode = gui_core.GuiTagFilterMode

    def _init_item_filter_extra_def_(self, widget):
        self._widget = widget
        self._item_keyword_filter_mode = self.TagFilterMode.MatchAll
        #
        self._item_tag_filter_mode = self.TagFilterMode.MatchAll
        self._item_tag_filter_keys_src = set()
        self._item_tag_filter_keys_tgt = set()
        #
        self._item_semantic_tag_filter_mode = self.TagFilterMode.MatchAll
        self._item_semantic_tag_filter_keys_tgt = dict()
        #
        self._item_keyword_filter_keys_tgt = set()
        #
        self._item_tag_filter_tgt_statistic_enable = False
        #
        self._item_keyword_filter_keys_tgt_cache = None

    def _set_item_keyword_filter_keys_tgt_(self, keys):
        self._item_keyword_filter_keys_tgt = set(keys)

    def _add_item_keyword_filter_key_tgt_(self, key):
        self._item_keyword_filter_keys_tgt.add(key)

    def _update_item_keyword_filter_keys_tgt_(self, keys):
        self._item_keyword_filter_keys_tgt.update(set(keys))

    def _get_keyword_filter_keys_tgt_(self):
        return list(self._item_keyword_filter_keys_tgt)

    def _get_keyword_filter_keys_tgt_as_split_(self):
        return [j for i in self._get_keyword_filter_keys_tgt_() for j in bsc_core.RawTextMtd.find_words(i)]

    def _get_keyword_filter_keys_auto_(self):
        keys = self._get_keyword_filter_keys_tgt_()
        if keys:
            return [i for i in keys if i]
        else:
            if hasattr(self, '_get_name_texts_'):
                if self._get_name_texts_():
                    return [i for i in self._get_name_texts_() if i]
            if hasattr(self, '_get_name_text_'):
                return [self._get_name_text_()]
        return []

    def _get_keyword_filter_keys_auto_use_cache_(self):
        if self._item_keyword_filter_keys_tgt_cache is not None:
            return self._item_keyword_filter_keys_tgt_cache
        self._item_keyword_filter_keys_tgt_cache = self._get_keyword_filter_keys_auto_()
        return self._item_keyword_filter_keys_tgt_cache

    def _generate_keyword_filter_keys_(self):
        return [j for i in self._get_keyword_filter_keys_auto_use_cache_() for j in bsc_core.RawTextMtd.split_any_to(i)]

    def _get_item_keyword_filter_context_(self):
        return '+'.join(self._get_keyword_filter_keys_auto_use_cache_())

    def _generate_item_keyword_filter_tgt_args_(self, texts):
        # todo: use match all mode then, maybe use match one mode also
        if texts:
            context = self._get_item_keyword_filter_context_()
            context = context.lower()
            for i_text in texts:
                # do not encode, keyword can be use unicode
                i_text = i_text.lower()
                if '*' in i_text:
                    i_filter_key = six.u('*{}*').format(i_text.lstrip('*').rstrip('*'))
                    if not fnmatch.filter([context], i_filter_key):
                        return True, True
                else:
                    if i_text not in context:
                        return True, True
            return True, False
        return False, False

    def _set_item_tag_filter_mode_(self, mode):
        self._item_tag_filter_mode = mode

    def _get_item_tag_filter_mode_(self):
        return self._item_tag_filter_mode

    # tag filter source
    def _set_item_tag_filter_keys_src_add_(self, key):
        self._item_tag_filter_keys_src.add(key)

    def _set_item_tag_filter_keys_src_update_(self, keys):
        self._item_tag_filter_keys_src.update(set(keys))

    def _get_item_tag_filter_keys_src_(self):
        return list(self._item_tag_filter_keys_src)

    # tag filter target
    def _add_item_tag_filter_key_tgt_(self, key, ancestors=False):
        self._item_tag_filter_keys_tgt.add(key)
        #
        if ancestors is True:
            self._set_item_tag_filter_tgt_ancestors_update_()

    def _update_item_tag_filter_keys_tgt_(self, keys):
        self._item_tag_filter_keys_tgt.update(set(keys))

    def _get_item_tag_filter_keys_tgt_(self):
        return self._item_tag_filter_keys_tgt

    def _set_item_tag_filter_tgt_ancestors_update_(self):
        pass

    def _set_item_tag_filter_tgt_statistic_enable_(self, boolean):
        self._item_tag_filter_tgt_statistic_enable = boolean

    def _get_item_tag_filter_tgt_statistic_enable_(self):
        return self._item_tag_filter_tgt_statistic_enable

    def _generate_item_tag_filter_tgt_args_(self, data_src):
        data_tgt = self._item_tag_filter_keys_tgt
        mode = self._item_tag_filter_mode
        if data_tgt:
            if mode == self.TagFilterMode.MatchAll:
                for i_key_tgt in data_tgt:
                    if i_key_tgt not in data_src:
                        return True, True
                return True, False
            elif mode == self.TagFilterMode.MatchOne:
                for i_key_tgt in data_tgt:
                    if i_key_tgt in data_src:
                        return True, False
                return True, True
            return True, False
        return False, False

    # semantic tag filter
    def _set_item_semantic_tag_filter_key_add_(self, key, value):
        self._item_semantic_tag_filter_keys_tgt.setdefault(
            key, set()
        ).add(value)

    def _update_item_semantic_tag_filter_keys_tgt_(self, data):
        self._item_semantic_tag_filter_keys_tgt.update(data)

    def _get_item_semantic_tag_filter_keys_tgt_(self):
        return self._item_semantic_tag_filter_keys_tgt

    def _generate_item_semantic_tag_filter_tgt_args_(self, data_src):
        data_tgt = self._item_semantic_tag_filter_keys_tgt
        mode = self._item_semantic_tag_filter_mode
        if data_tgt:
            if mode == self.TagFilterMode.MatchAll:
                for i_key, i_value_tgt in data_tgt.items():
                    if i_key in data_src:
                        v_src = data_src[i_key]
                        if not i_value_tgt.intersection(v_src):
                            return True, True
                return True, False
            elif mode == self.TagFilterMode.MatchOne:
                for i_key, i_value_tgt in data_tgt.items():
                    if i_key in data_src:
                        v_src = data_src[i_key]
                        if i_value_tgt.intersection(v_src):
                            return True, False
                return True, True
            return True, False
        # enable, hidden flag
        return False, False


class AbsQtViewFilterExtraDef(object):
    def _get_all_items_(self):
        raise NotImplementedError()

    def _init_view_filter_extra_def_(self, widget):
        self._widget = widget
        self._view_tag_filter_data_src = []
        self._view_semantic_tag_filter_data_src = {}
        self._view_keyword_filter_data_src = []
        self._view_keyword_filter_match_items = []
        #
        self._view_keyword_filter_bar = None
        #
        self._view_keyword_filter_occurrence_index_current = None

        self._view_keyword_filter_occurrence_dict = {}

    def _set_view_keyword_filter_bar_(self, widget):
        self._view_keyword_filter_bar = widget

    def _get_view_tag_filter_tgt_statistic_raw_(self):
        dic = {}
        items = self._get_all_items_()
        for i_item in items:
            enable = i_item._get_item_tag_filter_tgt_statistic_enable_()
            if enable is True:
                i_keys = i_item._get_item_tag_filter_keys_tgt_()
                for j_key in i_keys:
                    dic.setdefault(j_key, []).append(i_item)
        return dic

    def _set_view_tag_filter_data_src_(self, data_src):
        self._view_tag_filter_data_src = data_src

    def _get_view_tag_filter_data_src_(self):
        return self._view_tag_filter_data_src

    def _get_view_semantic_tag_filter_data_src_(self):
        return self._view_semantic_tag_filter_data_src

    def _set_view_semantic_tag_filter_data_src_(self, data_src):
        self._view_semantic_tag_filter_data_src = data_src

    def _set_view_keyword_filter_data_src_(self, data_src):
        self._view_keyword_filter_data_src = data_src

    def _refresh_view_items_visible_by_any_filter_(self):
        tag_filter_data_src = self._view_tag_filter_data_src
        semantic_tag_filter_data_src = self._view_semantic_tag_filter_data_src
        keyword_filter_data_src = self._view_keyword_filter_data_src
        self._view_keyword_filter_match_items = []
        #
        items = self._get_all_items_()
        for i_item in items:
            i_force_hidden_flag = i_item._get_force_hidden_flag_()
            if i_force_hidden_flag is True:
                i_is_hidden = True
            else:
                i_tag_filter_hidden_flag = False
                i_semantic_filter_hidden_flag = False
                i_keyword_filter_hidden_flag = False
                # tag filter
                if tag_filter_data_src:
                    i_is_enable, i_hidden_flag = i_item._generate_item_tag_filter_tgt_args_(tag_filter_data_src)
                    if i_is_enable is True:
                        i_tag_filter_hidden_flag = i_hidden_flag
                # semantic tag filter
                if semantic_tag_filter_data_src:
                    i_is_enable, i_hidden_flag = i_item._generate_item_semantic_tag_filter_tgt_args_(
                        semantic_tag_filter_data_src
                    )
                    if i_is_enable is True:
                        i_semantic_filter_hidden_flag = i_hidden_flag
                # keyword filter
                if keyword_filter_data_src:
                    i_is_enable, i_hidden_flag = i_item._generate_item_keyword_filter_tgt_args_(
                        keyword_filter_data_src
                    )
                    if i_is_enable is True:
                        i_keyword_filter_hidden_flag = i_hidden_flag
                        if i_keyword_filter_hidden_flag is False:
                            self._view_keyword_filter_match_items.append(i_item)
                # any hidden flag is True, hide this item
                if True in [i_tag_filter_hidden_flag, i_semantic_filter_hidden_flag, i_keyword_filter_hidden_flag]:
                    i_is_hidden = True
                else:
                    i_is_hidden = False
            #
            i_item._set_hidden_(i_is_hidden)
            # for tree
            for i in i_item._get_ancestors_():
                if i_is_hidden is False:
                    i._set_hidden_(False)
            #
            if self._view_keyword_filter_bar is not None:
                if self._view_keyword_filter_match_items:
                    self._view_keyword_filter_bar._set_filter_result_count_(
                        len(self._view_keyword_filter_match_items)
                    )
                else:
                    self._view_keyword_filter_bar._set_filter_result_count_(None)

    def _has_keyword_filter_results_(self):
        return self._view_keyword_filter_match_items != []

    def _register_keyword_filter_occurrence_(self, key, item):
        self._view_keyword_filter_occurrence_dict[key] = item

    def _do_keyword_filter_occurrence_(self, key):
        if key in self._view_keyword_filter_occurrence_dict:
            item_cur = self._view_keyword_filter_occurrence_dict[key]
            item_cur._set_selected_(True)
            self._widget._scroll_view_to_item_top_(item_cur)

    # noinspection PyUnusedLocal
    def _do_keyword_filter_occurrence_to_previous_(self):
        items = self._view_keyword_filter_match_items
        if items:
            idx_max, idx_min = len(items)-1, 0
            idx = self._view_keyword_filter_occurrence_index_current or 0
            #
            idx = max(min(idx, idx_max), 0)
            item_cur = items[idx]
            #
            if idx == idx_min:
                idx = idx_max
            else:
                idx -= 1
            idx_pre = max(min(idx, idx_max), 0)
            item_pre = items[idx_pre]
            self._widget._scroll_view_to_item_top_(item_pre)
            self._view_keyword_filter_occurrence_index_current = idx_pre
        else:
            self._view_keyword_filter_occurrence_index_current = None
        #
        if self._view_keyword_filter_bar is not None:
            self._view_keyword_filter_bar._set_filter_result_index_current_(
                self._view_keyword_filter_occurrence_index_current
            )

    # noinspection PyUnusedLocal
    def _do_keyword_filter_occurrence_to_next_(self):
        items = self._view_keyword_filter_match_items
        if items:
            idx_max, idx_min = len(items)-1, 0
            idx = self._view_keyword_filter_occurrence_index_current or 0
            #
            idx = max(min(idx, idx_max), 0)
            item_cur = items[idx]
            #
            if idx == idx_max:
                idx = idx_min
            else:
                idx += 1
            idx_nxt = max(min(idx, idx_max), 0)
            item_nxt = items[idx_nxt]
            self._widget._scroll_view_to_item_top_(item_nxt)
            self._view_keyword_filter_occurrence_index_current = idx_nxt
        else:
            self._view_keyword_filter_occurrence_index_current = None
        #
        if self._view_keyword_filter_bar is not None:
            self._view_keyword_filter_bar._set_filter_result_index_current_(
                self._view_keyword_filter_occurrence_index_current
            )


class AbsQtStateDef(object):
    ActionState = gui_core.GuiActionState

    def _set_state_def_init_(self):
        self._state = gui_core.GuiState.NORMAL
        self._state_draw_is_enable = False
        self._state_color = gui_qt_core.QtBrushes.Text

    # noinspection PyUnusedLocal
    def _set_state_(self, *args, **kwargs):
        self._state = args[0]

    # noinspection PyUnusedLocal
    def _get_state_(self, *args, **kwargs):
        return self._state

    def _get_state_color_(self):
        return self._state_color

    def _set_state_color_(self, color):
        self._state_color = color

    def _set_state_draw_enable_(self, boolean):
        self._state_draw_is_enable = boolean


class AbsQtDagDef(object):
    def _set_dag_def_init_(self):
        pass

    def _get_descendants_(self):
        return []

    def _get_ancestors_(self):
        return []


class AbsQtVisibleDef(object):
    def _init_visible_base_def_(self, widget):
        self._widget = widget

        self._force_visible_flag = False

    def _set_visible_(self, boolean):
        self._widget.setHidden(not boolean)

    def _get_is_visible_(self):
        return not self._widget.isHidden()

    def _set_hidden_(self, boolean, **kwargs):
        self._widget.setHidden(boolean)

    def _get_is_hidden_(self):
        return self._widget.isHidden()

    def _set_force_hidden_(self, boolean):
        self._force_visible_flag = boolean
        self._set_hidden_(boolean)

    def _get_force_hidden_flag_(self):
        return self._force_visible_flag


class AbsQtItemVisibleConnectionDef(object):
    def _get_item_is_hidden_(self):
        raise NotImplementedError()

    def _set_item_visible_connection_def_init_(self):
        self._item_visible_src_key = None
        self._item_visible_tgt_key = None
        #
        self._item_visible_tgt_view = None
        self._item_visible_tgt_raw = None

    def _set_item_visible_connect_to_(self, key, item_tgt):
        self._set_item_visible_src_key_(key)
        self._set_item_visible_tgt_view_(item_tgt._get_view_())
        #
        item_tgt._set_visible_tgt_key_(key)
        item_tgt._set_hidden_(self._get_item_is_hidden_())

    def _get_item_visible_src_key_(self):
        return self._item_visible_src_key

    def _set_item_visible_src_key_(self, key):
        self._item_visible_src_key = key

    def _get_item_visible_tgt_key_(self):
        return self._item_visible_tgt_key

    def _set_item_visible_tgt_key_(self, key):
        self._item_visible_tgt_key = key

    def _get_item_visible_tgt_view_(self):
        return self._item_visible_tgt_view

    def _set_item_visible_tgt_view_(self, view):
        self._item_visible_tgt_view = view

    def _get_item_visible_tgt_raw_(self):
        return self._item_visible_tgt_raw

    def _set_item_visible_tgt_raw_(self, raw):
        self._item_visible_tgt_raw = raw

    def _set_item_visible_connection_refresh_(self):
        src_item = self
        src_key = src_item._get_item_visible_src_key_()
        if src_key is not None:
            tgt_view = src_item._get_item_visible_tgt_view_()
            if tgt_view is not None:
                tgt_raw = tgt_view._get_view_visible_tgt_raw_()
                if src_key in tgt_raw:
                    items_tgt = tgt_raw[src_key]
                    for i_item_tgt in items_tgt:
                        i_item_tgt.set_hidden(self._get_item_is_hidden_())
                        i_item_tgt._set_item_show_start_auto_()


class AbsQtViewVisibleConnectionDef(object):
    def _get_all_items_(self):
        raise NotImplementedError()

    def _set_view_visible_connection_def_init_(self):
        self._view_visible_tgt_raw = []

    def _set_view_visible_tgt_raw_(self, raw):
        self._view_visible_tgt_raw = raw

    def _get_view_visible_tgt_raw_(self):
        return self._view_visible_tgt_raw

    def _set_view_visible_tgt_raw_clear_(self):
        self._set_view_visible_tgt_raw_({})

    def _set_view_visible_tgt_raw_update_(self):
        dic = {}
        items = self._get_all_items_()
        for i_item in items:
            i_tgt_key = i_item._get_item_visible_tgt_key_()
            if i_tgt_key is not None:
                dic.setdefault(
                    i_tgt_key, []
                ).append(i_item)
        #
        self._set_view_visible_tgt_raw_(dic)


class AbsQtViewStateDef(object):
    def _get_all_items_(self):
        raise NotImplementedError()

    def _set_view_state_def_init_(self):
        pass

    @staticmethod
    def _get_view_item_states_(items=None):
        if isinstance(items, (tuple, list)):
            lis = []
            for i_item in items:
                lis.append(i_item._get_state_())
            return lis
        return []

    @staticmethod
    def _get_view_item_state_colors_(items=None):
        if isinstance(items, (tuple, list)):
            lis = []
            for i_item in items:
                lis.append(i_item._get_state_color_())
            return lis
        return []


class AbsQtBuildBaseForItemDef(object):
    def _init_build_base_for_item_def_(self):
        pass

    def _get_view_(self):
        raise NotImplementedError()

    def _setup_item_show_runnable_stack_(self, view):
        self._build_runnable_stack = view._build_runnable_stack

    def _generate_item_show_runnable_(self, cache_fnc, build_fnc, post_fnc=None):
        return self._build_runnable_stack.generate_thread(
            cache_fnc, build_fnc, post_fnc
        )


# show base
# for item
class AbsQtShowBaseForItemDef(
    AbsQtBuildBaseForItemDef
):
    ShowStatus = gui_core.GuiShowStatus

    def _refresh_widget_all_(self, *args, **kwargs):
        raise NotImplementedError()

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _get_view_(self):
        raise NotImplementedError()

    def _get_item_widget_(self):
        raise NotImplementedError()

    def _init_show_base_for_item_def_(self, widget):
        self._widget = widget
        #
        if bsc_core.SysApplicationMtd.get_is_maya():
            self._item_show_use_thread = False
        else:
            self._item_show_use_thread = True
        #
        self._item_show_runnable = None
        self._item_show_image_runnable = None
        #
        self._item_show_cache_fnc = None
        self._item_show_build_fnc = None
        #
        self._item_show_status = self.ShowStatus.Unknown
        # image
        self._item_show_image_cache_fnc = None
        self._item_show_image_build_fnc = None
        #
        self._item_show_image_status = self.ShowStatus.Unknown

        self._init_build_base_for_item_def_()

        self._item_show_flag = False
        self._item_show_image_flag = False

    def _set_item_show_flag_(self, boolean):
        self._item_show_flag = boolean

    def _get_item_show_flag_(self):
        return self._item_show_flag

    def _setup_item_show_(self, view):
        self._setup_item_show_runnable_stack_(view)

        self._item_show_runnable = None
        self._item_show_image_runnable = None
        #
        self._item_show_timer = QtCore.QTimer(view)
        self._item_show_loading_index = 0
        self._item_show_loading_timer = QtCore.QTimer(view)
        self._item_show_loading_timer.timeout.connect(self._update_item_show_loading_)
        #
        self._item_show_image_timer = QtCore.QTimer(view)
        self._item_show_image_loading_index = 0
        self._item_show_image_loading_timer = QtCore.QTimer(view)
        self._item_show_image_loading_timer.timeout.connect(self._update_item_show_image_loading_)
        #
        self._item_show_image_sub_process = None
        self._item_show_image_cmd = None
        self._item_show_image_file_path = None

    def _set_item_show_build_fnc_(self, method):
        def cache_fnc_():
            return []

        # noinspection PyUnusedLocal
        def build_fnc_(data):
            method()

        if method is not None:
            self._set_item_show_fnc_(cache_fnc_, build_fnc_)

    # fnc
    def _set_item_show_fnc_(self, cache_fnc, build_fnc):
        if cache_fnc is not None and build_fnc is not None:
            if self._item_show_cache_fnc is None and self._item_show_build_fnc is None:
                self._item_show_cache_fnc = cache_fnc
                self._item_show_build_fnc = build_fnc
                self._item_show_status = self.ShowStatus.Waiting

                self._item_show_flag = True
                if self._get_item_is_viewport_showable_() is True:
                    self._checkout_item_show_()

    def _checkout_item_show_(self, delay_time=0):
        def run_fnc_():
            if self._item_show_cache_fnc is not None:
                self._start_item_show_()

        if self._item_show_flag is True:
            self._checkout_item_show_loading_()
            if delay_time > 0:
                self._item_show_timer.singleShot(delay_time, run_fnc_)
            else:
                run_fnc_()

    def _checkout_item_show_loading_(self):
        if self._item_show_status == self.ShowStatus.Waiting:
            self._item_show_loading_timer.start(100)

    def _start_item_show_(self):
        if self._item_show_flag is True:
            # update flag first
            self._item_show_flag = False
            self._item_show_status = self.ShowStatus.Loading
            if self._item_show_use_thread is True:
                self._item_show_runnable = self._generate_item_show_runnable_(
                    self._item_show_cache_fnc,
                    self._item_show_build_fnc,
                    self._finish_item_show_
                )
                self._item_show_runnable.set_start()
            else:
                self._item_show_build_fnc(
                    self._item_show_cache_fnc()
                )
                self._finish_item_show_()

    def _finish_item_show_(self):
        self._set_item_show_stop_(
            self.ShowStatus.Finished
        )

    def _set_item_show_stop_(self, status):
        self._item_show_status = status
        self._finish_item_show_loading_()

    def _get_item_show_is_finished_(self):
        return self._item_show_status in {
            self.ShowStatus.Completed, self.ShowStatus.Failed
        }

    # loading
    def _update_item_show_loading_(self):
        self._item_show_loading_index += 1
        # noinspection PyBroadException
        try:
            self._refresh_widget_draw_()
        except Exception:
            pass

    def _finish_item_show_loading_(self):
        # noinspection PyBroadException
        try:
            self._item_show_loading_timer.stop()
            self._refresh_widget_draw_()
        except Exception:
            pass

    # image fnc
    def _set_item_show_image_cmd_(self, image_file_path, cmd):
        def cache_fnc_():
            # noinspection PyBroadException
            try:
                bsc_core.PrcBaseMtd.execute_with_result(
                    cmd
                )
            except Exception:
                pass
            return []

        # noinspection PyUnusedLocal
        def build_fnc_(data):
            pass

        if cmd is not None:
            self._item_show_image_file_path = image_file_path
            self._set_item_show_image_fnc_(cache_fnc_, build_fnc_)

    def _set_item_show_image_fnc_(self, cache_fnc, build_fnc):
        if cache_fnc is not None and build_fnc is not None:
            if self._item_show_image_cache_fnc is None and self._item_show_image_build_fnc is None:
                self._item_show_image_cache_fnc = cache_fnc
                self._item_show_image_build_fnc = build_fnc

                self._item_show_image_flag = True

                self._item_show_image_status = self.ShowStatus.Waiting
                if self._get_item_is_viewport_showable_() is True:
                    self._checkout_item_show_image_()

    def _checkout_item_show_image_(self, delay_time=0):
        def run_fnc():
            if self._item_show_image_cache_fnc is not None:
                self._start_item_show_image_()

        if self._item_show_image_flag is True:
            self._checkout_item_show_image_loading_()
            if delay_time > 0:
                self._item_show_image_timer.singleShot(delay_time, run_fnc)
            else:
                run_fnc()

    def _checkout_item_show_image_loading_(self):
        if self._item_show_image_status == self.ShowStatus.Waiting:
            self._item_show_image_loading_timer.start(100)

    def _start_item_show_image_(self):
        if self._item_show_image_flag is True:
            self._item_show_image_status = self.ShowStatus.Loading
            self._item_show_image_flag = False
            if self._item_show_use_thread is True:
                self._item_show_image_runnable = self._generate_item_show_runnable_(
                    self._item_show_image_cache_fnc,
                    self._item_show_image_build_fnc,
                    self._finish_item_show_image_
                )
                self._item_show_image_runnable.set_start()
            else:
                self._item_show_image_build_fnc(
                    self._item_show_image_cache_fnc()
                )
                self._finish_item_show_image_()

    def _finish_item_show_image_(self):
        if self._item_show_image_file_path is not None:
            if os.path.isfile(self._item_show_image_file_path) is True:
                self._set_item_show_image_stop_(self.ShowStatus.Completed)
            else:
                self._set_item_show_image_stop_(self.ShowStatus.Failed)

    def _set_item_show_image_stop_(self, status):
        self._item_show_image_status = status
        if status == self.ShowStatus.Failed:
            item_widget = self._get_item_widget_()
            if item_widget is not None:
                item_widget._set_image_file_path_(
                    gui_core.GuiIcon.get('image_loading_failed_error')
                )
        #
        self._finish_item_show_image_loading_()

    def _get_item_is_viewport_showable_(self, *args, **kwargs):
        raise NotImplementedError()

    def _update_item_show_image_loading_(self):
        self._item_show_image_loading_index += 1
        # noinspection PyBroadException
        try:
            self._refresh_widget_all_()
        except Exception:
            pass

    def _finish_item_show_image_loading_(self):
        # noinspection PyBroadException
        try:
            self._item_show_image_loading_timer.stop()
            self._refresh_widget_all_()
        except Exception:
            pass

    def _checkout_item_show_all_(self):
        self._checkout_item_show_()
        self._checkout_item_show_image_()

    def _stop_item_show_all_(self):
        self._set_item_show_stop_(self.ShowStatus.Stopped)
        self._set_item_show_image_stop_(self.ShowStatus.Stopped)

    def _kill_item_all_show_runnables_(self):
        if self._item_show_runnable is not None:
            self._item_show_runnable.do_kill()
        #
        if self._item_show_image_runnable is not None:
            self._item_show_image_runnable.do_kill()

    def _set_item_viewport_visible_(self, boolean):
        if boolean is True:
            self._checkout_item_show_all_()
        #
        self._set_item_widget_visible_(boolean)

    def _set_item_widget_visible_(self, boolean):
        raise NotImplementedError()

    def _set_viewport_show_enable_(self, boolean):
        self._is_viewport_show_enable = boolean

    def _set_item_show_start_auto_(self):
        if self._get_item_is_viewport_showable_() is True:
            self._checkout_item_show_all_()


# for view
class AbsQtShowForViewDef(object):
    def _get_all_items_(self):
        raise NotImplementedError()

    def _init_show_for_view_def_(self, widget):
        self._widget = widget

    def _get_view_item_viewport_showable_(self, item):
        i_rect = self._widget.visualItemRect(item)
        i_w, i_h = i_rect.width(), i_rect.height()
        # check is visible
        if i_w != 0 and i_h != 0:
            viewport_rect = self._widget.rect()
            v_t, v_b = viewport_rect.top(), viewport_rect.bottom()
            i_t, i_b = i_rect.top(), i_rect.bottom()
            if v_b >= i_t and i_b >= v_t:
                return True
        return False

    def _refresh_view_all_items_viewport_showable_(self, includes=None):
        if isinstance(includes, (tuple, list)):
            items_ = includes
        else:
            items_ = self._widget._get_all_items_()
        #
        for i_item in items_:
            if i_item.isHidden() is False:
                if self._get_view_item_viewport_showable_(i_item) is True:
                    i_item._set_item_viewport_visible_(True)

        self._widget.update()

    def _refresh_viewport_showable_auto_(self):
        self._refresh_view_all_items_viewport_showable_(
            self._get_all_show_items_()
        )

    def _refresh_viewport_showable_by_scroll_(self):
        self._refresh_viewport_showable_auto_()

    def _get_all_show_items_(self):
        return [i for i in self._get_all_items_() if i._get_item_show_flag_() is True]


class ShowFnc(object):
    def __init__(self):
        pass


class AbsQtShowStackForItemDef(object):
    def _init_show_stack_for_item_(self):
        pass


class AbsQtDrawGridDef(object):
    def _set_draw_grid_def_init_(self, widget):
        self._widget = widget
        #
        self._grid_border_color = 71, 71, 71, 255
        self._grid_mark_border_color = 191, 191, 191, 255
        self._grid_axis_border_color_x, self._grid_axis_border_color_y = (255, 0, 63, 255), (63, 255, 127, 255)
        #
        self._grid_value_show_mode = 1
        #
        self._grid_width, self._grid_height = 20, 20
        #
        self._grid_offset_x, self._grid_offset_y = 0, 0
        self._grid_scale_x, self._grid_scale_y = 1, 1
        #
        self._grid_value_offset_x, self._grid_value_offset_y = 0, 0

        self._grid_dir_x, self._grid_dir_y = 1, 1

        self._grid_axis_lock_x, self._grid_axis_lock_y = 0, 0

    def _refresh_widget_draw_(self):
        raise NotImplementedError()


# delete
class AbsQtDeleteBaseDef(object):
    delete_text_accepted = qt_signal(str)

    def _init_delete_base_def_(self, widget):
        self._widget = widget
        #
        self._delete_is_enable = False
        self._delete_action_is_enable = False
        #
        self._delete_draw_is_enable = False
        self._delete_action_rect = QtCore.QRect()
        self._delete_icon_draw_rect = QtCore.QRect()
        #
        self._delete_icon_file_draw_size = 12, 12
        self._delete_is_pressed = False
        self._delete_is_hovered = False
        self._delete_icon_file_path = gui_core.GuiIcon.get('delete')

    def _set_delete_enable_(self, boolean):
        self._delete_is_enable = boolean
        self._delete_action_is_enable = boolean
        self._delete_draw_is_enable = boolean

    def _set_delete_rect_(self, x, y, w, h):
        self._delete_action_rect.setRect(
            x, y, w, h
        )

    def _set_delete_draw_rect_(self, x, y, w, h):
        self._delete_icon_draw_rect.setRect(
            x, y, w, h
        )

    def _get_action_delete_is_valid_(self, event):
        if self._delete_action_is_enable is True:
            p = event.pos()
            return self._delete_action_rect.contains(p)
        return False


class AbsQtHelpBaseDef(object):
    def _init_help_base_def_(self, widget):
        self._widget = widget

        self._help_text_is_enable = False
        #
        self._help_text_draw_size = 480, 240
        self._help_frame_draw_rect = QtCore.QRect()
        self._help_draw_rect = QtCore.QRect()
        self._help_text = ''

    def _set_help_text_(self, text):
        self._help_text = text


class AbsQtScreenshotBaseDef(AbsQtHelpBaseDef):
    class Mode(enum.IntEnum):
        Started = 0
        New = 1
        Edit = 2
        Stopped = 3

    RectRegion = gui_core.GuiRectRegion

    CURSOR_MAPPER = {
        RectRegion.Unknown: QtCore.Qt.ArrowCursor,
        RectRegion.Top: QtCore.Qt.SizeVerCursor,
        RectRegion.Bottom: QtCore.Qt.SizeVerCursor,
        RectRegion.Left: QtCore.Qt.SizeHorCursor,
        RectRegion.Right: QtCore.Qt.SizeHorCursor,
        RectRegion.TopLeft: QtCore.Qt.SizeFDiagCursor,
        RectRegion.TopRight: QtCore.Qt.SizeBDiagCursor,
        RectRegion.BottomLeft: QtCore.Qt.SizeBDiagCursor,
        RectRegion.BottomRight: QtCore.Qt.SizeFDiagCursor,
        RectRegion.Inside: QtCore.Qt.SizeAllCursor,
    }

    screenshot_started = qt_signal()
    screenshot_finished = qt_signal()
    screenshot_accepted = qt_signal(list)
    CACHE = 0, 0, 0, 0

    def _init_screenshot_base_def_(self, widget):
        self._widget = widget
        self._init_help_base_def_(widget)

        self._screenshot_mode = self.Mode.Started
        self._screenshot_is_modify = False

        self._screenshot_file_path = None

        self._screenshot_rect = QtCore.QRect()

        self._screenshot_is_activated = False
        #
        self._screenshot_point_start = QtCore.QPoint()
        #
        self._screenshot_rect_point_start = QtCore.QPoint()
        self._screenshot_rect_point_start_offset = [0, 0]
        self._screenshot_rect_point_start_offset_temp = [0, 0]
        self._screenshot_rect_point_end = QtCore.QPoint()
        self._screenshot_rect_point_end_offset = [0, 0]
        self._screenshot_rect_point_end_offset_temp = [0, 0]

        self._screenshot_rect_region_edit = self.RectRegion.Unknown

        self._screenshot_modify_gap = 8

    def _do_screenshot_press_(self, event):
        self._screenshot_point_start = event.pos()
        if self._screenshot_mode == self.Mode.Started:
            self._screenshot_mode = self.Mode.New

        self._widget.update()

    def _do_screenshot_press_move_(self, event):
        p = event.pos()
        if self._screenshot_mode == self.Mode.New:
            self._screenshot_rect_point_start.setX(self._screenshot_point_start.x())
            self._screenshot_rect_point_start.setY(self._screenshot_point_start.y())
            self._screenshot_rect_point_end = event.pos()
        elif self._screenshot_mode == self.Mode.Edit:
            d_p = p-self._screenshot_point_start
            d_p_x, d_p_y = d_p.x(), d_p.y()
            o_x_0, o_y_0 = self._screenshot_rect_point_start_offset_temp
            o_x_1, o_y_1 = self._screenshot_rect_point_end_offset_temp
            if self._screenshot_rect_region_edit == self.RectRegion.Inside:
                self._screenshot_rect_point_start_offset[0] = o_x_0+d_p_x
                self._screenshot_rect_point_start_offset[1] = o_y_0+d_p_y
                self._screenshot_rect_point_end_offset[0] = o_x_1+d_p_x
                self._screenshot_rect_point_end_offset[1] = o_y_1+d_p_y
            elif self._screenshot_rect_region_edit == self.RectRegion.Top:
                self._screenshot_rect_point_start_offset[1] = o_y_0+d_p_y
            elif self._screenshot_rect_region_edit == self.RectRegion.Bottom:
                self._screenshot_rect_point_end_offset[1] = o_y_1+d_p_y
            elif self._screenshot_rect_region_edit == self.RectRegion.Left:
                self._screenshot_rect_point_start_offset[0] = o_x_0+d_p_x
            elif self._screenshot_rect_region_edit == self.RectRegion.Right:
                self._screenshot_rect_point_end_offset[0] = o_x_1+d_p_x
            elif self._screenshot_rect_region_edit == self.RectRegion.TopLeft:
                self._screenshot_rect_point_start_offset[0] = o_x_0+d_p_x
                self._screenshot_rect_point_start_offset[1] = o_y_0+d_p_y
            elif self._screenshot_rect_region_edit == self.RectRegion.TopRight:
                self._screenshot_rect_point_start_offset[1] = o_y_0+d_p_y
                self._screenshot_rect_point_end_offset[0] = o_x_1+d_p_x
            elif self._screenshot_rect_region_edit == self.RectRegion.BottomLeft:
                self._screenshot_rect_point_start_offset[0] = o_x_0+d_p_x
                self._screenshot_rect_point_end_offset[1] = o_y_1+d_p_y
            elif self._screenshot_rect_region_edit == self.RectRegion.BottomRight:
                self._screenshot_rect_point_end_offset[0] = o_x_1+d_p_x
                self._screenshot_rect_point_end_offset[1] = o_y_1+d_p_y

        self._update_screenshot_geometry_()
        self._widget.update()

    def _do_screenshot_hover_(self, event):
        if self._screenshot_mode == self.Mode.Edit:
            pos = event.pos()

            x, y = self._screenshot_rect.x(), self._screenshot_rect.y()
            w, h = self._screenshot_rect.width(), self._screenshot_rect.height()

            m_x, m_y = pos.x(), pos.y()

            self._screenshot_rect_region_edit = self._get_rect_region_(
                m_x, m_y, x, y, w, h, 8
            )
            cursor = self.CURSOR_MAPPER[self._screenshot_rect_region_edit]

            self._widget.setCursor(QtGui.QCursor(cursor))

    # noinspection PyUnusedLocal
    def _do_screenshot_press_release_(self, event):
        if self._screenshot_mode == self.Mode.New:
            if self._screenshot_rect_point_start != self._screenshot_rect_point_end:
                self._screenshot_mode = self.Mode.Edit
        elif self._screenshot_mode == self.Mode.Edit:
            self._screenshot_rect_point_start_offset_temp[0] = self._screenshot_rect_point_start_offset[0]
            self._screenshot_rect_point_start_offset_temp[1] = self._screenshot_rect_point_start_offset[1]
            self._screenshot_rect_point_end_offset_temp[0] = self._screenshot_rect_point_end_offset[0]
            self._screenshot_rect_point_end_offset_temp[1] = self._screenshot_rect_point_end_offset[1]

        self._widget.update()

    def _update_screenshot_geometry_(self):
        x, y = 0, 0
        w, h = self._widget.width(), self._widget.height()

        x_0, y_0 = self._screenshot_rect_point_start.x(), self._screenshot_rect_point_start.y()
        x_1, y_1 = self._screenshot_rect_point_end.x(), self._screenshot_rect_point_end.y()

        o_x_0, o_y_0 = self._screenshot_rect_point_start_offset
        o_x_1, o_y_1 = self._screenshot_rect_point_end_offset

        x_0 += o_x_0
        y_0 += o_y_0
        x_1 += o_x_1
        y_1 += o_y_1

        s_x, s_y = min(x_0, x_1), min(y_0, y_1)
        s_w, s_h = abs(x_1-x_0), abs(y_1-y_0)

        self._screenshot_rect.setRect(
            s_x, s_y, s_w, s_h
        )

        t_w, t_h = self._help_text_draw_size

        t_t_w, t_t_h = t_w-48, t_h-48

        self._help_frame_draw_rect.setRect(
            x+(w-t_w)/2, y+(h-t_h)/2, t_w, t_h
        )
        self._help_draw_rect.setRect(
            x+(w-t_t_w)/2, y+(h-t_t_h)/2, t_t_w, t_t_h
        )

    def _cancel_screenshot_(self):
        self.screenshot_finished.emit()
        self._widget.close()
        self._widget.deleteLater()

    def _accept_screenshot_(self):
        def fnc_():
            x, y, w, h = self._get_screenshot_accept_geometry_args_()
            self.screenshot_finished.emit()
            self.screenshot_accepted.emit([x, y, w, h])
            self._widget.close()
            self._widget.deleteLater()

        self._screenshot_mode = self.Mode.Stopped
        self._widget.update()

        AbsQtScreenshotBaseDef.CACHE = self._get_screenshot_accept_geometry_args_()

        self._timer = QtCore.QTimer(self._widget)
        self._timer.singleShot(100, fnc_)

    def _start_screenshot_(self):
        self.screenshot_started.emit()
        self._widget.setGeometry(
            QtWidgets.QApplication.desktop().rect()
        )
        self._widget.show()
        self._widget.setCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )

    @classmethod
    def _get_rect_region_(cls, m_x, m_y, x, y, w, h, gap):
        # top
        if x+gap < m_x < x+w-gap and y-gap < m_y < y+gap:
            return cls.RectRegion.Top
        # bottom
        elif x+gap < m_x < x+w-gap and y+h-gap < m_y < y+h+gap:
            return cls.RectRegion.Bottom
        # left
        elif x-gap < m_x < x+gap and y+gap < m_y < y+h-gap:
            return cls.RectRegion.Left
        # right
        elif x+w-gap < m_x < x+w+gap and y+gap < m_y < y+h-gap:
            return cls.RectRegion.Right
        # top left
        elif x-gap < m_x < x+gap and y-gap < m_y < y+gap:
            return cls.RectRegion.TopLeft
        # top right
        elif x+w-gap <= m_x <= x+w+gap and y-gap <= m_y <= y+gap:
            return cls.RectRegion.TopRight
        # bottom left
        elif x-gap < m_x < x+gap and y+h-gap < m_y < y+h+gap:
            return cls.RectRegion.BottomLeft
        # bottom right
        elif x+w-gap < m_x < x+w+gap and y+h-gap < m_y < y+h+gap:
            return cls.RectRegion.BottomRight
        # inside
        elif x+gap < m_x < x+w-gap and y+gap < m_y < y+h-gap:
            return cls.RectRegion.Inside
        else:
            return cls.RectRegion.Unknown

    def _get_screenshot_accept_geometry_args_(self):
        x, y = self._widget.x(), self._widget.y()

        rect_0 = self._screenshot_rect
        x_0, y_0, w_0, h_0 = rect_0.x(), rect_0.y(), rect_0.width(), rect_0.height()
        return x+x_0, y+y_0, w_0, h_0

    @classmethod
    def _save_screenshot_to_(cls, geometry, file_path):
        bsc_storage.StgFileOpt(file_path).create_directory()
        rect = QtCore.QRect(*geometry)

        if bsc_core.SysApplicationMtd.get_is_maya():
            main_window = gui_qt_core.GuiQtMaya.get_qt_main_window()
            s = QtGui.QPixmap.grabWindow(
                long(main_window.winId())
            )
            s.copy(rect).save(file_path)
        else:
            app_ = QtWidgets.QApplication

            s = app_.primaryScreen().grabWindow(
                app_.desktop().winId()
            )
            s.copy(rect).save(file_path)


class AbsQtItemDagLoading(object):
    def _set_item_dag_loading_def_init_(self, widget):
        self._widget = widget

        self._loading_item = None

    def _set_item_dag_loading_start_(self):
        self._loading_item = self._widget._set_child_add_()
        self._loading_item.setText(0, 'loading ...')

    def _set_item_dag_loading_end_(self):
        if self._loading_item is not None:
            self._loading_item._kill_item_all_show_runnables_()
            self._loading_item._stop_item_show_all_()
            self._widget.takeChild(
                self._widget.indexOfChild(self._loading_item)
            )
            self._loading_item = None
