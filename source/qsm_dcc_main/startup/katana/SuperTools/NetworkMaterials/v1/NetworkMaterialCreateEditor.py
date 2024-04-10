# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Nov 16 2020, 22:23:17) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: SuperTools/NetworkMaterials/v1/NetworkMaterialCreateEditor.py
# Compiled at: 2021-06-28 21:25:19
"""
Module containing the NetworkMaterialCreate parameter editor class.
"""
import collections, logging, DrawingModule, RenderingAPI
from UI4.FormMaster import ParameterPolicy, KatanaFactory, NodeMimeData
from UI4.Util.Events import debounce
from UI4.Widgets import NodeColorsMenu
from NetworkMaterialBaseEditor import NetworkMaterialBaseEditor
from NetworkMaterialBaseNode import GetNodeFromParam
from NetworkMaterialCreateNode import MaterialLocation
from SceneGraphLocationListener import LeafSceneGraphLocationListener
from Katana import enum, ResourceFiles, NodegraphAPI, Utils, QtCore, QtGui, QtWidgets, QT4Widgets, UI4
log = logging.getLogger('NetworkMaterialCreate.Editor')

class NetworkMaterialCreateEditor(NetworkMaterialBaseEditor):
    """
    NetworkMaterialCreate parameter editor UI.
    """

    def __init__(self, parent, node):
        """
        Initializes an instance of this class.

        @type parent: C{QtWidgets.QWidget}
        @type node: C{NodegraphAPI.SuperTool}
        @param parent: Parent widget.
        @param node: NetworkMaterialCreate node to edit.
        """
        self.__treeWidget = None
        self.__selectedNodeInTabWidget = None
        NetworkMaterialBaseEditor.__init__(self, parent, node)
        Utils.EventModule.RegisterEventHandler(self.__on_nm_create, eventType='nodegraph_nmc_nm_create', eventID=hash(node))
        Utils.EventModule.RegisterEventHandler(self.__on_nm_delete, eventType='nodegraph_nmc_nm_delete', eventID=hash(node))
        Utils.EventModule.RegisterEventHandler(self.__on_namespace_create, eventType='nodegraph_nmc_namespace_create', eventID=hash(node))
        Utils.EventModule.RegisterEventHandler(self.__on_namespace_delete, eventType='nodegraph_nmc_namespace_delete', eventID=hash(node))
        return

    def _buildEditorWidgets(self, mainPanel):
        """
        Creates the main elements of the parameters interface for the node.

        @type mainPanel: C{QtWidgets.QWidget}
        @param mainPanel: Panel to add widgets to.
        """
        prefixParam = self._node.getParameter('rootLocation')
        if prefixParam:
            self._addParameterWidget(mainPanel, prefixParam)
        self.__buildNMAddButton(mainPanel)
        self.__treeWidget = _TreeWidget(self._node, mainPanel)
        self.__treeWidget.itemSelectionChanged.connect(self.__on_treeWidget_selectionChanged)
        mainPanel.layout().addWidget(self.__treeWidget)
        mainPanel.layout().addWidget(UI4.Widgets.VBoxLayoutResizer(self.__treeWidget, 160, 128))
        NetworkMaterialBaseEditor._buildEditorWidgets(self, mainPanel)
        self.__populateTreeWidget()

    def __buildNMAddButton(self, mainPanel):
        """
        Create "+" button to add NetworkMaterials and LocationCreate
        namespaces.

        @type mainPanel: C{QtWidgets.QWidget}
        @param mainPanel: Panel to add button to.
        """
        toolbarLayout = QtWidgets.QHBoxLayout()
        mainPanel.layout().addLayout(toolbarLayout)
        nmAddButton = _AddNetworkMaterialButton(self, self._node)
        toolbarLayout.addWidget(nmAddButton)
        toolbarLayout.addStretch()

    def __populateTreeWidget(self):
        """
        Construct the tree widget and start listening to relevant events on
        internal nodes.
        """
        nodes = self._node.getMaterialLocationNodesInMergeOrder()
        for node in nodes:
            self.__watchNode(node)

        self.__treeWidget.populate(nodes)
        self.__treeWidget.collapseAll()

    def __watchNode(self, node):
        """
        Listen for relevant events on given node.

        @type node: C{NodegraphAPI.Node}
        @param node: Node to listen out for.
        """
        if Utils.EventModule.IsHandlerRegistered(self.__on_parameter_finalizeValue, eventType='parameter_finalizeValue', eventID=hash(node)):
            return
        Utils.EventModule.RegisterEventHandler(self.__on_parameter_finalizeValue, eventType='parameter_finalizeValue', eventID=hash(node))
        if node.getType() == 'NetworkMaterial':
            Utils.EventModule.RegisterEventHandler(self.__on_node_bypassed, eventType='node_setBypassed', eventID=hash(node))

    def __unwatchNode(self, node):
        """
        Stop listening for relevant events on given node.

        @type node: C{NodegraphAPI.Node}
        @param node: Node to stop listening out for.
        """
        if not Utils.EventModule.IsHandlerRegistered(self.__on_parameter_finalizeValue, eventType='parameter_finalizeValue', eventID=hash(node)):
            return
        Utils.EventModule.UnregisterEventHandler(self.__on_parameter_finalizeValue, eventType='parameter_finalizeValue', eventID=hash(node))
        if node.getType() == 'NetworkMaterial':
            Utils.EventModule.UnregisterEventHandler(self.__on_node_bypassed, eventType='node_setBypassed', eventID=hash(node))

    def __setBypassedInTreeWidget(self, node, treeWidget):
        """
        Render appropriate icon for given node's disabled state.

        @type node: C{NodegraphAPI.Node}
        @param node: Node to query.
        @param treeWidget: Tree widget to update.
        """
        item = self.__findItemRepresentingNode(node, treeWidget)
        if item:
            if node.isBypassed():
                item.setIcon(_TreeWidget.ColumnHeaders.Name.index, _NetworkMaterialItem.iconDisabled())
            else:
                item.setIcon(_TreeWidget.ColumnHeaders.Name.index, _NetworkMaterialItem.iconNetwork())

    def __findItemRepresentingNode(self, node, treeWidget):
        """
        Find the tree widget row corresponding to given node.

        @type node: C{NodegraphAPI.Node}
        @type treeWidget: C{QtWidgets.QWidget}
        @rtype: L{_TreeWidgetItem} or C{None}
        @param node: Node to locate widget item for.
        @param treeWidget: Tree widget to search.
        @return: The item representing the node in the widget.
        """
        for i in range(treeWidget.topLevelItemCount()):
            item = treeWidget.topLevelItem(i)
            if node == item.getItemData():
                return item
            result = self.__findItemRepresentingNodeFromItem(node, item)
            if result:
                return result

        return

    def __findItemRepresentingNodeFromItem(self, node, treeWidgetItem):
        """
        Find the child tree widget row corresponding to given node.

        @type node: C{NodegraphAPI.Node}
        @type treeWidgetItem: L{_TreeWidgetItem}
        @rtype: L{_TreeWidgetItem}
        @param node: Node to locate widget item for.
        @param treeWidgetItem: Parent tree widget item.
        @return: The item representing the node in the widget.
        """
        for i in range(treeWidgetItem.childCount()):
            child = treeWidgetItem.child(i)
            if node == child.getItemData():
                return child
            result = self.__findItemRepresentingNodeFromItem(node, child)
            if result:
                return result

        return

    def _buildTabWidgets(self, tabWidget):
        """
        Set the tab to expose the parameters for each of the hidden internal
        nodes within the NetworkMaterialCreate.

        @type tabWidget: C{QtWidgets.QWidget}
        @param tabWidget: tab to set.
        """
        self._tabWidget = tabWidget

    def __populateTabWidgets(self, networkMaterialNode):
        """
        Populate the tab widget in with parameters from given node.

        @type networkMaterialNode: C{NodegraphAPI.Node}
        @param networkMaterialNode: NetworkMaterial node to display.
        """
        for i in range(self._tabWidget.count()):
            self._tabWidget.widget(i).deleteLater()

        nodeParametersTab = self._addTab(self._tabWidget, 'Node Parameters')
        interfaceTab = self._addTab(self._tabWidget, 'Interface Controls')
        materialInterfaceTab = self._addTab(self._tabWidget, 'Material Interface')
        if not networkMaterialNode or networkMaterialNode.isMarkedForDeletion():
            return
        # override
        # add extra
        nmc = networkMaterialNode.getParent()
        if nmc:
            # add customize
            for i in ['user', 'extra']:
                i_p = nmc.getParameter(i)
                if i_p:
                    self._addParameterWidget(nodeParametersTab, i_p)

        materialEditNode = GetNodeFromParam(networkMaterialNode, '__node_materialEdit')
        if materialEditNode:
            shadersParameter = materialEditNode.getParameter('shaders.parameters')
            if shadersParameter:
                self._addParameterWidget(nodeParametersTab, shadersParameter)
        #
        nodeParametersTab.layout().addStretch()
        groupStackNode = GetNodeFromParam(networkMaterialNode, '__node_groupStack')
        if groupStackNode:
            stackInfoParam = groupStackNode.getParameter('__stackInfo')
            if stackInfoParam:
                stackWidget = self._addParameterWidget(interfaceTab, stackInfoParam)
                if stackWidget:
                    stackWidget.selectionChanged.connect(self._on_groupStackSelectionChanged)
        if networkMaterialNode:
            interfaceParam = networkMaterialNode.getParameter('publicInterfaceOrder')
            if interfaceParam:
                self._addParameterWidget(materialInterfaceTab, interfaceParam, hideTitle=True)
        materialInterfaceTab.layout().addStretch()

    def __on_treeWidget_selectionChanged(self):
        """
        Slot handler for C{itemSelectionChanged} signal on tree widget.

        Update the tab widget showing newly selected NetworkMaterial's
        parameters.
        """
        selectedItems = self.__treeWidget.selectedItems()
        if len(selectedItems) == 0:
            return
        for item in selectedItems:
            node = item.getItemData()
            if node and node.getType() == 'NetworkMaterial':
                if node is not self.__selectedNodeInTabWidget:
                    self.__selectedNodeInTabWidget = node
                    self.__populateTabWidgets(node)
                    return

    def __on_nm_create(self, eventType, eventID, node=None, **kwargs):
        """
        Event handler for C{'nodegraph_nmc_nm_create'}.

        Watch relevant events on new node and update tree widget to show the
        node.

        @type eventType: C{str}
        @type eventID: C{object}
        @type node: C{NodegraphAPI.Node}
        @type kwargs: C{dict}
        @param eventType: Ignored.
        @param eventID: Ignored.
        @param node: Newly created NetworkMaterial node.
        @param kwargs: Ignored.
        """
        self.__watchNode(node)
        self.__repopulateTreeWidget()

    def __on_nm_delete(self, eventType, eventID, node=None, **kwargs):
        """
        Event handler for C{'nodegraph_nmc_nm_delete'}.

        Stop watching relevant events on deleted node and update tree widget to
        remove the node.

        @type eventType: C{str}
        @type eventID: C{object}
        @type node: C{NodegraphAPI.Node}
        @type kwargs: C{dict}
        @param eventType: Ignored.
        @param eventID: Ignored.
        @param node: Deleted NetworkMaterial node.
        @param kwargs: Ignored.
        """
        self.__unwatchNode(node)
        self.__repopulateTreeWidget()

    def __on_namespace_create(self, eventType, eventID, node=None, **kwargs):
        """
        Event handler for C{'nodegraph_nmc_namespace_create'}.

        Watch relevant events on new node and update tree widget to show the
        node.

        @type eventType: C{str}
        @type eventID: C{object}
        @type node: C{NodegraphAPI.Node}
        @type kwargs: C{dict}
        @param eventType: Ignored.
        @param eventID: Ignored.
        @param node: Newly created LocationCreate node.
        @param kwargs: Ignored.
        """
        self.__watchNode(node)
        self.__repopulateTreeWidget()

    def __on_namespace_delete(self, eventType, eventID, node=None, **kwargs):
        """
        Event handler for C{'nodegraph_nmc_namespace_delete'}.

        Stop watching relevant events on deleted node and update tree widget to
        remove the node.

        @type eventType: C{str}
        @type eventID: C{object}
        @type node: C{NodegraphAPI.Node}
        @type kwargs: C{dict}
        @param eventType: Ignored.
        @param eventID: Ignored.
        @param node: Deleted LocationCreate node.
        @param kwargs: Ignored.
        """
        self.__unwatchNode(node)
        self.__repopulateTreeWidget()

    def __on_node_bypassed(self, eventType, eventID, node=None, **kwargs):
        """
        Event handler for C{'node_setBypassed'}.

        Update tree widget row icon for node, if it's a NetworkMaterial child
        of the NetworkMaterialCreate.

        @type eventType: C{str}
        @type eventID: C{object}
        @type node: C{NodegraphAPI.Node}
        @type kwargs: C{dict}
        @param eventType: Ignored.
        @param eventID: Ignored.
        @param node: enabled/disabled node.
        @param kwargs: Ignored.
        """
        if self._isNodeChildNetworkMaterial(node):
            self.__setBypassedInTreeWidget(node, self.__treeWidget)

    def __on_parameter_finalizeValue(self, eventID, eventType, param=None, **kwargs):
        """
        Event handler for C{'parameter_finalizeValue'} on NetworkMaterial or
        LocationCreate nodes within the NetworkMaterialCreate.

        Update tree widget when B{name}, B{namespace} or B{namespaceName}
        parameter changes.

        @type eventType: C{str}
        @type eventID: C{object}
        @type param: C{NodegraphAPI.Parameter}
        @type kwargs: C{dict}
        @param eventType: Ignored.
        @param eventID: Ignored.
        @param param: updated parameter.
        @param kwargs: Ignored.
        """
        if param.getName() not in ('name', 'namespace', 'namespaceName'):
            return
        self.__repopulateTreeWidget()

    @debounce(20)
    def __repopulateTreeWidget(self):
        """
        Repopulate the tree widget to reflect any changes.

        Debounced so it only runs a max of once per 20ms.
        """
        self.__treeWidget.populate(self._node.getMaterialLocationNodesInMergeOrder())


