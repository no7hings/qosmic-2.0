# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Nov 16 2020, 22:23:17) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: SuperTools/NetworkMaterials/v1/NetworkMaterialBaseEditor.py
# Compiled at: 2021-06-28 21:25:19
"""
Module containing the base class for NetworkMaterialCreate and
NetworkMaterialEdit parameter editors.
"""
from Katana import QtWidgets, UI4, NodegraphAPI

class NetworkMaterialBaseEditor(QtWidgets.QWidget):
    """
    NetworkMaterialBase SuperTool parameter editor.
    """

    def __init__(self, parent, node):
        """
        Initializes an instance of this class.

        @type parent: C{QtWidgets.QWidget}
        @type node: C{NodegraphAPI.SuperTool}
        @param parent: Parent widget.
        @param node: NetworkMaterialCreate node.
        """
        self._node = node
        QtWidgets.QWidget.__init__(self, parent)
        QtWidgets.QVBoxLayout(self)
        mainPanel = QtWidgets.QWidget(self)
        mainPanel.setObjectName('mainPanel')
        QtWidgets.QVBoxLayout(mainPanel)
        self.layout().addWidget(mainPanel)
        self._buildEditorWidgets(mainPanel)

    def _buildEditorWidgets(self, mainPanel):
        """
        Creates the main elements of the parameters interface for the node.

        @type mainPanel: C{QtWidgets.QWidget}
        @param mainPanel: Panel to add the editor widgets to.
        """
        tabsPanel = QtWidgets.QWidget(self)
        QtWidgets.QVBoxLayout(tabsPanel)
        mainPanel.layout().addWidget(tabsPanel)
        tabWidget = QtWidgets.QTabWidget(tabsPanel)
        tabWidget.setObjectName('tabWidget')
        tabWidget.setTabBar(UI4.Widgets.WheelEventIgnoringTabBar())
        tabsPanel.layout().addWidget(tabWidget)
        self._buildTabWidgets(tabWidget)

    def _buildTabWidgets(self, tabWidget):
        """
        Populates the tabWidget with pages and contents to expose
        the parameters for each of the hidden internal nodes within
        the NetworkMaterialBaseNode.

        Base class implementation does nothing.

        @type tabWidget: C{QtWidgets.QTabWidget}
        @param tabWidget: The tab widget on which to add new pages
            and contents.
        """
        pass

    def _populateNodeTabWidget(self, tab, node, omit=None):
        """
        For a given tab name and parameter, creates a standard parameter
        widget for each of the referenced node's own parameters.

        @type tab: C{QtWidgets.QWidget}
        @type node: C{NodegraphAPI.Node}
        @type omit: C{list} of C{str} or C{None}
        @param tab: The tab on which to add the parameter widgets.
        @param node: The node whose parameters will be used to create widgets.
        @param omit: The names of any parameters which are not required to be
            exposed.
        """
        if omit is None:
            omit = []
        nodeRootParam = node.getParameters()
        for nodeParam in nodeRootParam.getChildren():
            if nodeParam.getName() in omit:
                continue
            self._addParameterWidget(tab, nodeParam)

        return

    def _addParameterWidget(self, parent, parameter, **hints):
        """
        Adds a new widget to the parent widget for the given parameter.

        @type parent: C{QtWidgets.QWidget}
        @type parameter: C{NodegraphAPI.Parameter}
        @rtype: C{QtWidgets.QWidget} or C{None}
        @param parent: The widget on which to add the parameter widgets.
        @param parameter: The parameter for which to create a widget.
        @param hints: Addtional keyword widgets hints to customize
            the created widget.
        @return: The created widget or None if the parameter node is marked
            for deletion.
        """
        node = parameter.getNode()
        if node and node.isMarkedForDeletion():
            return
        else:
            paramPolicy = UI4.FormMaster.CreateParameterPolicy(None, parameter)
            for key, value in hints.items():
                paramPolicy.getWidgetHints()[key] = value

            factory = UI4.FormMaster.ParameterWidgetFactory
            parameterWidget = factory.buildWidget(self, paramPolicy)
            parent.layout().addWidget(parameterWidget)
            return parameterWidget

    def _addTab(self, tabWidget, tabName):
        """
        Creates an empty widget with layout and adds it to the editor's
        QTabWidget.

        @type tabWidget: C{QtWidgets.QTabWidget}
        @type tabName: C{str}
        @rtype: C{QtWidgets.QWidget}
        @param tabWidget: The parent widget to which new tabs will be added.
        @param tabName: The text label to give the new tab.
        @return: The newly created tab widget.
        """
        tabNameId = tabName.replace(' ', '')
        tab = QtWidgets.QWidget()
        tab.setObjectName('%sPageWidget' % tabNameId)
        tabWidget.addTab(tab, tabName)
        vBoxLayout = QtWidgets.QVBoxLayout()
        vBoxLayout.setObjectName('%sLayout' % tabNameId)
        tab.setLayout(vBoxLayout)
        return tab

    def _on_groupStackSelectionChanged(self, nodeParameterWidgets):
        """
        Event handler for C{'selectionChanged'} events on the internal
        GroupStack node's list stack widget.

        Used to hide the B{materialLocation} parameter widget for any contained
        NetworkMaterialInterfaceControls nodes.

        @type nodeParameterWidgets: C{list} of C{QtWidgets.QWidget}
        @param nodeParameterWidgets: List of parameter widgets to hide.
        """
        for nodeParameterWidget in nodeParameterWidgets:
            materialLocationWidget = nodeParameterWidget.getFormWidgetChild('materialLocation')
            if materialLocationWidget:
                materialLocationWidget.hide()

    def _isNodeChildNetworkMaterial(self, node, nodeParent=None):
        """
        Whether given node is a direct child NetworkMaterial of the
        NetworkMaterialCreate.

        @type node: C{NodegraphAPI.Node}
        @type nodeParent: C{NodegraphAPI.Node} or C{None}
        @rtype: C{bool}
        @param node: Node to check.
        @param nodeParent: Optionally supply node's parent.
        @return: C{True} if C{node} is a child NetworkMaterial, C{False}
            otherwise.
        """
        if not node:
            return False
        if not nodeParent:
            nodeParent = node.getParent()
        if nodeParent is self._node and node.getType() == 'NetworkMaterial':
            return True
        return False

    def _isNodeChildNamespace(self, node, nodeParent=None):
        """
        Whether given node is a direct child LocationCreate namespace of the
        NetworkMaterialCreate.

        @type node: C{NodegraphAPI.Node}
        @type nodeParent: C{NodegraphAPI.Node} or C{None}
        @rtype: C{bool}
        @param node: Node to check.
        @param nodeParent: Optionally supply node's parent.
        @return: C{True} if C{node} is a child LocationCreate, C{False}
            otherwise.
        """
        if not node:
            return False
        if not nodeParent:
            nodeParent = node.getParent()
        if nodeParent is self._node and node.getType() == 'LocationCreate' and node.getParameter('namespaceName'):
            return True
        return False