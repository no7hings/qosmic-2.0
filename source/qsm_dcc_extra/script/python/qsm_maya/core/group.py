# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import node_for_dag as _node_for_dag


class Group(_node_for_dag.DagNode):
    @classmethod
    def create(cls, path, *args, **kwargs):
        if cmds.objExists(path):
            return path
        cmds.group(empty=1, name=cls.path_to_name(path), parent=cls.get_parent(path))
