# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Nov 16 2020, 22:23:17) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: SuperTools/NetworkMaterials/v1/NetworkMaterialBaseNode.py
# Compiled at: 2021-06-28 21:25:19
"""
Module containing the base class for NetworkMaterialCreate and
NetworkMaterialEdit nodes.
"""
import logging, re
from PackageSuperToolAPI import NodeUtils
from Katana import NodegraphAPI, Nodes3DAPI, RenderingAPI, Utils
log = logging.getLogger('NetworkMaterialBase.Node')
sceneGraphLocationRegex = re.compile('[^a-zA-Z0-9/]')

class NetworkMaterialBaseNode(Nodes3DAPI.NodeLayoutAttributes.LayoutAttributesMixin, NodegraphAPI.SuperTool):
    """
    Base class for NetworkMaterial-related SuperTool node types.

    @since: Katana 4.0v1
    """

    def __init__(self):
        """
        Initializes an instance of this class.
        """
        Nodes3DAPI.NodeLayoutAttributes.LayoutAttributesMixin.__init__(self)
        self.addOutputPort('out')
        paramsGroup = self.getParameters()
        paramsGroup.parseXML(_Parameter_XML)
        paramsGroup.createChildString(NodegraphAPI.NodeGraphContextParameter, NodegraphAPI.Context.NetworkMaterial)
        self._setupInternalNetwork()
        networkMaterialNode = NodegraphAPI.CreateNode('NetworkMaterial', self)
        self.handleNetworkMaterialNodeCreate(networkMaterialNode)

    def _setupInternalNetwork(self):
        """
        Construct the hidden utility nodes for this SuperTool.

        @raise NotImplementedError: Must be overridden by subclasses.
        """
        raise NotImplementedError()

    def getNodesCreatingSceneGraphLocations(self):
        """
        @rtype: C{list} of C{NodegraphAPI.Node} or C{None}
        @return: A list of internal nodes that implement
            C{getScenegraphLocation()} and are desirable to access from
            outside of the SuperTool.
        @since: Katana 4.0v1
        """
        return self.getNetworkMaterials()

    def _getExcludedNodes(self):
        """
        Get the list of nodes that should be excluded from
        C{material.B{layout}} attributes.

        @rtype: C{set} of C{NodegraphAPI.Node}
        @return: List of internal hidden nodes.
        """
        excludedNodes = set()
        for nm in self.getNetworkMaterials():
            excludedNodes.add(GetNodeFromParam(nm, '__node_groupStack'))
            excludedNodes.add(GetNodeFromParam(nm, '__node_materialEdit'))

        return excludedNodes

    def invalidateLayout(self):
        """
        Flag that C{material.B{layout}} attributes need to be reconstructed.
        """
        if not self._isLayoutAttributesValid():
            return
        Nodes3DAPI.NodeLayoutAttributes.LayoutAttributesMixin.invalidateLayout(self)
        for node in self.getNetworkMaterials():
            node.invalidateOps()

    def _getNetworkMaterialLocationExpr(self, networkMaterialNode):
        """
        Returns a parameter expression for the NetworkMaterialNode's
        scenegraph location.

        @type networkMaterialNode: C{NodegraphAPI.Node}
        @rtype: C{str}
        @param networkMaterialNode: The network material node we want to
            create an expression for
        @return: A parameter expression pointing to the NetworkMaterial
            scene graph location.
        """
        return '=%s/sceneGraphLocation' % networkMaterialNode.getName()

    def getNetworkMaterials(self):
        """
        Returns a list of network materials that this SuperTool manages.

        @rtype: C{list} of C{NodegraphAPI.Node}
        @return: NetworkMaterial nodes.
        @raise NotImplementedError: Must be overridden by subclass.
        @since: Katana 4.0v1
        """
        raise NotImplementedError()

    def polish(self):
        """
        This method is automatically called on the SuperTool
        after it has finished loading and initialization.

        It will only be called once.
        """
        Nodes3DAPI.NodeLayoutAttributes.LayoutAttributesMixin.polish(self)
        Utils.EventModule.RegisterEventHandler(self.__on_node_create, eventType='node_create', eventID=None)
        Utils.EventModule.RegisterEventHandler(self.__on_node_delete_begin, eventType='node_delete_begin', eventID=None)
        Utils.EventModule.RegisterEventHandler(self.__on_node_bypassed, eventType='node_setBypassed', eventID=None)
        return

    def _getNodeFromParam(self, parameterName):
        """
        Returns the internal node for the given parameter name.

        @type parameterName: C{str}
        @rtype: C{NodegraphAPI.Node} or C{None}
        @param parameterName: The name of the parameter referring to an
            internal node within the NetworkMaterialCreate.
        @return: The internal node referenced in the parameter.
        """
        return GetNodeFromParam(self, parameterName)

    def handleNetworkMaterialNodeCreate(self, node):
        """
        Handles the creation of a NetworkMaterial node's utility nodes
        (GroupStack and Material) and connects it all up to the return port.

        @type node: C{NodegraphAPI.Node}
        @param node: The NetworkMaterial node being created.
        @raise NotImplementedError: Must be overridden by subclass.
        @since: Katana 4.0v1
        """
        raise NotImplementedError()

    def handleNetworkMaterialNodeDelete(self, node):
        """
        Handles the cleaning of a NetworkMaterial node's utility nodes
        (GroupStack and Material) and cleans up excess connections on the merge
        node. This function will be called on the NetworkMaterialBase class
        whenever we move a NetworkMaterial node outside of the NMBN type or
        when deleting the NM node.

        @type node: C{NodegraphAPI.Node}
        @param node: The NetworkMaterial node being cleaned.
        @since: Katana 4.0v1
        """
        if node is None:
            return
        else:
            if node.getType() != 'NetworkMaterial':
                return
            Utils.UndoStack.DisableCapture()
            try:
                self._cleanUpDeletedNetworkMaterial(node)
                self._cleanMergeNodePorts()
                Utils.EventModule.QueueEvent('nodegraph_nmc_nm_delete', hash(self), node=node)
            finally:
                Utils.UndoStack.EnableCapture()

            return

    def _cleanUpDeletedNetworkMaterial(self, node):
        """
        Delete utility GroupStack and Material nodes for given NetworkMaterial.

        @type node: C{NodegraphAPI.Node}
        @param node: NetworkMaterial node being deleted.
        """
        groupStack = GetNodeFromParam(node, '__node_groupStack')
        if groupStack is not None:
            groupStack.delete()
            param = node.getParameter('__node_groupStack')
            if param is not None:
                node.getParameters().deleteChild(param)
        materialNode = GetNodeFromParam(node, '__node_materialEdit')
        if materialNode is not None:
            materialNode.delete()
            param = node.getParameter('__node_materialEdit')
            if param is not None:
                node.getParameters().deleteChild(param)
        return

    def handleNamespaceCreate(self, node, namespaceName=None, nameSanitized=False):
        """
        Configure parameters on newly created node if it is a child
        LocationCreate and trigger event to notify UI.

        @type node: C{NodegraphAPI.Node}
        @type namespaceName: C{str} or C{None}
        @type nameSanitized: C{bool}
        @param node: (potential) LocationCreate node.
        @param namespaceName: Namespace to set or C{None} to use existing.
        @param nameSanitized: Whether the namespace is already sanitized.
        @since: Katana 4.0v1
        """
        if node is None:
            return
        else:
            if node.getType() != 'LocationCreate':
                return
            if node.getParent() != self:
                return
            outPort = node.getOutputPort('out')
            connectedPorts = outPort.getConnectedPorts()
            if not connectedPorts:
                mergeNode = self._getNodeFromParam('__node_merge')
                if mergeNode is None:
                    log.warning('No Merge node found in NetworkMaterial Super Tool')
                    return
                node.getParameters().createChildNumber('__hidden', 1.0).setHintString('{"widget": "null"}')
                if namespaceName is None:
                    namespaceNameParam = node.getParameter('namespaceName')
                    if namespaceNameParam:
                        namespaceName = namespaceNameParam.getValue(0)
                saneNSName = namespaceName
                if not nameSanitized:
                    saneNSName = SanitizeSceneGraphLocationString(namespaceName)
                namespaceNameParam = node.getParameter('namespaceName')
                if not namespaceNameParam:
                    namespaceNameParam = node.getParameters().createChildString('namespaceName', '')
                namespaceNameParam.setHintString("{'widget': 'scenegraphLocation'}")
                namespaceNameParam.setValue(saneNSName, 0)
                locationsParam = node.getParameter('locations')
                locationParam = locationsParam.getChildByIndex(0)
                locationParam.setExpression('=^/rootLocation+~/namespaceName')
                outPort.connect(mergeNode.addInputPort('i'))
            Utils.EventModule.QueueEvent('nodegraph_nmc_namespace_create', hash(self), node=node)
            return

    def handleNamespaceDelete(self, node):
        """
        Event handler for C{'node_delete'} and C{'node_setParent'} to clean
        up internal Merge node ports upon removal of a LocationCreate
        namespace node.

        Does nothing if C{node} is not a LocationCreate.

        @type node: C{NodegraphAPI.Node}
        @param node: Deleted node.
        @since: Katana 4.0v1
        """
        if node is None:
            return
        else:
            if node.getType() != 'LocationCreate':
                return
            try:
                Utils.UndoStack.DisableCapture()
                self._cleanMergeNodePorts()
            finally:
                Utils.UndoStack.EnableCapture()

            Utils.EventModule.QueueEvent('nodegraph_nmc_namespace_delete', hash(self), node=node)
            return

    def _cleanMergeNodePorts(self):
        """
        Remove ports on internal Merge that are not connected to anything.
        """
        mergeNode = self._getNodeFromParam('__node_merge')
        if mergeNode is not None:
            inputPorts = mergeNode.getInputPorts()
            for port in inputPorts:
                if port.getNumConnectedPorts() == 0:
                    mergeNode.removeInputPort(port.getName())

        return

    def __on_node_create(self, eventType, eventID, node=None, **kwargs):
        """
        Handler for C{'node_create'} events.

        Any new children of an internal GroupStack node, have their
        B{materialLocation} parameter set to the scene graph location of the
        associated NetworkMaterial.

        @type eventType: C{str}
        @type eventID: C{object}
        @type node: {NodegraphAPI.Node}
        @type kwargs: C{dict}
        @param eventType: Ignored.
        @param eventID: Ignored.
        @param kwargs: Ignored.
        @param node: The newly created node.
        """
        if NodegraphAPI.IsLoading():
            return
        if self.isMarkedForDeletion():
            return
        self.handleNetworkMaterialNodeCreate(node)
        self.handleNamespaceCreate(node)
        networkMaterials = self.getNetworkMaterials()
        for networkMaterial in networkMaterials:
            groupStack = GetNodeFromParam(networkMaterial, '__node_groupStack')
            if not groupStack:
                continue
            if node.getParent() is not groupStack:
                continue
            locationParam = node.getParameter('materialLocation')
            if not locationParam:
                continue
            locationExpr = self._getNetworkMaterialLocationExpr(networkMaterial)
            locationParam.setExpression(locationExpr)

    def __on_node_delete_begin(self, eventType, eventID, node=None, parent=None, **kwargs):
        """
        Handler for C{'node_delete_begin'} events.

        Clean up after NetworkMaterial/LocationCreate nodes are deleted.

        @type eventType: C{str}
        @type eventID: C{object}
        @type node: C{NodegraphAPI.Node}
        @type parent: C{NodegraphAPI.Node}
        @type kwargs: C{dict}
        @param eventType: Ignored.
        @param eventID: Ignored.
        @param node: The newly created node.
        @param parent: Previous parent of deleted node.
        @param kwargs: Ignored.
        """
        if NodegraphAPI.IsLoading():
            return
        else:
            if node is None or parent != self:
                return
            self.handleNetworkMaterialNodeDelete(node)
            self.handleNamespaceDelete(node)
            return

    def __on_node_bypassed(self, eventType, eventID, node=None, **kwargs):
        """
        Handler for C{'node_setBypassed'} events.

        Detect if disabled/enabled node is an internal NetworkMaterial and
        also disable/enable it's associated GroupStack and Material nodes.

        @type eventType: C{str}
        @type eventID: C{object}
        @type node: C{NodegraphAPI.Node}
        @type kwargs: C{dict}
        @param eventType: Ignored.
        @param eventID: Ignored.
        @param kwargs: Ignored.
        @param node: Node that was disabled.
        """
        if node and node.getParent() is self:
            if node.getType() == 'NetworkMaterial':
                materialNode = GetNodeFromParam(node, '__node_materialEdit')
                if materialNode:
                    materialNode.setBypassed(node.isBypassed())
                groupStackNode = GetNodeFromParam(node, '__node_groupStack')
                if groupStackNode:
                    groupStackNode.setBypassed(node.isBypassed())

    def addInputTerminals(self, node):
        """
        Adds terminal input ports for all shader types on all available
        renderer.

        @type node: C{NodegraphAPI.Node}
        @param node: The NetworkMaterial node to add ports to.
        """
        rendererPluginNames = RenderingAPI.RenderPlugins.GetRendererPluginNames()
        if not rendererPluginNames:
            return
        for rendererPluginName in sorted(rendererPluginNames):
            nodeType = '%sShadingNode' % rendererPluginName.capitalize()
            if nodeType not in NodegraphAPI.GetNodeTypes():
                continue
            shaderTypes = RenderingAPI.RenderPlugins.GetRendererShaderTypes(rendererPluginName)
            for shaderType in shaderTypes:
                portName = node.generateShaderInputPortName(rendererPluginName, shaderType)
                port = node.getInputPort(portName)
                if not port:
                    port = node.addShaderInputPort(rendererPluginName, shaderType)
                if port:
                    port.addOrUpdateMetadata('page', rendererPluginName)

    def getConnectedInputPort(self, sendPort):
        """
        Traverse from internal send port through any ancestor Group nodes to
        the eventual connected external output port.

        @type sendPort: C{NodegraphAPI.Port}
        @rtype: C{NodegraphAPI.Port}
        @param sendPort: Internal Group node send port.
        @return: External output port serving given send port.
        @see: L{NodeUtils.GetUpstreamPort()}
        """
        inputPort = self.getInputPort(sendPort.getName())
        return NodeUtils.GetUpstreamPort(inputPort)

    def _createNetworkMaterialUtilNodes(self, networkMaterialNode):
        """
        Create and connect Material and GroupStack nodes for a given
        NetworkMaterial.

        @type networkMaterialNode: C{NodegraphAPI.Node}
        @param networkMaterialNode: NetworkMaterial node.
        @rtype: C{tuple} of C{NodegraphAPI.Node} and C{NodegraphAPI.Node}
        @return: New GroupStack and Material node as a tuple.
        """
        outPort = networkMaterialNode.getOutputPort('out')
        connectedPorts = outPort.getConnectedPorts()
        if len(connectedPorts) != 0:
            return
        nmParamGroup = networkMaterialNode.getParameters()
        groupStack = NodegraphAPI.CreateNode('GroupStack', self)
        groupStackParamNM = nmParamGroup.getChild('__node_groupStack') or nmParamGroup.createChildString('__node_groupStack', '')
        groupStackParamNM.setExpression('@%s' % groupStack.getName())
        materialNode = NodegraphAPI.CreateNode('Material', self)
        materialNodeParamNM = nmParamGroup.getChild('__node_materialEdit') or nmParamGroup.createChildString('__node_materialEdit', '')
        materialNodeParamNM.setExpression('@%s' % materialNode.getName())
        groupStack.getParameters().createChildNumber('__hidden', 1.0).setHintString('{"widget": "null"}')
        materialNode.getParameters().createChildNumber('__hidden', 1.0).setHintString('{"widget": "null"}')
        materialNode.getParameter('action').setValue('edit material', NodegraphAPI.GetCurrentTime())
        groupStack.setChildNodeType('NetworkMaterialInterfaceControls')
        locationExpr = self._getNetworkMaterialLocationExpr(networkMaterialNode)
        locationParam = materialNode.getParameter('edit.location')
        locationParam.setExpression(locationExpr)
        posX, posY = NodegraphAPI.GetNodePosition(networkMaterialNode)
        NodegraphAPI.SetNodePosition(groupStack, (posX, posY - 50))
        NodegraphAPI.SetNodePosition(materialNode, (posX, posY - 100))
        networkMaterialNode.getOutputPort('out').connect(groupStack.getInputPort('in'))
        groupStack.getOutputPort('out').connect(materialNode.getInputPort('in'))
        return (
         groupStack, materialNode)

    @classmethod
    def _invalidateInstanceLayout(cls, nodes):
        """
        Takes a list of nodes generated by a single event handler and
        invalidates the node layout if the node is an instance of this class.

        @type nodes: C{list} of C{NodegraphAPI.Node}
        @param nodes: List of potential nodes to invalidate.
        @see: L{invalidateLayout()}
        """
        for node in nodes:
            if node is None:
                continue
            if isinstance(node, cls):
                node.invalidateLayout()

        return


