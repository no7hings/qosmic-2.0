# coding:utf-8
import math
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import attribute as _attribute

from . import node as _node

from . import node_for_dag as _node_for_dag


class Transform(_node_for_dag.DagNode):
    @classmethod
    def to_shape_args(cls, path_or_name):
        if _node.Node.is_transform_type(path_or_name):
            transform_path = cls.to_path(path_or_name)
            _ = cls.get_shape(path_or_name)
            if cls.node_is_shape(_) is True:
                return transform_path, _
        elif cls.node_is_shape(path_or_name):
            return cls.get_shape_transform(path_or_name), cls.to_path(path_or_name)

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
    def get_shape(cls, path):
        _ = cmds.listRelatives(path, children=1, shapes=1, noIntermediate=1, fullPath=1)
        if _:
            return _[0]

    @classmethod
    def delete_all_shapes(cls, path):
        _ = cmds.listRelatives(path, children=1, shapes=1, fullPath=1) or []
        for i in _:
            cmds.delete(i)
    
    @classmethod
    def get_all_shapes(cls, path):
        return cmds.listRelatives(path, children=1, shapes=1, fullPath=1) or []
    
    @classmethod
    def get_all_non_intermediate_shapes(cls, path):
        return cmds.listRelatives(path, children=1, shapes=1, fullPath=1, noIntermediate=1) or []

    @classmethod
    def hide_all_shapes(cls, path):
        _ = cmds.listRelatives(path, children=1, shapes=1, fullPath=1)
        for i in _:
            cmds.setAttr(i+'.visibility', 0)

    @classmethod
    def get_world_extent(cls, path):
        _x, _y, _z, x, y, z = cmds.xform(path, boundingBox=1, worldSpace=1, query=1)
        # min, max
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
    def get_world_matrix(cls, path):
        return cmds.xform(path, matrix=1, worldSpace=1, query=1)

    @classmethod
    def get_world_translation(cls, path):
        return cmds.xform(path, translation=1, worldSpace=1, query=1)

    @classmethod
    def set_world_translation(cls, path, translation):
        cmds.xform(path, translation=translation, worldSpace=1)

    @classmethod
    def get_world_rotation(cls, path):
        return cmds.xform(path, rotation=1, worldSpace=1, query=1)

    @classmethod
    def set_world_rotation(cls, path, rotation):
        cmds.xform(path, rotation=rotation, worldSpace=1)

    @classmethod
    def set_world_transformation(cls, path, translation, rotation):
        cmds.xform(path, translation=translation, rotation=rotation, worldSpace=1)

    @classmethod
    def get_world_scale(cls, path):
        return cmds.xform(path, scale=1, worldSpace=1, query=1)

    @classmethod
    def get_world_transformation(cls, path):
        return (
            cls.get_world_translation(path),
            cls.get_world_rotation(path),
            cls.get_world_scale(path),
        )

    @classmethod
    def compute_distance(cls, p_0, p_1):
        x, y, z = p_0
        x_dst, y_dst, z_dst = p_1
        return math.sqrt((x-x_dst)**2+(y-y_dst)**2+(z-z_dst)**2)

    @classmethod
    def check_is_transform(cls, path):
        """
        check node is a transform (has shape) not a group
        """
        if cmds.nodeType(path) == 'transform':
            shape_paths = cmds.listRelatives(path, children=1, shapes=1, noIntermediate=0, fullPath=1) or []
            if shape_paths:
                return True
            return False
        return False
    
    @classmethod
    def delete_all_intermediate_shapes(cls, path):
        shapes = cls.get_all_shapes(path)
        non_intermediate_shapes = cls.get_all_non_intermediate_shapes(path)
        [cmds.delete(x) for x in shapes if x not in non_intermediate_shapes]

    @classmethod
    def is_visible(cls, path):
        return cmds.getAttr(path+'.visibility')

    @classmethod
    def is_show(cls, path):
        if cmds.getAttr(path+'.overrideEnabled') is True:
            return cmds.getAttr('.overrideVisibility')
        return cmds.getAttr(path+'.visibility')

    @classmethod
    def is_override_hidden(cls, path):
        if cmds.getAttr(path+'.overrideEnabled') is True:
            return not cmds.getAttr(path+'.overrideVisibility')
        return False

    @classmethod
    def get_translate(cls, path):
        return cmds.getAttr(path+'.translate')[0]

    @classmethod
    def set_translate(cls, path, p):
        cmds.setAttr(path+'.translate', *p)


class TransformOpt(object):
    def __init__(self, transform_path):
        self._transform_path = transform_path
        self._uuid = _node.Node.get_uuid(self._transform_path)
