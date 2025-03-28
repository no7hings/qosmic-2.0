# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxgui.core as gui_core

import qsm_maya.core as qsm_mya_core

import qsm_maya.motion as qsm_mya_motion


class ControlMoveOpt(object):
    ROOT_PATH = '|__CONTROL_MOVE_LOCATOR__'

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

    @qsm_mya_core.Undo.execute
    def create_locators(self):
        self.create_root()

        for i_path in self._main_controls:
            qsm_mya_motion.ControlMove.create_locator_fnc(
                i_path,
                root=self.ROOT_PATH
            )

    @qsm_mya_core.Undo.execute
    def remove_locators(self):
        for i_path in self._main_controls:
            qsm_mya_motion.ControlMove.remove_locator_fnc(i_path)
    
    @classmethod
    def create_auto(cls, **kwargs):
        scheme = kwargs['scheme']
        if scheme == 'default':
            # qsm_mya_core.AnmLayerOpt.switch_to_current_base()

            main_controls = qsm_mya_core.Selection.get_main_controls()
            if not main_controls:
                gui_core.GuiDialog.create(
                    '控制器移动定位器创建',
                    content='选择一个或多个主控制器（必须有移动和旋转属性，如大环）。' if gui_core.GuiUtil.get_language() == 'chs'
                    else 'Select one or more main control.',
                    status=gui_core.GuiDialog.ValidationStatus.Warning,
                    no_label='Close',
                    ok_visible=False, no_visible=True, cancel_visible=False,
                )
                return

            cls(main_controls).create_locators()
    
    @classmethod
    def remove_auto(cls, **kwargs):
        scheme = kwargs['scheme']
        if scheme == 'default':
            # qsm_mya_core.AnmLayerOpt.switch_to_current_base()

            locators = cmds.ls(selection=1, type='locator', dag=1, long=1)
            main_controls = []
            for i_path in locators:
                i_control = qsm_mya_motion.ControlMove.find_main_control(i_path)
                if i_control is not None:
                    main_controls.append(i_control)
            if not main_controls:
                gui_core.GuiDialog.create(
                    '控制器移动定位器移除',
                    content='选择一个或多个定位器（可以选择外面的组）。' if gui_core.GuiUtil.get_language() == 'chs'
                    else 'Select one or more locator (can be select group).',
                    status=gui_core.GuiDialog.ValidationStatus.Warning,
                    no_label='Close',
                    ok_visible=False, no_visible=True, cancel_visible=False,
                )

            cls(main_controls).remove_locators()
