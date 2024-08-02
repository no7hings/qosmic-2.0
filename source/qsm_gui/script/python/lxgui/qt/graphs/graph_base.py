# coding=utf-8
import enum

import lxbasic.core as bsc_core
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from . import undo_command as _undo_command


class _NGLayoutFlag(enum.IntEnum):
    Dependent = 0
    Line = 1


class _NGSelectionFlag(enum.IntEnum):
    Separate = 0
    Add = 1
    Sub = 2
    Invert = 3


class AbsQtNGUniverseDef(object):
    def _init_universe_def_(self, widget):
        self._widget = widget
        self._graph_universe = None
        self._ng_node_universe_dict = {}

    def _set_graph_universe_(self, *args, **kwargs):
        raise NotImplementedError()

    def _set_ng_show_by_universe_(self, *args, **kwargs):
        raise NotImplementedError()

    def _set_ng_universe_node_add_(self, *args, **kwargs):
        raise NotImplementedError()


# graph
class AbsQtGraphBaseDef(object):
    @classmethod
    def _get_nodes_basic_geometry_args_for_(cls, nodes):
        tl_xs = [x._node_basic_x for x in nodes]
        tl_ys = [x._node_basic_y for x in nodes]
        br_xs = [x._node_basic_x+x._node_basic_w for x in nodes]
        br_ys = [x._node_basic_y+x._node_basic_h for x in nodes]
        x_0, y_0 = min(tl_xs), min(tl_ys)
        x_1, y_1 = max(br_xs), max(br_ys)
        w_0, h_0 = x_1-x_0, y_1-y_0
        return x_0, y_0, x_1, y_1, w_0, h_0

    @staticmethod
    def _update_graph_point_by_matrix_(point, matrix):
        x_0, y_0 = point.x(), point.y()
        x_1, y_1 = (
            matrix[0][0]*x_0+matrix[0][1]*y_0+matrix[0][2],
            matrix[1][0]*x_0+matrix[1][1]*y_0+matrix[1][2]
        )
        point.setX(x_1)
        point.setY(y_1)

    def _init_graph_base_def_(self, widget):
        self._widget = widget

        self._ng_graph_translate_point = QtCore.QPoint(0, 0)
        #
        self._ng_graph_composite_matrix = bsc_core.RawMatrix33Opt.get_identity()
        #
        self._graph_translate_x, self._graph_translate_y = 0, 0
        self._ng_graph_translate_x_enable, self._ng_graph_translate_y_enable = True, True
        #
        self._graph_scale_x, self._graph_scale_y = 1.0, 1.0
        self._ng_graph_scale_radix_x, self._ng_graph_scale_radix_y = 0.25, 0.25
        # graph viewport 
        self._graph_basic_w, self._graph_basic_h = 1024, 1024
        self._graph_basic_w_minimum, self._graph_basic_w_maximum = 2, 8192
        self._graph_basic_h_minimum, self._graph_basic_h_maximum = 2, 8192
        #
        self._ng_graph_point_start = QtCore.QPoint(0, 0)
        self._ng_graph_point_end = QtCore.QPoint(
            self._graph_basic_w*self._graph_scale_x, self._graph_basic_h*self._graph_scale_y
        )
        self._ng_rect = QtCore.QRect(
            0, 0,
            self._graph_basic_w, self._graph_basic_h
        )

        self._graph_scale_x_enable, self._graph_scale_y_enable = True, True

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _refresh_widget_all_(self):
        raise NotImplementedError()

    def _update_graph_geometry_(self):
        x_0, y_0, x_1, y_1, r_w, r_h = self._get_graph_rect_args_()
        self._graph_translate_x, self._graph_translate_y = x_0, y_0

        self._graph_scale_x, self._graph_scale_y = (
            r_w/float(self._graph_basic_w), r_h/float(self._graph_basic_h)
        )
        self._ng_rect.setRect(
            x_0, y_0, r_w, r_h
        )

    # action
    def _do_graph_track_start_(self, event):
        self._ng_graph_translate_point = event.pos()
        self._refresh_widget_all_()

    def _do_graph_track_move_(self, event):
        point = event.pos()

        d_p = point-self._ng_graph_translate_point
        d_t_x, d_t_y = d_p.x(), d_p.y()

        self._update_graph_matrix_by_track_(d_t_x, d_t_y)
        self._update_graph_transformation_by_matrix_()
        if point is not None:
            self._ng_graph_translate_point = point
        else:
            self._ng_graph_translate_point = QtCore.QPoint(0, 0)
        self._refresh_widget_all_()

    def _do_graph_track_end_(self, event):
        self._ng_graph_translate_point = event.pos()
        self._refresh_widget_all_()

    # zoom
    def _do_graph_zoom_(self, event):
        delta = event.angleDelta().y()
        point = event.pos()

        if delta > 0:
            d_s_x, d_s_y = 1+self._ng_graph_scale_radix_x, 1+self._ng_graph_scale_radix_y
        else:
            d_s_x, d_s_y = 1/(1+self._ng_graph_scale_radix_x), 1/(1+self._ng_graph_scale_radix_y)

        c_x, c_y = point.x(), point.y()

        self._update_graph_matrix_by_zoom_(c_x, c_y, d_s_x, d_s_y)
        self._update_graph_transformation_by_matrix_()
        if point is not None:
            self._ng_graph_translate_point = point
        else:
            self._ng_graph_translate_point = QtCore.QPoint(0, 0)

        self._refresh_widget_all_()

    def _update_graph_rect_points_(self, x_0, y_0, x_1, y_1):
        self._ng_graph_point_start.setX(x_0)
        self._ng_graph_point_start.setY(y_0)
        self._ng_graph_point_end.setX(x_1)
        self._ng_graph_point_end.setY(y_1)

        self._refresh_widget_all_()

    def _get_graph_rect_args_(self):
        o_x_0, o_y_0 = self._ng_graph_point_start.x(), self._ng_graph_point_start.y()
        o_x_1, o_y_1 = self._ng_graph_point_end.x(), self._ng_graph_point_end.y()
        o_r_w, o_r_h = o_x_1-o_x_0, o_y_1-o_y_0
        return o_x_0, o_y_0, o_x_1, o_y_1, o_r_w, o_r_h

    def _translate_graph_to_(self, x, y):
        o_x_0, o_y_0, o_x_1, o_y_1, o_r_w, o_r_h = self._get_graph_rect_args_()
        x_0, y_0 = x, y
        x_1, y_1 = x+o_r_w, y+o_r_h

        self._update_graph_rect_points_(x_0, y_0, x_1, y_1)

    def _scale_graph_to_(self, s_x, s_y):
        x_0, y_0 = self._graph_translate_x, self._graph_translate_y
        x_1, y_1 = x_0+self._graph_basic_w*s_x, y_0+self._graph_basic_h*s_y

        self._update_graph_rect_points_(x_0, y_0, x_1, y_1)

    def _scale_graph_to_origin_(self, s_x, s_y):
        s_w_0, s_h_0 = self._graph_basic_w*s_x, self._graph_basic_h*s_y
        x_0, y_0 = 0, 0
        x_1, y_1 = s_w_0, s_h_0

        self._update_graph_rect_points_(x_0, y_0, x_1, y_1)

    def _get_graph_translate_(self):
        return self._graph_translate_x, self._graph_translate_y

    def _get_graph_scale_(self):
        return self._graph_scale_x, self._graph_scale_y

    def _update_graph_matrix_by_track_(self, d_t_x, d_t_y):
        m = self._ng_graph_composite_matrix
        m_t = bsc_core.RawMatrix33Opt.get_default()
        m_t = bsc_core.RawMatrix33Opt.identity_to(m_t)
        m_t[0][2] = d_t_x
        m_t[1][2] = d_t_y
        self._ng_graph_composite_matrix = bsc_core.RawMatrix33Opt(m_t).multiply_to(m)

    def _update_graph_matrix_by_zoom_(self, c_x, c_y, d_s_x, d_s_y):
        m = self._ng_graph_composite_matrix
        # scale matrix
        s_m = bsc_core.RawMatrix33Opt.get_default()
        s_m = bsc_core.RawMatrix33Opt.identity_to(s_m)
        if self._graph_scale_x_enable is True:
            s_m[0][0] = d_s_x
            s_m[0][2] = (1-d_s_x)*c_x
        if self._graph_scale_y_enable is True:
            s_m[1][1] = d_s_y
            s_m[1][2] = (1-d_s_y)*c_y
        self._ng_graph_composite_matrix = bsc_core.RawMatrix33Opt(s_m).multiply_to(m)

    def _update_graph_transformation_by_matrix_(self):
        m = self._ng_graph_composite_matrix

        self._update_graph_point_by_matrix_(self._ng_graph_point_start, m)
        self._update_graph_point_by_matrix_(self._ng_graph_point_end, m)
        x_0, y_0 = self._ng_graph_point_start.x(), self._ng_graph_point_start.y()
        x_1, y_1 = self._ng_graph_point_end.x(), self._ng_graph_point_end.y()
        # make scale != 0
        x_2, y_2 = (
            max(min(x_1, x_0+self._graph_basic_w_maximum), x_0+self._graph_basic_w_minimum),
            max(min(y_1, y_0+self._graph_basic_h_maximum), y_0+self._graph_basic_h_minimum)
        )
        self._ng_graph_point_end.setX(x_2)
        self._ng_graph_point_end.setY(y_2)
        # reset matrix
        self._ng_graph_composite_matrix = bsc_core.RawMatrix33Opt.identity_to(m)


