# coding:utf-8
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class ViewPanel(object):
    @classmethod
    def _set_viewport_shader_display_mode_(cls, name):
        cmds.modelEditor(
            name,
            edit=1,
            useDefaultMaterial=0,
            displayAppearance='smoothShaded',
            displayTextures=0,
            displayLights='default',
            shadows=0
        )

    @classmethod
    def _set_viewport_texture_display_mode_(cls, name):
        cmds.modelEditor(
            name,
            edit=1,
            useDefaultMaterial=0,
            displayAppearance='smoothShaded',
            displayTextures=1,
            displayLights='default',
            shadows=0
        )

    @classmethod
    def _set_viewport_light_display_mode_(cls, name):
        cmds.modelEditor(
            name,
            edit=1,
            useDefaultMaterial=0,
            displayAppearance='smoothShaded',
            displayTextures=1,
            displayLights='all',
            shadows=1
        )

    @classmethod
    def set_render_mode(cls, name, texture_enable=True, light_enable=True, shadow_enable=True):
        cmds.modelEditor(
            name,
            edit=1,
            useDefaultMaterial=0,
            displayAppearance='smoothShaded',
            displayTextures=texture_enable,
            displayLights='all' if light_enable is True else 'default',
            shadows=shadow_enable
        )

    @classmethod
    def set_display_mode(cls, name, display_mode):
        if display_mode == 5:
            cls._set_viewport_shader_display_mode_(name)
        elif display_mode == 6:
            cls._set_viewport_texture_display_mode_(name)
        elif display_mode == 7:
            cls._set_viewport_light_display_mode_(name)


class ViewPanels(object):
    @classmethod
    def get_all_names(cls):
        return cmds.getPanel(typ='modelPanel')

    @classmethod
    def get_current_name(cls):
        return cmds.paneLayout('viewPanes', q=True, pane1=True)

    @classmethod
    def isolate_select(cls, boolean):
        for i in cls.get_all_names():
            cmds.isolateSelect(i, state=boolean)

    @classmethod
    def isolate_select_for(cls, paths, boolean):
        for i in cls.get_all_names():
            cmds.isolateSelect(i, state=boolean)
            for j in paths:
                cmds.isolateSelect(i, addDagObject=j)


class ViewPanelIsolateSelectOpt(object):
    def __init__(self, panel_name='modelPanel4'):
        self._panel_name = panel_name

    def set_enable(self, boolean):
        cmds.isolateSelect(self._panel_name, state=boolean)

    def is_enable(self):
        return cmds.isolateSelect(self._panel_name, state=1, query=1)

    def add_node(self, path):
        cmds.isolateSelect(self._panel_name, addDagObject=path)

    def add_nodes(self, paths):
        [self.add_node(i) for i in paths]

    def remove_node(self, path):
        cmds.isolateSelect(self._panel_name, removeDagObject=path)

    def remove_nodes(self, paths):
        [self.remove_node(i) for i in paths]