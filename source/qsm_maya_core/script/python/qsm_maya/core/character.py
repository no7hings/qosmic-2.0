# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class Character(object):
    @classmethod
    def create(cls, name):
        return cmds.character(name=name)

    @classmethod
    def add(cls, name, *args):
        cmds.character(*args, add=name)