class AbsQtGraphSbjDef(object):
    NG_NODE_CLS = None
    NG_CONNECTION_CLS = None
    
    @classmethod
    def _filter_nodes_on_left_(cls, sbj, sbj_list):
        list_ = []
        x = sbj.x()
        for i_sbj in sbj_list:
            if i_sbj != sbj:
                i_x = i_sbj.x()
                if i_x < x:
                    list_.append(i_sbj)
        return list_

    def _init_sbj_base_def_(self, widget):
        self._widget = widget

        self._graph_nodes = []
        self._nodes_selected = []

        self._ng_graph_connections = []
        self._ng_graph_connections_selected = []

        self._node_current = None

        self._node_selection_flag = _NGSelectionFlag.Separate

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _create_node_(self, *args, **kwargs):
        raise NotImplementedError()

    def _create_connection_(self, *args, **kwargs):
        raise NotImplementedError()

    def _get_ng_graph_nodes_(self):
        return self._graph_nodes

    def _get_graph_selected_node_count_(self):
        return len(self._nodes_selected)

    def _get_graph_selected_nodes_(self):
        return self._nodes_selected

    def _update_graph_nodes_(self):
        for i_ng_node in self._get_ng_graph_nodes_():
            i_ng_node._refresh_widget_all_()

    def _set_ng_graph_clear_(self):
        pass

    def _do_graph_frame_scale_for_(self, nodes):
        x_0, y_0, x_1, y_1, w_0, h_0 = self._widget._get_nodes_basic_geometry_args_for_(nodes)

        w_1, h_1 = self._widget.width(), self._widget.height()
        if w_0 > h_0:
            s_x_0 = float(w_1)/float(w_0)
        else:
            s_x_0 = float(h_1)/float(h_0)

        self._widget._scale_graph_to_origin_(
            s_x_0*.875, s_x_0*.875
        )

    def _do_graph_frame_translate_for_(self, nodes):
        x_0, y_0, x_1, y_1, w_0, h_0 = self._widget._get_nodes_basic_geometry_args_for_(nodes)
        sx, sy = self._widget._graph_scale_x, self._widget._graph_scale_y

        s_x_0, s_y_0 = x_0*sx, y_0*sy
        s_w_0, s_h_0 = w_0*sx, h_0*sy
        w_1, h_1 = self._widget.width(), self._widget.height()
        x, y = -s_x_0+(w_1-s_w_0)/2, -s_y_0+(h_1-s_h_0)/2
        self._widget._translate_graph_to_(
            x, y
        )

    def _do_frame_nodes_for_(self, ng_nodes=None):
        if ng_nodes:
            if isinstance(ng_nodes, (tuple, list)):
                _ = ng_nodes
            else:
                _ = [ng_nodes]
            # scale
            self._do_graph_frame_scale_for_(_)
            # translate
            self._do_graph_frame_translate_for_(_)
    
    def _do_frame_nodes_auto_(self):
        if self._nodes_selected:
            ng_nodes = self._nodes_selected
        else:
            ng_nodes = self._graph_nodes
        self._do_frame_nodes_for_(ng_nodes)

    def _set_node_current_for_(self, sbj):
        self._node_current = sbj
        if sbj is not None:
            self._node_current.raise_()

        self._refresh_widget_draw_()

    def _get_ng_graph_node_current_name_text_(self):
        if self._node_current is not None:
            return self._node_current._get_name_text_()

    def _clear_node_selection_(self):
        for i_sbj in self._nodes_selected:
            i_sbj._set_selected_(False)

        self._nodes_selected = []
        self._node_current = None

    def _update_all_nodes_graph_args_(self, t_x, t_y, s_x, s_y):
        [x._update_graph_args_(t_x, t_y, s_x, s_y) for x in self._graph_nodes]

    def _get_node_selection_flag_(self):
        flags = self._widget._get_action_mdf_flags_()
        if not flags:
            return self._widget.NGSelectionFlag.Separate
        elif flags == [self._widget.ActionFlag.KeyShiftPress]:
            return self._widget.NGSelectionFlag.Add
        elif flags == [self._widget.ActionFlag.KeyControlPress]:
            return self._widget.NGSelectionFlag.Sub
        elif flags == [self._widget.ActionFlag.KeyControlShiftPress]:
            return self._widget.NGSelectionFlag.Invert

    # click
    def _do_node_press_start_for_(self, sbj):
        self._node_selection_flag = self._get_node_selection_flag_()
        self._set_node_current_for_(sbj)

    def _do_node_press_for_(self, sbj):
        if self._get_graph_selected_node_count_() == 0:
            self._separate_select_node_for_(sbj)

    def _do_node_press_end_for_(self, sbj):
        if self._widget._is_action_flag_match_(
            self._widget.ActionFlag.NGNodePressMove
        ) is False:
            if self._node_selection_flag == self._widget.NGSelectionFlag.Separate:
                self._separate_select_node_for_(sbj)
            elif self._node_selection_flag == self._widget.NGSelectionFlag.Add:
                self._add_select_node_for_(sbj)
            elif self._node_selection_flag == self._widget.NGSelectionFlag.Sub:
                self._sub_select_node_for_(sbj)
            elif self._node_selection_flag == self._widget.NGSelectionFlag.Invert:
                self._invert_select_node_for_(sbj)

    # move
    def _do_node_press_start_for_any_action_(self):
        [i._push_last_properties_() for i in self._nodes_selected]

    def _do_node_press_move_for_(self, sbj, d_point):
        if sbj._is_selected_() is True:
            self._together_move_nodes_(sbj, d_point)
        else:
            self._separate_move_node_(sbj)

    def _together_move_nodes_(self, sbj, d_point):
        self._set_node_current_for_(sbj)

        if self._node_current is not None:
            p_0 = sbj.pos()
            for i_sbj in self._nodes_selected:
                if i_sbj != self._node_current:
                    i_p = i_sbj.pos()
                    i_offset_point = p_0-i_p
                    i_sbj._move_by_point_(d_point, i_offset_point)
                else:
                    i_sbj._move_by_point_(d_point)

    def _separate_move_node_(self, sbj):
        self._separate_select_node_for_(sbj)

    # resize
    def _do_node_press_resize_for_(self, sbj, d_point, start_size, flag):
        if sbj._is_selected_() is True:
            self._together_resize_nodes_(sbj, d_point, start_size, flag)
        else:
            self._separate_resize_node_(sbj, d_point, start_size, flag)

    def _together_resize_nodes_(self, sbj, d_point, start_size, flag):
        # if self._node_current is not None:
        if flag == self._widget.ActionFlag.NGTimeResizeLeft:
            p_0 = sbj.pos()
            sbj._resize_left_fnc_(d_point)
            # nodes = self._filter_nodes_on_left_(sbj, self._nodes_selected)
            # print nodes
        elif flag == self._widget.ActionFlag.NGTimeResizeRight:
            sbj._resize_right_fnc_(d_point, start_size)

    def _separate_resize_node_(self, sbj, d_point, start_size, flag):
        sbj.raise_()
        if flag == self._widget.ActionFlag.NGTimeResizeLeft:
            sbj._resize_left_fnc_(d_point)
        elif flag == self._widget.ActionFlag.NGTimeResizeRight:
            sbj._resize_right_fnc_(d_point, start_size)

    # scale
    def _do_node_press_scale_for_(self, sbj, d_point, start_size, flag):
        if sbj._is_selected_() is True:
            self._together_scale_nodes_(sbj, d_point, start_size, flag)
        else:
            self._separate_scale_node_(sbj, d_point, start_size, flag)
            
    def _together_scale_nodes_(self, sbj, d_point, start_size, flag):
        pass
    
    def _separate_scale_node_(self, sbj, d_point, start_size, flag):
        sbj.raise_()
        if flag == self._widget.ActionFlag.NGTimeScaleLeft:
            sbj._scale_left_fnc_(d_point)
        elif flag == self._widget.ActionFlag.NGTimeScaleRight:
            sbj._scale_right_fnc_(d_point, start_size)

    # undo
    def _do_node_press_end_for_any_action_(self, sbj=None):
        data = []
        for i in self._nodes_selected:
            i_coord, i_last_coord = i._get_basic_coord_(), i._get_basic_last_coord_()
            i_size, i_last_size = i._get_basic_size_(), i._get_basic_last_size_()
            if i_coord != i_last_coord or i_size != i_last_size:
                data.append(
                    (i, i_coord, i_last_coord, i_size, i_last_size)
                )
        if sbj is not None:
            coord, last_coord = sbj._get_basic_coord_(), sbj._get_basic_last_coord_()
            size, last_size = sbj._get_basic_size_(), sbj._get_basic_last_size_()
            if coord != last_coord or size != last_size:
                data.append(
                    (sbj, coord, last_coord, size, last_size)
                )
        if data:
            c = _undo_command.QtNodeActionCommand(
                data
            )
            self._widget._undo_stack.push(c)

    # select
    def _separate_select_node_for_(self, sbj):
        self._clear_node_selection_()
        sbj._set_selected_(True)
        self._nodes_selected = [sbj]

    def _add_select_node_for_(self, sbj):
        if sbj not in self._nodes_selected:
            sbj._set_selected_(True)
            self._nodes_selected.append(sbj)

    def _sub_select_node_for_(self, sbj):
        if sbj in self._nodes_selected:
            sbj._set_selected_(False)
            self._nodes_selected.remove(sbj)

    def _invert_select_node_for_(self, sbj):
        if sbj in self._nodes_selected:
            sbj._set_selected_(False)
            self._nodes_selected.remove(sbj)
        elif sbj not in self._nodes_selected:
            sbj._set_selected_(True)
            self._nodes_selected.append(sbj)

    def _select_all_nodes_(self):
        for i_sbj in self._graph_nodes:
            self._add_select_node_for_(i_sbj)


