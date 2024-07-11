# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ... import core as _mya_core

from ...motion import core as _mtn_core


class AdvTransformationLocatorOpt(object):
    ROOT_PATH = '|__TRANSFORMATION_LOCATOR__'

    def __init__(self, namespaces):
        self._namespaces = namespaces

    @classmethod
    def create_root(cls):
        if cmds.objExists(cls.ROOT_PATH) is False:
            name = cls.ROOT_PATH.split('|')[-1]
            cmds.createNode(
                'dagContainer', name=name, shared=1, skipSelect=1
            )
            cmds.setAttr(cls.ROOT_PATH+'.iconName', 'folder-closed.png', type='string')

    @classmethod
    def remove_root(cls):
        if cmds.objExists(cls.ROOT_PATH) is False:
            cmds.delete(cls.ROOT_PATH)

    @_mya_core.Undo.execute
    def create_transformation_locators(self):
        self.create_root()

        for i_namespace in self._namespaces:
            _mtn_core.AdvRigMotionOpt(i_namespace).create_transformation_locator(
                root=self.ROOT_PATH
            )

    @_mya_core.Undo.execute
    def remove_transformation_locators(self):
        for i_namespace in self._namespaces:
            _mtn_core.AdvRigMotionOpt(i_namespace).remove_transformation_locator()


class ControlTransformationLocator(object):
    ROOT_PATH = '|__TRANSFORMATION_LOCATOR__'

    def __init__(self, main_controls):
        self._main_controls = main_controls

    @classmethod
    def create_root(cls):
        if cmds.objExists(cls.ROOT_PATH) is False:
            name = cls.ROOT_PATH.split('|')[-1]
            cmds.createNode(
                'dagContainer', name=name, shared=1, skipSelect=1
            )
            cmds.setAttr(cls.ROOT_PATH+'.iconName', 'folder-closed.png', type='string')

    @classmethod
    def remove_root(cls):
        if cmds.objExists(cls.ROOT_PATH) is False:
            cmds.delete(cls.ROOT_PATH)

    @_mya_core.Undo.execute
    def create_transformation_locators(self):
        self.create_root()

        for i_path in self._main_controls:
            _mtn_core.AdvRigMotionOpt.create_transformation_locator_fnc(
                i_path,
                root=self.ROOT_PATH
            )

    @_mya_core.Undo.execute
    def remove_transformation_locators(self):
        for i_path in self._main_controls:
            _mtn_core.AdvRigMotionOpt.remove_transformation_locator_fnc(i_path)
