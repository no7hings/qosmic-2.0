# coding=utf-8
import lxbasic.core as bsc_core
# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *
# qt widgets
from .. import core as _qt_core

from .. import abstracts as _qt_abstracts

from . import button as _qt_wgt_button


class _QtStatusItem(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtFrameBaseDef,
    _qt_abstracts.AbsQtNameBaseDef,
    _qt_abstracts.AbsQtIconBaseDef,
    #
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForCheckDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtStatusItem, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self.setMaximumHeight(20)
        self.setMinimumHeight(20)
        #
        self.installEventFilter(self)
        #
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._init_frame_base_def_(self)
        self._init_name_base_def_(self)
        self._set_name_text_('status button')
        self._init_icon_base_def_(self)
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_check_def_(self)
        #
        self._refresh_check_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        icn_w, icn_h = self._icon_color_draw_size
        self._set_color_icon_rect_(
            x+(w-icn_w)/2, y+(h-icn_h)/2, icn_w, icn_h
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            #
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.CheckPress)
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
        is_hovered = self._is_hovered_()
        #
        if self._is_checked_():
            background_color = [_qt_core.QtRgba.Yellow, _qt_core.QtRgba.BackgroundHover][is_hovered]
            painter._draw_image_use_text_by_rect_(
                rect=self._color_icon_draw_rect,
                text='l',
                background_color=background_color,
                offset=offset,
                is_hovered=is_hovered,
                border_radius=1
            )
        else:
            background_color = [_qt_core.QtRgba.Transparent, _qt_core.QtRgba.BackgroundHover][is_hovered]
            painter._draw_image_use_text_by_rect_(
                rect=self._color_icon_draw_rect,
                text='d',
                background_color=background_color,
                offset=offset,
                is_hovered=is_hovered,
                border_radius=1
            )


class _QtHContractItem(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtIconBaseDef,
    #
    _qt_abstracts.AbsQtNameBaseDef,
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForPressDef,
    _qt_abstracts.AbsQtActionForExpandDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtHContractItem, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        #
        self._name_draw_font = _qt_core.QtFonts.ToolGroup
        #
        self._init_icon_base_def_(self)
        self._init_name_base_def_(self)
        self._name_icon_flag = True
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)
        self._init_action_for_expand_def_(self)
        #
        self._is_expanded = False
        self._expand_icon_file_path_0 = _gui_core.GuiIcon.get('contract_v_r')
        self._expand_icon_file_path_1 = _gui_core.GuiIcon.get('contract_v_l')

        self._expand_sub_icon_file_path_0 = None
        self._expand_sub_icon_file_path_1 = None

        self._is_hovered = False
        #
        self._refresh_expand_()
        #
        r, g, b = 207, 207, 207
        h, s, v = bsc_core.BscColor.rgb_to_hsv(r, g, b)
        color = bsc_core.BscColor.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        #
        self._name_draw_color = color
        self._hover_name_color = hover_color
        #
        r, g, b = 135, 135, 135
        h, s, v = bsc_core.BscColor.rgb_to_hsv(r, g, b)
        color = bsc_core.BscColor.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        #
        self._frame_border_color = color
        self._hovered_frame_border_color = hover_color
        #
        r, g, b = 119, 119, 119
        h, s, v = bsc_core.BscColor.rgb_to_hsv(r, g, b)
        color = bsc_core.BscColor.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        self._frame_background_color = color
        self._hovered_frame_background_color = hover_color
        # font
        self.setFont(_qt_core.QtFonts.NameNormal)

        self._icon_frame_draw_size = 12, 24
        self._icon_draw_percent = 1
        self._icon_draw_size = 10, 20

    def _set_expand_direction_(self, direction):
        if direction == self.CollapseDirection.RightToLeft:
            self._expand_icon_file_path_0 = _gui_core.GuiIcon.get('contract_v_r')
            self._expand_icon_file_path_1 = _gui_core.GuiIcon.get('contract_v_l')
        elif direction == self.CollapseDirection.LeftToRight:
            self._expand_icon_file_path_0 = _gui_core.GuiIcon.get('contract_v_l')
            self._expand_icon_file_path_1 = _gui_core.GuiIcon.get('contract_v_r')
        #
        self._refresh_expand_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        c_x, c_y = 0, 0
        w, h = self.width(), self.height()
        #
        frm_w, frm_h = self._icon_frame_draw_size
        icn_w, icn_h = self._icon_draw_size
        self._set_icon_file_draw_rect_(
            c_x+(w-icn_w)/2, c_y+(frm_h-icn_h)/2, icn_w, icn_h
        )

    def _set_expand_icon_file_path_(self, icon_file_path_0, icon_file_path_1):
        self._expand_icon_file_path_1 = icon_file_path_0
        self._expand_icon_file_path_0 = icon_file_path_1
        self._refresh_expand_()

    def _set_expand_icon_names_(self, icon_name_0, icon_name_1):
        self._expand_icon_file_path_1 = _gui_core.GuiIcon.get(icon_name_0)
        self._expand_icon_file_path_0 = _gui_core.GuiIcon.get(icon_name_1)
        self._refresh_expand_()

    def _set_expand_sub_icon_names_(self, icon_name_0, icon_name_1):
        self._expand_sub_icon_file_path_0 = _gui_core.GuiIcon.get(icon_name_0)
        self._expand_sub_icon_file_path_1 = _gui_core.GuiIcon.get(icon_name_1)
        self._refresh_expand_()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            #
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.ExpandPress)
                    #
                    self.press_toggled.emit(True)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_() == self.ActionFlag.ExpandPress:
                        self._execute_action_expand_()
                    #
                    self.press_toggled.emit(False)
                #
                self._clear_all_action_flags_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        #
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        # file-icon
        painter._draw_icon_file_by_rect_(
            self._icon_draw_rect,
            self._icon_file_path,
            offset=offset,
            is_hovered=self._is_hovered
        )

    def set_expanded(self, boolean):
        self._is_expanded = boolean

    def _refresh_expand_(self):
        self._set_icon_file_path_(
            [self._expand_icon_file_path_0, self._expand_icon_file_path_1][self._is_expanded]
        )
        self._set_sub_icon_file_path_(
            [self._expand_sub_icon_file_path_1, self._expand_sub_icon_file_path_0][self._is_expanded]
        )
        #
        self._set_hovered_(False)
        self._refresh_widget_draw_()


