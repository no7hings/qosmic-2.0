# coding=utf-8
import json

import copy
# gui
from ... import core as _gui_core
# qt
from ...core.wrap import *

from ... import core as _qt_core

from ... import abstracts as _qt_abstracts

from ...widgets import base as _qt_wgt_base

from ...widgets import entry_frame as _qt_wgt_entry_frame

from ..base import graph as _bsc_graph

from ..general import connection as _gnl_connection

from . import node as _node

from . import timeline as _timeline

from . import timehandle as _timehandle

from . import undo_command as _undo_command

from . import layer as _layer

from . import guide as _guide


class QtTrackGraph(
    QtWidgets.QWidget,

    _qt_abstracts.AbsQtActionBaseDef,
    _bsc_graph.AbsQtActionForRectSelectDef,

    _bsc_graph.AbsQtGraphBaseDef,
    _bsc_graph.AbsQtGraphSbjDef,

    _bsc_graph.AbsQtNGUniverseDef,
):
    NG_NODE_CLS = _node.QtTrackNode
    NG_CONNECTION_CLS = _gnl_connection.QtConnection

    NGSelectionFlag = _bsc_graph._NGSelectionFlag

    focus_accepted = qt_signal(bool)

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._graph_update_nodes_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        width, height = self.width(), self.height()

        rect = QtCore.QRect(
            x, y, width, height
        )
        # x axis for timeline
        self._track_timeline._update_from_graph_(
            rect,
            self._graph_model.tx, self._graph_model.sx
        )
        # y axis for layer
        self._track_layer._update_from_graph_(
            rect,
            self._graph_model.ty, self._graph_model.sy
        )
        # update sbj layer
        self._timetrack_trim_sbj_layer.setGeometry(
            self.rect()
        )
        self._connection_sbj_layer.setGeometry(
            self.rect()
        )
        self._track_layer.setGeometry(
            QtCore.QRect(
                self.x(), self.y(), self.width(), self.height()
            )
        )

        self._track_guide._refresh_widget_all_()

    def _graph_node_move_together_fnc_(self, sbj, d_point):
        p_0 = sbj.pos()
        p_1_x, p_1_y = d_point.x(), d_point.y()
        x_1 = self._track_stage_model.step_x_loc(p_1_x)
        d_point_step = QtCore.QPoint(x_1, p_1_y)
        for i_node in self._graph_select_nodes:
            if i_node != sbj:
                i_p = i_node.pos()
                i_offset_point = p_0-i_p
                i_node._move_by_point_(d_point_step, i_offset_point)
            else:
                i_node._move_by_point_(d_point_step)

    def _push_selects_nodes_transformation_changed_action_(self, sbj=None, flag=None):
        data = []
        nodes = list(self._graph_select_nodes)
        if sbj is not None:
            if sbj not in nodes:
                nodes += [sbj]

        for i_node in nodes:
            i_model, i_last_model = i_node._track_model, i_node._track_last_model
            if i_model != i_last_model:
                data.append(
                    (i_node, flag, (i_model, i_last_model))
                )

        if data:
            c = _undo_command.QtTrackActionCommand(
                data
            )
            c._graph = self
            self._widget._undo_stack.push(c)

    def _on_graph_node_bypass_auto_(self):
        data = []

        hover_node = self._get_hovered_node_()
        if hover_node is None:
            return

        bypass_flag = hover_node._track_model.is_bypass

        nodes = list(self._graph_select_nodes)
        if hover_node not in nodes:
            nodes.append(hover_node)

        if nodes:
            for i_node in nodes:
                i_model = i_node._track_model
                data.append(
                    # to target flag
                    (i_node, 'bypass', (i_model, not bypass_flag))
                )

        if data:
            c = _undo_command.QtTrackActionCommand(
                data
            )
            c._graph = self
            self._widget._undo_stack.push(c)

    def _on_graph_node_trash_auto_(self):
        data = []

        nodes = self._get_selected_nodes_()
        if nodes:
            for i_node in nodes:
                i_model = i_node._track_model
                data.append(
                    (i_node, 'trash', (i_model, True))
                )

        if data:
            c = _undo_command.QtTrackActionCommand(
                data
            )
            c._graph = self
            self._widget._undo_stack.push(c)

    def _on_graph_node_copy_(self):
        track_data = []
        nodes = self._get_selected_nodes_()
        if nodes:
            for i_node in nodes:
                i_model = i_node._track_model
                track_data.append(i_model.to_dict())

        data_string = json.dumps(
            dict(
                QSMTrackData=track_data
            )
        )
        _qt_core.QtUtil.copy_text_to_clipboard(data_string)
        
    def _on_graph_node_cut_(self):
        # use trash
        self._on_graph_node_trash_auto_()

    def _on_graph_node_paste_(self):
        
        current_layer_index = self._track_layer._get_current_index_()
        text = _qt_core.QtUtil.get_text_from_clipboard()
        if text.startswith('{"QSMTrackData": '):
            data = json.loads(text)
            track_data = data['QSMTrackData']
            for i_idx, i_data in enumerate(track_data):
                i_data_copy = dict(i_data)
                i_key_copy = '{}_copy'.format(i_data['key'])
                i_data_copy['key'] = i_key_copy
                i_layer_index = current_layer_index+i_idx
                i_data_copy['layer_index'] = i_layer_index

                self._create_node_(**i_data_copy)

    def _graph_node_update_transformation_fnc_(self, track_model):
        key = track_model.key
        if key in self._graph_node_dict:
            node_widget = self._graph_node_dict[key]
            node_widget._node_update_transformation_fnc_(track_model)

    def _graph_node_delete_fnc_(self, track_model):
        key = track_model.key
        if key in self._graph_node_dict:
            node_widget = self._graph_node_dict[key]
            # todo: remove fnc has bug
            if node_widget in self._graph_select_nodes:
                self._graph_select_nodes.remove(node_widget)
            if node_widget in self._graph_nodes:
                self._graph_nodes.remove(node_widget)

            self._track_guide._delete_node_(node_widget._track_model)
            node_widget._do_delete_()

    def _graph_node_create_fnc_(self, track_model):
        self._create_node_(
            **track_model.to_dict()
        )

    def _graph_bypass_node_fnc_(self, track_model, bypass_flag):
        key = track_model.key
        if key in self._graph_node_dict:
            node_widget = self._graph_node_dict[key]

            track_model.set_bypass(int(bypass_flag))

            node_widget._refresh_by_bypass_()

    def _graph_node_trash_fnc_(self, track_model, trash_flag):
        key = track_model.key
        if key in self._graph_node_dict:
            node_widget = self._graph_node_dict[key]

            track_model.set_trash(int(trash_flag))

            node_widget._refresh_by_trash_()

    def _update_stage_(self):
        self._track_guide._update_stage_()

    def _do_graph_frame_scale_for_(self, nodes):
        x_0, y_0, x_1, y_1, w_0, h_0 = self._graph_model._compute_nodes_basic_geometry_args_for(nodes)
        w_1, h_1 = self.width(), self.height()

        s_x_0 = float(w_1)/float(w_0)

        self._graph_model.scale_to_origin(
            s_x_0*.875, 1.0
        )

    def _do_graph_frame_translate_for_(self, nodes):
        x_0, y_0, x_1, y_1, w_0, h_0 = self._graph_model._compute_nodes_basic_geometry_args_for(nodes)
        sx, sy = self._graph_model.sx, self._graph_model.sy

        # scale to
        s_x_0, s_y_0 = x_0*sx, y_0*sy
        s_w_0, s_h_0 = w_0*sx, h_0*sy

        w_1, h_1 = self.width(), self.height()
        x, y = -s_x_0+(w_1-s_w_0)/2, -s_y_0+(h_1-s_h_0)/2
        self._graph_model.translate_to(
            x, y
        )

    def _do_layer_press_start_(self, event):
        p = event.pos()

        y = p.y()

        self._current_layer_index_tmp = self._track_stage_model.compute_layer_index(y)

    def _do_layer_press_end_auto_(self, event):
        if self._is_action_flag_match_(
            self.ActionFlag.PressClick
        ):
            self._track_layer._set_current_index_(self._current_layer_index_tmp)
            self._track_layer._refresh_widget_draw_()

    def __init__(self, *args, **kwargs):
        super(QtTrackGraph, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        self._init_action_base_def_(self)
        self._init_action_for_rect_select_def_(self)

        self._init_graph_base_def_(self)
        self._init_sbj_base_def_(self)

        self._init_universe_def_(self)

        self._graph_model._graph_scale_x_enable = True
        self._graph_model._graph_scale_y_enable = False

        self._track_guide = None
        self._track_stage_model = None

        self._graph_node_dict = {}

        self._track_timeline = None

        self._track_layer = None

        self._current_layer_index_tmp = None

        self._timetrack_trim_sbj_layer = _bsc_graph.QtSbjLayer(self)
        self._connection_sbj_layer = _bsc_graph.QtSbjLayer(self)
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

        self.installEventFilter(self)
        actions = [
            # frame
            (self._on_graph_node_frame_auto_, 'F'),
            # select
            (self._on_graph_node_select_all_, 'Ctrl+A'),
            # bypass
            (self._on_graph_node_bypass_auto_, 'D'),
            # trash
            (self._on_graph_node_trash_auto_, 'Delete'),
            # copy
            (self._on_graph_node_copy_, 'Ctrl+C'),
            # cut
            (self._on_graph_node_cut_, 'Ctrl+X'),
            # paste
            (self._on_graph_node_paste_, 'Ctrl+V')
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

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                pass
            
            # key press
            elif event.type() == QtCore.QEvent.KeyPress:
                # bypass
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
                elif event.modifiers() == (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier):
                    self._set_action_mdf_flags_(
                        [self.ActionFlag.KeyControlShiftPress]
                    )
            elif event.type() == QtCore.QEvent.KeyRelease:
                self._clear_action_modifier_flags_()
            #
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._is_action_flag_match_(
                        self.ActionFlag.NGNodePressClick,
                        self.ActionFlag.NGNodeAnyAction
                    ) is False:
                        self._set_action_flag_(
                            self.ActionFlag.PressClick
                        )
                        # rect select
                        self._do_rect_select_start_(event)

                        # layer press
                        self._do_layer_press_start_(event)
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
                if event.buttons() == QtCore.Qt.NoButton:
                    self._do_graph_hover_move_(event)
                elif event.buttons() == QtCore.Qt.LeftButton:
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
                    # rect select
                    self._do_rect_select_end_auto_(event)
                    # layer press
                    self._do_layer_press_end_auto_(event)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    self._do_graph_track_end_(event)
                else:
                    event.ignore()
                #
                self._clear_all_action_flags_()

            # zoom
            elif event.type() == QtCore.QEvent.Wheel:
                self._do_graph_zoom_(event)
                return True
            #
            elif event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                self.focus_accepted.emit(True)
                parent = self.parent()
                if isinstance(parent, _qt_wgt_entry_frame.QtEntryFrame):
                    parent._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                self.focus_accepted.emit(False)
                parent = self.parent()
                if isinstance(parent, _qt_wgt_entry_frame.QtEntryFrame):
                    parent._set_focused_(False)
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtNGPainter(self)

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

    def _setup_graph_by_universe_(self):
        obj_type = self._graph_universe.get_obj_type('graph/track')
        objs = obj_type.get_objs()
        for i_obj in objs:
            self._create_node_(**{x.name: x.get() for x in i_obj.get_parameters()})

    def _set_timeline_(self, widget):
        self._track_timeline = widget

    def _set_track_layer_(self, widget):
        self._track_layer = widget

    def _set_track_guide_(self, widget):
        self._track_guide = widget
        self._track_stage_model = self._track_guide._stage_model

    def _create_node_(self, *args, **kwargs):
        key = kwargs['key']
        if self._track_stage_model.is_exists(key) is True:
            return self._track_guide._stage_model.get_one_node(key)

        node_widget = self.NG_NODE_CLS(self)
        self._graph_nodes.append(node_widget)
        self._graph_node_dict[key] = node_widget

        node_widget._set_graph_(self)
        node_widget._setup_track_(**kwargs)
        node_widget._refresh_widget_all_()

        return node_widget

    def _create_connection_(self, *args, **kwargs):
        ng_connection = self.NG_CONNECTION_CLS(self._connection_sbj_layer)
        self._ng_graph_connections.append(ng_connection)
        ng_connection._set_graph_(self)
        return ng_connection

    def _restore_graph_(self):
        self._track_guide._restore_stage_()
        self._clear_graph_()
        # clear undo
        self._undo_stack.clear()


class QtTrackView(
    _qt_wgt_entry_frame.QtEntryFrame
):
    def __init__(self, *args, **kwargs):
        super(QtTrackView, self).__init__(*args, **kwargs)

        self._lot = _qt_wgt_base.QtVBoxLayout(self)
        self._lot.setContentsMargins(*[2]*4)
        self._lot.setSpacing(2)
        # create track first
        self._track_layer = _layer.QtTrackLayer(self)

        self._track_guide = _guide.QtTrackGuide()
        self._lot.addWidget(self._track_guide)
        self._track_layer._set_coord_model_(self._track_guide._stage_model._layer_coord_model)

        self._graph = QtTrackGraph()
        self._lot.addWidget(self._graph)
        self._graph._set_track_guide_(self._track_guide)
        self._track_layer._set_graph_(self._graph)

        self._track_guide._set_graph_(self._graph)

        self._graph._set_track_layer_(self._track_layer)

        self._track_timeline = _timeline.QtTrackTimeline()
        self._lot.addWidget(self._track_timeline)
        self._track_timeline._set_coord_model_(self._track_guide._stage_model._time_coord_model)
        self._track_timeline._set_graph_(self._graph)
        self._graph._set_timeline_(self._track_timeline)

        self._track_timehandle = _timehandle.QtTimeHandle(self)
        self._track_timeline._set_timehandle_(self._track_timehandle)

