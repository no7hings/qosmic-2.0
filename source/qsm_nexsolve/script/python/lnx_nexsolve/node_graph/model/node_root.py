# coding:utf-8
import collections

import os

import contextlib

import functools

import json

import six

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

from lxgui.qt.core.wrap import *

import lxgui.qt.core as gui_qt_core

from ...core import base as _scn_cor_base

from ..core import base as _cor_base

from ..core import action as _cor_action

from ..core import undo as _cor_undo

from ...stage import model as _stg_model


class SceneFile(object):
    def __init__(self, root_model):
        self._root_model = root_model

        self._default_path = '{}/QSM/scenes/untitled.nxs_prj'.format(bsc_core.BscSystem.get_home_directory())
        self._current_path = self._default_path

        self._current_data = self._root_model.to_data()

    def is_dirty(self):
        return self._root_model.to_data() != self._current_data

    def get_current(self):
        return self._current_path

    def is_default(self):
        return self.get_current() == self._default_path

    def _set_current_path(self, file_path):
        self._current_path = file_path

    def _set_current_data(self, data):
        self._current_data = data

    def save_to(self, file_path):
        data = self._root_model.to_data()
        if data:
            bsc_storage.StgFileOpt(file_path).set_write(data)
            self._set_current_path(file_path)
            self._set_current_data(data)

    def save(self):
        self.save_to(self.get_current())

    def open(self, file_path):
        data = bsc_storage.StgFileOpt(file_path).set_read()
        if data:
            self._root_model.load_from_data(data)
            self._set_current_path(file_path)
            self._set_current_data(data)

    def new(self):
        self._current_path = self._default_path
        return self._root_model.restore()

    def new_with_dialog(self):
        if self.is_dirty() is True:
            if gui_core.GuiUtil.language_is_chs():
                result = gui_core.GuiApplication.exec_message_dialog(
                    u'保存修改到: {}?'.format(
                        self.get_current()
                    ),
                    title='保存文件？',
                    show_no=True,
                    show_cancel=True,
                    size=(320, 120),
                    status='warning',
                )
            else:
                result = gui_core.GuiApplication.exec_message_dialog(
                    u'Save changes to: {}?'.format(
                        self.get_current()
                    ),
                    title='Save Scene?',
                    show_no=True,
                    show_cancel=True,
                    size=(320, 120),
                    status='warning',
                )
            if result is True:
                self.save_to(self.get_current())
                self.new()
                return True
            elif result is False:
                self.new()
                return True
        else:
            self.new()
            return True
        return False

    def open_with_dialog(self, file_path):
        if self.is_dirty() is True:
            if gui_core.GuiUtil.language_is_chs():
                result = gui_core.GuiApplication.exec_message_dialog(
                    u'保存修改到: {}?'.format(
                        self.get_current()
                    ),
                    title='保存文件？',
                    show_no=True,
                    show_cancel=True,
                    size=(320, 120),
                    status='warning'
                )
            else:
                result = gui_core.GuiApplication.exec_message_dialog(
                    u'Save changes to: {}?'.format(
                        self.get_current()
                    ),
                    title='Save Scene?',
                    show_no=True,
                    show_cancel=True,
                    size=(320, 120),
                    status='warning'
                )

            if result is True:
                self.save_to(self.get_current())
                self.open(file_path)
                return True
            elif result is False:
                self.open(file_path)
                return True
        else:
            self.open(file_path)
            return True
        return False
    
    def save_as_with_dialog(self, file_path):
        # check file directory is changed, when changed save to.
        if os.path.abspath(file_path) == os.path.abspath(self.get_current()):
            if self.is_dirty() is True:
                self.save_to(file_path)
                return True

            if gui_core.GuiUtil.language_is_chs():
                gui_core.GuiApplication.exec_message_dialog(
                    '沒有需要保存的更改。',
                    title='保存文件',
                    size=(320, 120),
                    status='warning',
                )
            else:
                gui_core.GuiApplication.exec_message_dialog(
                    'No changes to save.',
                    title='Save Scene',
                    size=(320, 120),
                    status='warning',
                )
            return False
        self.save_to(file_path)
        return True

    def save_with_dialog(self):
        self.save_as_with_dialog(self.get_current())


