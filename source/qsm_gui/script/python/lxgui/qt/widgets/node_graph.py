# coding=utf-8
import functools

import os.path

import enum

import collections

import lxbasic.core as bsc_core
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import core as gui_qt_core

from .. import abstracts as gui_qt_abstracts
# qt widgets
from . import utility as gui_qt_wgt_utility

from . import entry as gui_qt_wgt_entry

from . import item_for_tree as gui_qt_wgt_item_for_tree

from . import view_for_tree as gui_qt_wgt_view_for_tree


class _NGLayoutFlag(enum.IntEnum):
    Dependent = 0
    Line = 1


class _NGSelectionFlag(enum.IntEnum):
    Separate = 0
    Add = 1
    Sub = 2
    Invert = 3


class _QtNGLayer(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(_QtNGLayer, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            event.ignore()
        return False


class AbsQtActionRectSelectDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _set_action_rect_select_def_init_(self, widget):
        self._widget = widget

        self._action_rect_select_point_start = QtCore.QPoint(0, 0)
        self._action_rect_select_rect = QtCore.QRect(
            0, 0, 0, 0
        )

    def _set_action_rect_select_start_(self, event):
        self._action_rect_select_point_start = event.pos()

    def _set_action_rect_select_execute_(self, event):
        self._action_rect_select_rect.setTopLeft(
            self._action_rect_select_point_start
        )
        self._action_rect_select_rect.setBottomRight(
            event.pos()
        )
        self._refresh_widget_draw_()

    def _set_action_rect_select_end_(self, event):
        raise NotImplementedError()


class AbsQtActionFrameDef(object):
    def _set_action_frame_def_init_(self, widget):
        pass

    # action frame select
    def _set_action_frame_execute_(self, event):
        raise NotImplementedError()


class AbsQtBypassDef(object):
    def _set_bypass_def_init_(self, widget):
        self._widget = widget

        self._bypass = False

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _set_bypass_(self, boolean):
        self._bypass = boolean

        self._refresh_widget_draw_()


class AbsQtNGUniverseDef(object):
    def _set_ng_universe_def_init_(self):
        self._ng_node_universe = None
        self._ng_node_universe_dict = {}

    def _set_ng_universe_(self, *args, **kwargs):
        raise NotImplementedError()

    def _set_ng_show_by_universe_(self, *args, **kwargs):
        raise NotImplementedError()

    def _set_ng_universe_node_add_(self, *args, **kwargs):
        raise NotImplementedError()


class AbsQtNGDef(object):
    def _set_ng_def_init_(self, widget):
        self._widget = widget


class AbsQtNGGraphDef(object):
    def _set_ng_graph_def_init_(self, widget):
        self._widget = widget

        self._ng_graph_translate_point = QtCore.QPoint(0, 0)
        #
        self._ng_graph_composite_matrix = bsc_core.RawMatrix33Opt.get_identity()
        #
        self._ng_graph_translate_x, self._ng_graph_translate_y = 0, 0
        self._ng_graph_translate_x_enable, self._ng_graph_translate_y_enable = True, True
        #
        self._ng_graph_scale_x, self._ng_graph_scale_y = 1.0, 1.0
        self._ng_graph_scale_minimum_x, self._ng_graph_scale_minimum_y = 0.000001, 0.000001
        self._ng_graph_scale_maximum_x, self._ng_graph_scale_maximum_y = 100000.0, 100000.0
        self._ng_graph_scale_radix_x, self._ng_graph_scale_radix_y = 0.25, 0.25
        #
        self._ng_graph_w_basic, self._ng_graph_h_basic = 512, 512
        #
        self._ng_graph_point_0 = QtCore.QPoint(0, 0)
        self._ng_graph_point_1 = QtCore.QPoint(
            self._ng_graph_w_basic*self._ng_graph_scale_x, self._ng_graph_h_basic*self._ng_graph_scale_y
        )
        self._ng_rect = QtCore.QRect(
            0, 0,
            self._ng_graph_w_basic, self._ng_graph_h_basic
        )

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _refresh_widget_all_(self):
        raise NotImplementedError()

    #
    def _set_ng_graph_transformation_update_(self):
        x_0, y_0, x_1, y_1, r_w, r_h = self._get_ng_graph_rect_args_()
        self._ng_graph_translate_x, self._ng_graph_translate_y = x_0, y_0
        self._ng_graph_scale_x, self._ng_graph_scale_y = (
            r_w/float(self._ng_graph_w_basic), r_h/float(self._ng_graph_h_basic)
        )
        self._ng_rect.setRect(
            x_0, y_0, r_w, r_h
        )

    # action
    def _set_ng_action_graph_translate_start_(self, event):
        self._ng_graph_translate_point = event.pos()
        self._refresh_widget_all_()

    def _set_ng_action_graph_translate_execute_(self, event):
        point = event.pos()
        #
        d_p = point-self._ng_graph_translate_point
        d_t_x, d_t_y = d_p.x(), d_p.y()
        #
        self._set_ng_graph_translate_matrix_(d_t_x, d_t_y)
        self._set_ng_graph_transformation_matrix_update_()
        if point is not None:
            self._ng_graph_translate_point = point
        else:
            self._ng_graph_translate_point = QtCore.QPoint(0, 0)
        #
        self._refresh_widget_all_()

    def _set_ng_action_graph_translate_stop_(self, event):
        self._ng_graph_translate_point = event.pos()
        self._refresh_widget_all_()

    def _set_ng_action_graph_scale_execute_(self, event):
        delta = event.angleDelta().y()
        point = event.pos()
        #
        if delta > 0:
            d_s_x, d_s_y = 1+self._ng_graph_scale_radix_x, 1+self._ng_graph_scale_radix_y
        else:
            d_s_x, d_s_y = 1/(1+self._ng_graph_scale_radix_x), 1/(1+self._ng_graph_scale_radix_y)
        #
        c_x, c_y = point.x(), point.y()
        #
        self._set_ng_graph_scale_matrix_(c_x, c_y, d_s_x, d_s_y)
        self._set_ng_graph_transformation_matrix_update_()
        if point is not None:
            self._ng_graph_translate_point = point
        else:
            self._ng_graph_translate_point = QtCore.QPoint(0, 0)
        #
        self._refresh_widget_all_()

    #
    def _set_ng_graph_points_(self, x_0, y_0, x_1, y_1):
        # print x_0, y_0, x_1, y_1
        # print self._ng_graph_point_0, self._ng_graph_point_1, 'B'
        self._ng_graph_point_0.setX(x_0)
        self._ng_graph_point_0.setY(y_0)
        self._ng_graph_point_1.setX(x_1)
        self._ng_graph_point_1.setY(y_1)
        self._refresh_widget_all_()

    def _get_ng_graph_rect_args_(self):
        o_x_0, o_y_0 = self._ng_graph_point_0.x(), self._ng_graph_point_0.y()
        o_x_1, o_y_1 = self._ng_graph_point_1.x(), self._ng_graph_point_1.y()
        o_r_w, o_r_h = o_x_1-o_x_0, o_y_1-o_y_0
        return o_x_0, o_y_0, o_x_1, o_y_1, o_r_w, o_r_h

    def _set_ng_graph_translate_to_(self, x, y):
        o_x_0, o_y_0, o_x_1, o_y_1, o_r_w, o_r_h = self._get_ng_graph_rect_args_()
        x_0, y_0 = x, y
        x_1, y_1 = x+o_r_w, y+o_r_h
        self._set_ng_graph_points_(x_0, y_0, x_1, y_1)

    def _set_ng_graph_scale_to_(self, s_x, s_y):
        o_x_0, o_y_0 = self._ng_graph_translate_x, self._ng_graph_translate_y
        x_0, y_0 = o_x_0, o_y_0
        x_1, y_1 = o_x_0+self._ng_graph_w_basic*s_x, o_y_0+self._ng_graph_h_basic*s_y
        self._set_ng_graph_points_(x_0, y_0, x_1, y_1)

    def _get_ng_graph_translate_(self):
        return self._ng_graph_translate_x, self._ng_graph_translate_y

    #
    def _get_ng_graph_scale_(self):
        return self._ng_graph_scale_x, self._ng_graph_scale_y

    #
    def _set_ng_graph_translate_matrix_(self, d_t_x, d_t_y):
        m = self._ng_graph_composite_matrix
        #
        m_t = bsc_core.RawMatrix33Opt.get_default()
        m_t = bsc_core.RawMatrix33Opt.identity_to(m_t)
        #
        m_t[0][2] = d_t_x
        m_t[1][2] = d_t_y
        #
        self._ng_graph_composite_matrix = bsc_core.RawMatrix33Opt(m_t).multiply_to(m)

    #
    def _set_ng_graph_scale_matrix_(self, c_x, c_y, d_s_x, d_s_y):
        m = self._ng_graph_composite_matrix
        #
        s_m = bsc_core.RawMatrix33Opt.get_default()
        s_m = bsc_core.RawMatrix33Opt.identity_to(s_m)
        #
        s_m[0][0] = d_s_x
        s_m[0][2] = (1-d_s_x)*c_x
        #
        s_m[1][1] = d_s_y
        s_m[1][2] = (1-d_s_y)*c_y
        #
        self._ng_graph_composite_matrix = bsc_core.RawMatrix33Opt(s_m).multiply_to(m)

    #
    def _set_ng_graph_transformation_matrix_update_(self):
        m = self._ng_graph_composite_matrix
        #
        self.__set_ng_graph_point_update_bt_matrix_(
            self._ng_graph_point_0, m
        )
        #
        self.__set_ng_graph_point_update_bt_matrix_(
            self._ng_graph_point_1, m
        )
        #
        self._ng_graph_composite_matrix = bsc_core.RawMatrix33Opt.identity_to(m)

    @staticmethod
    def __set_ng_graph_point_update_bt_matrix_(point, matrix):
        i_x_0, i_y_0 = point.x(), point.y()
        i_x_0_, i_y_0_ = (
            matrix[0][0]*i_x_0+matrix[0][1]*i_y_0+matrix[0][2],
            matrix[1][0]*i_x_0+matrix[1][1]*i_y_0+matrix[1][2]
        )
        point.setX(i_x_0_)
        point.setY(i_y_0_)


class AbsQtNGDrawGraphDef(object):
    def _set_ng_draw_graph_def_init_(self, widget):
        self._widget = widget

        self._ng_draw_graph_grid_enable = True
        self._ng_draw_graph_grid_mark_enable = True
        self._ng_draw_graph_grid_axis_enable = True

        #
        self._ng_draw_graph_grid_translate_direction_x, self._ng_draw_graph_grid_translate_direction_y = 1, 1
        self._ng_draw_graph_grid_translate_x, self._ng_draw_graph_grid_translate_y = 0, 0

    def _set_ng_draw_graph_update_(self, t_x, t_y):
        self._ng_draw_graph_grid_translate_x, self._ng_draw_graph_grid_translate_y = (
            t_x*self._ng_draw_graph_grid_translate_direction_x, t_y*self._ng_draw_graph_grid_translate_direction_y
        )


class AbsQtNGGraphSbjDef(object):
    NG_NODE_CLS = None
    NG_CONNECTION_CLS = None

    def _set_ng_graph_sbj_def_init_(self, widget):
        self._widget = widget

        self._ng_graph_nodes = []
        self._ng_graph_nodes_selected = []
        #
        self._ng_graph_connections = []
        self._ng_graph_connections_selected = []

        self._ng_graph_node_current = None

        self._ng_graph_selection_flag = _NGSelectionFlag.Separate

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _set_ng_graph_sbj_node_create_(self, *args, **kwargs):
        raise NotImplementedError()

    def _set_ng_graph_sbj_connection_create_(self, *args, **kwargs):
        raise NotImplementedError()

    def _get_ng_graph_nodes_(self):
        return self._ng_graph_nodes

    def _get_ng_graph_node_select_count_(self):
        return len(self._ng_graph_nodes_selected)

    def _get_ng_graph_nodes_select_(self):
        return self._ng_graph_nodes_selected

    def _set_ng_graph_nodes_update_(self):
        for i_ng_node in self._get_ng_graph_nodes_():
            i_ng_node._refresh_widget_all_()

    def _set_ng_graph_clear_(self):
        pass

    def _set_ng_graph_frame_to_nodes_(self, *args):
        raise NotImplementedError()

    def _set_ng_graph_node_current_(self, sbj):
        self._ng_graph_node_current = sbj
        if sbj is not None:
            self._ng_graph_node_current.raise_()
        #
        self._refresh_widget_draw_()

    def _get_ng_graph_node_current_name_text_(self):
        if self._ng_graph_node_current is not None:
            return self._ng_graph_node_current._get_name_text_()

    def _set_ng_graph_node_select_clear_(self):
        for i in self._ng_graph_nodes_selected:
            i._set_selected_(False)

        self._ng_graph_nodes_selected = []
        self._ng_graph_node_current = None

    def _set_ng_graph_nodes_transformation_(self, t_x, t_y, s_x, s_y):
        [i._set_ng_node_transformation_(t_x, t_y, s_x, s_y) for i in self._ng_graph_nodes]

    def _get_ng_action_graph_selection_flag_(self):
        pass

    # action press
    def _set_ng_action_graph_node_press_start_(self, sbj):
        self._ng_graph_selection_flag = self._get_ng_action_graph_selection_flag_()
        self._set_ng_graph_node_current_(sbj)

    def _set_ng_action_graph_node_press_execute_(self, sbj):
        if self._get_ng_graph_node_select_count_() == 0:
            self._set_ng_action_graph_select_as_separate_(sbj)

    def _set_ng_action_graph_node_press_end_(self, sbj):
        raise NotImplementedError()

    def _set_ng_graph_node_move_execute_(self, *args, **kwargs):
        raise NotImplementedError()

    def _set_ng_action_graph_select_as_separate_(self, sbj):
        raise NotImplementedError()


# sub object def
class AbsQtNGSbjDef(object):
    def _set_ng_sbj_def_init_(self, widget):
        self._widget = widget
        #
        self._ng_draw_font_h_basic = 10
        self._ng_draw_border_w_basic = 2
        self._ng_draw_connection_r_basic = 1
        self._ng_draw_input_r_basic = 10
        self._ng_draw_output_r_basic = 12
        self._ng_draw_name_h_basic = 24
        self._ng_draw_head_h_basic = 24
        self._ng_draw_icon_w_basic, self._ng_draw_icon_h_basic = 16, 16
        self._ng_draw_button_w_basic, self._ng_draw_button_h_basic = 16, 16
        #
        self._ng_draw_font_h = 10
        self._ng_draw_border_w = 2
        self._ng_draw_connection_r = 1
        self._ng_draw_input_r = 10
        self._ng_draw_output_r = 12
        self._ng_draw_name_h = 24
        self._ng_draw_head_h = 24
        self._ng_draw_icon_w, self._ng_draw_icon_h = 16, 16
        self._ng_draw_button_w, self._ng_draw_button_h = 16, 16

        self._ng_sbj_graph = None

    def _set_ng_sbj_graph_(self, widget):
        self._ng_sbj_graph = widget

    def _get_ng_sbj_scale_(self):
        return self._ng_sbj_graph._get_ng_graph_scale_()

    def _set_ng_action_sbj_flag_(self, flag):
        self._ng_sbj_graph._set_action_flag_(flag)

    def _get_ng_action_sbj_flag_is_match_(self, *args):
        return self._ng_sbj_graph._get_action_flag_is_match_(*args)

    def _get_ng_sbj_mdf_flags_is_include_(self, flag):
        return self._ng_sbj_graph._get_action_mdf_flags_is_include_(flag)

    def _get_ng_sbj_mdf_flags_(self):
        return self._ng_sbj_graph._get_action_mdf_flags_()

    def _set_ng_sbj_update_draw_(self):
        s_x, s_y = self._get_ng_sbj_scale_()
        #
        self._ng_draw_border_w = self._ng_draw_border_w_basic*s_y
        self._ng_draw_connection_r = self._ng_draw_connection_r_basic*s_y
        self._ng_draw_input_r = self._ng_draw_input_r_basic*s_y
        self._ng_draw_output_r = self._ng_draw_output_r_basic*s_y
        self._ng_draw_font_h = self._ng_draw_font_h_basic*s_y
        self._ng_draw_font_h = max(self._ng_draw_font_h, 1)
        self._ng_draw_name_h = self._ng_draw_name_h_basic*s_y
        self._ng_draw_head_h = self._ng_draw_head_h_basic*s_y
        self._ng_draw_icon_w, self._ng_draw_icon_h = self._ng_draw_icon_w_basic*s_x, self._ng_draw_icon_h_basic*s_y
        self._ng_draw_button_w, self._ng_draw_button_h = self._ng_draw_button_w_basic*s_x, self._ng_draw_button_h_basic*s_y

    def _get_undo_stack_(self):
        return self._ng_sbj_graph._undo_stack

    def _get_ng_graph_(self):
        return self._ng_sbj_graph


class AbsQtNGConnectionDef(AbsQtNGSbjDef):
    def _set_ng_connection_def_init_(self, widget):
        self._widget = widget

        self._set_ng_sbj_def_init_(widget)

        self._ng_connection_point_start = QtCore.QPoint(0, 0)
        self._ng_connection_point_end = QtCore.QPoint(0, 0)

        self._ng_connection_dir = 0
        self._ng_draw_connection_dir = 0

        self._ng_draw_connection_point_start = QtCore.QPoint(0, 0)
        self._ng_draw_connection_point_end = QtCore.QPoint(0, 0)

        self._ng_draw_connection_path_curve = QtGui.QPainterPath()
        self._ng_draw_connection_coord_arrow = []
        self._ng_draw_connection_point = QtCore.QPoint()

    def _refresh_widget_all_(self):
        raise NotImplementedError()

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _set_wgt_update_shape_(self):
        b_w = self._ng_draw_border_w
        #
        x_0, y_0 = self._ng_connection_point_start.x(), self._ng_connection_point_start.y()
        x_1, y_1 = self._ng_connection_point_end.x(), self._ng_connection_point_end.y()
        #
        x, y = min(x_1, x_0), min(y_1, y_0)
        #
        width, height = abs(x_0-x_1), abs(y_0-y_1)
        #
        self._widget.setGeometry(
            x-b_w*2, y-b_w*2,
            width+b_w*4, height+b_w*4
        )
        #
        if x_1 < x_0 and y_1 > y_0:
            self._ng_connection_dir = 1
        elif x_1 > x_0 and y_1 < y_0:
            self._ng_connection_dir = 1
        else:
            self._ng_connection_dir = 0
        #
        if x_1 < x_0:
            self._ng_draw_connection_dir = 1
        else:
            self._ng_draw_connection_dir = 0

    def _set_ng_connection_point_start_(self, point):
        self._ng_connection_point_start.setX(point.x())
        self._ng_connection_point_start.setY(point.y())

    def _set_ng_connection_point_end_(self, point):
        self._ng_connection_point_end.setX(point.x())
        self._ng_connection_point_end.setY(point.y())


class _QtNGConnection(
    QtWidgets.QWidget,
    AbsQtNGConnectionDef,
    #
    gui_qt_abstracts.AbsQtActionBaseDef,
    gui_qt_abstracts.AbsQtActionForHoverDef,
    gui_qt_abstracts.AbsQtActionForPressDef,
    #
    gui_qt_abstracts.AbsQtPressSelectExtraDef,
):
    def _refresh_widget_all_(self):
        self._set_wgt_update_shape_()
        self._set_ng_sbj_update_draw_()
        self._refresh_widget_draw_geometry_(self.rect())
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self, rect):
        def add_cubic_fnc_(p_0, p_1, index):
            c1, c2 = (
                QtCore.QPointF((p_0.x()+p_1.x())/index, p_0.y()),
                QtCore.QPointF((p_0.x()+p_1.x())/index, p_1.y())
            )
            path.cubicTo(c1, c2, p_1)
            path.lineTo(p_1)
            path.cubicTo(c2, c1, p_0)

        #
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        #
        b_w = self._ng_draw_border_w
        #
        if self._ng_connection_dir == 0:
            self._ng_draw_connection_point_start.setX(x+b_w*2)
            self._ng_draw_connection_point_start.setY(y+b_w*2)
            #
            self._ng_draw_connection_point_end.setX(x+w-b_w*4)
            self._ng_draw_connection_point_end.setY(y+h-b_w*2)
        else:
            self._ng_draw_connection_point_start.setX(x+b_w*2)
            self._ng_draw_connection_point_start.setY(y+h-b_w*2)
            #
            self._ng_draw_connection_point_end.setX(x+w-b_w*2)
            self._ng_draw_connection_point_end.setY(y+b_w*2)
        #
        path = QtGui.QPainterPath(self._ng_draw_connection_point_start)
        #
        self._ng_draw_connection_path_curve = path
        #
        add_cubic_fnc_(
            self._ng_draw_connection_point_start,
            self._ng_draw_connection_point_end,
            [2, 1][self._ng_draw_connection_dir]
        )
        #
        p = self._ng_draw_connection_path_curve.pointAtPercent(0.25)
        a = self._ng_draw_connection_path_curve.angleAtPercent(0.25)
        if self._ng_draw_connection_dir == 1:
            a += 180
        r_ = self._ng_draw_border_w*4
        x_, y_ = p.x(), p.y()
        self._ng_draw_connection_coord_arrow = [
            gui_core.GuiEllipse2d.get_coord_at_angle_(center=(x_, y_), radius=r_, angle=90+a),
            gui_core.GuiEllipse2d.get_coord_at_angle_(center=(x_, y_), radius=r_, angle=210+a),
            gui_core.GuiEllipse2d.get_coord_at_angle_(center=(x_, y_), radius=r_, angle=330+a),
            gui_core.GuiEllipse2d.get_coord_at_angle_(center=(x_, y_), radius=r_, angle=90+a)
        ]
        self._ng_draw_connection_point = p

    def _get_ng_draw_connection_background_color_(self, start_point, end_point, draw_dir, is_selected, is_hovered):
        if is_hovered:
            start_color = end_color = QtGui.QColor(63, 255, 255, 255)
        else:
            if is_selected is True:
                start_color = end_color = QtGui.QColor(255, 127, 0, 255)
            else:
                if draw_dir == 1:
                    start_color = QtGui.QColor(63, 255, 127, 255)
                    end_color = QtGui.QColor(255, 63, 31, 255)
                else:
                    start_color = QtGui.QColor(255, 63, 31, 255)
                    end_color = QtGui.QColor(63, 255, 127, 255)
        #
        gradient = QtGui.QLinearGradient(start_point, end_point)
        gradient.setColorAt(0, start_color)
        gradient.setColorAt(1, end_color)
        brush = QtGui.QBrush(gradient)
        pen = QtGui.QPen(brush, self._ng_draw_connection_r)
        pen.setJoinStyle(QtCore.Qt.RoundJoin)
        return pen, brush

    def __init__(self, *args, **kwargs):
        super(_QtNGConnection, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)
        self._init_press_select_extra_def_(self)

        self._set_ng_connection_def_init_(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    pass
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    pass
                elif event.buttons() == QtCore.Qt.RightButton:
                    pass
                elif event.buttons() == QtCore.Qt.MidButton:
                    pass
                elif event.buttons() == QtCore.Qt.NoButton:
                    self._do_hover_move_(event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    pass
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
        return False

    def paintEvent(self, event):
        painter = gui_qt_core.QtNGPainter(self)

        painter.setRenderHints(
            painter.Antialiasing
        )
        #
        pen, brush = self._get_ng_draw_connection_background_color_(
            self._ng_draw_connection_point_start, self._ng_draw_connection_point_end,
            self._ng_draw_connection_dir,
            False, False
        )
        #
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawPath(
            self._ng_draw_connection_path_curve
        )
        painter._draw_path_by_coords_(
            self._ng_draw_connection_coord_arrow
        )

    def _do_hover_move_(self, event):
        _point = event.pos()


class AbsQtNGNodeDef(AbsQtNGSbjDef):
    def _set_ng_node_def_init_(self, widget):
        self._widget = widget

        self._set_ng_sbj_def_init_(widget)

        self._ng_node_obj = None

        self._ng_action_node_move_point_start = QtCore.QPoint(0, 0)

        self._ng_node_translate_x, self._ng_node_translate_y = 0, 0
        self._ng_node_scale_x, self._ng_node_scale_y = 1.0, 1.0
        #
        self._ng_node_x_glb, self._ng_node_y_glb = 0.0, 0.0
        self._ng_node_x_glb_orig, self._ng_node_y_glb_orig = 0, 0

        self._ng_node_w_basic, self._ng_node_h_basic = 192, 80

        self._ng_node_rect = QtCore.QRect(0, 0, 0, 0)
        self._ng_node_rect_select_glb = QtCore.QRect(0, 0, 0, 0)
        self._ng_node_rect_select = QtCore.QRect(0, 0, 0, 0)
        self._ng_node_rect_frame = QtCore.QRect(0, 0, 0, 0)
        self._ng_node_rect_frame_head = QtCore.QRect(0, 0, 0, 0)
        self._ng_node_rect_frame_body = QtCore.QRect(0, 0, 0, 0)

        self._ng_node_rect_input = QtCore.QRect(0, 0, 0, 0)
        self._ng_node_rect_output = QtCore.QRect(0, 0, 0, 0)

        self._ng_node_connection_starts = []
        self._ng_node_connection_ends = []

        self._ng_node_resize_rect = QtCore.QRect(0, 0, 0, 0)

    def _set_ng_node_size_basic_(self, w, h):
        self._ng_node_w_basic, self._ng_node_h_basic = w, h

    def _get_ng_node_size_basic_(self):
        return self._ng_node_w_basic, self._ng_node_h_basic

    def _refresh_widget_all_(self):
        raise NotImplementedError()

    def _set_wgt_update_shape_(self):
        self._widget.setGeometry(
            self._ng_node_rect
        )

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _refresh_widget_draw_geometry_(self, rect):
        raise NotImplementedError()

    def _set_ng_node_connection_update_(self):
        p = self._ng_node_rect_output.center()
        p = self._widget.mapToParent(p)
        for i in self._ng_node_connection_starts:
            i._set_ng_connection_point_start_(
                p
            )
            i._refresh_widget_all_()
        p = self._ng_node_rect_input.center()
        p = self._widget.mapToParent(p)
        for i in self._ng_node_connection_ends:
            i._set_ng_connection_point_end_(
                p
            )
            i._refresh_widget_all_()

    def _set_ng_node_update_(self):
        x, y, w, h = self._get_ng_node_geometry_by_transformation_()
        self._ng_node_rect.setRect(
            x, y,
            w, h
        )
        x_1, y_1 = self._ng_node_rect_select.x(), self._ng_node_rect_select.y()
        w_1, h_1 = self._ng_node_rect_select.width(), self._ng_node_rect_select.height()

        self._ng_node_rect_select_glb.setRect(
            x+x_1, y+y_1,
            w_1, h_1
        )

    def _set_ng_node_transformation_(self, t_x, t_y, s_x, s_y):
        self._ng_node_translate_x, self._ng_node_translate_y = t_x, t_y
        self._ng_node_scale_x, self._ng_node_scale_y = s_x, s_y

    def _get_ng_node_translate_(self):
        return self._ng_node_translate_x, self._ng_node_translate_y

    def _get_ng_node_scale_(self):
        return self._ng_node_scale_x, self._ng_node_scale_y

    def _get_ng_node_transformation_(self):
        return self._ng_node_translate_x, self._ng_node_translate_y, self._ng_node_scale_x, self._ng_node_scale_y

    def _get_ng_node_coord_glb_update_(self, x, y):
        t_x, t_y, s_x, s_y = self._get_ng_node_transformation_()
        #
        x, y = (x-t_x)/s_x, (y-t_y)/s_y
        self._ng_node_x_glb, self._ng_node_y_glb = x, y

    def _get_ng_node_geometry_by_transformation_(self):
        t_x, t_y, s_x, s_y = self._get_ng_node_transformation_()
        return self._ng_node_x_glb*s_x+t_x, self._ng_node_y_glb*s_y+t_y, self._ng_node_w_basic*s_x, self._ng_node_h_basic*s_y

    def _get_ng_node_geometry_(self):
        p = self._widget.pos()
        rect = self._widget.rect()
        return p.x(), p.y(), rect.width(), rect.height()

    def _set_ng_node_obj_(self, obj):
        self._ng_node_obj = obj

    def _set_ng_action_node_press_start_(self, event):
        raise NotImplementedError()

    def _set_ng_action_node_press_execute_(self, event):
        raise NotImplementedError()

    def _set_ng_action_node_press_end_(self, event):
        raise NotImplementedError()

    def _set_ng_action_node_press_move_start_(self, event):
        self._ng_action_node_move_point_start = event.globalPos()-self._widget.pos()
        #
        self._set_ng_node_coord_glb_orig_update_()
        self._get_ng_graph_()._set_ng_graph_node_move_start_()

    def _set_ng_action_node_press_move_execute_(self, event):
        raise NotImplementedError()

    # noinspection PyUnusedLocal
    def _set_ng_action_node_press_move_stop_(self, event):
        self._get_ng_graph_()._set_ng_graph_node_move_stop_()

    def _set_ng_node_update_by_pos_(self, d_point, offset_point=None):
        if offset_point is not None:
            d_point = d_point-offset_point
            x, y = d_point.x(), d_point.y()
            self._set_ng_node_move_by_coord_(x, y)
        else:
            x, y = d_point.x(), d_point.y()
            self._set_ng_node_move_by_coord_(x, y)

    def _set_ng_node_move_by_coord_(self, x, y):
        self._widget.move(x, y)
        self._get_ng_node_coord_glb_update_(x, y)
        self._set_ng_node_update_()
        self._set_ng_node_connection_update_()

    # global coord
    def _set_ng_node_coord_glb_(self, x, y):
        self._ng_node_x_glb, self._ng_node_y_glb = x, y
        self._refresh_widget_all_()

    def _get_ng_node_coord_glb_(self):
        return self._ng_node_x_glb, self._ng_node_y_glb

    def _get_ng_node_coord_glb_orig_(self):
        return self._ng_node_x_glb_orig, self._ng_node_y_glb_orig

    def _set_ng_node_coord_glb_orig_update_(self):
        self._ng_node_x_glb_orig, self._ng_node_y_glb_orig = self._ng_node_x_glb, self._ng_node_y_glb

    def _set_ng_node_connection_start_add_(self, connection):
        self._ng_node_connection_starts.append(connection)

    def _set_ng_node_connection_end_add_(self, connection):
        self._ng_node_connection_ends.append(connection)


class AbsQtNGDrawNodeDef(object):
    def _set_ng_draw_node_def_init_(self, widget):
        self._widget = widget


class _QtNGNode(
    QtWidgets.QWidget,
    #
    gui_qt_abstracts.AbsQtFrameBaseDef,
    gui_qt_abstracts.AbsQtTypeDef,
    gui_qt_abstracts.AbsQtNameBaseDef,
    gui_qt_abstracts.AbsQtIconBaseDef,
    gui_qt_abstracts.AbsQtImageBaseDef,
    gui_qt_abstracts.AbsQtMenuBaseDef,
    #
    AbsQtBypassDef,
    #
    gui_qt_abstracts.AbsQtActionBaseDef,
    gui_qt_abstracts.AbsQtActionForHoverDef,
    gui_qt_abstracts.AbsQtActionForPressDef,
    #
    gui_qt_abstracts.AbsQtPressSelectExtraDef,
    #
    AbsQtNGNodeDef,
    AbsQtNGDrawNodeDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtNGNode, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
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
        self._init_image_base_def_()
        self._init_menu_base_def_(self)
        #
        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)
        self._init_press_select_extra_def_(self)

        self._set_ng_node_def_init_(self)
        self._set_ng_draw_node_def_init_(self)

    def _refresh_widget_all_(self):
        self._set_ng_node_update_()
        self._set_wgt_update_shape_()
        self._set_ng_sbj_update_draw_()
        #
        self._refresh_widget_draw_geometry_(self.rect())
        #
        self._set_ng_node_connection_update_()
        #
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self, rect):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()

        self._set_frame_draw_rect_(x, y, w, h)

        b_w_0 = self._ng_draw_border_w

        c_i_r = self._ng_draw_input_r
        c_o_r = self._ng_draw_output_r

        x_0, y_0 = x+b_w_0/2, y+b_w_0/2
        w_0, h_0 = w-b_w_0, h-b_w_0
        # select
        self._ng_node_rect_select.setRect(
            x_0, y_0, w_0, h_0
        )
        # name
        n_x, n_y = x_0+c_i_r/2, y_0
        n_w, n_h = w_0-c_i_r, self._ng_draw_name_h
        self._set_name_draw_rect_(
            n_x, n_y, n_w, n_h
        )
        # frame
        f_x, f_y = x_0+c_i_r/2, y_0+n_h
        f_w, f_h = w_0-c_i_r, h_0-n_h
        self._ng_node_rect_frame.setRect(
            f_x, f_y, f_w, f_h
        )
        f_h_x, f_h_y = f_x, f_y
        f_h_w, f_h_h = f_w, self._ng_draw_head_h
        self._ng_node_rect_frame_head.setRect(
            f_h_x, f_h_y, f_h_w, f_h_h
        )
        # icon & button
        i_w, i_h = self._ng_draw_icon_w, self._ng_draw_icon_h
        self._set_icon_text_draw_rect_(
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
        self._ng_node_rect_frame_body.setRect(
            f_b_x, f_b_y, f_b_w, f_b_h
        )

        i_x_2, i_y_2 = x_0, f_b_y

        self._ng_node_rect_input.setRect(
            i_x_2, i_y_2+(f_b_h-c_i_r)/2, c_i_r, c_i_r
        )
        self._ng_node_rect_output.setRect(
            w-b_w_0/2-c_o_r, i_y_2+(f_b_h-c_o_r)/2, c_o_r, c_o_r
        )

    def _set_ng_action_update_press_click_flag_check_(self, event):
        point = event.pos()
        if self._ng_node_rect_select.contains(point):
            self._set_action_flag_(
                self.ActionFlag.NGNodePressClick
            )
            self._set_ng_action_sbj_flag_(
                self.ActionFlag.NGNodePressClick
            )

    def _set_ng_action_update_press_move_flag_check_(self, event):
        point = event.pos()
        if self._ng_node_rect_select.contains(point):
            self._set_action_flag_(
                self.ActionFlag.NGNodePressMove
            )
            self._set_ng_action_sbj_flag_(
                self.ActionFlag.NGNodePressMove
            )

    def _set_ng_action_node_press_start_(self, event):
        self._ng_sbj_graph._set_ng_action_graph_node_press_start_(self)
        self._refresh_widget_draw_()

    def _set_ng_action_node_press_execute_(self, event):
        self._ng_sbj_graph._set_ng_action_graph_node_press_execute_(self)
        self._refresh_widget_draw_()

    def _set_ng_action_node_press_end_(self, event):
        self._ng_sbj_graph._set_ng_action_graph_node_press_end_(self)
        self._refresh_widget_draw_()

    def _do_hover_move_(self, event):
        point = event.pos()
        if self._ng_node_rect_select.contains(point):
            self._set_action_hovered_(True)
        else:
            self._set_action_hovered_(False)

    def _set_ng_action_node_press_move_execute_(self, event):
        d_point = event.globalPos()-self._ng_action_node_move_point_start
        #
        self._ng_sbj_graph._set_ng_graph_node_move_execute_(
            self, d_point
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            #
            if event.type() == QtCore.QEvent.Resize:
                pass
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_ng_action_update_press_click_flag_check_(event)
                    if self._get_action_flag_is_match_(
                            self.ActionFlag.NGNodePressClick,
                    ):
                        self._set_ng_action_node_press_start_(event)
                        self._set_ng_action_node_press_move_start_(event)
                #
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    if not self._get_ng_action_sbj_flag_is_match_(
                            self.ActionFlag.RectSelectMove
                    ):
                        self._set_ng_action_update_press_move_flag_check_(event)
                        if self._get_action_flag_is_match_(
                                self.ActionFlag.NGNodePressMove,
                        ):
                            self._set_ng_action_node_press_execute_(event)
                            self._set_ng_action_node_press_move_execute_(event)
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
                    if self._get_action_flag_is_match_(
                            self.ActionFlag.NGNodePressClick,
                            self.ActionFlag.NGNodePressMove
                    ):
                        self._set_ng_action_node_press_end_(event)
                        self._set_ng_action_node_press_move_stop_(event)
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
        painter = gui_qt_core.QtNGPainter(self)

        offset = 0

        painter._set_ng_node_frame_head_draw_(
            self._ng_node_rect_frame_head,
            border_color=self._type_color,
            border_width=self._ng_draw_border_w,
            border_radius=self._ng_draw_border_w,
            is_hovered=self._get_is_hovered_(),
            is_selected=self._is_selected,
            is_actioned=self._get_is_actioned_(),
        )

        painter._set_ng_node_frame_body_draw_(
            self._ng_node_rect_frame_body,
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
            self._ng_node_rect_input,
            border_width=self._ng_draw_border_w,
            offset=offset
        )

        painter._set_ng_node_output_draw_(
            self._ng_node_rect_output,
            border_width=self._ng_draw_border_w,
            offset=offset
        )

        if self._name_text is not None:
            painter._draw_text_by_rect_(
                self._name_draw_rect,
                self._name_text,
                font=gui_qt_core.GuiQtFont.generate(size=self._ng_draw_font_h),
                font_color=gui_qt_core.QtFontColors.Basic,
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


class NGCmdNodesMove(QtWidgets.QUndoCommand):
    def __init__(self, data):
        super(NGCmdNodesMove, self).__init__()
        self._data = data

    def undo(self):
        for i, i_coord, i_coord_orig in self._data:
            i._set_ng_node_coord_glb_(*i_coord_orig)
            print 'node move: name="{}", coord=({}, {})'.format(i._get_name_text_(), *i_coord_orig)

    def redo(self):
        for i, i_coord, i_coord_orig in self._data:
            i._set_ng_node_coord_glb_(*i_coord)
            print 'node move: name="{}", coord=({}, {})'.format(i._get_name_text_(), *i_coord)


class _QtNGGraph(
    QtWidgets.QWidget,
    #
    gui_qt_abstracts.AbsQtDrawGridDef,
    AbsQtNGGraphSbjDef,
    #
    gui_qt_abstracts.AbsQtActionBaseDef,
    AbsQtActionRectSelectDef,
    AbsQtActionFrameDef,
    #
    AbsQtNGGraphDef,
    AbsQtNGDrawGraphDef,
    #
    AbsQtNGUniverseDef
):
    NG_NODE_CLS = _QtNGNode
    NG_CONNECTION_CLS = _QtNGConnection
    #
    NGLayoutFlag = _NGLayoutFlag
    NGSelectionFlag = _NGSelectionFlag

    def __init__(self, *args, **kwargs):
        super(_QtNGGraph, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        #
        self._init_action_base_def_(self)
        self._set_action_rect_select_def_init_(self)
        self._set_action_frame_def_init_(self)
        #
        self._set_ng_graph_sbj_def_init_(self)
        #
        self._set_ng_graph_def_init_(self)
        self._set_ng_draw_graph_def_init_(self)
        #
        self._set_draw_grid_def_init_(self)
        self._grid_border_color = 63, 63, 63, 255
        self._grid_axis_lock_x, self._grid_axis_lock_y = 1, 1
        self._grid_dir_x, self._grid_dir_y = self._ng_draw_graph_grid_translate_direction_x, self._ng_draw_graph_grid_translate_direction_y

        self._ng_graph_node_connection_layer = _QtNGLayer(self)

        self._ng_graph_layout_flag = self.NGLayoutFlag.Dependent

        self._set_ng_universe_def_init_()
        # undo
        self._undo_stack = QtWidgets.QUndoStack()
        self._undo_action = self._undo_stack.createUndoAction(self, 'undo')
        self._undo_action.setShortcut(
            QtGui.QKeySequence(
                QtCore.Qt.CTRL+QtCore.Qt.Key_Z
            )
        )
        self.addAction(self._undo_action)
        # redo
        self._redo_action = self._undo_stack.createRedoAction(self, 'redo')
        self._redo_action.setShortcut(
            QtGui.QKeySequence(
                QtCore.Qt.CTRL+QtCore.Qt.SHIFT+QtCore.Qt.Key_Z
            )
        )
        self.addAction(self._redo_action)
        #
        actions = [
            (functools.partial(self._set_ng_action_graph_layout_selection_, 'x'), 'L'),
            (functools.partial(self._set_ng_action_graph_layout_selection_, '-height'), 'Ctrl+L'),
            (functools.partial(self._set_ng_action_graph_layout_selection_, 'height'), 'Shift+L'),
            (self._set_ng_action_graph_frame_, 'F'),
            (self._set_ng_action_graph_select_all_, 'Ctrl+A')
        ]
        for i_fnc, i_shortcut in actions:
            i_action = QtWidgets.QAction(self)
            i_action.triggered.connect(
                i_fnc
            )
            i_action.setShortcut(
                QtGui.QKeySequence(
                    i_shortcut
                )
            )
            self.addAction(i_action)

    def _get_undo_stack_(self):
        return self._undo_stack

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_all_(self):
        self._set_ng_graph_transformation_update_()
        #
        self._set_ng_draw_graph_update_(
            self._ng_graph_translate_x, self._ng_graph_translate_y
        )
        self._refresh_widget_draw_geometry_(
            self.rect()
        )
        #
        self._set_ng_graph_nodes_update_geometry_()
        self._set_ng_graph_nodes_update_()

        self._refresh_widget_draw_()

    def _refresh_widget_draw_geometry_(self, rect):
        self._ng_graph_node_connection_layer.setGeometry(
            rect
        )

    def _set_ng_graph_nodes_update_geometry_(self):
        self._set_ng_graph_nodes_transformation_(
            self._ng_graph_translate_x, self._ng_graph_translate_y, self._ng_graph_scale_x, self._ng_graph_scale_y
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                pass
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.modifiers() == QtCore.Qt.ControlModifier:
                    self._set_action_mdf_flag_add_(
                        self.ActionFlag.KeyControlPress
                    )
                elif event.modifiers() == QtCore.Qt.ShiftModifier:
                    self._set_action_mdf_flag_add_(
                        self.ActionFlag.KeyShiftPress
                    )
                elif event.modifiers() == QtCore.Qt.AltModifier:
                    self._set_action_mdf_flag_add_(
                        self.ActionFlag.KeyAltPress
                    )
                elif event.modifiers() == (QtCore.Qt.ControlModifier|QtCore.Qt.ShiftModifier):
                    self._set_action_mdf_flags_(
                        [self.ActionFlag.KeyControlShiftPress]
                    )
            elif event.type() == QtCore.QEvent.KeyRelease:
                self._clear_action_modifier_flags_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_is_match_(
                            self.ActionFlag.NGNodePressClick
                    ) is False:
                        self._set_action_flag_(
                            self.ActionFlag.RectSelectClick
                        )
                        self._set_action_rect_select_start_(event)
                #
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    self._set_action_flag_(
                        self.ActionFlag.NGGraphTrackClick
                    )
                    self._set_ng_action_graph_translate_start_(event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_is_match_(
                            self.ActionFlag.NGNodePressClick, self.ActionFlag.NGNodePressMove
                    ) is False:
                        self._set_action_flag_(
                            self.ActionFlag.RectSelectMove
                        )
                        self._set_action_rect_select_execute_(event)
                elif event.buttons() == QtCore.Qt.RightButton:
                    pass
                elif event.buttons() == QtCore.Qt.MidButton:
                    self._set_action_flag_(
                        self.ActionFlag.NGGraphTrackMove
                    )
                    self._set_ng_action_graph_translate_execute_(event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_rect_select_end_(event)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    self._set_ng_action_graph_translate_stop_(event)
                else:
                    event.ignore()
                #
                self._clear_all_action_flags_()
            #
            elif event.type() == QtCore.QEvent.Wheel:
                self._set_ng_action_graph_scale_execute_(event)
                return True
            #
            elif event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                parent = self.parent()
                if isinstance(parent, gui_qt_wgt_entry.QtEntryFrame):
                    parent._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                parent = self.parent()
                if isinstance(parent, gui_qt_wgt_entry.QtEntryFrame):
                    parent._set_focused_(False)
        return False

    def paintEvent(self, event):
        painter = gui_qt_core.QtNGPainter(self)
        x, y = 0, 0
        width, height = self.width(), self.height()

        rect = QtCore.QRect(
            x, y, width, height
        )
        if self._ng_draw_graph_grid_enable is True:
            painter._set_grid_draw_(
                rect,
                axis_dir=(self._grid_dir_x, self._grid_dir_y),
                grid_scale=(self._ng_graph_scale_x, self._ng_graph_scale_y),
                grid_size=(self._grid_width, self._grid_height),
                translate=(self._ng_draw_graph_grid_translate_x, self._ng_draw_graph_grid_translate_y),
                grid_offset=(self._grid_offset_x, self._grid_offset_y),
                border_color=self._grid_border_color
            )
        if self._ng_draw_graph_grid_mark_enable is True:
            painter._set_grid_mark_draw_(
                rect,
                (self._grid_dir_x, self._grid_dir_y),
                (self._grid_width, self._grid_height),
                (self._ng_draw_graph_grid_translate_x, self._ng_draw_graph_grid_translate_y),
                (self._grid_offset_x, self._grid_offset_y),
                (self._ng_graph_scale_x, self._ng_graph_scale_y),
                (self._grid_value_offset_x, self._grid_value_offset_y),
                self._grid_mark_border_color,
                self._grid_value_show_mode
            )
        if self._ng_draw_graph_grid_axis_enable is True:
            painter._set_grid_axis_draw_(
                rect,
                (self._grid_dir_x, self._grid_dir_y),
                (self._ng_draw_graph_grid_translate_x, self._ng_draw_graph_grid_translate_y),
                (self._grid_offset_x, self._grid_offset_y),
                (self._grid_axis_lock_x, self._grid_axis_lock_y),
                (self._grid_axis_border_color_x, self._grid_axis_border_color_y)
            )

        if self._get_action_flag_is_match_(
                self.ActionFlag.RectSelectMove
        ):
            painter._set_dotted_frame_draw_(
                self._action_rect_select_rect,
                border_color=gui_qt_core.QtBorderColors.Selected,
                background_color=gui_qt_core.QtBackgroundColors.Transparent
            )

        infos = collections.OrderedDict(
            [
                ('translate', '{}, {}'.format(self._ng_graph_translate_x, self._ng_graph_translate_y)),
                ('scale', '{}, {}'.format(self._ng_graph_scale_x, self._ng_graph_scale_y)),
                ('action flag', str(self._get_action_flag_())),
                ('modifier action flag', str(', '.join(map(str, self._get_action_mdf_flags_())))),
                ('current node', self._get_ng_graph_node_current_name_text_()),
                ('count', str(len(self._ng_graph_nodes)))
            ]
        )

        key_text_width = gui_qt_core.GuiQtText.get_draw_width_maximum(
            painter, infos.keys()
        )
        c = len(infos)
        i_h = 20
        y = height-i_h*c
        for i, (i_key, i_value) in enumerate(infos.items()):
            i_rect = QtCore.QRect(
                x+40, y+i*20, width, i_h
            )
            painter._set_text_draw_by_rect_use_key_value_(
                i_rect,
                key_text=i_key,
                value_text=i_value,
                key_text_width=key_text_width
            )

    # universe
    def _set_ng_universe_(self, universe):
        self._ng_node_universe = universe
        obj = self._ng_node_universe.get_objs()
        for i_obj in obj:
            i_ng_node = self._set_ng_graph_sbj_node_create_()
            i_ng_node._set_ng_node_obj_(i_obj)
            i_ng_node._set_type_text_(
                i_obj.type_name
            )
            i_ng_node._set_name_text_(
                i_obj.name
            )
            i_ng_node._set_icon_name_text_(
                i_obj.type_name
            )
            i_ng_node._set_tool_tip_(['path: "{}"'.format(i_obj.path)])
            # i_image_file_path = i_obj.get('image')
            # if i_image_file_path:
            #     i_ng_node._set_image_file_path_(i_image_file_path)

            i_obj.set_gui_ng_graph_node(i_ng_node)

        connections = self._ng_node_universe.get_connections()
        for i_connection in connections:
            i_ng_connection = self._set_ng_graph_sbj_connection_create_()
            i_obj_src = i_connection.get_source_obj()
            i_obj_tgt = i_connection.get_target_obj()
            i_obj_src.get_gui_ng_graph_node()._set_ng_node_connection_start_add_(i_ng_connection)
            i_obj_tgt.get_gui_ng_graph_node()._set_ng_node_connection_end_add_(i_ng_connection)

    def _set_ng_show_by_universe_(self, *args, **kwargs):
        def frame_fnc_():
            self._set_ng_graph_frame_to_nodes_auto_()
            t.stop()

        if args:
            obj_path = args[0]
        else:
            obj_path = None

        if obj_path is not None:
            objs = [self._ng_node_universe.get_obj(obj_path)]
        else:
            objs = self._ng_node_universe.get_basic_source_objs()
        #
        if objs:
            ng_nodes = [i.get_gui_ng_graph_node() for i in objs]
            idx = 0
            for i_ng_node in ng_nodes:
                i_ng_node._set_ng_node_move_by_coord_(
                    0, idx*192
                )
                idx += 1
            #
            ng_nodes_0 = self._set_ng_graph_node_layout_by_connection_(
                ng_nodes,
                size=(192, 192)
            )
            ng_nodes.extend(ng_nodes_0)
            for i_ng_node in self._get_ng_graph_nodes_():
                if i_ng_node not in ng_nodes:
                    i_ng_node._set_ng_node_move_by_coord_(
                        0, idx*192
                    )
                    idx += 1

        t = QtCore.QTimer(self)
        t.timeout.connect(frame_fnc_)
        t.start(50)

    def _set_ng_universe_node_add_(self, *args, **kwargs):
        pass

    def _get_ng_action_graph_selection_flag_(self):
        flags = self._get_action_mdf_flags_()
        if not flags:
            return self.NGSelectionFlag.Separate
        elif flags == [self.ActionFlag.KeyShiftPress]:
            return self.NGSelectionFlag.Add
        elif flags == [self.ActionFlag.KeyControlPress]:
            return self.NGSelectionFlag.Sub
        elif flags == [self.ActionFlag.KeyControlShiftPress]:
            return self.NGSelectionFlag.Invert

    # frame
    @classmethod
    def _get_ng_graph_frame_args_(cls, ng_nodes):
        xs_0, ys_0 = [i.x() for i in ng_nodes], [i.y() for i in ng_nodes]
        xs_1, ys_1 = [i.x()+i.width() for i in ng_nodes], [i.y()+i.height() for i in ng_nodes]
        x_0, y_0 = min(xs_0), min(ys_0)
        x_1, y_1 = max(xs_1), max(ys_1)
        w_0, h_0 = x_1-x_0, y_1-y_0
        return x_0, y_0, x_1, y_1, w_0, h_0

    @classmethod
    def _get_ng_graph_layout_args_(cls, ng_nodes):
        xs_0, ys_0 = [i.x() for i in ng_nodes], [i.y() for i in ng_nodes]
        xs_1, ys_1 = [i.x() for i in ng_nodes], [i.y()+i.height() for i in ng_nodes]
        x_0, y_0 = min(xs_0), min(ys_0)
        x_1, y_1 = max(xs_1), max(ys_1)
        _w_0, _h_0 = x_1-x_0, y_1-y_0
        return x_0, y_0, x_1, y_1

    def _set_ng_graph_frame_translate_to_nodes_(self, ng_nodes):
        t_x, t_y = self._ng_graph_translate_x, self._ng_graph_translate_y
        o_w, o_h = self.width(), self.height()
        x_0, y_0, x_1, y_1, w_0, h_0 = self._get_ng_graph_frame_args_(ng_nodes)
        c_x, c_y = x_0+(x_1-x_0)/2, y_0+(y_1-y_0)/2
        x, y = o_w/2-c_x+t_x, o_h/2-c_y+t_y
        self._set_ng_graph_translate_to_(
            x, y
        )

    def _set_ng_graph_frame_scale_to_nodes_(self, ng_nodes):
        o_s_x, o_s_y = self._ng_graph_scale_x, self._ng_graph_scale_y
        o_w, o_h = self.width(), self.height()
        x_0, y_0, x_1, y_1, w_0, h_0 = self._get_ng_graph_frame_args_(ng_nodes)
        #
        i_x, i_y, i_w, i_h = bsc_core.RawSizeMtd.fit_to(
            (w_0, h_0), (o_w, o_h)
        )
        o_r = (i_w*.75)
        r_0 = w_0
        s_x_0, s_y_0 = float(o_r)/float(r_0), float(o_r)/float(r_0)
        s_x_0, s_y_0 = s_x_0*o_s_x, s_y_0*o_s_y
        self._set_ng_graph_scale_to_(
            s_x_0, s_y_0
        )

    def _set_ng_graph_frame_to_nodes_(self, ng_nodes=None):
        if ng_nodes:
            if isinstance(ng_nodes, (tuple, list)):
                _ = ng_nodes
            else:
                _ = [ng_nodes]
            # scale
            self._set_ng_graph_frame_scale_to_nodes_(_)
            # translate
            self._set_ng_graph_frame_translate_to_nodes_(_)

    def _set_ng_graph_frame_to_nodes_auto_(self):
        if self._ng_graph_nodes_selected:
            ng_nodes = self._ng_graph_nodes_selected
        else:
            ng_nodes = self._ng_graph_nodes
        #
        self._set_ng_graph_frame_to_nodes_(ng_nodes)

    # layout
    def _set_ng_graph_node_layout_by_connection_(self, ng_nodes, size, direction=('r-l', 't-b')):
        def rcs_fnc_(obj_, column_):
            _source_objs = obj_.get_source_objs()
            if _source_objs:
                _cur_column = column_+1
                #
                for _row, _i_obj in enumerate(_source_objs):
                    #
                    _i_obj_path = _i_obj.path
                    if _i_obj_path in o2c_dict:
                        _pre_column = o2c_dict[_i_obj_path]
                        if _cur_column > _pre_column:
                            o2c_dict[_i_obj_path] = _cur_column
                    else:
                        o2c_dict[_i_obj_path] = _cur_column
                    #
                    if _i_obj not in obj_stack:
                        obj_stack.append(_i_obj)
                        rcs_fnc_(_i_obj, _cur_column)

        #
        obj_stack = []
        o2c_dict = {}
        c2o_dict = {}
        #
        x, y, w, h = ng_nodes[0]._get_ng_node_geometry_()
        [rcs_fnc_(i._ng_node_obj, 0) for i in ng_nodes]

        # objs = [i._ng_node_obj for i in ng_nodes]
        # basic_source_objs = self._ng_node_universe.get_basic_source_objs(objs)
        ys = []
        for i in ng_nodes:
            i_x, i_y, i_w, i_h = i._get_ng_node_geometry_()
            ys.append(i_y)

        y_min, y_max = min(ys), max(ys)
        y = y_min+(y_max-y_min)/2
        #
        dir_x, dir_y = direction
        w, h = size
        #
        for k, v in o2c_dict.items():
            c2o_dict.setdefault(v, []).append(k)
        #
        if c2o_dict:
            for column, v in c2o_dict.items():
                v = bsc_core.RawTextsMtd.sort_by_number(v)
                row_count = len(v)
                if dir_x == 'r-l':
                    s_x = x-column*w*2
                elif dir_x == 'l-r':
                    s_x = x+column*w*2
                else:
                    raise ValueError()
                #
                if dir_y == 'b-t':
                    s_y = y+(row_count-1)*h/2
                elif dir_y == 't-b':
                    s_y = y-(row_count-1)*h/2
                else:
                    raise ValueError()
                if v:
                    for i_row, i_obj_path in enumerate(v):
                        i_obj = self._ng_node_universe.get_obj(i_obj_path)
                        i_x = s_x
                        if dir_y == 'b-t':
                            i_y = s_y-i_row*h
                        elif dir_y == 't-b':
                            i_y = s_y+i_row*h
                        else:
                            raise ValueError()
                        #
                        i_ng_node = i_obj.get_gui_ng_graph_node()
                        i_ng_node._set_ng_node_move_by_coord_(
                            i_x, i_y
                        )
        return [i.get_gui_ng_graph_node() for i in obj_stack]

    @classmethod
    def _set_ng_graph_nodes_sort_by_(cls, ng_nodes, sort_key=None):
        """
        :param ng_nodes:
        :param sort_key: "x", "-x" / "height" / "-height"
        :return:
        """
        keys = []
        list_ = []
        query_dict = {}
        for i_ng_node in ng_nodes:
            i_x = i_ng_node.pos().x()
            _i_width = i_ng_node.width()
            i_height = i_ng_node._get_image_line_height_()

            if sort_key in ['x', '-x']:
                i_key = i_x
            elif sort_key in ['height', '-height']:
                i_key = i_height
            else:
                raise RuntimeError()
            #
            if i_key not in keys:
                keys.append(i_key)
            #
            query_dict.setdefault(
                i_key, []
            ).append(
                i_ng_node
            )
        keys.sort()
        if sort_key in ['-x', '-height']:
            keys.reverse()

        for i_key in keys:
            i_ng_nodes = query_dict[i_key]
            for j_ng_node in i_ng_nodes:
                list_.append(j_ng_node)

        return list_

    def _set_ng_graph_node_layout_as_line_(self, ng_nodes, sort_key=None):
        #
        if sort_key is not None:
            ng_nodes = self._set_ng_graph_nodes_sort_by_(
                ng_nodes,
                sort_key=sort_key
            )

        x_0, y_0, x_1, y_1 = self._get_ng_graph_layout_args_(ng_nodes)
        #
        for seq, i_ng_node in enumerate(ng_nodes):
            i_w, i_h = i_ng_node.width(), i_ng_node.height()

            y_0 = y_1-i_h

            i_x, i_y = x_0, y_0
            i_ng_node._set_ng_node_move_by_coord_(
                i_x, i_y
            )

            x_0 += i_w
            x_1 += i_w

    def _set_ng_graph_node_layout_by_nodes_(self, ng_nodes, sort_key='x'):
        if ng_nodes:
            if self._ng_graph_layout_flag == self.NGLayoutFlag.Dependent:
                x, y, w, h = ng_nodes[0]._get_ng_node_geometry_()
                self._set_ng_graph_node_layout_by_connection_(
                    ng_nodes,
                    size=(w, w)
                )
                self._refresh_widget_all_()
            elif self._ng_graph_layout_flag == self.NGLayoutFlag.Line:
                self._set_ng_graph_node_layout_as_line_(
                    ng_nodes,
                    sort_key=sort_key
                )

    # sbj
    def _set_ng_graph_sbj_node_create_(self, *args, **kwargs):
        ng_node = self.NG_NODE_CLS(self)
        self._ng_graph_nodes.append(ng_node)
        ng_node._set_ng_sbj_graph_(self)
        return ng_node

    def _set_ng_graph_sbj_connection_create_(self, *args, **kwargs):
        ng_connection = self.NG_CONNECTION_CLS(self._ng_graph_node_connection_layer)
        self._ng_graph_connections.append(ng_connection)
        ng_connection._set_ng_sbj_graph_(self)
        return ng_connection

    #
    def _set_ng_graph_node_move_start_(self):
        [i._set_ng_node_coord_glb_orig_update_() for i in self._ng_graph_nodes_selected]

    def _set_ng_graph_node_move_execute_(self, sbj, d_point):
        if sbj._get_is_selected_() is True:
            self._set_ng_graph_node_move_as_together_(sbj, d_point)
        else:
            self._set_ng_graph_node_move_as_separate_(sbj)

    #
    def _set_ng_graph_node_move_stop_(self):
        data = []
        for i in self._ng_graph_nodes_selected:
            i_coord_orig, i_coord_glb_orig = i._get_ng_node_coord_glb_(), i._get_ng_node_coord_glb_orig_()
            if i_coord_orig != i_coord_glb_orig:
                data.append(
                    (i, i_coord_orig, i_coord_glb_orig)
                )
        if data:
            c = NGCmdNodesMove(
                data
            )
            self._undo_stack.push(c)

    #
    def _set_ng_graph_node_move_as_separate_(self, sbj):
        self._set_ng_action_graph_select_as_separate_(sbj)

    def _set_ng_graph_node_move_as_together_(self, sbj, d_point):
        self._set_ng_graph_node_current_(sbj)
        #
        if self._ng_graph_node_current is not None:
            p_0 = self._ng_graph_node_current.pos()
            for i in self._ng_graph_nodes_selected:
                if i != self._ng_graph_node_current:
                    i_p = i.pos()
                    i_offset_point = p_0-i_p
                    i._set_ng_node_update_by_pos_(d_point, i_offset_point)
                else:
                    i._set_ng_node_update_by_pos_(d_point)

    # action press
    def _set_ng_action_graph_node_press_end_(self, sbj):
        if self._get_action_flag_is_match_(
                self.ActionFlag.NGNodePressMove
        ) is False:
            if self._ng_graph_selection_flag == self.NGSelectionFlag.Separate:
                self._set_ng_action_graph_select_as_separate_(sbj)
            elif self._ng_graph_selection_flag == self.NGSelectionFlag.Add:
                self._set_ng_action_graph_select_as_add_(sbj)
            elif self._ng_graph_selection_flag == self.NGSelectionFlag.Sub:
                self._set_ng_action_graph_select_as_sub_(sbj)
            elif self._ng_graph_selection_flag == self.NGSelectionFlag.Invert:
                self._set_ng_action_graph_select_as_invert_(sbj)

    # action frame select
    def _set_action_frame_execute_(self, event):
        self._set_ng_graph_frame_to_nodes_auto_()

    def _set_ng_action_graph_frame_(self):
        self._set_ng_graph_frame_to_nodes_auto_()

    def _set_ng_action_graph_layout_selection_(self, sort_key='x'):
        if self._ng_graph_nodes_selected:
            self._set_ng_graph_node_move_start_()
            #
            self._set_ng_graph_node_layout_by_nodes_(
                self._ng_graph_nodes_selected, sort_key
            )
            #
            self._set_ng_graph_node_move_stop_()

    def _set_ng_action_graph_select_all_(self):
        for i_sbj in self._ng_graph_nodes:
            self._set_ng_action_graph_select_as_add_(i_sbj)

    # action rect select
    def _set_action_rect_select_start_(self, event):
        super(_QtNGGraph, self)._set_action_rect_select_start_(event)
        #
        self._ng_graph_selection_flag = self._get_ng_action_graph_selection_flag_()
        # self._set_ng_graph_node_select_clear_()

    def _set_action_rect_select_end_(self, event):
        if self._get_action_flag_is_match_(
                self.ActionFlag.RectSelectMove
        ):
            if self._ng_graph_selection_flag == self.NGSelectionFlag.Separate:
                self._set_ng_action_graph_rect_select_as_separate_()
            elif self._ng_graph_selection_flag == self.NGSelectionFlag.Add:
                self._set_ng_action_graph_rect_select_as_add_()
            elif self._ng_graph_selection_flag == self.NGSelectionFlag.Sub:
                self._set_ng_action_graph_rect_select_as_sub_()
            elif self._ng_graph_selection_flag == self.NGSelectionFlag.Invert:
                self._set_ng_action_graph_rect_select_as_invert_()
        elif self._get_action_flag_is_match_(
                self.ActionFlag.RectSelectClick
        ):
            self._set_ng_graph_node_select_clear_()
        #
        self._refresh_widget_draw_()

    def _set_ng_action_graph_select_as_separate_(self, sbj):
        self._set_ng_graph_node_select_clear_()
        #
        sbj._set_selected_(True)
        self._ng_graph_nodes_selected = [sbj]

    def _set_ng_action_graph_select_as_add_(self, sbj):
        if sbj not in self._ng_graph_nodes_selected:
            sbj._set_selected_(True)
            self._ng_graph_nodes_selected.append(sbj)

    def _set_ng_action_graph_select_as_sub_(self, sbj):
        if sbj in self._ng_graph_nodes_selected:
            sbj._set_selected_(False)
            self._ng_graph_nodes_selected.remove(sbj)

    def _set_ng_action_graph_select_as_invert_(self, sbj):
        if sbj in self._ng_graph_nodes_selected:
            sbj._set_selected_(False)
            self._ng_graph_nodes_selected.remove(sbj)
        elif sbj not in self._ng_graph_nodes_selected:
            sbj._set_selected_(True)
            self._ng_graph_nodes_selected.append(sbj)

    def _set_ng_action_graph_rect_select_as_separate_(self):
        self._set_ng_graph_node_select_clear_()
        #
        contains = []
        for i_sbj in self._ng_graph_nodes:
            if self._action_rect_select_rect.intersects(
                    i_sbj._ng_node_rect_select_glb
            ) is True:
                i_sbj._set_selected_(True)
                contains.append(i_sbj)

        self._ng_graph_nodes_selected = contains

    def _set_ng_action_graph_rect_select_as_add_(self):
        for i_sbj in self._ng_graph_nodes:
            if self._action_rect_select_rect.intersects(
                    i_sbj._ng_node_rect_select_glb
            ) is True:
                self._set_ng_action_graph_select_as_add_(i_sbj)

    def _set_ng_action_graph_rect_select_as_sub_(self):
        for i_sbj in self._ng_graph_nodes:
            if self._action_rect_select_rect.intersects(
                    i_sbj._ng_node_rect_select_glb
            ) is True:
                self._set_ng_action_graph_select_as_sub_(i_sbj)

    def _set_ng_action_graph_rect_select_as_invert_(self):
        for i_sbj in self._ng_graph_nodes:
            if self._action_rect_select_rect.intersects(
                    i_sbj._ng_node_rect_select_glb
            ) is True:
                self._set_ng_action_graph_select_as_invert_(i_sbj)


class _QtNGTreeNode(
    gui_qt_wgt_item_for_tree.QtTreeWidgetItem
):
    def __init__(self, *args, **kwargs):
        super(_QtNGTreeNode, self).__init__(*args, **kwargs)

        self._ng_node_obj = None

    def _get_node_(self):
        return self._ng_node_obj

    def __str__(self):
        return str(self._ng_node_obj)


class _QtNGTree(
    gui_qt_wgt_view_for_tree.QtTreeWidget,
    AbsQtNGUniverseDef
):
    QT_MENU_CLS = gui_qt_wgt_utility.QtMenu

    def _set_ng_universe_(self, universe):
        self.clear()
        self._ng_node_universe = universe
        objs = self._ng_node_universe.get_objs()
        for i_obj in objs:
            self._set_ng_universe_node_add_(i_obj)

    def _set_ng_show_by_universe_(self, *args, **kwargs):
        pass

    def __init__(self, *args, **kwargs):
        super(_QtNGTree, self).__init__(*args, **kwargs)
        self._set_ng_universe_def_init_()
        #
        # self.itemSelectionChanged.connect(self._set_ng_graph_node_select_)

    def _set_ng_node_add_0_(self, obj):
        parent = obj.get_parent()
        item = _QtNGTreeNode()
        obj.set_gui_ng_tree_node(item)
        if parent is not None:
            item_parent = parent.get_gui_ng_tree_node()
            item_parent.addChild(item)
        else:
            self.addTopLevelItem(item)

        name_text = obj.properties.get('gui.name')
        if name_text:
            item._set_name_text_(name_text)
        else:
            item._set_name_text_(obj.name)
        icon_file_path = obj.properties.get('gui.icon_file')
        if icon_file_path:
            item._set_icon_file_path_(icon_file_path)
        else:
            item._set_icon_file_path_(
                gui_core.GuiIcon.get('obj/group')
            )

        tool_tip = obj.properties.get('gui.tool_tip')
        if tool_tip:
            item._set_tool_tip_(tool_tip)

        item._set_check_state_(False)
        item._ng_node_obj = obj

    def _set_ng_universe_node_add_(self, obj):
        if obj.get_gui_ng_tree_node() is None:
            ancestors = obj.get_ancestors()
            if ancestors:
                ancestors.reverse()
                for i_ancestor in ancestors:
                    if i_ancestor.get_gui_ng_tree_node() is None:
                        self._set_ng_node_add_0_(i_ancestor)

            self._set_ng_node_add_0_(obj)

    def _set_ng_graph_node_select_(self):
        if self._selected_indices:
            items = self._get_items_selected_()
            for i in items:
                obj = i._ng_node_obj
                print obj.get_gui_ng_graph_node()
        else:
            pass


class _QtNGImage(_QtNGNode):
    def __init__(self, *args, **kwargs):
        super(_QtNGImage, self).__init__(*args, **kwargs)

        self._ng_draw_name_h_basic = 48
        self._ng_draw_font_h_basic = 8

        self._image_line_height = 0

    def paintEvent(self, event):
        painter = gui_qt_core.QtNGPainter(self)

        offset = 0

        painter._set_node_frame_draw_by_rect_(
            self._ng_node_rect_frame,
            border_width=self._ng_draw_border_w,
            is_selected=self._is_selected,
            is_hovered=self._is_hovered,
            is_actioned=self._get_is_actioned_()
        )

        if self._name_text is not None:
            text = '{}\n{}cm'.format(
                self._name_text, self._get_image_line_height_()
            )
            painter._draw_text_by_rect_(
                self._name_draw_rect,
                text,
                font=gui_qt_core.GuiQtFont.generate(size=self._ng_draw_font_h),
                font_color=gui_qt_core.QtFontColors.Basic,
                text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                offset=offset,
                word_warp=True
            )

        if self._image_file_path is not None:
            painter._draw_image_by_rect_(
                self._ng_node_rect_frame,
                self._image_file_path,
                offset=offset
            )

    def _refresh_widget_draw_geometry_(self, rect):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()

        b_w_0 = self._ng_draw_border_w

        x_0, y_0 = x+b_w_0/2, y+b_w_0/2
        w_0, h_0 = w-b_w_0, h-b_w_0

        self._set_frame_draw_rect_(
            x_0, y_0, w_0, h_0
        )
        # select
        self._ng_node_rect_select.setRect(
            x_0, y_0, w_0, h_0
        )
        # name
        n_x, n_y = x_0, y_0
        n_w, n_h = w_0, self._ng_draw_name_h
        self._set_name_draw_rect_(
            n_x, n_y, n_w, n_h
        )
        # frame
        f_x, f_y = x_0, y_0+n_h
        f_w, f_h = w_0, h_0-n_h
        self._ng_node_rect_frame.setRect(
            f_x, f_y, f_w, f_h
        )

    def _set_image_line_height_(self, h):
        self._image_line_height = h

    def _get_image_line_height_(self):
        return self._image_line_height


class _QtNGImageGraph(_QtNGGraph):
    NG_NODE_CLS = _QtNGImage

    def __init__(self, *args, **kwargs):
        super(_QtNGImageGraph, self).__init__(*args, **kwargs)

        self._ng_graph_image_scale = 0.2

        self._ng_graph_layout_flag = self.NGLayoutFlag.Line

    # widget
    def paintEvent(self, event):
        painter = gui_qt_core.QtNGPainter(self)
        x, y = 0, 0
        width, height = self.width(), self.height()

        rect = QtCore.QRect(
            x, y, width, height
        )

        if self._ng_draw_graph_grid_enable is True:
            painter._set_grid_draw_(
                rect,
                axis_dir=(self._grid_dir_x, self._grid_dir_y),
                grid_scale=(self._ng_graph_scale_x, self._ng_graph_scale_y),
                grid_size=(self._grid_width, self._grid_height),
                translate=(self._ng_draw_graph_grid_translate_x, self._ng_draw_graph_grid_translate_y),
                grid_offset=(self._grid_offset_x, self._grid_offset_y),
                border_color=self._grid_border_color
            )

        if self._get_action_flag_is_match_(
                self.ActionFlag.RectSelectMove
        ):
            painter._set_dotted_frame_draw_(
                self._action_rect_select_rect,
                border_color=gui_qt_core.QtBorderColors.Selected,
                background_color=gui_qt_core.QtBackgroundColors.Transparent
            )

    def _set_ng_universe_(self, universe):
        self._ng_node_universe = universe

        obj = self._ng_node_universe.get_objs()
        for i_obj in obj:
            i_image_file_path = i_obj.get('image')
            if i_image_file_path:
                i_ng_node = self._set_ng_graph_sbj_node_create_()
                i_ng_node._set_ng_node_obj_(i_obj)
                i_ng_node._set_type_text_(
                    i_obj.type_name
                )
                i_ng_node._set_name_text_(
                    i_obj.name
                )
                i_ng_node._set_icon_name_text_(
                    i_obj.type_name
                )

                i_ng_node._set_image_file_path_(i_image_file_path)
                i_w, i_h = i_ng_node._get_image_size_()

                i_width, i_height = i_w*self._ng_graph_image_scale, i_h*self._ng_graph_image_scale
                i_width -= 1
                i_height -= 2
                i_ng_node._set_ng_node_size_basic_(
                    i_width, i_height+i_ng_node._ng_draw_name_h_basic
                )

                i_ng_node._set_image_line_height_(i_height)

                i_ng_node._set_tool_tip_(
                    [
                        'path: "{}"'.format(i_obj.path),
                        'width: "{}"'.format(i_width),
                        'height: "{}"'.format(i_height)
                    ]
                )

                i_obj.set_gui_ng_graph_node(i_ng_node)

                if self.isHidden() is False:
                    i_ng_node.show()
                    i_ng_node._refresh_widget_all_()

    def _set_ng_show_by_universe_(self, *args, **kwargs):
        def layout_fnc_():
            self._set_ng_graph_node_layout_as_line_(
                ng_nodes,
                sort_key='-height'
            )
            self._set_ng_graph_frame_to_nodes_auto_()
            #
            l_t.stop()

        objs = self._ng_node_universe.get_objs()
        if objs:
            ng_nodes = []
            for i_obj in objs:
                i_image_file_path = i_obj.get('image')
                if i_image_file_path:
                    i_ng_node = i_obj.get_gui_ng_graph_node()
                    ng_nodes.append(i_ng_node)
            #
            if ng_nodes:
                l_t = QtCore.QTimer(self)
                l_t.timeout.connect(layout_fnc_)

                if self.isHidden() is False:
                    l_t.start(5)
                else:
                    l_t.start(100)

    def _get_ng_graph_image_geometry_args_(self):
        ng_nodes = self._ng_graph_nodes
        xs_0, ys_0 = [i.x() for i in ng_nodes], [i.y() for i in ng_nodes]
        xs_1, ys_1 = [i.x()+i._ng_node_w_basic for i in ng_nodes], [i.y()+i._ng_node_h_basic for i in ng_nodes]
        x_0, y_0 = min(xs_0), min(ys_0)
        x_1, y_1 = max(xs_1), max(ys_1)
        w_0, h_0 = x_1-x_0, y_1-y_0
        return x_0, y_0, w_0, h_0

    @classmethod
    def _get_ng_graph_image_size_(cls, ng_nodes):
        return sum([i._ng_node_w_basic for i in ng_nodes]), max([i._ng_node_h_basic for i in ng_nodes])

    def _save_ng_graph_image_to_(self, file_path):
        ng_nodes = self._ng_graph_nodes
        scale = 10
        m = 48
        w, h = self._get_ng_graph_image_size_(ng_nodes)
        w_, h_ = w*scale+m*2, h*scale+m*2
        size = QtCore.QSize(w_, h_)
        pixmap = QtGui.QPixmap(size)
        pixmap.fill(QtGui.QColor(55, 55, 55, 255))
        painter = gui_qt_core.QtPainter(pixmap)
        rect = pixmap.rect()
        ng_nodes = self._set_ng_graph_nodes_sort_by_(ng_nodes, sort_key='x')
        offset = 0
        x_0, y_0 = rect.x()+m, rect.y()+m
        for i_ng_node in ng_nodes:
            i_t_h = i_ng_node._ng_draw_name_h_basic*scale
            i_i_w, i_i_h = i_ng_node._ng_node_w_basic*scale, i_ng_node._ng_node_h_basic*scale-i_t_h
            i_t_rect = QtCore.QRect(
                x_0, h_-i_i_h-m-i_t_h, i_i_w, i_t_h
            )
            i_t_font_size = i_ng_node._ng_draw_font_h_basic*scale
            i_t_name_text = '{}\n{}cm'.format(
                i_ng_node._get_name_text_(),
                i_ng_node._get_image_line_height_()
            )
            painter._draw_text_by_rect_(
                i_t_rect,
                i_t_name_text,
                font=gui_qt_core.GuiQtFont.generate(size=i_t_font_size),
                font_color=gui_qt_core.QtFontColors.Basic,
                text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                offset=offset,
                word_warp=True
            )
            i_i_rect = QtCore.QRect(
                x_0, h_-i_i_h-m, i_i_w, i_i_h
            )
            i_image_file_path = i_ng_node._get_image_file_path_()
            # painter.fillRect(i_i_rect, QtGui.QColor(255, 0, 255))
            painter._draw_image_by_rect_(
                i_i_rect,
                i_image_file_path,
                offset=offset
            )
            x_0 += i_i_w

        painter.end()

        ext = os.path.splitext(file_path)[-1]
        if ext:
            if ext.lower() not in ['.png', '.jpg', '.jpeg']:
                # file_path += '.png'
                format_ = 'PNG'
            else:
                format_ = str(ext[1:]).upper()
        else:
            # file_path += '.png'
            format_ = 'PNG'

        pixmap.save(
            file_path,
            format_
        )

    def _set_restore_(self):
        pass

    def _set_clear_(self):
        for i in self._ng_graph_nodes:
            i.deleteLater()

        self._ng_graph_nodes = []
        self._ng_graph_nodes_selected = []
