# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class ControlKey:
    @classmethod
    def find_one_control_fnc(cls, control_key, namespace):
        if namespace:
            _ = cmds.ls('{}:{}'.format(namespace, control_key), long=1)
            if _:
                return _[0]
        else:
            _ = cmds.ls(control_key, long=1)
            if _:
                return _[0]
