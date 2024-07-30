# coding:utf-8
import re

# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import attribute as _attribute


class ParentConstraint(object):
    @classmethod
    def create(cls, parent_path, child_path, maintain_offset=0):
        # parentConstraint -mo -weight 1
        return cmds.parentConstraint(parent_path, child_path, maintainOffset=maintain_offset)[0]

    @classmethod
    def get_all_from_source(cls, target_node):
        return list(
            set(
                cmds.listConnections(
                    target_node, destination=0, source=1, type='parentConstraint'
                ) or []
            )
        )

    @classmethod
    def clear_all_from_source(cls, target_node):
        _ = cls.get_all_from_source(target_node)
        if _:
            for i in _:
                cmds.delete(i)


class ScaleConstraint(object):
    @classmethod
    def create(cls, parent_path, child_path):
        return cmds.scaleConstraint(parent_path, child_path)[0]

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
    def create(cls, parent_path, child_path):
        return cmds.pointConstraint(parent_path, child_path)[0]

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
    def create(cls, source_node, target_node):
        # orientConstraint -mo -weight 1;
        return cmds.orientConstraint(source_node, target_node)[0]

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
