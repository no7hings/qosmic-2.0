# coding=utf-8
# qt
from ...core.wrap import *

from ... import core as _qt_core

from ... import abstracts as _qt_abstracts

from ..base import sbj as _bsc_sbj


class AbsQtNGDrawNodeDef(object):
    def _set_ng_draw_node_def_init_(self, widget):
        self._widget = widget


class QtGeneralNode(
    QtWidgets.QWidget,
    #
    _qt_abstracts.AbsQtFrameBaseDef,
    _qt_abstracts.AbsQtTypeDef,
    _qt_abstracts.AbsQtNameBaseDef,
    _qt_abstracts.AbsQtIconBaseDef,
    _qt_abstracts.AbsQtImageBaseDef,
    _qt_abstracts.AbsQtMenuBaseDef,
    #
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForPressDef,
    _qt_abstracts.AbsQtActionForSelectDef,
    #
    _bsc_sbj.AbsQtBypassDef,
    _bsc_sbj.AbsQtNodeDef,
    AbsQtNGDrawNodeDef,
):
    def __init__(self, *args, **kwargs):
        super(QtGeneralNode, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        self._init_frame_base_def_(self)
        self._init_type_base_def_(self)
        self._init_name_base_def_(self)
        self._init_icon_base_def_(self)
        self._init_image_base_def_(self)
        self._init_menu_base_def_(self)

        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)
        self._init_action_for_select_def_(self)

        self._init_node_def_(self)
        self._set_ng_draw_node_def_init_(self)

        self.installEventFilter(self)

    def _refresh_widget_all_(self):
        self._update_node_geometry_properties_()
        self._update_node_geometry_()
        self._update_node_draw_properties_()

        self._refresh_widget_draw_geometry_()

        self._update_node_attachments_()

        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        rect = self.rect()
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()

        self._set_frame_draw_rect_(x, y, w, h)

        b_w_0 = self._ng_draw_border_w

        c_i_r = self._ng_draw_input_r
        c_o_r = self._ng_draw_output_r

        x_0, y_0 = x+b_w_0/2, y+b_w_0/2
        w_0, h_0 = w-b_w_0, h-b_w_0

        # select
        self._node_selection_rect.setRect(
            x_0, y_0, w_0, h_0
        )

        # name
        n_x, n_y = x_0+c_i_r/2, y_0
        n_w, n_h = w_0-c_i_r, self._ng_draw_name_h
        self._name_draw_rect.setRect(
            n_x, n_y, n_w, n_h
        )

        # frame
        f_x, f_y = x_0+c_i_r/2, y_0+n_h
        f_w, f_h = w_0-c_i_r, h_0-n_h
        self._node_rect_frame.setRect(
            f_x, f_y, f_w, f_h
        )
        f_h_x, f_h_y = f_x, f_y
        f_h_w, f_h_h = f_w, self._ng_draw_head_h
        self._head_frame_rect.setRect(
            f_h_x, f_h_y, f_h_w, f_h_h
        )

        # icon & button
        i_w, i_h = self._ng_draw_icon_w, self._ng_draw_icon_h
        self._icon_text_draw_rect.setRect(
            f_x+(f_h_h-i_h)/2, f_y+(f_h_h-i_h)/2, i_w, i_h
        )

        # button
        b_w, b_h = self._ng_draw_button_w, self._ng_draw_button_h
        s_x = f_x+f_h_h
        self._ng_node_resize_rect.setRect(
            s_x+(f_h_h-i_h)/2, f_y+(f_h_h-i_h)/2, b_w, b_h
        )

        # frame body
        f_b_x, f_b_y = f_x, f_y+f_h_h
        f_b_w, f_b_h = f_w, f_h-f_h_h
        self._body_frame_rect.setRect(
            f_b_x, f_b_y, f_b_w, f_b_h
        )

        i_x_2, i_y_2 = x_0, f_b_y

        self._node_intput_rect.setRect(
            i_x_2, i_y_2+(f_b_h-c_i_r)/2, c_i_r, c_i_r
        )
        self._node_output_rect.setRect(
            w-b_w_0/2-c_o_r, i_y_2+(f_b_h-c_o_r)/2, c_o_r, c_o_r
        )

    def _do_hover_move_(self, event):
        point = event.pos()
        if self._node_selection_rect.contains(point):
            self._set_hovered_(True)
        else:
            self._set_hovered_(False)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)

            if event.type() == QtCore.QEvent.Resize:
                pass
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._update_press_click_flag_(event)
                    if self._is_action_flag_match_(
                        self.ActionFlag.NGNodePressClick,
                    ):
                        self._do_press_click_start_(event)
                        self._do_press_move_start_(event)

                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    if not self._graph._is_action_flag_match_(
                        self.ActionFlag.RectSelectMove
                    ):
                        self._update_press_move_flag_(event)
                        if self._graph._is_action_flag_match_(
                                self.ActionFlag.NGNodePressMove,
                        ):
                            self._do_press_click_(event)
                            self._do_press_move_(event)
                elif event.buttons() == QtCore.Qt.RightButton:
                    pass
                elif event.buttons() == QtCore.Qt.MidButton:
                    pass
                elif event.button() == QtCore.Qt.NoButton:
                    self._do_hover_move_(event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._is_action_flag_match_(
                        self.ActionFlag.NGNodePressClick,
                        self.ActionFlag.NGNodePressMove
                    ):
                        self._do_press_click_end_(event)
                        self._do_press_move_end_(event)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
                #
                self._clear_all_action_flags_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtNGPainter(self)

        offset = 0

        painter._draw_node_frame_head_by_rect_(
            self._head_frame_rect,
            border_color=self._type_color,
            border_width=self._ng_draw_border_w,
            border_radius=self._ng_draw_border_w,
            is_hovered=self._is_hovered_(),
            is_selected=self._is_selected,
            is_actioned=self._get_is_actioned_(),
        )

        painter._draw_node_frame_body_by_rect_(
            self._body_frame_rect,
            border_color=self._type_color,
            border_width=self._ng_draw_border_w,
            border_radius=self._ng_draw_border_w,
        )
        #
        painter._set_ng_node_resize_button_draw_(
            self._ng_node_resize_rect,
            border_width=self._ng_draw_border_w,
            mode=1,
            is_current=True,
            is_hovered=False
        )

        painter._set_ng_node_input_draw_(
            self._node_intput_rect,
            border_width=self._ng_draw_border_w,
            offset=offset
        )

        painter._set_ng_node_output_draw_(
            self._node_output_rect,
            border_width=self._ng_draw_border_w,
            offset=offset
        )

        if self._name_text is not None:
            painter._draw_text_by_rect_(
                self._name_draw_rect,
                self._name_text,
                font=_qt_core.QtFont.generate(size=self._ng_draw_font_h),
                text_color=_qt_core.QtRgba.Text,
                text_option=QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter,
                offset=offset
            )

        if self._icon_text is not None:
            painter._draw_image_use_text_by_rect_(
                self._icon_text_draw_rect,
                text=self._icon_text,
                offset=offset,
                border_width=self._ng_draw_border_w,
                border_radius=-1
            )

    def __str__(self):
        return 'Node(name="{}")'.format(
            self._get_name_text_()
        )

    def __repr__(self):
        return self.__str__()
