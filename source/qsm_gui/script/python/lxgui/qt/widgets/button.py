# coding=utf-8
import os

import lxbasic.core as bsc_core
# gui
from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from ...qt import abstracts as _qt_abstracts
# qt widgets
from . import utility as _utility

from . import drag as _drag


class QtCheckButton(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtFrameBaseDef,
    _qt_abstracts.AbsQtIconBaseDef,
    _qt_abstracts.AbsQtNameBaseDef,
    #
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForCheckDef,
    #
    _qt_abstracts.AbsQtValueDefaultExtraDef,
    _qt_abstracts.AbsQtValueHistoryExtraDef
):
    def _refresh_widget_all_(self):
        pass

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        spacing = 2
        icn_frm_w, icn_frm_h = self._icon_frame_draw_size
        icn_w, icn_h = self._icon_draw_size
        #
        self._set_frame_draw_rect_(
            x, y, w-1, h-1
        )
        self._set_check_action_rect_(
            x, y, icn_frm_w, icn_frm_h
        )
        #
        self._set_check_icon_draw_rect_(
            x+(icn_frm_w-icn_w)/2, y+(icn_frm_h-icn_h)/2, icn_w, icn_h
        )
        x += icn_frm_w+spacing
        self._set_name_draw_rect_(
            x, y, w-x, h
        )

    def __init__(self, *args, **kwargs):
        super(QtCheckButton, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        qt_palette = _qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)
        self.setFont(_qt_core.QtFonts.NameNormal)
        #
        self.setMaximumHeight(20)
        self.setMinimumHeight(20)
        #
        self.installEventFilter(self)
        #
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._init_frame_base_def_(self)
        self._init_icon_base_def_(self)
        self._init_name_base_def_(self)
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_check_def_(self)
        self._set_check_enable_(True)
        #
        self._init_value_default_extra_def_(self)
        self._init_value_history_base_def_(self)
        #
        self._refresh_check_()
        #
        self._set_name_draw_font_(_qt_core.QtFonts.Button)

        self.user_check_toggled.connect(self._push_history_)

    def _get_value_is_valid_(self, value):
        if isinstance(value, bool):
            return True
        return False

    def _pull_history_(self, value):
        self._set_checked_(value)

    def _get_value_(self):
        return self._is_checked_()

    def _set_value_(self, value):
        self._set_checked_(value)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            #
            if event.type() in {QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonDblClick}:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.CheckPress)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_() == self.ActionFlag.CheckPress:
                        self._swap_user_check_action_()
                    #
                    self.user_check_clicked.emit()
                    #
                    self._clear_all_action_flags_()
            # elif event.type() == QtCore.QEvent.ToolTip:
            #     pos = event.globalPos()
            #     QtWidgets.QToolTip.showText(
            #         pos, self._tool_tip_text, self, QtCore.QRect(pos.x(), pos.y(), 480, 160)
            #     )
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        #
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        #
        if self._check_is_enable is True:
            if self._check_icon_file_path_current is not None:
                painter._draw_icon_file_by_rect_(
                    rect=self._check_icon_draw_rect,
                    file_path=self._check_icon_file_path_current,
                    offset=offset,
                    is_hovered=self._is_hovered
                )
        #
        if self._name_text is not None:
            name_text = self._name_text
            if self._action_is_enable is True:
                text_color = [_qt_core.QtRgba.Text, _qt_core.QtRgba.TextHover][self._is_hovered]
            else:
                text_color = _qt_core.QtRgba.TxtDisable
            #
            painter._draw_text_by_rect_(
                rect=self._name_draw_rect,
                text=name_text,
                font=self._name_draw_font,
                text_color=text_color,
                text_option=QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter,
                offset=offset
            )


