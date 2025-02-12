# coding=utf-8
import json
# gui
from .... import core as _gui_core
# qt
from ...core.wrap import *

from ... import core as _qt_core

from ... import abstracts as _qt_abstracts

from ...widgets import base as _qt_wgt_base

from ...widgets import button as _wgt_button

from ...widgets import scroll as _wgt_scroll

from ...widgets import container as _wgt_container

from ...widgets.input import input_for_filter as _wgt_input_for_filter

from ...view_widgets import base as _vew_wgt_base

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

        rect = qt_rect(
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
        # update node layer
        self._timetrack_trim_sbj_layer.setGeometry(
            self.rect()
        )
        self._connection_sbj_layer.setGeometry(
            self.rect()
        )
        self._track_layer.setGeometry(
            qt_rect(
                self.x(), self.y(), self.width(), self.height()
            )
        )

        self._track_guide._refresh_widget_all_()

        self._track_timeline._set_play_timeframe_range_(*self._track_model_stage.track_range)

    def __init__(self, *args, **kwargs):
        super(QtTrackGraph, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        self._init_action_base_def_(self)

        self._init_graph_base_def_(self)
        self._init_sbj_base_def_(self)

        self._init_universe_def_(self)

        self._graph_model._graph_scale_x_enable = True
        self._graph_model._graph_scale_y_enable = False

        self._track_guide = None
        self._track_model_stage = None

        self._graph_node_dict = {}

        self._track_timeline = None

        self._track_layer = None

        self._current_layer_index_tmp = None
        self._current_timeframe_tmp = None

        self._timetrack_trim_sbj_layer = _bsc_graph.QtSbjLayer(self)
        self._connection_sbj_layer = _bsc_graph.QtSbjLayer(self)

        # undo
        self._undo_stack = QtWidgets.QUndoStack()
        self._undo_stack.setUndoLimit(100)
        self._undo_button = None
        self._undo_action = self._undo_stack.createUndoAction(self, 'undo')
        self._undo_action.setShortcut(
            QtGui.QKeySequence(
                QtCore.Qt.CTRL+QtCore.Qt.Key_Z
            )
        )
        self.addAction(self._undo_action)

        # redo
        self._redo_action = self._undo_stack.createRedoAction(self, 'redo')
        self._redo_button = None
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
            (self._selection_all_fnc_, 'Ctrl+A'),
            # bypass
            (self._on_bypass_auto_, 'D'),
            # trash
            (self._on_trash_auto_, 'Delete'),
            # copy
            (self._on_copy_auto_, 'Ctrl+C'),
            # cut
            (self._on_graph_node_cut_auto_, 'Ctrl+X'),
            # paste
            (self._on_paste_auto_, 'Ctrl+V'),
            # layout
            (self._on_layout_auto_, 'L'),
            # trim
            (self._on_trim_left_auto_, '['),
            (self._on_trim_right_auto_, ']')
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
                pass
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

                        # layer or timeline press
                        self._do_graph_press_start_(event)
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
                    self._do_graph_press_end_auto_(event)
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

    def _graph_node_move_together_fnc_(self, node_widget, d_point):
        p_0 = node_widget.pos()
        p_1_x, p_1_y = d_point.x(), d_point.y()
        x_1 = self._track_model_stage.step_x_loc(p_1_x)
        d_point_step = QtCore.QPoint(x_1, p_1_y)
        for i_node_widget in self._graph_selection_nodes:
            if i_node_widget != node_widget:
                i_p = i_node_widget.pos()
                i_offset_point = p_0-i_p
                i_node_widget._move_by_point_(d_point_step, i_offset_point)
            else:
                i_node_widget._move_by_point_(d_point_step)

    def _push_node_transformation_action_fnc_(self, node_widget=None, flag=None):
        cmd_data = []

        node_widgets = list(self._graph_selection_nodes)
        if node_widget is not None:
            if node_widget not in node_widgets:
                node_widgets += [node_widget]

        for i_node_widget in node_widgets:
            i_model, i_last_model = i_node_widget._track_model, i_node_widget._last_track_model
            if i_model != i_last_model:
                cmd_data.append(
                    (flag, (i_model, i_last_model))
                )

        self._push_track_action_fnc_(cmd_data)

    # bypass
    def _on_bypass_auto_(self):
        cmd_data = []

        hover_node = self._get_hovered_node_()
        if hover_node is None:
            return

        bypass_flag = hover_node._track_model.is_bypass

        node_widgets = list(self._graph_selection_nodes)
        if hover_node not in node_widgets:
            node_widgets.append(hover_node)

        if node_widgets:
            for i_node_widget in node_widgets:
                i_model = i_node_widget._track_model
                cmd_data.append(
                    # to target flag
                    ('bypass', (i_model, not bypass_flag))
                )

        self._push_track_action_fnc_(cmd_data)

    def _graph_node_bypass_fnc_(self, track_model, flag):
        key = track_model.key
        if key in self._graph_node_dict:
            node_widget = self._graph_node_dict[key]

            track_model.set_bypass(int(flag))

            node_widget._refresh_by_bypass_()

    # trash
    def _on_trash_auto_(self):
        cmd_data = []

        node_widgets = self._get_selected_nodes_()
        if node_widgets:
            for i_node_widget in node_widgets:
                i_model = i_node_widget._track_model
                cmd_data.append(
                    ('trash', (i_model, True))
                )

        self._push_track_action_fnc_(cmd_data)

    def _graph_node_trash_fnc_(self, track_model, flag):
        key = track_model.key
        if key in self._graph_node_dict:
            node_widget = self._graph_node_dict[key]
            track_model.set_trash(int(flag))
            node_widget._refresh_by_trash_()

    # copy cut paste
    def _on_copy_auto_(self):
        track_data = []
        node_widgets = self._get_selected_nodes_()
        if node_widgets:
            for i_node_widget in node_widgets:
                i_track_model = i_node_widget._track_model
                track_data.append(i_track_model.to_dict())

        data_string = json.dumps(
            dict(
                QSMMineData=dict(
                    type='track',
                    data=track_data,
                    flag='copy'
                ),
            )
        )
        _qt_core.QtUtil.write_clipboard(data_string)

    def _on_graph_node_cut_auto_(self):
        track_data = []
        node_widgets = self._get_selected_nodes_()
        if node_widgets:
            for i_node_widget in node_widgets:
                i_model = i_node_widget._track_model
                track_data.append(i_model.to_dict())

        data_string = json.dumps(
            dict(
                QSMMineData=dict(
                    type='track',
                    data=track_data,
                    flag='cut'
                ),
            )
        )
        _qt_core.QtUtil.write_clipboard(data_string)
        # use trash
        self._on_trash_auto_()

    def _on_paste_auto_(self):

        cmd_data = []

        text = _qt_core.QtUtil.read_clipboard()
        if text.startswith('{"QSMMineData": '):
            current_timeframe = self._track_timeline._get_current_timeframe_()
            current_layer_index = self._track_layer._get_current_index_()

            dict_ = json.loads(text)
            mine_data = dict_['QSMMineData']
            type_ = mine_data['type']
            if type_ == 'track':
                track_data_list = mine_data['data']
                flag = mine_data['flag']

                # copy
                if flag == 'copy':
                    track_args_list = []

                    for i_idx, i_track_data in enumerate(track_data_list):
                        i_track_data_copy = dict(i_track_data)

                        i_key_copy = self._track_model_stage.find_next_key(i_track_data['key'])
                        i_track_data_copy['key'] = i_key_copy

                        i_track_model_copy = self._track_model_stage.create_node_fnc(**i_track_data_copy)

                        track_args_list.append(i_track_model_copy)

                        cmd_data.append(
                            ('paste_copy', (i_track_model_copy, True))
                        )

                    track_model_group = self._track_model_stage.create_group_fnc(track_args_list)
                    track_model_group.sort_by_time()

                    track_model_group.apply_timeframe(current_timeframe)
                    track_model_group.apply_layer_index(current_layer_index)

                # cut
                elif flag == 'cut':
                    # todo: maybe node not in this stage
                    track_data_list = [x for x in track_data_list if x['key'] in self._graph_node_dict]

                    track_args_list = []

                    for i_idx, i_track_data in enumerate(track_data_list):
                        i_key = i_track_data['key']

                        # fixme: maybe paste from other graph
                        if i_key not in self._graph_node_dict:
                            continue

                        i_node_widget = self._graph_node_dict[i_key]

                        i_last_track_model = i_node_widget._track_model

                        i_track_model = i_node_widget._track_model.copy()
                        i_track_model.set_trash(0)

                        track_args_list.append(i_track_model)

                        cmd_data.append(
                            ('paste_cut', (i_track_model, i_last_track_model))
                        )

                    track_model_group = self._track_model_stage.create_group_fnc(track_args_list)
                    track_model_group.sort_by_time()

                    track_model_group.apply_timeframe(current_timeframe)
                    track_model_group.apply_layer_index(current_layer_index)

                    # _qt_core.QtUtil.clear_clipboard()
        self._push_track_action_fnc_(cmd_data)

    def _graph_node_paste_copy_fnc_(self, track_model, flag):
        # create
        key = track_model.key
        if flag is True:
            # if exists, mark trash disable for redo
            if key in self._graph_node_dict:
                node_widget = self._graph_node_dict[key]
                track_model = node_widget._track_model
                track_model.set_trash(0)
                node_widget._refresh_by_trash_()
            else:
                self._create_node_(**track_model.to_dict())
        # trash
        else:
            # mark trash for undo
            if key in self._graph_node_dict:
                node_widget = self._graph_node_dict[key]
                track_model = node_widget._track_model
                track_model.set_trash(1)
                node_widget._refresh_by_trash_()

    def _graph_node_paste_cut_fnc_(self, track_model):
        return self._graph_node_update_track_model_fnc_(track_model)

    # blend
    def _push_node_blend_action_fnc_(self, key, blend_flag):
        cmd_data = []
        if key in self._graph_node_dict:
            node_widget = self._graph_node_dict[key]
            track_model = node_widget._track_model

            track_model_new = track_model.copy()
            if blend_flag == 0:
                track_model_new.set_pre_blend(node_widget._pre_blend_tmp)
            elif blend_flag == 1:
                track_model_new.set_post_blend(node_widget._post_blend_tmp)

            last_track_model = track_model.copy()
            cmd_data.append(('blend', (track_model_new, last_track_model)))

        self._push_track_action_fnc_(cmd_data)

    def _graph_node_update_blend_fnc_(self, track_model):
        key = track_model.key
        if key in self._graph_node_dict:
            node_widget = self._graph_node_dict[key]
            self._graph_node_update_track_model_fnc_(track_model)
            node_widget._update_blend_tmp_()
            self._update_stage_()

    def _graph_node_update_track_model_fnc_(self, track_model):
        key = track_model.key
        if key in self._graph_node_dict:
            node_widget = self._graph_node_dict[key]
            return node_widget._node_update_track_model_fnc_(track_model)
        return False
    
    # layout
    def _on_layout_auto_(self):
        cmd_data = []

        track_args_list = []
        node_widgets = self._get_selected_nodes_()
        # todo: mark changed only?
        if node_widgets:
            for i_node_widget in node_widgets:
                i_last_track_model = i_node_widget._track_model
                i_track_model = i_node_widget._track_model.copy()
                track_args_list.append(i_track_model)

                cmd_data.append(
                    ('layout', (i_track_model, i_last_track_model))
                )

        if track_args_list:
            track_model_group = self._track_model_stage.create_group_fnc(track_args_list)
            track_model_group.sort_by_layer()
            track_model_group.do_layout()

        self._push_track_action_fnc_(cmd_data)

    # trim
    def _on_trim_left_auto_(self):
        cmd_data = []
        node_widgets = self._get_selected_nodes_() or filter(None, [self._get_hovered_node_()])
        if node_widgets:
            current_timeframe = self._track_timeline._get_current_timeframe_()

            node_widget = node_widgets[0]
            last_track_model = node_widget._track_model
            track_model = node_widget._track_model.copy()
            track_model.clip_start = current_timeframe

            cmd_data.append(
                ('trim', (track_model, last_track_model))
            )

        self._push_track_action_fnc_(cmd_data)

    def _on_trim_right_auto_(self):
        cmd_data = []

        node_widgets = self._get_selected_nodes_() or filter(None, [self._get_hovered_node_()])
        if node_widgets:
            current_timeframe = self._track_timeline._get_current_timeframe_()

            node_widget = node_widgets[0]
            last_track_model = node_widget._track_model
            track_model = node_widget._track_model.copy()
            track_model.clip_end = current_timeframe-1

            cmd_data.append(
                ('trim', (track_model, last_track_model))
            )

        self._push_track_action_fnc_(cmd_data)

    def _push_track_action_fnc_(self, cmd_data):
        if cmd_data:
            c = _undo_command.QtTrackActionCommand(
                cmd_data
            )
            c._graph = self
            self._widget._undo_stack.push(c)

    # delete and create
    def _graph_node_delete_fnc_(self, track_model):
        key = track_model.key
        if key in self._graph_node_dict:
            node_widget = self._graph_node_dict[key]
            # todo: remove fnc has bug
            if node_widget in self._graph_selection_nodes:
                self._graph_selection_nodes.remove(node_widget)
            if node_widget in self._graph_nodes:
                self._graph_nodes.remove(node_widget)

            self._track_guide._delete_node_(node_widget._track_model)
            node_widget._do_delete_()

    def _graph_node_create_fnc_(self, track_model):
        self._create_node_(
            **track_model.to_dict()
        )

    def _update_stage_(self):
        self._track_guide._update_stage_()

    def _do_graph_frame_scale_for_(self, node_widgets):
        x_0, y_0, x_1, y_1, w_0, h_0 = self._graph_model._compute_nodes_basic_geometry_args_for(node_widgets)
        w_1, h_1 = self.width(), self.height()

        s_x_0 = float(w_1)/float(w_0)

        self._graph_model.scale_to_origin(
            s_x_0*.875, 1.0
        )

    def _do_graph_frame_translate_for_(self, node_widgets):
        x_0, y_0, x_1, y_1, w_0, h_0 = self._graph_model._compute_nodes_basic_geometry_args_for(node_widgets)
        sx, sy = self._graph_model.sx, self._graph_model.sy

        # scale to
        s_x_0, s_y_0 = x_0*sx, y_0*sy
        s_w_0, s_h_0 = w_0*sx, h_0*sy

        w_1, h_1 = self.width(), self.height()
        x, y = -s_x_0+(w_1-s_w_0)/2, -s_y_0+(h_1-s_h_0)/2
        self._graph_model.translate_to(
            x, y
        )

    def _do_graph_press_start_(self, event):
        p = event.pos()

        x, y = p.x(), p.y()
        # time
        if _qt_core.QtUtil.is_ctrl_modifier():
            self._current_timeframe_tmp = self._track_model_stage.compute_timeframe(x)
        # later
        self._current_layer_index_tmp = self._track_model_stage.compute_layer_index(y)

    def _do_graph_press_end_auto_(self, event):
        if self._is_action_flag_match_(
            self.ActionFlag.PressClick
        ):
            # time
            if _qt_core.QtUtil.is_ctrl_modifier():
                self._track_timeline._accept_current_timeframe_(self._current_timeframe_tmp)
            # layer
            self._track_layer._set_current_index_(self._current_layer_index_tmp)
            self._track_layer._refresh_widget_draw_()

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
        self._track_model_stage = self._track_guide._track_model_stage

    def _set_undo_button_(self, widget):
        self._undo_button = widget
        self._undo_button.press_clicked.connect(self._undo_action.trigger)
        # noinspection PyUnresolvedReferences
        self._undo_stack.canUndoChanged.connect(self._update_undo_)

    def _update_undo_(self):
        self._undo_button._set_action_enable_(self._undo_stack.canUndo())

    def _set_redo_button_(self, widget):
        self._redo_button = widget
        self._redo_button.press_clicked.connect(self._redo_action.trigger)
        # noinspection PyUnresolvedReferences
        self._undo_stack.canRedoChanged.connect(self._update_redo_)

    def _update_redo_(self):
        self._redo_button._set_action_enable_(self._undo_stack.canRedo())

    def _create_node_(self, *args, **kwargs):
        key = kwargs['key']
        if self._track_model_stage.is_exists(key) is True:
            return self._track_guide._track_model_stage.get_one_node(key)

        node_widget = self.NG_NODE_CLS(self)
        self._graph_nodes.append(node_widget)
        self._graph_node_dict[key] = node_widget

        node_widget._set_graph_(self)
        node_widget._setup_track_(**kwargs)
        node_widget._refresh_widget_all_()

        return node_widget

    def _create_connection_(self, *args, **kwargs):
        connection_widget = self.NG_CONNECTION_CLS(self._connection_sbj_layer)
        self._ng_graph_connections.append(connection_widget)
        connection_widget._set_graph_(self)
        return connection_widget

    def _restore_graph_(self):
        self._track_guide._restore_stage_()
        self._clear_graph_()
        # clear undo
        self._undo_stack.clear()


class QtTrackView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QtTrackView, self).__init__(*args, **kwargs)

        self._lot = _qt_wgt_base.QtVBoxLayout(self)
        self._lot.setContentsMargins(*[2]*4)
        self._lot.setSpacing(2)
        # create track first
        self._track_layer = _layer.QtTrackLayer(self)

        self._track_guide = _guide.QtTrackGuide()
        self._lot.addWidget(self._track_guide)
        self._track_layer._set_coord_model_(self._track_guide._track_model_stage._layer_coord_model)

        self._graph = QtTrackGraph()
        self._lot.addWidget(self._graph)
        self._graph._set_track_guide_(self._track_guide)
        self._track_layer._set_graph_(self._graph)

        self._track_guide._set_graph_(self._graph)

        self._graph._set_track_layer_(self._track_layer)

        self._track_timeline = _timeline.QtTrackTimeline()
        self._lot.addWidget(self._track_timeline)
        self._track_timeline._set_coord_model_(self._track_guide._track_model_stage._time_coord_model)
        self._track_timeline._set_graph_(self._graph)
        self._graph._set_timeline_(self._track_timeline)

        self._track_timehandle = _timehandle.QtTimeHandle(self)
        self._track_timeline._set_timehandle_(self._track_timehandle)
        self._track_timehandle._set_graph_(self._graph)


class QtTrackWidget(_vew_wgt_base._BaseViewWidget):
    def __init__(self, *args, **kwargs):
        super(QtTrackWidget, self).__init__(*args, **kwargs)
        # refresh
        self._refresh_button = _wgt_button.QtIconPressButton()
        self._grid_lot.addWidget(self._refresh_button, 0, 0, 1, 1)
        self._refresh_button.setFixedSize(self.TOOL_BAR_W, self.TOOL_BAR_W)
        self._refresh_button._set_icon_file_path_(
            _gui_core.GuiIcon.get('refresh')
        )
        self._refresh_button.press_clicked.connect(self.refresh.emit)
        # top
        self._top_scroll_box = _wgt_scroll.QtHScrollBox()
        self._grid_lot.addWidget(self._top_scroll_box, 0, 1, 1, 1)
        self._top_scroll_box._set_layout_align_left_or_top_()
        self._top_scroll_box.setFixedHeight(self.TOOL_BAR_W)
        # left
        self._left_scroll_box = _wgt_scroll.QtVScrollBox()
        self._grid_lot.addWidget(self._left_scroll_box, 1, 0, 1, 1)
        self._left_scroll_box._set_layout_align_left_or_top_()
        self._left_scroll_box.setFixedWidth(self.TOOL_BAR_W)

        self._undo_and_redo_tool_box = self._add_top_tool_box_('undo and redo')

        # keyword filter
        self._keyword_filter_tool_box = self._add_top_tool_box_('keyword filter', size_mode=1)

        self._view = QtTrackView()
        self._grid_lot.addWidget(self._view, 1, 1, 1, 1)
        self._view._graph.setFocusProxy(self)
        # self.setFocusProxy(self._view._graph)

        self._track_layer = self._view._track_layer
        self._track_guide = self._view._track_guide
        self._graph = self._view._graph
        self._track_timeline = self._view._track_timeline
        self._track_timehandle = self._view._track_timehandle

        self._build_keyword_filter_tool_box_()

        self._build_undo_and_redo_tool_box_()

    def _add_top_tool_box_(self, name, size_mode=0):
        tool_box = _wgt_container.QtHToolBox()
        self._top_scroll_box.addWidget(tool_box)
        tool_box._set_expanded_(True)
        tool_box._set_name_text_(name)
        tool_box._set_size_mode_(size_mode)
        return tool_box

    def _insert_top_tool_box_(self, index, name):
        tool_box = _wgt_container.QtVToolBox()
        self._top_scroll_box.insertWidget(index, tool_box)
        tool_box._set_expanded_(True)
        tool_box._set_name_text_(name)
        return tool_box

    def _add_left_tool_box_(self, name):
        tool_box = _wgt_container.QtVToolBox()
        self._left_scroll_box.addWidget(tool_box)
        tool_box._set_expanded_(True)
        tool_box._set_name_text_(name)
        return tool_box

    def _insert_left_tool_box_(self, index, name):
        tool_box = _wgt_container.QtVToolBox()
        self._left_scroll_box.insertWidget(index, tool_box)
        tool_box._set_expanded_(True)
        tool_box._set_name_text_(name)
        return tool_box

    def _build_undo_and_redo_tool_box_(self):
        self._undo_button = _wgt_button.QtIconPressButton()
        self._undo_button._set_name_text_('undo')
        self._undo_button._set_icon_name_('montage/undo')
        self._undo_button._set_action_enable_(False)
        self._undo_and_redo_tool_box._add_widget_(self._undo_button)
        self._view._graph._set_undo_button_(self._undo_button)

        self._redo_button = _wgt_button.QtIconPressButton()
        self._redo_button._set_name_text_('redo')
        self._redo_button._set_icon_name_('montage/redo')
        self._redo_button._set_action_enable_(False)
        self._undo_and_redo_tool_box._add_widget_(self._redo_button)
        self._view._graph._set_redo_button_(self._redo_button)

    def _build_keyword_filter_tool_box_(self):
        self._keyword_filter_input = _wgt_input_for_filter.QtInputForFilter()
        self._keyword_filter_tool_box._add_widget_(self._keyword_filter_input)

        # self._keyword_filter_input._set_input_completion_buffer_fnc_(self._keyword_filter_input_completion_buffer_fnc)
        # self._keyword_filter_input.input_value_changed.connect(self._on_keyword_filer)
        # self._keyword_filter_input.occurrence_previous_press_clicked.connect(
        #     self._view_model.occurrence_item_previous
        # )
        # self._keyword_filter_input.occurrence_next_press_clicked.connect(
        #     self._view_model.occurrence_item_next
        # )
        # self._keyword_filter_input._set_occurrence_buttons_enable_(True)