class _AddNetworkMaterialButton(UI4.Widgets.MenuButton):
    """
    Button to add NetworkMaterial / namespace nodes to a given
    NetworkMaterialCreate
    """

    def __init__(self, parent, nmc):
        """
        Initializes an instance of this class.

        @type parent: C{QtWidgets.QWidget}
        @type nmc: C{NodegraphAPI.SuperTool}
        @param parent: Widget this button belongs to.
        @param nmc: NetworkMaterialCreate node to add to.
        """
        UI4.Widgets.MenuButton.__init__(self, parent)
        self.__nmc = nmc
        self.setIcon(UI4.Util.IconManager.GetIcon('Icons/plus16.png'))
        self.setIconSize(UI4.Util.IconManager.GetSize('Icons/find20.png'))
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setArrowVisible(False)
        self.setFlat(True)
        self.setButtonType('toolbar')
        addNetMatAction = QtWidgets.QAction('Add NetworkMaterial', self)
        addNetMatAction.triggered.connect(self.__on_addNetMat)
        self.menu().addAction(addNetMatAction)
        addNamespaceAction = QtWidgets.QAction('Add Namespace', self)
        addNamespaceAction.triggered.connect(self.__on_addNamespace)
        self.menu().addAction(addNamespaceAction)

    def _displayMenu(self):
        """
        Show the menu.

        Override base class to disable menu items if the NetworkMaterialCreate
        is locked.
        """
        isDisabled = self.__nmc.isLocked()
        for action in self.menu().actions():
            action.setDisabled(isDisabled)

        UI4.Widgets.MenuButton._displayMenu(self)

    def __on_addNetMat(self):
        """
        Signal handler for "+" button menu action.

        Create a NetworkMaterial node within the NetworkMaterialCreate.
        """
        self.__nmc.addNetworkMaterialNode()

    def __on_addNamespace(self):
        """
        Signal handler for "+" button menu action.

        Create a LocationCreate namespace node within the
        NetworkMaterialCreate.
        """
        self.__nmc.addNamespace()


