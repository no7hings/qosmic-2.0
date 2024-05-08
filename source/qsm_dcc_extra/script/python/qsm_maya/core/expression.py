# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class Expression(object):
    @classmethod
    def create(cls, name, script, node):
        if cmds.objExists(name):
            return name

        return cmds.expression(
            name=name,
            string=script,
            object=node,
            alwaysEvaluate=0,
            unitConversion='none'
        )

    @classmethod
    def set_script(cls, name, script):
        cmds.setAttr(
            name+'.expression', script, type='string'
        )
