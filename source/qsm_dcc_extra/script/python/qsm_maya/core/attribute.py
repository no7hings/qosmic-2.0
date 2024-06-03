# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class NodeAttribute(object):
    @classmethod
    def to_atr_path(cls, path, atr_name=None):
        if atr_name is None:
            return path
        return '{}.{}'.format(path, atr_name)

    @classmethod
    def get_value(cls, path, atr_name):
        return cmds.getAttr(cls.to_atr_path(path, atr_name))

    @classmethod
    def get_is_value(cls, path, atr_name, value):
        if cls.is_exists(path, atr_name):
            _ = cls.get_value(path, atr_name)
            if value == _:
                return True
        return False

    @classmethod
    def get_as_string(cls, path, atr_name):
        return cmds.getAttr(cls.to_atr_path(path, atr_name), asString=True) or ''

    @classmethod
    def set_value(cls, path, atr_name, value):
        cmds.setAttr(cls.to_atr_path(path, atr_name), value)

    @classmethod
    def set_as_tuple(cls, path, atr_name, value):
        cmds.setAttr(cls.to_atr_path(path, atr_name), *value, clamp=1)

    @classmethod
    def set_as_string(cls, path, atr_name, value):
        cmds.setAttr(cls.to_atr_path(path, atr_name), value, type='string')

    @classmethod
    def is_lock(cls, path, atr_name):
        return cmds.getAttr(cls.to_atr_path(path, atr_name), lock=1)

    @classmethod
    def set_visible(cls, path, boolean):
        cmds.setAttr(
            cls.to_atr_path(path, 'visibility'), boolean
        )

    @classmethod
    def is_exists(cls, path, atr_name):
        return cmds.objExists(
            cls.to_atr_path(path, atr_name)
        )

    @classmethod
    def unlock(cls, path, atr_name):
        cmds.setAttr(cls.to_atr_path(path, atr_name), lock=0)

    @classmethod
    def has_source(cls, path, atr_name):
        return cmds.connectionInfo(
            cls.to_atr_path(path, atr_name),
            isDestination=1
        )

    @classmethod
    def break_source(cls, path, atr_name):
        atr_path_dst = cls.to_atr_path(path, atr_name)
        atr_path_src = cmds.connectionInfo(
            atr_path_dst,
            sourceFromDestination=1
        )
        if atr_path_src:
            path_src = atr_path_src.split('.')[0]
            if not cmds.referenceQuery(path_src, isNodeReferenced=1):
                cmds.disconnectAttr(atr_path_src, atr_path_dst)
                return True
        return False

    @classmethod
    def get_source(cls, path, atr_name):
        _ = cmds.listConnections(
            cls.to_atr_path(path, atr_name), destination=0, source=1, plugs=1
        )
        if _:
            return _[0]

    @classmethod
    def get_targets(cls, path, atr_name):
        return cmds.listConnections(
            cls.to_atr_path(path, atr_name), destination=1, source=0, plugs=1
        ) or []

    @classmethod
    def get_all_sources(cls, path):
        list_ = []
        _ = cmds.listConnections(path, destination=0, source=1, connections=1, plugs=1) or []
        # ["source-atr-path", "target-atr-path", ...]
        for seq, i in enumerate(_):
            if seq % 2:
                source_atr_path = i
                target_atr_path = _[seq - 1]
                #
                list_.append((source_atr_path, target_atr_path))
        return list_

    @classmethod
    def get_all_targets(cls, path):
        lis = []
        _ = cmds.listConnections(path, destination=1, source=0, connections=1, plugs=1) or []
        # ["source-atr-path", "target-atr-path", ...]
        for seq, i in enumerate(_):
            if seq%2:
                source_atr_path = _[seq-1]
                target_atr_path = i
                #
                lis.append((source_atr_path, target_atr_path))
        return lis

    @classmethod
    def get_source_node(cls, path, atr_name, node_type=None, skip_conversion_nodes=0):
        kwargs = dict(
            destination=0, source=1, skipConversionNodes=skip_conversion_nodes
        )
        if node_type is not None:
            kwargs['type'] = node_type

        _ = cmds.listConnections(
            cls.to_atr_path(path, atr_name), **kwargs
        ) or []
        if _:
            return _[0]

    @classmethod
    def get_target_nodes(cls, path, atr_name, node_type=None):
        kwargs = dict(
            destination=1, source=0
        )
        if node_type is not None:
            kwargs['type'] = node_type

        return cmds.listConnections(
            cls.to_atr_path(path, atr_name), **kwargs
        ) or []

    @classmethod
    def create_as_string(cls, path, atr_name, default=None):
        if cls.is_exists(path, atr_name) is False:
            cmds.addAttr(path, longName=atr_name, dataType='string')
            if default is not None:
                cls.set_as_string(path, atr_name, default)

    @classmethod
    def create_as_boolean(cls, path, atr_name, default=None):
        if cls.is_exists(path, atr_name) is False:
            cmds.addAttr(path, longName=atr_name, attributeType='bool', keyable=1)
            if default is not None:
                cls.set_value(path, atr_name, default)

    @classmethod
    def create_as_integer(cls, path, atr_name, default=None):
        if cls.is_exists(path, atr_name) is False:
            cmds.addAttr(path, longName=atr_name, attributeType='long', keyable=1)
            if default is not None:
                cls.set_value(path, atr_name, default)

    @classmethod
    def create_as_float(cls, path, atr_name, default=None):
        if cls.is_exists(path, atr_name) is False:
            cmds.addAttr(path, longName=atr_name, attributeType='double', keyable=1)
            if default is not None:
                cls.set_value(path, atr_name, default)

    @classmethod
    def create_as_enumerate(cls, path, atr_name, options, default=None):
        if cls.is_exists(path, atr_name) is False:
            cmds.addAttr(
                path, longName=atr_name, attributeType='enum', enumName=':'.join(options), keyable=1
            )
            if default is not None:
                cls.set_value(path, atr_name, default)


class NodeAttributes(object):

    @classmethod
    def get_all_keyable_names(cls, path):
        return cmds.listAttr(path, keyable=1)
