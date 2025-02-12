# coding=utf-8
import enum
# qt
from ...core.wrap import *

from ... import core as _qt_core

from ... import graph_models as _graph_models

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

    def _init_graph_base_def_(self, widget):
        self._widget = widget

        self._graph_model = _graph_models.ModelForBaseGraph(self._widget)

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _refresh_widget_all_(self):
        raise NotImplementedError()

    def _do_graph_hover_move_(self, event):
        self._graph_model.on_hover(event.pos())

    # action
    def _do_graph_track_start_(self, event):
        self._graph_model.on_track_start(event.pos())

    def _do_graph_track_move_(self, event):
        self._graph_model.on_track_move(event.pos())

    def _do_graph_track_end_(self, event):
        self._graph_model.on_track_end(event.pos())

    # zoom
    def _do_graph_zoom_(self, event):
        self._graph_model.on_zoom(event.pos(), event.angleDelta().y())


class _AbsQtSbjRectSelectDef(object):
    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _init_sbj_rect_selection_def_(self, widget):
        self._widget = widget

        self._action_rect_select_point_start = QtCore.QPoint(0, 0)
        self._rect_selection_rect = qt_rect(
            0, 0, 0, 0
        )

    # rect select
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

    def _do_rect_select_end_auto_(self, event):
        if self._widget._is_action_flag_match_(
            self._widget.ActionFlag.RectSelectMove
        ):
            if self._node_selection_flag == self._widget.NGSelectionFlag.Separate:
                self._widget._selection_separate_fnc_(self._get_rect_intersects_nodes_())
            elif self._node_selection_flag == self._widget.NGSelectionFlag.Add:
                self._widget._selection_add_fnc_(self._get_rect_intersects_nodes_())
            elif self._node_selection_flag == self._widget.NGSelectionFlag.Sub:
                self._widget._selection_sub_fnc_(self._get_rect_intersects_nodes_())
            elif self._node_selection_flag == self._widget.NGSelectionFlag.Invert:
                self._widget._selection_invert_fnc_(self._get_rect_intersects_nodes_())
        elif self._widget._is_action_flag_match_(self._widget.ActionFlag.PressClick):
            self._widget._selection_clear_fnc_()
        #
        self._refresh_widget_draw_()

    def _get_rect_intersects_nodes_(self):
        node_widgets = []
        for i_node_widget in self._widget._graph_nodes:
            if self._rect_selection_rect.intersects(
                i_node_widget._node_global_selection_rect
            ) is True:
                node_widgets.append(i_node_widget)
        return node_widgets