class _TreeWidget(QT4Widgets.SortableTreeWidget):
    ColumnHeaders = enum.Enum('Name', 'Renderers', 'Terminals', 'Interactive', 'Color')

    def __init__(self, nmc, mainPanel):
        """
        Create the multi-output interface for the NMC node.

        @type nmc: C{NodegraphAPI.SuperTool}
        @type mainPanel: C{QtWidgets.QWidget}
        @param nmc: NetworkMaterialCreate node.
        @param mainPanel: Panel to add widget to.
        """
        QT4Widgets.SortableTreeWidget.__init__(self, mainPanel)
        self.__nmc = nmc
        self.setObjectName('treeWidget')
        self.setStyleSheet('QTreeView::item { min-height: 24px; }')
        self.setColumnCount(len(self.ColumnHeaders))
        self.setHeaderLabels(self.ColumnHeaders._keys)
        self.setSelectionMode(self.ExtendedSelection)
        self.setDraggable(True)
        self.aboutToDrag.connect(self.__onDragStart)
        self.dragMoveEventSignal.connect(self.__onDragMove)
        self.dropEventSignal.connect(self.__onDragDrop)
        self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.header().setSectionsMovable(False)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.setMinimumHeight(165)
        self.contextMenuEventSignal.connect(_ContextMenu(nmc, self).open)
        QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl++'), self).activated.connect(self.expandSelectedItemsRecursively)
        QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+-'), self).activated.connect(self.collapseSelectedItemsRecursively)
        QtWidgets.QShortcut(QtCore.Qt.Key_Delete, self).activated.connect(self.deleteSelectedItemsRecursively)
        QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+D'), self).activated.connect(self.duplicateSelectedItems)

    def populate(self, nodes):
        """
        Populate the tree with given list of nodes.

        @type nodes: C{list} of C{NodegraphAPI.Node}
        @param nodes: List of NetworkMaterial and LocationCreate nodes in
            depth-first top-down tree order.
        """
        itemByPath = {'/': self.invisibleRootItem()}
        offsetByPath = collections.defaultdict(int)
        newItems = []
        selectedItems = []
        selectedNodes = [ item.getItemData() for item in self.selectedItems() ]
        scrollPosition = self.verticalScrollBar().value()
        expandedByNode = {item.getItemData():item.isExpanded() for item in self.__gatherAllChildren(self.invisibleRootItem())}
        self.clear()
        for node in nodes:
            location = MaterialLocation(node)
            item = _TreeWidgetItem.createForNode(node)
            offset = offsetByPath[location.parentPath]
            parentItem = itemByPath[location.parentPath]
            parentItem.insertChild(offset, item)
            item.populateWidgets()
            expanded = expandedByNode.get(node)
            if expanded is None:
                newItems.append(item)
                item.setExpanded(True)
            else:
                item.setExpanded(expanded)
            if node in selectedNodes:
                selectedItems.append(item)
            itemByPath[location.path] = item
            offsetByPath[location.parentPath] += 1

        if newItems:
            self.selectItemExclusive(newItems[0])
        else:
            for item in selectedItems:
                item.setSelected(True)

            self.verticalScrollBar().setValue(scrollPosition)
        self.setStyle(self.style())
        return

    def __onDragStart(self, items, dragObject):
        """
        Slot handler for C{aboutToDrag} signal.

        Set MIME data from selected nodes.

        @type items: C{list} of L{_TreeWidgetItem}
        @type dragObject: C{InteractiveDrag}
        @param items:  List of items being dragged.
        @param dragObject: Drag interface.
        """
        nodes = filter(None, (item.getItemData() for item in items))
        mimeData = NodeMimeData.GetNodeMimeData(nodes)
        mimeData.removeFormat(NodeMimeData.MIME_TYPE_NODES)
        dragObject.setMimeData(mimeData)
        return

    def __onDragMove(self, event, parent, index, callbackRecord):
        """
        Slot handler for C{dragMoveEventSignal} signal.

        Prevent dropping selected items on invalid locations.

        @type event: C{QtCore.QEvent}
        @type parent:  C{_TreeWidgetItem} or C{None}
        @type index: c{int}
        @type callbackRecord: C{CallbackRecord}
        @param event: Ignored.
        @param parent: Potential new parent item.
        @param index: Ignored.
        @param callbackRecord: Record to flag if dropping is allowed here
        """
        items = self.getDragItems()
        if not items:
            return
        else:
            if parent is not None:
                parentNode = parent.getItemData()
                if parentNode.getType() != 'LocationCreate':
                    return
                parentPath = MaterialLocation(parentNode).path
                locations = (MaterialLocation(item.getItemData()) for item in items)
                if any(loc.isAncestorOf(parentPath) for loc in locations):
                    return
            callbackRecord.accept()
            return

    def __onDragDrop(self, event, parent, index):
        """
        Slot handler for C{dropEventSignal} signal.

        Re-parent selected NetworkMaterial and LocationCreate namespace
        scene graph location under new parent.

        @type event: C{QtCore.QEvent}
        @type parent:  C{_TreeWidgetItem} or C{None}
        @type index: c{int}
        @param event: Ignored.
        @param parent: New parent item.
        @param index: Index amongst siblings under new parent.
        """
        if parent and parent in self.getDragItems():
            return
        parent = parent and parent.getItemData()
        for offset, item in enumerate(self.getDragItems()):
            self.__nmc.reparentNamespace(item.getItemData(), parent, index + offset)

    def selectItemExclusive(self, item):
        """
        Clear current selection, scroll to item and select it.

        @type item: C{_TreeWidgetItem}
        @param item: Item to select.
        """
        self.clearSelection()
        self.scrollToItem(item)
        item.setSelected(True)

    def findRootItem(self, nameText):
        """
        Find top-level tree widget item with given label.

        @type nameText: C{str}
        @rtype: C{_TreeWidgetItem} or C{None}
        @param nameText: Text to search for.
        @return: Found item or C{None} if not found.
        """
        for i in range(self.topLevelItemCount()):
            topLevelItem = self.topLevelItem(i)
            topLevelName = topLevelItem.text(self.ColumnHeaders.Name.index)
            if topLevelName == nameText:
                return topLevelItem

        return

    @staticmethod
    def findChildItem(parentItem, nameText):
        """
        Find child tree widget item with given label.

        @type parentItem: C{_TreeWidgetItem}
        @type nameText: C{str}
        @rtype: C{_TreeWidgetItem} or C{None}
        @param parentItem: Item to start search from
        @param nameText: Text to search for.
        @return: Found item or C{None} if not found.
        """
        for i in range(parentItem.childCount()):
            child = parentItem.child(i)
            childName = child.text(_TreeWidget.ColumnHeaders.Name.index)
            if childName == nameText:
                return child

        return

    def expandSelectedItemsRecursively(self):
        """
        Recursively expand all selected tree widget items.
        """
        for item in self.selectedItems():
            self.__expandItemRecursively(item)

    def __expandItemRecursively(self, item):
        """
        Recursively expand given tree widget item.

        @type item: C{_TreeWidgetItem}
        @param item: Item to expand.
        """
        numChildren = item.childCount()
        if numChildren:
            self.expandItem(item)
            for childIdx in xrange(numChildren):
                self.__expandItemRecursively(item.child(childIdx))

    def collapseSelectedItemsRecursively(self):
        """
        Recursively collapse all selected tree widget items.
        """
        for item in self.selectedItems():
            self.__collapseItemRecursively(item)

    def __collapseItemRecursively(self, item):
        """
        Recursively collapse given tree widget item.

        @type item: C{_TreeWidgetItem}
        @param item: Item to collapse.
        """
        numChildren = item.childCount()
        if numChildren:
            self.collapseItem(item)
            for childIdx in xrange(numChildren):
                self.__collapseItemRecursively(item.child(childIdx))

    def deleteSelectedItemsRecursively(self):
        """
        Recursively delete all selected tree widget items.
        """
        if self.__nmc.isLocked():
            return
        Utils.UndoStack.OpenGroup('Delete selected items in "%s"' % self.__nmc.getName())
        try:
            for item in self.selectedItems():
                node = item.getItemData()
                self.__nmc.deleteNamespace(node)

        finally:
            Utils.UndoStack.CloseGroup()

    def __gatherAllChildren(self, item):
        """
        Recurse through child items collecting them all in a list.

        @type item: C{_TreeWidgetItem}
        @rtype: C{list} of C{_TreeWidgetItem}
        @param item: Item to recurse through.
        @return: List of descendent items.
        """
        numChildren = item.childCount()
        result = []
        for childIdx in xrange(numChildren):
            childItem = item.child(childIdx)
            result.append(childItem)
            result.extend(self.__gatherAllChildren(childItem))

        return result

    def __pruneNestedSelections(self, items):
        """
        Filter out descendents in list of items.

        Will mutate C{items}.

        @type items: C{list} of C{_TreeWidgetItem}
        @rtype: C{list} of C{_TreeWidgetItem}
        @param items: Items to filter.
        @return: list of items with descendents removed.
        """
        for item in items[:]:
            parent = item.parent()
            while parent and parent != self:
                if parent in items:
                    items.remove(item)
                    break
                parent = parent.parent()

        return items

    def duplicateSelectedItems(self):
        """
        Duplicate NetworkMaterial and LocationCreate namespace nodes
        corresponding to selected items.
        """
        if self.__nmc.isLocked():
            return
        Utils.UndoStack.OpenGroup('Duplicate selected items in "%s"' % self.__nmc.getName())
        try:
            items = self.selectedItems()
            if len(items) > 1:
                items = self.__pruneNestedSelections(items)
            for item in items:
                self.__duplicateItem(item)

        finally:
            Utils.UndoStack.CloseGroup()

    def __duplicateItem(self, item):
        """
        Duplicate a NetworkMaterial or LocationCreate namespace node
        corresponding to given item.

        @type item: C{_TreeWidgetItem}
        @param item: Item to duplicate.
        """
        if self.__nmc.isLocked():
            return
        node = item.getItemData()
        if not node:
            return
        if node.getType() == 'NetworkMaterial':
            self.__nmc.duplicateNetworkMaterialNode(node)
        elif node.getType() == 'LocationCreate':
            self.__nmc.duplicateNamespace(node)


