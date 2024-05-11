# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.api.OpenMaya as om2

import lxbasic.core as bsc_core

import lxmaya.core as mya_core

from . import node as _node

from . import node_for_dag as _node_dag


class Shape(_node_dag.DagNode):

    @classmethod
    def get_transform(cls, path):
        return cmds.listRelatives(path, parent=1, fullPath=1, type='transform')[0]

    @classmethod
    def get_instanced_transforms(cls, path):
        return cmds.listRelatives(path, fullPath=1, allParents=1) or []

    @classmethod
    def is_instanced(cls, path):
        _ = cmds.listRelatives(path, fullPath=1, allParents=1)
        return len(_) > 1

    @classmethod
    def remove_instanced(cls, path):
        transform = cls.get_transform(path)
        transform_name = transform.split('|')[-1]
        transform_name_copy = '{}_copy'.format(transform_name)
        transform_copy = cmds.duplicate(
            transform, name=transform_name_copy
        )
        cmds.delete(transform)
        cmds.rename(transform_copy[0], transform_name)

    @classmethod
    def instance_to(cls, path, transform_path_dst):
        name = path.split('|')[-1]
        new_path = '{}|{}'.format(transform_path_dst, name)
        if cmds.objExists(new_path) is True:
            return path
        _ = cmds.parent(path, transform_path_dst, shape=1, add=1)
        return _node_dag.DagNode.to_path(_[0])


class ShapeOpt(_node_dag.DagNodeOpt):
    def __init__(self, path):
        super(ShapeOpt, self).__init__(path)

    @property
    def shape_path(self):
        return self._path

    @property
    def shape_name(self):
        return self._name

    @property
    def transform_path(self):
        return bsc_core.PthNodeMtd.get_dag_parent_path(
            self._path, _node_dag.DagNode.PATHSEP
        )

    @property
    def transform_name(self):
        return self.transform_path.split('|')[-1]
