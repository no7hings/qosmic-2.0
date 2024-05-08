# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import attribute as _attribute

from . import connection as _connection

from . import node_graph as _node_graph


class Material(object):
    @classmethod
    def create(cls, name):
        if cmds.objExists(name) is True:
            return name
        return cmds.sets(
            renderable=1, noSurfaceShader=1, empty=1, name=name
        )

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

    @classmethod
    def assign_surface_shader(cls, path, shader):
        _connection.Connection.create(
            _attribute.Attribute.to_atr_path(
                shader, 'outColor'
            ),
            _attribute.Attribute.to_atr_path(
                path, 'surfaceShader'
            )
        )

    @classmethod
    def assign_to(cls, path, geometry_path):
        cmds.sets(geometry_path, forceElement=path)

