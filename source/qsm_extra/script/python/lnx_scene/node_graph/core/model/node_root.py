# coding:utf-8
import collections
import contextlib

import functools

import json

import six

import lxbasic.core as bsc_core

from lxgui.qt.core.wrap import *

import lxgui.qt.core as gui_qt_core

from .. import base as _base

from .. import undo as _undo


# scene model
class RootNode(
    _base._SbjBase,
    _base._AbsAction
):
    ActionFlags = _base._ActionFlags

    NODE_GUI_CLS_DICT = dict()

    def __init__(self, gui_widget):
        super(RootNode, self).__init__(gui_widget)

        self._close_flag = False

        self._data.type = 'root'
        self._data.path = '/'
        self._data.name = ''

        self._data.nodes = collections.OrderedDict()
        self._gui_data.connection_dict = collections.OrderedDict()

        # connection
        self._builtin_data.connection = _base._Dict(
            gui_cls=None,
        )

        self._init_action()
        self._pan_start = QtCore.QPoint()

        self._gui_data.zoom = _base._Dict(
            factor=1.2
        )
        self._gui_data.track = _base._Dict(
            start_point=QtCore.QPointF()
        )

        # node move
        self._gui_data.node_move = _base._Dict(
            node_position_data=[]
        )

        # rect selection
        self._gui_data.rect_selection = _base._Dict(
            origin=QtCore.QPoint()
        )

        # menu
        self._gui_data.menu = _base._Dict(
            content=None,
            content_generate_fnc=None,
            data=None,
            data_generate_fnc=None,
            name_dict=dict()
        )

        self._gui_data.viewed = _base._Dict(
            node_path_set=set()
        )
        self._gui_data.edited = _base._Dict(
            node_path_set=set()
        )

        self._gui_data.image_cache_dict = bsc_core.LRUCache(maximum=1024)
        self._gui_data.video_cache_dict = bsc_core.LRUCache(maximum=1024)

        self.set_menu_data_generate_fnc(
            self._add_node_menu_data_generate_fnc
        )

        # node parameters
        self._param_root_stack_gui = None

    # image cache
    def remove_image_cache(self, key):
        if key in self._gui_data.image_cache_dict:
            self._gui_data.image_cache_dict.pop(key)

    def pull_image_cache(self, key):
        return self._gui_data.image_cache_dict.get(key)

    def push_image_cache(self, key, data):
        self._gui_data.image_cache_dict[key] = data

    # video cache
    def pull_video_cache(self, key):
        return self._gui_data.video_cache_dict.get(key)

    def push_video_cache(self, key, data):
        self._gui_data.video_cache_dict[key] = data

    def _add_node_menu_data_generate_fnc(self):
        sub_menu_data = []
        for k, v in self.NODE_GUI_CLS_DICT.items():
            if self._gui_language == 'chs':
                i_gui_type_name = v.get('type_gui_name_chs')
            else:
                i_gui_type_name = v.get('type_gui_name')

            i_name = i_gui_type_name or k

            sub_menu_data.append(
                (i_name, 'file/file', functools.partial(self._push_add_node_cmd, k))
            )

        if self._gui_language == 'chs':
            return [
                [
                    '添加节点', 'file/folder',
                    sub_menu_data
                ]
            ]
        else:
            return [
                [
                    'Add Node', 'file/folder',
                    sub_menu_data
                ]
            ]

    @_undo.GuiUndoFactory.push(_undo.UndoActions.NodeAdd)
    def _push_add_node_cmd(self, type_name, *args, **kwargs):
        def redo_fnc_():
            if type_name not in self.NODE_GUI_CLS_DICT:
                raise RuntimeError()

            node_data = self.NODE_GUI_CLS_DICT[type_name]
            model_cls = node_data['model_cls']

            flag, node = model_cls.create(self, path=new_node_path)
            w, h = node.get_size()
            node.set_position((p.x()-w/2, p.y()-h/2))
            return new_node_path

        def undo_fnc_():
            node = self.get_node(new_node_path)
            if node:
                self._unregister_node(node)
            return new_node_path

        new_node_path = self._find_next_node_path(self._data.nodes, type_name)
        point = QtGui.QCursor().pos()
        p = self._gui._map_from_global(point)

        return self, redo_fnc_, undo_fnc_

    def add_node(self, type_name, *args, **kwargs):
        if type_name not in self.NODE_GUI_CLS_DICT:
            raise RuntimeError()

        node_data = self.NODE_GUI_CLS_DICT[type_name]
        model_cls = node_data['model_cls']
        return model_cls.create(self, *args, **kwargs)

    # viewed
    def has_viewed_nodes(self):
        return bool(self._gui_data.viewed.node_path_set)

    def _check_node_viewed(self, node):
        return node.get_path() in self._gui_data.viewed.node_path_set

    def get_viewed_nodes(self):
        return filter(None, [self.get_node(x) for x in self._gui_data.viewed.node_path_set])

    def _clear_viewed_node(self):
        [x._update_viewed(False) for x in self.get_viewed_nodes()]
        self._gui_data.viewed.node_path_set.clear()

    def set_viewed_node(self, node):
        self._clear_viewed_node()
        node._update_viewed(True)
        self._gui_data.viewed.node_path_set.add(node.get_path())

    # edited
    def has_edited_nodes(self):
        return bool(self._gui_data.edited.node_path_set)

    def _check_node_edited(self, node):
        return node.get_path() in self._gui_data.edited.node_path_set

    def get_edited_nodes(self):
        return filter(None, [self.get_node(x) for x in self._gui_data.edited.node_path_set])

    def _clear_edited_node(self):
        [x._update_edited(False) for x in self.get_edited_nodes()]
        self._gui_data.edited.node_path_set.clear()

    def set_edited_node(self, node):
        self._clear_edited_node()
        node._update_edited(True)
        self._gui_data.edited.node_path_set.add(node.get_path())

        self._gui.node_edited_changed.emit(node.get_path())

    def crate_by_data(self, data):
        pass

    # node
    def get_node_path_set(self):
        return set(self._data.nodes.keys())

    @classmethod
    def register_node_type(cls, type_name, model_cls, gui_cls, type_gui_name=None, type_gui_name_chs=None):
        gui_cls.MODEL_CLS = model_cls
        cls.NODE_GUI_CLS_DICT[type_name] = dict(
            model_cls=model_cls,
            gui_cls=gui_cls,
            type_gui_name=type_gui_name,
            type_gui_name_chs=type_gui_name_chs,
        )

    def generate_node(self, type_name, name=None, parent_path=None, path=None, *args, **kwargs):
        if type_name not in self.NODE_GUI_CLS_DICT:
            raise RuntimeError()

        if path is None:
            if name is None:
                path = self._find_next_node_path(self._data.nodes, type_name, parent_path)
            else:
                path = '{}/{}'.format(parent_path or '', name)

        if path in self._data.nodes:
            return False, self._data.nodes[path]

        path_opt = bsc_core.BscNodePathOpt(path)
        node_data = self.NODE_GUI_CLS_DICT[type_name]
        gui_cls = node_data['gui_cls']
        gui = gui_cls()
        self._gui.scene().addItem(gui)

        model = gui._model
        model._set_type(
            type_name, gui_name=node_data['type_gui_name'], gui_name_chs=node_data['type_gui_name_chs']
        )
        model._set_path(path)
        model.set_name(kwargs.get('name', path_opt.get_name()))
        model._auto_resize()

        self._data.nodes[path] = model
        return True, model

    def _create_node_by_data(self, data):
        type_name = data['type']
        name = data['name']
        flag, node = self.generate_node(type_name, name)
        node.set_options(data['options'])
        for k, v in data.get('inputs', {}).items():
            node._add_input_by_data(v)
        for k, v in data.get('outputs', {}).items():
            node._add_output_by_data(v)
        for k, v in data.get('parameters', {}).items():
            node.parameters._add_parameter_by_data(v)
        return node

    def _remove_node_by_data(self, data):
        node = self.get_node(data['path'])
        if node:
            self._unregister_node(node)

    def _unregister_node(self, node):
        if self._param_root_stack_gui is not None:
            self._param_root_stack_gui._unregister_node(node)

        path = node.get_path()
        self._data.nodes.pop(path)
        gui = node._gui
        self._gui.scene().removeItem(gui)
        del gui

    def get_node(self, node_path):
        return self._data.nodes.get(node_path)

    def set_node_position(self, node_path, position):
        self.get_node(node_path).set_position(position)

    def set_node_size(self, node_path, size):
        self.get_node(node_path).set_size(size)

    def add_node_input(self, node_path, port_path):
        self.get_node(node_path).add_input(port_path=port_path)

    def remove_node_input(self, node_path, port_path):
        self.get_node(node_path).remove_input(port_path)

    def node_auto_connect_input(self, node_path, port_flag, port_path, source_path):
        node = self.get_node(node_path)
        if port_flag is True:
            node.add_input(port_path)

        target_path = bsc_core.BscAttributePath.join_by(node.get_path(), port_path)
        self._connect_port_paths(source_path, target_path)

    def node_auto_disconnect_input(self, node_path, port_flag, port_path, source_path):
        node = self.get_node(node_path)

        # disconnect first
        target_path = bsc_core.BscAttributePath.join_by(node.get_path(), port_path)
        self._disconnect_port_paths(source_path, target_path)

        if port_flag is True:
            node.remove_input(port_path)

    # connection
    def create_connection(self, source_arg, target_args):
        if isinstance(source_arg, six.string_types) and isinstance(target_args, six.string_types):
            self._connect_port_paths(source_arg, target_args)
        else:
            self._connect_ports(source_arg, target_args)

    def _connect_path(self, path):
        self._connect_port_paths(*self._split_to_connection_args(path))

    def _connect_paths(self, paths):
        [self._connect_path(x) for x in paths]

    def _to_node_input(self, atr_path):
        node_path, port_path = bsc_core.BscAttributePath.split_by(atr_path)
        return self.get_node(node_path).get_input(port_path)

    def _to_node_output(self, atr_path):
        node_path, port_path = bsc_core.BscAttributePath.split_by(atr_path)
        return self.get_node(node_path).get_output(port_path)

    def _connect_port_paths(self, source_path, target_path):
        source_path_opt = bsc_core.BscAttributePathOpt(source_path)
        source_node_path = source_path_opt.obj_path
        source_node = self.get_node(source_node_path)
        if not source_node:
            raise RuntimeError(
                'source node is not found: {}'.format(source_node_path)
            )
        source_port_path = source_path_opt.port_path
        source_port = source_node.get_output(source_port_path)
        if not source_port:
            raise RuntimeError(
                'source port is not found: {}'.format(source_path)
            )
        target_path_opt = bsc_core.BscAttributePathOpt(target_path)
        target_node_path = target_path_opt.obj_path
        target_node = self.get_node(target_node_path)
        if not target_node:
            raise RuntimeError(
                'target node is not found: {}'.format(target_node_path)
            )
        target_port_path = target_path_opt.port_path
        target_port = target_node.get_input(target_port_path)
        if not target_port:
            raise RuntimeError(
                'target port is not found: {}'.format(target_path)
            )

        if source_node_path == target_node_path:
            raise RuntimeError(
                'can not connect same port.'
            )

        return self._connect_ports(source_port, target_port)

    def _connect_ports(self, source_port, target_port):
        path = self._join_to_connection_path(source_port.get_path(), target_port.get_path())
        if path in self._gui_data.connection_dict:
            return False, self._gui_data.connection_dict[path]

        if target_port.has_source():
            # when target port has source, break connection first
            source_port_old = target_port.get_source()
            if self._disconnect_ports(source_port_old, target_port) is False:
                return False, None

        gui = self._builtin_data.connection.gui_cls(source_port, target_port)
        gui._set_hover_enable(True)
        model = gui._model
        model._set_path(path)
        model.update_v()

        source_port._register_connection(path)
        target_port._register_connection(path)
        self._gui.scene().addItem(gui)

        self._gui_data.connection_dict[path] = model
        return True, model

    @_undo.GuiUndoFactory.push(_undo.UndoActions.PortConnect)
    def _push_connect_cmd(self, source_port, target_port):
        def redo_fnc_():
            self._connect_path(path)
            return path

        def undo_fnc_():
            self._disconnect_path(path)
            return path

        path = self._join_to_connection_path(source_port.get_path(), target_port.get_path())
        if self.has_connection(path) is True:
            return
        return self, redo_fnc_, undo_fnc_
    
    @_undo.GuiUndoFactory.push(_undo.UndoActions.NodeInputConnectAuto)
    def _push_auto_connect_input_cmd(self, source_port, target_node):
        def redo_fnc_():
            self.node_auto_connect_input(node_path, port_flag, port_path, source_path)
            return node_path, port_path

        def undo_fnc_():
            self.node_auto_disconnect_input(node_path, port_flag, port_path, source_path)
            return node_path, port_path

        flag, port = target_node._generate_next_input_args()

        node_path, port_flag, port_path, source_path = (
            target_node.get_path(), flag, port.get_port_path(), source_port.get_path()
        )
        return self, redo_fnc_, undo_fnc_

    # disconnect
    def _disconnect_path(self, path):
        self._disconnect_port_paths(*self._split_to_connection_args(path))

    def _disconnect_paths(self, paths):
        [self._disconnect_path(x) for x in paths]

    def _disconnect_port_paths(self, source_path, target_path):
        self._disconnect_ports(
            self._to_node_output(source_path), self._to_node_input(target_path)
        )

    def _disconnect_ports(self, source_port, target_port):
        path = self._join_to_connection_path(source_port.get_path(), target_port.get_path())
        if path in self._gui_data.connection_dict:
            connection = self._gui_data.connection_dict[path]
            self._gui_data.connection_dict.pop(path)
            source_port._unregister_connection(path)
            target_port._unregister_connection(path)
            self._gui.scene().removeItem(connection._gui)
            return True
        return False

    @_undo.GuiUndoFactory.push(_undo.UndoActions.PortDisconnect)
    def _push_disconnect_cmd(self, source_port, target_port):
        def redo_fnc_():
            self._disconnect_path(path)
            return path

        def undo_fnc_():
            self._connect_path(path)
            return path

        path = self._join_to_connection_path(source_port.get_path(), target_port.get_path())
        return self, redo_fnc_, undo_fnc_

    def _reconnect_path(self, path_0, path_1):
        self._disconnect_path(path_0)
        self._connect_path(path_1)

    def _reconnect_paths(self, disconnect_paths, connect_paths):
        [self._disconnect_path(x) for x in disconnect_paths]
        [self._connect_path(x) for x in connect_paths]

    def _reconnect_source(self, source_port, target_port, source_port_new):
        path = self._join_to_connection_path(source_port.get_path(), target_port.get_path())
        self.remove_connection_path(path)
        self._connect_ports(source_port_new, target_port)

    def _reconnect_target(self, source_port, target_port, target_port_new):
        path = self._join_to_connection_path(source_port.get_path(), target_port.get_path())
        self.remove_connection_path(path)
        self._connect_ports(source_port, target_port_new)

    @_undo.GuiUndoFactory.push(_undo.UndoActions.PortReconnect)
    def _push_reconnect_cmd(self, disconnect_args, connect_args):
        def redo_fnc_():
            self._reconnect_paths(disconnect_paths, connect_paths)
            return '...'

        def undo_fnc():
            self._reconnect_paths(connect_paths, disconnect_paths)
            return '...'

        disconnect_paths = [self._join_to_connection_path(x[0].get_path(), x[1].get_path()) for x in disconnect_args]
        connect_paths = [self._join_to_connection_path(x[0].get_path(), x[1].get_path()) for x in connect_args]
        return self, redo_fnc_, undo_fnc

    def get_connection(self, path):
        return self._gui_data.connection_dict.get(path)

    def remove_connection_path(self, path):
        if path in self._gui_data.connection_dict:
            connection = self._gui_data.connection_dict[path]
            self._remove_connection(connection)
            return True
        return False

    def _remove_connection(self, connection):
        path = connection.get_path()
        source_port = connection.get_source()
        target_port = connection.get_target()
        source_port._unregister_connection(path)
        target_port._unregister_connection(path)
        self._gui_data.connection_dict.pop(path)
        self._gui.scene().removeItem(connection._gui)

    def has_connection(self, path):
        return path in self._gui_data.connection_dict

    @property
    def data(self):
        return self._data

    @property
    def gui_data(self):
        return self._gui_data

    # zoom
    def _do_zoom(self, event):
        zoom_in = event.angleDelta().y() > 0

        f = self._gui_data.zoom.factor
        factor = f if zoom_in else 1/f

        mouse_scene_pos = self._gui.mapToScene(event.pos())

        self._gui.scale(factor, factor)

        new_mouse_scene_pos = self._gui.mapToScene(event.pos())
        delta = new_mouse_scene_pos-mouse_scene_pos

        self._gui.translate(delta.x(), delta.y())

    # track
    def _do_track_start(self, event):
        self._gui_data.track.start_point = event.pos()
        self._gui.setCursor(QtCore.Qt.ClosedHandCursor)

    def _do_track_move(self, event):
        delta = event.pos()-self._gui_data.track.start_point
        self._gui_data.track.start_point = event.pos()
        scale_factor = self._gui.transform().m11()

        self._gui.translate(delta.x()/scale_factor, delta.y()/scale_factor)

    def _do_tack_end(self):
        self._gui.unsetCursor()

    # node move
    def _do_node_move_start(self, event):
        node_position_data = []

        items = self._gui.scene().selectedItems()
        for i in items:
            if i.ENTITY_TYPE in {_base.EntityTypes.Node}:
                i_node = i._model
                node_position_data.append(
                    (i_node.get_path(), i_node.get_position())
                )

        self._gui_data.node_move.node_position_data = node_position_data

    def _do_node_move(self, event):
        pass

    @_undo.GuiUndoFactory.push(_undo.UndoActions.NodeMove)
    def _push_node_move_cmd(self):
        def redo_fnc_():
            [self.set_node_position(*x) for x in redo_data]
            return '...'

        def undo_fnc_():
            [self.set_node_position(*x) for x in undo_data]
            return '...'

        redo_data = []
        undo_data = []

        for i in self._gui_data.node_move.node_position_data:
            i_node_path, i_node_position = i

            i_node = self.get_node(i_node_path)
            i_node_position_new = i_node.get_position()

            redo_data.append((i_node_path, i_node_position_new))
            undo_data.append((i_node_path, i_node_position))
        return self, redo_fnc_, undo_fnc_

    def _do_node_move_end(self):
        self._push_node_move_cmd()

    # node add input
    @_undo.GuiUndoFactory.push(_undo.UndoActions.NodeAddInput)
    def _push_add_node_input_cmd(self, node):
        def redo_fnc_():
            self.add_node_input(node_path, port_path_new)
            return node_path, port_path_new
        
        def undo_fnc_():
            self.remove_node_input(node_path, port_path_new)
            return node_path, port_path_new

        node_path = node.get_path()
        port_path_new = node._generate_next_input_path()
        return self, redo_fnc_, undo_fnc_

    # rect selection
    def _do_rect_selection_start(self, event):
        p = event.pos()
        self._gui_data.rect_selection.origin = p
        self._gui._rubber_band.setGeometry(QtCore.QRect(p, p))
        self._gui._rubber_band.show()

    def _do_rect_selection_move(self, event):
        p_0 = self._gui_data.rect_selection.origin
        rect = QtCore.QRect(p_0, event.pos()).normalized()
        self._gui._rubber_band.setGeometry(rect)

    def _do_rect_selection_end(self, event):
        self._gui._rubber_band.hide()

        rect = self._gui._rubber_band.geometry()
        scene_rect = self._gui.mapToScene(rect).boundingRect()

        selected_items = self._gui.scene().items(scene_rect, QtCore.Qt.IntersectsItemShape)

        if event.modifiers() == QtCore.Qt.ShiftModifier:
            for i_item in selected_items:
                if i_item.ENTITY_TYPE in {_base.EntityTypes.Node}:
                    i_item.setSelected(True)
        elif event.modifiers() == QtCore.Qt.ControlModifier:
            for i_item in selected_items:
                if i_item.ENTITY_TYPE in {_base.EntityTypes.Node}:
                    i_item.setSelected(False)
        else:
            self._gui.scene().clearSelection()
            for i_item in selected_items:
                if i_item.ENTITY_TYPE in {_base.EntityTypes.Node}:
                    i_item.setSelected(True)
    
    @_undo.GuiUndoFactory.push(_undo.UndoActions.Delete)
    def _push_delete_cmd(self, node_args, connection_args):
        def redo_fnc_():
            [self._disconnect_path(x) for x in connection_args]
            [self._remove_node_by_data(x) for x in node_args]
            return '...'
        
        def undo_fnc_():
            [self._create_node_by_data(x) for x in node_args]
            [self._connect_path(x) for x in connection_args]
            return '...'

        return self, redo_fnc_, undo_fnc_

    @_undo.GuiUndoFactory.push(_undo.UndoActions.Cut)
    def _push_cut_cmd(self, node_args, connection_args):
        def redo_fnc_():
            [self._disconnect_path(x) for x in connection_args]
            [self._remove_node_by_data(x) for x in node_args]
            return '...'

        def undo_fnc_():
            [self._create_node_by_data(x) for x in node_args]
            [self._connect_path(x) for x in connection_args]
            return '...'

        return self, redo_fnc_, undo_fnc_

    @_undo.GuiUndoFactory.push(_undo.UndoActions.Paste)
    def _push_paste_cmd(self, node_args, connection_args):
        def redo_fnc_():
            [self._create_node_by_data(x) for x in node_args]
            [self._connect_path(x) for x in connection_args]
            return '...'

        def undo_fnc_():
            [self._disconnect_path(x) for x in connection_args]
            [self._remove_node_by_data(x) for x in node_args]
            return '...'

        return self, redo_fnc_, undo_fnc_

    def _do_paste(self, node_args):
        node_group = _base._NodeGroup(self, node_args)
        node_args, connection_args = node_group.generate_create_data()

        self._push_paste_cmd(node_args, connection_args)

    # actions
    def _on_delete_action(self):
        node_args = []
        connection_args = []
        items = self._gui.scene().selectedItems()
        for i in items:
            if i.ENTITY_TYPE in {_base.EntityTypes.Node}:
                i_node = i._model
                i_connection_path_set = i_node.get_connection_path_set()
                connection_args.extend(list(i_connection_path_set))
                node_args.append(i_node.to_data())
            elif i.ENTITY_TYPE in {_base.EntityTypes.Backdrop}:
                node_args.append(i._model.to_data())
            elif i.ENTITY_TYPE in {_base.EntityTypes.Connection}:
                connection_args.append(i._model.get_path())

        if node_args or connection_args:
            self._push_delete_cmd(node_args, connection_args)

    def _on_copy_action(self):
        node_args = []
        items = self._gui.scene().selectedItems()
        for i in items:
            if i.ENTITY_TYPE in {_base.EntityTypes.Node, _base.EntityTypes.Backdrop}:
                node_args.append(i._model.to_data())

        if node_args:
            data_string = json.dumps(
                dict(
                    QSMMineData=dict(
                        type='scene',
                        data=node_args,
                        flag='copy'
                    ),
                )
            )
            gui_qt_core.QtUtil.write_clipboard(data_string)

    def _on_duplicate_action(self):
        node_args = []
        items = self._gui.scene().selectedItems()
        for i in items:
            if i.ENTITY_TYPE in {_base.EntityTypes.Node, _base.EntityTypes.Backdrop}:
                node_args.append(i._model.to_data())

        node_group = _base._NodeGroup(self, node_args)
        node_args, connection_args = node_group.generate_create_data()

        self._push_paste_cmd(node_args, connection_args)

    def _on_cut_action(self):
        node_args = []
        connection_args = []
        items = self._gui.scene().selectedItems()
        for i in items:
            if i.ENTITY_TYPE in {_base.EntityTypes.Node}:
                i_node = i._model
                i_connection_path_set = i_node.get_connection_path_set()
                connection_args.extend(list(i_connection_path_set))
                node_args.append(i_node.to_data())
            elif i.ENTITY_TYPE in {_base.EntityTypes.Connection}:
                connection_args.append(i._model.get_path())

        if node_args or connection_args:
            self._push_cut_cmd(node_args, connection_args)

            data_string = json.dumps(
                dict(
                    QSMMineData=dict(
                        type='scene',
                        data=node_args,
                        flag='cut'
                    ),
                )
            )
            gui_qt_core.QtUtil.write_clipboard(data_string)

    def _on_paste_action(self):
        text = gui_qt_core.QtUtil.read_clipboard()
        if text.startswith('{"QSMMineData": '):
            dict_ = json.loads(text)
            mine_data = dict_['QSMMineData']
            type_ = mine_data['type']
            if type_ == 'scene':
                node_args = mine_data['data']
                self._do_paste(node_args)
                flag = mine_data['flag']
                if flag == 'cut':
                    gui_qt_core.QtUtil.clear_clipboard()

    def _on_bypass_action(self):
        point = QtGui.QCursor().pos()
        p = self._gui._map_from_global(point)
        selection_area = QtGui.QPainterPath()
        selection_area.addRect(QtCore.QRectF(p.x()-1, p.y()-1, 2, 2))
        items = self._gui.scene().items(selection_area, QtCore.Qt.IntersectsItemShape)
        for i in items:
            if i.ENTITY_TYPE in {_base.EntityTypes.Node}:
                i._model._on_swap_bypass()

    def clear_selection(self):
        self._gui.scene().clearSelection()

    # menu
    def set_menu_content(self, content):
        self._gui_data.menu.content = content

    def get_menu_content(self):
        return self._gui_data.menu.content

    def set_menu_data(self, data):
        self._gui_data.menu.data = data

    def get_menu_data(self):
        return self._gui_data.menu.data

    def set_menu_data_generate_fnc(self, fnc):
        self._gui_data.menu.data_generate_fnc = fnc

    def get_menu_data_generate_fnc(self):
        return self._gui_data.menu.data_generate_fnc

    def set_menu_name_dict(self, dict_):
        if isinstance(dict_, dict):
            self._gui_data.menu.name_dict = dict_

    def get_menu_name_dict(self):
        return self._gui_data.menu.name_dict

    def to_json(self):
        return _base._ToJson(self._data._dict).generate()

    def to_data(self):
        return self._json_str_to_data(self.to_json())

    def _event_sent(self, data):
        self._gui.event_sent.emit(data)

    # parameter
    def _set_param_root_stack_gui(self, widget):
        self._param_root_stack_gui = widget

    # undo

    @contextlib.contextmanager
    def undo_group(self, name=''):
        self._gui._undo_group_index += 1
        self._gui._undo_stack.beginMacro('{}{}'.format(name, self._gui._undo_group_index))
        yield
        self._gui._undo_stack.endMacro()
