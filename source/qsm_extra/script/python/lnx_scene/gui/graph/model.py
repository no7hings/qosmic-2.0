# coding:utf-8
import re

import sys

import collections

import functools

import json

import enum

import six

import lxbasic.core as bsc_core
# gui
import lxgui.core as gui_core

from lxgui.qt.core.wrap import *

import lxgui.qt.core as gui_qt_core

from . import base as _base


class _QtUndoCommand(QtWidgets.QUndoCommand):
    class Actions(enum.IntEnum):
        Connect = 0x00
        Disconnect = 0x01
        Reconnect = 0x02

        Delete = 0x10

        Copy = 0x11
        Cut = 0x12
        Paste = 0x13
        PasteCut = 0x14

        NodeMove = 0x20
        NodeResize = 0x21

    ACTION_NAME_MAP = {
        Actions.Connect: 'Connect',
        Actions.Disconnect: 'Disconnect',
        Actions.Reconnect: 'Reconnect',
    }

    @classmethod
    def trace(cls, text):
        return sys.stdout.write(text+'\n')

    @classmethod
    def trace_error(cls, text):
        return sys.stderr.write(text+'\n')

    def __init__(self, scene_model, data):
        super(_QtUndoCommand, self).__init__()
        self._scene_model = scene_model
        self._data = data

    def undo(self):
        for i_flag, i_args in self._data:
            if i_flag == self.Actions.Connect:
                self._scene_model._disconnect_path(i_args)
                self.trace('{}: {}'.format(self.ACTION_NAME_MAP[i_flag], i_args))
            elif i_flag == self.Actions.Disconnect:
                self._scene_model._connect_path(i_args)
                self.trace('{}: {}'.format(self.ACTION_NAME_MAP[i_flag], i_args))
            elif i_flag == self.Actions.Reconnect:
                i_path_0, i_path_1 = i_args
                self._scene_model._reconnect_path(i_path_1, i_path_0)
                self.trace('{}: {}'.format(self.ACTION_NAME_MAP[i_flag], i_args))
            elif i_flag == self.Actions.Delete:
                i_node_args, i_connection_args = i_args
                for j_args in i_node_args:
                    self._scene_model.create_node_by_data(j_args)
                for j_args in i_connection_args:
                    self._scene_model._connect_path(j_args)
            elif i_flag == self.Actions.Cut:
                i_node_args, i_connection_args = i_args
                for j_args in i_node_args:
                    self._scene_model.create_node_by_data(j_args)
                for j_args in i_connection_args:
                    self._scene_model._connect_path(j_args)
            elif i_flag == self.Actions.NodeMove:
                i_node_path, i_position_0, i_position_1 = i_args
                self._scene_model.set_node_position(i_node_path, i_position_0)
            elif i_flag == self.Actions.NodeResize:
                i_node_path, i_size_0, i_size_1 = i_args
                self._scene_model.set_node_size(i_node_path, i_size_0)
            elif i_flag == self.Actions.Paste:
                i_node_args, i_connection_args = i_args
                for j_args in i_connection_args:
                    self._scene_model._disconnect_path(j_args)
                for j_args in i_node_args:
                    self._scene_model._remove_node_by_data(j_args)

    def redo(self):
        for i_flag, i_args in self._data:
            if i_flag == self.Actions.Connect:
                self._scene_model._connect_path(i_args)
                self.trace('{}: {}'.format(self.ACTION_NAME_MAP[i_flag], i_args))
            elif i_flag == self.Actions.Disconnect:
                self._scene_model._disconnect_path(i_args)
                self.trace('{}: {}'.format(self.ACTION_NAME_MAP[i_flag], i_args))
            elif i_flag == self.Actions.Reconnect:
                i_path_0, i_path_1 = i_args
                self._scene_model._reconnect_path(i_path_0, i_path_1)
                self.trace('{}: {}'.format(self.ACTION_NAME_MAP[i_flag], i_args))
            elif i_flag == self.Actions.Delete:
                i_node_args, i_connection_args = i_args
                for j_args in i_connection_args:
                    self._scene_model._disconnect_path(j_args)
                for j_args in i_node_args:
                    self._scene_model._remove_node_by_data(j_args)
            elif i_flag == self.Actions.Cut:
                i_node_args, i_connection_args = i_args
                for j_args in i_connection_args:
                    self._scene_model._disconnect_path(j_args)
                for j_args in i_node_args:
                    self._scene_model._remove_node_by_data(j_args)
            elif i_flag == self.Actions.NodeMove:
                i_node_path, i_position_0, i_position_1 = i_args
                self._scene_model.set_node_position(i_node_path, i_position_1)
            elif i_flag == self.Actions.NodeResize:
                i_node_path, i_size_0, i_size_1 = i_args
                self._scene_model.set_node_size(i_node_path, i_size_1)
            elif i_flag == self.Actions.Paste:
                i_node_args, i_connection_args = i_args
                for j_args in i_node_args:
                    self._scene_model.create_node_by_data(j_args)
                for j_args in i_connection_args:
                    self._scene_model._connect_path(j_args)


# connection model
class _ConnectionModel(_base._SbjBase):
    SEP = '->'

    def __init__(self, item):
        super(_ConnectionModel, self).__init__(item)
        self._data.category = 'connection'

    @classmethod
    def _to_path(cls, source_path, target_path):
        return cls.SEP.join([source_path, target_path])

    @classmethod
    def _to_args(cls, path):
        return path.split(cls.SEP)

    @classmethod
    def _get_source(cls, scene_model, path):
        source_path, _ = path.split(cls.SEP)
        node_path, port_path = bsc_core.BscAttributePath.split_by(source_path)
        return scene_model.get_node(node_path).get_output_port(port_path)

    @classmethod
    def _get_target(cls, scene_model, path):
        _, target_path = path.split(cls.SEP)
        node_path, port_path = bsc_core.BscAttributePath.split_by(target_path)
        return scene_model.get_node(node_path).get_input_port(port_path)

    def get_source(self):
        return self._get_source(self.scene_model, self.get_path())

    def get_target(self):
        return self._get_target(self.scene_model, self.get_path())

    def do_delete(self):
        self.scene_model.remove_connection_path(self.get_path())

    # update
    def update_v(self, *args, **kwargs):
        self._item._update_v(*args, **kwargs)

    def update_h(self, *args, **kwargs):
        self._item._update_h(*args, **kwargs)

    def reset_status(self):
        self._item._set_color(
            QtGui.QColor(255, 255, 0, 255)
        )

    def to_correct_status(self):
        self._item._set_color(
            QtGui.QColor(0, 255, 0, 255)
        )


# port model
class _PortModel(_base._SbjBase):

    def __init__(self, *args, **kwargs):
        super(_PortModel, self).__init__(*args, **kwargs)

        self._data.category = 'port'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.get_path() == other.get_path()
        return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.get_path() != other.get_path()
        return True

    def set_name(self, text):
        if super(_PortModel, self).set_name(text) is True:
            self._item._name_aux.setPlainText(text)
            self._item._update()


