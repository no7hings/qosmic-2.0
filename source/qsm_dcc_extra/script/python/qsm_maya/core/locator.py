# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import node_for_dag as _node_for_dag


class VectorLocator(object):
    @classmethod
    def create(cls, path):
        name = _node_for_dag.DagNode.to_name(path)
        t = _node_for_dag.DagNode.create_transform(path)
        for i_key, i_vector in [
            ('X', (1, 0, 0)),
            ('Y', (0, 1, 0)),
            ('Z', (0, 0, 1))
        ]:
            i_shape = cmds.createNode('locator', name=name+i_key+'Shape', parent=t, skipSelect=1)
            cmds.setAttr(i_shape+'.localPosition', *i_vector)
            cmds.setAttr(i_shape+'.localScale', *i_vector)
            _node_for_dag.NodeDrawOverride.set_color(i_shape, i_vector)
