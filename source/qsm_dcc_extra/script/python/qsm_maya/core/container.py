# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import node_dag as _node_dag


class Container(object):
    @classmethod
    def create(cls, path):
        if cmds.objExists(path):
            return path
        name = path.split('|')[-1]
        _ = cmds.container(type='dagContainer', name=name)
        return _node_dag.NodeDag.to_path(_)

    @classmethod
    def create_as_expression(cls, path):
        _ = cls.create(path)
        cmds.setAttr(_+'.iconName', 'out_expression.png', type='string')
        return _

    @classmethod
    def create_as_default(cls, path):
        _ = cls.create(path)
        cmds.setAttr(_+'.iconName', 'fileNew.png', type='string')
        return _

    @classmethod
    def add_nodes(cls, path, nodes):
        cmds.container(path, edit=1, force=1, addNode=nodes)

    @classmethod
    def add_dag_nodes(cls, path, nodes):
        return [cmds.parent(x, path, relative=1)[0] for x in nodes]