class _TreeWidgetItem(QT4Widgets.SortableTreeWidgetItem):
    """
    Item representing a row in a NetworkMaterialCreate editor tree widget.
    """

    @staticmethod
    def createForNode(node):
        """
        Create the appropriate subclass for given node type.

        @type node: C{NodegraphAPI.Node}
        @rtype: C{_NetworkMaterialItem} or C{_NamespaceItem}
        @param node: Node to create corresponding item for.
        @return: New item corresponding to C{node}.
        @raise TypeError: If type of C{node} is not NetworkMaterial or
            LocationCreate.
        """
        if node.getType() == 'NetworkMaterial':
            return _NetworkMaterialItem(node)
        if node.getType() == 'LocationCreate':
            return _NamespaceItem(node)
        raise TypeError('Tree widget item cannot be constructed for node %s of type %s' % (
         node.getName(), node.getType()))

    def __init__(self, node):
        """
        Initializes an instance of this class.

        @type node: C{NodegraphAPI.Node}
        @param node: Node this item corresponds to.
        """
        QT4Widgets.SortableTreeWidgetItem.__init__(self, None, data=node)
        self.setText(_TreeWidget.ColumnHeaders.Name.index, MaterialLocation(node).leafPath)
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled)
        return

    def setData(self, column, role, value):
        """
        Override Qt hook to handle user editing of item text.

        Sets NetworkMaterial/LocationCreate leaf name to given value when
        user updates the text in the widget.

        @type column: C{int}
        @type role: C{int}
        @type value: C{str}
        @param column: Column that was edited.
        @param role: Qt role idenitifier (we only care about `EditRole`).
        @param value: Text value to set.
        """
        QT4Widgets.SortableTreeWidgetItem.setData(self, column, role, value)
        if role != QtCore.Qt.EditRole:
            return
        else:
            if column != _TreeWidget.ColumnHeaders.Name.index:
                return
            node = self.getItemData()
            if node is None:
                return
            if node.getType() == 'NetworkMaterial':
                node.getParent().setNetworkMaterialNodeName(node, str(value))
            elif node.getType() == 'LocationCreate':
                node.getParent().setNamespaceLeafName(node, str(value))
            return

    def populateWidgets(self):
        """
        Construct child widgets.
        """
        pass


