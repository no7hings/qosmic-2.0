# coding:utf-8
import math
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import attribute as _attribute

from . import node as _node

from . import node_for_dag as _node_for_dag


class Transform(_node_for_dag.DagNode):

    @classmethod
    def create(cls, path, *args, **kwargs):
        return super(Transform, cls).create(path, 'transform')

    @classmethod
    def zero_transformations(cls, path, with_visibility=False):
        dict_ = dict(
            translate=(0.0, 0.0, 0.0),
            rotate=(0.0, 0.0, 0.0),
            scale=(1.0, 1.0, 1.0)
        )
        for k, v in dict_.items():
            if _attribute.NodeAttribute.is_lock(path, k) is True:
                _attribute.NodeAttribute.unlock(path, k)

            cmds.setAttr('{}.{}'.format(path, k), *v)

        if with_visibility:
            cmds.setAttr(path+'.visibility', 1)

    @classmethod
    def freeze_transformations(cls, path):
        cmds.makeIdentity(path, apply=1, translate=1, rotate=1, scale=1)

    @classmethod
    def reset_transformations(cls, path):
        cmds.makeIdentity(path, apply=0, translate=1, rotate=1, scale=1)

    @classmethod
    def get_shape_path(cls, path):
        _ = cmds.listRelatives(path, children=1, shapes=1, noIntermediate=1, fullPath=1)
        if _:
            return _[0]

    @classmethod
    def delete_all_shapes(cls, path):
        _ = cmds.listRelatives(path, children=1, shapes=1, fullPath=1)
        for i in _:
            cmds.delete(i)

    @classmethod
    def hide_all_shapes(cls, path):
        _ = cmds.listRelatives(path, children=1, shapes=1, fullPath=1)
        for i in _:
            cmds.setAttr(i+'.visibility', 0)

    @classmethod
    def get_world_extent(cls, path):
        _x, _y, _z, x, y, z = cmds.xform(path, boundingBox=1, worldSpace=1, query=1)
        return (_x, _y, _z), (x, y, z)

    @classmethod
    def get_dimension(cls, path):
        (_x, _y, _z), (x, y, z) = cls.get_world_extent(path)
        return x-_x, y-_y, z-_z

    @classmethod
    def get_world_center(cls, path):
        _x, _y, _z, x, y, z = cmds.xform(path, boundingBox=1, worldSpace=1, query=1)
        return (_x+x)/2, (_y+y)/2, (_z+z)/2

    @classmethod
    def compute_distance(cls, p_0, p_1):
        x, y, z = p_0
        x_dst, y_dst, z_dst = p_1
        return math.sqrt((x-x_dst)**2+(y-y_dst)**2+(z-z_dst)**2)


class TransformOpt(object):
    def __init__(self, transform_path):
        self._transform_path = transform_path
        self._uuid = _node.Node.get_uuid(self._transform_path)
