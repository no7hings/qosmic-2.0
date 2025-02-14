# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class History(object):

    @classmethod
    def get_all(cls, path):
        return cmds.listHistory(path, allConnections=1) or []

    @classmethod
    def find_one(cls, path, type_includes):
        _ = cls.get_all(path)
        return [x for x in _ if cmds.nodeType(x) in type_includes]