class _NamespaceItem(_TreeWidgetItem):
    """
    Tree widget item representing a LocationCreate namespace node.
    """
    pass


class _NetworkMaterialItem(_TreeWidgetItem):
    """
    Tree widget item representing a NetworkMaterial node.
    """
    __iconNetwork = None
    __iconDisabled = None

    @classmethod
    def iconDisabled(cls):
        """
        Load disabled icon and cache for future reference.

        @rtype: C{QtGui.QIcon}
        @return: Disabled icon.
        """
        if cls.__iconDisabled is None:
            cls.__iconDisabled = QtGui.QIcon(QtGui.QPixmap(ResourceFiles.GetResourceFile('Icons/remove16.png')))
        return cls.__iconDisabled

    @classmethod
    def iconNetwork(cls):
        """
        Load network icon and cache for future reference.

        @rtype: C{QtGui.QIcon}
        @return: network icon.
        """
        if cls.__iconNetwork is None:
            cls.__iconNetwork = QtGui.QIcon(QtGui.QPixmap(ResourceFiles.GetResourceFile('Icons/network.png')))
        return cls.__iconNetwork

    def __init__(self, node):
        """
        Initializes an instance of this class.

        @type node: C{NodegraphAPI.Node}
        @param node: NetworkMaterial node to represent.
        """
        _TreeWidgetItem.__init__(self, node)
        if node.isBypassed():
            self.setIcon(_TreeWidget.ColumnHeaders.Name.index, self.iconDisabled())
        else:
            self.setIcon(_TreeWidget.ColumnHeaders.Name.index, self.iconNetwork())

    def populateWidgets(self):
        """
        Construct child widgets.

        Interactive checkbox, terminals and renderers counters, and colour hint
        picker.
        """
        treeWidget = self.treeWidget()
        node = self.getItemData()
        treeWidget.setItemWidget(self, _TreeWidget.ColumnHeaders.Interactive.index, _MakeInteractiveCheckBox(treeWidget, node))
        treeWidget.setItemWidget(self, _TreeWidget.ColumnHeaders.Color.index, _ColourBox(treeWidget, node))
        treeWidget.setItemWidget(self, _TreeWidget.ColumnHeaders.Terminals.index, _TerminalsLabel(treeWidget, node))
        treeWidget.setItemWidget(self, _TreeWidget.ColumnHeaders.Renderers.index, _RenderersLabel(treeWidget, node))


