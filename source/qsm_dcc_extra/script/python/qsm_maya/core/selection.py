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
