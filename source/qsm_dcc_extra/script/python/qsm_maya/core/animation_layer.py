# coding:utf-8

# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class AnimationOpt(object):
    def __init__(self, path):
        self._path = path

    def is_active(self):
        return not cmds.animLayer(self._path, query=1, mute=1)

    def get_weight(self):
        return cmds.animLayer(self._path, query=1, weight=1)


class AnimationLayers(object):
    @classmethod
    def get_root(cls):
        return cmds.animLayer(query=1, root=1)

    @classmethod
    def get_all(cls):
        return cmds.ls(type='animLayer', long=1) or []

