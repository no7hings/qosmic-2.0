# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.api.OpenMaya as om2

import lxbasic.core as bsc_core

import lxmaya.core as mya_core

from . import node as _node

from . import node_for_dag as _node_for_dag


class Shape(_node_for_dag.DagNode):

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
        return _node_for_dag.DagNode.to_path(_[0])

    @classmethod
    def check_is_shape(cls, path):
        return not not cmds.ls(path, shapes=1)

    @classmethod
    def clear_all_instanced(cls, shape_path):
        transform_paths = cmds.listRelatives(shape_path, fullPath=1, allParents=1) or []
        if len(transform_paths) > 1:
            for i_transform_path in transform_paths:
                i_children = cmds.listRelatives(i_transform_path, children=1, fullPath=1)
                i_parents = cmds.listRelatives(i_children[0], fullPath=1, allParents=1)
                if i_parents > 1:
                    i_transform_name = i_transform_path.split('|')[-1]
                    i_transform_name_copy = '{}_copy'.format(i_transform_name)
                    transform_copy = cmds.duplicate(
                        i_transform_path, name=i_transform_name_copy
                    )
                    cmds.delete(i_transform_path)
                    cmds.rename(transform_copy[0], i_transform_name)

    @classmethod
    def is_intermediate(cls, path):
        return bool(cmds.getAttr(path+'.intermediateObject'))


class Geometry(Shape):

    @classmethod
    def get_materials(cls, shape_path):
        return cmds.listConnections(
            shape_path, destination=1, source=0, type=mya_core.MyaNodeTypes.Material
        ) or []

    @classmethod
    def get_material_assign_map(cls, shape_path):
        dict_ = {}
        transform_path = cls.get_transform(shape_path)
        material_paths = cls.get_materials(shape_path)
        if material_paths:
            for i_material_path in material_paths:
                i_results = cmds.sets(i_material_path, query=1)
                if i_results:
                    i_element_paths = cmds.ls(i_results, leaf=1, noIntermediate=1, long=1) or []
                    for j_element_path in i_element_paths:
                        dict_[j_element_path] = i_material_path
        return dict_


class ShapeOpt(_node_for_dag.DagNodeOpt):
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
        return bsc_core.BscPath.get_dag_parent_path(
            self._path, _node_for_dag.DagNode.PATHSEP
        )

    @property
    def transform_name(self):
        return self.transform_path.split('|')[-1]