# scene model
class RootNode(
    _scn_cor_base._SbjBase,
    _cor_action._AbsAction
):
    ActionFlags = _cor_action.ActionFlags

    NODE_GUI_CLS_DICT = dict()

    def __init__(self, gui_widget):
        super(RootNode, self).__init__(gui_widget)

        self._close_flag = False

        self._data.type = 'root'
        self._data.path = '/'
        self._data.name = ''

        self._data.nodes = collections.OrderedDict()
        self._builtin_data.connection_dict = collections.OrderedDict()

        self._data.options = _scn_cor_base._Dict(
            translate=_scn_cor_base._Dict(
                x=0, y=0,
            ),
            scale=_scn_cor_base._Dict(
                x=1, y=1,
            ),
        )

        # connection
        self._builtin_data.connection = _scn_cor_base._Dict(
            gui_cls=None,
        )

        self._init_action()
        self._pan_start = QtCore.QPoint()

        self._gui_data.zoom = _scn_cor_base._Dict(
            factor=1.2
        )
        self._gui_data.track = _scn_cor_base._Dict(
            start_point=QtCore.QPointF()
        )

        # node move
        self._gui_data.node_move = _scn_cor_base._Dict(
            node_position_data=[]
        )

        # rect selection
        self._gui_data.rect_selection = _scn_cor_base._Dict(
            origin=QtCore.QPoint()
        )

        # menu
        self._gui_data.menu = _scn_cor_base._Dict(
            content=None,
            content_generate_fnc=None,
            data=None,
            data_generate_fnc=None,
            name_dict=dict()
        )

        self._gui_data.viewed = _scn_cor_base._Dict(
            node_path_set=set()
        )
        self._gui_data.edited = _scn_cor_base._Dict(
            node_path_set=set()
        )

        self._gui_data.image_cache_dict = bsc_core.LRUCache(maximum=1024)
        self._gui_data.video_cache_dict = bsc_core.LRUCache(maximum=1024)

        self.set_menu_data_generate_fnc(
            self._add_node_menu_data_generate_fnc
        )

        # node parameters
        self._param_root_stack_gui = None

        self._stage_model = None

        self._scene_file = SceneFile(self)

    def get_gui_scene(self):
        return self._gui.scene()

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

    @_cor_undo.GuiUndoFactory.push(_cor_undo.UndoActions.NodeAdd)
    def _push_add_node_cmd(self, type_name, *args, **kwargs):
        def _redo_fnc():
            if type_name not in self.NODE_GUI_CLS_DICT:
                raise RuntimeError()

            node_data = self.NODE_GUI_CLS_DICT[type_name]
            model_cls = node_data['model_cls']

            flag, node = self._generate_node(type_name, **kwargs)
            model_cls.create(node)
            w, h = node.get_size()
            node._set_position((p.x()-w/2, p.y()-h/2))
            return flag, node

        def _undo_fnc():
            node = self.get_node(node_path_new)
            if node:
                self._unregister_node(node)
            return node_path_new

        if 'path' in kwargs:
            node_path_new = kwargs['path']
        else:
            node_path_new = self._find_next_node_path(self._data.nodes, type_name, **kwargs)

        point = QtGui.QCursor().pos()
        p = self._gui._map_from_global(point)

        return self.undo_stack, _redo_fnc, _undo_fnc

    @_cor_undo.GuiUndoFactory.push(_cor_undo.UndoActions.NodeAdd)
    def add_node(self, type_name, *args, **kwargs):
        # do not remove *args
        def _redo_fnc():
            if type_name not in self.NODE_GUI_CLS_DICT:
                raise RuntimeError()

            node_data = self.NODE_GUI_CLS_DICT[type_name]
            model_cls = node_data['model_cls']

            flag, node = self._generate_node(type_name, **kwargs)
            model_cls.create(node)
            return flag, node

        def _undo_fnc():
            node = self.get_node(node_path_new)
            if node:
                self._unregister_node(node)
            return node_path_new

        if 'path' in kwargs:
            node_path_new = kwargs['path']
        else:
            node_path_new = self._find_next_node_path(self._data.nodes, type_name, **kwargs)

        return self.undo_stack, _redo_fnc, _undo_fnc

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
        node_path = node.get_path()
        if node_path not in self._gui_data.viewed.node_path_set:
            self._clear_viewed_node()

            node._update_viewed(True)
            self._gui_data.viewed.node_path_set.add(node.get_path())

            self._update_stage_for(node)
            return True
        return False

    def _update_stage_for(self, node):
        self._stage_model = node.compute_chain_to_stage()
        print(self._stage_model)

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
        node_path = node.get_path()
        if node_path not in self._gui_data.edited.node_path_set:
            self._clear_edited_node()
            node._update_edited(True)
            self._gui_data.edited.node_path_set.add(node_path)
            self._gui.node_edited_changed.emit(node_path)
            return True
        return False

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

    def _generate_node(self, type_name, name=None, parent_path=None, path=None, *args, **kwargs):
        if type_name not in self.NODE_GUI_CLS_DICT:
            raise RuntimeError()

        if path is None:
            prefix = name or type_name
            path = self._find_next_node_path(self._data.nodes, prefix, parent_path)

        if path in self._data.nodes:
            return False, self._data.nodes[path]

        path_opt = bsc_core.BscNodePathOpt(path)
        node_data = self.NODE_GUI_CLS_DICT[type_name]
        gui_cls = node_data['gui_cls']
        gui = gui_cls()
        self._gui.scene().addItem(gui)

        model = gui._model
        model._set_root_model(self)
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
        flag, node = self._generate_node(type_name, name)
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
        # remove in param root
        if self._param_root_stack_gui is not None:
            self._param_root_stack_gui._unregister_node(node)

        node_path = node.get_path()

        # remove view
        if node_path in self._gui_data.viewed.node_path_set:
            self._gui_data.viewed.node_path_set.remove(node_path)

        # remove edit
        if node_path in self._gui_data.edited.node_path_set:
            self._gui_data.edited.node_path_set.remove(node_path)

        # remove from scene
        self._data.nodes.pop(node_path)
        gui = node._gui
        self._gui.scene().removeItem(gui)
        del gui

    def get_all_nodes(self):
        return list(self._data.nodes.values())

    def get_node(self, node_path):
        return self._data.nodes.get(node_path)

    def set_node_position(self, node_path, position):
        self.get_node(node_path).set_position(position)

    def _set_node_position(self, node_path, position):
        self.get_node(node_path)._set_position(position)

    def set_node_size(self, node_path, size):
        self.get_node(node_path).set_size(size)

    def add_node_input(self, node_path, port_path):
        self.get_node(node_path)._generate_input(port_path=port_path)

    def remove_node_input(self, node_path, port_path):
        self.get_node(node_path)._remove_input(port_path)

    def node_auto_connect_input(self, node_path, port_path, port_flag, source_path):
        node = self.get_node(node_path)

        # add input first
        if port_flag is True:
            node._generate_input(port_path=port_path)

        target_path = bsc_core.BscAttributePath.join_by(node.get_path(), port_path)
        self._connect_port_paths(source_path, target_path)

    def node_auto_disconnect_input(self, node_path, port_path, port_flag, source_path):
        node = self.get_node(node_path)

        # disconnect first
        target_path = bsc_core.BscAttributePath.join_by(node.get_path(), port_path)
        self._disconnect_port_paths(source_path, target_path)

        # remove added input later
        if port_flag is True:
            node._remove_input(port_path)

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
        if path in self._builtin_data.connection_dict:
            return False, self._builtin_data.connection_dict[path]

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

        self._builtin_data.connection_dict[path] = model
        return True, model

    @_cor_undo.GuiUndoFactory.push(_cor_undo.UndoActions.PortConnect)
    def connect_ports(self, source_port, target_port):
        def _redo_fnc():
            self._connect_path(path)
            return path

        def _undo_fnc():
            self._disconnect_path(path)
            return path

        path = self._join_to_connection_path(source_port.get_path(), target_port.get_path())
        if self.has_connection(path) is True:
            return

        return self.undo_stack, _redo_fnc, _undo_fnc
    
    @_cor_undo.GuiUndoFactory.push(_cor_undo.UndoActions.NodeInputConnectAuto)
    def _push_connect_input_auto_cmd(self, source_port, target_node):
        def _redo_fnc():
            self.node_auto_connect_input(node_path, port_path, port_flag, source_path)

        def _undo_fnc():
            self.node_auto_disconnect_input(node_path, port_path, port_flag, source_path)

        flag, target_port = target_node._generate_next_input_args()

        source_path = source_port.get_path()

        node_path, port_path, port_flag = (
            target_node.get_path(), target_port.get_port_path(), flag
        )

        return self.undo_stack, _redo_fnc, _undo_fnc

    @_cor_undo.GuiUndoFactory.push(_cor_undo.UndoActions.NodeInputReconnectAuto)
    def _push_reconnect_input_auto_cmd(self, source_port, target_port, target_node):
        def _redo_fnc():
            self._disconnect_port_paths(source_path_0, target_path_0)
            self.node_auto_connect_input(node_path, port_path, port_flag, source_path_0)

        def _undo_fnc():
            self.node_auto_disconnect_input(node_path, port_path, port_flag, source_path_0)
            self._connect_port_paths(source_path_0, target_path_0)

        source_path_0, target_path_0 = source_port.get_path(), target_port.get_path()

        flag, target_port_1 = target_node._generate_next_input_args()

        node_path, port_path, port_flag = (
            target_node.get_path(), target_port_1.get_port_path(), flag
        )
        return self.undo_stack, _redo_fnc, _undo_fnc

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
        if path in self._builtin_data.connection_dict:
            connection = self._builtin_data.connection_dict[path]
            self._builtin_data.connection_dict.pop(path)
            source_port._unregister_connection(path)
            target_port._unregister_connection(path)
            self._gui.scene().removeItem(connection._gui)
            return True
        return False

    @_cor_undo.GuiUndoFactory.push(_cor_undo.UndoActions.PortDisconnect)
    def disconnect_ports(self, source_port, target_port):
        def _redo_fnc():
            self._disconnect_path(path)
            return path

        def _undo_fnc():
            self._connect_path(path)
            return path

        path = self._join_to_connection_path(source_port.get_path(), target_port.get_path())

        return self.undo_stack, _redo_fnc, _undo_fnc

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

    @_cor_undo.GuiUndoFactory.push(_cor_undo.UndoActions.PortReconnect)
    def _push_reconnect_cmd(self, disconnect_args, connect_args):
        def _redo_fnc():
            self._reconnect_paths(disconnect_paths, connect_paths)
            return '...'

        def _undo_fnc():
            self._reconnect_paths(connect_paths, disconnect_paths)
            return '...'

        disconnect_paths = [self._join_to_connection_path(x[0].get_path(), x[1].get_path()) for x in disconnect_args]
        connect_paths = [self._join_to_connection_path(x[0].get_path(), x[1].get_path()) for x in connect_args]

        return self.undo_stack, _redo_fnc, _undo_fnc

    def get_all_connections(self):
        return list(self._builtin_data.connection_dict.values())

    def get_connection(self, path):
        return self._builtin_data.connection_dict.get(path)

    def remove_connection_path(self, path):
        if path in self._builtin_data.connection_dict:
            connection = self._builtin_data.connection_dict[path]
            self._unregister_connection(connection)
            return True
        return False

    def _unregister_connection(self, connection):
        path = connection.get_path()
        source_port = connection.get_source()
        target_port = connection.get_target()
        source_port._unregister_connection(path)
        target_port._unregister_connection(path)
        self._builtin_data.connection_dict.pop(path)
        self._gui.scene().removeItem(connection._gui)

    def has_connection(self, path):
        return path in self._builtin_data.connection_dict

    @property
    def data(self):
        return self._data

    @property
    def gui_data(self):
        return self._gui_data

    # translate and scale
    def _save_translate(self, translate):
        x, y = translate
        self._data.options.translate.x = x
        self._data.options.translate.y = y

    def _set_translate(self, translate):
        self._save_translate(translate)

        tx, ty = translate
        sx, sy = self._get_gui_scale()
        self._set_gui_transformation(tx, ty, sx, sy)

    def _get_translate(self):
        return self._data.options.translate.x, self._data.options.translate.y

    def _save_scale(self, scale):
        x, y = scale
        self._data.options.scale.x = x
        self._data.options.scale.y = y

    def _get_scale_(self):
        return self._data.option.scale.x, self._data.option.scale.y

    def _set_scale(self, scale):
        sx, sy = scale
        transform = self._gui.transform()
        transform.reset()
        transform.scale(sx, sy)

    # options
    def _set_options(self, options):
        tx, ty = options['translate']['x'], options['translate']['y']
        self._save_translate((tx, ty))
        sx, sy = options['scale']['x'], options['scale']['y']
        self._save_scale((sx, sy))

        self._set_gui_transformation(tx, ty, sx, sy)

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

        self._update_transformation()

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
        self._update_transformation()

        self._gui.unsetCursor()

    def _update_transformation(self):
        tx, ty, sx, sy = self._get_gui_transformation_args()
        self._save_translate((tx, ty))
        self._save_scale((sx, sy))

    def _get_gui_translate(self):
        transform = self._gui.transform()
        return transform.dx(), transform.dy()

    def _get_gui_scale(self):
        transform = self._gui.transform()
        return transform.m11(), transform.m22()

    def _get_gui_transformation_args(self):
        transform = self._gui.transform()
        return transform.dx(), transform.dy(), transform.m11(), transform.m22()

    def _set_gui_transformation(self, tx, ty, sx, sy):
        transform = self._gui.transform()
        transform.reset()
        transform.scale(sx, sy)
        transform.translate(tx/sx, ty/sy)
        self._gui.setTransform(transform)

    # node move
    def _do_node_move_start(self, event):
        node_position_data = []

        items = self._gui.scene().selectedItems()
        for i in items:
            if i.ENTITY_TYPE in {_scn_cor_base.EntityTypes.Node}:
                i_node = i._model
                node_position_data.append(
                    (i_node.get_path(), i_node._get_gui_position())
                )

        self._gui_data.node_move.node_position_data = node_position_data

    def _do_node_move(self, event):
        pass

    @_cor_undo.GuiUndoFactory.push(_cor_undo.UndoActions.NodeMove)
    def _push_node_move_cmd(self):
        def _redo_fnc():
            [self._set_node_position(*x) for x in redo_data]
            return '...'

        def _undo_fnc():
            [self._set_node_position(*x) for x in undo_data]
            return '...'

        redo_data = []
        undo_data = []

        for i in self._gui_data.node_move.node_position_data:
            i_node_path, i_node_position = i

            i_node = self.get_node(i_node_path)
            i_node_position_new = i_node._get_gui_position()

            if i_node_position_new != i_node_position:
                redo_data.append((i_node_path, i_node_position_new))
                undo_data.append((i_node_path, i_node_position))

        if redo_data or undo_data:
            return self.undo_stack, _redo_fnc, _undo_fnc

    def _do_node_move_end(self):
        self._push_node_move_cmd()

    # node add input
    @_cor_undo.GuiUndoFactory.push(_cor_undo.UndoActions.NodeAddInput)
    def _push_add_node_input_cmd(self, node):
        def _redo_fnc():
            self.add_node_input(node_path, port_path_new)
            return node_path, port_path_new
        
        def _undo_fnc():
            self.remove_node_input(node_path, port_path_new)
            return node_path, port_path_new

        node_path = node.get_path()
        port_path_new = node._generate_next_input_path()

        return self.undo_stack, _redo_fnc, _undo_fnc

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
                if i_item.ENTITY_TYPE in {_scn_cor_base.EntityTypes.Node}:
                    i_item.setSelected(True)
        elif event.modifiers() == QtCore.Qt.ControlModifier:
            for i_item in selected_items:
                if i_item.ENTITY_TYPE in {_scn_cor_base.EntityTypes.Node}:
                    i_item.setSelected(False)
        else:
            self._gui.scene().clearSelection()
            for i_item in selected_items:
                if i_item.ENTITY_TYPE in {_scn_cor_base.EntityTypes.Node}:
                    i_item.setSelected(True)
    
    @_cor_undo.GuiUndoFactory.push(_cor_undo.UndoActions.Delete)
    def _push_delete_cmd(self, node_args, connection_args):
        def _redo_fnc():
            [self._disconnect_path(x) for x in connection_args]
            [self._remove_node_by_data(x) for x in node_args]
            return '...'
        
        def _undo_fnc():
            [self._create_node_by_data(x) for x in node_args]
            [self._connect_path(x) for x in connection_args]
            return '...'

        return self.undo_stack, _redo_fnc, _undo_fnc

    @_cor_undo.GuiUndoFactory.push(_cor_undo.UndoActions.Cut)
    def _push_cut_cmd(self, node_args, connection_args):
        def _redo_fnc():
            [self._disconnect_path(x) for x in connection_args]
            [self._remove_node_by_data(x) for x in node_args]
            return '...'

        def _undo_fnc():
            [self._create_node_by_data(x) for x in node_args]
            [self._connect_path(x) for x in connection_args]
            return '...'

        return self.undo_stack, _redo_fnc, _undo_fnc

    @_cor_undo.GuiUndoFactory.push(_cor_undo.UndoActions.Paste)
    def _push_paste_cmd(self, node_args, connection_args):
        def _redo_fnc():
            [self._create_node_by_data(x) for x in node_args]
            [self._connect_path(x) for x in connection_args]
            return '...'

        def _undo_fnc():
            [self._disconnect_path(x) for x in connection_args]
            [self._remove_node_by_data(x) for x in node_args]
            return '...'

        return self.undo_stack, _redo_fnc, _undo_fnc

    def _do_paste(self, node_args):
        node_group = _cor_base._NodeGroup(self, node_args)
        node_args, connection_args = node_group.generate_create_data()

        self._push_paste_cmd(node_args, connection_args)

    # actions
    def _on_delete_action(self):
        node_args = []
        connection_args = []
        items = self._gui.scene().selectedItems()
        for i in items:
            if i.ENTITY_TYPE in {_scn_cor_base.EntityTypes.Node}:
                i_node = i._model
                i_connection_path_set = i_node.get_connection_path_set()
                connection_args.extend(list(i_connection_path_set))
                node_args.append(i_node.to_data())
            elif i.ENTITY_TYPE in {_scn_cor_base.EntityTypes.Backdrop}:
                node_args.append(i._model.to_data())
            elif i.ENTITY_TYPE in {_scn_cor_base.EntityTypes.Connection}:
                connection_args.append(i._model.get_path())

        if node_args or connection_args:
            self._push_delete_cmd(node_args, connection_args)

    def _on_copy_action(self):
        node_args = []
        items = self._gui.scene().selectedItems()
        for i in items:
            if i.ENTITY_TYPE in {_scn_cor_base.EntityTypes.Node, _scn_cor_base.EntityTypes.Backdrop}:
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
            if i.ENTITY_TYPE in {_scn_cor_base.EntityTypes.Node, _scn_cor_base.EntityTypes.Backdrop}:
                node_args.append(i._model.to_data())

        node_group = _cor_base._NodeGroup(self, node_args)
        node_args, connection_args = node_group.generate_create_data()

        self._push_paste_cmd(node_args, connection_args)

    def _on_cut_action(self):
        node_args = []
        connection_args = []
        items = self._gui.scene().selectedItems()
        for i in items:
            if i.ENTITY_TYPE in {_scn_cor_base.EntityTypes.Node}:
                i_node = i._model
                i_connection_path_set = i_node.get_connection_path_set()
                connection_args.extend(list(i_connection_path_set))
                node_args.append(i_node.to_data())
            elif i.ENTITY_TYPE in {_scn_cor_base.EntityTypes.Connection}:
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
            # keep order
            dict_ = json.loads(text, object_pairs_hook=collections.OrderedDict)
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
            if i.ENTITY_TYPE in {_scn_cor_base.EntityTypes.Node}:
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
        return _scn_cor_base._ToJson(self._data._dict).generate()

    def to_data(self):
        return self._json_str_to_data(self.to_json())

    def _event_sent(self, event_type, event_id, data):
        self._gui.event_sent.emit(event_type, event_id, data)

    def _get_selected_node_guis(self):
        list_ = []
        items = self._gui.scene().selectedItems()

        for i in items:
            if i.ENTITY_TYPE in {_scn_cor_base.EntityTypes.Node, _scn_cor_base.EntityTypes.Backdrop}:
                list_.append(i)

        return list_

    def _get_all_node_guis(self):
        return [i._gui for i in self.get_all_nodes()]

    # frame select
    def _on_frame_select_action(self):
        items = self._get_selected_node_guis()
        if not items:
            items = self._get_all_node_guis()

        if not items:
            return

        bounding_rect = self._compute_items_rect(items)

        if bounding_rect.isEmpty() is False:
            padding = 20
            self._gui.fitInView(
                bounding_rect.adjusted(-padding, -padding, padding, padding), QtCore.Qt.KeepAspectRatio
            )

            self._update_transformation()

    @classmethod
    def _compute_items_rect(cls, items):
        bounding_rect = items[0].sceneBoundingRect()
        for item in items[1:]:
            bounding_rect = bounding_rect.united(item.sceneBoundingRect())
        return bounding_rect

    # parameter
    def _set_param_root_stack_gui(self, widget):
        self._param_root_stack_gui = widget

    # undo
    @contextlib.contextmanager
    def undo_group(self, name=None):
        self._gui._undo_group_index += 1
        self.undo_stack.beginMacro('{}{}'.format(name or '', self._gui._undo_group_index))
        yield
        self.undo_stack.endMacro()

    @contextlib.contextmanager
    def disable_undo(self):
        self.undo_stack.setActive(False)
        yield
        self.undo_stack.setActive(True)

    @property
    def undo_stack(self):
        return self._gui._undo_stack

    def restore(self):
        for i in self.get_all_connections():
            self._unregister_connection(i)

        for i in self.get_all_nodes():
            self._unregister_node(i)

        self.undo_stack.clear()

    def load_from_data(self, data):
        self.restore()

        # node
        for i_k, i_v in data['nodes'].items():
            self._create_node_by_data(i_v)

        # connections
        for i_node_path, i_v in data['nodes'].items():
            for j_port_path, j_v in i_v.get('inputs', {}).items():
                j_source_path = j_v['source']
                if j_source_path:
                    j_target_path = self._join_to_attr_path(i_node_path, j_port_path)
                    self._connect_port_paths(j_source_path, j_target_path)

        self._set_options(data['options'])

    # file
    def _on_new_file_action(self):
        if self._scene_file.new_with_dialog():
            self._gui.scene_path_accepted.emit(self._scene_file.get_current())

    def _on_open_file_action(self):
        file_path = gui_core.GuiStorageDialog.open_file(
            ext_filter='All File (*.nxs_prj)',
            parent=self._gui,
            default=self._scene_file.get_current(),
            title='Open Scene'
        )
        if file_path:
            if self._scene_file.open_with_dialog(file_path):
                self._gui.scene_path_accepted.emit(self._scene_file.get_current())

    def _on_save_file_action(self):
        if self._scene_file.is_default():
            file_path = gui_core.GuiStorageDialog.save_file(
                ext_filter='All File (*.nxs_prj)',
                parent=self._gui,
                default=self._scene_file.get_current(),
                title='Save Scene'
            )
            if file_path:
                if self._scene_file.save_as_with_dialog(file_path):
                    self._gui.scene_path_accepted.emit(self._scene_file.get_current())
        else:
            if self._scene_file.save_with_dialog():
                self._gui.scene_path_accepted.emit(self._scene_file.get_current())

    def _on_save_file_as_action(self):
        file_path = gui_core.GuiStorageDialog.save_file(
            ext_filter='All File (*.nxs_prj)',
            parent=self._gui,
            default=self._scene_file.get_current(),
            title='Save Scene As'
        )
        if file_path:
            if self._scene_file.save_as_with_dialog(file_path):
                self._gui.scene_path_accepted.emit(self._scene_file.get_current())
