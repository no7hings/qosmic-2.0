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
            _attribute.NodeAttribute.to_atr_path(
                shader, 'outColor'
            ),
            _attribute.NodeAttribute.to_atr_path(
                path, 'surfaceShader'
            )
        )

    @classmethod
    def assign_to(cls, path, geometry_path):
        cmds.sets(geometry_path, forceElement=path)


class MaterialLightLink(object):
    OBJ_NAME_0 = 'renderPartition'
    OBJ_NAME_1 = 'lightLinker1'
    OBJ_NAME_2 = 'defaultLightSet'

    @classmethod
    def create(cls, path):
        def get_connection_index_():
            for i in range(5000):
                if (
                    get_is_partition_connected_at_(i)
                    and get_is_obj_link_connected_at_(i)
                    and get_is_obj_shadow_link_connected_at_(i)
                    and get_is_light_link_connected_at_(i)
                    and get_is_light_shadow_link_connected_at_(i)
                ):
                    return i

        def get_is_connected_(connection):
            boolean = False
            if cmds.objExists(connection):
                if not cmds.connectionInfo(connection, isDestination=1):
                    boolean = True
            return boolean

        def get_is_partition_connected_at_(index):
            connection = cls.OBJ_NAME_0+'.sets[%s]' % index
            return get_is_connected_(connection)

        def get_is_obj_link_connected_at_(index):
            connection = cls.OBJ_NAME_1+'.link[%s].object' % index
            return get_is_connected_(connection)

        def get_is_obj_shadow_link_connected_at_(index):
            connection = cls.OBJ_NAME_1+'.shadowLink[%s].shadowObject' % index
            return get_is_connected_(connection)

        def get_is_light_link_connected_at_(index):
            connection = cls.OBJ_NAME_1+'.link[%s].light' % index
            return get_is_connected_(connection)

        def get_is_light_shadow_link_connected_at_(index):
            connection = cls.OBJ_NAME_1+'.shadowLink[%s].shadowLight' % index
            return get_is_connected_(connection)

        def main_fnc_():
            index = get_connection_index_()
            if index:
                # Debug ( Repeat )
                if not cmds.connectionInfo(path+'.partition', isSource=1):
                    cmds.connectAttr(path+'.partition', cls.OBJ_NAME_0+'.sets[%s]'%index)
                    cmds.connectAttr(
                        path+'.message',
                        cls.OBJ_NAME_1+'.link[%s].object'%index
                    )
                    cmds.connectAttr(
                        path+'.message',
                        cls.OBJ_NAME_1+'.shadowLink[%s].shadowObject'%index
                    )
                    cmds.connectAttr(
                        cls.OBJ_NAME_2+'.message',
                        cls.OBJ_NAME_1+'.link[%s].light'%index
                    )
                    cmds.connectAttr(
                        cls.OBJ_NAME_2+'.message',
                        cls.OBJ_NAME_1+'.shadowLink[%s].shadowLight'%index
                    )

        main_fnc_()