class _InputPortModel(_PortModel):
    def __init__(self, *args, **kwargs):
        super(_InputPortModel, self).__init__(*args, **kwargs)
        self._gui_data.connection_path = None
        self._data.source = None

    def __str__(self):
        return 'InputPort(path={})'.format(
            self.get_path()
        )

    def __repr__(self):
        return '\n'+self.__str__()

    def _register_connection(self, path):
        self._gui_data.connection_path = path
        source_path, target_path = _ConnectionModel._to_args(path)
        self._data.source = source_path

    def _unregister_connection(self, path):
        self._gui_data.connection_path = None
        self._data.source = None

    def has_source(self):
        return bool(self._data.source)

    def get_source(self):
        if self._data.source:
            node_path, port_path = bsc_core.BscAttributePath.split_by(self._data.source)
            return self.scene_model.get_node(node_path).get_output_port(port_path)

    def get_connection_path_set(self):
        if self._gui_data.connection_path:
            return {self._gui_data.connection_path}
        return set()

    def get_connections_itr(self):
        if self._gui_data.connection_path:
            connection = self.scene_model.get_connection(self._gui_data.connection_path)
            if connection:
                yield connection

    def get_connections(self):
        return list(self.get_connections_itr())

    def connect(self, source_port):
        if not isinstance(source_port, _OutputPortModel):
            raise RuntimeError()

        self.scene_model._connect_ports(source_port, self)


class _OutputPortModel(_PortModel):
    def __init__(self, *args, **kwargs):
        super(_OutputPortModel, self).__init__(*args, **kwargs)
        self._gui_data.connection_path_set = set()

    def __str__(self):
        return 'OutputPort(path={})'.format(
            self.get_path()
        )

    def __repr__(self):
        return '\n'+self.__str__()

    def _register_connection(self, path):
        if path not in self._gui_data.connection_path_set:
            self._gui_data.connection_path_set.add(path)

    def _unregister_connection(self, path):
        if path in self._gui_data.connection_path_set:
            self._gui_data.connection_path_set.remove(path)

    def has_targets(self):
        return bool(self._gui_data.connection_path_set)

    def get_target_itr(self):
        for i in self._gui_data.connection_path_set:
            yield _ConnectionModel._get_target(self.scene_model, i)

    def get_targets(self):
        return list(self.get_target_itr())

    def get_connection_path_set(self):
        return set(self._gui_data.connection_path_set)

    def get_connections_itr(self):
        for i in set(self._gui_data.connection_path_set):
            i_connection = self.scene_model.get_connection(i)
            if i_connection:
                yield i_connection

    def get_connections(self):
        return list(self.get_connections_itr())

    def connect(self, target_port):
        if not isinstance(target_port, _InputPortModel):
            raise RuntimeError()

        self.scene_model._connect_ports(self, target_port)


class _AbsAction(object):
    ActionFlags = _base._ActionFlags

    @property
    def gui_data(self):
        raise NotImplementedError()

    def _init_action(self):
        self.gui_data.action = _base._Dict(
            flag=None,
            sub_flag=None,
        )

    def set_action_flag(self, flag):
        self.gui_data.action.flag = flag

    def set_action_sub_flag(self, flag):
        self.gui_data.action.sub_flag = flag

    def is_action_flag_matching(self, *args):
        return self.gui_data.action.flag in args

    def is_action_sub_flag_matching(self, *args):
        return self.gui_data.action.sub_flag in args

    def clear_action_flag(self):
        self.gui_data.action.flag = None

    def clear_action_sub_flag(self):
        self.gui_data.action.sub_flag = None


class _AbsNodeModel(
    _base._SbjBase,
    _AbsAction
):

    # hover
    def _update_hover(self, flag):
        if flag != self._data.hover.flag:
            self._data.hover.flag = flag

    # select
    def _update_select(self, flag):
        if flag != self._gui_data.select.flag:
            self._gui_data.select.flag = flag

    def __init__(self, *args, **kwargs):
        super(_AbsNodeModel, self).__init__(*args, **kwargs)

        self._data.options = _base._Dict(
            position=_base._Dict(
                x=0.0, y=0.0
            ),
            size=_base._Dict(
                width=160, height=24
            ),
            color_enable=False,
            color=_base._Dict(
                r=95, g=95, b=95
            )
        )

        self._init_action()

        # refresh
        self._gui_data.force_refresh_flag = True
        #
        self._gui_data.cut_flag = False
        # main
        self._gui_data.rect = qt_rect()

        # basic
        self._gui_data.basic = _base._Dict(
            rect=qt_rect(),
            size=QtCore.QSize(),
        )

        # color
        self._gui_data.color = _base._Dict(
            rect=qt_rect(),
            border=_base._QtColors.NodeBorder,
            background=_base._QtColors.NodeBackground,
            alpha=255,
        )

        # head
        self._gui_data.head = _base._Dict(
            rect=QtCore.QRectF(),
            size=QtCore.QSize(),
        )

        # edit
        self._gui_data.edited = _base._Dict(
            rect=QtCore.QRectF(),
            value=False,
            value_rect=QtCore.QRectF(),
        )

        # viewed
        self._gui_data.viewed = _base._Dict(
            rect=QtCore.QRectF(),
            value=False,
            value_rect=QtCore.QRectF(),
        )

        # text option for draw
        self._gui_data.text = _base._Dict(
            font=gui_qt_core.QtFont.generate(size=10),
            color=_base._QtColors.Text,
            action_color=_base._QtColors.TextHover,
            # all text height
            height=24
        )

        # type
        self._gui_data.type = _base._Dict(
            rect=qt_rect(),
            font=gui_qt_core.QtFont.generate(size=12, weight=75),
            color=_base._QtColors.TypeText,
        )

        self._gui_data.name = _base._Dict(
            rect=qt_rect(),
            font=gui_qt_core.QtFont.generate(size=12, weight=75),
            color=_base._QtColors.TypeText,
        )

        # hover
        self._gui_data.hover = _base._Dict(
            enable=True,
            flag=False,
            rect=qt_rect(),
            color=QtGui.QColor(*gui_core.GuiRgba.LightOrange),
        )

        # select
        self._gui_data.select = _base._Dict(
            enable=True,
            flag=False,
            rect=qt_rect(),
            color=QtGui.QColor(*gui_core.GuiRgba.LightAzureBlue),
        )

        # menu
        self._gui_data.menu = _base._Dict(
            content=None,
            content_generate_fnc=None,
            data=None,
            data_generate_fnc=None,
            name_dict=dict()
        )

    def set_options(self, options):
        position = options['position']
        self.set_position((position['x'], position['y']))

        size = options['size']
        self.set_size((size['width'], size['height']))

        color_enable = options['color_enable']
        if color_enable is True:
            color = options['color']
            self.set_color((color['r'], color['g'], color['b']))

    def set_position(self, position):
        x, y = position
        self._data.options.position.x = x
        self._data.options.position.y = y
        self._item.setPos(*position)

    def get_position(self):
        return self._item.x(), self._item.y()

    def _update_position(self):
        self._data.options.position.x = self._item.x()
        self._data.options.position.y = self._item.y()

    def set_size(self, size):
        w, h = size
        self._data.options.size.width = w
        self._data.options.size.height = h
        self._item.setRect(0, 0, w, h)
        self._update_attaches()

    def _update_size(self):
        self._data.options.size.width = self._item.rect().width()
        self._data.options.size.height = self._item.rect().height()

    def get_size(self):
        return self._item.rect().width(), self._item.rect().height()

    def set_selected(self, boolean):
        self._item.setSelected(boolean)

    # color
    def set_color_enable(self, boolean):
        self._data.options.color_enable = boolean

    def set_color(self, args):
        self.set_color_enable(True)
        self._data.options.color.r = args[0]
        self._data.options.color.g = args[1]
        self._data.options.color.b = args[2]

        self._gui_data.color.background = QtGui.QColor(
            self._data.options.color.r,
            self._data.options.color.g,
            self._data.options.color.b,
            self._gui_data.color.alpha
        )

    def set_basic_size(self, size):
        self._gui_data.basic.size = size
        self.set_size((size.width(), size.height()))

    def _update_attaches(self):
        pass

    def set_basic_head_size(self, size):
        self._gui_data.head.size = size

    def set_cut_flag(self, flag):
        self._data.cut_flag = flag
        if flag is True:
            self._item.hide()
        else:
            self._item.show()

    def move_by(self, x, y):
        self._item.moveBy(x, y)

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
        self._update_position()
        self._update_size()
        return _base._ToJson(self._data._dict).generate()

    def to_data(self):
        return _SceneModel._json_str_to_data(self.to_json())


