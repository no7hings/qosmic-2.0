# coding=utf-8
import lxbasic.core as bsc_core
# qt
from ..core.wrap import *


class ModelForBaseGraph(object):
    @classmethod
    def _compute_nodes_basic_geometry_args_for(cls, nodes):
        tl_xs = [x._node_basic_x for x in nodes]
        tl_ys = [x._node_basic_y for x in nodes]
        br_xs = [x._node_basic_x+x._node_basic_w for x in nodes]
        br_ys = [x._node_basic_y+x._node_basic_h for x in nodes]
        x_0, y_0 = min(tl_xs), min(tl_ys)
        x_1, y_1 = max(br_xs), max(br_ys)
        w_0, h_0 = x_1-x_0, y_1-y_0
        return x_0, y_0, x_1, y_1, w_0, h_0

    @staticmethod
    def _update_point_by_matrix(point, matrix):
        x_0, y_0 = point.x(), point.y()
        x_1, y_1 = (
            matrix[0][0]*x_0+matrix[0][1]*y_0+matrix[0][2],
            matrix[1][0]*x_0+matrix[1][1]*y_0+matrix[1][2]
        )
        point.setX(x_1)
        point.setY(y_1)

    def update_matrix_by_track(self, d_t_x, d_t_y):
        m = self._graph_composite_matrix
        m_t = bsc_core.RawMatrix33Opt.get_default()
        m_t = bsc_core.RawMatrix33Opt.identity_to(m_t)
        m_t[0][2] = d_t_x
        m_t[1][2] = d_t_y
        self._graph_composite_matrix = bsc_core.RawMatrix33Opt(m_t).multiply_to(m)

    def update_transformation(self):
        m = self._graph_composite_matrix

        self._update_point_by_matrix(self._graph_start_point, m)
        self._update_point_by_matrix(self._graph_end_point, m)
        x_0, y_0 = self._graph_start_point.x(), self._graph_start_point.y()
        x_1, y_1 = self._graph_end_point.x(), self._graph_end_point.y()
        # make scale != 0
        x_2, y_2 = (
            max(min(x_1, x_0+self._graph_basic_w_maximum), x_0+self._graph_basic_w_minimum),
            max(min(y_1, y_0+self._graph_basic_h_maximum), y_0+self._graph_basic_h_minimum)
        )
        self._graph_end_point.setX(x_2)
        self._graph_end_point.setY(y_2)
        # reset matrix
        self._graph_composite_matrix = bsc_core.RawMatrix33Opt.identity_to(m)

    def get_rect_args(self):
        o_x_0, o_y_0 = self._graph_start_point.x(), self._graph_start_point.y()
        o_x_1, o_y_1 = self._graph_end_point.x(), self._graph_end_point.y()
        o_r_w, o_r_h = o_x_1-o_x_0, o_y_1-o_y_0
        return o_x_0, o_y_0, o_x_1, o_y_1, o_r_w, o_r_h

    def update(self):
        x_0, y_0, x_1, y_1, r_w, r_h = self.get_rect_args()
        self._graph_translate_x, self._graph_translate_y = x_0, y_0

        self._graph_scale_x, self._graph_scale_y = (
            r_w/float(self._graph_basic_w), r_h/float(self._graph_basic_h)
        )
        self._graph_rect.setRect(
            x_0, y_0, r_w, r_h
        )

    def update_rect_by_points(self, x_0, y_0, x_1, y_1):
        self._graph_start_point.setX(x_0)
        self._graph_start_point.setY(y_0)
        self._graph_end_point.setX(x_1)
        self._graph_end_point.setY(y_1)

        self.update()

        self._widget._refresh_widget_all_()

    def update_matrix_by_zoom(self, c_x, c_y, d_s_x, d_s_y):
        m = self._graph_composite_matrix
        # scale matrix
        s_m = bsc_core.RawMatrix33Opt.get_default()
        s_m = bsc_core.RawMatrix33Opt.identity_to(s_m)
        if self._graph_scale_x_enable is True:
            s_m[0][0] = d_s_x
            s_m[0][2] = (1-d_s_x)*c_x
        if self._graph_scale_y_enable is True:
            s_m[1][1] = d_s_y
            s_m[1][2] = (1-d_s_y)*c_y
        self._graph_composite_matrix = bsc_core.RawMatrix33Opt(s_m).multiply_to(m)

    def __init__(self, widget):
        self._widget = widget

        self._graph_hover_point = QtCore.QPoint(0, 0)
        self._graph_track_start_point = QtCore.QPoint(0, 0)

        self._graph_composite_matrix = bsc_core.RawMatrix33Opt.get_identity()

        self._graph_translate_x, self._graph_translate_y = 0, 0

        self._graph_scale_x, self._graph_scale_y = 1.0, 1.0
        self._graph_scale_radix_x, self._graph_scale_radix_y = 0.25, 0.25

        self._graph_basic_w, self._graph_basic_h = 1024, 1024
        self._graph_basic_w_minimum, self._graph_basic_w_maximum = 2, 8192
        self._graph_basic_h_minimum, self._graph_basic_h_maximum = 2, 8192
        #
        self._graph_start_point = QtCore.QPoint(0, 0)
        self._graph_end_point = QtCore.QPoint(
            self._graph_basic_w*self._graph_scale_x, self._graph_basic_h*self._graph_scale_y
        )
        self._graph_rect = qt_rect(0, 0, self._graph_basic_w, self._graph_basic_h)

        self._graph_translate_x_enable, self._graph_translate_y_enable = True, True
        self._graph_scale_x_enable, self._graph_scale_y_enable = True, True

    @property
    def tx(self):
        return self._graph_translate_x

    @property
    def ty(self):
        return self._graph_translate_y

    @property
    def sx(self):
        return self._graph_scale_x

    @property
    def sy(self):
        return self._graph_scale_y

    @property
    def hover_point(self):
        return self._graph_hover_point

    def on_hover(self, point):
        self._graph_hover_point = point

    def on_track_start(self, point):
        self._graph_track_start_point = point

        self.update()

        self._widget._refresh_widget_all_()

    def on_track_move(self, point):
        d_p = point-self._graph_track_start_point
        d_t_x, d_t_y = d_p.x(), d_p.y()

        self.update_matrix_by_track(d_t_x, d_t_y)
        self.update_transformation()

        if point is not None:
            self._graph_track_start_point = point
        else:
            self._graph_track_start_point = QtCore.QPoint(0, 0)

        self.update()

        self._widget._refresh_widget_all_()

    def on_track_end(self, point):
        self._graph_track_start_point = point

        self.update()

        self._widget._refresh_widget_all_()

    def on_zoom(self, point, delta):

        if delta > 0:
            d_s_x, d_s_y = 1+self._graph_scale_radix_x, 1+self._graph_scale_radix_y
        else:
            d_s_x, d_s_y = 1/(1+self._graph_scale_radix_x), 1/(1+self._graph_scale_radix_y)

        c_x, c_y = point.x(), point.y()

        self.update_matrix_by_zoom(c_x, c_y, d_s_x, d_s_y)
        self.update_transformation()
        if point is not None:
            self._graph_track_start_point = point
        else:
            self._graph_track_start_point = QtCore.QPoint(0, 0)

        self.update()

        self._widget._refresh_widget_all_()

    def translate_to(self, x, y):
        o_x_0, o_y_0, o_x_1, o_y_1, o_r_w, o_r_h = self.get_rect_args()
        x_0, y_0 = x, y
        x_1, y_1 = x+o_r_w, y+o_r_h

        self.update_rect_by_points(x_0, y_0, x_1, y_1)

    def scale_to(self, s_x, s_y):
        x_0, y_0 = self._graph_translate_x, self._graph_translate_y
        x_1, y_1 = x_0+self._graph_basic_w*s_x, y_0+self._graph_basic_h*s_y

        self.update_rect_by_points(x_0, y_0, x_1, y_1)

    def scale_to_origin(self, s_x, s_y):
        s_w_0, s_h_0 = self._graph_basic_w*s_x, self._graph_basic_h*s_y
        x_0, y_0 = 0, 0
        x_1, y_1 = s_w_0, s_h_0

        self.update_rect_by_points(x_0, y_0, x_1, y_1)

    def get_translate(self):
        return self._graph_translate_x, self._graph_translate_y

    def get_scale(self):
        return self._graph_scale_x, self._graph_scale_y

    def get_transformation(self):
        return self._graph_translate_x, self._graph_translate_y, self._graph_scale_x, self._graph_scale_y
