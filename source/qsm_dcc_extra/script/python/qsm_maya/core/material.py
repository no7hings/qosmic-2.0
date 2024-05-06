# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import node_graph as _node_graph


class Material(object):

    @classmethod
    def get_all_shading_engines(cls, path):
        return cmds.listConnections(
            path, destination=1, source=0, type='shadingEngine'
        ) or []

    @classmethod
    def get_all_texture_references(cls, path):
        return _node_graph.NodeGraph.get_all_source_nodes(
            path, type_includes=['file']
        )
