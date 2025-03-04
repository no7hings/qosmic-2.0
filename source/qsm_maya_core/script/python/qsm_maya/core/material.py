# coding:utf-8
import sys

# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

from . import node as _node

from . import attribute as _attribute

from . import connection as _connection

from . import node_graph as _node_graph

from . import node_for_shader as _node_for_shader


class Material(object):
    @classmethod
    def create(cls, name):
        if cmds.objExists(name) is True:
            return name
        return cmds.sets(
            renderable=1, noSurfaceShader=1, empty=1, name=name
        )

    @classmethod
    def create_as_lambert(cls, name, color):
        shader_name = '{}_SRF'.format(name)
        _node_for_shader.Shader.create(
            shader_name, 'lambert'
        )
        material_name = name
        cls.create(material_name)

        _connection.Connection.create(
            shader_name+'.outColor', material_name+'.surfaceShader'
        )

        _attribute.NodeAttribute.set_as_tuple(
            shader_name, 'color', color
        )
        return material_name

    @classmethod
    def get_all_shading_engines(cls, name):
        return cmds.listConnections(
            name, destination=1, source=0, type='shadingEngine'
        ) or []

    @classmethod
    def get_all_texture_references(cls, name):
        return _node_graph.NodeGraph.get_all_source_nodes(
            name, type_includes=['file']
        )

    @classmethod
    def assign_surface_shader(cls, name, shader):
        _connection.Connection.create(
            _attribute.NodeAttribute.to_atr_path(
                shader, 'outColor'
            ),
            _attribute.NodeAttribute.to_atr_path(
                name, 'surfaceShader'
            )
        )

    @classmethod
    def assign_to(cls, name, geometry_path):
        cmds.sets(geometry_path, forceElement=name)

    @classmethod
    def get_surface_shader(cls, name):
        return _attribute.NodeAttribute.get_source_node(
            name, 'surfaceShader'
        )

    @classmethod
    def unlock_default(cls):
        name = 'initialShadingGroup'
        if _node_for_shader.Shader.is_locked(name) is True:
            sys.stderr.write('initialShadingGroup is locked. try to unlock it.\n')
            # noinspection PyBroadException
            try:
                _node_for_shader.Shader.unlock(name)
            except Exception:
                pass


class MaterialOpt(_node.NodeOpt):
    def __init__(self, *args, **kwargs):
        super(MaterialOpt, self).__init__(*args, **kwargs)

    def assign_to(self, path):
        # noinspection PyBroadException
        try:
            Material.assign_to(
                self._name_or_path, path
            )
        except Exception:
            bsc_core.BscException.set_print()


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
