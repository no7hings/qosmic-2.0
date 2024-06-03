# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class ParentConstraint(object):
    @classmethod
    def create(cls, parent_path, child_path, maintain_offset=0):
        # parentConstraint -mo -weight 1
        return cmds.parentConstraint(parent_path, child_path, maintainOffset=maintain_offset)[0]

    @classmethod
    def get_all(cls, path):
        return list(
            set(
                cmds.listConnections(
                    path, destination=0, source=1, type='parentConstraint'
                ) or []
            )
        )

    @classmethod
    def clear_all(cls, path):
        _ = cls.get_all(path)
        if _:
            for i in _:
                cmds.delete(i)


class ScaleConstraint(object):
    @classmethod
    def create(cls, parent_path, child_path):
        return cmds.scaleConstraint(parent_path, child_path)[0]

    @classmethod
    def get_all(cls, path):
        return list(
            set(
                cmds.listConnections(
                    path, destination=0, source=1, type='scaleConstraint'
                ) or []
            )
        )

    @classmethod
    def clear_all(cls, path):
        _ = cls.get_all(path)
        if _:
            for i in _:
                cmds.delete(i)
