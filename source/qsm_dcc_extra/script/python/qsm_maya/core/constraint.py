# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class ParentConstraint(object):
    @classmethod
    def create(cls, parent_path, child_path):
        cmds.parentConstraint(parent_path, child_path)