# node model
class _NodeModel(_AbsNodeModel):

    @classmethod
    def find_next_port_path(cls, paths, name, parent_path=None):
        if parent_path is None:
            port_path = name
        else:
            port_path = '{}.{}'.format(parent_path, name)

        if port_path not in paths:
            return port_path
        else:
            count = 1
            new_path = port_path
            while new_path in paths:
                if parent_path is None:
                    new_path = '{}{}'.format(name, count)
                else:
                    new_path = '{}.{}'.format(parent_path, name)

                count += 1

            if new_path not in paths:
                return new_path

    def __init__(self, *args, **kwargs):
        super(_NodeModel, self).__init__(*args, **kwargs)
        self._data.category = 'node'
        self._data.options.bypass = False
        # basic
        self._gui_data.color.border=_base._QtColors.NodeBorder
        self._gui_data.color.background = _base._QtColors.NodeBackground
        # port
        self._gui_data.port = _base._Dict(
            input=_base._Dict(
                cls=None
            ),
            output=_base._Dict(
                cls=None
            ),
            size=QtCore.QSize(16, 8),
            spacing=4
        )
        # input port
        self._data.input_ports = collections.OrderedDict()
        # output port
        self._data.output_ports = collections.OrderedDict()

        self.set_menu_data(
            [
                [
                    'Node', 'file/folder',
                    [
                        ('Add Input Port', 'file/file', self._add_input_port_action)
                    ]
                ]
            ]
        )

    def _add_input_port_action(self):
        self.add_input_port('input')

    def add_input_port(self, type_name, name=None, parent_path=None, *args, **kwargs):
        if name is None:
            port_path = self.find_next_port_path(self._data.input_ports, type_name, parent_path)
        else:
            if parent_path is None:
                port_path = name
            else:
                port_path = '{}.{}'.format(parent_path, name)

        if port_path in self._data.input_ports:
            return False, self._data.input_ports[port_path]

        prt_size = self._gui_data.port.size
        prt_w, prt_h = prt_size.width(), prt_size.height()

        port = self._gui_data.port.input.cls(self._item, prt_w, prt_h)
        atr_path = bsc_core.BscAttributePath.join_by(self.get_path(), port_path)

        model = port._model
        self._data.input_ports[port_path] = model
        self._update_input_ports()
        port._update()

        model.set_type(type_name)
        model.set_path(atr_path)
        model.set_name(port_path)

        return True, model

    def _add_input_port_by_data(self, data):
        type_name = data['type']
        name = data['name']
        flag, node = self.add_input_port(type_name, name)
        return node

    def get_input_ports(self):
        return list(self._data.input_ports.values())

    def get_input_port(self, name):
        return self._data.input_ports.get(name)

    def _update_input_ports(self):
        rect = self._item.boundingRect()
        x, y = 0, 0
        w, h = rect.width(), rect.height()

        spc = self._gui_data.port.spacing

        ports = self.get_input_ports()
        prt_c = len(ports)
        if not prt_c:
            return

        prt_size = self._gui_data.port.size
        prt_w, prt_h = prt_size.width(), prt_size.height()
        prt_ws = prt_c*prt_w+spc*(prt_c-1)
        prt_x, prt_y = x+(w-prt_ws)/2, y-prt_h-1

        x_c = prt_x
        for i in ports:
            i._item.setPos(x_c, prt_y)
            x_c += prt_w+spc

    def add_output_port(self, type_name, name=None, parent_path=None, *args, **kwargs):
        if name is None:
            port_path = self.find_next_port_path(self._data.input_ports, type_name, parent_path)
        else:
            if parent_path is None:
                port_path = name
            else:
                port_path = '{}.{}'.format(parent_path, name)

        if port_path in self._data.output_ports:
            return False, self._data.output_ports[port_path]

        prt_size = self._gui_data.port.size
        prt_w, prt_h = prt_size.width(), prt_size.height()

        port = self._gui_data.port.output.cls(self._item, prt_w, prt_h)
        atr_path = bsc_core.BscAttributePath.join_by(self.get_path(), port_path)

        model = port._model
        self._data.output_ports[port_path] = model
        self._update_output_ports()
        port._update()

        model.set_type(type_name)
        model.set_path(atr_path)
        model.set_name(port_path)

        return True, model

    def _add_output_port_by_data(self, data):
        type_name = data['type']
        name = data['name']
        flag, node = self.add_output_port(type_name, name)
        return node

    def get_output_ports(self):
        return list(self._data.output_ports.values())

    def get_output_port(self, name):
        return self._data.output_ports.get(name)

    # connection, source
    def has_source_connections(self):
        for i in self.get_input_ports():
            if i.has_source():
                return True
        return False

    def get_source_connection_path_set(self):
        set_ = set()
        for i in self.get_input_ports():
            set_.update(i.get_connection_path_set())
        return set_

    def get_source_connections_itr(self):
        for i in self.get_input_ports():
            for j in i.get_connections_itr():
                yield j

    # target
    def has_target_connections(self):
        for i in self.get_output_ports():
            if i.has_targets():
                return True
        return False

    def get_target_connection_path_set(self):
        set_ = set()
        for i in self.get_output_ports():
            set_.update(i.get_connection_path_set())
        return set_

    def get_target_connections_itr(self):
        for i in self.get_output_ports():
            for j in i.get_connections_itr():
                yield j

    def get_connection_path_set(self):
        set_ = set()
        set_.update(self.get_source_connection_path_set())
        set_.update(self.get_target_connection_path_set())
        return set_

    def _update_output_ports(self):
        rect = self._item.boundingRect()
        x, y = 0, 0
        w, h = rect.width(), rect.height()

        spc = self._gui_data.port.spacing

        ports = self.get_output_ports()
        prt_c = len(ports)
        if not prt_c:
            return

        prt_size = self._gui_data.port.size
        prt_w, prt_h = prt_size.width(), prt_size.height()
        prt_ws = prt_c*prt_w+spc*(prt_c-1)
        prt_x, prt_y = x+(w-prt_ws)/2, y+h+2

        x_c = prt_x
        for i in ports:
            i._item.setPos(x_c, prt_y)
            x_c += prt_w+spc

    def update(self, rect):
        # check rect is change
        if rect != self._gui_data.rect or self._gui_data.force_refresh_flag is True:
            self._gui_data.rect = qt_rect(rect)

            x, y, w, h = rect.x()+1, rect.y()+1, rect.width()-2, rect.height()-2

            mrg = 2

            spc = 2

            self._gui_data.basic.rect.setRect(
                x, y, w, h
            )

            hed_size = self._gui_data.head.size
            hed_w, hed_h = hed_size.width(), hed_size.height()

            frm_w, frm_h = 16, 16

            self._gui_data.viewed.rect.setRect(
                x+(hed_h-frm_w)/2, y+(hed_h-frm_h)/2, frm_w, frm_h
            )
            self._gui_data.edited.rect.setRect(
                x+(w-hed_h)+(hed_h-frm_w)/2, y+(hed_h-frm_h)/2, frm_w, frm_h
            )

            frm_vlu_w, frm_vlu_h = 14, 14
            self._gui_data.viewed.value_rect.setRect(
                x+(hed_h-frm_vlu_w)/2, y+(hed_h-frm_vlu_h)/2, frm_vlu_w, frm_vlu_h
            )
            self._gui_data.edited.value_rect.setRect(
                x+(w-hed_h)+(hed_h-frm_vlu_w)/2, y+(hed_h-frm_vlu_h)/2, frm_vlu_w, frm_vlu_h
            )

            self._gui_data.type.rect.setRect(
                x+hed_h, y, w-hed_h*2, hed_h
            )

            return True
        return False

    def draw(self, painter, option):
        painter.save()

        self.update(option.rect)

        self._update_select(bool(option.state & QtWidgets.QStyle.State_Selected))

        self.draw_base(painter, option)

        painter.restore()

    def draw_base(self, painter, option):
        if self._gui_data.select.flag is True:
            border_color = self._gui_data.select.color
            border_width = 2
        elif self._gui_data.hover.flag is True:
            border_color = self._gui_data.hover.color
            border_width = 2
        else:
            border_color = self._gui_data.color.border
            border_width = 1

        if self.is_bypass():
            background_color = _base._QtColors.NodeBackgroundBypass
        else:
            background_color = self._gui_data.color.background

        gui_qt_core.QtItemDrawBase._draw_frame(
            painter,
            rect=self._gui_data.basic.rect,
            border_color=border_color,
            background_color=background_color,
            border_width=border_width,
            border_radius=2
        )

        # draw type
        gui_qt_core.QtItemDrawBase._draw_name_text(
            painter, self._gui_data.type.rect, self._data.type,
            self._gui_data.type.color, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            font=self._gui_data.type.font
        )

        # draw viewed
        gui_qt_core.QtItemDrawBase._draw_frame(
            painter,
            rect=self._gui_data.viewed.rect,
            border_color=border_color,
            background_color=QtGui.QColor(47, 47, 47, 255),
            border_width=1,
            border_radius=2
        )
        if self._gui_data.viewed.value is True:
            gui_qt_core.QtItemDrawBase._draw_frame(
                painter,
                rect=self._gui_data.viewed.value_rect,
                border_color=QtGui.QColor(47, 47, 47, 255),
                background_color=QtGui.QColor(*gui_core.GuiRgba.Purple),
                border_width=1,
                border_radius=2
            )

        # draw edited
        gui_qt_core.QtItemDrawBase._draw_frame(
            painter,
            rect=self._gui_data.edited.rect,
            border_color=border_color,
            background_color=QtGui.QColor(47, 47, 47, 255),
            border_width=1,
            border_radius=2
        )
        if self._gui_data.edited.value is True:
            gui_qt_core.QtItemDrawBase._draw_frame(
                painter,
                rect=self._gui_data.edited.value_rect,
                border_color=QtGui.QColor(47, 47, 47, 255),
                background_color=QtGui.QColor(*gui_core.GuiRgba.NeonGreen),
                border_width=1,
                border_radius=2
            )

    # name
    def set_name(self, text):
        if super(_NodeModel, self).set_name(text) is True:
            self._item._name_aux.setPlainText(text)

    # hover
    def _update_hover(self, flag):
        if flag != self._gui_data.hover.flag:
            self._gui_data.hover.flag = flag

    # select
    def _update_select(self, flag):
        if flag != self._gui_data.select.flag:
            self._gui_data.select.flag = flag

    def _update_attaches(self):
        self._update_name()
        self._update_bypass()
        self._update_input_ports()
        self._update_output_ports()

    def _update_name(self):
        rect = self._item.boundingRect()
        x, y = 0, 0
        w, h = rect.width(), rect.height()
        self._item._name_aux.setPos(x+w, y)

    # bypass
    def _update_bypass(self):
        rect = self._item.boundingRect()
        x, y = 0, 0
        w, h = rect.width(), rect.height()

        w_0, h_0 = 96, 96

        self._item._bypass_aux.setRect(
            x+(w-w_0)/2, y+(h-h_0)/2, w_0, h_0
        )

    def set_bypass(self, boolean):
        self._data.options.bypass = boolean
        self._item._bypass_aux.setVisible(boolean)
        self.scene_model._graph.update()

    def is_bypass(self):
        return self._data.options.bypass

    def _on_swap_bypass(self):
        self.set_bypass(not self.is_bypass())

    # viewed
    def set_viewed(self, boolean):
        if boolean is True:
            self._gui_data.viewed.value = boolean
            self.scene_model._clear_viewed_node()
            self.scene_model._register_viewed_node(self)
        else:
            if self.scene_model.has_viewed_nodes():
                if self.scene_model._check_node_viewed(self) is False:
                    self._gui_data.viewed.value = boolean

        self.scene_model._graph.update()

    def _update_viewed(self, boolean):
        self._gui_data.viewed.value = boolean
        self.scene_model._graph.update()

    def is_viewed(self):
        return self._gui_data.viewed.value

    def _on_swap_viewed(self):
        self.set_viewed(not self.is_viewed())
        
    def _check_viewed(self, point):
        if self._gui_data.viewed.rect.contains(point):
            return True
        return False

    # edited
    def set_edited(self, boolean):
        if boolean is True:
            self._gui_data.edited.value = boolean
            self.scene_model._clear_edited_node()
            self.scene_model._register_edited_node(self)
        else:
            if self.scene_model.has_edited_nodes():
                if self.scene_model._check_node_edited(self) is False:
                    self._gui_data.edited.value = boolean

    def _update_edited(self, boolean):
        self._gui_data.edited.value = boolean
        self.scene_model._graph.update()

    def is_edited(self):
        return self._gui_data.edited.value

    def _on_swap_edited(self):
        self.set_edited(not self.is_edited())

    def _check_edited(self, point):
        if self._gui_data.edited.rect.contains(point):
            return True
        return False

    def do_delete(self):
        for i in self.get_source_connections_itr():
            i.do_delete()

        for i in self.get_target_connections_itr():
            i.do_delete()

        self.scene_model._unregister_node(self)


