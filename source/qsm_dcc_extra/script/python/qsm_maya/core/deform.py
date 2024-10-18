# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import lxbasic.core as bsc_core

from . import undo as _undo

from . import node as _node

from . import attribute as _attribute

from . import transform as _transform


class NonLinear(object):
    @classmethod
    def create_for(cls, key, target_shape_path, target_any_paths):
        # noinspection PyUnresolvedReferences
        # import maya.internal.common.cmd.base as cmd_base

        cmds.select(target_any_paths)

        if _transform.Transform.is_transform_type(target_shape_path):
            target_shape_path = _transform.Transform.get_shape(target_shape_path)

        mel.eval('{};'.format(key.upper()))
        # cmd_base.executeCommand('{}.cmd_create'.format(key))
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


class BlendShape:

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


class CurveWarp:
    PLUG_NAME = 'curveWarp'

    @classmethod
    def test(cls):
        cls.replace_to(
            'pPlane2', 'pPlane1'
        )
        # cls.replace_node(
        #     'curveWarp1', 'curveWarp2'
        # )

    @classmethod
    def get_args_from(cls, deformed_node):
        args = _transform.Transform.to_shape_args(deformed_node)
        if args:
            transform, shape = args
            shape_type = _node.Node.get_type(shape)
            if shape_type == 'mesh':
                _0 = list(
                    set(
                        cmds.listConnections(
                            shape+'.inMesh', destination=0, source=1, type='curveWarp'
                        ) or []
                    )
                )
            elif shape_type == 'lattice':
                _0 = list(
                    set(
                        cmds.listConnections(
                            shape+'.latticeInput', destination=0, source=1, type='curveWarp'
                        ) or []
                    )
                )
            else:
                return None
            if _0:
                deform_node = _0[0]
                curve = cls.get_curve(deform_node)
                if curve:
                    return deform_node, curve
            return None

    @classmethod
    def get_curve(cls, deform_node, shape=False):
        _ = list(
            set(
                cmds.listConnections(
                    deform_node+'.inputCurve', destination=0, source=1, type='nurbsCurve', shapes=shape
                ) or []
            )
        )
        if _:
            return _[0]

    @classmethod
    def load_plugin(cls):
        cmds.loadPlugin(cls.PLUG_NAME, quiet=1)

    @classmethod
    def create_for(cls, node, curve):
        cls.load_plugin()

        cmds.select([node, curve])
        mel.eval('CurveWarp;')

    @classmethod
    def create_for_lattice(cls, node, curve):
        args = _transform.Transform.to_shape_args(node)
        if args:
            transform, shape = args
            if _node.Node.get_type(shape) == 'lattice':
                scale = list(cmds.getAttr(transform+'.scale')[0])
                lgh = max(scale)

                axis_index = scale.index(lgh)

                cmds.setAttr(transform+'.scale', 1, 1, 1)

                cmds.select([node, curve])
                mel.eval('CurveWarp;')

                args = cls.get_args_from(shape)
                if args:
                    deform_node, curve = args
                    # 1: auto, 2: X, ...
                    cmds.setAttr(deform_node+'.alignmentMode', axis_index+2)
                    cmds.setAttr(deform_node+'.lengthScale', lgh)

    @classmethod
    @_undo.Undo.execute
    def create_for_lattice_0(cls, node, curve):
        cls.create_for_lattice(node, curve)

    @classmethod
    def replace_node(cls, deform_node_src, deform_node_tgt):
        for i_atr_name in [
            'input[0].inputGeometry',
            'input[0].groupId'
        ]:
            i_source_node_0 = _attribute.NodeAttribute.get_source_node(
                deform_node_src, i_atr_name
            )
            if i_source_node_0:
                _node.Node.delete(i_source_node_0)
            i_source_1 = _attribute.NodeAttribute.get_source(
                deform_node_tgt, i_atr_name
            )
            if i_source_1:
                _attribute.NodeAttribute.connect_from(
                    deform_node_src, i_atr_name, i_source_1
                )

        for i_atr_name in [
            'outputGeometry[0]'
        ]:
            _attribute.NodeAttribute.break_targets(
                deform_node_src, i_atr_name
            )
            i_targets_1 = _attribute.NodeAttribute.get_targets(
                deform_node_tgt, i_atr_name
            )
            if i_targets_1:
                i_target_1 = i_targets_1[0]
                i_target_node = i_target_1.split('.')[0]
                i_target_node_type = _node.Node.get_type(i_target_node)
                if i_target_node_type == 'mesh':
                    _attribute.NodeAttribute.connect_to(
                        deform_node_src, i_atr_name, i_target_node+'.inMesh'
                    )
                else:
                    _attribute.NodeAttribute.connect_to(
                        deform_node_src, i_atr_name, i_target_node+'.latticeInput'
                    )

    @classmethod
    @_undo.Undo.execute
    def replace_all(cls, paths):
        path_map = bsc_core.RawTextsMtd.group_elements(
            paths, 2
        )
        for (i_node_0, i_node_1) in path_map:
            cls.replace_to(i_node_0, i_node_1)

    @classmethod
    @_undo.Undo.execute
    def replace_to(cls, node, deformed_node):
        _ = cls.get_args_from(deformed_node)
        if _:
            deform_node_0, curve = _
            cls.create_for(node, curve)
            deform_node_1, curve = cls.get_args_from(node)
            cls.replace_node(deform_node_0, deform_node_1)
