# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import node_for_dag as _node_for_dag


class Container(object):
    @classmethod
    def create(cls, path_or_name, icon=None):
        if cmds.objExists(path_or_name):
            return _node_for_dag.DagNode.to_path(path_or_name)
        name = path_or_name.split('|')[-1]
        _ = cmds.container(type='dagContainer', name=name)
        if icon is not None:
            cmds.setAttr(_+'.iconName', icon, type='string')
        return _node_for_dag.DagNode.to_path(_)

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
    def add_dag_nodes(cls, path, nodes, relative=False):
        return [cmds.parent(x, path, relative=relative)[0] for x in nodes]

    @classmethod
    def get_all_nodes(cls, path):
        return cmds.container(path, query=1, nodeList=1) or []

    @classmethod
    def find_all_nodes(cls, path, type_includes):
        return [x for x in cls.get_all_nodes(path) if cmds.nodeType(x) in type_includes]
