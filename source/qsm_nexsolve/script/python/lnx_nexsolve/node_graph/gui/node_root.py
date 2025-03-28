# coding:utf-8
# gui
import lxgui.core as gui_core

from lxgui.qt.core.wrap import *

import lxgui.qt.core as gui_qt_core

import lxgui.qt.abstracts as gui_qt_abstracts

import lxgui.qt.widgets as gui_qt_widgets

from ...core import base as _scn_cor_base

from ..core import base as _cor_base

from ..core import action as _cor_action

from ..model import node_root as _mdl_node_root

from . import aux_ as _aux

from . import connection as _connection

from . import port as _port

from . import node as _node


class SceneGui(QtWidgets.QGraphicsScene):
    def __init__(self, *args):
        super(SceneGui, self).__init__(*args)

        self._model = None

    def _set_model(self, model):
        self._model = model

    def _get_items_by_rect(self, x, y, w, h):
        return self.items(QtCore.QRectF(x, y, w, h), QtCore.Qt.IntersectsItemBoundingRect)


class QtQRubberBand(QtWidgets.QRubberBand):
    def __init__(self, *args, **kwargs):
        super(QtQRubberBand, self).__init__(*args, **kwargs)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        x, y, w, h = 0, 0, self.rect().width(), self.rect().height()
        r, g, b, a = gui_core.GuiRgba.LightAzureBlue
        painter.setPen(QtGui.QColor(r, g, b))
        painter.setBrush(QtGui.QColor(r, g, b, 31))
        painter.drawRect(QtCore.QRect(x, y, w-1, h-1))