class _NetworkMaterialPortNumberLabel(QtWidgets.QFrame):
    """
    Widget base class for a label with rounded border, updated when
    NetworkMaterial's scene graph location attrs change.
    """
    __stylesheet = '\n    QFrame {\n        background-color: rgba(0, 0, 0, 0);\n    }\n    QLabel {\n        background-color: rgba(0, 0, 0, 0);\n        border-color: rgb(128, 128, 128);\n        border-radius: 8px;\n        border-style: solid;\n        border-width: 1px;\n        color: rgb(255, 255, 255);\n        font-size: 11px;\n        min-width: 11px;\n        min-height: 14px;\n        padding-left: 2px;\n        padding-right: 2px;\n    }\n    QLabel[error="true"] {\n        border-color: #d66161;\n    }\n    '
    __locationChangedEvent = 'nodegraph_nmc_nm_location_changed'

    def __init__(self, parent, node):
        """
        Initializes an instance of this class.

        @type parent: C{_TreeWidget}
        @type node: C{NodegraphAPI.Node}
        @param parent: Tree widget this widget belongs to.
        @param node: NetworkMaterial node to query.
        """
        QtWidgets.QFrame.__init__(self, parent)
        self._node = node
        self.__isShown = False
        self.__label = QtWidgets.QLabel('', self)
        self.__label.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet(self.__stylesheet)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.__label, 0, QtCore.Qt.AlignCenter)
        self.setLayout(layout)
        self.__listener = LeafSceneGraphLocationListener(self._node, self._node, self.__locationChangedEvent, hash(self))
        Utils.EventModule.RegisterEventHandler(self.__onLocationChanged, self.__locationChangedEvent, hash(self))
        Utils.EventModule.RegisterEventHandler(self.__onNodeSetBypassed, 'node_setBypassed', hash(self._node))
        self._updateTextAndErrorState()

    def showEvent(self, event):
        """
        Qt event handler.

        Start listening to scene graph updates corresponding to watched
        NetworkMaterial node, if not already listening.

        @type event: C{QtCore.QEvent}
        @param event: Ignored.
        """
        if not self.__isShown:
            self.__listener.registerEventHandlers()
            self.__isShown = True

    def hideEvent(self, event):
        """
        Qt event handler.

        Stop listening to scene graph updates corresponding to watched
        NetworkMaterial node, if currently listening.

        @type event: C{QtCore.QEvent}
        @param event: Ignored.
        """
        if self.__isShown:
            self.__listener.unregisterEventHandlers()
            self.__isShown = False

    def __onLocationChanged(self, eventType, eventID):
        """
        Event handler for C{'nodegraph_nmc_nm_location_changed'}.

        Update text counter when scene graph location attributes of watched
        NetworkMaterial change.

        Ignore if the NetworkMaterial is disabled.

        @type eventType: C{str}
        @type eventID: C{object}
        @param eventType: Ignored.
        @param eventID: Ignored.
        """
        if self._node.isBypassed():
            return
        self._updateTextAndErrorState()

    def _updateTextAndErrorState(self):
        """
        Update counter text and style.
        """
        raise NotImplementedError()

    def __onNodeSetBypassed(self, eventType, eventID, **kwargs):
        """
        Event handler for C{'node_setBypassed'}.

        Update text, tooltip and style if watched NetworkMaterial is disabled.

        @type eventType: C{str}
        @type eventID: C{object}
        @type kwargs: C{dict}
        @param eventType: Ignored.
        @param eventID: Ignored.
        @param kwargs: Ignored.
        """
        if self._node.isBypassed():
            self._setLabelText('0')
            self._setToolTip('%s is disabled' % self._node.getName())
            self._setError(False)

    def _setLabelText(self, text):
        """
        @type text: C{str}
        @param text: label to set.
        """
        self.__label.setText(text)

    def _setToolTip(self, text):
        """
        @type text: C{str}
        @param text: Tooltip text to set.
        """
        self.__label.setToolTip(text)

    def _setError(self, isError):
        """
        Update styling to show that the watched NetworkMaterial is in an error
        state.

        @type isError: C{bool}
        @param isError: C{True} to flag an error, C{False} otherwise.
        """
        self.__label.setProperty('error', isError)
        self.__label.setStyle(self.__label.style())

    def _getConnectedTerminals(self):
        """
        Get all connected input ports of watched NetworkMaterial.

        @rtype: C{list} of C{NodegraphAPI.Port}
        @return: List of connected input ports.
        """
        return [ port for port in self._node.getInputPorts() if port.getConnectedPorts()
               ]


