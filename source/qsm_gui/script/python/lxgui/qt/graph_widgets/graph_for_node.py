# coding=utf-8
import functools

import enum

import collections

import lxbasic.core as bsc_core
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import core as _qt_core

from .. import abstracts as _qt_abstracts
# qt widgets
from ..widgets import utility as _qt_wgt_utility

from ..widgets import entry_frame as _qt_wgt_entry_frame

from ..widgets import item_for_tree as _qt_wgt_item_for_tree

from ..widgets import view_for_tree as _qt_wgt_view_for_tree

from . import graph_base as _graph_base

from . import sbj_node as _sbj_node

from . import sbj_connection as _sbj_connection

from . import undo_command as _undo_command


class AbsQtActionFrameDef(object):
    def _set_action_frame_def_init_(self, widget):
        pass

    # action frame select
    def _set_action_frame_execute_(self, event):
        raise NotImplementedError()


class AbsQtNGDrawNodeDef(object):
    def _set_ng_draw_node_def_init_(self, widget):
        self._widget = widget


class QtNodeGraph(
    QtWidgets.QWidget,

    _qt_abstracts.AbsQtDrawGridDef,
    _graph_base.AbsQtGraphSbjDef,

    _qt_abstracts.AbsQtActionBaseDef,
    _graph_base.AbsQtActionForRectSelectDef,
    AbsQtActionFrameDef,

    _graph_base.AbsQtGraphBaseDef,
    _graph_base.AbsQtGraphDrawBaseDef,

    _graph_base.AbsQtNGUniverseDef
):
    NG_NODE_CLS = _sbj_node.QtNode
    NG_CONNECTION_CLS = _sbj_connection.QtConnection
    #
    NGLayoutFlag = _graph_base._NGLayoutFlag
    NGSelectionFlag = _graph_base._NGSelectionFlag
    
    # frame
    def _refresh_widget_all_(self):
        # self._update_graph_geometry_()

        self._update_graph_draw_args_(
            self._graph_model.tx, self._graph_model.ty
        )
        self._refresh_widget_draw_geometry_(self.rect())
        self._update_graph_nodes_()

        self._refresh_widget_draw_()

    def _refresh_widget_draw_geometry_(self, rect):
        self._connection_sbj_layer.setGeometry(rect)

    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtNodeGraph, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        #
        self._init_action_base_def_(self)
        self._init_action_for_rect_select_def_(self)
        self._set_action_frame_def_init_(self)
        #
        self._init_sbj_base_def_(self)
        #
        self._init_graph_base_def_(self)
        self._init_graph_draw_base_def_(self)
        #
        self._init_draw_grid_def_(self)
        self._grid_border_color = 63, 63, 63, 255
        self._grid_axis_lock_x, self._grid_axis_lock_y = 1, 1
        self._grid_dir_x, self._grid_dir_y = self._grid_translate_direction_x, self._grid_translate_direction_y

        self._connection_sbj_layer = _graph_base.QtSbjLayer(self)

        self._ng_graph_layout_flag = self.NGLayoutFlag.Dependent

        self._init_universe_def_(self)
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
            (self._select_all_nodes_, 'Ctrl+A')
        ]
        for i_fnc, i_shortcut in actions:
            i_action = QtWidgets.QAction(self)
            # noinspection PyUnresolvedReferences
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
                    self._add_action_modifier_flag_(
                        self.ActionFlag.KeyControlPress
                    )
                elif event.modifiers() == QtCore.Qt.ShiftModifier:
                    self._add_action_modifier_flag_(
                        self.ActionFlag.KeyShiftPress
                    )
                elif event.modifiers() == QtCore.Qt.AltModifier:
                    self._add_action_modifier_flag_(
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
                    if self._is_action_flag_match_(
                        self.ActionFlag.NGNodePressClick,
                        self.ActionFlag.NGNodeAnyAction
                    ) is False:
                        self._set_action_flag_(
                            self.ActionFlag.RectSelectClick
                        )
                        self._do_rect_select_start_(event)
                #
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    self._set_action_flag_(
                        self.ActionFlag.NGGraphTrackClick
                    )
                    self._do_graph_track_start_(event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    if self._is_action_flag_match_(
                        self.ActionFlag.NGNodePressClick, self.ActionFlag.NGNodePressMove,
                        self.ActionFlag.NGNodeAnyAction
                    ) is False:
                        self._set_action_flag_(
                            self.ActionFlag.RectSelectMove
                        )
                        self._do_rect_select_move_(event)
                elif event.buttons() == QtCore.Qt.RightButton:
                    pass
                elif event.buttons() == QtCore.Qt.MidButton:
                    self._set_action_flag_(
                        self.ActionFlag.NGGraphTrackMove
                    )
                    self._do_graph_track_move_(event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self._do_rect_select_end_(event)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    self._do_graph_track_end_(event)
                else:
                    event.ignore()
                #
                self._clear_all_action_flags_()
            #
            elif event.type() == QtCore.QEvent.Wheel:
                self._do_graph_zoom_(event)
                return True
            #
            elif event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                parent = self.parent()
                if isinstance(parent, _qt_wgt_entry_frame.QtEntryFrame):
                    parent._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                parent = self.parent()
                if isinstance(parent, _qt_wgt_entry_frame.QtEntryFrame):
                    parent._set_focused_(False)
        return False

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
        if self._ng_draw_graph_grid_mark_enable is True:
            painter._draw_grid_mark_(
                rect,
                (self._grid_dir_x, self._grid_dir_y),
                (self._grid_width, self._grid_height),
                (self._graph_grid_translate_x, self._graph_grid_translate_y),
                (self._grid_offset_x, self._grid_offset_y),
                (self._graph_model.sx, self._graph_model.sy),
                (self._grid_value_offset_x, self._grid_value_offset_y),
                self._grid_mark_border_color,
                self._grid_value_show_mode
            )
        if self._ng_draw_graph_grid_axis_enable is True:
            painter._draw_grid_axis_(
                rect,
                (self._grid_dir_x, self._grid_dir_y),
                (self._graph_grid_translate_x, self._graph_grid_translate_y),
                (self._grid_offset_x, self._grid_offset_y),
                (self._grid_axis_lock_x, self._grid_axis_lock_y),
                (self._grid_axis_border_color_x, self._grid_axis_border_color_y)
            )

        if self._is_action_flag_match_(
            self.ActionFlag.RectSelectMove
        ):
            painter._draw_dotted_frame_(
                self._rect_selection_rect,
                border_color=_qt_core.QtRgba.BorderSelect,
                background_color=_qt_core.QtRgba.Transparent
            )

        infos = collections.OrderedDict(
            [
                (
                    'translate', '{}, {}'.format(
                        self._graph_model.tx,
                        self._graph_model.ty
                    )
                ),
                (
                    'scale', '{}, {}'.format(
                        self._graph_model.sx,
                        self._graph_model.sy
                    )
                ),
                ('action flag', str(self._get_action_flag_())),
                ('modifier action flag', str(', '.join(map(str, self._get_action_mdf_flags_())))),
            ]
        )

        key_text_width = _qt_core.GuiQtText.get_draw_width_maximum(
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
    def _set_graph_universe_(self, universe):
        self._graph_universe = universe
        objs = self._graph_universe.get_objs()
        for i_obj in objs:
            i_ng_node = self._create_node_()
            i_ng_node._set_unr_obj_(i_obj)
            i_ng_node._set_type_text_(
                i_obj.type_name
            )
            i_ng_node._set_name_text_(
                i_obj.name
            )
            i_ng_node._set_icon_by_text_(
                i_obj.type_name
            )
            i_ng_node._set_tool_tip_(['path: "{}"'.format(i_obj.path)])
            # i_image_path = i_obj.get('image')
            # if i_image_path:
            #     i_ng_node._set_image_path_(i_image_path)

            i_obj.set_gui_ng_graph_node(i_ng_node)

        connections = self._graph_universe.get_connections()
        for i_connection in connections:
            i_ng_connection = self._create_connection_()
            i_obj_src = i_connection.get_source_obj()
            i_obj_tgt = i_connection.get_target_obj()
            i_obj_src.get_gui_ng_graph_node()._add_start_connection_(i_ng_connection)
            i_obj_tgt.get_gui_ng_graph_node()._add_end_connection_(i_ng_connection)

    def _set_ng_show_by_universe_(self, *args, **kwargs):
        def frame_fnc_():
            self._do_frame_nodes_auto_()
            t.stop()

        if args:
            obj_path = args[0]
        else:
            obj_path = None

        if obj_path is not None:
            objs = [self._graph_universe.get_obj(obj_path)]
        else:
            objs = self._graph_universe.get_basic_source_objs()
        #
        if objs:
            ng_nodes = [i.get_gui_ng_graph_node() for i in objs]
            idx = 0
            for i_ng_node in ng_nodes:
                i_ng_node._move_to_coord_(
                    0, idx*192
                )
                idx += 1
            #
            ng_nodes_0 = self._layout_nodes_by_connection_for_(
                ng_nodes,
                size=(192, 192)
            )
            ng_nodes.extend(ng_nodes_0)
            for i_ng_node in self._get_ng_graph_nodes_():
                if i_ng_node not in ng_nodes:
                    i_ng_node._move_to_coord_(
                        0, idx*192
                    )
                    idx += 1

        t = QtCore.QTimer(self)
        t.timeout.connect(frame_fnc_)
        t.start(50)

    def _set_ng_universe_node_add_(self, *args, **kwargs):
        pass

    @classmethod
    def _get_ng_graph_layout_args_(cls, ng_nodes):
        xs_0, ys_0 = [i.x() for i in ng_nodes], [i.y() for i in ng_nodes]
        xs_1, ys_1 = [i.x() for i in ng_nodes], [i.y()+i.height() for i in ng_nodes]
        x_0, y_0 = min(xs_0), min(ys_0)
        x_1, y_1 = max(xs_1), max(ys_1)
        _w_0, _h_0 = x_1-x_0, y_1-y_0
        return x_0, y_0, x_1, y_1

    # layout
    def _layout_nodes_by_connection_for_(self, nodes, size, direction=('r-l', 't-b')):
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

        obj_stack = []
        o2c_dict = {}
        c2o_dict = {}
        #
        x, y, w, h = nodes[0]._get_geometry_args_()
        [rcs_fnc_(i._ng_node_obj, 0) for i in nodes]

        # objs = [i._ng_node_obj for i in nodes]
        # basic_source_objs = self._graph_universe.get_basic_source_objs(objs)
        ys = []
        for i in nodes:
            i_x, i_y, i_w, i_h = i._get_geometry_args_()
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
                        i_obj = self._graph_universe.get_obj(i_obj_path)
                        i_x = s_x
                        if dir_y == 'b-t':
                            i_y = s_y-i_row*h
                        elif dir_y == 't-b':
                            i_y = s_y+i_row*h
                        else:
                            raise ValueError()
                        #
                        i_ng_node = i_obj.get_gui_ng_graph_node()
                        i_ng_node._move_to_coord_(
                            i_x, i_y
                        )
        return [i.get_gui_ng_graph_node() for i in obj_stack]

    @classmethod
    def _set_ng_graph_nodes_sort_by_(cls, nodes, sort_key=None):
        """
        :param nodes:
        :param sort_key: "x", "-x" / "height" / "-height"
        :return:
        """
        keys = []
        list_ = []
        query_dict = {}
        for i_ng_node in nodes:
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

    def _set_ng_graph_node_layout_as_line_(self, nodes, sort_key=None):
        if sort_key is not None:
            nodes = self._set_ng_graph_nodes_sort_by_(
                nodes,
                sort_key=sort_key
            )

        x_0, y_0, x_1, y_1 = self._get_ng_graph_layout_args_(nodes)

        for seq, i_ng_node in enumerate(nodes):
            i_w, i_h = i_ng_node.width(), i_ng_node.height()

            y_0 = y_1-i_h

            i_x, i_y = x_0, y_0
            i_ng_node._move_to_coord_(
                i_x, i_y
            )

            x_0 += i_w
            x_1 += i_w

    def _layout_nodes_for_(self, nodes, sort_key='x'):
        if nodes:
            if self._ng_graph_layout_flag == self.NGLayoutFlag.Dependent:
                x, y, w, h = nodes[0]._get_geometry_args_()
                self._layout_nodes_by_connection_for_(
                    nodes,
                    size=(w, w)
                )
                self._refresh_widget_all_()
            elif self._ng_graph_layout_flag == self.NGLayoutFlag.Line:
                self._set_ng_graph_node_layout_as_line_(
                    nodes,
                    sort_key=sort_key
                )

    # sbj
    def _create_node_(self, *args, **kwargs):
        ng_node = self.NG_NODE_CLS(self)
        self._graph_nodes.append(ng_node)
        ng_node._set_graph_(self)
        return ng_node

    def _create_connection_(self, *args, **kwargs):
        ng_connection = self.NG_CONNECTION_CLS(self._connection_sbj_layer)
        self._ng_graph_connections.append(ng_connection)
        ng_connection._set_graph_(self)
        return ng_connection

    # action frame select
    def _set_action_frame_execute_(self, event):
        self._do_frame_nodes_auto_()

    def _set_ng_action_graph_frame_(self):
        self._do_frame_nodes_auto_()

    def _set_ng_action_graph_layout_selection_(self, sort_key='x'):
        if self._graph_select_nodes:
            self._do_node_press_start_for_any_action_()
            self._layout_nodes_for_(
                self._graph_select_nodes, sort_key
            )
            self._do_node_press_end_for_any_action_()


class _QtNGTreeNode(
    _qt_wgt_item_for_tree.QtTreeWidgetItem
):
    def __init__(self, *args, **kwargs):
        super(_QtNGTreeNode, self).__init__(*args, **kwargs)

        self._ng_node_obj = None

    def _get_node_(self):
        return self._ng_node_obj

    def __str__(self):
        return str(self._ng_node_obj)


class _QtNGTree(
    _qt_wgt_view_for_tree.QtTreeWidget,
    _graph_base.AbsQtNGUniverseDef
):
    QT_MENU_CLS = _qt_wgt_utility.QtMenu

    def _set_graph_universe_(self, universe):
        self.clear()
        self._graph_universe = universe
        objs = self._graph_universe.get_objs()
        for i_obj in objs:
            self._set_ng_universe_node_add_(i_obj)

    def _set_ng_show_by_universe_(self, *args, **kwargs):
        pass

    def __init__(self, *args, **kwargs):
        super(_QtNGTree, self).__init__(*args, **kwargs)
        self._init_universe_def_(self)

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
                gui_core.GuiIcon.get('node/group')
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
        else:
            pass
