# coding:utf-8
import sys

import enum

from lxgui.qt.core.wrap import *


class QtUndoCommand(QtWidgets.QUndoCommand):
    class Actions(enum.IntEnum):
        PortConnect = 0x00
        PortDisconnect = 0x01
        PortReconnect = 0x02

        Delete = 0x10

        Copy = 0x11
        Cut = 0x12
        Paste = 0x13
        PasteCut = 0x14

        NodeMove = 0x20
        NodeResize = 0x21

        NodeAddInput = 0x22
        NodeAutoConnectInput = 0x23

    ACTION_NAME_MAP = {
        Actions.PortConnect: 'PortConnect',
        Actions.PortDisconnect: 'PortDisconnect',
        Actions.PortReconnect: 'PortReconnect',
    }

    @classmethod
    def trace(cls, text):
        return sys.stdout.write(text+'\n')

    @classmethod
    def trace_error(cls, text):
        return sys.stderr.write(text+'\n')

    def __init__(self, root_model, data):
        super(QtUndoCommand, self).__init__()
        self._root_model = root_model
        self._data = data

    def undo(self):
        for i_flag, i_args in self._data:
            if i_flag == self.Actions.PortConnect:
                self._root_model._disconnect_path(i_args)
                self.trace('{}: {}'.format(self.ACTION_NAME_MAP[i_flag], i_args))
            elif i_flag == self.Actions.PortDisconnect:
                self._root_model._connect_path(i_args)
                self.trace('{}: {}'.format(self.ACTION_NAME_MAP[i_flag], i_args))
            elif i_flag == self.Actions.PortReconnect:
                i_path_0, i_path_1 = i_args
                self._root_model._reconnect_path(i_path_1, i_path_0)
                self.trace('{}: {}'.format(self.ACTION_NAME_MAP[i_flag], i_args))
            elif i_flag == self.Actions.Delete:
                i_node_args, i_connection_args = i_args
                for j_args in i_node_args:
                    self._root_model.create_node_by_data(j_args)
                for j_args in i_connection_args:
                    self._root_model._connect_path(j_args)
            elif i_flag == self.Actions.Cut:
                i_node_args, i_connection_args = i_args
                for j_args in i_node_args:
                    self._root_model.create_node_by_data(j_args)
                for j_args in i_connection_args:
                    self._root_model._connect_path(j_args)
            elif i_flag == self.Actions.NodeMove:
                i_node_path, i_position_0, i_position_1 = i_args
                self._root_model.set_node_position(i_node_path, i_position_0)
            elif i_flag == self.Actions.NodeResize:
                i_node_path, i_size_0, i_size_1 = i_args
                self._root_model.set_node_size(i_node_path, i_size_0)
            elif i_flag == self.Actions.NodeAddInput:
                i_node_path, i_port_path_new = i_args
                self._root_model.remove_node_input(i_node_path, i_port_path_new)
            elif i_flag == self.Actions.NodeAutoConnectInput:
                i_node_path, i_port_flag, i_port_path, i_source_path = i_args
                self._root_model.node_auto_disconnect_input(i_node_path, i_port_flag, i_port_path, i_source_path)
            elif i_flag == self.Actions.Paste:
                i_node_args, i_connection_args = i_args
                for j_args in i_connection_args:
                    self._root_model._disconnect_path(j_args)
                for j_args in i_node_args:
                    self._root_model._remove_node_by_data(j_args)

    def redo(self):
        for i_flag, i_args in self._data:
            if i_flag == self.Actions.PortConnect:
                self._root_model._connect_path(i_args)
                self.trace('{}: {}'.format(self.ACTION_NAME_MAP[i_flag], i_args))
            elif i_flag == self.Actions.PortDisconnect:
                self._root_model._disconnect_path(i_args)
                self.trace('{}: {}'.format(self.ACTION_NAME_MAP[i_flag], i_args))
            elif i_flag == self.Actions.PortReconnect:
                i_path_0, i_path_1 = i_args
                self._root_model._reconnect_path(i_path_0, i_path_1)
                self.trace('{}: {}'.format(self.ACTION_NAME_MAP[i_flag], i_args))
            elif i_flag == self.Actions.Delete:
                i_node_args, i_connection_args = i_args
                for j_args in i_connection_args:
                    self._root_model._disconnect_path(j_args)
                for j_args in i_node_args:
                    self._root_model._remove_node_by_data(j_args)
            elif i_flag == self.Actions.Cut:
                i_node_args, i_connection_args = i_args
                for j_args in i_connection_args:
                    self._root_model._disconnect_path(j_args)
                for j_args in i_node_args:
                    self._root_model._remove_node_by_data(j_args)
            elif i_flag == self.Actions.NodeMove:
                i_node_path, i_position_0, i_position_1 = i_args
                self._root_model.set_node_position(i_node_path, i_position_1)
            elif i_flag == self.Actions.NodeResize:
                i_node_path, i_size_0, i_size_1 = i_args
                self._root_model.set_node_size(i_node_path, i_size_1)
            elif i_flag == self.Actions.NodeAddInput:
                i_node_path, i_port_path_new = i_args
                self._root_model.add_node_input(i_node_path, i_port_path_new)
            elif i_flag == self.Actions.NodeAutoConnectInput:
                i_node_path, i_port_flag, i_port_path, i_source_path = i_args
                self._root_model.node_auto_connect_input(i_node_path, i_port_flag, i_port_path, i_source_path)
            elif i_flag == self.Actions.Paste:
                i_node_args, i_connection_args = i_args
                for j_args in i_node_args:
                    self._root_model.create_node_by_data(j_args)
                for j_args in i_connection_args:
                    self._root_model._connect_path(j_args)
