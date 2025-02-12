# coding:utf-8
from __future__ import print_function
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.OpenMayaUI as om_ui

import lxgui.qt.core as gui_qt_core


class AttributeEditor(object):
    @classmethod
    def get_current_node(cls):
        ptr = om_ui.MQtUtil.findControl('AttributeEditor')
        ptr = om_ui.MQtUtil.findLayout('MainAttributeEditorLayout')
        _ = gui_qt_core.QtMaya.to_qt_object(ptr)
        if _.isVisible() is True:
            for i in _.children():
                print(i.objectName())
                print(i.children())