class AbsQtGraphSbjDef(_AbsQtSbjRectSelectDef):
    NG_NODE_CLS = None
    NG_CONNECTION_CLS = None

    @classmethod
    def _filter_nodes_on_left_(cls, node_widget, sbj_list):
        list_ = []
        x = node_widget.x()
        for i_node_widget in sbj_list:
            if i_node_widget != node_widget:
                i_x = i_node_widget.x()
                if i_x < x:
                    list_.append(i_node_widget)
        return list_

    def _init_sbj_base_def_(self, widget):
        self._widget = widget
        self._init_sbj_rect_selection_def_(widget)

        self._graph_nodes = []
        self._graph_selection_nodes = []

        self._ng_graph_connections = []
        self._ng_graph_connections_selected = []

        self._graph_current_node = None
        self._graph_hover_node = None

        self._node_selection_flag = _NGSelectionFlag.Separate

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _create_node_(self, *args, **kwargs):
        raise NotImplementedError()

    def _clear_graph_(self):
        for i in self._graph_nodes:
            i._do_delete_()

        self._widget.unsetCursor()

        self._graph_selection_nodes = []
        self._graph_nodes = []

        self._ng_graph_connections = []
        self._ng_graph_connections_selected = []

        self._graph_current_node = None
        self._graph_hover_node = None

    def _create_connection_(self, *args, **kwargs):
        raise NotImplementedError()

    def _get_ng_graph_nodes_(self):
        return self._graph_nodes

    def _get_graph_selected_node_count_(self):
        return len(self._graph_selection_nodes)

    def _get_selected_nodes_(self):
        return self._graph_selection_nodes

    def _graph_update_nodes_(self):
        for i_ng_node in self._get_ng_graph_nodes_():
            i_ng_node._refresh_widget_all_()

    def _do_graph_frame_scale_for_(self, nodes):
        x_0, y_0, x_1, y_1, w_0, h_0 = self._widget._graph_model._compute_nodes_basic_geometry_args_for(nodes)

        w_1, h_1 = self._widget.width(), self._widget.height()
        if w_0 > h_0:
            s_x_0 = float(w_1)/float(w_0)
        else:
            s_x_0 = float(h_1)/float(h_0)

        self._widget._graph_model.scale_to_origin(
            s_x_0*.875, s_x_0*.875
        )

    def _do_graph_frame_translate_for_(self, nodes):
        x_0, y_0, x_1, y_1, w_0, h_0 = self._widget._graph_model._compute_nodes_basic_geometry_args_for(nodes)
        sx, sy = self._widget._graph_model.sx, self._widget._graph_model.sy

        s_x_0, s_y_0 = x_0*sx, y_0*sy
        s_w_0, s_h_0 = w_0*sx, h_0*sy
        w_1, h_1 = self._widget.width(), self._widget.height()
        x, y = -s_x_0+(w_1-s_w_0)/2, -s_y_0+(h_1-s_h_0)/2
        self._widget._graph_model.translate_to(
            x, y
        )

    def _get_hovered_node_(self):
        point = self._widget._graph_model.hover_point
        for i in self._graph_nodes:
            if i._node_global_selection_rect.contains(point):
                return i

    def _do_frame_nodes_for_(self, nodes):
        # scale
        self._do_graph_frame_scale_for_(nodes)
        # translate
        self._do_graph_frame_translate_for_(nodes)

    def _on_graph_node_frame_auto_(self):
        if self._graph_selection_nodes:
            nodes = self._graph_selection_nodes
        else:
            node_widget = self._get_hovered_node_()
            if node_widget:
                nodes = [node_widget]
            else:
                nodes = self._graph_nodes

        self._do_frame_nodes_for_(nodes)

    def _update_current_node_(self, node_widget):
        self._graph_current_node = node_widget
        if node_widget is not None:
            self._graph_current_node.raise_()

        self._refresh_widget_draw_()

    def _update_hover_node_(self, node_widget):
        self._graph_hover_node = node_widget
        if node_widget is not None:
            self._graph_hover_node.raise_()

        self._refresh_widget_draw_()

    def _get_ng_graph_node_current_name_text_(self):
        if self._graph_current_node is not None:
            return self._graph_current_node._get_name_text_()

    def _get_node_selection_flag_(self):
        if _qt_core.QtApplication.is_shift_modifier():
            return self._widget.NGSelectionFlag.Add
        elif _qt_core.QtApplication.is_ctrl_modifier():
            return self._widget.NGSelectionFlag.Sub
        elif _qt_core.QtApplication.is_ctrl_shift_modifier():
            return self._widget.NGSelectionFlag.Invert
        else:
            return self._widget.NGSelectionFlag.Separate

    # click
    def _do_node_press_start_for_(self, node_widget):
        self._node_selection_flag = self._get_node_selection_flag_()
        self._update_current_node_(node_widget)

    def _do_node_press_for_(self, node_widget):
        if self._get_graph_selected_node_count_() == 0:
            self._selection_separate_fnc_([node_widget])

    def _do_node_press_end_for_(self, node_widget):
        if self._widget._is_action_flag_match_(
            self._widget.ActionFlag.NGNodePressMove
        ) is False:
            if self._node_selection_flag == self._widget.NGSelectionFlag.Separate:
                self._selection_separate_fnc_([node_widget])
            elif self._node_selection_flag == self._widget.NGSelectionFlag.Add:
                self._selection_add_fnc_([node_widget])
            elif self._node_selection_flag == self._widget.NGSelectionFlag.Sub:
                self._selection_sub_fnc_([node_widget])
            elif self._node_selection_flag == self._widget.NGSelectionFlag.Invert:
                self._selection_invert_fnc_([node_widget])

    # move
    def _do_node_press_start_for_any_action_(self):
        [i._push_last_properties_() for i in self._graph_selection_nodes]

    def _do_node_press_move_for_(self, node_widget, d_point):
        if node_widget._is_selected_() is True:
            self._graph_node_move_together_fnc_(node_widget, d_point)
        else:
            self._separate_move_node_(node_widget)

    def _graph_node_move_together_fnc_(self, node_widget, d_point):
        self._update_current_node_(node_widget)

        if self._graph_current_node is not None:
            p_0 = node_widget.pos()
            for i_node_widget in self._graph_selection_nodes:
                if i_node_widget != self._graph_current_node:
                    i_p = i_node_widget.pos()
                    i_offset_point = p_0-i_p
                    i_node_widget._move_by_point_(d_point, i_offset_point)
                else:
                    i_node_widget._move_by_point_(d_point)

    def _separate_move_node_(self, node_widget):
        self._selection_separate_fnc_([node_widget])

    # resize
    def _do_node_press_move_trim_for_(self, node_widget, d_point, start_size, flag):
        if node_widget._is_selected_() is True:
            self._together_trim_nodes_(node_widget, d_point, start_size, flag)
        else:
            self._separate_trim_node_(node_widget, d_point, start_size, flag)

    def _together_trim_nodes_(self, node_widget, d_point, start_size, flag):
        # if self._graph_current_node is not None:
        if flag == self._widget.ActionFlag.NGSbjTrimLeft:
            p_0 = node_widget.pos()
            node_widget._trim_left_fnc_(d_point)
            # nodes = self._filter_nodes_on_left_(node_widget, self._graph_selection_nodes)
            # print nodes
        elif flag == self._widget.ActionFlag.NGSbjTrimRight:
            node_widget._trim_right_fnc_(d_point, start_size)

    def _separate_trim_node_(self, node_widget, d_point, start_size, flag):
        node_widget.raise_()
        if flag == self._widget.ActionFlag.NGSbjTrimLeft:
            node_widget._trim_left_fnc_(d_point)
        elif flag == self._widget.ActionFlag.NGSbjTrimRight:
            node_widget._trim_right_fnc_(d_point, start_size)

    # scale
    def _do_node_press_scale_for_(self, node_widget, d_point, start_size, flag):
        if node_widget._is_selected_() is True:
            self._together_scale_nodes_(node_widget, d_point, start_size, flag)
        else:
            self._separate_scale_node_(node_widget, d_point, start_size, flag)

    def _together_scale_nodes_(self, node_widget, d_point, start_size, flag):
        # if self._graph_current_node is not None:
        if flag == self._widget.ActionFlag.NGSbjScaleLeft:
            p_0 = node_widget.pos()
            node_widget._scale_left_fnc_(d_point)
            # nodes = self._filter_nodes_on_left_(node_widget, self._graph_selection_nodes)
            # print nodes
        elif flag == self._widget.ActionFlag.NGSbjScaleRight:
            node_widget._scale_right_fnc_(d_point, start_size)

    def _separate_scale_node_(self, node_widget, d_point, start_size, flag):
        node_widget.raise_()
        if flag == self._widget.ActionFlag.NGSbjScaleLeft:
            node_widget._scale_left_fnc_(d_point)
        elif flag == self._widget.ActionFlag.NGSbjScaleRight:
            node_widget._scale_right_fnc_(d_point, start_size)

    # transformation
    def _push_node_transformation_action_fnc_(self, node_widget=None, flag=None):
        cmd_data = []
        for i_node_widget in self._graph_selection_nodes:
            i_coord, i_last_coord = i_node_widget._get_basic_coord_(), i_node_widget._get_basic_last_coord_()
            if i_coord != i_last_coord:
                cmd_data.append(
                    (flag, (i_node_widget, i_coord, i_last_coord))
                )

        if node_widget is not None:
            coord, last_coord = node_widget._get_basic_coord_(), node_widget._get_basic_last_coord_()
            if coord != last_coord:
                cmd_data.append(
                    (flag, (node_widget, coord, last_coord))
                )
        
        if cmd_data:
            self._push_general_action_fnc_(cmd_data)

    # selection
    def _selection_clear_fnc_(self):
        self._selection_separate_fnc_([])

    def _selection_separate_fnc_(self, node_widgets):
        cmd_data = []

        node_widgets = node_widgets or []
        for i_node_widget in self._graph_selection_nodes:
            if i_node_widget not in node_widgets:
                cmd_data.append(
                    ('selection', (i_node_widget, False))
                )

        for i_node_widget in node_widgets:
            if i_node_widget not in self._graph_selection_nodes:
                cmd_data.append(
                    ('selection', (i_node_widget, True))
                )

        if node_widgets:
            self._graph_current_node = node_widgets[0]
        else:
            self._graph_current_node = None

        self._push_general_action_fnc_(cmd_data)

    def _selection_add_fnc_(self, node_widgets):
        cmd_data = []

        for i_node_widget in node_widgets:
            if i_node_widget not in self._graph_selection_nodes:
                cmd_data.append(
                    ('selection', (i_node_widget, True))
                )

        self._push_general_action_fnc_(cmd_data)

    def _selection_sub_fnc_(self, node_widgets):
        cmd_data = []

        for i_node_widget in node_widgets:
            if i_node_widget in self._graph_selection_nodes:
                cmd_data.append(
                    ('selection', (i_node_widget, False))
                )

        self._push_general_action_fnc_(cmd_data)

    def _selection_invert_fnc_(self, node_widgets):
        cmd_data = []

        for i_node_widget in node_widgets:
            if i_node_widget in self._graph_selection_nodes:
                cmd_data.append(
                    ('selection', (i_node_widget, False))
                )
            elif i_node_widget not in self._graph_selection_nodes:
                cmd_data.append(
                    ('selection', (i_node_widget, True))
                )

        self._push_general_action_fnc_(cmd_data)

    def _push_general_action_fnc_(self, cmd_data):
        if cmd_data:
            c = _undo_command.QtGraphActionCommand(
                cmd_data
            )
            c._graph = self
            self._widget._undo_stack.push(c)

    def _selection_all_fnc_(self):
        self._selection_add_fnc_(self._graph_nodes)


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