def on_nodegraph_changed(eventType, eventID, **kwargs):
    """
    Event handler for C{'nodegraph_changed'}.

    Invalidate layout of NetworkMaterialCreate / NetworkMaterialEdit nodes on
    relevant C{'nodegraph_changed'} events.

    @type eventType: C{str}
    @type eventID: C{object}
    @type kwargs: C{dict}
    @param eventType: Ignored.
    @param eventID: Ignored.
    @param kwargs: dict containing arguments of original event that triggered
        the C{'nodegraph_changed'}.
    """
    originalEvent = kwargs.get('originalEventType')
    node = kwargs.get('node')
    nodesToInvalidate = []
    if originalEvent == 'node_setName':
        nodesToInvalidate.extend([node, node.getParent()])
    elif originalEvent in ('port_connect', 'port_disconnect'):
        nodeNameA = kwargs.get('nodeNameA')
        nodeNameB = kwargs.get('nodeNameB')
        nodeA = NodegraphAPI.GetNode(nodeNameA)
        nodeB = NodegraphAPI.GetNode(nodeNameB)
        if nodeA is not None:
            nodesToInvalidate.extend([nodeA, nodeA.getParent()])
        if nodeB is not None:
            nodesToInvalidate.extend([nodeB, nodeB.getParent()])
    elif originalEvent == 'node_shapeAttrsChanged':
        if node is None:
            nodeName = kwargs.get('nodeName')
            node = NodegraphAPI.GetNode(nodeName)
        if node is not None:
            nodesToInvalidate.append(node.getParent())
    elif node is not None:
        nodesToInvalidate.append(node.getParent())
    NetworkMaterialBaseNode._invalidateInstanceLayout(nodesToInvalidate)
    return