class _TerminalsLabel(_NetworkMaterialPortNumberLabel):
    """
    Widget showing the total number of connections to a node.
    """

    def _updateTextAndErrorState(self):
        """
        Update counter text and style.

        Construct tooltip listing connected input ports on watched
        NetworkMaterial including any errors related to those ports.

        Update label with number of connected input ports.

        Enable/disable error styling if any port is erroring.
        """
        connectedTerminals = self._getConnectedTerminals()
        okToolTips = []
        errorToolTips = []
        for terminal in connectedTerminals:
            errorMessages = []
            for outputPort in terminal.getConnectedPorts():
                self._node.validateConnection(outputPort, terminal, errorMessages=errorMessages)

            if not errorMessages:
                okToolTips.append(terminal.getName())
            else:
                errorToolTips.append('%s: %s' % (terminal.getName(), (', ').join(errorMessages)))

        toolTipText = (', ').join(okToolTips)
        if errorToolTips:
            toolTipText = ('\n').join((toolTipText, ('\n').join(errorToolTips)))
        self._setLabelText(str(len(connectedTerminals)))
        self._setToolTip(toolTipText)
        self._setError(bool(errorToolTips))


class _RenderersLabel(_NetworkMaterialPortNumberLabel):
    """
    Widget showing the number of renderers in use by a NetworkMaterial.
    """

    def _updateTextAndErrorState(self):
        """
        Update counter text and style.

        Set tooltip to list of renderers in use by watched NetworkMaterial.

        Set label to number of renderers.
        """
        renderers = RenderingAPI.RenderPlugins.GetRendererPluginNames()
        used = set()
        for port in self._getConnectedTerminals():
            match = next((renderer for renderer in renderers if port.getName().startswith(renderer)), 'unknown')
            used.add(match)

        self._setLabelText(str(len(used)))
        self._setToolTip((', ').join(sorted(used)))


class _MakeInteractiveCheckBox(QtWidgets.QFrame):
    """
    Widget showing a simplified checkbox ParameterPolicy widget for the
    B{makeInteractive} parameter of the given node.
    """
    __stylesheet = '\n    QCheckBox::indicator {\n        background-color: rgba(0, 0, 0, 0);\n        border-color: rgb(128, 128, 128);\n        border-style: solid;\n        border-width: 1px;\n        outline: none;\n        min-width: 13px;\n        min-height: 13px;\n    }\n    QCheckBox::indicator:hover {\n        background-color: rgba(0, 0, 0, 0);\n    }\n    QCheckBox::indicator:checked {\n        image: url(%s);\n    }\n    ' % QtCore.QDir.fromNativeSeparators(ResourceFiles.GetResourceFile('Icons/NodeGraphView/tick.png'))

    def __init__(self, parent, node):
        """
        Initialize an instance of this class.

        Constructs a parameter policy checkbox widget and restyles it.

        @type parent: C{_TreeWidget}
        @type node: C{NodegraphAPI.Node}
        @param parent: Tree widget this checkbox belongs to.
        @param node: NetworkMaterial node to query.
        """
        QtWidgets.QFrame.__init__(self, parent)
        param = GetNodeFromParam(node, '__node_materialEdit').getParameter('makeInteractive')
        policy = ParameterPolicy.CreateParameterPolicy(None, param)
        policy.getWidgetHints()['widget'] = 'checkBox'
        policy.getWidgetHints()['suppressLabel'] = True
        factory = KatanaFactory.ParameterWidgetFactory
        policyWidget = factory.buildWidget(self, policy)
        palette = policyWidget.palette()
        palette.setColor(QtGui.QPalette.Background, QtGui.QColor(0, 0, 0, 0))
        policyWidget.setPalette(palette)
        policyWidget.setHighlightStyle(policyWidget.HIGHLIGHTSTYLE_NONE)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(policyWidget, 0, QtCore.Qt.AlignCenter)
        self.setLayout(layout)
        self.setStyleSheet(self.__stylesheet)
        return