class AbsQtGraphDrawBaseDef(object):
    def _init_graph_draw_base_def_(self, widget):
        self._widget = widget

        self._ng_draw_graph_grid_enable = True
        self._ng_draw_graph_grid_mark_enable = True
        self._ng_draw_graph_grid_axis_enable = True
        self._grid_translate_direction_x, self._grid_translate_direction_y = 1, 1
        self._graph_grid_translate_x, self._graph_grid_translate_y = 0, 0

    def _update_graph_draw_args_(self, t_x, t_y):
        self._graph_grid_translate_x, self._graph_grid_translate_y = (
            t_x*self._grid_translate_direction_x, t_y*self._grid_translate_direction_y
        )


class AbsQtActionForRectSelectDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _init_action_for_rect_select_def_(self, widget):
        self._widget = widget

        self._action_rect_select_point_start = QtCore.QPoint(0, 0)
        self._rect_selection_rect = QtCore.QRect(
            0, 0, 0, 0
        )

    def _do_rect_select_start_(self, event):
        self._action_rect_select_point_start = event.pos()
        self._node_selection_flag = self._widget._get_node_selection_flag_()

    def _do_rect_select_move_(self, event):
        self._rect_selection_rect.setTopLeft(
            self._action_rect_select_point_start
        )
        self._rect_selection_rect.setBottomRight(
            event.pos()
        )
        self._refresh_widget_draw_()

    def _do_rect_select_end_(self, event):
        if self._widget._is_action_flag_match_(
            self._widget.ActionFlag.RectSelectMove
        ):
            if self._node_selection_flag == self._widget.NGSelectionFlag.Separate:
                self._separate_rect_select_nodes_()
            elif self._node_selection_flag == self._widget.NGSelectionFlag.Add:
                self._add_rect_select_nodes_()
            elif self._node_selection_flag == self._widget.NGSelectionFlag.Sub:
                self._sub_rect_select_nodes_()
            elif self._node_selection_flag == self._widget.NGSelectionFlag.Invert:
                self._invert_rect_select_nodes_()
        elif self._widget._is_action_flag_match_(
            self._widget.ActionFlag.RectSelectClick
        ):
            self._widget._clear_node_selection_()
        #
        self._refresh_widget_draw_()

    def _separate_rect_select_nodes_(self):
        self._widget._clear_node_selection_()
        #
        contains = []
        for i_sbj in self._widget._graph_nodes:
            if self._rect_selection_rect.intersects(
                i_sbj._node_global_selection_rect
            ) is True:
                i_sbj._set_selected_(True)
                contains.append(i_sbj)

        self._nodes_selected = contains

    def _add_rect_select_nodes_(self):
        for i_sbj in self._widget._graph_nodes:
            if self._rect_selection_rect.intersects(
                    i_sbj._node_global_selection_rect
            ) is True:
                self._widget._add_select_node_for_(i_sbj)

    def _sub_rect_select_nodes_(self):
        for i_sbj in self._widget._graph_nodes:
            if self._rect_selection_rect.intersects(
                    i_sbj._node_global_selection_rect
            ) is True:
                self._widget._sub_select_node_for_(i_sbj)

    def _invert_rect_select_nodes_(self):
        for i_sbj in self._widget._graph_nodes:
            if self._rect_selection_rect.intersects(
                    i_sbj._node_global_selection_rect
            ) is True:
                self._widget._invert_select_node_for_(i_sbj)


class QtSbjLayer(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QtSbjLayer, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            event.ignore()
        return False
