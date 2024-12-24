# coding:utf-8
import re
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

from . import undo as _undo

from . import attribute as _attribute


class ParentConstraint(object):
    NODE_TYPE = 'parentConstraint'

    @classmethod
    def create(cls, parent_node, child_node, maintain_offset=0):
        # parentConstraint -mo -weight 1
        return cmds.parentConstraint(parent_node, child_node, maintainOffset=maintain_offset)[0]

    @classmethod
    def get_all_from_source(cls, target_node):
        return list(
            set(
                cmds.listConnections(
                    target_node, destination=0, source=1, type=cls.NODE_TYPE
                ) or []
            )
        )

    @classmethod
    def clear_all_from_source(cls, target_node):
        _ = cls.get_all_from_source(target_node)
        if _:
            for i in _:
                cmds.delete(i)

    @classmethod
    def set_source(cls, constraint_node, source_node):
        cs = [
            ('parentMatrix[0]', 'target[0].targetParentMatrix'),
            ('translate', 'target[0].targetTranslate'),
            ('rotatePivot', 'target[0].targetRotatePivot'),
            ('rotatePivotTranslate', 'target[0].targetRotateTranslate'),
            ('rotate', 'target[0].targetRotate'),
            ('rotateOrder', 'target[0].targetRotateOrder'),
            ('scale', 'target[0].targetScale'),
        ]
        for i_src, i_dst in cs:
            i_source, i_target = '{}.{}'.format(source_node, i_src), '{}.{}'.format(constraint_node, i_dst)
            if cmds.isConnected(i_source, i_target) is False:
                cmds.connectAttr(
                    i_source, i_target, force=1
                )


class ParentConstraintSource:

    @classmethod
    def get_constraint_nodes(cls, source):
        return _attribute.NodeAttribute.get_target_nodes(
            source, 'translate', ParentConstraint.NODE_TYPE
        )


class ScaleConstraint(object):
    @classmethod
    def create(cls, parent_node, child_node):
        return cmds.scaleConstraint(parent_node, child_node)[0]

    @classmethod
    def get_all_from_source(cls, target_node):
        return list(
            set(
                cmds.listConnections(
                    target_node, destination=0, source=1, type='scaleConstraint'
                ) or []
            )
        )

    @classmethod
    def clear_all(cls, target_node):
        _ = cls.get_all_from_source(target_node)
        if _:
            for i in _:
                cmds.delete(i)


class PointConstraint(object):
    @classmethod
    def create(cls, parent_node, child_node, maintain_offset=False):
        return cmds.pointConstraint(parent_node, child_node, maintainOffset=maintain_offset)[0]

    @classmethod
    def get_next_index(cls, node):
        connections = _attribute.NodeAttribute.get_all_source_connections(
            node+'.target'
        )
        atr = connections[-1][1]

        # noinspection RegExpRedundantEscape
        result = re.findall(r'.*\.target\[(\d+)\]\..*', atr)
        if result:
            return int(result[0])+1

    @classmethod
    def get_all_from_source(cls, target_node):
        return list(
            set(
                cmds.listConnections(
                    target_node+'.translateX', destination=0, source=1, type='pointConstraint'
                ) or []
            )
        )

    @classmethod
    def get_all_from_target(cls, source_node):
        return list(
            set(
                cmds.listConnections(
                    source_node+'.translate', destination=1, source=0, type='pointConstraint'
                ) or []
            )
        )

    @classmethod
    def get_all_target_nodes(cls, path):
        set_ = set()
        for i in [
            'constraintTranslateX',
            'constraintTranslateY',
            'constraintTranslateZ',
        ]:
            _ = cmds.listConnections(
                path+'.'+i, destination=1, source=0
            ) or []
            set_.update(_)
        return list(set_)


class OrientConstraint(object):
    @classmethod
    def create(cls, source_node, target_node, maintain_offset=False):
        # orientConstraint -mo -weight 1;
        return cmds.orientConstraint(source_node, target_node, maintainOffset=maintain_offset)[0]

    @classmethod
    def get_next_index(cls, node):
        connections = _attribute.NodeAttribute.get_all_source_connections(
            node+'.target'
        )
        atr = connections[-1][1]
        # noinspection RegExpRedundantEscape
        result = re.findall(r'.*\.target\[(\d+)\]\..*', atr)
        if result:
            return int(result[0])+1

    @classmethod
    def get_all_from_source(cls, target_node):
        return list(
            set(
                cmds.listConnections(
                    target_node+'.rotateX', destination=0, source=1, type='orientConstraint'
                ) or []
            )
        )

    @classmethod
    def get_all_from_target(cls, source_node):
        return list(
            set(
                cmds.listConnections(
                    source_node+'.rotate', destination=1, source=0, type='orientConstraint'
                ) or []
            )
        )

    @classmethod
    def get_all_target_nodes(cls, path):
        set_ = set()
        for i in [
            'constraintRotateX',
            'constraintRotateY',
            'constraintRotateZ',
        ]:
            _ = cmds.listConnections(
                path+'.'+i, destination=1, source=0
            ) or []
            set_.update(_)
        return list(set_)


class MotionPath:

    @classmethod
    def get_all(cls, constrained_node):
        # get from source
        return list(
            set(
                cmds.listConnections(
                    constrained_node+'.rotateX', destination=0, source=1, type='motionPath'
                ) or []
            )
        )

    @classmethod
    def get_args_from(cls, constrained_node):
        pass

    @classmethod
    def replace_target(cls, path, target_node):
        axes = ['x', 'y', 'z']

        for i_axis in axes:
            i_atr_0 = '{}Coordinate'.format(i_axis)
            i_add_nodes = cmds.listConnections(
                path+'.'+i_atr_0, destination=1, source=0, type='addDoubleLinear'
            ) or []
            if i_add_nodes:
                i_add_node = i_add_nodes[0]
                # break source first
                _attribute.NodeAttribute.break_source(
                    i_add_node, 'input1'
                )
                _attribute.NodeAttribute.break_targets(
                    i_add_node, 'output'
                )

                # connect target
                _attribute.NodeAttribute.connect_from(
                    i_add_node, 'input1', target_node+'.transMinusRotatePivot{}'.format(i_axis.upper())
                )
                _attribute.NodeAttribute.connect_to(
                    i_add_node, 'output',
                    target_node+'.translate{}'.format(i_axis.upper())
                )

            i_atr_1 = 'rotate{}'.format(i_axis.upper())
            # break target
            _attribute.NodeAttribute.break_targets(
                path, i_atr_1
            )
            # connect target
            _attribute.NodeAttribute.connect_to(
                path, i_atr_1,
                target_node+'.rotate{}'.format(i_axis.upper())
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
    def replace_to(cls, node, constrained_node):
        _ = cls.get_all(
            constrained_node
        )
        if _:
            cls.replace_target(_[0], node)

    @classmethod
    def test(cls):
        _ = cls.get_all(
            'pSphere1'
        )
        if _:
            cls.replace_target(_[0], 'pCube1')