class _ColourBox(QtWidgets.QFrame):
    """
    Widget showing a node's shape attr colour and presenting the "Colors" menu
    for the node when clicked.
    """
    __defaultColour = (
     95.0 / 255, 94.0 / 255, 94.0 / 255)
    __stylesheet = '\n    QPushButton{\n        border-color: rgb(31, 31, 31);\n        border-style: solid;\n        border-width: 1px;\n        width: 13px;\n        height: 13px;\n        min-width: 13px;\n        min-height: 13px;\n        outline: none;\n    }\n    '

    def __init__(self, parent, node):
        """
        Initializes an instance of this class.

        @type parent: C{_TreeWidget}
        @type node: C{NodegraphAPI.Node}
        @param parent: Tree widget this widget belongs to.
        @param node: NetworkMaterial node to query.
        """
        QtWidgets.QFrame.__init__(self, parent)
        self.__node = node
        self.__colourDrop = QtWidgets.QPushButton(self)
        self.__colourDrop.setFlat(True)
        self.__colourDrop.setAutoFillBackground(True)
        self.__colourDrop.clicked.connect(self.onClicked)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.__colourDrop, 0, QtCore.Qt.AlignCenter)
        self.setLayout(layout)
        self.setStyleSheet(self.__stylesheet)
        self.__onNodeSetColour(node)
        Utils.EventModule.RegisterEventHandler(self.__onNodeSetShapeAttributes, eventType='node_setShapeAttributes', eventID=hash(node))

    def __onNodeSetShapeAttributes(self, eventType, eventID, node=None):
        """
        Event handler for C{'node_setShapeAttributes'}.

        Update widget colour when node colour shape attribute changes.

        @type eventType: C{str}
        @type eventID: C{object}
        @type node: C{NodegraphAPI.Node}
        @param eventType: Ignored.
        @param eventID: Ignored.
        @param node: NetworkMaterial node.
        """
        self.__onNodeSetColour(node)

    def __onNodeSetColour(self, node):
        """
        Update widget colour to match node colour shape attribute.

        @type node: C{NodegraphAPI.Node}
        @param node: NetworkMaterial node to take colour from.
        """
        colour = DrawingModule.GetCustomNodeColor(node)
        if colour is None:
            colour = self.__defaultColour
        colour = [ str(int(c * 255)) for c in colour ]
        self.__colourDrop.setStyleSheet('background-color: rgb(%s)' % (', ').join(colour))
        return

    def onClicked(self):
        """
        Qt C{clicked} signal handler.

        Open colour picker to select new colour hint for node.
        """
        menu = NodeColorsMenu(self, [self.__node])
        menu.exec_(self.__colourDrop.mapToGlobal(self.__colourDrop.pos()))


class _ContextMenu(QtWidgets.QMenu):
    """
    Right-click context menu for NetworkMaterialCreate editor tree widget.
    """

    def __init__(self, nmc, parent):
        """
        Initializes an instance of this class.

        @type nmc: C{NodegraphAPI.SuperTool}
        @type parent: C{_TreeWidget}
        @param nmc: NetworkMaterialCreate node to operate on.
        @param parent: Tree widget this menu belongs to.
        """
        QtWidgets.QMenu.__init__(self, 'NetworkMaterialCreate tree menu', parent)
        self.__nmc = nmc
        self.__itemNode = None
        self.__item = None
        self.__createActions = (
         self.addAction('Add NetworkMaterial', self.__onAddNetworkMaterial),
         self.addAction('Add Namespace', self.__onAddNamespace))
        self.addSeparator()
        self.__deleteAction = self.addAction('Delete', self.__onDeleteItem)
        self.__deleteAction.setShortcut(QtCore.Qt.Key_Delete)
        self.__duplicateAction = self.addAction('Duplicate', self.__onDupeItem)
        self.__duplicateAction.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_D))
        self.addSeparator()
        self.__viewActions = (
         self.addAction('Expand All', self.__onExpandItem),
         self.addAction('Collapse All', self.__onCollapseItem))
        self.__viewActions[0].setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Plus))
        self.__viewActions[1].setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Minus))
        return

    def open(self, event):
        """
        Qt C{contextMenuEventSignal} handler.

        Show this menu.

        @type event: C{QtCore.QEvent}
        @param event: Event containing click location.
        """
        createActionsDisabled = False
        delAndDupeActionDisabled = False
        viewActionsDisabled = False
        if self.__nmc.isLocked(True):
            createActionsDisabled = True
            delAndDupeActionDisabled = True
            viewActionsDisabled = True
        else:
            self.__item = self.parent().itemAt(event.pos())
            self.__itemNode = self.__item and self.__item.getItemData()
            if self.__itemNode is None:
                delAndDupeActionDisabled = True
                viewActionsDisabled = True
            else:
                if self.__itemNode.getType() == 'NetworkMaterial':
                    createActionsDisabled = True
                    viewActionsDisabled = True
                for action in self.__createActions:
                    action.setDisabled(createActionsDisabled)

            self.__deleteAction.setDisabled(delAndDupeActionDisabled)
            self.__duplicateAction.setDisabled(delAndDupeActionDisabled)
            for action in self.__viewActions:
                action.setDisabled(viewActionsDisabled)

        self.exec_(event.globalPos())
        return

    def __onAddNetworkMaterial(self):
        """
        "Add NetworkMaterial" menu action handler.

        Create a new NetworkMaterial node under selected namespace or root.
        """
        self.__nmc.addNetworkMaterialNode(namespace=self.__getSelectedNamespace())

    def __onAddNamespace(self):
        """
        "Add Namespace" menu action handler.

        Create a new LocationCreate namespace node under selected namespace or
        root.
        """
        namespace = 'namespace'
        parentNamespace = self.__getSelectedNamespace()
        if parentNamespace is not None:
            namespace = ('/').join((parentNamespace, namespace))
        self.__nmc.addNamespace(name=namespace)
        return

    def __getSelectedNamespace(self):
        """
        Get the B{namespaceName} parameter value of the LocationCreate
        namespace node corresponding to the selected tree widget item.

        @rtype: C{str} or C{None}
        @return: Namespace string or C{None} if no namespace is selected.
        """
        if self.__itemNode is None:
            return
        else:
            if self.__itemNode.getType() != 'LocationCreate':
                return
            return self.__itemNode.getParameter('namespaceName').getValue(0)

    def __onDeleteItem(self):
        """
        "Delete" menu action handler.

        Recursively delete all selected items.
        """
        self.parent().deleteSelectedItemsRecursively()

    def __onDupeItem(self):
        """
        "Duplicate" menu action handler.

        Recursively duplicate all selected items.
        """
        self.parent().duplicateSelectedItems()

    def __onExpandItem(self):
        """
        "Expand All" menu action handler.

        Recursively expand all selected items.
        """
        self.parent().expandSelectedItemsRecursively()

    def __onCollapseItem(self):
        """
        "Collapse All" menu action handler.

        Recursively collapse all selected items.
        """
        self.parent().collapseSelectedItemsRecursively()