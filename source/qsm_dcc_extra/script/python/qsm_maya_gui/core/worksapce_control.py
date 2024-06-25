# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core


# class WorkspaceControlOpt(object):
#     @classmethod
#     def _to_qt_instance(cls, ptr, base):
#         # noinspection PyUnresolvedReferences
#         from shiboken2 import wrapInstance
#
#         return wrapInstance(long(ptr), base)
#
#     def __init__(self, name):
#         self._name = name
#
#     def is_exists(self):
#         return cmds.workspaceControl(self._name, exists=True)
#
#     def set_visible(self, boolean):
#         if self.is_exists():
#             cmds.workspaceControl(
#                 self._name,
#                 edit=True,
#                 visible=boolean,
#             )
#
#     def restore(self):
#         cmds.workspaceControl(
#             self._name,
#             edit=True,
#             restore=True,
#         )
#
#     def do_delete(self):
#         if cmds.workspaceControl(self._name, exists=True):
#             cmds.workspaceControl(
#                 self._name,
#                 edit=True,
#                 close=True
#             )
#             #
#             cmds.deleteUI(self._name)
#
#     def set_script(self, script):
#         cmds.workspaceControl(
#             self._name,
#             edit=True,
#             uiScript=script
#         )
#
#     def create(self, width=320, height=320):
#         if self.is_exists():
#             self.restore()
#             # self.set_visible(True)
#         else:
#             cmds.workspaceControl(
#                 self._name,
#                 label=bsc_core.RawStrUnderlineOpt(self._name).to_prettify(capitalize=False),
#                 dockToMainWindow=['right', False],
#                 initialWidth=width, initialHeight=height,
#                 widthProperty='free', heightProperty='free'
#             )
#         return self
#
#     def to_qt_widget(self):
#         # noinspection PyUnresolvedReferences
#         from PySide2 import QtWidgets
#
#         # noinspection PyUnresolvedReferences
#         from maya import OpenMayaUI
#
#         ptr = OpenMayaUI.MQtUtil.findControl(self._name)
#         if ptr is not None:
#             return self._to_qt_instance(
#                 ptr, base=QtWidgets.QWidget
#             )
#
#     def get_qt_layout(self):
#         widget = self.to_qt_widget()
#         if widget is not None:
#             return widget.layout()
#
#     @classmethod
#     def _test(cls):
#         # noinspection PyUnresolvedReferences
#         from maya import cmds, mel, OpenMayaUI
#         # noinspection PyUnresolvedReferences
#         from shiboken2 import wrapInstance, getCppPointer
#         # noinspection PyUnresolvedReferences
#         from PySide2 import QtWidgets
#
#         width, height = 400, 400
#         control_name = 'lynxi_tool'
#         control_label = 'Lynxi Tool'
#         if cmds.workspaceControl(control_name, query=1, exists=1):
#             cmds.workspaceControl(
#                 control_name, edit=1, visible=1, restore=1,
#                 initialWidth=width,
#                 minimumWidth=height
#             )
#         else:
#             LEcomponent = mel.eval(r'getUIComponentDockControl("Channel Box / Layer Editor", false);')
#             cmds.workspaceControl(
#                 control_name,
#                 label=control_label, tabToControl=(LEcomponent, -1),
#                 initialWidth=width, initialHeight=height,
#                 widthProperty='free', heightProperty='free'
#             )
#             parentPtr = OpenMayaUI.MQtUtil.getCurrentParent()
#             parentWidget = wrapInstance(parentPtr, QtWidgets.QWidget)
#             import qsm_gui.proxy.widgets as qsm_gui_prx_widgets
#             p = qsm_gui_prx_widgets.AbsPrxUnitForWorkarea()
#             p.widget.setParent(parentWidget)
#             OpenMayaUI.MQtUtil.addWidgetToMayaLayout(
#                 long(getCppPointer(p.widget)[0]), long(parentPtr)
#             )
#         pass
