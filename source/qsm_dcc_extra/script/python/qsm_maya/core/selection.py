# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class Selection(object):
    @classmethod
    def set(cls, paths):
        cmds.select(paths)

    @classmethod
    def clear(cls):
        cmds.select(clear=1)

    @classmethod
    def get(cls):
        return cmds.ls(selection=1, long=1) or {}