class _BackdropModel(_AbsNodeModel):
    def __init__(self, *args, **kwargs):
        super(_BackdropModel, self).__init__(*args, **kwargs)
        self._data.category = 'backdrop'
        # basic
        self._gui_data.color.border = _base._QtColors.BackdropBorder
        self._gui_data.color.background = _base._QtColors.BackdropBackground
        self._gui_data.color.alpha = 31

        self._gui_data.name.color = _base._QtColors.BackdropName

        self._gui_data.move = _base._Dict(
            start_position=QtCore.QPointF(),
            start_point=QtCore.QPointF(),
            node_position_data=[],
            node_set=set(),
        )

        self._gui_data.resize = _base._Dict(
            start_point=QtCore.QPointF(),
            start_rect=QtCore.QRect(),
            rect=QtCore.QRectF(),
            icon_rect=QtCore.QRectF(),
            icon=_base._Dict(
                file=gui_core.GuiIcon.get('resize'),
            )
        )

        self._gui_data.description = _base._Dict(
            rect=QtCore.QRect(),
            text_rect=QtCore.QRect(),
            text='',
            color=QtGui.QColor(223, 223, 223, 255),
            font=gui_qt_core.QtFont.generate(size=12)
        )

        self.set_menu_data(
            [
                [
                    'Backdrop', 'file/folder',
                    [
                        ('Set Description', 'file/file', self._add_description_action)
                    ]
                ]
            ]
        )

    def _add_description_action(self):
        pass

    def set_description(self, text):
        self._gui_data.description.text = text

    def update(self, rect):
        # check rect is change
        if rect != self._gui_data.rect or self._gui_data.force_refresh_flag is True:
            self._gui_data.rect = qt_rect(rect)

            x, y, w, h = rect.x()+1, rect.y()+1, rect.width()-2, rect.height()-2

            self._gui_data.basic.rect.setRect(
                x, y, w, h
            )

            hed_size = self._gui_data.head.size
            hed_w, hed_h = hed_size.width(), hed_size.height()

            self._gui_data.head.rect.setRect(
                x, y, w, hed_h
            )

            mrg = 4

            self._gui_data.description.rect.setRect(
                x+mrg, y+hed_h+mrg, w-mrg*2, h-hed_h-mrg*2
            )
            self._gui_data.description.text_rect.setRect(
                x+mrg*2, y+hed_h+mrg*2, w-mrg*4, h-hed_h-mrg*4
            )

            icn_w, icn_h = 20, 20

            self._gui_data.resize.rect.setRect(
                x+w-icn_w-mrg*2, y+h-icn_h-mrg*2, icn_w+mrg*2, icn_h+mrg*2
            )
            self._gui_data.resize.icon_rect.setRect(
                x+w-icn_w-mrg*2, y+h-icn_h-mrg*2, icn_w, icn_h
            )

            self._gui_data.name.rect.setRect(
                x, y, w, hed_h
            )

            return True
        return False

    def draw(self, painter, option):
        painter.save()

        self.update(option.rect)

        self._update_select(bool(option.state & QtWidgets.QStyle.State_Selected))

        self.draw_base(painter, option)

        painter.restore()

    def draw_base(self, painter, option):
        if self._gui_data.select.flag is True:
            border_color = self._gui_data.select.color
            border_width = 2
        elif self._gui_data.hover.flag is True:
            border_color = self._gui_data.hover.color
            border_width = 2
        else:
            border_color = self._gui_data.color.border
            border_width = 1

        gui_qt_core.QtItemDrawBase._draw_frame(
            painter,
            rect=self._gui_data.basic.rect,
            border_color=border_color,
            background_color=self._gui_data.color.background,
            border_width=border_width,
            border_radius=0
        )

        # name
        gui_qt_core.QtItemDrawBase._draw_name_text(
            painter, self._gui_data.name.rect, self._data.name,
            color=self._gui_data.name.color,
            option=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            font=self._gui_data.name.font
        )

        # headline
        gui_qt_core.QtItemDrawBase._draw_line(
            painter, point_0=self._gui_data.head.rect.bottomLeft(), point_1=self._gui_data.head.rect.bottomRight(),
            border_color=border_color, border_width=border_width
        )

        # description
        gui_qt_core.QtItemDrawBase._draw_frame(
            painter,
            rect=self._gui_data.description.rect,
            border_color=border_color,
            background_color=QtGui.QColor(0, 0, 0, 0),
            border_width=1,
            border_radius=4
        )

        gui_qt_core.QtItemDrawBase._draw_description_text(
            painter,
            rect=self._gui_data.description.text_rect,
            text=self._gui_data.description.text,
            color=self._gui_data.description.color,
            font=self._gui_data.description.font
        )

        # resize
        gui_qt_core.QtItemDrawBase._draw_icon_by_file(
            painter,
            rect=self._gui_data.resize.icon_rect,
            file_path=self._gui_data.resize.icon.file
        )

    def _check_move(self, point):
        if self._gui_data.head.rect.contains(point):
            return True
        return False

    def _check_scene_move(self, point):
        return self._check_move(point-self._item.pos())

    def do_move_start(self, event):
        self._gui_data.move.start_point = event.pos()
        self._gui_data.move.start_position = self.get_position()
        x, y = self._item.x(), self._item.y()
        rect = self._item.boundingRect()
        w, h = rect.width(), rect.height()

        node_position_data = []

        self.scene_model.clear_selection()

        self._item.setSelected(True)
        all_items = self.scene._get_items_by_rect(x, y, w, h)
        for i in all_items:
            if i.SBJ_TYPE == _base._QtSbjTypes.Node:
                i_node = i._model
                node_position_data.append(
                    (i_node, i_node.get_position())
                )
                # i.setSelected(True)

        self._gui_data.move.node_position_data = node_position_data

    def do_move(self, event):
        delta = event.pos()-self._gui_data.move.start_point
        x, y = delta.x(), delta.y()

        self._item.moveBy(x, y)

        for i in self._gui_data.move.node_position_data:
            i[0]._item.moveBy(x, y)

    def _push_move_cmd(self):
        data = [
            (
                _QtUndoCommand.Actions.NodeMove,
                (self.get_path(), self._gui_data.move.start_position, self.get_position())
            )
        ]
        for i in self._gui_data.move.node_position_data:
            i_node = i[0]
            data.append(
                (
                    _QtUndoCommand.Actions.NodeMove,
                    (i_node.get_path(), i[1], i_node.get_position())
                )
            )
        self.scene_model._graph._undo_stack.push(_QtUndoCommand(self.scene_model, data))

    def do_move_end(self):
        self._push_move_cmd()
    
    def _check_scene_resize(self, point):
        return self._check_resize(point-self._item.pos())

    def _check_resize(self, point):
        if self._gui_data.resize.rect.contains(point):
            return True
        return False

    def do_resize_start(self, event):
        self._gui_data.resize.start_point = event.pos()
        self._gui_data.resize.start_rect = self._item.rect()

    def do_resize_move(self, event):
        delta = event.pos()-self._gui_data.resize.start_point
        rect = self._gui_data.resize.start_rect
        w, h = rect.width()+delta.x(), rect.height()+delta.y()
        w, h = max(min(w, 1024), 128), max(min(h, 1024), 64)
        self.set_size((w, h))

    def _push_resize_cmd(self):
        rect = self._gui_data.resize.start_rect
        data = [
            (_QtUndoCommand.Actions.NodeResize, (self.get_path(), (rect.width(), rect.height()), self.get_size()))
        ]
        self.scene_model._graph._undo_stack.push(_QtUndoCommand(self.scene_model, data))

    def do_resize_end(self):
        self._push_resize_cmd()


