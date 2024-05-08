# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class DisplayLayer(object):
    @classmethod
    def create(cls, name):
        if cmds.objExists(name) is True:
            return name
        return cmds.createDisplayLayer(name=name, number=1, empty=True)

    @classmethod
    def add_nodes(cls, name, nodes):
        cmds.editDisplayLayerMembers(name, *nodes, noRecurse=1)

    @classmethod
    def set_visible(cls, name, boolean):
        cmds.setAttr(name + '.visibility', boolean)
