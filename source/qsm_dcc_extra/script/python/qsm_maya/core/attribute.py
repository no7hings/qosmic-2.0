# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class Attribute(object):
    @classmethod
    def to_atr_path(cls, path, atr_name=None):
        if atr_name is None:
            return path
        return '{}.{}'.format(path, atr_name)

    @classmethod
    def get_value(cls, path, atr_name):
        return cmds.getAttr(cls.to_atr_path(path, atr_name))

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
    def find_source_node(cls, path, atr_name, node_type=None):
        kwargs = dict(
            destination=0, source=1
        )
        if node_type is not None:
            kwargs['type'] = node_type

        _ = cmds.listConnections(
            cls.to_atr_path(path, atr_name), **kwargs
        ) or []
        if _:
            return _[0]

    @classmethod
    def find_target_node(cls, path, atr_name, node_type=None):
        kwargs = dict(
            destination=1, source=0
        )
        if node_type is not None:
            kwargs['type'] = node_type

        _ = cmds.listConnections(
            cls.to_atr_path(path, atr_name), **kwargs
        ) or []
        if _:
            return _[0]

    @classmethod
    def find_target(cls, path, atr_name):
        _ = cmds.listConnections(
            cls.to_atr_path(path, atr_name), destination=1, source=0, plugs=1
        ) or []
        if _:
            return _[0]

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
    def create_as_enumerate(cls, path, atr_name, options, default=None):
        if cls.is_exists(path, atr_name) is False:
            cmds.addAttr(
                path, longName=atr_name, attributeType='enum', enumName=':'.join(options), keyable=1
            )
            if default is not None:
                cls.set_value(path, atr_name, default)


class Attributes(object):

    @classmethod
    def get_all_keyable_names(cls, path):
        return cmds.listAttr(path, keyable=1)