def on_node_setParent(eventType, eventID, node, newParent, oldParent, oldParentName, newParentName, **kwargs):
    """
    Event handler for C{'node_setParent'}.

    Invalidates the layout when nodes are moved out/into a
    NetworkMaterialCreate / NetworkMaterialEdit.

    @type eventType: C{str}
    @type eventID: C{object}
    @type node: C{NodegraphAPI.Node}
    @type newParent: C{NodegraphAPI.GroupNode}
    @type oldParent: C{NodegraphAPI.GroupNode}
    @type oldParentName: C{str}
    @type kwargs: C{dict}
    @param eventType: Ignored.
    @param eventID: Ignored.
    @param node: Node that has been re-parented.
    @param newParent: New parent node.
    @param oldParent: Previous parent node.
    @param oldParentName: New parent node's name.
    @param newParentName: Previous parent node's name.
    @param kwargs: Ignored.
    """
    nodesToInvalidate = []
    op = NodegraphAPI.GetNode(oldParentName)
    nodesToInvalidate += [op] if op is not None else []
    op = NodegraphAPI.GetNode(newParentName)
    nodesToInvalidate += [op] if op is not None else []
    NetworkMaterialBaseNode._invalidateInstanceLayout(nodesToInvalidate)
    if node is None:
        return
    else:
        if oldParentName == newParentName:
            return
        if isinstance(oldParent, NetworkMaterialBaseNode):
            oldParent.handleNetworkMaterialNodeDelete(node)
            oldParent.handleNamespaceDelete(node)
        if isinstance(newParent, NetworkMaterialBaseNode):
            namespaceNameParam = node.getParameter('namespaceName')
            if node.getType() == 'LocationCreate' and namespaceNameParam:
                newParent.handleNamespaceCreate(node, namespaceNameParam.getValue(0))
            else:
                newParent.handleNetworkMaterialNodeCreate(node)
        return


