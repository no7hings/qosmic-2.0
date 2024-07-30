# coding=utf-8
import functools

import os.path

import enum

import collections

import lxbasic.core as bsc_core
# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *

from .. import core as _qt_core

from .. import abstracts as _qt_abstracts

from ..widgets import base as _qt_wgt_base

from ..widgets import entry_frame as _qt_wgt_entry_frame

from . import graph_base as _graph_base

from . import sbj_track as _sbj_time_track

from . import track_time as _track_time

from . import timehandle as _timehandle

from . import undo_command as _undo_command

from . import sbj_connection as _sbj_connection

from . import track_layer as _track_layer

from . import track_stage as _track_stage


class QtTimeTrackGraph(
    QtWidgets.QWidget,

    _qt_abstracts.AbsQtActionBaseDef,
    _graph_base.AbsQtActionForRectSelectDef,

    _graph_base.AbsQtGraphBaseDef,
    _graph_base.AbsQtGraphSbjDef,
):
    NG_NODE_CLS = _sbj_time_track.QtTimeTrack
    NG_CONNECTION_CLS = _sbj_connection.QtConnection

    NGSelectionFlag = _graph_base._NGSelectionFlag

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        width, height = self.width(), self.height()

        rect = QtCore.QRect(
            x, y, width, height
        )
        # update graph first
        self._update_graph_geometry_()
        # x axis for timeline
        self._track_time._update_from_graph_(rect, self._graph_translate_x, self._graph_scale_x)
        # y axis for layer
        self._track_layer._update_from_graph_(rect, self._graph_translate_y, self._graph_scale_y)
        # update nodes
        self._update_all_nodes_graph_args_(
            self._graph_translate_x, self._graph_translate_y, self._graph_scale_x, self._graph_scale_y
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

        self._track_stage._refresh_widget_all_()

        self._update_graph_nodes_()

    def _together_move_nodes_(self, sbj, d_point):
        self._set_node_current_for_(sbj)
        if self._node_current is not None:
            p_0 = self._node_current.pos()
            p_1_x, p_1_y = d_point.x(), d_point.y()
            x_1, y_1 = self._track_stage_model.step_coord_loc(p_1_x, p_1_y)
            d_point_step = QtCore.QPoint(x_1, y_1)
            for i_sbj in self._nodes_selected:
                if i_sbj != self._node_current:
                    i_p = i_sbj.pos()
                    i_offset_point = p_0-i_p
                    i_sbj._move_by_point_(d_point_step, i_offset_point)
                else:
                    i_sbj._move_by_point_(d_point_step)

    def _do_node_move_or_resize_end_(self, sbj=None):
        data = []
        nodes = self._nodes_selected
        if sbj is not None:
            if sbj not in nodes:
                nodes += [sbj]

        for i in nodes:
            i_model, i_last_model = i._track_model, i._track_last_model
            if i_model != i_last_model:
                data.append(
                    (i, i_model, i_last_model)
                )

        if data:
            c = _undo_command.QtTimetrackActionCommand(
                data
            )
            self._widget._undo_stack.push(c)
            c._graph = self
            self._track_stage._update_stage_()

    def _update_stage_(self):
        self._track_stage._update_stage_()

    def __init__(self, *args, **kwargs):
        super(QtTimeTrackGraph, self).__init__(*args, **kwargs)
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

        self._graph_scale_x_enable, self._graph_scale_y_enable = True, False

        self._track_stage = None
        self._track_stage_model = None

        self._track_time = None

        self._track_layer = None

        self._timetrack_trim_sbj_layer = _graph_base.QtSbjLayer(self)
        self._connection_sbj_layer = _graph_base.QtSbjLayer(self)
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
            #
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
            # zoom
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

        # self._draw_layer_basic_(painter)
        
        if self._is_action_flag_match_(
            self.ActionFlag.RectSelectMove
        ):
            painter._draw_dotted_frame_(
                self._rect_selection_rect,
                border_color=_qt_core.QtBorderColors.Selected,
                background_color=_qt_core.QtBackgroundColors.Transparent
            )

        infos = collections.OrderedDict(
            [
                ('translate', '{}, {}'.format(self._graph_translate_x, self._graph_translate_y)),
                ('scale', '{}, {}'.format(self._graph_scale_x, self._graph_scale_y)),
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

    def _set_timeline_(self, widget):
        self._track_time = widget

    def _set_track_layer_(self, widget):
        self._track_layer = widget

    def _set_track_stage_(self, widget):
        self._track_stage = widget
        self._track_stage_model = self._track_stage._stage_model

    def _create_node_(self, *args, **kwargs):
        ng_node = self.NG_NODE_CLS(self)
        self._graph_nodes.append(ng_node)
        ng_node._set_graph_(self)
        ng_node._setup_track_(
            **kwargs
        )
        return ng_node

    def _create_connection_(self, *args, **kwargs):
        ng_connection = self.NG_CONNECTION_CLS(self._connection_sbj_layer)
        self._ng_graph_connections.append(ng_connection)
        ng_connection._set_graph_(self)
        return ng_connection

    def _set_ng_graph_frame_translate_to_nodes_(self, ng_nodes):
        t_x, t_y = self._graph_translate_x, self._graph_translate_y
        o_w, o_h = self.width(), self.height()
        x_0, y_0, x_1, y_1, w_0, h_0 = self._get_graph_frame_args_by_nodes_(ng_nodes)
        c_x, c_y = x_0+(x_1-x_0)/2, y_0+(y_1-y_0)/2
        x, y = o_w/2-c_x+t_x, o_h/2-c_y+t_y
        self._translate_graph_to_(
            x, y
        )

    def _set_ng_graph_frame_scale_to_nodes_(self, ng_nodes):
        o_s_x, o_s_y = self._graph_scale_x, 1.0
        o_w, o_h = self.width(), self.height()
        x_0, y_0, x_1, y_1, w_0, h_0 = self._get_graph_frame_args_by_nodes_(ng_nodes)
        #
        i_x, i_y, i_w, i_h = bsc_core.RawSizeMtd.fit_to(
            (w_0, h_0), (o_w, o_h)
        )
        o_r = (i_w*.75)
        r_0 = w_0
        s_x_0, s_y_0 = float(o_r)/float(r_0), float(o_r)/float(r_0)
        s_x_0, s_y_0 = s_x_0*o_s_x, s_y_0*o_s_y
        self._scale_graph_to_(
            s_x_0, 1.0
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
        if self._nodes_selected:
            ng_nodes = self._nodes_selected
        else:
            ng_nodes = self._graph_nodes
        #
        self._set_ng_graph_frame_to_nodes_(ng_nodes)


class QtComposition(
    _qt_wgt_entry_frame.QtEntryFrame
):
    def __init__(self, *args, **kwargs):
        super(QtComposition, self).__init__(*args, **kwargs)

        self._lot = _qt_wgt_base.QtVBoxLayout(self)
        self._lot.setSpacing(0)
        self._lot.setContentsMargins(*[2]*4)
        # create track first
        self._track_layer = _track_layer.QtTrackLayer(self)

        self._track_stage = _track_stage.QtTrackStage()
        self._lot.addWidget(self._track_stage)
        self._track_layer._set_coord_model_(self._track_stage._stage_model._layer_coord_model)

        self._graph = QtTimeTrackGraph()
        self._lot.addWidget(self._graph)
        self._graph._set_track_stage_(self._track_stage)
        self._track_layer._set_graph_(self._graph)

        self._track_stage._set_graph_(self._graph)

        self._graph._set_track_layer_(self._track_layer)

        self._track_time = _track_time.QtTrackTime()
        self._lot.addWidget(self._track_time)
        self._track_time._set_coord_model_(self._track_stage._stage_model._time_coord_model)
        self._track_time._set_graph_(self._graph)
        self._graph._set_timeline_(self._track_time)

        self._timehandle = _timehandle.QtTimeHandle(self)
        self._track_time._set_timehandle_(self._timehandle)

