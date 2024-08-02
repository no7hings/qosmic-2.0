# coding=utf-8
# qt
from ..core.wrap import *


# sub object def
class AbsQtSbjBaseDef(object):
    def _init_sbj_base_def_(self, widget):
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
        self._button_basic_w, self._button_basic_h = 16, 16
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

        self._graph = None

    def _set_graph_(self, widget):
        self._graph = widget

    def _get_graph_scale_(self):
        return self._graph._get_graph_scale_()

    def _update_graph_action_flag_(self, flag):
        self._graph._set_action_flag_(flag)

    def _get_ng_sbj_mdf_flags_(self):
        return self._graph._get_action_mdf_flags_()

    def _update_node_draw_properties_(self):
        s_x, s_y = self._get_graph_scale_()

        self._ng_draw_border_w = self._ng_draw_border_w_basic*s_y
        self._ng_draw_connection_r = self._ng_draw_connection_r_basic*s_y
        self._ng_draw_input_r = self._ng_draw_input_r_basic*s_y
        self._ng_draw_output_r = self._ng_draw_output_r_basic*s_y
        self._ng_draw_font_h = self._ng_draw_font_h_basic*s_y
        self._ng_draw_font_h = max(self._ng_draw_font_h, 1)
        self._ng_draw_name_h = self._ng_draw_name_h_basic*s_y
        self._ng_draw_head_h = self._ng_draw_head_h_basic*s_y
        self._ng_draw_icon_w, self._ng_draw_icon_h = self._ng_draw_icon_w_basic*s_x, self._ng_draw_icon_h_basic*s_y
        self._ng_draw_button_w, self._ng_draw_button_h = self._button_basic_w*s_x, self._button_basic_h*s_y

    def _get_undo_stack_(self):
        return self._graph._undo_stack

    def _get_graph_(self):
        return self._graph


