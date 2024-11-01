# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

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
    def create_dag(cls, group_path, *args, **kwargs):
        if cmds.objExists(group_path):
            return group_path

        path_opt = bsc_core.BscNodePathOpt(group_path)
        paths = path_opt.get_component_paths()
        paths.reverse()
        for i_path in paths:
            if i_path != path_opt.pathsep:
                cls.create(i_path)

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
    def add_one(cls, group_path, path, relative=False):
        parent_path = _node_for_dag.DagNode.get_parent(path)
        if parent_path == group_path:
            return path

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


class GroupOpt(_node_for_dag.DagNodeOpt):
    def __init__(self, *args, **kwargs):
        super(GroupOpt, self).__init__(*args, **kwargs)

    def add_one(self, path):
        parent_path = _node_for_dag.DagNode.get_parent(path)
        if parent_path == self._path:
            return path
        return Group.add(self._path, path)
    
    def find_all_shapes_by_type(self, type_name):
        return cmds.ls(
            self._path, dag=1, type=type_name, noIntermediate=1, long=1
        ) or []
