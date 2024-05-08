# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import attribute as _attribute


class Transform(object):

    @classmethod
    def zero_transformations(cls, path, with_visibility=False):
        dict_ = dict(
            translate=(0.0, 0.0, 0.0),
            rotate=(0.0, 0.0, 0.0),
            scale=(1.0, 1.0, 1.0)
        )
        for k, v in dict_.items():
            if _attribute.Attribute.is_lock(path, k) is True:
                _attribute.Attribute.unlock(path, k)

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
