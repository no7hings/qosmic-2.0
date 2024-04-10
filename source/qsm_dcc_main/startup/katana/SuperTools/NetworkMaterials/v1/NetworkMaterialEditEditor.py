# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Nov 16 2020, 22:23:17) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: SuperTools/NetworkMaterials/v1/NetworkMaterialEditEditor.py
# Compiled at: 2021-06-28 21:25:19
"""
Module containing the NetworkMaterialEdit parameter editor class.
"""
from NetworkMaterialBaseEditor import NetworkMaterialBaseEditor
from NetworkMaterialBaseNode import GetNodeFromParam

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

    def _buildTabWidgets(self, tabWidget):
        """
        Creates a tab to expose the parameters for each of the hidden internal
        nodes within the NetworkMaterialEdit.

        @type tabWidget: C{QtWidgets.QWidget}
        @param tabWidget: Parent widget.
        """
        nodeParametersTab = self._addTab(tabWidget, 'Node Parameters')
        networkMaterials = self._node.getNetworkMaterials()
        networkMaterialNode = None
        if len(networkMaterials) > 0:
            networkMaterialNode = networkMaterials[0]
        if networkMaterialNode:
            sceneGraphLocationParam = networkMaterialNode.getParameter('sceneGraphLocation')
            if sceneGraphLocationParam:
                self._addParameterWidget(nodeParametersTab, sceneGraphLocationParam, widget='scenegraphLocation')
        materialEditNode = GetNodeFromParam(self._node, '__node_materialEdit')
        if materialEditNode:
            makeInteractiveParam = materialEditNode.getParameter('makeInteractive')
            if makeInteractiveParam:
                self._addParameterWidget(nodeParametersTab, makeInteractiveParam)
            shadersParameter = materialEditNode.getParameter('shaders.parameters')
            if shadersParameter:
                self._addParameterWidget(nodeParametersTab, shadersParameter)
        nodeParametersTab.layout().addStretch()
        groupStackNode = GetNodeFromParam(self._node, '__node_groupStack')
        if groupStackNode:
            stackInfoParam = groupStackNode.getParameter('__stackInfo')
            if stackInfoParam:
                interfaceTab = self._addTab(tabWidget, 'Interface Controls')
                stackWidget = self._addParameterWidget(interfaceTab, stackInfoParam)
                if stackWidget:
                    stackWidget.selectionChanged.connect(self._on_groupStackSelectionChanged)
        materialInterfaceTab = self._addTab(tabWidget, 'Material Interface')
        if networkMaterialNode:
            interfaceParam = networkMaterialNode.getParameter('publicInterfaceOrder')
            if interfaceParam:
                self._addParameterWidget(materialInterfaceTab, interfaceParam, hideTitle=True)
        materialInterfaceTab.layout().addStretch()
        return