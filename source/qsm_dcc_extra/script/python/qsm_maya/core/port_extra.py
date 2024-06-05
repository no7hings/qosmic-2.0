# coding:utf-8
import six

import fnmatch
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

from . import node_query as _node_query


class BscPortOpt(object):
    PATHSEP = '.'

    def __init__(self, node_path, port_path):
        self._node_path = node_path
        self._port_path = port_path
        self._path = self._to_atr_path(
            self._node_path, self._port_path
        )
        self._port_query = None
        self._type_name = None

    @classmethod
    def create(cls, node_path, port_path, type_name, enumerate_strings=None):
        if cls.check_exists(node_path, port_path) is False:
            if type_name == 'string':
                cmds.addAttr(
                    node_path,
                    longName=port_path,
                    dataType=type_name
                )
            elif type_name == 'enum':
                if isinstance(enumerate_strings, (tuple, list)):
                    cmds.addAttr(
                        node_path,
                        longName=port_path,
                        attributeType=type_name,
                        enumName=':'.join(enumerate_strings)
                    )
                else:
                    cmds.addAttr(
                        node_path,
                        longName=port_path,
                        attributeType=type_name
                    )
            else:
                cmds.addAttr(
                    node_path,
                    longName=port_path,
                    attributeType=type_name
                )

    @classmethod
    def check_exists(cls, node_path, port_path):
        atr_path = cls._to_atr_path(node_path, port_path)
        return cmds.objExists(atr_path)

    @classmethod
    def _to_atr_path(cls, node_path, port_path):
        return cls.PATHSEP.join(
            [node_path, port_path]
        )

    @classmethod
    def _set_connection_create_(cls, atr_path_src, atr_path_tgt):
        if cmds.isConnected(atr_path_src, atr_path_tgt) is False:
            if cmds.getAttr(atr_path_tgt, lock=1) is False:
                cmds.connectAttr(atr_path_src, atr_path_tgt, force=1)

    def get_port_query(self):
        if self._port_query is not None:
            return self._port_query

        _ = _node_query.PortQuery(
            cmds.nodeType(self._node_path),
            self._port_path
        )
        self._port_query = _
        return _

    def get_node_path(self):
        return self._node_path

    node_path = property(get_node_path)

    def get_type_name(self):
        if self._type_name is not None:
            return self._type_name

        _ = cmds.getAttr(self._path, type=1)
        self._type_name = _
        return _

    type_name = property(get_type_name)

    def get_path(self):
        return self._path

    path = property(get_path)

    def join_by(self):
        return self._path

    atr_path = property(join_by)

    def get_port_path(self):
        return self._port_path

    port_path = property(get_port_path)

    def get_array_indices(self):
        if self.get_port_query().is_array(self.get_node_path()) is True:
            return cmds.getAttr(
                '.'.join([self.get_node_path(), self.get_port_path()]),
                multiIndices=1,
                silent=1
            ) or []
        return []

    def get(self, as_string=False):
        if self.get_type_name() in {'message', 'TdataCompound'}:
            return None

        if as_string is True:
            return cmds.getAttr(self.path, asString=True) or ''
        #
        _ = cmds.getAttr(self.get_path())
        if self.get_port_query().has_channels(self.get_node_path()):
            return _[0]
        return _

    def set(self, value, enumerate_strings=None):
        if self.has_source() is False:
            # unlock first
            is_lock = cmds.getAttr(self.get_path(), lock=1)
            if is_lock:
                cmds.setAttr(self.get_path(), lock=0)
            #
            if self.get_port_query().is_writable(self.get_node_path()) is True:
                if self.get_type_name() == 'string':
                    cmds.setAttr(self.get_path(), value, type=self.get_type_name())
                elif self.get_type_name() == 'enum':
                    if enumerate_strings is not None:
                        cmds.addAttr(
                            self.get_path(),
                            enumName=':'.join(enumerate_strings),
                            edit=1
                        )
                    #
                    if isinstance(value, six.string_types):
                        enumerate_strings = self.get_port_query().get_enumerate_strings(self.get_node_path())
                        index = enumerate_strings.index(value)
                        cmds.setAttr(self.get_path(), index)
                    else:
                        cmds.setAttr(self.get_path(), value)
                else:
                    if isinstance(value, (tuple, list)):
                        cmds.setAttr(self.get_path(), *value, clamp=1)
                    else:
                        # Debug ( Clamp Maximum or Minimum Value )
                        cmds.setAttr(self.get_path(), value, clamp=1)

    def get_default(self):
        if self.get_type_name() == 'message':
            return None
        elif self.get_type_name() == 'TdataCompound':
            return None
        #
        _ = self.get_port_query().get_default()
        if self.get_type_name() == 'bool':
            return bool(int(_))
        elif self.get_type_name() == 'matrix':
            return [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        return _

    def get_is_changed(self):
        return self.get() != self.get_default()

    def get_is_enumerate(self):
        return self.get_port_query().get_is_enumerate(self.get_node_path())

    def get_enumerate_strings(self):
        return self.get_port_query().get_enumerate_strings(
            self.get_node_path()
        )

    def set_enumerate_strings(self, strings):
        cmds.addAttr(
            self._path,
            edit=1, enumName=':'.join(strings)
        )

    def has_source(self):
        _ = cmds.connectionInfo(
            self.get_path(), isExactDestination=True
        )
        if self.get_port_query().get_has_channels(self.get_node_path()) is True:
            return cmds.connectionInfo(
                self.get_path(), isDestination=True
            )
        elif self.get_port_query().get_has_parent(self.get_node_path()) is True:
            return cmds.connectionInfo(
                self.get_path(), isDestination=True
            )
        return _

    def get_has_source_(self, exact=False):
        if exact is True:
            return cmds.connectionInfo(
                self.get_path(), isExactDestination=True
            )
        return cmds.connectionInfo(
            self.get_path(), isDestination=True
        )

    def get_source(self):
        _ = cmds.connectionInfo(
            self.get_path(),
            sourceFromDestination=1
        )
        if _:
            atr = bsc_core.PthAttributeOpt(_)
            node_path = atr.obj_path
            
            if cmds.objExists(node_path) is True:
                port_path = atr.port_path
                return self.PATHSEP.join(
                    [_node_query.NodeQuery._to_node_path(node_path), port_path]
                )

    def set_disconnect(self):
        source = self.get_source()
        if source:
            cmds.disconnectAttr(source, self.get_path())

    def set_default(self):
        default_value = self.get_default()
        if default_value is not None:
            self.set(default_value)

    def get_is_naming_match(self, pattern):
        return fnmatch.filter(
            [self.get_port_path()], pattern
        ) != []

    def get_is_naming_matches(self, patterns):
        for i in patterns:
            if self.get_is_naming_match(i) is True:
                return True
        return False

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__, 
            self.get_type_name(),
            self.get_path()
        )

    def __repr__(self):
        return '\n'+self.__str__()
