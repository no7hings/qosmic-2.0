# coding=utf-8
import os.path
# qt
from ...core.wrap import *

from ... import core as _qt_core

from ..general import node as _gnl_node

from ..general import graph as _gnl_graph


class QtImageNode(_gnl_node.QtGeneralNode):
    def __init__(self, *args, **kwargs):
        super(QtImageNode, self).__init__(*args, **kwargs)

        self._ng_draw_name_h_basic = 48
        self._ng_draw_font_h_basic = 8

        self._image_line_height = 0

    def paintEvent(self, event):
        painter = _qt_core.QtNGPainter(self)

        offset = 0

        painter._set_node_frame_draw_by_rect_(
            self._node_rect_frame,
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
                font=_qt_core.QtFont.generate(size=self._ng_draw_font_h),
                text_color=_qt_core.QtRgba.Text,
                text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                offset=offset,
                word_warp=True
            )

        if self._image_path is not None:
            painter._draw_image_by_rect_(
                self._node_rect_frame,
                self._image_path,
                offset=offset
            )

    def _refresh_widget_draw_geometry_(self):
        rect = self.rect()

        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()

        b_w_0 = self._ng_draw_border_w

        x_0, y_0 = x+b_w_0/2, y+b_w_0/2
        w_0, h_0 = w-b_w_0, h-b_w_0

        self._set_frame_draw_rect_(
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
        self._node_rect_frame.setRect(
            f_x, f_y, f_w, f_h
        )

    def _set_image_line_height_(self, h):
        self._image_line_height = h

    def _get_image_line_height_(self):
        return self._image_line_height


class QtImageGraph(_gnl_graph.QtGeneralNodeGraph):
    NG_NODE_CLS = QtImageNode

    def __init__(self, *args, **kwargs):
        super(QtImageGraph, self).__init__(*args, **kwargs)

        self._ng_graph_image_scale = 0.2

        self._ng_graph_layout_flag = self.NGLayoutFlag.Line

    # widget
    def paintEvent(self, event):
        painter = _qt_core.QtNGPainter(self)
        x, y = 0, 0
        width, height = self.width(), self.height()

        rect = QtCore.QRect(
            x, y, width, height
        )

        if self._ng_draw_graph_grid_enable is True:
            painter._draw_grid_(
                rect,
                axis_dir=(self._grid_dir_x, self._grid_dir_y),
                grid_scale=(self._graph_model.sx, self._graph_model.sy),
                grid_size=(self._grid_width, self._grid_height),
                translate=(self._graph_grid_translate_x, self._graph_grid_translate_y),
                grid_offset=(self._grid_offset_x, self._grid_offset_y),
                border_color=self._grid_border_color
            )

        if self._is_action_flag_match_(
                self.ActionFlag.RectSelectMove
        ):
            painter._draw_dotted_frame_(
                self._rect_selection_rect,
                border_color=_qt_core.QtRgba.BorderSelect,
                background_color=_qt_core.QtRgba.Transparent
            )

    def _set_graph_universe_(self, universe):
        self._graph_universe = universe

        obj = self._graph_universe.get_objs()
        for i_obj in obj:
            i_image_path = i_obj.get('image')
            if i_image_path:
                i_ng_node = self._create_node_()
                i_ng_node._set_unr_obj_(i_obj)
                i_ng_node._set_type_text_(
                    i_obj.type_name
                )
                i_ng_node._set_name_text_(
                    i_obj.name
                )
                i_ng_node._set_name_icon_text_(
                    i_obj.type_name
                )

                i_ng_node._set_image_path_(i_image_path)
                i_w, i_h = i_ng_node._get_image_file_size_()

                i_width, i_height = i_w*self._ng_graph_image_scale, i_h*self._ng_graph_image_scale
                i_width -= 1
                i_height -= 2
                i_ng_node._set_basic_size_(
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
            self._on_graph_node_frame_auto_()
            #
            l_t.stop()

        objs = self._graph_universe.get_objs()
        if objs:
            ng_nodes = []
            for i_obj in objs:
                i_image_path = i_obj.get('image')
                if i_image_path:
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
        ng_nodes = self._graph_nodes
        xs_0, ys_0 = [i.x() for i in ng_nodes], [i.y() for i in ng_nodes]
        xs_1, ys_1 = [i.x()+i._node_basic_w for i in ng_nodes], [i.y()+i._node_basic_h for i in ng_nodes]
        x_0, y_0 = min(xs_0), min(ys_0)
        x_1, y_1 = max(xs_1), max(ys_1)
        w_0, h_0 = x_1-x_0, y_1-y_0
        return x_0, y_0, w_0, h_0

    @classmethod
    def _get_ng_graph_image_size_(cls, ng_nodes):
        return sum([i._node_basic_w for i in ng_nodes]), max([i._node_basic_h for i in ng_nodes])

    def _save_ng_graph_image_to_(self, file_path):
        ng_nodes = self._graph_nodes
        scale = 10
        m = 48
        w, h = self._get_ng_graph_image_size_(ng_nodes)
        w_, h_ = w*scale+m*2, h*scale+m*2
        size = QtCore.QSize(w_, h_)
        pixmap = QtGui.QPixmap(size)
        pixmap.fill(QtGui.QColor(55, 55, 55, 255))
        painter = _qt_core.QtPainter(pixmap)
        rect = pixmap.rect()
        ng_nodes = self._set_ng_graph_nodes_sort_by_(ng_nodes, sort_key='x')
        offset = 0
        x_0, y_0 = rect.x()+m, rect.y()+m
        for i_ng_node in ng_nodes:
            i_t_h = i_ng_node._ng_draw_name_h_basic*scale
            i_i_w, i_i_h = i_ng_node._node_basic_w*scale, i_ng_node._node_basic_h*scale-i_t_h
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
                font=_qt_core.QtFont.generate(size=i_t_font_size),
                text_color=_qt_core.QtRgba.Text,
                text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                offset=offset,
                word_warp=True
            )
            i_i_rect = QtCore.QRect(
                x_0, h_-i_i_h-m, i_i_w, i_i_h
            )
            i_image_path = i_ng_node._get_image_path_()
            # painter.fillRect(i_i_rect, QtGui.QColor(255, 0, 255))
            painter._draw_image_by_rect_(
                i_i_rect,
                i_image_path,
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

    def _do_clear_(self):
        for i in self._graph_nodes:
            i.deleteLater()

        self._graph_nodes = []
        self._graph_selection_nodes = []