class QtPressButton(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtFrameBaseDef,
    _qt_abstracts.AbsQtVisibleDef,
    _qt_abstracts.AbsQtStatusBaseDef,
    #
    _qt_abstracts.AbsQtSubProcessBaseDef,
    _qt_abstracts.AbsQtValidatorBaseDef,
    #
    _qt_abstracts.AbsQtIconBaseDef,
    _qt_abstracts.AbsQtMenuBaseDef,
    _qt_abstracts.AbsQtNameBaseDef,
    _qt_abstracts.AbsQtProgressBaseDef,
    #
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForPressDef,
    _qt_abstracts.AbsQtActionForCheckDef,
    _qt_abstracts.AbsQtActionForOptionPressDef,
    #
    _qt_abstracts.AbsQtItemLayoutBaseDef,
):
    def _refresh_widget_all_(self):
        pass

    clicked = qt_signal()
    checked = qt_signal()
    toggled = qt_signal(bool)
    option_clicked = qt_signal()
    #
    status_changed = qt_signal(int)
    #
    rate_status_update_at = qt_signal(int, int)
    rate_finished_at = qt_signal(int, int)
    rate_finished = qt_signal()
    #
    QT_MENU_CLS = _utility.QtMenu

    def __init__(self, *args, **kwargs):
        super(QtPressButton, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        qt_palette = _qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)
        self.setFont(_qt_core.QtFonts.NameNormal)

        self.setMaximumHeight(20)
        self.setMinimumHeight(20)

        self.installEventFilter(self)

        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self._init_frame_base_def_(self)
        self._init_visible_base_def_(self)
        self._init_status_base_def_(self)
        self._init_sub_process_base_def_()
        self._init_validator_base_def_(self)

        self._init_icon_base_def_(self)
        self._init_name_base_def_(self)
        self._init_menu_base_def_(self)
        self._init_progress_base_def_()

        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)
        self._init_action_for_check_def_(self)
        self._init_action_for_option_press_def_(self)

        self._init_item_layout_base_def_(self)

        self._refresh_check_()

        self._set_name_draw_font_(_qt_core.QtFonts.Button)

        r, g, b = 167, 167, 167
        h, s, v = bsc_core.BscColor.rgb_to_hsv(r, g, b)
        color = bsc_core.BscColor.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b

        self._frame_border_color = color
        self._hovered_frame_border_color = hover_color

        r, g, b = 151, 151, 151
        h, s, v = bsc_core.BscColor.rgb_to_hsv(r, g, b)
        color = bsc_core.BscColor.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        self._frame_background_color = color
        self._hovered_frame_background_color = hover_color

        self.status_changed.connect(
            self._set_status_
        )
        self.rate_status_update_at.connect(
            self._set_sub_process_status_at_
        )
        self.rate_finished_at.connect(
            self._finish_sub_process_at_
        )

        self._sub_process_timer = QtCore.QTimer(self)

        # noinspection PyUnresolvedReferences
        self._sub_process_timer.timeout.connect(
            self._refresh_sub_process_draw_
        )

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()

        check_enable = self._get_check_action_is_enable_()
        # noinspection PyUnusedLocal
        option_click_enable = self._get_option_click_is_enable_()
        status_is_enable = self._get_status_is_enable_()
        sub_process_is_enable = self._get_sub_process_is_enable_()
        validator_is_enable = self._get_validator_is_enable_()
        progress_enable = self._get_progress_is_enable_()

        icn_frm_w, icn_frm_h = self._icon_frame_draw_size

        i_f_w, i_f_h = self._icon_draw_size
        i_c_w, i_c_h = self._icon_color_draw_size
        i_n_w, i_n_h = self._icon_name_draw_size

        c_x, c_y = x, y
        c_w, c_h = w, h

        c_icn_x, c_icn_y = x, y
        c_name_w, c_name_h = w, h

        if check_enable is True:
            self._check_frame_rect.setRect(
                c_icn_x, c_icn_y, icn_frm_w, icn_frm_h
            )
            self._check_icon_draw_rect.setRect(
                c_icn_x+(icn_frm_w-i_f_w)/2, c_icn_y+(icn_frm_h-i_f_h)/2, i_f_w, i_f_h
            )
            c_icn_x += icn_frm_h
            c_name_w -= icn_frm_w
            c_x += icn_frm_h
            c_w -= icn_frm_w

        if self._file_icon_flag is True:
            self._icon_draw_rect.setRect(
                c_icn_x+(icn_frm_w-i_f_w)/2, c_icn_y+(icn_frm_h-i_f_h)/2, i_f_w, i_f_h
            )
            self._icon_color_draw_rect.setRect(
                c_icn_x+(icn_frm_w-i_c_w)/2, c_icn_y+(icn_frm_h-i_c_h)/2, i_c_w, i_c_h
            )
            self._icon_text_draw_rect.setRect(
                c_icn_x+(icn_frm_w-i_n_w)/2, c_icn_y+(icn_frm_h-i_n_h)/2, i_n_w, i_n_h
            )
            c_icn_x += icn_frm_h
            c_name_w -= icn_frm_w

        # option
        if self._get_option_click_is_enable_() is True:
            self._option_rect.setRect(
                w-icn_frm_w, y, icn_frm_w, icn_frm_h
            )
            self._option_icon_draw_rect.setRect(
                (w-icn_frm_w)+(icn_frm_w-i_f_w)/2, y+(icn_frm_h-i_f_h)/2, i_f_w, i_f_h
            )
            c_name_w -= icn_frm_w
            c_w -= icn_frm_w
        
        # menu
        elif self._menu_flag is True:
            self._menu_rect.setRect(
                w-icn_frm_w, y, icn_frm_w, icn_frm_h
            )
            self._menu_icon_draw_rect.setRect(
                (w-icn_frm_w)+(icn_frm_w-i_f_w)/2, y+(icn_frm_h-i_f_h)/2, i_f_w, i_f_h
            )
            c_name_w -= icn_frm_w
            c_w -= icn_frm_w
        #
        self._frame_draw_rect.setRect(
            c_x, c_y, c_w, c_h
        )
        self._status_rect.setRect(
            c_x, c_y, c_w, c_h
        )
        self._name_draw_rect.setRect(
            c_icn_x, c_icn_y, c_name_w, c_name_h
        )
        self._sub_name_draw_rect.setRect(
            c_icn_x, c_icn_y, c_name_w-8, c_name_h
        )
        # progress
        if progress_enable is True:
            progress_percent = self._get_progress_percent_()
            self._progress_rect.setRect(
                c_x, c_y, c_w*progress_percent, 4
            )
        #
        if status_is_enable is True:
            self._status_rect.setRect(
                c_x, c_y, c_w, c_h
            )
        #
        e_h = 2
        if sub_process_is_enable is True:
            self._sub_process_status_rect.setRect(
                c_x, c_h-e_h, c_w, e_h
            )
        #
        if validator_is_enable is True:
            self._validator_status_rect.setRect(
                c_x, c_h-e_h, c_w, e_h
            )

    def _initialization_sub_process_(self, count, status):
        super(QtPressButton, self)._initialization_sub_process_(count, status)
        if count > 0:
            self._set_status_(
                self.Status.Running
            )
            self._sub_process_timer.start(100)

    def _finish_sub_process_at_(self, index, status):
        super(QtPressButton, self)._finish_sub_process_at_(index, status)
        # check is finished
        if self._get_sub_process_is_finished_() is True:
            if self.Status.Failed in self._sub_process_statuses:
                self._set_status_(
                    self.Status.Failed
                )
            else:
                self._set_status_(
                    self.Status.Completed
                )
            self._sub_process_is_started = False
            # when finish send emit
            self.rate_finished.emit()

            self._sub_process_timer.stop()

        self._refresh_widget_draw_()

    def _connect_sub_process_finished_to_(self, fnc):
        self.rate_finished.connect(fnc)

    def _restore_sub_process_(self):
        super(QtPressButton, self)._restore_sub_process_()

        self._set_status_(
            self.Status.Stopped
        )

    def _execute_(self):
        self.press_clicked.emit()

    # noinspection PyPep8Naming
    def setText(self, text):
        self._name_text = text

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            # update rect first
            action_enable = self._get_action_is_enable_()

            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.Show:
                self._refresh_widget_draw_geometry_()
                self._refresh_widget_draw_()
            #
            if action_enable is True:
                if event.type() == QtCore.QEvent.Enter:
                    self._is_hovered = True
                    self.update()
                elif event.type() == QtCore.QEvent.Leave:
                    self._is_hovered = False
                    self.update()
                # press
                elif event.type() in {QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonDblClick}:
                    self._action_flag = None

                    check_enable = self._get_check_action_is_enable_()
                    click_enable = self._get_action_press_is_enable_()
                    option_enable = self._get_option_click_is_enable_()
                    menu_enable = self._menu_flag

                    flag_raw = [
                        (check_enable, self._check_frame_rect, self.ActionFlag.CheckPress),
                        (click_enable, self._frame_draw_rect, self.ActionFlag.Press),
                        (option_enable, self._option_rect, self.ActionFlag.OptionPress),
                        (menu_enable, self._menu_rect, self.ActionFlag.MenuPress),
                    ]
                    if event.button() == QtCore.Qt.LeftButton:
                        pos = event.pos()
                        for i_enable, i_rect, i_flag in flag_raw:
                            if i_enable is True:
                                if i_rect.contains(pos) is True:
                                    self._action_flag = i_flag
                                    break
                    elif event.button() == QtCore.Qt.RightButton:
                        self._popup_menu_()
                    #
                    self._is_hovered = True
                    self.update()
                elif event.type() == QtCore.QEvent.MouseButtonRelease:
                    if self._action_flag == self.ActionFlag.CheckPress:
                        self._swap_check_()
                        self.checked.emit()
                        self.press_clicked.emit()
                    elif self._action_flag == self.ActionFlag.Press:
                        self.clicked.emit()
                        self.press_clicked.emit()
                    elif self._action_flag == self.ActionFlag.OptionPress:
                        self.option_clicked.emit()
                    elif self._action_flag == self.ActionFlag.MenuPress:
                        self._popup_menu_()
                    #
                    self._action_flag = None
                    self.update()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        #
        if self._action_is_enable is True:
            bdr_color = [_qt_core.QtRgba.BdrButton, _qt_core.QtRgba.BdrButtonHover][self._is_hovered]
            bkg_color = [_qt_core.QtRgba.BkgButton, _qt_core.QtRgba.BkgButtonHover][self._is_hovered]
        else:
            bdr_color = _qt_core.QtRgba.BdrButtonDisable
            bkg_color = _qt_core.QtRgba.BkgButtonDisable

        painter._draw_frame_by_rect_(
            rect=self._frame_draw_rect,
            border_color=bdr_color,
            background_color=bkg_color,
            border_radius=4,
            offset=offset
        )
        # status
        if self._get_status_is_enable_() is True and self._get_sub_process_is_enable_() is False:
            bkg_color_ = [self._status_background_color, self._hover_status_background_color][self._is_hovered]
            bdr_color_ = [self._status_border_color, self._hover_status_border_color][self._is_hovered]
            painter._draw_frame_by_rect_(
                rect=self._frame_draw_rect,
                border_color=bdr_color_,
                background_color=bkg_color_,
                border_radius=4,
                offset=offset
            )
        # sub process
        if self._get_sub_process_is_enable_() is True:
            status_rgba = [
                self._status_background_color, self._hover_status_background_color
            ][self._is_hovered]
            sub_status_rgba_array = [
                self._sub_process_status_colors, self._hover_sub_process_status_colors
            ][self._is_hovered]
            #
            r, g, b, a = status_rgba
            painter._draw_alternating_colors_by_rect_(
                rect=self._frame_draw_rect,
                colors=((r, g, b, 127), (0, 0, 0, 0)),
                offset=offset,
                border_radius=4,
                running=not self._get_sub_process_is_finished_()
            )
            #
            painter._draw_process_statuses_by_rect_(
                rect=self._sub_process_status_rect,
                colors=sub_status_rgba_array,
                offset=offset,
                border_radius=1,
            )
        # validator
        elif self._get_validator_is_enable_() is True:
            sub_status_rgba_array = [
                self._validator_status_colors, self._hover_validator_status_colors
            ][self._is_hovered]
            painter._draw_process_statuses_by_rect_(
                self._validator_status_rect,
                colors=sub_status_rgba_array,
                offset=offset,
                border_radius=1,
            )
        #
        if self._get_progress_is_enable_() is True:
            painter._draw_frame_by_rect_(
                rect=self._progress_rect,
                border_color=_qt_core.QtRgba.Transparent,
                background_color=_qt_core.QtRgba.BkgProgress,
                border_radius=2,
                offset=offset
            )
        # check
        if self._get_check_action_is_enable_() is True:
            painter._draw_icon_file_by_rect_(
                self._check_icon_draw_rect,
                self._check_icon_file_path_current,
                offset=offset,
                is_hovered=self._is_hovered
            )
        # icon
        if self._file_icon_flag is True:
            if self._icon_file_path is not None:
                painter._draw_icon_file_by_rect_(
                    self._icon_draw_rect,
                    self._icon_file_path,
                    offset=offset,
                    is_hovered=self._is_hovered
                )
            elif self._icon_color_rgb is not None:
                painter._set_color_icon_draw_(
                    self._icon_color_draw_rect, self._icon_color_rgb, offset=offset
                )
            elif self._icon_text is not None:
                painter._draw_image_use_text_by_rect_(
                    self._icon_text_draw_rect,
                    self._icon_text,
                    offset=offset,
                    border_radius=2,
                    is_hovered=self._is_hovered
                )
        # name
        if self._name_text is not None:
            name_text = self._name_text
            if self._action_is_enable is True:
                text_color = [_qt_core.QtRgba.Text, _qt_core.QtRgba.TextHover][self._is_hovered]
            else:
                text_color = _qt_core.QtRgba.TxtDisable
            #
            if self._get_sub_process_is_enable_() is True:
                name_text = '{} - {}'.format(
                    bsc_core.ensure_string(self._name_text), self._get_sub_process_status_text_()
                )
            #
            painter._draw_text_by_rect_(
                self._name_draw_rect,
                text=name_text,
                text_color=text_color,
                font=self._name_draw_font,
                offset=offset
            )
        if self._sub_name_text is not None:
            painter._draw_text_by_rect_(
                self._sub_name_draw_rect,
                text=self._sub_name_text,
                text_option=QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter,
                text_color=_qt_core.QtRgba.TxtTemporary,
                font=self._name_draw_font,
                offset=offset,
            )
        # option
        if self._get_option_click_is_enable_() is True:
            painter._draw_icon_file_by_rect_(
                self._option_icon_draw_rect,
                self._option_icon_file_path,
                offset=offset,
                is_hovered=self._is_hovered
            )
        elif self._menu_flag is True:
            painter._draw_icon_file_by_rect_(
                self._menu_icon_draw_rect,
                self._menu_icon_file_path,
                offset=offset,
                is_hovered=self._is_hovered
            )


