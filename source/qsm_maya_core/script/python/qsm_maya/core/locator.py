# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import node_for_dag as _node_for_dag

from . import shape as _shape


class VectorLocator(object):
    @classmethod
    def create(cls, path, scale=1.0):
        if cmds.objExists(path) is True:
            return False, path
        name = _node_for_dag.DagNode.to_name(path)
        transform = _node_for_dag.DagNode.create_transform(path)
        for i_key, i_vector in [
            ('X', (scale*.5, 0, 0)),
            ('Y', (0, scale*.5, 0)),
            ('Z', (0, 0, scale*.5))
        ]:
            i_shape = cmds.createNode('locator', name=name+i_key+'Shape', parent=transform, skipSelect=1)
            cmds.setAttr(i_shape+'.localPosition', *i_vector)
            cmds.setAttr(i_shape+'.localScale', *i_vector)
            _node_for_dag.NodeDrawOverride.set_color(i_shape, i_vector)
        return True, transform

    @classmethod
    def create_for(cls, target):
        if cmds.objExists(target) is False:
            return
        name = _node_for_dag.DagNode.to_name_without_namespace(target)
        return cls.create('|{}__loc'.format(name))