def on_node_delete_begin(eventType, eventID, **kwargs):
    """
    Event handler for C{'node_delete_begin'}.

    Invalidates layout when a node is deleted.

    @type eventType: C{str}
    @type eventID: C{object}
    @type kwargs: C{dict}
    @param eventType: Ignored.
    @param eventID: Ignored.
    @param kwargs: Event data dictionary containing the parent node.
    """
    parent = kwargs.get('parent')
    if parent is None:
        return
    else:
        NetworkMaterialBaseNode._invalidateInstanceLayout([parent])
        return


def GetNodeFromParam(node, parameterName):
    """
    Returns the internal node for the given parameter name.

    @type node: C{NodegraphAPI.Node}
    @type parameterName: C{str}
    @rtype: C{NodegraphAPI.Node} or C{None}
    @param node: Node to interrogate.
    @param parameterName: Name of parameter on C{node} to interrogate.
    @return: The internal node referenced in the parameter.
    """
    if not node:
        return None
    else:
        nodeNameParam = node.getParameter(parameterName)
        if not nodeNameParam:
            return None
        result = NodegraphAPI.GetNode(nodeNameParam.getValue(NodegraphAPI.GetCurrentTime()))
        return result


def SanitizeSceneGraphLocationString(sceneGraphLocation):
    """
    This method takes an input string and ensures it can represent a valid
    scene graph location in Katana, also ensuring it begins with a leading '/'.

    See TP 199304.

    @type sceneGraphLocation: C{str}
    @rtype: C{str}
    @param sceneGraphLocation: Potentially invalid scene graph location.
    @return: Sanitized string representing a scene graph location.
    """
    if not sceneGraphLocation or not isinstance(sceneGraphLocation, str):
        return ''
    result = sceneGraphLocationRegex.sub('_', sceneGraphLocation)
    if not re.search('^/', result):
        result = '/' + result
    result = result.rstrip('/')
    return result


def onNodeSetShapeAttributes(eventType, eventID, **kwargs):
    """
    Event handler for C{'node_setShapeAttributes'}.

    Invalidate layout of NetworkMaterialCreate / NetworkMaterialEdit when
    a child node's shape attribtues change.

    @type eventType: C{str}
    @type eventID: C{object}
    @type kwargs: C{dict}
    @param eventType: Ignored.
    @param eventID: Ignored.
    @param kwargs: Event data containing C{node}.
    """
    node = kwargs.get('node')
    if node is None:
        return
    else:
        NetworkMaterialBaseNode._invalidateInstanceLayout([node.getParent()])
        return


Utils.EventModule.RegisterEventHandler(onNodeSetShapeAttributes, eventType='node_setShapeAttributes')
Utils.EventModule.RegisterEventHandler(on_nodegraph_changed, eventType='nodegraph_changed')
Utils.EventModule.RegisterEventHandler(on_node_delete_begin, eventType='node_delete_begin')
Utils.EventModule.RegisterEventHandler(on_node_setParent, eventType='node_setParent')
_Parameter_XML = "\n<group_parameter>\n  <string_parameter name='_rendererContext' value=''/>\n</group_parameter>\n"