class _QtWindowHead(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtFrameBaseDef,
):
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_QtWindowHead, self).__init__(*args, **kwargs)
        #
        self.setMinimumHeight(24)
        self.setMaximumHeight(24)
        #
        self._init_frame_base_def_(self)
        #
        self._frame_background_color = 71, 71, 71, 255
        self._frame_border_color = 95, 95, 95, 255
        #
        self._close_button = _qt_wgt_button.QtIconPressButton(self)
        self._close_button._set_icon_file_path_(
            _gui_core.GuiIcon.get('close')
        )
        self._close_button._set_hover_icon_file_path_(
            _gui_core.GuiIcon.get('close-hover')
        )
        #
        self._close_button.press_clicked.connect(
            self._set_window_close_
        )
        #
        self._orientation = QtCore.Qt.Horizontal

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        #
        self._set_widget_geometries_update_()
        #
        painter._draw_frame_by_rect_(
            self._frame_draw_rect,
            background_color=self._frame_background_color,
            border_color=self._frame_border_color
        )

    def _set_window_close_(self):
        self.parent().close()
        self.parent().deleteLater()

    def _set_widget_geometries_update_(self):
        pos_x, pos_y = 0, 0
        width, height = self.width(), self.height()
        self._set_frame_draw_rect_(
            pos_x, pos_y, width, height
        )
        #
        side = 2
        i_x, i_y = width-side, pos_y+side
        i_w, i_h = 20, 20
        if self._orientation == QtCore.Qt.Horizontal:
            self._close_button.setGeometry(
                i_x-i_w, i_y, i_w, i_h
            )
