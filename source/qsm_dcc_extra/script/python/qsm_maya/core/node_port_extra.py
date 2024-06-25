# coding:utf-8
import six

import fnmatch
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

from . import node_query as _node_query


class BscNodePortOpt(object):
    PATHSEP = '.'

    def __init__(self, node_path, port_path):
        self._node_path = node_path
        self._port_path = port_path
        self._path = self._to_atr_path(
            self._node_path, self._port_path
        )
        self._port_query = None
        self._type_name = None

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.get_type_name(),
            self.get_path()
        )

    def __repr__(self):
        return '\n'+self.__str__()

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
        if self.get_type_name() in {'message', 'TdataCompound', 'Nobject', 'nurbsCurve'}:
            return None

        if as_string is True:
            return cmds.getAttr(self.path, asString=True) or ''
        #
        _ = cmds.getAttr(self.get_path())
        if self.get_port_query().has_channels(self.get_node_path()):
            return _[0]
        return _

    def set(self, value, enumerate_strings=None):
        # ignore None value
        if value is None:
            return
        # ignore connection
        if self.has_source():
            return
        # ignore lock
        if cmds.getAttr(self.get_path(), lock=1):
            return

        type_name = self.get_type_name()
        path = self.get_path()
        # noinspection PyBroadException
        try:
            if self.get_port_query().is_writeable(self.get_node_path()) is True:
                if type_name == 'string':
                    cmds.setAttr(path, value, type=self.get_type_name())
                elif type_name == 'enum':
                    if enumerate_strings is not None:
                        cmds.addAttr(
                            path,
                            enumName=':'.join(enumerate_strings),
                            edit=1
                        )
                    if isinstance(value, six.string_types):
                        enumerate_strings = self.get_port_query().get_enumerate_strings(self.get_node_path())
                        index = enumerate_strings.index(value)
                        cmds.setAttr(path, index)
                    else:
                        cmds.setAttr(path, value)
                else:
                    if isinstance(value, (tuple, list)):
                        if type_name == 'matrix':
                            # ((1, 1, 1), ...)
                            if isinstance(value[0], (tuple, list)):
                                value = [j for i in value for j in i]
                            cmds.setAttr(path, value, type=type_name)
                        elif type_name in 'doubleArray':
                            cmds.setAttr(path, value, type=type_name)
                        elif type_name in 'vectorArray':
                            cmds.setAttr(path, len(value), *value, type=type_name)
                        else:
                            # print path, type_name, value
                            cmds.setAttr(path, *value, clamp=1, type=type_name)
                    else:
                        if isinstance(value, bool):
                            cmds.setAttr(path, int(value))
                        elif isinstance(value, (float, int)):
                            cmds.setAttr(path, value)
                        else:
                            # print path, type_name, value
                            # Debug ( Clamp Maximum or Minimum Value )
                            cmds.setAttr(path, value, clamp=1)
        except Exception:
            import traceback
            traceback.print_exc()

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

    def is_changed(self):
        return self.get() != self.get_default()

    def is_locked(self):
        return cmds.getAttr(self._path, lock=1)

    def is_enumerate(self):
        return self.get_port_query().is_enumerate(self.get_node_path())

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
        if self.get_port_query().has_channels(self.get_node_path()) is True:
            return cmds.connectionInfo(
                self.get_path(), isDestination=True
            )
        elif self.get_port_query().has_parent(self.get_node_path()) is True:
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
        args = self.get_source_args()
        if args:
            return self.PATHSEP.join(args)

    def get_source_args(self):
        _ = cmds.connectionInfo(
            self.get_path(),
            sourceFromDestination=1
        )
        if _:
            atr = bsc_core.PthAttributeOpt(_)
            node_path = atr.obj_path
            if cmds.objExists(node_path) is True:
                port_path = atr.port_path
                return _node_query.NodeQuery._to_node_path(node_path), port_path

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
