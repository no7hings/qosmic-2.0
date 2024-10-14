# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

from . import history as _history

from . import node as _node

from . import node_for_dag as _node_for_dag

from . import attribute as _attribute

from . import transform as _transform

from . import shape as _shape


class RebuildForNucleus(object):
    @classmethod
    def create_for(cls, node_type, target_shape_path, target_any_paths):
        """
        nClothCreate;
        performCreateNCloth 0;
        createNCloth 0;
        sets -e -forceElement initialShadingGroup;
        """
        target_any_paths = [
            _shape.Shape.get_transform(x) if _shape.Shape.check_is_shape(x) else x
            for x in target_any_paths
        ]
        cmds.select(target_any_paths)

        if _transform.Transform.is_transform_type(target_shape_path):
            target_shape_path = _transform.Transform.get_shape(target_shape_path)

        if node_type == 'nCloth':
            mel.eval('nClothCreate;')
        elif node_type == 'nRigid':
            mel.eval('nClothMakeCollide;')
        elif node_type == 'hairSystem':
            mel.eval('assignNewHairSystem;')
        else:
            raise RuntimeError()

        # _history.History.find_one(target_shape_path, [node_type])

        _ = _attribute.NodeAttribute.get_target_nodes(
            target_shape_path, 'worldMesh', node_type
        )
        if _:
            node_path = _[0]
            return node_path

    @classmethod
    def find_any_from(cls, target_shape_path):
        # source
        _ = _attribute.NodeAttribute.get_source_node(
            target_shape_path, 'inMesh'
        )
        if _:
            node_path = _
            node_type = _node.Node.get_type(node_path)
            if node_type == 'nCloth':
                return node_path
        # target
        _ = _attribute.NodeAttribute.get_target_nodes(
            target_shape_path, 'worldMesh'
        )
        if _:
            node_path = _[0]
            node_type = _node.Node.get_type(node_path)
            if node_type == 'nRigid':
                return node_path


class NCloth(object):
    @classmethod
    def find_input_mesh_transform(cls, path):
        # target
        _ = _attribute.NodeAttribute.get_source_node(
            path, 'inputMesh', 'mesh'
        )
        if _:
            return _shape.Shape.get_transform(_)


class NRigid(object):
    @classmethod
    def find_input_mesh_transform(cls, path):
        # source
        _ = _attribute.NodeAttribute.get_source_node(
            path, 'inputMesh', 'mesh'
        )
        if _:
            return _shape.Shape.get_transform(_)


class Field(object):
    @classmethod
    def create_for(cls, node_type, target_shape_path, target_any_paths):
        """
        Air;
        """
        target_any_paths = [
            _shape.Shape.get_transform(x) if _shape.Shape.check_is_shape(x) else x
            for x in target_any_paths
        ]
        cmds.select(target_any_paths)

        if _transform.Transform.is_transform_type(target_shape_path):
            target_shape_path = _transform.Transform.get_shape(target_shape_path)

        if node_type == 'airField':
            mel.eval('Air;')
        else:
            raise RuntimeError()
