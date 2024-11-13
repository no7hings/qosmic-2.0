# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class Set(object):
    @classmethod
    def create(cls, set_name):
        if cmds.objExists(set_name) is False:
            return cmds.sets(name=set_name, empty=1)
        return set_name

    @classmethod
    def add_one(cls, set_name, path):
        cmds.sets(path, addElement=set_name, edit=1)

    @classmethod
    def get_all(cls, set_name):
        return cmds.sets(set_name, query=1) or []

    @classmethod
    def remove_one(cls, set_name, path):
        cmds.sets(path, remove=set_name, edit=1)

    @classmethod
    def clear(cls, set_name):
        _ = cls.get_all(set_name)
        [cls.remove_one(set_name, x) for x in _]
