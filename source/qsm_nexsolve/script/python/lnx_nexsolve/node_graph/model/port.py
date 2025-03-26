# coding:utf-8
import lxbasic.core as bsc_core

from ...core import base as _scn_cor_base


class InputModel(_scn_cor_base._PortBase):
    def __init__(self, *args, **kwargs):
        super(InputModel, self).__init__(*args, **kwargs)
        self._gui_data.connection_path = None
        
        self._data.type = 'input'
        self._data.source = None

    def __str__(self):
        return 'InputPort(path={})'.format(
            self.get_path()
        )

    def __repr__(self):
        return '\n'+self.__str__()

    def _register_connection(self, path):
        self._gui_data.connection_path = path
        source_path, target_path = self._split_to_connection_args(path)
        self._data.source = source_path

    def _unregister_connection(self, path):
        self._gui_data.connection_path = None
        self._data.source = None

    def is_connected(self):
        return self.has_source()

    def has_source(self):
        return bool(self._data.source)

    def get_source(self):
        if self._data.source:
            node_path, port_path = bsc_core.BscAttributePath.split_by(self._data.source)
            return self.root_model.get_node(node_path).get_output(port_path)

    def get_connection_path_set(self):
        if self._gui_data.connection_path:
            return {self._gui_data.connection_path}
        return set()

    def get_connections_itr(self):
        if self._gui_data.connection_path:
            connection = self.root_model.get_connection(self._gui_data.connection_path)
            if connection:
                yield connection

    def get_connections(self):
        return list(self.get_connections_itr())

    def connect(self, source_port):
        if not isinstance(source_port, OutputModel):
            raise RuntimeError()

        self.root_model._connect_ports(source_port, self)


class OutputModel(_scn_cor_base._PortBase):
    def __init__(self, *args, **kwargs):
        super(OutputModel, self).__init__(*args, **kwargs)
        
        self._data.type = 'output'

        self._builtin_data.connection_path_set = set()

    def __str__(self):
        return 'OutputPort(path={})'.format(
            self.get_path()
        )

    def __repr__(self):
        return '\n'+self.__str__()

    def _register_connection(self, path):
        if path not in self._builtin_data.connection_path_set:
            self._builtin_data.connection_path_set.add(path)

    def _unregister_connection(self, path):
        if path in self._builtin_data.connection_path_set:
            self._builtin_data.connection_path_set.remove(path)

    def is_connected(self):
        return self.has_targets()

    def has_targets(self):
        return bool(self._builtin_data.connection_path_set)

    def get_target_itr(self):
        for i in self._builtin_data.connection_path_set:
            yield self._get_connection_target(self.root_model, i)

    def get_targets(self):
        return list(self.get_target_itr())

    def get_connection_path_set(self):
        return set(self._builtin_data.connection_path_set)

    def get_connections_itr(self):
        for i in set(self._builtin_data.connection_path_set):
            i_connection = self.root_model.get_connection(i)
            if i_connection:
                yield i_connection

    def get_connections(self):
        return list(self.get_connections_itr())

    def connect(self, target_port):
        if not isinstance(target_port, InputModel):
            raise RuntimeError()

        self.root_model.connect_ports(self, target_port)
    
    def connect_node(self, target_node):
        target_port = target_node.get_connectable_input()
        if target_port is None:
            raise RuntimeError()

        self.root_model.connect_ports(self, target_port)
