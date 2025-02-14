# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import node as _node


class DisplayLayer:
    @classmethod
    def create(cls, name):
        if cmds.objExists(name) is True:
            return name
        return cmds.createDisplayLayer(name=name, number=1, empty=True)

    @classmethod
    def add_all(cls, name, nodes):
        return cmds.editDisplayLayerMembers(name, *nodes, noRecurse=1)

    @classmethod
    def add_one(cls, name, node):
        return cmds.editDisplayLayerMembers(name, node, noRecurse=1)

    @classmethod
    def set_visible(cls, name, boolean):
        cmds.setAttr(name + '.visibility', boolean)

    @classmethod
    def set_rgb(cls, name, rgb):
        cmds.setAttr(name+'.overrideRGBColors', 1)
        cmds.setAttr(name+'.overrideColorRGB', *rgb)

    @classmethod
    def get_all(cls, name):
        return cmds.editDisplayLayerMembers(name, query=1) or []


class DisplayLayerOpt(_node.NodeOpt):
    def __init__(self, *args, **kwargs):
        super(DisplayLayerOpt, self).__init__(*args, **kwargs)

    def add_all(self, paths):
        return DisplayLayer.add_all(self._name_or_path, paths)

    def add_one(self, path):
        return DisplayLayer.add_all(self._name_or_path, [path])

    def set_visible(self, boolean):
        DisplayLayer.set_visible(self.name_or_path, boolean)
