# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ... import core as _mya_core

from ... import motion as _motion


class TransformationLocatorOpt(object):
    LOCATION_PATH = '|__TRANSFORMATION_LOCATOR__'

    def __init__(self, namespaces):
        self._namespace = namespaces

    @classmethod
    def create_location(cls):
        if cmds.objExists(cls.LOCATION_PATH) is False:
            name = cls.LOCATION_PATH.split('|')[-1]
            cmds.createNode(
                'dagContainer', name=name, shared=1, skipSelect=1
            )
            cmds.setAttr(cls.LOCATION_PATH+'.iconName', 'folder-closed.png', type='string')

    @classmethod
    def remove_location(cls):
        if cmds.objExists(cls.LOCATION_PATH) is False:
            cmds.delete(cls.LOCATION_PATH)

    @_mya_core.Undo.execute
    def create_transformation_locators(self):
        self.create_location()

        for i_namespace in self._namespace:
            _motion.AdvMotionOpt(i_namespace).create_transformation_locator(
                location=self.LOCATION_PATH
            )

    @_mya_core.Undo.execute
    def remove_transformation_locators(self):
        for i_namespace in self._namespace:
            _motion.AdvMotionOpt(i_namespace).remove_transformation_locator()
