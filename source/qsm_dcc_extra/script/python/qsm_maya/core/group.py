# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import node_for_dag as _node_for_dag


class Group(_node_for_dag.DagNode):
    @classmethod
    def create(cls, group_path, *args, **kwargs):
        if cmds.objExists(group_path):
            return group_path
        parent_path = cls.to_parent_path(group_path)
        if parent_path:
            return cmds.group(empty=1, name=cls.to_name(group_path), parent=parent_path)
        return cmds.group(empty=1, name=cls.to_name(group_path))

    @classmethod
    def clear(cls, group_path):
        [cmds.delete(x) for x in cmds.listRelatives(group_path, children=1, fullPath=1) or []]

    @classmethod
    def add(cls, group_path, path, relative=False):
        results = cmds.parent(
            path,
            group_path,
            relative=relative
        )
        if results:
            return cls.to_path(results[0])

    @classmethod
    def get_children(cls, group_path):
        return cmds.listRelatives(group_path, children=1, fullPath=1) or []