class QtIconPressButton(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtFrameBaseDef,
    _qt_abstracts.AbsQtNameBaseDef,
    _qt_abstracts.AbsQtPathBaseDef,
    _qt_abstracts.AbsQtIconBaseDef,
    _qt_abstracts.AbsQtMenuBaseDef,
    #
    _qt_abstracts.AbsQtStatusBaseDef,
    _qt_abstracts.AbsQtStateDef,
    #
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForPressDef,
    _qt_abstracts.AbsQtActionForDragDef,
    #
    _qt_abstracts.AbsQtThreadBaseDef,
    #
    _qt_abstracts.AbsQtItemLayoutBaseDef,
):
    clicked = qt_signal()
    press_dbl_clicked = qt_signal()
    #
    QT_MENU_CLS = _utility.QtMenu

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()

        if self._icon_geometry_mode == self.IconGeometryMode.Square:
            icn_frm_w = icn_frm_h = w
        elif self._icon_geometry_mode == self.IconGeometryMode.Auto:
            icn_frm_w, icn_frm_h = w, h
        else:
            raise RuntimeError()

        self._frame_draw_rect.setRect(
            x, y, w-1, h-1
        )

        icn_w, icn_h = int(icn_frm_w*self._icon_draw_percent), int(icn_frm_h*self._icon_draw_percent)
        icn_x, icn_y = x+(icn_frm_w-icn_w)/2, y+(icn_frm_h-icn_h)/2

        if self._file_icon_flag is True:
            # sub icon
            if self._icon is not None or \
                    self._sub_icon_file_path or \
                    self._sub_icon_text or \
                    self._icon_state_draw_is_enable:
                if self._icon_state_draw_is_enable is True:
                    icn_s_p = self._icon_sub_draw_percent
                    icn_s_w, icn_s_h = icn_frm_w*icn_s_p, icn_frm_h*icn_s_p
                    o_x, o_y = icn_x, icn_y
                    self._icon_draw_rect.setRect(
                        x+1, y+1, icn_w, icn_h
                    )
                    icn_s_w, icn_s_h = min(icn_s_w, 16), min(icn_s_h, 16)
                    self._icon_sub_draw_rect.setRect(
                        x+icn_frm_w-icn_s_w-1-o_x, y+icn_frm_h-icn_s_h-1-o_y, icn_s_w, icn_s_h
                    )
                    icn_sst_p = self._icon_state_draw_percent
                    icn_stt_w, icn_stt_h = icn_frm_w*icn_sst_p, icn_frm_h*icn_sst_p
                    #
                    self._icon_state_rect.setRect(
                        x+icn_frm_w-icn_stt_w-1, y+icn_frm_h-icn_stt_h-1, icn_stt_w, icn_stt_h
                    )
                    icn_stt_w, icn_stt_h = min(icn_stt_w, 8), min(icn_stt_h, 8)
                    self._icon_state_draw_rect.setRect(
                        x+icn_frm_w-icn_stt_w-1, y+icn_frm_h-icn_stt_h-1, icn_stt_w, icn_stt_h
                    )
                else:
                    icn_s_p = self._icon_sub_draw_percent
                    icn_s_w, icn_s_h = icn_frm_w*icn_s_p, icn_frm_h*icn_s_p
                    icn_s_w, icn_s_h = min(icn_s_w, 16), min(icn_s_h, 16)
                    self._icon_draw_rect.setRect(
                        icn_x, icn_y, icn_w, icn_h
                    )
                    self._icon_sub_draw_rect.setRect(
                        x+icn_frm_w-icn_s_w-1, y+icn_frm_h-icn_s_h-1, icn_s_w, icn_s_h
                    )
            else:
                self._icon_draw_rect.setRect(
                    icn_x, icn_y, icn_w, icn_h
                )

        self._name_draw_rect.setRect(
            x, y+icn_frm_h, w, h-icn_frm_w
        )

        s_w, s_h = w*.5, w*.5
        self._action_state_rect.setRect(
            x, y+h-s_h, s_w, s_h
        )

    def __init__(self, *args, **kwargs):
        super(QtIconPressButton, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFont(_qt_core.QtFonts.NameNormal)
        self.setFixedSize(20, 20)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._init_frame_base_def_(self)
        self._init_path_base_def_(self)
        self._init_name_base_def_(self)
        self._init_icon_base_def_(self)
        self._init_menu_base_def_(self)
        self._init_status_base_def_(self)
        self._set_state_def_init_()
        #
        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)
        self._init_action_for_drag_def_(self)
        self._init_thread_base_def_(self)
        #
        self._init_item_layout_base_def_(self)
        #
        self._choose_enable = False
        self._choose_args = []

        self.__use_as_tool = False
        self.__icon_style = None

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if self._get_action_is_enable_() is True:
                self._execute_action_hover_by_filter_(event)
                if event.type() == QtCore.QEvent.MouseButtonPress:
                    self._press_point = event.pos()
                    if event.button() == QtCore.Qt.LeftButton:
                        if self._choose_enable is True:
                            pass
                        self.pressed.emit()
                        self._set_action_flag_(self.ActionFlag.Press)
                    elif event.button() == QtCore.Qt.RightButton:
                        self._popup_menu_()
                    self._refresh_widget_draw_()
                elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                    if event.button() == QtCore.Qt.LeftButton:
                        self._set_action_flag_(self.ActionFlag.PressDblClick)
                    elif event.button() == QtCore.Qt.RightButton:
                        pass
                elif event.type() == QtCore.QEvent.MouseButtonRelease:
                    if event.button() == QtCore.Qt.LeftButton:
                        if self._is_action_flag_match_(self.ActionFlag.PressDblClick):
                            self.press_dbl_clicked.emit()
                        elif self._is_action_flag_match_(self.ActionFlag.Press):
                            p = event.pos()
                            if self._icon_state_draw_is_enable:
                                if self._icon_state_rect.contains(p):
                                    self._popup_menu_()
                                else:
                                    self.press_clicked.emit()
                            else:
                                self.press_clicked.emit()
                    elif event.button() == QtCore.Qt.RightButton:
                        pass
                    #
                    self._set_hovered_(False)
                    self._clear_all_action_flags_()
                # drag move
                elif event.type() == QtCore.QEvent.MouseMove:
                    if event.buttons() == QtCore.Qt.LeftButton:
                        if self._drag_is_enable is True:
                            if self._is_action_flag_match_(self.ActionFlag.Press):
                                self._drag_press_point = self._press_point
                                self._set_action_flag_(self.ActionFlag.DragPress)
                            elif self._is_action_flag_match_(self.ActionFlag.DragPress):
                                self._do_drag_press_(event)
                            elif self._is_action_flag_match_(self.ActionFlag.DragMove):
                                self._do_drag_move_(event)
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        self._refresh_widget_draw_geometry_()
        offset = self._get_action_offset_()
        is_pressed = self._is_action_flag_match_(
            self.ActionFlag.Press, self.ActionFlag.DragPress, self.ActionFlag.DragMove
        )
        if self._is_action_flag_match_(self.ActionFlag.DragMove):
            painter._draw_frame_by_rect_(
                rect=self._frame_draw_rect,
                border_color=_qt_core.QtRgba.BdrButton,
                background_color=_qt_core.QtRgba.BackgroundSelect,
            )

        if self._thread_draw_flag is True:
            painter._draw_alternating_colors_by_rect_(
                rect=self._frame_draw_rect,
                colors=((0, 0, 0, 63), (0, 0, 0, 0)),
                # border_radius=4,
                running=True
            )
        # icon
        if self._file_icon_flag is True:
            if self._icon:
                painter._draw_icon_by_rect_(
                    icon=self._icon,
                    rect=self._icon_draw_rect,
                    offset=offset
                )
            elif self._icon_file_path is not None:
                painter._draw_icon_file_by_rect_(
                    rect=self._icon_draw_rect,
                    file_path=self._icon_file_path,
                    offset=offset,
                    is_hovered=self._is_hovered,
                    hover_color=self._icon_hover_color,
                    is_pressed=is_pressed,
                    is_action_enable=self._action_is_enable,
                )
            elif self._icon_text is not None:
                if self.__icon_style is not None:
                    painter._draw_styled_button_use_text_by_rect_(
                        rect=self._icon_draw_rect,
                        text=self._icon_text,
                        icon_style=self.__icon_style,
                        background_color=self._icon_name_rgba,
                        offset=offset,
                        is_hovered=self._is_hovered,
                        is_pressed=is_pressed
                    )
                else:
                    painter._draw_image_use_text_by_rect_(
                        rect=self._icon_draw_rect,
                        text=self._icon_text,
                        background_color=self._icon_name_rgba,
                        offset=offset,
                        border_width='auto',
                        border_radius=2,
                        is_hovered=self._is_hovered,
                        is_pressed=is_pressed
                    )
            #
            if self._sub_icon_file_path:
                painter._draw_image_use_file_path_by_rect_(
                    rect=self._icon_sub_draw_rect,
                    file_path=self._sub_icon_file_path,
                    offset=offset,
                    is_hovered=self._is_hovered,
                    #
                    draw_frame=True,
                    background_color=_qt_core.QtRgba.BkgSubIcon,
                    border_color=_qt_core.QtRgba.BdrSubIcon,
                    border_radius=4
                )
            #
            if self._icon_state_draw_is_enable is True:
                if self._icon_state_file_path is not None:
                    painter._draw_icon_file_by_rect_(
                        rect=self._icon_state_draw_rect,
                        file_path=self._icon_state_file_path,
                        offset=offset,
                        is_hovered=self._is_hovered,
                        is_action_enable=self._action_is_enable,
                    )
        # state
        # if self._action_state in [self.ActionState.Disable]:
        #     painter._draw_icon_file_by_rect_(
        #         self._action_state_rect,
        #         _gui_core.GuiIcon.get('state-disable')
        #     )
        # text
        if self._name_text:
            painter._draw_text_by_rect_(
                rect=self._name_draw_rect,
                text=self._name_text,
                font=_qt_core.QtFonts.Default,
                text_option=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop,
                word_warp=self._name_word_warp,
                offset=offset,
                # is_hovered=self._is_hovered,
            )

    def _set_use_as_tool_(self, boolean):
        self.__use_as_tool = boolean

    def _set_icon_style_(self, style):
        self.__icon_style = style

    def _do_drag_press_(self, event):
        p = event.pos()
        p_d = p-self._drag_press_point
        x, y = p_d.x(), p_d.y()
        # enable when mouse moved more than 10 pixel
        if abs(x) > 10 or abs(y) > 10:
            self._set_action_flag_(self.ActionFlag.DragMove)

    # noinspection PyUnusedLocal
    def _do_drag_move_(self, event):
        self.__drag = _drag.QtDrag(self)

        item = self._get_layout_item_()
        if item is not None:
            key = item.get_drag_and_drop_key()
            self._set_drag_data_(
                {
                    'lynxi/drag-and-drop-key': key,
                    'lynxi/drag-and-drop-scheme': self._get_drag_and_drop_scheme_()
                }
            )
            item.start_drag_and_drop(self._get_drag_and_drop_scheme_())

            self.__drag.setMimeData(self._generate_drag_mime_data_())

            self.__drag._do_drag_move_(self._drag_press_point)

            self.__drag.released.connect(self._drag_release_cbk_)

            self._refresh_widget_draw_()

    def _drag_release_cbk_(self):
        self._clear_all_action_flags_()
        l_i = self._get_layout_item_()
        if l_i is not None:
            l_i.get_layout_view()._drag_release_cbk_()

    def _set_visible_(self, boolean):
        self.setVisible(boolean)

    def _execute_choose_start_(self):
        pass

    def _set_menu_data_(self, data):
        super(QtIconPressButton, self)._set_menu_data_(data)
        #
        self._icon_state_draw_is_enable = True
        self._icon_state_file_path = _gui_core.GuiIcon.get(
            'state/popup'
        )

    def _set_menu_data_generate_fnc_(self, fnc):
        super(QtIconPressButton, self)._set_menu_data_generate_fnc_(fnc)
        #
        self._icon_state_draw_is_enable = True
        self._icon_state_file_path = _gui_core.GuiIcon.get(
            'state/popup'
        )

    def _save_main_icon_to_file_(self, file_path, size=(128, 128)):
        w, h = size
        size = QtCore.QSize(w, h)
        pixmap = QtGui.QPixmap(size)
        painter = _qt_core.QtPainter(pixmap)
        pixmap.fill(QtGui.QColor(64, 64, 64, 255))
        rect = pixmap.rect()

        offset = 0
        is_pressed = False

        if self._file_icon_flag is True:
            if self._icon:
                painter._draw_icon_by_rect_(
                    icon=self._icon,
                    rect=rect,
                    offset=offset
                )
            elif self._icon_file_path is not None:
                painter._draw_icon_file_by_rect_(
                    rect=rect,
                    file_path=self._icon_file_path,
                    offset=offset,
                    is_hovered=self._is_hovered,
                    hover_color=self._icon_hover_color,
                    is_pressed=is_pressed,
                )
            elif self._icon_text is not None:
                if self.__icon_style is not None:
                    painter._draw_styled_button_use_text_by_rect_(
                        rect=rect,
                        text=self._icon_text,
                        icon_style=self.__icon_style,
                        background_color=self._icon_name_rgba,
                        offset=offset,
                        is_hovered=self._is_hovered,
                        is_pressed=is_pressed
                    )
                else:
                    painter._draw_image_use_text_by_rect_(
                        rect=rect,
                        text=self._icon_text,
                        background_color=self._icon_name_rgba,
                        offset=offset,
                        border_width='auto',
                        border_radius=2,
                        is_hovered=self._is_hovered,
                        is_pressed=is_pressed
                    )

        painter.end()

        ext = os.path.splitext(file_path)[-1]
        if ext:
            if ext.lower() not in ['.png', '.jpg', '.jpeg']:
                format_ = 'PNG'
            else:
                format_ = str(ext[1:]).upper()
        else:
            format_ = 'PNG'

        pixmap.save(
            file_path,
            format_
        )


