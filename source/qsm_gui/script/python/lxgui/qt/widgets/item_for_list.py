# coding=utf-8
import six

import math

import lxbasic.core as bsc_core
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import core as gui_qt_core

from .. import abstracts as gui_qt_abstracts
# qt widgets
from . import utility as gui_qt_wgt_utility

from . import drag as gui_qt_wgt_drag


class QtListItemWidget(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtWidgetBaseDef,
    gui_qt_abstracts.AbsQtFrameBaseDef,
    gui_qt_abstracts.AbsQtTypeDef,
    gui_qt_abstracts.AbsQtIndexBaseDef,
    gui_qt_abstracts.AbsQtImageBaseDef,
    gui_qt_abstracts.AbsQtMovieBaseDef,
    #
    gui_qt_abstracts.AbsQtMenuBaseDef,
    #
    gui_qt_abstracts.AbsQtIconBaseDef,
    gui_qt_abstracts.AbsQtIconsBaseDef,
    gui_qt_abstracts.AbsQtNamesBaseDef,
    #
    gui_qt_abstracts.AbsQtActionBaseDef,
    gui_qt_abstracts.AbsQtActionForHoverDef,
    gui_qt_abstracts.AbsQtActionForCheckDef,
    gui_qt_abstracts.AbsQtActionForPressDef,
    gui_qt_abstracts.AbsQtPressSelectExtraDef,
    gui_qt_abstracts.AbsQtActionForDragDef,
    #
    gui_qt_abstracts.AbsQtStateDef,
    gui_qt_abstracts.AbsQtStatusBaseDef,
    #
    gui_qt_abstracts.AbsQtItemMovieActionDef,
    #
    gui_qt_abstracts.AbsQtItemWidgetExtra,
):
    viewport_show = qt_signal()
    viewport_hide = qt_signal()
    #
    drag_pressed = qt_signal(tuple)
    drag_released = qt_signal(tuple)
    #
    QT_MENU_CLS = gui_qt_wgt_utility.QtMenu

    def _refresh_widget_all_(self, *args, **kwargs):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_force_(self):
        self._refresh_widget_draw_geometry_()
        # noinspection PyUnresolvedReferences
        self.update()

    def _refresh_widget_draw_geometry_(self):
        self._refresh_widget_frame_draw_geometries_()
        #
        self._refresh_widget_icon_draw_geometries_()
        self._refresh_widget_image_draw_geometries_()
        self._refresh_widget_name_draw_geometries_()

    def _refresh_widget_icon_draw_geometries_(self):
        if self._get_has_icons_() is True or self._check_is_enable is True:
            rect = self._icon_frame_draw_rect
            x, y = rect.x(), rect.y()
            w, h = rect.width(), rect.height()
            #
            _side = 2
            spacing = 0
            #
            icn_frm_w, icn_frm_h = self._icon_frame_draw_size
            icn_w, icn_h = self._icon_draw_size
            if self._check_is_enable is True:
                check_icn_frm_w, check_icn_frm_h = icn_frm_w*self._check_icon_frame_draw_percent, icn_frm_h*self._check_icon_frame_draw_percent
                check_icn_w, check_icn_h = icn_frm_w*self._check_icon_draw_percent, icn_frm_h*self._check_icon_draw_percent
                #
                self._set_check_action_rect_(
                    x, y, icn_frm_w, icn_frm_h
                )
                self._set_check_icon_frame_draw_rect_(
                    x+(icn_frm_w-check_icn_frm_w)/2, y+(icn_frm_h-check_icn_frm_h)/2, check_icn_frm_w, check_icn_frm_h
                )
                self._set_check_icon_draw_rect_(
                    x+(icn_frm_w-check_icn_w)/2, y+(icn_frm_h-check_icn_h)/2, check_icn_w, check_icn_h
                )
            icn_indices = self._get_icon_indices_()
            if icn_indices:
                c_0 = int(float(h)/icn_frm_h)
                if self._check_is_enable is True:
                    icn_indices_ = icn_indices+[len(icn_indices)]
                    for i_icn_index in icn_indices_:
                        i_column = int(float(i_icn_index)/c_0)
                        if i_column > 0:
                            i_icn_index_draw = i_icn_index%c_0
                        else:
                            i_icn_index_draw = i_icn_index
                        #
                        if i_icn_index > 0:
                            self._set_icon_rect_at_(
                                x+(icn_frm_w-icn_w)/2+icn_frm_w*i_column,
                                y+(icn_frm_h-icn_h)/2+i_icn_index_draw*(icn_frm_h+spacing), icn_w, icn_h,
                                i_icn_index-1
                            )
                else:
                    for i_icn_index in icn_indices:
                        i_column = int(float(i_icn_index)/c_0)
                        if i_column > 0:
                            i_icn_index_draw = i_icn_index%c_0
                        else:
                            i_icn_index_draw = i_icn_index
                        #
                        self._set_icon_rect_at_(
                            x+(icn_frm_w-icn_w)/2+icn_frm_w*i_column,
                            y+(icn_frm_h-icn_h)/2+i_icn_index_draw*(icn_frm_h+spacing), icn_w, icn_h,
                            i_icn_index
                        )

    def _refresh_widget_image_draw_geometries_(self):
        if self._get_has_image_() is True:
            rect = self._image_frame_rect
            x, y = rect.x(), rect.y()
            w, h = rect.width(), rect.height()
            frm_r = min(w, h)
            i_w_0, i_h_0 = self._get_image_size_()
            if (i_w_0, i_h_0) != (0, 0):
                i_x, i_y, img_w, img_h = bsc_core.RawSizeMtd.fit_to(
                    (i_w_0, i_h_0), (w, h)
                )
                if self._get_play_draw_is_enable_() is True:
                    m_f_w, m_f_h = frm_r/4, frm_r/4
                    self._set_movie_rect_(
                        x+i_x+(img_w-m_f_w)/2, y+i_y+(img_h-m_f_h)/2,
                        m_f_w, m_f_h
                    )
                #
                if self._image_file_path is not None:
                    self._image_draw_rect.setRect(
                        x+i_x+2, y+i_y+2, img_w-4, img_h-4
                    )
                else:
                    self._image_draw_rect.setRect(
                        x+i_x, y+i_y, img_w, img_h
                    )
                #
                if self._image_sub_file_path:
                    img_s_w, img_s_h = 24, 24
                    self._image_sub_draw_rect.setRect(
                        x+i_x+img_w-img_s_w, y+i_y+img_h-img_s_h, img_s_w, img_s_h
                    )

    def _refresh_widget_name_draw_geometries_(self):
        if self._get_has_names_():
            name_indices = self._get_name_indices_()
            #
            rect = self._name_frame_draw_rect
            x, y = rect.x(), rect.y()
            w, h = rect.width(), rect.height()
            #
            side = 2
            spacing = 0
            #
            nme_frm_w, nme_frm_h = self._name_frame_size
            nme_w, nme_h = self._name_size
            #
            self._set_index_draw_rect_(
                x+2, y+h-nme_h, w-4, nme_h
            )
            for i_name_index in name_indices:
                i_x, i_y = x+(nme_frm_w-nme_w)/2+side, y+(nme_frm_h-nme_h)/2+i_name_index*(nme_frm_h+spacing)
                if i_y+nme_h < y+h:
                    self._set_name_text_draw_rect_at_(
                        i_x, i_y, w-(i_x-x)-side, nme_h,
                        i_name_index
                    )
                else:
                    self._set_name_text_draw_rect_at_(
                        0, 0, 0, 0,
                        i_name_index
                    )
            #
            if self._icon_is_enable is True:
                if self._icon_text:
                    self._icon_text_draw_rect.setRect(
                        x+(w-h), y, h, h
                    )

    def _refresh_widget_frame_draw_geometries_(self):
        if self._list_widget is not None:
            side = 4
            x, y = 0, 0
            w, h = self.width(), self.height()

            b_x, b_y = side, side
            b_w, b_h = w-side*2, h-side*2
            self._set_frame_draw_rect_(b_x, b_y, b_w, b_h)

            frm_x, frm_y = side, side
            frm_w, frm_h = w-side*2, h-side*2
            #
            m_frm_x, m_frm_y = frm_x+x, frm_y+y
            m_frm_w, m_frm_h = frm_w-x, frm_h-y

            if self._list_widget._get_is_grid_mode_():
                self._do_update_widget_frame_geometries_for_grid_mode_(
                    (m_frm_x, m_frm_y), (m_frm_w, m_frm_h)
                )
            else:
                self._do_update_widget_frame_geometries_for_list_mode_(
                    (m_frm_x, m_frm_y), (m_frm_w, m_frm_h)
                )

    # frame for grid mode
    def _do_update_widget_frame_geometries_for_grid_mode_(self, pos, size):
        x, y = pos
        w, h = size
        frm_s = self._frame_spacing
        # name
        name_bsc_w, name_bsc_h = 0, -frm_s
        if self._get_has_names_() is True:
            name_f_w, name_f_h = self._name_frame_size
            name_c = len(self._get_name_indices_())
            if self._names_draw_range is not None:
                name_c = len(self._get_name_indices_()[self._names_draw_range[0]:self._names_draw_range[1]])
            #
            name_bsc_w, name_bsc_h = w, name_c*name_f_h
            name_x_, name_y_ = x, y+h-name_bsc_h
            #
            self._name_frame_draw_rect.setRect(
                name_x_, name_y_,
                name_bsc_w, name_bsc_h
            )
        # icon
        icon_bsc_w, icon_bsc_h = -frm_s, 0
        if self._get_has_icons_() is True or self._check_is_enable is True:
            #
            icn_frm_w, icn_frm_h = self._icon_frame_draw_size
            icn_x_, icn_y_ = x, y
            # add when check is enable
            icn_c = self._get_icon_count_()+[0, 1][self._check_is_enable]
            icon_bsc_h = h-name_bsc_h-frm_s
            c_0 = int(float(icon_bsc_h)/float(icn_frm_h))
            if c_0 > 0:
                c_1 = math.ceil(float(icn_c)/c_0)
                icon_bsc_w, icon_bsc_h = icn_frm_w*c_1, icon_bsc_h
                #
                self._icon_frame_draw_rect.setRect(
                    icn_x_, icn_y_,
                    icon_bsc_w, icon_bsc_h
                )
            else:
                self._icon_frame_draw_rect.setRect(
                    -40, -40, 20, 20
                )
        # image
        if self._get_has_image_() is True:
            image_x_, image_y_ = x+icon_bsc_w+frm_s, y
            image_bsc_w, image_bsc_h = w-(icon_bsc_w+frm_s), h-(name_bsc_h+frm_s)
            self._image_frame_rect.setRect(
                image_x_, image_y_, image_bsc_w, image_bsc_h
            )

    def _do_update_widget_frame_geometries_for_list_mode_(self, pos, size):
        x, y = pos
        w, h = size
        _f_side = self._frame_side
        spc_frm = self._frame_spacing
        # icon
        c_x = x
        icon_bsc_w, icon_bsc_h = -spc_frm, 0
        if self._get_has_icons_() is True or self._check_is_enable is True:
            icn_frm_w, icn_frm_h = self._icon_frame_draw_size
            icn_x_, icn_y_ = x, y
            # add when check is enable
            icn_c = self._get_icon_count_()+[0, 1][self._check_is_enable]
            icon_bsc_h = h
            c_0 = int(float(icon_bsc_h)/icn_frm_h)
            if c_0 > 0:
                c_1 = math.ceil(float(icn_c)/c_0)
                # grid to
                icon_bsc_w, icon_bsc_h = icn_frm_w*c_1, icon_bsc_h
                #
                self._icon_frame_draw_rect.setRect(
                    icn_x_, icn_y_,
                    icon_bsc_w, icon_bsc_h
                )
            else:
                self._icon_frame_draw_rect.setRect(
                    -40, -40, 20, 20
                )

            c_x += icon_bsc_w+spc_frm
        #
        image_bsc_w, image_bsc_h = -spc_frm, 0
        if self._get_has_image_() is True:
            image_x_, image_y_ = x+(icon_bsc_w+spc_frm), y
            image_bsc_w, image_bsc_h = h, h
            self._image_frame_rect.setRect(
                c_x+spc_frm, image_y_, image_bsc_w, image_bsc_h
            )

            c_x += image_bsc_w+spc_frm
        #
        if self._get_has_names_() is True:
            name_x_, name_y_ = x+(icon_bsc_w+spc_frm)+(image_bsc_w+spc_frm), y
            name_bsc_w, name_bsc_h = w-c_x+spc_frm, h
            #
            self._name_frame_draw_rect.setRect(
                c_x+spc_frm, name_y_,
                name_bsc_w, name_bsc_h
            )

    def __init__(self, *args, **kwargs):
        super(QtListItemWidget, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        #
        self._init_widget_base_def_(self)
        self._init_frame_base_def_(self)
        self._init_type_base_def_(self)
        self._init_index_base_def_(self)
        self._init_icon_base_def_(self)
        self._init_icons_base_def_(self)
        self._init_image_base_def_()
        self._init_names_base_def_(self)
        self._set_name_text_option_to_align_center_top_()
        self._init_menu_base_def_(self)
        self._init_movie_base_def_()
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_check_def_(self)
        self._check_icon_file_path_0 = gui_core.GuiIcon.get('filter_unchecked')
        self._check_icon_file_path_1 = gui_core.GuiIcon.get('filter_checked')
        self._check_icon_file_path_current = self._check_icon_file_path_0
        self._init_action_for_press_def_(self)
        self._init_press_select_extra_def_(self)
        self._init_action_for_drag_def_(self)
        self._init_item_widget_extra_(self)
        #
        self._set_item_movie_action_def_init_()
        #
        self._set_state_def_init_()
        self._init_status_base_def_(self)
        #
        self._file_type_icon = None
        #
        self._list_widget = None
        #
        self._frame_icon_width, self._frame_icon_height = 40, 128
        self._frame_image_width, self._frame_image_height = 128, 128
        self._frame_name_width, self._frame_name_height = 128, 40
        #
        self._frame_side = 4
        self._frame_spacing = 2
        #
        self._frame_size = 128, 128
        #
        self._frame_background_color = gui_qt_core.QtBackgroundColors.Light
        #
        self._is_viewport_show_enable = True
        #
        self.setFont(gui_qt_core.QtFonts.Default)

        self._sort_name_key = ''
        self._sort_number_key = 0

        self._drag = None

    def dragMoveEvent(self, event):
        pass

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Enter:
                self._set_action_hovered_(True)
            elif event.type() == QtCore.QEvent.Leave:
                self._set_action_hovered_(False)
            #
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            # drag move
            elif event.type() == QtCore.QEvent.MouseMove:
                if self._get_action_flag_is_match_(self.ActionFlag.Press):
                    if self._drag_is_enable is True:
                        self._set_action_flag_(self.ActionFlag.DragMove)
                        #
                        self._drag = gui_qt_wgt_drag.QtDrag(self)
                        view = self._get_view_()
                        if view._get_is_multiply_selection_() is True:
                            selected_item_widgets = view._get_selected_item_widgets_()
                            urls = [j for i in selected_item_widgets for j in i._get_drag_urls_()]
                            mine_data = self._create_mine_data_(urls)
                            self._drag.setMimeData(mine_data)
                            self._drag._set_drag_count_(len(selected_item_widgets))
                        else:
                            self._drag.setMimeData(self._generate_drag_mime_data_())
                        #
                        self._drag._do_drag_copy_(self._drag_point_offset)
                        self._drag.released.connect(self._drag_release_cbk_)
                else:
                    self._do_hover_move_(event)
            #
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._drag_point_offset = event.pos()
                    # check
                    if self._get_action_check_is_valid_(event) is True:
                        self._set_action_flag_(self.ActionFlag.CheckPress)
                        event.accept()
                        return True
                    # press
                    else:
                        self._set_pressed_(True)
                        self._set_action_flag_(self.ActionFlag.Press)
                elif event.button() == QtCore.Qt.RightButton:
                    self._popup_menu_()
                    self._clear_all_action_flags_()
                    self._set_action_hovered_(False)
                    event.accept()
                    return True
            #
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    # check
                    if self._get_action_check_is_valid_(event) is True:
                        self._set_action_flag_(self.ActionFlag.CheckDbClick)
                        event.accept()
                        return True
                    # press
                    else:
                        self._set_action_flag_(self.ActionFlag.PressDbClick)
            #
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if self._get_action_flag_is_match_(self.ActionFlag.CheckPress):
                    self._do_check_press_(event)
                    self.check_clicked.emit()
                    self.check_toggled.emit(self._is_checked)
                    self.user_check_toggled.emit(self._is_checked)
                    event.accept()
                    self._clear_all_action_flags_()
                    return True
                elif self._get_action_flag_is_match_(self.ActionFlag.CheckDbClick):
                    self.check_db_clicked.emit()
                elif self._get_action_flag_is_match_(self.ActionFlag.Press):
                    self.press_clicked.emit()
                elif self._get_action_flag_is_match_(self.ActionFlag.PressDbClick):
                    self.press_db_clicked.emit()
                #
                self._clear_all_action_flags_()
            #
            elif event.type() == QtCore.QEvent.ChildAdded:
                self._do_drag_pressed_((self._drag_mime_data,))
                self._set_pressed_(False)
                self._clear_all_action_flags_()
            elif event.type() == QtCore.QEvent.ChildRemoved:
                pass
        else:
            pass
        return False

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)
        #
        x, y = 0, 0
        w, h = self.width(), self.height()
        bsc_x, bsc_y = x+1, y+1
        bsc_w, bsc_h = w-2, h-2
        #
        offset = self._get_action_offset_()
        is_actioned = self._get_is_actioned_()
        #
        base_rect = QtCore.QRect(bsc_x, bsc_y, bsc_w, bsc_h)
        shadow_rect = QtCore.QRect(bsc_x+2, bsc_y+2, bsc_w-2, bsc_h-2)

        bkg_color = painter._get_frame_background_color_by_rect_(
            rect=base_rect,
            check_is_hovered=self._check_is_hovered,
            is_checked=self._is_checked,
            press_is_hovered=self._press_is_hovered,
            is_pressed=is_actioned,
            is_selected=self._is_selected,
        )
        if self._get_status_is_enable_() is True:
            bdr_color_, bdr_hover_color = self._get_rgba_args_by_validator_status_(
                self._status
            )
            if self._press_is_hovered is True:
                bdr_color = bdr_hover_color
            else:
                bdr_color = bdr_color_
        else:
            bdr_color = gui_qt_core.QtBackgroundColors.Transparent
        #
        item = self._get_item_()
        if item._item_show_status in {item.ShowStatus.Loading, item.ShowStatus.Waiting}:
            painter._draw_loading_by_rect_(
                self._rect_frame_draw,
                item._item_show_loading_index
            )
        # else:
        if self._icon_frame_draw_enable is True:
            painter._draw_frame_by_rect_(
                rect=shadow_rect,
                border_color=gui_qt_core.QtBorderColors.Transparent,
                background_color=gui_qt_core.QtBackgroundColors.Shadow,
                offset=4
            )
        # base
        painter._draw_frame_by_rect_(
            rect=base_rect,
            border_color=bdr_color,
            background_color=bkg_color,
            border_radius=0,
            offset=offset,
        )
        # icon frame
        if self._icon_frame_draw_enable is True:
            if self._get_has_icons_() or self._check_is_enable is True:
                painter._draw_frame_by_rect_(
                    self._icon_frame_draw_rect,
                    border_color=gui_qt_core.QtBorderColors.Transparent,
                    background_color=self._frame_background_color,
                    offset=offset
                )
        # name frame
        if self._name_frame_draw_enable is True:
            if self._get_has_names_():
                painter._draw_frame_by_rect_(
                    self._name_frame_draw_rect,
                    border_color=gui_qt_core.QtBorderColors.Transparent,
                    background_color=self._frame_background_color,
                    offset=offset
                )
        #
        if self._image_frame_draw_enable is True:
            if self._get_has_image_():
                painter._draw_frame_by_rect_(
                    self._image_frame_rect,
                    border_color=gui_qt_core.QtBorderColors.Transparent,
                    background_color=self._frame_background_color,
                    offset=offset
                )
        # check icon
        if self._check_is_enable is True:
            painter._draw_icon_file_by_rect_(
                rect=self._check_icon_draw_rect,
                file_path=self._check_icon_file_path_current,
                offset=offset,
                # frame_rect=self._check_icon_frame_draw_rect,
                is_hovered=self._check_is_hovered
            )
        # icons
        if self._get_has_icons_() is True:
            icon_indices = self._get_icon_indices_()
            if icon_indices:
                icon_pixmaps = self._get_icons_as_pixmap_()
                if icon_pixmaps:
                    for icon_index in icon_indices:
                        painter._set_pixmap_draw_by_rect_(
                            self._get_icon_rect_at_(icon_index),
                            self._get_icon_as_pixmap_at_(icon_index),
                            offset=offset
                        )
                else:
                    icon_file_paths = self._get_icon_file_paths_()
                    if icon_file_paths:
                        for icon_index in icon_indices:
                            painter._draw_icon_file_by_rect_(
                                self._get_icon_rect_at_(icon_index),
                                self._get_icon_file_path_at_(icon_index),
                                offset=offset,
                                is_hovered=self._check_is_hovered
                            )
        # icon
        if self._icon_is_enable is True:
            if self._icon_text:
                painter._draw_frame_color_with_name_text_by_rect_(
                    rect=self._name_frame_draw_rect,
                    text=self._icon_text,
                    offset=offset,
                )
        # name
        if self._get_has_names_() is True:
            name_indices = self._get_name_indices_()
            if name_indices:
                text_option = self._name_text_option
                name_text_dict = self._get_name_text_dict_()
                if name_text_dict:
                    painter.setFont(gui_qt_core.QtFonts.Default)
                    key_text_width = gui_qt_core.GuiQtText.get_draw_width_maximum(
                        painter, self._name_text_dict.keys()
                    )
                    if self._list_widget._get_is_grid_mode_():
                        if self._names_draw_range is not None:
                            key_text_width = gui_qt_core.GuiQtText.get_draw_width_maximum(
                                painter,
                                self._name_text_dict.keys()[self._names_draw_range[0]:self._names_draw_range[1]]
                            )
                    #
                    for i_name_index, (i_key, i_value) in enumerate(name_text_dict.items()):
                        painter._set_text_draw_by_rect_use_key_value_(
                            rect=self._get_name_rect_at_(i_name_index),
                            key_text=i_key,
                            value_text=i_value,
                            key_text_width=key_text_width,
                            offset=offset,
                            is_hovered=self._is_hovered,
                            is_selected=self._is_selected
                        )
                else:
                    for i_name_index in name_indices:
                        painter._draw_text_by_rect_(
                            rect=self._get_name_rect_at_(i_name_index),
                            text=self._get_name_text_at_(i_name_index),
                            font=gui_qt_core.QtFonts.Default,
                            text_option=text_option,
                            word_warp=self._name_word_warp,
                            offset=offset,
                            is_hovered=self._is_hovered,
                            is_selected=self._is_selected
                        )
        # image
        if self._get_has_image_() is True:
            if self._image_pixmap:
                painter._draw_pixmap_by_rect_(
                    rect=self._image_draw_rect,
                    pixmap=self._image_pixmap,
                    offset=offset,
                )
            # draw by image file
            elif self._image_file_path:
                painter._draw_image_use_file_path_by_rect_(
                    rect=self._image_draw_rect,
                    file_path=self._image_file_path,
                    offset=offset
                )
            # draw image by text
            elif self._image_text:
                painter._draw_image_use_text_by_rect_(
                    rect=self._image_draw_rect,
                    text=self._image_text,
                    border_radius=4,
                    offset=offset,
                    border_color=gui_qt_core.QtBorderColors.Icon,
                    border_width=2
                )
            #
            if self._image_sub_file_path:
                painter._draw_image_use_file_path_by_rect_(
                    rect=self._image_sub_draw_rect,
                    file_path=self._image_sub_file_path,
                    offset=offset,
                    #
                    draw_frame=True,
                    background_color=gui_qt_core.QtBorderColors.Icon,
                    border_color=gui_qt_core.QtBorderColors.Icon,
                    border_radius=4
                )
            #
        # play button
        if self._get_play_draw_is_enable_() is True:
            painter._set_movie_play_button_draw_by_rect_(
                self._movie_rect,
                offset=offset,
                is_hovered=self._is_hovered,
                is_selected=self._is_selected,
                is_actioned=self._get_is_actioned_()
            )
        # index
        if self._index_draw_enable is True:
            painter._draw_index_by_rect_(
                rect=self._rect_frame_draw,
                text=self._index_text,
                offset=offset,
            )
        #
        if item._item_show_image_status in [item.ShowStatus.Loading, item.ShowStatus.Waiting]:
            painter._draw_loading_by_rect_(
                rect=self._image_frame_rect,
                loading_index=item._item_show_image_loading_index
            )

    @classmethod
    def _create_mine_data_(cls, urls):
        mime_data = QtCore.QMimeData()
        mime_data.setUrls(
            [QtCore.QUrl.fromLocalFile(i) for i in urls]
        )
        return mime_data

    def _do_hover_move_(self, event):
        p = event.pos()
        self._check_is_hovered = False
        self._press_is_hovered = False
        if self._check_action_is_enable is True:
            if self._check_rect.contains(p):
                self._check_is_hovered = True
            else:
                self._press_is_hovered = True
        else:
            self._press_is_hovered = True
        #
        self._refresh_widget_draw_()

    def _get_action_check_is_valid_(self, event):
        if self._check_action_is_enable is True:
            p = event.pos()
            return self._check_rect.contains(p)
        return False

    def _set_drag_enable_(self, boolean):
        super(QtListItemWidget, self)._set_drag_enable_(boolean)
        self.setAcceptDrops(True)

    # noinspection PyUnusedLocal
    def _do_drag_pressed_(self, *args, **kwargs):
        self.drag_pressed.emit(
            args[0]
        )

    # noinspection PyUnusedLocal
    def _drag_release_cbk_(self, *args, **kwargs):
        self._get_view_()._clear_selection_()
        self._get_view_()._set_current_item_(self._get_item_())
        self.drag_released.emit(
            args[0]
        )

    def _set_action_hovered_(self, boolean):
        if boolean is True:
            self._check_is_hovered = True
        else:
            self._check_is_hovered = False
            self._press_is_hovered = False
        #
        self._refresh_widget_draw_()

    def _set_frame_icon_size_(self, w, h):
        self._frame_icon_width, self._frame_icon_height = w, h

    def _set_frame_image_size_(self, w, h):
        self._frame_image_width, self._frame_image_height = w, h

    def _set_frame_name_size_(self, w, h):
        self._frame_name_width, self._frame_name_height = w, h

    def _set_view_(self, widget):
        self._list_widget = widget

    def _get_view_(self):
        return self._list_widget

    def _set_sort_number_key_(self, value):
        self._sort_number_key = value
        if self._get_view_()._get_sort_mode_() == gui_core.GuiSortMode.Number:
            self._get_item_().setText(str(value).zfill(4))

    def _set_sort_name_key_(self, value):
        self._sort_name_key = value
        if self._get_view_()._get_sort_mode_() == gui_core.GuiSortMode.Name:
            if isinstance(value, six.text_type):
                value = value.encode('utf-8')
            #
            self._get_item_().setText(str(value))

    def __str__(self):
        return '{}(names={})'.format(
            self.__class__.__name__,
            ', '.join(map(lambda x: '"{}"'.format(x), self._get_name_texts_()))
        )

    def __repr__(self):
        return self.__str__()
