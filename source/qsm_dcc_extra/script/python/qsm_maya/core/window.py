# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core


class Window(object):
    @classmethod
    def create(cls, name, resolution=(480, 320)):
        return cmds.window(
            name, title=bsc_core.RawTextMtd.to_prettify(name),
            width=resolution[0], height=resolution[1],
            minimizeButton=1, maximizeButton=1, sizeable=0
        )

    @classmethod
    def delete(cls, name):
        if cmds.window(name, query=1, exists=1):
            cmds.deleteUI(name, window=1)

    @classmethod
    def create_force(cls, name, resolution=(480, 320)):
        cls.delete(name)
        return cls.create(name, resolution)

    @classmethod
    def show(cls, name):
        cmds.showWindow(name)