class QtIconMenuButton(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtIconBaseDef,
    _qt_abstracts.AbsQtNameBaseDef,
    _qt_abstracts.AbsQtMenuBaseDef,
    #
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForPressDef,
):
    QT_MENU_CLS = _utility.QtMenu

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        icn_frm_w, icn_frm_h = w, h
        #
        icn_w, icn_h = int(icn_frm_w*self._icon_draw_percent), int(icn_frm_h*self._icon_draw_percent)
        icn_x, icn_y = x+(w-icn_w)/2, y+(h-icn_h)/2
        #
        if self._file_icon_flag is True:
            self._icon_draw_rect.setRect(
                icn_x, icn_y, icn_w, icn_h
            )

    def __init__(self, *args, **kwargs):
        super(QtIconMenuButton, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFont(_qt_core.QtFonts.NameNormal)
        self.setFixedSize(20, 20)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._init_name_base_def_(self)
        self._init_icon_base_def_(self)
        self._init_menu_base_def_(self)
        #
        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if self._get_action_is_enable_() is True:
                self._execute_action_hover_by_filter_(event)
                #
                if event.type() == QtCore.QEvent.Resize:
                    self._refresh_widget_draw_geometry_()
                elif event.type() in {QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonDblClick}:
                    self._set_action_flag_(self.ActionFlag.Press)
                    self._refresh_widget_all_()
                elif event.type() == QtCore.QEvent.MouseButtonRelease:
                    if self._is_action_flag_match_(self.ActionFlag.Press):
                        self._popup_menu_()
                    self._clear_all_action_flags_()
                    self._refresh_widget_all_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        offset = self._get_action_offset_()
        # icon
        if self._file_icon_flag is True:
            if self._icon_file_path is not None:
                painter._draw_icon_file_by_rect_(
                    rect=self._icon_draw_rect,
                    file_path=self._icon_file_path,
                    offset=offset,
                    is_hovered=self._is_hovered,
                    is_pressed=self._is_pressed
                )


class QtIconToggleButton(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtWidgetBaseDef,
    _qt_abstracts.AbsQtFrameBaseDef,
    _qt_abstracts.AbsQtIconBaseDef,
    _qt_abstracts.AbsQtNameBaseDef,
    _qt_abstracts.AbsQtMenuBaseDef,
    #
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForCheckDef,
    #
    _qt_abstracts.AbsQtValueDefaultExtraDef,
):
    def _refresh_widget_all_(self):
        pass

    QT_MENU_CLS = _utility.QtMenu

    def __init__(self, *args, **kwargs):
        super(QtIconToggleButton, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        qt_palette = _qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)
        self.setFont(_qt_core.QtFonts.NameNormal)

        self.setFixedSize(20, 20)

        self.installEventFilter(self)

        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self._init_widget_base_def_(self)
        self._init_frame_base_def_(self)
        self._init_icon_base_def_(self)
        self._init_name_base_def_(self)
        self._init_menu_base_def_(self)

        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_check_def_(self)
        self._set_check_enable_(True)

        self._init_value_default_extra_def_(self)

        self._refresh_check_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        spacing = 2
        r = min(w, h)
        icn_frm_w = icn_frm_h = min(w, h)-2
        icn_p = self._icon_draw_percent
        icn_w = icn_h = r*icn_p
        #
        self._frame_draw_rect.setRect(
            x, y, w-1, h-1
        )
        self._check_frame_rect.setRect(
            x+(w-icn_frm_w)/2, y+(h-icn_frm_w)/2, icn_frm_w, icn_frm_h
        )
        #
        if self._file_icon_flag is True:
            if self._sub_icon_file_path or self._sub_icon_text:
                self._icon_draw_rect.setRect(
                    x+2, y+2, icn_w, icn_h
                )
                #
                icn_s_p = self._icon_sub_draw_percent
                icn_s_w, icn_s_h = icn_frm_w*icn_s_p, icn_frm_h*icn_s_p
                self._icon_sub_draw_rect.setRect(
                    x+w-icn_s_w-1, y+h-icn_s_h-1, icn_s_w, icn_s_h
                )
            # state
            elif self._icon_state_draw_is_enable is True:
                icn_s_p = self._icon_state_draw_percent
                icn_s_w, icn_s_h = icn_frm_w*icn_s_p, icn_frm_h*icn_s_p
                self._icon_state_draw_rect.setRect(
                    x+w-icn_s_w-1, y+h-icn_s_h-1, icn_s_w, icn_s_h
                )
                self._icon_draw_rect.setRect(
                    x+2, y+2, w-icn_s_w, h-icn_s_h
                )
            else:
                self._set_icon_file_draw_rect_(
                    x+(w-icn_w)/2, y+(h-icn_h)/2, icn_w, icn_h
                )
        #
        x += icn_frm_w+spacing
        self._set_name_draw_rect_(
            x, y, w-x, h
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            #
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.CheckPress)
                elif event.button() == QtCore.Qt.RightButton:
                    self._popup_menu_()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_() == self.ActionFlag.CheckPress:
                        self._swap_user_check_action_()
                    #
                    self._clear_all_action_flags_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        #
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        #
        background_color = painter._generate_item_background_color_by_rect_(
            self._check_frame_rect,
            is_hovered=self._is_hovered,
            is_selected=self._is_checked,
            is_actioned=self._get_is_actioned_()
        )
        painter._draw_frame_by_rect_(
            self._check_frame_rect,
            border_color=_qt_core.QtRgba.Transparent,
            background_color=background_color,
            border_radius=2,
            offset=offset
        )
        #
        if self._file_icon_flag is True:
            if self._icon_file_path is not None:
                painter._draw_icon_file_by_rect_(
                    rect=self._icon_draw_rect,
                    file_path=self._icon_file_path,
                    offset=offset,
                    is_hovered=self._is_hovered
                )
                if self._sub_icon_text:
                    painter._draw_image_use_text_by_rect_(
                        rect=self._icon_sub_draw_rect,
                        text=self._sub_icon_text,
                        border_radius=4,
                        offset=offset
                    )
                elif self._sub_icon_file_path:
                    painter._draw_icon_file_by_rect_(
                        rect=self._icon_sub_draw_rect,
                        file_path=self._sub_icon_file_path,
                        offset=offset,
                        is_hovered=self._is_hovered
                    )
                elif self._icon_state_draw_is_enable is True:
                    if self._icon_state_file_path is not None:
                        painter._draw_icon_file_by_rect_(
                            rect=self._icon_state_draw_rect,
                            file_path=self._icon_state_file_path,
                            offset=offset,
                            is_hovered=self._is_hovered
                        )
        #
        if self._name_text is not None:
            painter._draw_text_by_rect_(
                self._name_draw_rect,
                self._name_text,
                font=_qt_core.QtFonts.NameNormal,
                text_color=_qt_core.QtRgba.Text,
                text_option=QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter,
                offset=offset
            )

    def _get_value_(self):
        return self._is_checked_()

    def _set_menu_data_(self, data):
        super(QtIconToggleButton, self)._set_menu_data_(data)
        self._icon_state_draw_is_enable = True
        self._icon_state_file_path = _gui_core.GuiIcon.get(
            'state/popup'
        )

    def _set_menu_data_generate_fnc_(self, fnc):
        super(QtIconToggleButton, self)._set_menu_data_generate_fnc_(fnc)
        #
        self._icon_state_draw_is_enable = True
        self._icon_state_file_path = _gui_core.GuiIcon.get(
            'state/popup'
        )
