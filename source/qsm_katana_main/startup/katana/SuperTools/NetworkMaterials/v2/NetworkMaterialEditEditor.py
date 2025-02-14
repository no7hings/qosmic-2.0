# uncompyle6 version 3.8.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Oct 30 2018, 23:45:53) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Warning: this version of Python has problems handling the Python 3 byte type in constants properly.

# Embedded file name: SuperTools/NetworkMaterials/v1/NetworkMaterialEditEditor.py
# Compiled at: 2022-08-18 19:44:51
"""
Module containing the NetworkMaterialEdit parameter editor class.
"""
from __future__ import absolute_import
import QT4FormWidgets, UI4.FormMaster
from .NetworkMaterialBaseEditor import NetworkMaterialBaseEditor
from .NetworkMaterialBaseNode import GetNodeFromParam

class NetworkMaterialEditEditor(NetworkMaterialBaseEditor):
    """
    NetworkMaterialEdit parameter editor UI.
    """

    def __init__(self, parent, node):
        """
        Initializes an instance of this class.

        @type parent: C{QtWidgets.QWidget}
        @type node: C{NodegraphAPI.SuperTool}
        @param parent: Parent widget.
        @param node: NetworkMaterialEdit node to edit.
        """
        NetworkMaterialBaseEditor.__init__(self, parent, node)

    def _buildEditorWidgets(self, mainPanel):
        """
        Creates the main elements of the parameters interface for the node.

        @type mainPanel: C{QtWidgets.QWidget}
        @param mainPanel: Panel to add widgets to.
        """
        pythonGroupPolicy = QT4FormWidgets.PythonGroupPolicy('nme')
        pythonGroupPolicy.getWidgetHints()['hideTitle'] = True
        networkMaterials = self._node.getNetworkMaterials()
        networkMaterialNode = None
        if networkMaterials:
            networkMaterialNode = networkMaterials[0]
        if networkMaterialNode:
            sceneGraphLocationParam = networkMaterialNode.getParameter('sceneGraphLocation')
            if sceneGraphLocationParam:
                childPolicy = UI4.FormMaster.CreateParameterPolicy(None, sceneGraphLocationParam)
                childPolicy.getWidgetHints()['widget'] = 'scenegraphLocation'
                childPolicy.getWidgetHints()['label'] = 'Material Location to Edit'
                pythonGroupPolicy.addChildPolicy(childPolicy)
        factory = UI4.FormMaster.ParameterWidgetFactory
        parameterWidget = factory.buildWidget(self, pythonGroupPolicy)
        mainPanel.layout().addWidget(parameterWidget)
        NetworkMaterialBaseEditor._buildEditorWidgets(self, mainPanel)
        return

    def _buildTabWidgets(self, tabWidget):
        """
        Creates a tab to expose the parameters for each of the hidden internal
        nodes within the NetworkMaterialEdit.

        @type tabWidget: C{QtWidgets.QWidget}
        @param tabWidget: Parent widget.
        """
        defaultsTab = self._addTab(tabWidget, 'Defaults')
        visibilityAndLockingTab = self._addTab(tabWidget, 'Visibility && Locking')
        sourcesAndOrderTab = self._addTab(tabWidget, 'Sources && Order')
        materialEditNode = GetNodeFromParam(self._node, '__node_materialEdit')
        if materialEditNode:
            shadersParameter = materialEditNode.getParameter('shaders.parameters')
            if shadersParameter:
                self._addParameterWidget(defaultsTab, shadersParameter, hideTitle=True)
        defaultsTab.layout().addStretch()
        groupStackNode = GetNodeFromParam(self._node, '__node_groupStack')
        if groupStackNode:
            stackInfoParam = groupStackNode.getParameter('__stackInfo')
            if stackInfoParam:
                stackWidget = self._addParameterWidget(visibilityAndLockingTab, stackInfoParam, hideChildType=True)
                if stackWidget:
                    stackWidget.selectionChanged.connect(self._on_groupStackSelectionChanged)
        networkMaterials = self._node.getNetworkMaterials()
        networkMaterialNode = None
        if networkMaterials:
            networkMaterialNode = networkMaterials[0]
        if networkMaterialNode:
            interfaceParam = networkMaterialNode.getParameter('publicInterfaceOrder')
            if interfaceParam:
                self._addParameterWidget(sourcesAndOrderTab, interfaceParam, hideTitle=True)
        sourcesAndOrderTab.layout().addStretch()
        return