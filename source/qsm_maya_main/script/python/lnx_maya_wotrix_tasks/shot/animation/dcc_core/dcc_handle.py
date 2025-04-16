# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class ShotAnimationAssetHandle(object):
    def __init__(self, rig_namespace):
        self._rig_namespace = rig_namespace

    @property
    def rig_namespace(self):
        return self._rig_namespace
