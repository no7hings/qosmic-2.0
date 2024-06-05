# coding:utf-8
from PySidd2 import QtWidgets

import shiboken2

import maya.cmds as cmds

import maya.mel as mel

import maya.OpenMayaUI as mui

import qsm_maya_gui


class TestWidget(QtWidgets.QTreeWidget):
    def __init__(self, *args, **kwargs):
        super(TestWidget, self).__init__(*args, **kwargs)

        qsm_maya_gui.WORKAREA = self

    def refresh(self, *args, **kwargs):
        pass

    def detachMe(self, *args, **kwargs):
        pass


def createDescriptionEditor(showIt=True):
    """Create a description editor."""

    if qsm_maya_gui.WORKAREA is None:
        cmds.waitCursor(state=1)

        TestWidget()
        # delete the previous dock control if there is one
        if cmds.dockControl("XGenDockableWidget", q=True, ex=True):
            cmds.deleteUI("XGenDockableWidget")

        # to set it up in Maya as a panel,  it'll need an object name
        descui = qsm_maya_gui.WORKAREA
        descui.setObjectName("XGenDescriptionEditor")

        cmds.waitCursor(state=0)

    if showIt:
        # show it in the dock
        # if the user hit the close button, it actually only hides the widget, so we both raise it and make sure it's visible.
        if cmds.workspaceControl('XGenDockableWidget', q=True, ex=True):
            cmds.workspaceControl('XGenDockableWidget', e=True, vis=True, r=True)
        else:
            LEcomponent = mel.eval('getUIComponentDockControl("Channel Box / Layer Editor", false);')
            cmds.workspaceControl('XGenDockableWidget',
                                  requiredPlugin='xgenToolkit',
                                  tabToControl=(LEcomponent, -1),
								  initialWidth=cmds.optionVar( q='workspacesWidePanelInitialWidth' ),
								  minimumWidth=cmds.optionVar( q='workspacesWidePanelInitialWidth' ),
                                  label='test',
                                  uiScript='''import maya.cmds as xguibootstrap
if not xguibootstrap.pluginInfo('xgenToolkit', q=True, loaded=True):
    xguibootstrap.loadPlugin('xgenToolkit')
del xguibootstrap
xgui.createDockControl()''')
            cmds.workspaceControl('XGenDockableWidget', e=True, r=True)

    return qsm_maya_gui.WORKAREA


def createDockControl():
    ''' Add the Description Editor widget to Maya workspace control '''
    if qsm_maya_gui.WORKAREA is None:
        # Create the Description Editor if not exists
        cmds.waitCursor(state=1)
        TestWidget()
        descui = qsm_maya_gui.WORKAREA
        descui.setObjectName("XGenDescriptionEditor")
        cmds.waitCursor(state=0)

    if qsm_maya_gui.MAYA and qsm_maya_gui.WORKAREA:
        # Get the layout of the parent workspace control and Description Editor widget
        parent = mui.MQtUtil.getCurrentParent()
        widget = mui.MQtUtil.findControl('XGenDescriptionEditor')

        # Add the Description Editor to workspace control layout
        mui.MQtUtil.addWidgetToMayaLayout(long(widget), long(parent))
        qsm_maya_gui.WORKAREA.refresh("Full")

        # Maya workspace control should never delete its content widget when
        # retain flag is true. But it still deletes in certain cases. We avoid
        # deleting the global widget by removing it from its parent's children.
        # destroyed signal is emitted right before deleting children.
        parentWidget = shiboken2.wrapInstance(long(parent), QtWidgets.QWidget)
        if parentWidget:
            parentWidget.destroyed.connect(qsm_maya_gui.WORKAREA.detachMe)


def main(session):
    import lxgui.qt.core as gui_qt_core

    import lxgui.proxy.widgets as gui_prx_widgets

    import qsm_maya_gui.core as qsm_mya_gui_core

    import qsm_maya_tool.workarea.gui.widgets as qsm_wka_gui_widgets



if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
