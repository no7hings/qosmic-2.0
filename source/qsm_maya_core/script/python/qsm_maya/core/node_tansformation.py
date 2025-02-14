# coding:utf-8
import math
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.api.OpenMaya as om2

from . import transformation as _transformation


class NodeRotate:
    @classmethod
    def apply_and_reorder_to(cls, node, rotate, rotate_order):
        """
        apply to target with auto reorder
        """
        cmds.setAttr(
            node+'.rotate', *cls.reorder_to(node, rotate, rotate_order)
        )

    @classmethod
    def reorder_to(cls, node, rotate, rotate_order):
        rotate_order_0 = cmds.getAttr(node+'.rotateOrder')
        if rotate_order_0 != rotate_order:
            rotation = _transformation.Rotation.to_rotation(rotate, rotate_order)
            rotation_tgt = rotation.reorder(rotate_order_0)
            return _transformation.Rotation.decompose(rotation_tgt)
        return rotate
