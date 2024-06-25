# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.internal.common.cmd.base as cmd_base

from . import node as _node

from . import attribute as _attribute

from . import transform as _transform


class NonLinear(object):
    @classmethod
    def create_for(cls, key, target_shape_path, target_any_paths):
        cmds.select(target_any_paths)

        if _transform.Transform.is_transform(target_shape_path):
            target_shape_path = _transform.Transform.get_shape(target_shape_path)

        cmd_base.executeCommand('{}.cmd_create'.format(key))
        node = _attribute.NodeAttribute.get_source_node(
            target_shape_path, 'inMesh', 'nonLinear'
        )
        handle_shape = _attribute.NodeAttribute.get_source_node(
            node, 'deformerData', 'deform'+key.capitalize()
        )
        return handle_shape
    
    @classmethod
    def find_any_from(cls, target_shape_path):
        # source
        _ = _attribute.NodeAttribute.get_source_node(
            target_shape_path, 'inMesh'
        )
        if _:
            node_path = _
            node_type = _node.Node.get_type(node_path)
            if node_type == 'nonLinear':
                handle_shape_path = _attribute.NodeAttribute.get_source_node(
                    node_path, 'deformerData'
                )
                if handle_shape_path:
                    return handle_shape_path


class BlendShape(object):

    @classmethod
    def create(cls, transform_path_src, transform_path_tgt, visibility=False):
        nodes = []

        shape_path_src = _transform.Transform.get_shape(transform_path_src)
        name_src = _transform.Transform.to_name(transform_path_src)
        shape_path_tgt = _transform.Transform.get_shape(transform_path_tgt)
        # Debug Source Shape Hide
        cmds.setAttr(shape_path_tgt+'.visibility', 1)
        #
        bls_name = '{}_bls'.format(name_src)
        # Create
        # Must Use "before" Arg
        results = cmds.blendShape(
            shape_path_src, shape_path_tgt,
            name=bls_name,
            weight=(0, 1),
            origin='world',
            before=1
        )
        nodes.extend(results)
        if visibility is True:
            cmds.setAttr(
                transform_path_tgt+'.visibility', cmds.getAttr(transform_path_src+'.visibility')
            )
            cmds.setAttr(
                shape_path_tgt+'.visibility', cmds.getAttr(shape_path_tgt+'.visibility')
            )
        return nodes
