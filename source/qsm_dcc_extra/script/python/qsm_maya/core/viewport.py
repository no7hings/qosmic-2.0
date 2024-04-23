# coding:utf-8
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class ViewPanels(object):
    @classmethod
    def get_all_names(cls):
        return cmds.getPanel(typ='modelPanel')

    @classmethod
    def get_current_name(cls):
        return cmds.paneLayout('viewPanes', q=True, pane1=True)


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