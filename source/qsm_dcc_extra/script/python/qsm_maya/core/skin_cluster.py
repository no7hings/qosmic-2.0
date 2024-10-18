# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class SkinCluster:
    @classmethod
    def get_geometries(cls, path):
        return cmds.skinCluster(path, query=True, geometry=True) or []

    @classmethod
    def get_joints(cls, path):
        return cmds.skinCluster(path, query=True, influence=True)


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
