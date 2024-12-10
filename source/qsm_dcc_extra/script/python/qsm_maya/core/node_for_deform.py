# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import lxbasic.core as bsc_core

from . import undo as _undo

from . import node as _node

from . import attribute as _attribute

from . import node_for_transform as _node_for_transform

from . import shape as _node_for_shape


class NonLinear(object):
    KEY_MAPPER = dict(
        deformBend='bend',
        deformFlare='flare',
        deformSine='sine',
        deformSquash='squash',
        deformTwist='twist',
        deformWave='wave',
    )

    @classmethod
    def get_all_node_types(cls):
        return cls.KEY_MAPPER.keys()

    @classmethod
    def create_for(cls, key, target_shape_path, target_any_paths):
        # noinspection PyUnresolvedReferences
        # import maya.internal.common.cmd.base as cmd_base

        cmds.select(target_any_paths)

        if _node_for_transform.Transform.is_transform_type(target_shape_path):
            target_shape_path = _node_for_transform.Transform.get_shape(target_shape_path)

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

    @classmethod
    def is_valid(cls, transform_path):
        history = cmds.listHistory(transform_path)
        _ = cmds.ls(history, type=cls.get_all_node_types()) or []
        if _:
            return True
        return False


class BlendShape:

    @classmethod
    def create(cls, transform_path_src, transform_path_tgt, visibility=False):
        nodes = []

        shape_path_src = _node_for_transform.Transform.get_shape(transform_path_src)
        name_src = _node_for_transform.Transform.to_name_without_namespace(transform_path_src)
        shape_path_tgt = _node_for_transform.Transform.get_shape(transform_path_tgt)
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


class MeshBlend:
    @classmethod
    def get_target_shapes(cls, deform_node):
        return _attribute.NodeAttribute.get_target_nodes(
            deform_node, 'outputGeometry', 'mesh'
        )

    @classmethod
    def get_target_transforms(cls, deform_node):
        return [
            _node_for_shape.Shape.get_transform(x) for x in cls.get_target_shapes(deform_node)
        ]

    @classmethod
    def set_source_transform(cls, deform_node, transform_path):
        shape_path = _node_for_transform.Transform.get_shape(transform_path)
        source = '{}.worldMesh[0]'.format(shape_path)
        target = '{}.inputTarget[0].inputTargetGroup[0].inputTargetItem[6000].inputGeomTarget'.format(deform_node)
        if cmds.isConnected(source, target) is False:
            cmds.connectAttr(source, target, force=1)


class MeshBlendSource:
    @classmethod
    def get_target_args_map(cls, transform_path):
        dict_ = {}
        nodes = cls.get_deform_nodes(transform_path)
        if nodes:
            for i_node in nodes:
                i_target_transforms = MeshBlend.get_target_transforms(
                    i_node
                )
                if i_target_transforms:
                    dict_[i_node] = i_target_transforms
        return dict_

    @classmethod
    def get_deform_nodes(cls, transform_path):
        shape_path = _node_for_transform.Transform.get_shape(transform_path)
        return _attribute.NodeAttribute.get_target_nodes(
            shape_path, 'worldMesh', 'blendShape'
        )

    @classmethod
    def get_deform_connection(cls, transform_path):
        pass

    @classmethod
    def get_all_target_transforms(cls, transform_path):
        set_ = set()
        nodes = cls.get_deform_nodes(transform_path)
        if nodes:
            for i_node in nodes:
                i_target_transforms = MeshBlend.get_target_transforms(
                    i_node
                )
                if i_target_transforms:
                    set_.update(set(i_target_transforms))
        return list(set_)


