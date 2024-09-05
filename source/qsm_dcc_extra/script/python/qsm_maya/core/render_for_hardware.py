# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import scene as _scene

from . import render as _render


class HardwareRenderSetup(object):
    @classmethod
    def create_for(cls, texture_enable, light_enable, shadow_enable):
        if _scene.Scene.get_is_ui_mode():
            pass
        else:
            # cmds.setAttr(camera+'.backgroundColor', 0.106, 0.106, 0.106, type='double3')
            _render.RenderSettings.set_renderer('mayaHardware2')
            _render.RenderSettings.open_color_transform()

            cmds.setAttr('hardwareRenderingGlobals.lineAAEnable', 1)
            cmds.setAttr('hardwareRenderingGlobals.multiSampleEnable', 1)
            cmds.setAttr('hardwareRenderingGlobals.ssaoEnable', 1)
            cmds.setAttr('hardwareRenderingGlobals.hwInstancing', 1)
            _render.HardwareRenderSettings.set_render_mode(texture_enable, light_enable, shadow_enable)
            # set filter
            cmds.setAttr(
                'hardwareRenderingGlobals.objectTypeFilterValueArray',
                [0L, 1L, 1L, 1L, 1L, 1L, 1L, 1L, 1L, 1L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L],
                type='Int32Array'
            )
            # gpu
            cmds.setAttr(
                'hardwareRenderingGlobals.pluginObjectTypeFilterValueArray',
                [1L],
                type='Int32Array'
            )
