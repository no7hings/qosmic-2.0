# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ... import core as _mya_core


class SkinClusterOpt(object):
    def __init__(self, path_or_name):
        """
        is non-dag node
        """
        self._path = path_or_name

    def get_geometries(self):
        return cmds.skinCluster(self._path, query=True, geometry=True) or []

    def get_joints(self):
        return cmds.skinCluster(self._path, query=True, influence=True)
