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
    def set_value(cls, path, atr_name, value):
        cmds.setAttr(cls.to_atr_path(path, atr_name), value)

    @classmethod
    def is_lock(cls, path, atr_name):
        return cmds.getAttr(cls.to_atr_path(path, atr_name), lock=1)

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
    def find_source_node(cls, path, atr_name, node_type):
        _ = cmds.listConnections(
            cls.to_atr_path(path, atr_name), destination=0, source=1, type=node_type
        ) or []
        if _:
            return _[0]


class Attributes(object):

    @classmethod
    def get_all_keyable_names(cls, path):
        return cmds.listAttr(path, keyable=1)