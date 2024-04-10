# uncompyle6 version 3.8.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Oct 30 2018, 23:45:53) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Warning: this version of Python has problems handling the Python 3 byte type in constants properly.

# Embedded file name: SuperTools/NetworkMaterials/v1/NetworkMaterialBaseEditor.py
# Compiled at: 2022-08-18 19:44:51
"""
Module containing the base class for NetworkMaterialCreate and
NetworkMaterialEdit parameter editors.
"""
from __future__ import absolute_import
from PyQt5 import QtWidgets
from Katana import UI4
from QT4Panels.DragTabs import DroppableTabBar
from UI4.Widgets import WheelEventIgnoringTabBar

class NMXTabBar(DroppableTabBar, WheelEventIgnoringTabBar):
    """
    Class implementing a droppable tab bar that ignores wheel events, but
    accepts drops.
    """

    def __init__(self, *args, **kwargs):
        DroppableTabBar.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)


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
        self.__frozen = True
        self._node = node
        QtWidgets.QWidget.__init__(self, parent)
        QtWidgets.QVBoxLayout(self)
        mainPanel = QtWidgets.QWidget(self)
        mainPanel.setObjectName('mainPanel')
        QtWidgets.QVBoxLayout(mainPanel)
        self.layout().addWidget(mainPanel)
        self._buildEditorWidgets(mainPanel)

    def showEvent(self, event):
        """
        Event handler for widget show events.

        @type event: C{QtGui.QShowEvent}
        @param event: An object containing details about the widget show event
            to handle.
        """
        QtWidgets.QWidget.showEvent(self, event)
        if self.__frozen:
            self._thaw()

    def hideEvent(self, event):
        """
        Event handler for widget hide events.
        Hide events are sent to widgets immediately after they have been
        hidden.

        @type event: C{QtGui.QHideEvent}
        @param event: An object containing details about the widget hide event
            to handle.
        """
        QtWidgets.QWidget.hideEvent(self, event)
        if not self.__frozen:
            self._freeze()

    def _isFrozen(self):
        """
        @rtype: C{bool}
        @return: C{True} if this editor is currently frozen, meaning that none
            of its event handlers or signal/slot connections are currently
            active, otherwise C{False}.
        """
        return self.__frozen

    def _thaw(self):
        """
        Is called when the editor widget is about to be shown after it was
        previously frozen.

        To be implemented in derived classes in order to register event
        handlers and/or establish signal/slot connections.

        Base class implementation sets the frozen flag.
        """
        self.__frozen = False

    def _freeze(self):
        """
        Is called when the editor widget is about to be hidden after it was
        previously thawed.

        To be implemented in derived classes in order to deregister event
        handlers and/or break signal/slot connections.

        Base class implementation sets the frozen flag.
        """
        self.__frozen = True

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
        tabWidget.setTabBar(NMXTabBar(self))
        tabsPanel.layout().addWidget(QtWidgets.QLabel('Material Interface'))
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

    def _addTab(self, tabWidget, tabName, index=-1):
        """
        Creates an empty widget with layout and adds it to the editor's
        QTabWidget.

        @type tabWidget: C{QtWidgets.QTabWidget}
        @type tabName: C{str}
        @type index: C{int}
        @rtype: C{QtWidgets.QWidget}
        @param tabWidget: The parent widget to which new tabs will be added.
        @param tabName: The text label to give the new tab.
        @param index: Optional position at which to insert the new tab.
        @return: The newly created tab widget.
        """
        tabNameId = tabName.replace(' ', '')
        tab = QtWidgets.QWidget()
        tab.setObjectName('%sPageWidget' % tabNameId)
        tabWidget.insertTab(index, tab, tabName)
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