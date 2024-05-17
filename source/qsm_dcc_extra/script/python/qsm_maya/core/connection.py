# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class Connection(object):
    @classmethod
    def create(cls, atr_path_src, atr_path_dst):
        cmds.connectAttr(atr_path_src, atr_path_dst, force=1)
