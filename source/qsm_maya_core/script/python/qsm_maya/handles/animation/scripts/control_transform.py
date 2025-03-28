# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxgui.core as gui_core

import qsm_maya.core as qsm_mya_core

import qsm_maya.motion as qsm_mya_motion


class ControlTransformOpt(object):
    ROOT_PATH = '|__CONTROL_TRANSFORM_LOCATOR__'

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

    @classmethod
    @qsm_mya_core.Undo.execute
    def create_locators(cls, main_controls):
        cls.create_root()

        for i_main_control in main_controls:
            qsm_mya_motion.ControlTransform.create_locator_fnc(
                i_main_control,
                root=cls.ROOT_PATH
            )

    @classmethod
    @qsm_mya_core.Undo.execute
    def remove_locators(cls, main_locators):
        for i_main_locator in main_locators:
            qsm_mya_motion.ControlTransform.remove_locator_fnc(i_main_locator)

    @classmethod
    def create_auto(cls, **kwargs):
        scheme = kwargs['scheme']
        if scheme == 'default':
            # qsm_mya_core.AnmLayerOpt.switch_to_current_base()

            main_controls = qsm_mya_core.Selection.get_main_controls()
            if not main_controls:
                gui_core.GuiDialog.create(
                    '控制器变换定位器创建',
                    content='选择一个或多个主控制器。' if gui_core.GuiUtil.get_language() == 'chs'
                    else 'Select one or more main control.',
                    status=gui_core.GuiDialog.ValidationStatus.Warning,
                    no_label='Close',
                    ok_visible=False, no_visible=True, cancel_visible=False,
                )
                return

            cls.create_locators(main_controls)

    @classmethod
    def remove_auto(cls, **kwargs):
        scheme = kwargs['scheme']
        if scheme == 'default':
            # qsm_mya_core.AnmLayerOpt.switch_to_current_base()

            locator_shapes = cmds.ls(selection=1, type='locator', dag=1, long=1)
            main_locators = []
            for i_locator_shape in locator_shapes:
                i_main_locator = qsm_mya_core.Shape.get_transform(i_locator_shape)
                if i_main_locator is not None:
                    main_locators.append(i_main_locator)

            if not main_locators:
                gui_core.GuiDialog.create(
                    '控制器变换定位器移除',
                    content='选择一个或多个定位器（可以选择外面的组）。' if gui_core.GuiUtil.get_language() == 'chs'
                    else 'Select one or more locator (can be select group).',
                    status=gui_core.GuiDialog.ValidationStatus.Warning,
                    no_label='Close',
                    ok_visible=False, no_visible=True, cancel_visible=False,
                )

            cls.remove_locators(main_locators)