class _NodeDataGrop(object):
    def __init__(self, scene_model, data):
        self._scene_model = scene_model
        self._data = data

    def generate_create_data(self):
        node_args = []
        connection_args = []

        if self._data:
            xs = []
            ys = []
            for i in self._data:
                xs.append(i['options']['position']['x'])
                ys.append(i['options']['position']['y'])

            x_min = min(xs)
            y_min = min(ys)

            point = QtGui.QCursor().pos()
            p = self._scene_model._graph._map_from_global(point)
            p_x, p_y = p.x(), p.y()

            path_set = self._scene_model.get_node_path_set()
            for i in self._data:
                i_x = i['options']['position']['x']
                i_y = i['options']['position']['y']
                i['options']['position']['x'] = p_x+(i_x-x_min)
                i['options']['position']['y'] = p_y+(i_y-y_min)

                i_name = i['name']
                i_new_path = _SceneModel._find_next_node_path(
                    path_set, i_name
                )
                path_set.add(i_new_path)
                i_new_name = bsc_core.BscNodePath.to_dag_name(i_new_path)
                i['path'] = i_new_path
                i['name'] = i_new_name
                node_args.append(i)

        return node_args, connection_args


# scene model
class _SceneModel(_AbsAction):
    ActionFlags = _base._ActionFlags
    
    @classmethod
    def _to_name_args(cls, name):
        match = re.match(r"([^\d]*)(\d*)$", name)
        if match:
            return match.group(1), match.group(2)
        return name, ""

    @classmethod
    def _find_next_node_path(cls, path_set, name, parent_path=None):
        parent_path = parent_path or ''
        path = u'{}/{}'.format(parent_path, name)
        if path not in path_set:
            return path
        else:
            name_str, number = cls._to_name_args(name)
            if number:
                count = int(number)
            else:
                count = 1

            new_path = path
            while new_path in path_set:
                new_path = u'{}/{}{}'.format(parent_path, name_str, count)
                count += 1

            if new_path not in path_set:
                return new_path

    @classmethod
    def _json_str_to_data(cls, json_str):
        return json.loads(json_str, object_pairs_hook=collections.OrderedDict)

    def __init__(self, widget):
        self._graph = widget

        self._data = _base._Dict()
        self._gui_data = _base._Dict()

        self._data.nodes = collections.OrderedDict()
        self._gui_data.connection_dict = collections.OrderedDict()

        self._gui_data.node = _base._Dict(
            cls=None,
            group_cls=None,
            size=QtCore.QSize(160, 24),
            head=_base._Dict(
                size=QtCore.QSize(160, 24),
            )
        )

        # backdrop
        self._gui_data.backdrop = _base._Dict(
            cls=None,
            size=QtCore.QSize(320, 240),
            head=_base._Dict(
                size=QtCore.QSize(320, 24),
            )
        )

        # connection
        self._gui_data.connection = _base._Dict(
            cls=None,
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

        self.set_menu_data(
            [
                [
                    'Graph', 'file/folder',
                    [
                        ('Add Node', 'file/file', functools.partial(self._add_node_action, 'node')),
                        ('Add Backdrop', 'file/file', functools.partial(self._add_backdrop_action, 'backdrop'))
                    ]
                ]
            ]
        )

    def _add_node_action(self, type_name):
        point = QtGui.QCursor().pos()
        p = self._graph._map_from_global(point)

        _, node = self.create_node(type_name)
        w, h = node.get_size()
        node.set_position((p.x()-w/2, p.y()-h/2))
        node.add_input_port('input')
        node.add_output_port('output')

    def _add_backdrop_action(self, type_name):
        point = QtGui.QCursor().pos()
        p = self._graph._map_from_global(point)

        _, node = self.create_backdrop(type_name)
        w, h = node.get_size()
        node.set_position((p.x()-w/2, p.y()-h/2))

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

    def _register_viewed_node(self, node):
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

    def _register_edited_node(self, node):
        self._gui_data.edited.node_path_set.add(node.get_path())

    def crate_by_data(self, data):
        pass

    def get_node_path_set(self):
        return set(self._data.nodes.keys())

    def create_node(self, type_name, name=None, parent_path=None, *args, **kwargs):
        if name is None:
            path = self._find_next_node_path(self._data.nodes, type_name, parent_path)
        else:
            path = u'{}/{}'.format(parent_path or '', name)

        if path in self._data.nodes:
            return False, self._data.nodes[path]

        path_opt = bsc_core.BscNodePathOpt(path)
        item = self._gui_data.node.cls()
        self._graph.scene().addItem(item)

        model = item._model
        model.set_type(type_name)
        model.set_path(path)
        model.set_name(kwargs.get('name', path_opt.get_name()))
        model.set_basic_size(self._gui_data.node.size)
        model.set_basic_head_size(self._gui_data.node.head.size)

        self._data.nodes[path] = model
        return True, model

    def create_node_by_data(self, data):
        category = data['category']
        if category == 'node':
            type_name = data['type']
            name = data['name']
            flag, node = self.create_node(type_name, name)
            node.set_options(data['options'])
            for k, v in data['input_ports'].items():
                node._add_input_port_by_data(v)
            for k, v in data['output_ports'].items():
                node._add_output_port_by_data(v)
            return node
        elif category == 'backdrop':
            type_name = data['type']
            name = data['name']
            flag, node = self.create_backdrop(type_name, name)
            node.set_options(data['options'])

    def _remove_node_by_data(self, data):
        node = self.get_node(data['path'])
        if node:
            self._unregister_node(node)

    def _unregister_node(self, node):
        path = node.get_path()
        self._data.nodes.pop(path)
        item = node._item
        self._graph.scene().removeItem(item)
        del item

    def get_node(self, path):
        return self._data.nodes.get(path)

    def create_backdrop(self, type_name=None, name=None, parent_path=None, *args, **kwargs):
        type_name = type_name or 'backdrop'
        if name is None:
            path = self._find_next_node_path(self._data.nodes, type_name, parent_path)
        else:
            path = u'{}/{}'.format(parent_path or '', name)

        if path in self._data.nodes:
            return False, self._data.nodes[path]

        path_opt = bsc_core.BscNodePathOpt(path)
        item = self._gui_data.backdrop.cls()
        self._graph.scene().addItem(item)

        model = item._model
        model.set_type(type_name)
        model.set_path(path)
        model.set_name(kwargs.get('name', path_opt.get_name()))
        model.set_basic_size(self._gui_data.backdrop.size)
        model.set_basic_head_size(self._gui_data.backdrop.head.size)

        self._data.nodes[path] = model
        return True, model

    def set_node_position(self, path, position):
        self.get_node(path).set_position(position)

    def set_node_size(self, path, size):
        self.get_node(path).set_size(size)

    # connection
    def create_connection(self, source_arg, target_args):
        if isinstance(source_arg, six.string_types) and isinstance(target_args, six.string_types):
            self._connect_port_paths(source_arg, target_args)
        else:
            self._connect_ports(source_arg, target_args)

    def _connect_path(self, path):
        self._connect_port_paths(*_ConnectionModel._to_args(path))

    def _connect_paths(self, paths):
        [self._connect_path(x) for x in paths]

    def _to_node_input_port(self, atr_path):
        node_path, port_path = bsc_core.BscAttributePath.split_by(atr_path)
        return self.get_node(node_path).get_input_port(port_path)

    def _to_node_output_port(self, atr_path):
        node_path, port_path = bsc_core.BscAttributePath.split_by(atr_path)
        return self.get_node(node_path).get_output_port(port_path)

    def _connect_port_paths(self, source_path, target_path):
        source_path_opt = bsc_core.BscAttributePathOpt(source_path)
        source_node_path = source_path_opt.obj_path
        source_node = self.get_node(source_node_path)
        if not source_node:
            return False, None
        source_port_path = source_path_opt.port_path
        source_port = source_node.get_output_port(source_port_path)
        if not source_port:
            return False, None
        target_path_opt = bsc_core.BscAttributePathOpt(target_path)
        target_node_path = target_path_opt.obj_path
        target_node = self.get_node(target_node_path)
        if not target_node:
            return False, None
        target_port_path = target_path_opt.port_path
        target_port = target_node.get_input_port(target_port_path)
        if not target_port:
            return False, None

        if source_node_path == target_node_path:
            return False, None

        return self._connect_ports(source_port, target_port)

    def _connect_ports(self, source_port, target_port):
        path = _ConnectionModel._to_path(source_port.get_path(), target_port.get_path())
        if path in self._gui_data.connection_dict:
            return False, self._gui_data.connection_dict[path]

        if target_port.has_source():
            # when target port has source, break connection first
            source_port_old = target_port.get_source()
            if self._disconnect_ports(source_port_old, target_port) is False:
                return False, None

        item = self._gui_data.connection.cls(source_port, target_port)
        item._set_hover_enable(True)
        model = item._model
        model.set_path(path)
        model.update_v()

        source_port._register_connection(path)
        target_port._register_connection(path)
        self._graph.scene().addItem(item)

        self._gui_data.connection_dict[path] = model
        return True, model

    def _push_connect_cmd(self, source_port, target_port):
        path = _ConnectionModel._to_path(source_port.get_path(), target_port.get_path())
        if self.has_connection(path) is True:
            return

        data = [
            (_QtUndoCommand.Actions.Connect, _ConnectionModel._to_path(source_port.get_path(), target_port.get_path()))
        ]
        self._graph._undo_stack.push(_QtUndoCommand(self, data))

    # disconnect
    def _disconnect_path(self, path):
        self._disconnect_port_paths(*_ConnectionModel._to_args(path))

    def _disconnect_paths(self, paths):
        [self._disconnect_path(x) for x in paths]

    def _disconnect_port_paths(self, source_path, target_path):
        self._disconnect_ports(
            self._to_node_output_port(source_path), self._to_node_input_port(target_path)
        )

    def _disconnect_ports(self, source_port, target_port):
        path = _ConnectionModel._to_path(source_port.get_path(), target_port.get_path())
        if path in self._gui_data.connection_dict:
            connection = self._gui_data.connection_dict[path]
            self._gui_data.connection_dict.pop(path)
            source_port._unregister_connection(path)
            target_port._unregister_connection(path)
            self._graph.scene().removeItem(connection._item)
            return True
        return False

    def _push_disconnect_cmd(self, source_port, target_port):
        data = [
            (_QtUndoCommand.Actions.Disconnect, _ConnectionModel._to_path(source_port.get_path(), target_port.get_path()))
        ]
        self._graph._undo_stack.push(_QtUndoCommand(self, data))

    def _reconnect_path(self, path_0, path_1):
        self._disconnect_path(path_0)
        self._connect_path(path_1)

    def _reconnect_source(self, source_port, target_port, source_port_new):
        path = _ConnectionModel._to_path(source_port.get_path(), target_port.get_path())
        self.remove_connection_path(path)
        self._connect_ports(source_port_new, target_port)

    def _push_reconnect_source_cmd(self, source_port, target_port, source_port_new):
        path_0 = _ConnectionModel._to_path(source_port.get_path(), target_port.get_path())
        path_1 = _ConnectionModel._to_path(source_port_new.get_path(), target_port.get_path())
        data = [
            (_QtUndoCommand.Actions.Reconnect, (path_0, path_1))
        ]
        self._graph._undo_stack.push(_QtUndoCommand(self, data))

    def _reconnect_target(self, source_port, target_port, target_port_new):
        path = _ConnectionModel._to_path(source_port.get_path(), target_port.get_path())
        self.remove_connection_path(path)
        self._connect_ports(source_port, target_port_new)

    def _push_reconnect_target_cmd(self, source_port, target_port, target_port_new):
        path_0 = _ConnectionModel._to_path(source_port.get_path(), target_port.get_path())
        path_1 = _ConnectionModel._to_path(source_port.get_path(), target_port_new.get_path())
        data = [
            (_QtUndoCommand.Actions.Reconnect, (path_0, path_1))
        ]
        self._graph._undo_stack.push(_QtUndoCommand(self, data))

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
        self._graph.scene().removeItem(connection._item)

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

        mouse_scene_pos = self._graph.mapToScene(event.pos())

        self._graph.scale(factor, factor)

        new_mouse_scene_pos = self._graph.mapToScene(event.pos())
        delta = new_mouse_scene_pos-mouse_scene_pos

        self._graph.translate(delta.x(), delta.y())

    # track
    def _do_track_start(self, event):
        self._gui_data.track.start_point = event.pos()
        self._graph.setCursor(QtCore.Qt.ClosedHandCursor)

    def _do_track_move(self, event):
        delta = event.pos()-self._gui_data.track.start_point
        self._gui_data.track.start_point = event.pos()
        scale_factor = self._graph.transform().m11()

        self._graph.translate(delta.x()/scale_factor, delta.y()/scale_factor)

    def _do_tack_end(self):
        self._graph.unsetCursor()

    # node move
    def _do_node_move_start(self, event):
        node_position_data = []

        items = self._graph.scene().selectedItems()
        for i in items:
            if i.SBJ_TYPE in {_base._QtSbjTypes.Node}:
                i_node = i._model
                node_position_data.append(
                    (i_node, i_node.get_position())
                )

        self._gui_data.node_move.node_position_data = node_position_data

    def _do_node_move(self, event):
        pass

    def _push_node_move_cmd(self):
        data = []
        for i in self._gui_data.node_move.node_position_data:
            i_node = i[0]
            data.append(
                (
                    _QtUndoCommand.Actions.NodeMove,
                    (i_node.get_path(), i[1], i_node.get_position())
                )
            )

        self._graph._undo_stack.push(_QtUndoCommand(self, data))

    def _do_node_move_end(self):
        self._push_node_move_cmd()

    # rect selection
    def _do_rect_selection_start(self, event):
        p = event.pos()
        self._gui_data.rect_selection.origin = p
        self._graph._rubber_band.setGeometry(QtCore.QRect(p, p))
        self._graph._rubber_band.show()

    def _do_rect_selection_move(self, event):
        p_0 = self._gui_data.rect_selection.origin
        rect = QtCore.QRect(p_0, event.pos()).normalized()
        self._graph._rubber_band.setGeometry(rect)

    def _do_rect_selection_end(self, event):
        self._graph._rubber_band.hide()

        rect = self._graph._rubber_band.geometry()
        scene_rect = self._graph.mapToScene(rect).boundingRect()

        selected_items = self._graph.scene().items(scene_rect, QtCore.Qt.IntersectsItemShape)

        if event.modifiers() == QtCore.Qt.ShiftModifier:
            for i_item in selected_items:
                if i_item.SBJ_TYPE in {_base._QtSbjTypes.Node}:
                    i_item.setSelected(True)
        elif event.modifiers() == QtCore.Qt.ControlModifier:
            for i_item in selected_items:
                if i_item.SBJ_TYPE in {_base._QtSbjTypes.Node}:
                    i_item.setSelected(False)
        else:
            self._graph.scene().clearSelection()
            for i_item in selected_items:
                if i_item.SBJ_TYPE in {_base._QtSbjTypes.Node}:
                    i_item.setSelected(True)

    def _push_delete_cmd(self, node_args, connection_args):
        data = [
            (_QtUndoCommand.Actions.Delete, (node_args, connection_args))
        ]
        self._graph._undo_stack.push(_QtUndoCommand(self, data))

    def _push_cut_cmd(self, node_args, connection_args):
        data = [
            (_QtUndoCommand.Actions.Cut, (node_args, connection_args))
        ]
        self._graph._undo_stack.push(_QtUndoCommand(self, data))

    def _push_paste_cmd(self, node_args, connection_args):
        data = [
            (_QtUndoCommand.Actions.Paste, (node_args, connection_args))
        ]
        self._graph._undo_stack.push(_QtUndoCommand(self, data))

    def _do_paste(self, node_args):
        nodes_data = _NodeDataGrop(self, node_args)
        node_args, connection_args = nodes_data.generate_create_data()

        self._push_paste_cmd(node_args, connection_args)

    # actions
    def _on_delete_action(self):
        node_args = []
        connection_args = []
        items = self._graph.scene().selectedItems()
        for i in items:
            if i.SBJ_TYPE in {_base._QtSbjTypes.Node}:
                i_node = i._model
                i_connection_path_set = i_node.get_connection_path_set()
                connection_args.extend(list(i_connection_path_set))
                node_args.append(i_node.to_data())
            elif i.SBJ_TYPE in {_base._QtSbjTypes.Backdrop}:
                node_args.append(i._model.to_data())
            elif i.SBJ_TYPE in {_base._QtSbjTypes.Connection}:
                connection_args.append(i._model.get_path())

        if node_args or connection_args:
            self._push_delete_cmd(node_args, connection_args)

    def _on_copy_action(self):
        node_args = []
        items = self._graph.scene().selectedItems()
        for i in items:
            if i.SBJ_TYPE in {_base._QtSbjTypes.Node}:
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

    def _on_cut_action(self):
        node_args = []
        connection_args = []
        items = self._graph.scene().selectedItems()
        for i in items:
            if i.SBJ_TYPE in {_base._QtSbjTypes.Node}:
                i_node = i._model
                i_connection_path_set = i_node.get_connection_path_set()
                connection_args.extend(list(i_connection_path_set))
                node_args.append(i_node.to_data())
            elif i.SBJ_TYPE in {_base._QtSbjTypes.Connection}:
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
        p = self._graph._map_from_global(point)
        selection_area = QtGui.QPainterPath()
        selection_area.addRect(QtCore.QRectF(p.x()-1, p.y()-1, 2, 2))
        items = self._graph.scene().items(selection_area, QtCore.Qt.IntersectsItemShape)
        for i in items:
            if i.SBJ_TYPE in {_base._QtSbjTypes.Node}:
                i._model._on_swap_bypass()

    def clear_selection(self):
        self._graph.scene().clearSelection()

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
        return _SceneModel._json_str_to_data(self.to_json())