# root
class RootNodeGui(
    QtWidgets.QGraphicsView,
    gui_qt_abstracts.AbsQtThreadWorkerExtraDef,
):
    node_edited_changed = qt_signal(str)

    event_sent = qt_signal(int, int, dict)
    
    scene_path_accepted = qt_signal(str)

    ActionFlags = _cor_action.ActionFlags

    QT_MENU_CLS = gui_qt_widgets.QtMenu

    def _map_from_global(self, point):
        return self.mapToScene(self.mapFromGlobal(point))

    def __init__(self, *args):
        super(RootNodeGui, self).__init__(*args)
        self.setAutoFillBackground(True)
        self.setPalette(gui_qt_core.GuiQtDcc.generate_qt_palette())
        self.setStyleSheet(gui_qt_core.QtStyle.get('QGraphicsView'))

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.setRenderHint(QtGui.QPainter.Antialiasing, True)
        self.setDragMode(self.RubberBandDrag)
        self.setTransformationAnchor(self.NoAnchor)
        self.setResizeAnchor(self.NoAnchor)
        self.setInteractive(True)
        self.setDragMode(self.NoDrag)

        self._init_thread_worker_extra_def_(self)

        self._rubber_band = QtQRubberBand(QtWidgets.QRubberBand.Rectangle, self)

        self._model = _mdl_node_root.RootNode(self)
        self._model._builtin_data.connection.gui_cls = _connection.ConnectionGui

        self._drag_start_point = None
        self._drag_port = None
        self._drag_connection = None

        # undo
        self._undo_group_index = 0
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
        actions = [
            # delete
            (self._model._on_delete_action, 'Delete'),
            # copy
            (self._model._on_copy_action, 'Ctrl+C'),
            # duplicate
            (self._model._on_duplicate_action, 'Ctrl+D'),
            # cut
            (self._model._on_cut_action, 'Ctrl+X'),
            # paste
            (self._model._on_paste_action, 'Ctrl+V'),
            # bypass
            (self._model._on_bypass_action, 'D'),
            # frame select, todo: frame select make glob position error
            (self._model._on_frame_select_action, 'F'),
            # new file
            (self._model._on_new_file_action, 'Ctrl+N'),
            # open file
            (self._model._on_open_file_action, 'Ctrl+O'),
            # save file
            (self._model._on_save_file_action, 'Ctrl+S'),
            # save file to
            (self._model._on_save_file_as_action, 'Ctrl+Shift+S')
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

        self.installEventFilter(self)

    # undo
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

    def _accept_source_connect(self, port_gui):
        if isinstance(port_gui, _port.InputGui):
            source_port = self._drag_port
            target_port = port_gui._model

            if target_port.has_source():
                source_port_old = target_port.get_source()

                disconnect_args = [(source_port_old, target_port)]
                connect_args = [(source_port, target_port)]
                self._model._push_reconnect_cmd(
                    disconnect_args, connect_args
                )
            else:
                self._model.connect_ports(source_port, target_port)

        self.scene().removeItem(self._drag_connection._gui)

        self._drag_connection = None
        self._drag_port = None

    def _accept_source_connect_auto(self, target_node):
        source_port = self._drag_port
        self._model._push_connect_input_auto_cmd(source_port, target_node)

        self.scene().removeItem(self._drag_connection._gui)

        self._drag_connection = None
        self._drag_port = None

    def _accept_target_connect(self, port_gui):
        if isinstance(port_gui, _port.OutputGui):
            source_port = port_gui._model
            target_port = self._drag_port
            if target_port.has_source():
                source_port_old = target_port.get_source()

                disconnect_args = [(source_port_old, target_port)]
                connect_args = [(source_port, target_port)]
                self._model._push_reconnect_cmd(
                    disconnect_args, connect_args
                )
            else:
                self._model.connect_ports(source_port, target_port)

        self.scene().removeItem(self._drag_connection._gui)
        self._drag_connection = None
        self._drag_port = None

    def _cancel_connect(self):
        if self._drag_connection is None:
            return

        self.scene().removeItem(self._drag_connection._gui)
        self._drag_connection = None
        self._drag_port = None

    def _accept_source_reconnect(self, port_gui):
        if isinstance(port_gui, _port.OutputGui):
            source_port_0 = self._drag_connection.get_source()
            target_port_0 = self._drag_connection.get_target()

            disconnect_args = [(source_port_0, target_port_0)]
            source_port_new = port_gui._model
            if source_port_0 != source_port_new:
                connect_args = [(source_port_new, target_port_0)]
                self._model._push_reconnect_cmd(
                    disconnect_args, connect_args
                )
            else:
                self._drag_connection.reset_status()
                self._drag_connection.update_v()
        else:
            source_port = self._drag_connection.get_source()
            target_port = self._drag_connection.get_target()
            self._model.disconnect_ports(source_port, target_port)

        self._drag_connection = None

    def _accept_target_reconnect(self, port_gui):
        if isinstance(port_gui, _port.InputGui):
            source_port_0 = self._drag_connection.get_source()
            target_port_0 = self._drag_connection.get_target()

            disconnect_args = [(source_port_0, target_port_0)]
            target_port_1 = port_gui._model
            if target_port_0 != target_port_1:
                if target_port_1.has_source():
                    source_port_1 = target_port_1.get_source()
                    disconnect_args.append((source_port_1, target_port_1))

                connect_args = [(source_port_0, target_port_1)]
                self._model._push_reconnect_cmd(
                    disconnect_args, connect_args
                )
            else:
                self._drag_connection.reset_status()
                self._drag_connection.update_v()
        else:
            source_port = self._drag_connection.get_source()
            target_port = self._drag_connection.get_target()
            self._model.disconnect_ports(source_port, target_port)

        self._drag_connection = None

    def _accept_target_reconnect_auto(self, target_node):
        source_port_0 = self._drag_connection.get_source()
        target_port_0 = self._drag_connection.get_target()
        
        self._model._push_reconnect_input_auto_cmd(source_port_0, target_port_0, target_node)

        self._drag_connection = None

    def _cancel_reconnect(self):
        self._drag_connection = None

    @classmethod
    def _find_item(cls, items, item_cls):
        for i in items:
            if isinstance(i, item_cls):
                return i
        return None

    def _get_items_under_cursor(self, pos):
        scene_pos = self.mapToScene(pos)
        selection_area = QtGui.QPainterPath()
        selection_area.addRect(QtCore.QRectF(scene_pos.x()-1, scene_pos.y()-1, 2, 2))
        return self.scene().items(selection_area, QtCore.Qt.IntersectsItemShape)

    def mousePressEvent(self, event):
        if (
            event.button() == QtCore.Qt.LeftButton
            and event.modifiers() in (QtCore.Qt.ShiftModifier, QtCore.Qt.ControlModifier)
        ):
            items_under_cursor = self._get_items_under_cursor(event.pos())
            if items_under_cursor:
                for i_item in items_under_cursor:
                    if isinstance(i_item, _node.StandardNodeGui):
                        if event.modifiers() == QtCore.Qt.ShiftModifier:
                            i_item.setSelected(True)
                        elif event.modifiers() == QtCore.Qt.ControlModifier:
                            i_item.setSelected(False)
            else:
                self._model.set_action_flag(self.ActionFlags.RectSelectPressClick)
                self._model._do_rect_selection_start(event)

        elif event.button() == QtCore.Qt.LeftButton:
            items_under_cursor = self._get_items_under_cursor(event.pos())
            point = event.pos()
            p = self.mapToScene(point)
            self._drag_start_point = point
            # port
            if self._model.is_action_sub_flag_matching(self.ActionFlags.PortSourceHoverMove):
                self._model.clear_action_sub_flag()
                if self._find_item(items_under_cursor, _aux.AddInputAuxGui):
                    aux_gui = self._find_item(items_under_cursor, _aux.AddInputAuxGui)
                    node = aux_gui.parentItem()._model
                    self._accept_source_connect_auto(node)
                else:
                    port_gui = self._find_item(items_under_cursor, _port.InputGui)
                    self._accept_source_connect(port_gui)
            elif self._model.is_action_sub_flag_matching(self.ActionFlags.PortTargetHoverMove):
                self._model.clear_action_sub_flag()
                port_gui = self._find_item(items_under_cursor, _port.OutputGui)
                self._accept_target_connect(port_gui)
            # connection
            elif self._model.is_action_sub_flag_matching(self.ActionFlags.ConnectionSourceHoverMove):
                self._model.clear_action_sub_flag()
                port_gui = self._find_item(items_under_cursor, _port.OutputGui)
                self._accept_source_reconnect(port_gui)
            elif self._model.is_action_sub_flag_matching(self.ActionFlags.ConnectionTargetHoverMove):
                self._model.clear_action_sub_flag()
                if self._find_item(items_under_cursor, _aux.AddInputAuxGui):
                    aux_gui = self._find_item(items_under_cursor, _aux.AddInputAuxGui)
                    node = aux_gui.parentItem()._model
                    self._accept_target_reconnect_auto(node)
                else:
                    port_gui = self._find_item(items_under_cursor, _port.InputGui)
                    self._accept_target_reconnect(port_gui)
            else:
                # do not change if elif order
                # node add input
                if self._find_item(items_under_cursor, _aux.AddInputAuxGui):
                    aux_gui = self._find_item(items_under_cursor, _aux.AddInputAuxGui)
                    node = aux_gui.parentItem()._model
                    self._model._push_add_node_input_cmd(node)
                # node move
                elif self._find_item(items_under_cursor, _node.StandardNodeGui):
                    super(RootNodeGui, self).mousePressEvent(event)
                    self._model.set_action_flag(self.ActionFlags.NodePressClick)
                    self._model._do_node_move_start(event)
                # port
                elif self._find_item(items_under_cursor, _port.OutputGui):
                    item = self._find_item(items_under_cursor, _port.OutputGui)
                    self._model.set_action_flag(self.ActionFlags.PortSourcePressClick)
                    self._model.set_action_sub_flag(self.ActionFlags.PortSourcePressClick)
                    self._drag_port = item._model
                    # temp connection
                    connection_gui = _connection.ConnectionGui(source_port=self._drag_port)
                    connection_gui._set_default_color(_cor_base._QtColors.ConnectionNew)
                    self._drag_connection = connection_gui._model
                    self.scene().addItem(connection_gui)
                    self._drag_connection.update_v(end_point=p)
                elif self._find_item(items_under_cursor, _port.InputGui):
                    item = self._find_item(items_under_cursor, _port.InputGui)
                    self._model.set_action_flag(self.ActionFlags.PortTargetPressClick)
                    self._model.set_action_sub_flag(self.ActionFlags.PortTargetPressClick)
                    self._drag_port = item._model
                    connection_gui = _connection.ConnectionGui(target_port=self._drag_port)
                    connection_gui._set_default_color(_cor_base._QtColors.ConnectionNew)
                    self._drag_connection = connection_gui._model
                    self.scene().addItem(connection_gui)
                    self._drag_connection.update_v(start_point=p)
                # connection
                elif self._find_item(items_under_cursor, _connection.ConnectionGui):
                    item = self._find_item(items_under_cursor, _connection.ConnectionGui)
                    self._drag_connection = item._model
                    region = item._get_region(p)
                    if region == _connection.ConnectionGui.Regions.Source:
                        self._model.set_action_flag(self.ActionFlags.ConnectionSourcePressClick)
                        self._model.set_action_sub_flag(self.ActionFlags.ConnectionSourcePressClick)
                        self._drag_connection.update_v(start_point=p)
                    elif region == _connection.ConnectionGui.Regions.Target:
                        self._model.set_action_flag(self.ActionFlags.ConnectionTargetPressClick)
                        self._model.set_action_sub_flag(self.ActionFlags.ConnectionTargetPressClick)
                        self._drag_connection.update_v(end_point=p)
                elif self._find_item(items_under_cursor, _node.BackdropGui):
                    item = self._find_item(items_under_cursor, _node.BackdropGui)
                    # pass event first
                    super(RootNodeGui, self).mousePressEvent(event)
                    if item._model.get_move_flag() is False and item._model.get_resize_flag() is False:
                        self._model.set_action_flag(self.ActionFlags.RectSelectPressClick)
                        self._model._do_rect_selection_start(event)
                # node bypass
                elif self._find_item(items_under_cursor, _aux.IconAuxGui):
                    super(RootNodeGui, self).mousePressEvent(event)
                else:
                    self._model.set_action_flag(self.ActionFlags.RectSelectPressClick)
                    self._model._do_rect_selection_start(event)
                    super(RootNodeGui, self).mousePressEvent(event)
        elif event.button() == QtCore.Qt.MidButton:
            self._model.set_action_flag(self.ActionFlags.GraphTrackClick)
            self._model._do_track_start(event)
        else:
            super(RootNodeGui, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.NoButton:
            items_under_cursor = self._get_items_under_cursor(event.pos())
            # port
            if self._model.is_action_sub_flag_matching(
                self.ActionFlags.PortSourcePressClick, self.ActionFlags.PortSourceHoverMove
            ):
                if self._drag_connection is not None:
                    point = event.pos()
                    item = self._find_item(items_under_cursor, _port.InputGui)
                    p = self.mapToScene(point)

                    if isinstance(item, _port.InputGui):
                        self._drag_connection.to_correct_status()
                    else:
                        self._drag_connection.reset_status()

                    self._drag_connection.update_v(end_point=p)
                    self._model.set_action_sub_flag(self.ActionFlags.PortSourceHoverMove)
            elif self._model.is_action_sub_flag_matching(
                self.ActionFlags.PortTargetPressClick, self.ActionFlags.PortTargetHoverMove
            ):
                if self._drag_connection is not None:
                    point = event.pos()
                    item = self._find_item(items_under_cursor, _port.OutputGui)
                    p = self.mapToScene(point)
                    if isinstance(item, _port.OutputGui):
                        self._drag_connection.to_correct_status()
                    else:
                        self._drag_connection.reset_status()

                    self._drag_connection.update_v(start_point=p)
                    self._model.set_action_sub_flag(self.ActionFlags.PortTargetHoverMove)
            # connections
            elif self._model.is_action_sub_flag_matching(
                self.ActionFlags.ConnectionSourcePressClick, self.ActionFlags.ConnectionSourceHoverMove
            ):
                if self._drag_connection is not None:
                    point = event.pos()
                    item = self._find_item(items_under_cursor, _port.OutputGui)
                    p = self.mapToScene(point)

                    if isinstance(item, _port.OutputGui):
                        self._drag_connection.to_correct_status()
                    else:
                        self._drag_connection.reset_status()

                    self._drag_connection.update_v(start_point=p)
                    self._model.set_action_sub_flag(self.ActionFlags.ConnectionSourceHoverMove)
            elif self._model.is_action_sub_flag_matching(
                self.ActionFlags.ConnectionTargetPressClick, self.ActionFlags.ConnectionTargetHoverMove
            ):
                if self._drag_connection is not None:
                    point = event.pos()
                    item = self._find_item(items_under_cursor, _port.InputGui)
                    p = self.mapToScene(point)
                    if isinstance(item, _port.InputGui):
                        self._drag_connection.to_correct_status()
                    else:
                        self._drag_connection.reset_status()

                    self._drag_connection.update_v(end_point=p)
                    self._model.set_action_sub_flag(self.ActionFlags.ConnectionTargetHoverMove)
            super(RootNodeGui, self).mouseMoveEvent(event)
        elif event.buttons() == QtCore.Qt.LeftButton:
            point = event.pos()
            items_under_cursor = self._get_items_under_cursor(event.pos())
            p = self.mapToScene(point)
            # node
            if self._model.is_action_flag_matching(
                self.ActionFlags.NodePressClick, self.ActionFlags.NodePressMove
            ):
                super(RootNodeGui, self).mouseMoveEvent(event)
                self._model._do_node_move(event)
            # port
            elif self._model.is_action_flag_matching(
                self.ActionFlags.PortSourcePressClick, self.ActionFlags.PortSourcePressMove
            ):
                item = self._find_item(items_under_cursor, _port.InputGui)
                if isinstance(item, _port.InputGui):
                    self._drag_connection.to_correct_status()
                else:
                    self._drag_connection.reset_status()

                self._drag_connection.update_v(end_point=p)
                self._model.set_action_flag(self.ActionFlags.PortSourcePressMove)
            elif self._model.is_action_flag_matching(
                self.ActionFlags.PortTargetPressClick, self.ActionFlags.PortTargetPressMove
            ):
                item = self._find_item(items_under_cursor, _port.OutputGui)
                if isinstance(item, _port.OutputGui):
                    self._drag_connection.to_correct_status()
                else:
                    self._drag_connection.reset_status()

                self._drag_connection.update_v(start_point=p)
                self._model.set_action_flag(self.ActionFlags.PortTargetPressMove)
            # connection
            elif self._model.is_action_flag_matching(
                self.ActionFlags.ConnectionSourcePressClick, self.ActionFlags.ConnectionSourcePressMove
            ):
                item = self._find_item(items_under_cursor, _port.OutputGui)
                if isinstance(item, _port.OutputGui):
                    self._drag_connection.to_correct_status()
                else:
                    self._drag_connection.reset_status()

                self._drag_connection.update_v(start_point=p)
                self._model.set_action_flag(self.ActionFlags.ConnectionSourcePressMove)
            elif self._model.is_action_flag_matching(
                self.ActionFlags.ConnectionTargetPressClick, self.ActionFlags.ConnectionTargetPressMove
            ):
                item = self._find_item(items_under_cursor, _port.InputGui)
                if isinstance(item, _port.InputGui):
                    self._drag_connection.to_correct_status()
                else:
                    self._drag_connection.reset_status()

                self._drag_connection.update_v(end_point=p)
                self._model.set_action_flag(self.ActionFlags.ConnectionTargetPressMove)
            # rect selection
            elif self._model.is_action_flag_matching(
                self.ActionFlags.RectSelectPressClick, self.ActionFlags.RectSelectPressMove
            ):
                self._model.set_action_flag(self.ActionFlags.RectSelectPressMove)
                self._model._do_rect_selection_move(event)
            else:
                super(RootNodeGui, self).mouseMoveEvent(event)
        elif event.buttons() == QtCore.Qt.MidButton:
            if self._model.is_action_flag_matching(
                self.ActionFlags.GraphTrackClick,
                self.ActionFlags.GraphTrackMove
            ):
                self._model.set_action_flag(self.ActionFlags.GraphTrackMove)
                self._model._do_track_move(event)
        else:
            super(RootNodeGui, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            items_under_cursor = self._get_items_under_cursor(event.pos())
            # node
            if self._model.is_action_flag_matching(
                self.ActionFlags.NodePressClick, self.ActionFlags.NodePressMove
            ):
                super(RootNodeGui, self).mouseReleaseEvent(event)
                self._model._do_node_move_end()
            # connect
            elif self._model.is_action_flag_matching(self.ActionFlags.PortSourcePressMove):
                self._model.clear_action_sub_flag()
                item = self._find_item(items_under_cursor, _port.InputGui)
                self._accept_source_connect(item)
            elif self._model.is_action_flag_matching(self.ActionFlags.PortTargetPressMove):
                self._model.clear_action_sub_flag()
                item = self._find_item(items_under_cursor, _port.OutputGui)
                self._accept_target_connect(item)
            # reconnect
            elif self._model.is_action_flag_matching(self.ActionFlags.ConnectionSourcePressMove):
                self._model.clear_action_sub_flag()
                item = self._find_item(items_under_cursor, _port.OutputGui)
                self._accept_source_reconnect(item)
            elif self._model.is_action_flag_matching(self.ActionFlags.ConnectionTargetPressMove):
                self._model.clear_action_sub_flag()
                item = self._find_item(items_under_cursor, _port.InputGui)
                self._accept_target_reconnect(item)
            # rect selection
            elif self._model.is_action_flag_matching(self.ActionFlags.RectSelectPressMove):
                self._model._do_rect_selection_end(event)
            else:
                super(RootNodeGui, self).mouseReleaseEvent(event)
        # track
        elif event.button() == QtCore.Qt.MidButton:
            if self._model.is_action_flag_matching(
                self.ActionFlags.GraphTrackClick,
                self.ActionFlags.GraphTrackMove
            ):
                self._model._do_tack_end()
        else:
            super(RootNodeGui, self).mouseReleaseEvent(event)

        self._rubber_band.hide()
        self._model.clear_action_flag()

    def wheelEvent(self, event):
        self._model._do_zoom(event)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            pass
        return False

    def contextMenuEvent(self, event):
        menu = None

        menu_data = self._model.get_menu_data()
        menu_content = self._model.get_menu_content()
        menu_data_generate_fnc = self._model.get_menu_data_generate_fnc()
        menu_name_dict = self._model.get_menu_name_dict()

        if menu_content:
            if menu is None:
                menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
            menu._set_menu_content_(menu_content, append=True)

        if menu_data:
            if menu is None:
                menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
            menu._set_menu_data_(menu_data)

        if menu_data_generate_fnc:
            if menu is None:
                menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
            menu._set_menu_data_(menu_data_generate_fnc())

        # data from item
        items_under_cursor = self._get_items_under_cursor(event.pos())
        if items_under_cursor:
            menu = None
            item = self._find_item(
                items_under_cursor, _node._AbsNodeGui
            )
            if item.ENTITY_TYPE in {_scn_cor_base.EntityTypes.Node, _scn_cor_base.EntityTypes.Backdrop}:
                item_menu_data = item._model.get_menu_data()
                item_menu_content = item._model.get_menu_content()
                item_menu_data_generate_fnc = item._model.get_menu_data_generate_fnc()
                item_menu_name_dict = item._model.get_menu_name_dict()
                menu_name_dict.update(item_menu_name_dict)

                if item_menu_content:
                    if menu is None:
                        menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
                    menu._set_menu_content_(item_menu_content, append=True)

                if item_menu_data:
                    if menu is None:
                        menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
                    menu._set_menu_data_(item_menu_data)

                if item_menu_data_generate_fnc:
                    if menu is None:
                        menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
                    menu._set_menu_data_(item_menu_data_generate_fnc())

                if menu is not None:
                    menu._update_menu_name_dict_(item_menu_name_dict)

        if menu is not None:
            menu._popup_start_()

    def _get_gui_translate(self):
        transform = self.transform()
        return transform.dx(), transform.dy()

    def _get_gui_scale(self):
        transform = self.transform()
        return round(transform.m11(), 3), round(transform.m22(), 3)

    def drawBackground(self, painter, rect):
        super(RootNodeGui, self).drawBackground(painter, rect)