class MeshBlendTarget:

    @classmethod
    def get_args(cls, transform_path):
        node = cls.get_deform_node(transform_path)
        if node:
            pass

    @classmethod
    def get_deform_node(cls, transform_path):
        pass


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
        args = _node_for_transform.Transform.to_shape_args(deformed_node)
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
        args = _node_for_transform.Transform.to_shape_args(node)
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
        path_map = bsc_core.BscTexts.group_elements(
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


class Wrap:
    NODE_TYPE = 'wrap'

    @classmethod
    def get_driver_transforms(cls, node):
        list_ = []
        array_indices = _attribute.NodeAttribute.get_array_indices(node, 'driverPoints')
        for i in array_indices:
            i_shape = _attribute.NodeAttribute.get_source_node(
                node, 'driverPoints[{}]'.format(i), shapes=1
            )
            i_transform = _node_for_shape.Shape.get_transform(i_shape)
            list_.append(i_transform)
        return list_

    @classmethod
    def get_base_transforms(cls, node):
        list_ = []
        array_indices = _attribute.NodeAttribute.get_array_indices(node, 'basePoints')
        for i in array_indices:
            i_shape = _attribute.NodeAttribute.get_source_node(
                node, 'basePoints[{}]'.format(i), shapes=1
            )
            i_transform = _node_for_shape.Shape.get_transform(i_shape)
            list_.append(i_transform)
        return list_
    

class MeshWrap:
    @classmethod
    def get_driver_transforms(cls, deform_node):
        return Wrap.get_driver_transforms(deform_node)

    @classmethod
    def get_base_transforms(cls, deform_node):
        return Wrap.get_base_transforms(deform_node)

    @classmethod
    def get_target_shapes(cls, deform_node):
        return _attribute.NodeAttribute.get_target_nodes(
            deform_node, 'outputGeometry', 'mesh'
        )

    @classmethod
    def get_target_transforms(cls, deform_node):
        return [
            _node_for_shape.Shape.get_transform(x) for x in cls.get_target_shapes(deform_node)
        ]


class MeshWrapSource:
    @classmethod
    def get_target_args_map(cls, transform_path):
        dict_ = {}
        nodes = cls.get_deform_nodes(transform_path)
        if nodes:
            for i_node in nodes:
                i_target_transforms = MeshWrap.get_target_transforms(
                    i_node
                )
                if i_target_transforms:
                    dict_[i_node] = i_target_transforms
        return dict_

    @classmethod
    def get_base_transforms(cls, transform_path):
        deform_nodes = cls.get_deform_nodes(transform_path)
        set_ = set()
        [set_.update(set(Wrap.get_base_transforms(x))) for x in deform_nodes]
        return list(set_)

    @classmethod
    def get_deform_nodes(cls, transform_path):
        shape_path = _node_for_transform.Transform.get_shape(transform_path)
        return _attribute.NodeAttribute.get_target_nodes(
            shape_path, 'worldMesh', Wrap.NODE_TYPE
        )

    @classmethod
    def auto_collect_base_transforms(cls, transform_path):
        base_transforms = cls.get_base_transforms(transform_path)
        if base_transforms:
            parent_path = _node_for_transform.Transform.get_parent(transform_path)
            for i_base_transform in base_transforms:
                i_parent_path = _node_for_transform.Transform.get_parent(i_base_transform)
                if i_parent_path != parent_path:
                    i_base_transform = _node_for_transform.Transform.parent_to(
                        i_base_transform, parent_path
                    )

                i_name = _node_for_transform.Transform.to_name_without_namespace(transform_path)
                i_name_new = '{}Base'.format(i_name)
                _node_for_transform.Transform.rename(i_base_transform, i_name_new)

    @classmethod
    def get_all_target_transforms(cls, transform_path):
        set_ = set()
        nodes = cls.get_deform_nodes(transform_path)
        if nodes:
            for i_node in nodes:
                i_target_transforms = MeshWrap.get_target_transforms(
                    i_node
                )
                if i_target_transforms:
                    set_.update(set(i_target_transforms))
        return list(set_)
    

class MeshWrapTarget:
    @classmethod
    def get_args(cls, transform_path):
        node = cls.get_deform_node(transform_path)
        if node:
            return node, Wrap.get_driver_transforms(node), Wrap.get_base_transforms(node)

    @classmethod
    def get_deform_node(cls, transform_path):
        shape_path = _node_for_transform.Transform.get_shape(transform_path)
        return _attribute.NodeAttribute.get_source_node(
            shape_path, 'inMesh', Wrap.NODE_TYPE
        )


class MeshDeform:
    @classmethod
    def break_deform(cls, transform_path):
        shape_path = _node_for_transform.Transform.get_shape(transform_path)
        _attribute.NodeAttribute.break_source(shape_path, 'inMesh')

    @classmethod
    def is_valid(cls, transform_path):
        shape = _node_for_transform.Transform.get_shape(transform_path)
        history = cmds.listHistory(shape)
        _ = cmds.ls(history, type=NonLinear.get_all_node_types()) or []
        if _:
            return True
        return False