class AbsQtNodeDef(AbsQtSbjBaseDef):
    def _refresh_widget_all_(self):
        raise NotImplementedError()

    def _init_node_def_(self, widget):
        self._widget = widget

        self._init_sbj_base_def_(widget)

        self._ng_node_obj = None

        self._move_start_point = QtCore.QPoint(0, 0)

        self._graph_translate_x, self._graph_translate_y = 0, 0
        self._graph_scale_x, self._graph_scale_y = 1.0, 1.0
        # coord without graph translate and scale
        self._node_basic_x, self._node_basic_y = 0, 0
        self._node_basic_last_x, self._node_basic_last_y = 0, 0

        self._node_basic_w, self._node_basic_h = 192, 80
        self._node_basic_last_w, self._node_basic_last_h = 192, 80

        self._node_rect = QtCore.QRect(0, 0, 0, 0)
        self._node_global_selection_rect = QtCore.QRect(0, 0, 0, 0)
        self._node_selection_rect = QtCore.QRect(0, 0, 0, 0)
        self._node_rect_frame = QtCore.QRect(0, 0, 0, 0)
        self._head_frame_rect = QtCore.QRect(0, 0, 0, 0)
        self._body_frame_rect = QtCore.QRect(0, 0, 0, 0)

        self._node_intput_rect = QtCore.QRect(0, 0, 0, 0)
        self._node_output_rect = QtCore.QRect(0, 0, 0, 0)

        self._ng_node_connection_starts = []
        self._ng_node_connection_ends = []

        self._ng_node_resize_rect = QtCore.QRect(0, 0, 0, 0)
        
        self._resize_start_point_0, self._resize_start_size = QtCore.QPoint(), QtCore.QPoint()

    def _set_basic_size_(self, w, h):
        self._node_basic_w, self._node_basic_h = w, h

    def _get_ng_node_size_basic_(self):
        return self._node_basic_w, self._node_basic_h

    def _update_node_geometry_(self):
        self._widget.setGeometry(
            self._node_rect
        )

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _refresh_widget_draw_geometry_(self):
        raise NotImplementedError()

    def _update_press_click_flag_(self, event):
        point = event.pos()
        if self._node_selection_rect.contains(point):
            self._widget._set_action_flag_(
                self._widget.ActionFlag.NGNodePressClick
            )
            self._update_graph_action_flag_(
                self._widget.ActionFlag.NGNodePressClick
            )

    def _update_connections_(self):
        p = self._node_output_rect.center()
        p = self._widget.mapToParent(p)
        for i in self._ng_node_connection_starts:
            i._set_ng_connection_point_start_(
                p
            )
            i._refresh_widget_all_()
        #
        p = self._node_intput_rect.center()
        p = self._widget.mapToParent(p)
        for i in self._ng_node_connection_ends:
            i._set_ng_connection_point_end_(
                p
            )
            i._refresh_widget_all_()

    def _update_node_rect_properties_(self):
        x, y, w, h = self._compute_geometry_by_graph_args_()

        self._node_rect.setRect(
            x, y, w, h
        )

        x_1, y_1, w_1, h_1 = (
            self._node_selection_rect.x(), self._node_selection_rect.y(),
            self._node_selection_rect.width(), self._node_selection_rect.height()
        )

        self._node_global_selection_rect.setRect(
            x+x_1, y+y_1, w_1, h_1
        )

    def _update_graph_args_(self, t_x, t_y, s_x, s_y):
        self._graph_translate_x, self._graph_translate_y = t_x, t_y
        self._graph_scale_x, self._graph_scale_y = s_x, s_y

    def _get_graph_translate_(self):
        return self._graph_translate_x, self._graph_translate_y

    def _get_graph_scale_(self):
        return self._graph_scale_x, self._graph_scale_y

    def _get_graph_args_(self):
        return self._graph_translate_x, self._graph_translate_y, self._graph_scale_x, self._graph_scale_y

    def _update_basic_coord_(self, x, y):
        def _int(_c):
            if _c >= 0:
                return int(_c)
            return int(_c)-1

        t_x, t_y, s_x, s_y = self._get_graph_args_()
        x_1, y_1 = (x-t_x)/s_x, (y-t_y)/s_y

        self._node_basic_x, self._node_basic_y = _int(x_1), _int(y_1)
        
    def _update_basic_args_as_left_resize_(self, x, y, w, h):
        def _int(_c):
            if _c >= 0:
                return int(_c)
            return int(_c)-1

        t_x, t_y, s_x, s_y = self._get_graph_args_()

        x_1, y_1 = (x-t_x)/s_x, (y-t_y)/s_y
        self._node_basic_x, self._node_basic_y = _int(x_1), _int(y_1)

        w_1, h_1 = w/s_x, h/s_y
        self._node_basic_w, self._node_basic_h = int(w_1), int(h_1)

    def _update_basic_args_as_right_resize_(self, w, h):
        t_x, t_y, s_x, s_y = self._get_graph_args_()

        w_1, h_1 = w/s_x, h/s_y
        self._node_basic_w, self._node_basic_h = int(w_1), int(h_1)

    def _compute_geometry_by_graph_args_(self):
        t_x, t_y, s_x, s_y = self._get_graph_args_()
        return self._node_basic_x*s_x+t_x, self._node_basic_y*s_y+t_y, self._node_basic_w*s_x, self._node_basic_h*s_y

    def _get_geometry_args_(self):
        p = self._widget.pos()
        rect = self._widget.rect()
        return p.x(), p.y(), rect.width(), rect.height()

    def _set_unr_obj_(self, obj):
        self._ng_node_obj = obj

    def _do_press_click_start_(self, event):
        self._graph._do_node_press_start_for_(self)
        self._refresh_widget_draw_()

    def _do_press_click_(self, event):
        self._graph._do_node_press_for_(self)
        self._refresh_widget_draw_()

    def _do_press_click_end_(self, event):
        self._graph._do_node_press_end_for_(self)
        self._refresh_widget_draw_()

    # move or resize or scale
    def _do_press_start_for_any_action_(self, event):
        # position
        self._resize_start_point_0 = event.globalPos()-self._widget.pos()
        # size
        self._resize_start_size = QtCore.QSize(self._widget.width(), self._widget.height())
        # mark self last basic coord and size
        self._push_last_properties_()
        # may be more than one node resizing
        self._get_graph_()._do_node_press_start_for_any_action_()    
    
    # move
    def _update_press_move_flag_(self, event):
        point = event.pos()
        if self._node_selection_rect.contains(point):
            self._widget._set_action_flag_(
                self._widget.ActionFlag.NGNodePressMove
            )
            self._update_graph_action_flag_(
                self._widget.ActionFlag.NGNodePressMove
            )

    def _do_press_move_start_(self, event):
        self._move_start_point = event.globalPos()-self._widget.pos()
        # mark self last basic coord and size
        self._push_last_properties_()
        # may be more than one node moving
        self._get_graph_()._do_node_press_start_for_any_action_()

    def _do_press_move_(self, event):
        d_point = event.globalPos()-self._move_start_point
        self._graph._do_node_press_move_for_(self, d_point)

    def _do_press_move_end_(self, event):
        self._get_graph_()._do_node_press_end_for_any_action_()

    def _move_to_coord_(self, x, y):
        # move real time
        self._widget.move(x, y)

        self._update_basic_coord_(x, y)
        self._update_node_rect_properties_()

        self._update_attachments_()

    def _update_attachments_(self):
        self._update_connections_()

    def _move_to_x_(self, x):
        y = self._widget.y()
        # move real time
        self._widget.move(x, y)

        self._update_basic_coord_(x, y)
        self._update_node_rect_properties_()

        self._update_attachments_()

    def _move_by_point_(self, d_point, offset_point=None):
        if offset_point is not None:
            d_point = d_point-offset_point
            x, y = d_point.x(), d_point.y()
            self._move_to_coord_(x, y)
        else:
            x, y = d_point.x(), d_point.y()
            self._move_to_coord_(x, y)
    
    # resize
    def _do_press_resize_(self, event):
        # point offset
        d_point = event.globalPos()-self._resize_start_point_0

        self._graph._do_node_press_resize_for_(
            self, d_point, self._resize_start_size, self._widget._get_action_flag_()
        )
    
    def _do_press_resize_end_(self, event):
        self._get_graph_()._do_node_press_end_for_any_action_(self)

    def _resize_left_fnc_(self, d_point, offset_point=None):
        if offset_point is not None:
            pass
        else:
            # offset point
            x, y = d_point.x(), d_point.y()
            x_0, y_0 = self._widget.x(), self._widget.y()
            w_0, h_0 = self._widget.width(), self._widget.height()
            x_o = x_0-x
            w, h = w_0+x_o, h_0
            self._resize_left_by_geometry_(x, y, w, h)
    
    def _resize_right_fnc_(self, d_point, start_size, offset_point=None):
        if offset_point is not None:
            pass
        else:
            x_0, y_0 = d_point.x(), d_point.y()
            w_0, h_0 = start_size.width(), start_size.height()
            x, y = self._widget.x(), self._widget.y()
            x_o = x_0-x
            w, h = w_0+x_o, h_0
            self._resize_right_by_size_(w, h)

    def _resize_left_by_geometry_(self, x, y, w, h):
        self._update_basic_args_as_left_resize_(x, y, w, h)

        self._refresh_widget_all_()

        self._update_attachments_()
    
    def _resize_right_by_size_(self, w, h):
        self._update_basic_args_as_right_resize_(w, h)

        self._refresh_widget_all_()

        self._update_attachments_()

    # scale
    def _do_press_scale_(self, event):
        # point offset
        d_point = event.globalPos()-self._resize_start_point_0

    def _do_press_scale_end_(self, event):
        self._get_graph_()._do_node_press_end_for_any_action_(self)
    
    def _scale_left_fnc_(self, d_point, offset_point=None):
        if offset_point is not None:
            pass
        else:
            # offset point
            x, y = d_point.x(), d_point.y()
            x_0, y_0 = self._widget.x(), self._widget.y()
            w_0, h_0 = self._widget.width(), self._widget.height()
            x_o = x_0-x
            w, h = w_0+x_o, h_0
            self._scale_left_by_geometry_(x, y, w, h)
    
    def _scale_right_fnc_(self, d_point, start_size, offset_point=None):
        pass

    def _scale_left_by_geometry_(self, x, y, w, h):
        self._update_basic_args_as_left_scale_(x, y, w, h)

        self._refresh_widget_all_()

        self._update_attachments_()

    def _update_basic_args_as_left_scale_(self, x, y, w, h):
        pass

    # basic coord
    def _pull_basic_coord_(self, x, y):
        self._node_basic_x, self._node_basic_y = x, y
        self._refresh_widget_all_()

    def _get_basic_coord_(self):
        return self._node_basic_x, self._node_basic_y

    def _get_basic_last_coord_(self):
        return self._node_basic_last_x, self._node_basic_last_y

    # basic size
    def _pull_basic_size_(self, w, h):
        self._node_basic_w, self._node_basic_h = w, h
        self._refresh_widget_all_()

    def _get_basic_size_(self):
        return self._node_basic_w, self._node_basic_h
    
    def _get_basic_last_size_(self):
        return self._node_basic_last_w, self._node_basic_last_h

    # mark
    def _push_basic_last_coord_(self):
        self._node_basic_last_x, self._node_basic_last_y = self._node_basic_x, self._node_basic_y
        
    def _push_basic_last_size_(self):
        self._node_basic_last_w, self._node_basic_last_h = self._node_basic_w, self._node_basic_h

    def _push_last_properties_(self):
        self._push_basic_last_coord_()
        self._push_basic_last_size_()

    def _add_start_connection_(self, connection):
        self._ng_node_connection_starts.append(connection)

    def _add_end_connection_(self, connection):
        self._ng_node_connection_ends.append(connection)


class AbsQtConnectionDef(AbsQtSbjBaseDef):
    def _init_connection_def_(self, widget):
        self._widget = widget

        self._init_sbj_base_def_(widget)

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

    def _update_node_geometry_(self):
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


class AbsQtBypassDef(object):
    def _init_bypass_def_(self, widget):
        self._widget = widget

        self._bypass = False

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _set_bypass_(self, boolean):
        self._bypass = boolean

        self._refresh_widget_draw_()
