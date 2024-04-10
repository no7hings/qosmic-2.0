# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Nov 16 2020, 22:23:17) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: SuperTools/NetworkMaterials/v1/NetworkMaterialEditNode.py
# Compiled at: 2021-06-28 21:25:19
"""
Module defining the L{NetworkMaterialEditNode} class.
"""
import collections, contextlib, logging, operator, re
from Nodes3DAPI.ShadingNodeBase import ShadingNodeBase
from Nodes3DAPI_cmodule import BuildAttrListFromDynamicParameterGroup
from Katana import NodegraphAPI, FnAttribute, Utils, Nodes3DAPI, PyXmlIO, Configuration, UI4, enum, NodeGraphView
from NetworkMaterialBaseNode import NetworkMaterialBaseNode
from NetworkMaterialEditUtil import LayoutNodesSorter, OpArgNodeReferenceSearcher, OpArgPaths, LayoutParameterExtractor, LayoutNodesSearcher
import PyScenegraphAttrFnAttributeBridge as AttrBridge
from SceneGraphLocationListener import SceneGraphLocationListener
log = logging.getLogger('NetworkMaterialEdit.Node')
NodegraphAPI.AddNodeFlavor('NetworkMaterialEdit', '3d')
UpdateStatus = enum.Enum('Succeeded', 'Failed', 'UserCancelled')

class NetworkMaterialEditNode(NetworkMaterialBaseNode):
    """
    Class implementing the NetworkMaterialEdit SuperTool node type.

    @since: Katana 4.0v1
    """

    def __init__(self):
        """
        Initializes an instance of this class.
        """
        self.addInputPort('in')
        NetworkMaterialBaseNode.__init__(self)
        networkMaterialNode = self._getNodeFromParam('__node_networkMaterial')
        genericOpNode = self._getNodeFromParam('__node_genericOp')
        incomingNode = self._getNodeFromParam('__node_incoming')
        networkMaterialNode.getParameter('sceneGraphLocation').setValue('', 0)
        celParam = genericOpNode.getParameter('opArgs').createChildString('CEL', '/root')
        celParam.setExpression(self._getNetworkMaterialLocationExpr(networkMaterialNode), 0)
        celParam.setExpressionFlag(True)
        celParam = incomingNode.getParameter('opArgs').createChildString('CEL', '/root')
        celParam.setExpression(self._getNetworkMaterialLocationExpr(networkMaterialNode), 0)
        celParam.setExpressionFlag(True)
        incomingNode.getParameter('opArgs').createChildNumber('layoutVersion', networkMaterialNode.kNodeGraphViewLayoutVersion)
        self.__eventHandlers = None
        self.__collapsedHandlers = None
        self.__isDeletingMe = None
        self.__isDeletedNodeADescendent = None
        self.__nodeSourceNameLookup = None
        self.__shadingNetworkNodes = None
        self.__queuedNodeGraphEvents = None
        self.__lastUpstreamMaterialHash = None
        self.__upstreamListener = None
        self.__isUndoGroupOpened = None
        self.__isLayoutInitialised = None
        return

    def polish(self):
        """
        This method is automatically called on the SuperTool
        after it has finished loading and initialization.

        It will only be called once.

        Initialize members and event handlers.
        """
        NetworkMaterialBaseNode.polish(self)
        self.__isDeletingMe = False
        self.__isDeletedNodeADescendent = False
        self.__nodeSourceNameLookup = {}
        self.__shadingNetworkNodes = {}
        self.__layoutHash = None
        self.__reconstructionInProgress = False
        self.__isUndoGroupOpened = False
        self.__nodeHashes = {}
        self.__isLayoutInitialised = False
        self.__lastUpstreamMaterialHash = None
        self.__eventHandlers = {('nodegraph_changed', None): self.__onNodeGraphChanged, 
           ('nodegraph_nme_populate_layout', hash(self)): self.__onPopulateLayout}
        self.__collapsedHandlers = {('nodegraph_nme_entered', hash(self)): self.__onEnter, 
           ('nodegraph_nme_reconstruct', hash(self)): self.__onReconstruct, 
           ('node_delete', None): self.__onExternalNodeDelete, 
           ('undo_end', None): self.__onUndoEnd, 
           ('geolib_processingStateChanged', None): self.__onGeolibProcessingStateChanged}
        self.__upstreamListener = None
        Utils.EventModule.RegisterCollapsedHandler(self.__onEnter, eventType='nodegraph_nme_entered', eventID=hash(self))
        return

    def __onUndoEnd(self, eventData):
        """
        Collapsed event handler for C{'undo_end'}.

        After an undo has executed, trigger a C{'event_idle'} to ensure a
        cook is triggered, if required.

        We can then listen for the Geolib state changes and repopulate the
        NME network before allowing the undo stack to move on to the next undo
        event.

        @type eventData: C{tuple} of C{list} of C{dict}
        @param eventData: Unused.
        @see: C{__onGeolibProcessingStateChanged}
        @see: C{Node3D_geolib3.__idleCB}
        """
        if not Utils.UndoStack.IsUndoInProgress():
            return
        Utils.EventModule.QueueEvent('event_idle', 0)

    def __onGeolibProcessingStateChanged(self, eventData):
        """
        Collapsed event handler for C{'geolib_processingStateChanged'}.

        When undo-ing an upstream material change, we need to quickly
        repopulate ready for potential further undo events that are expecting
        the shader network to be in it's previous state.

        @type eventData: C{tuple} of C{list} of C{dict}
        @param eventData: Unused.
        """
        if not Utils.UndoStack.IsUndoInProgress():
            return
        upstreamMaterial = self.__getIncomingMaterialAttributes()
        upstreamHash = upstreamMaterial and upstreamMaterial.getHash()
        if upstreamHash == self.__lastUpstreamMaterialHash:
            return
        Utils.EventModule.QueueEvent('nodegraph_nme_reconstruct', hash(self))

    def handleNetworkMaterialNodeCreate(self, networkMaterialNode):
        """
        Handles the creation of a NetworkMaterial node's utility nodes
        (GroupStack and Material).

        This is called with a newly created NetworkMaterial immediately after
        C{_setupInternalNetwork}.

        @type networkMaterialNode: C{NodegraphAPI.Node}
        @param networkMaterialNode: The NetworkMaterial node being created.
        @since: Katana 4.0v1
        """
        if networkMaterialNode is None:
            return
        else:
            if networkMaterialNode.getType() != 'NetworkMaterial':
                return
            if networkMaterialNode.getParent() != self:
                return
            if self._getNodeFromParam('__node_networkMaterial') is not None:
                return
            groupStack, materialNode = self._createNetworkMaterialUtilNodes(networkMaterialNode)
            paramsGroup = self.getParameters()
            networkMaterialParam = paramsGroup.createChildString('__node_networkMaterial', '')
            networkMaterialParam.setExpression('@%s' % networkMaterialNode.getName())
            groupStackNodeParam = paramsGroup.createChildString('__node_groupStack', '')
            groupStackNodeParam.setExpression('@%s' % groupStack.getName())
            materialNodeParam = paramsGroup.createChildString('__node_materialEdit', '')
            materialNodeParam.setExpression('@%s' % materialNode.getName())
            if networkMaterialNode.getNumInputPorts() == 0:
                self.addInputTerminals(networkMaterialNode)
            genericOpNode = self._getNodeFromParam('__node_genericOp')
            x, y = NodegraphAPI.GetNodePosition(groupStack)
            NodegraphAPI.SetNodePosition(genericOpNode, (x, y + 50))
            genericOpNode.getOutputPort('out').connect(groupStack.getInputPort('in'))
            materialNode.getOutputPort('out').connect(self.getReturnPort('out'))
            return

    def _setupInternalNetwork(self):
        """
        Connect the internal utility nodes to the group's send & return ports.

        Note that the NetworkMaterial node (and hence it's associated
        GroupStack and Material) is not yet created when this method is called.
        """
        paramsGroup = self.getParameters()
        incomingNode = NodegraphAPI.CreateNode('GenericOp', self)
        incomingNode.addInputPort('in')
        incomingNode.setName('_nme_incoming_node')
        incomingNode.getParameters().createChildNumber('__hidden', 1.0).setHintString('{"widget": "null"}')
        incomingNodeParam = paramsGroup.createChildString('__node_incoming', '')
        incomingNodeParam.setExpression('@%s' % incomingNode.getName())
        incomingNode.getParameter('opType').setValue('NetworkMaterialLayout', 0)
        genericOpNode = NodegraphAPI.CreateNode('GenericOp', self)
        genericOpNode.addInputPort('in')
        genericOpNodeParam = paramsGroup.createChildString('__node_genericOp', '')
        genericOpNode.getParameters().createChildNumber('__hidden', 1.0).setHintString('{"widget": "null"}')
        genericOpNodeParam.setExpression('@%s' % genericOpNode.getName())
        genericOpNode.getParameter('opType').setValue('NetworkMaterialEdit', 0)
        incomingNode.getInputPortByIndex(0).connect(self.getSendPort('in'))
        genericOpNode.getInputPort('in').connect(incomingNode.getOutputPort('out'))

    def getNetworkMaterials(self):
        """
        Get the (only) NetworkMaterial node.

        @rtype: C{list} of C{NodegraphAPI.Node}
        @return: List containing a single element, the internal
            NetworkMaterial.
        @since: Katana 4.0v1
        """
        return [
         self._getNodeFromParam('__node_networkMaterial')]

    def __getPersistentNodes(self):
        """
        Get nodes that should not be deleted when the NetworkMaterialEdit
        contents are cleared pending a re-population.

        @rtype: C{list} of C{NodegraphAPI.Node}
        @return: List of persistent nodes.
        """
        persistentNodes = self._getExcludedNodes() | set(self.getNetworkMaterials())
        return persistentNodes

    def isChildNodePersistent(self, node):
        """
        Check if given node should not be deleted when the NetworkMaterialEdit
        contents are cleared pending a re-population.

        @type node: C{NodegraphAPI.Node}
        @rtype: C{bool}
        @param node: Node to check.
        @return: C{True} if C{node} is persistent, C{False} otherwise.
        """
        persistentNodes = self.__getPersistentNodes()
        if node in persistentNodes:
            return True
        return False

    def getContentsLayoutAttributes(self, **kwargs):
        """
        Construct the layout attributes of child nodes (and their descendents)

        @rtype: C{FnAttribute.GroupAttribute}
        @param kwargs: Ignored
        @return: Layout attributes
        """
        return Nodes3DAPI.NodeLayoutAttributes.LayoutAttributesMixin.getContentsLayoutAttributes(self, nodeNames=self.__nodeSourceNameLookup)

    def getNodeStates(self):
        """
        Returns the "EditState" of all the internal interactive child nodes
        of this node.

        @rtype: C{dict}
        @return: A dictionary of all child nodes keyed on their
            current "EditState".
        """
        addedNodeNames, editedNodeNames, disconnectedNodeNames = self.__findEditedNodeNames()
        editedNodeSet = set(filter(None, map(self.getNodeFromSourceNodeName, editedNodeNames)))
        addedNodeSet = set(filter(None, map(self.getNodeFromSourceNodeName, addedNodeNames)))
        disconnectedNodeSet = set(filter(None, map(self.getNodeFromSourceNodeName, disconnectedNodeNames)))
        return {NodeGraphView.NodeEdited: editedNodeSet, 
           NodeGraphView.NodeAdded: addedNodeSet, 
           NodeGraphView.NodeDisconnected: disconnectedNodeSet}

    def getNodeFromSourceNodeName(self, nodeName):
        """
        Get node within NetworkMaterialEdit that mirrors upstream node with
        given name.

        @type nodeName: C{str}
        @rtype: C{NodegraphAPI.Node} or C{None}
        @param nodeName: Upstream node's name.
        @return: Local node that mirrors node with given name, or C{None} if
            not found.
        """
        result = self.getChild(nodeName)
        if result is None:
            result = self.__shadingNetworkNodes.get(nodeName, None)
        return result

    def __getSourceNodeNameFromNode(self, node):
        """
        Get the name of the upstream node that the given node mirrors.

        @type node: C{NodegraphAPI.Node}
        @rtype: C{str} or C{None}
        @param node: Node to query.
        @return: Upstream node's name, or C{None} if not found.
        """
        return self.__nodeSourceNameLookup.get(node)

    def _buildAttrFromGroupParam(self, param, multiSampleDefault=False):
        """
        Convert a C{Parameter} to a C{GroupAttribue}.

        @type param: C{NodegraphAPI.Parameter}
        @type multiSampleDefault: C{bool}
        @rtype: C{FnAttribute.GroupAttribute}
        @param param: Group parameter to convert.
        @param multiSampleDefault: Enable/disable multisampling.
        @return: C{GroupAttribute} mirroring given C{Parameter} group.
        """
        gs = self.getGraphState() or NodegraphAPI.GetCurrentGraphState()
        return NodegraphAPI.BuildAttrFromGroupParameter(param, gs, multisampleDefault=multiSampleDefault)

    def _buildDataAttrFromGroupParam(self, param, multiSampleDefault=False):
        """
        Converts a group C{Parameter} containing the C{'enable'}, C{'type'},
        and C{'value'} parameters to C{FnAttribute.DataAttribute}.

        @type param: C{NodegraphAPI.Parameter}
        @type multiSampleDefault: C{bool}
        @rtype: C{FnAttribute.DataAttribute}
        @param param: Group parameter to convert.
        @param multiSampleDefault: Enable/disable multisampling.
        @return: C{FnAttribute.DataAttribute} mirroring the given C{Parameter}
            group.
        @raise RuntimeError: If unable to convert parameter to attribute.
        @since: Katana 3.6v5
        """
        paramName = param.getName()
        parent = param.getParent()
        if parent is not None:
            gs = self.getGraphState() or NodegraphAPI.GetCurrentGraphState()
            attrList = BuildAttrListFromDynamicParameterGroup(groupParam=parent, graphState=gs, multisampleDefault=multiSampleDefault)
            for name, attr in attrList:
                if name == paramName:
                    return AttrBridge.scenegraphAttrToAttr(attr)

        raise RuntimeError(('Unable to convert "{}" parameter to FnAttribute').format(paramName))
        return

    def __updateOpArgsFromAttr(self, attr):
        """
        Update NetworkMaterialEdit op args parameter from given attribute.

        Enssures B{CEL} parameter remains an expression.

        @type attr: C{FnAttribute.GroupAttribute}
        @param attr: Op args to set.
        """
        genericOpNode = self._getNodeFromParam('__node_genericOp')
        with NodegraphAPI.UnlockedNode(genericOpNode):
            genericOpNode.updateArgsParametersFromAttr(attr)
            networkMaterialNode = self._getNodeFromParam('__node_networkMaterial')
            celParam = genericOpNode.getParameter('opArgs.CEL')
            celParam.setExpression(self._getNetworkMaterialLocationExpr(networkMaterialNode), 0)
            celParam.setExpressionFlag(True)
            incomingNode = self._getNodeFromParam('__node_incoming')
            celParam = incomingNode.getParameter('opArgs.CEL')
            celParam.setExpression(self._getNetworkMaterialLocationExpr(networkMaterialNode), 0)
            celParam.setExpressionFlag(True)

    def _getGenericOpArgs(self):
        """
        Get the op args passed to the internal GenericOp as a
        C{GroupAttribute}.

        @rtype: C{FnAttribute.GroupAttribute}
        @return: GenericOp's op args.
        """
        genericOpNode = self._getNodeFromParam('__node_genericOp')
        if not genericOpNode:
            return None
        else:
            return self._buildAttrFromGroupParam(genericOpNode.getParameter('opArgs'))

    def _getExcludedNodes(self):
        """
        Get the list of nodes that should be excluded from
        C{material.B{layout}} attributes.

        Augment base class list with internal GenericOp and Dot sentinel nodes.

        @rtype: C{set} of C{NodegraphAPI.Node}
        @return: List of internal hidden nodes.
        """
        return NetworkMaterialBaseNode._getExcludedNodes(self) | {
         self._getNodeFromParam('__node_genericOp'),
         self._getNodeFromParam('__node_incoming')}

    def __onEnter(self, eventData):
        """
        Event Handler for C{'nodegraph_nme_entered'} events. Triggered when the
        user clicks the "Enter" button on an NME node in the B{Node Graph} tab.

        @type eventData: C{list} of C{dict}
        @param eventData: List of event info.
        """
        if self.__reconstructionInProgress:
            return
        kwargses = [ kwargs for _, _, kwargs in eventData if not self.__isChildNode(kwargs['previousNodeView'])
                   ]
        if not kwargses:
            return
        else:
            isFirstEntry = self.__lastUpstreamMaterialHash is None
            status = self.__updateContents()
            if status is UpdateStatus.Failed:
                self.__invalidMaterialLocationMsg()
            elif status is UpdateStatus.UserCancelled:
                parent = self.getParent()
                if parent:
                    for kwargs in kwargses:
                        Utils.EventModule.QueueEvent('nodegraph_setNodeView', kwargs['nodeGraphWidgetId'], node=parent)

            elif status is UpdateStatus.Succeeded:
                if isFirstEntry:
                    Utils.EventModule.QueueEvent('nodegraph_nme_generated', hash(self))
                self.__validMaterialLocationMsg()
            return

    def __onReconstruct(self, eventData):
        """
        Event handler for C{'nodegraph_nme_reconstruct'}.

        Update NME contents and potentially display error banner.

        @type eventData: C{list} of C{dict}
        @param eventData: Ignored.
        """
        if self.__reconstructionInProgress:
            return
        status = self.__updateContents()
        if status is UpdateStatus.Failed:
            self.__invalidMaterialLocationMsg()
        elif status is UpdateStatus.Succeeded:
            self.__validMaterialLocationMsg()

    def __invalidateOnSceneGraphLocationChange(self, node=None, param=None, **kwargs):
        """
        Trigger C{'nodegraph_nme_invalidate'} if C{param} is the
        B{sceneGraphLocation} parameter of the internal NetworkMaterial node.

        @type node: C{NodegraphAPI.Node}
        @type param: C{NodegraphAPI.Parameter}
        @type kwargs: C{dict}
        @rtype: C{bool}
        @param node: Potential internal NetworkMaterial node.
        @param param: Potential B{sceneGraphLocation} parameter.
        @param kwargs: Ignored.
        @return: C{True} if contents were invalidated, C{False} otherwise.
        """
        if not param:
            return False
        else:
            if param.getName() == 'sceneGraphLocation' and self.__isInternalNetworkMaterialNode(node):
                self.__lastUpstreamMaterialHash = None
                Utils.EventModule.QueueEvent('nodegraph_nme_invalidate', hash(self), invalidateAll=True)
                return True
            return False

    def __populateFromInputMaterial(self, incomingMaterial, materialAttr):
        """
        Create nodes in the NetworkMaterialEdit using the C{material.B{layout}}
        attributes of this NME's NetworkMaterial.

        @type incomingMaterial: C{PyFnScenegraphAttr.GroupAttr}
        @type materialAttr: C{PyFnScenegraphAttr.GroupAttr}
        @rtype: C{bool}
        @param incomingMaterial: Upstream B{material} attribute.
        @param materialAttr: B{material} attribute of this NME's
            NetworkMaterial.
        @return: C{True} if population succeeded, C{False} if failed.
        """
        self.__reconstructionInProgress = True
        nmcNetworkMaterialNodeNameAttr = materialAttr.getChildByName('info.name')
        if nmcNetworkMaterialNodeNameAttr is None:
            return False
        else:
            nmcNetworkMaterialNodeName = nmcNetworkMaterialNodeNameAttr.getValue()
            layoutAttr = materialAttr.getChildByName('layout')
            if layoutAttr is None:
                return False
            parentAttr = layoutAttr.getChildByName('%s.parent' % nmcNetworkMaterialNodeName)
            if parentAttr is None:
                return False
            nmcName = parentAttr.getValue()
            self.__nodeSourceNameLookup[self] = nmcName
            opArgs = self._getGenericOpArgs()
            layoutAttr = materialAttr.getChildByName('layout')
            totalNodes = layoutAttr.getNumberOfChildren()
            progressCallback = _GetUpdateProgressCallback(totalNodes)
            orderedNodeNames = LayoutNodesSorter(layoutAttr).build()
            paramExtractor = LayoutParameterExtractor(opArgs, orderedNodeNames)
            try:
                for i in range(totalNodes):
                    nodeName = orderedNodeNames[i]
                    nodeLayoutAttr = layoutAttr.getChildByName(nodeName)
                    node = self.__createNodeFromLayoutAttr(paramExtractor, nodeName, nodeLayoutAttr)
                    if node:
                        self.__shadingNetworkNodes[nodeName] = node
                        self.__nodeSourceNameLookup[node] = nodeName
                        progress = progressCallback(i)
                        if not progress:
                            self.__clearContents()
                            return False

                Utils.EventModule.ProcessAllEvents()
                self.__connectNodes(layoutAttr)
                Utils.EventModule.ProcessAllEvents()
                self.__setMaterialLocationCallbackOnNodes(incomingMaterial)
                self.__lockNonContributingNodes(materialAttr, orderedNodeNames)
                self.__reconstructionInProgress = False
                self.invalidateLayout()
                sourceLayoutVersionAttr = materialAttr.getChildByName('info.sourceLayoutVersion')
                nodesToLayout = paramExtractor.getSparseNodes('position')
                viewState = None
                if sourceLayoutVersionAttr is not None and sourceLayoutVersionAttr.getValue() == 0:
                    nodesToLayout = self.__shadingNetworkNodes.values()
                    viewState = 1.0
                if nodesToLayout:
                    self.__autoLayoutShadingNetworkNodes(nodesToLayout, viewState)
                Utils.EventModule.QueueEvent('nodegraph_nme_populate_layout', hash(self))
                return True
            finally:
                self.__reconstructionInProgress = False
                progressCallback(totalNodes)

            return

    def invalidateLayout(self):
        """
        Flag that C{material.B{layout}} attributes need to be reconstructed.

        Override base class to prevent cooking layout attributes if NME is
        currently populating.
        """
        if self.__reconstructionInProgress:
            return
        NetworkMaterialBaseNode.invalidateLayout(self)

    def __clearNetworkMaterialConnections(self):
        """
        Disconnect all input ports on internal NetworkMaterial.
        """
        networkMaterialNode = self._getNodeFromParam('__node_networkMaterial')
        for inputPort in networkMaterialNode.getInputPorts():
            outputPort = inputPort.getConnectedPort(0)
            if outputPort:
                outputPort.disconnect(inputPort)

    def __clearContents(self):
        """
        Reset the NME, deleting all non-persistent nodes.
        """
        self.__shadingNetworkNodes = {}
        self.__isDeletedNodeADescendent = True
        persistentNodes = self.__getPersistentNodes()
        for node in self.getChildren():
            if node not in persistentNodes:
                node.setLocked(False)
                node.delete()

        self.__clearNetworkMaterialConnections()
        self.__lastUpstreamMaterialHash = None
        return

    def __updateContents(self):
        """
        Updates the interactive nodes of the NME from its source,
        if one is required.

        @rtype: C{NetworkMaterialEditNode.UpdateStatus}
        @return: The resulting status following the attempted update.
        """
        with self.__ignoreChanges():
            upstreamMaterial = self.__getIncomingMaterialAttributes()
            producer = self.__getEditedGeometryProducer()
            materialAttr = None
            if producer is not None:
                materialAttr = producer.getGlobalAttribute('material')
            status = UpdateStatus.Succeeded
            if not upstreamMaterial or not materialAttr or producer.getType() == 'error':
                self.__clearContents()
                status = UpdateStatus.Failed
            elif upstreamMaterial.getHash() != self.__lastUpstreamMaterialHash:
                self.__clearContents()
                populated = self.__populateFromInputMaterial(upstreamMaterial, materialAttr)
                if not populated:
                    status = UpdateStatus.UserCancelled
            if status == UpdateStatus.UserCancelled:
                self.__lastUpstreamMaterialHash = None
            else:
                self.__lastUpstreamMaterialHash = materialAttr and upstreamMaterial and upstreamMaterial.getHash()
            self.__notifyUpdated()
            return status
        return

    def __notifyUpdated(self):
        """
        Trigger C{'nodegraph_nme_updated'} event.
        """
        Utils.EventModule.QueueEvent('nodegraph_nme_updated', hash(self), node=self)

    @contextlib.contextmanager
    def __ignoreChanges(self):
        """
        Context manager to temporarily disable
        * Event handlers.
        " Redraws of the B{Node Graph}.
        * Undo event capturing.
        * Locked state of any C{GroupNode} (i.e. LiveGroup) ancestors of this
            NME.
        """
        self.__unregisterEventHandlers()
        Utils.EventModule.QueueEvent('nodegraph_pauseRedraw', 0)
        Utils.UndoStack.DisableCapture()
        lockedAncestors = []
        ancestor = self
        while ancestor is not None:
            if ancestor.isLocked():
                lockedAncestors.append(ancestor)
                ancestor.setLocked(False)
            ancestor = ancestor.getParent()

        try:
            yield
        finally:
            for ancestor in lockedAncestors:
                ancestor.setLocked(True)

            Utils.UndoStack.EnableCapture()
            Utils.EventModule.QueueEvent('nodegraph_resumeRedraw', 0)
            self.__registerEventHandlers()

        return

    def __getIncomingMaterialAttributes(self):
        """
        Get B{material} attribute of upstream NetworkMaterial.

        @rtype: C{FnAttribute.GroupAttribute}
        @return: B{material} attribute.
        """
        internalNode = self._getNodeFromParam('__node_incoming')
        return self.__getMaterialAttributesOfNode(internalNode)

    def __getEditedGeometryProducer(self):
        """
        Get a C{GeometryProducer} for querying attributes on edited network.

        @rtype: C{GeoAPI.GeometryProducer}
        @return: C{GeometryProducer} viewing internal GenericOp node.
        """
        internalNode = self._getNodeFromParam('__node_genericOp')
        return self.__getGeometryProducer(internalNode)

    def __getMaterialAttributesOfNode(self, node):
        """
        Get the (global) B{material} attribute as viewed from given C{node}.

        @type node: C{NodegraphAPI.Node}
        @param node: Node to view attributes at.
        @rtype: C{PyFnScenegraphAttr.GroupAttr} or C{None}
        @return: B{material} attributes, or C{None} if an appropriate
            C{GeometryProducer} cannot be created.
        """
        producer = self.__getGeometryProducer(node)
        if not producer:
            return None
        else:
            return producer.getGlobalAttribute('material')

    def __getGeometryProducer(self, node):
        """
        Get a C{GeometryProducer} for querying B{material} attributes.

        @type node: C{NodegraphAPI.Node}
        @param node: Node to view attributes at.
        @rtype: C{GeoAPI.GeometryProducer} or C{None}
        @return: C{GeometryProducer} for node, or C{None} if no appropriate
            B{material} attribute exists at C{node}.
        """
        materialLocation = self.getScenegraphLocation()
        producer = Nodes3DAPI.GetGeometryProducer(node)
        if not producer:
            return None
        else:
            producer = producer.getProducerByPath(materialLocation)
            if not producer:
                return None
            materialAttr = producer.getGlobalAttribute('material')
            if materialAttr and not materialAttr.getChildByName('layout'):
                return None
            return producer

    def __createNodeFromLayoutAttr(self, paramExtractor, nodeName, nodeLayoutAttr):
        """
        Create a node from it's C{material.B{layout}} attribute.

        @type paramExtractor: C{LayoutParameterExtractor}
        @type nodeName: C{str}
        @type nodeLayoutAttr: C{PyFnScenegraphAttr.GroupAttr}
        @rtype: C{NodegraphAPI.Node} or C{None}
        @param paramExtractor: Utility object to extract node parameters from
            B{layout} attribute.
        @param nodeName: Name to set on the node when constructing.
        @param nodeLayoutAttr: B{layout} attribute.
        @return: Newly created node, or C{None} if creation failed.
        """
        nodeType = nodeLayoutAttr.getChildByName('katanaNodeType')
        parent = nodeLayoutAttr.getChildByName('parent')
        if not nodeType or not parent:
            return None
        parentNode = self.__shadingNetworkNodes.get(parent.getValue(), self)
        if nodeType.getValue() == 'NetworkMaterial':
            node = self._getNodeFromParam('__node_networkMaterial')
        else:
            if nodeType.getValue() == 'GroupStack':
                return None
            if nodeType.getValue() == 'Material':
                return None
            node = NodegraphAPI.CreateNode(nodeType.getValue(), parentNode)
        if not node:
            return None
        else:
            disabledAttr = nodeLayoutAttr.getChildByName('disabled')
            if disabledAttr:
                node.setBypassed(bool(disabledAttr.getValue(0)))
            node.setName(nodeName)
            paramExtractor.extractAndSetOnNode(node, nodeLayoutAttr, nodeName)
            nodeUserParams = nodeLayoutAttr.getChildByName('userParameters')
            _ExtractUserParameters(node, nodeUserParams)
            if nodeType.getValue() == 'ShadingGroup':
                outputPorts = nodeLayoutAttr.getChildByName('nodeSpecificAttributes.outputPorts')
                inputPorts = nodeLayoutAttr.getChildByName('nodeSpecificAttributes.inputPorts')
                _ExtractShadingGroupPorts(outputPorts, inputPorts, node, nodeName)
            elif nodeType.getValue() == 'Switch':
                activePort = nodeLayoutAttr.getChildByName('nodeSpecificAttributes.in')
                if activePort:
                    node.getParameter('in').setValue(activePort.getValue(), 0)
            elif nodeType.getValue() == 'VariableSwitch':
                variableName = nodeLayoutAttr.getChildByName('nodeSpecificAttributes.variableName')
                if variableName:
                    node.getParameter('variableName').setValue(variableName.getValue(), 0)
                patterns = nodeLayoutAttr.getChildByName('nodeSpecificAttributes.patterns')
                if patterns:
                    for i in range(patterns.getNumberOfChildren()):
                        childName = patterns.getChildName(i)
                        childAttr = patterns.getChildByIndex(i)
                        node.addInputPort(childName)
                        patternsAttr = node.getParameter('patterns')
                        patternsAttr.getChild(childName).setValue(childAttr.getValue(), 0)

            elif nodeType.getValue() == 'ShadingNodeArrayConnector':
                inputPorts = nodeLayoutAttr.getChildByName('nodeSpecificAttributes.inputs.inputPortNames')
                inputPortDisplayNames = nodeLayoutAttr.getChildByName('nodeSpecificAttributes.inputs.inputPortDisplayNames')
                if inputPorts and inputPortDisplayNames:
                    inputPortNames = inputPorts.getData()
                    inputPortDisplayNames = inputPortDisplayNames.getData()
                    displayNamesValid = len(inputPortNames) == len(inputPortDisplayNames)
                    for i, name in enumerate(inputPortNames):
                        inputPort = node.addInputPort(name)
                        if displayNamesValid:
                            inputPort.addOrUpdateMetadata('label', inputPortDisplayNames[i])

            nodeShapeAttrs = {'displayName': nodeName}
            nodeShapeAttrsAttr = nodeLayoutAttr.getChildByName('nodeShapeAttributes')
            if nodeShapeAttrsAttr:
                for i in range(nodeShapeAttrsAttr.getNumberOfChildren()):
                    childName = nodeShapeAttrsAttr.getChildName(i)
                    childAttr = nodeShapeAttrsAttr.getChildByIndex(i)
                    nodeShapeAttrs[childName] = childAttr.getValue()

            NodegraphAPI.SetNodeShapeNodeAttrs(node, nodeShapeAttrs)
            Utils.EventModule.QueueEvent('node_setShapeAttributes', hash(node), node=node)
            return node

    def __getIncomingNodeAndLocation(self):
        """
        Get the internal Dot sentinel node at the entrance to the
        NetworkMaterialEdit as well as the internal NetworkMaterial's
        B{sceneGraphLocation} parameter value.

        Used by shading nodes to populate their default parameters from the
        upstream attributes.

        @rtype: C{tuple} of C{NodegraphAPI.Node} and C{str}
        @return: Tuple containing the Dot sentinel node and the
            B{sceneGraphLocation} value.
        """
        return (
         self._getNodeFromParam('__node_incoming'),
         self.getScenegraphLocation())

    def __connectNodes(self, layoutAttr):
        """
        Connect up nodes using layout attributes.

        @type layoutAttr: C{PyFnScenegraphAttr.GroupAttr}
        @param layoutAttr: C{material.B{layout}} attribute.
        """
        for i in range(layoutAttr.getNumberOfChildren()):
            nodeName = layoutAttr.getChildName(i)
            node = self.__shadingNetworkNodes.get(nodeName)
            if not node:
                continue
            nodeType = layoutAttr.getChildByName('%s.katanaNodeType' % nodeName)
            if nodeType.getValue() == 'ShadingGroup':
                returnConnections = layoutAttr.getChildByName('%s.nodeSpecificAttributes.returnConnections' % nodeName)
                if returnConnections:
                    for connection in returnConnections.getNearestSample(0):
                        toPortName, fromPortName, fromNodeName = re.match('(.*?):(.*?)@(.*)', connection).groups()
                        fromNode = self.__shadingNetworkNodes[fromNodeName]
                        fromPort = None
                        if fromNode:
                            fromPort = fromNode.getOutputPort(fromPortName)
                        if fromNode is not None and fromPort is None:
                            fromPort = fromNode.addOutputPort(fromPortName)
                        if fromNode is node:
                            fromPort = fromNode.getSendPort(fromPortName)
                        toPort = node.getReturnPort(toPortName)
                        if toPort and fromPort:
                            toPort.connect(fromPort)

            connections = layoutAttr.getChildByName('%s.connections' % nodeName)
            if connections:
                for connection in connections.getNearestSample(0):
                    toPortName, fromPortName, fromNodeName = re.match('(.*?):(.*?)@(.*)', connection).groups()
                    fromNode = self.__shadingNetworkNodes[fromNodeName]
                    if fromNode:
                        fromPort = fromNode.getOutputPort(fromPortName)
                        if fromNode is node.getParent():
                            fromPort = fromNode.getSendPort(fromPortName)
                        elif fromPort is None:
                            fromPort = fromNode.addOutputPort(fromPortName)
                        toPort = node.getInputPort(toPortName)
                        if toPort is None:
                            toPort = node.addInputPort(toPortName)
                        if toPort and fromPort:
                            toPort.connect(fromPort)

        return

    def __setMaterialLocationCallbackOnNodes(self, upstreamMaterial):
        """
        Set C{upstreamMaterialCB} callback function on shading nodes within
        this NetworkMaterialEdit that mirror upstream nodes.

        Used when cooking to populate default parameter values.

        @type upstreamMaterial: C{PyFnScenegraphAttr.GroupAttr}
        @param upstreamMaterial: B{material} attribute of the upstream
            NetworkMaterial.
        """
        upstreamLayout = upstreamMaterial.getChildByName('layout')
        upstreamNodeNames = {upstreamLayout.getChildName(childIdx) for childIdx in xrange(upstreamLayout.getNumberOfChildren())}
        for nodeName, node in self.__shadingNetworkNodes.iteritems():
            if nodeName in upstreamNodeNames and isinstance(node, ShadingNodeBase):
                node.upstreamMaterialCB = self.__getIncomingNodeAndLocation

    def __lockNonContributingNodes(self, materialAttr, layoutNodeNames):
        """
        Lock all nodes within this NetworkMaterialEdit that mirror upstream
        nodes and are not contributing to the NetworkMaterial.

        @type materialAttr: C{PyFnScenegraphAttr.GroupAttr}
        @type layoutNodeNames: C{list} of C{str}
        @param materialAttr: C{B{material}} attributes of edited network.
        @param layoutNodeNames: Names of nodes to consider.
        """
        nodesAttr = materialAttr.getChildByName('nodes')
        contributingNodeNames = set()
        if nodesAttr:
            for _, attr in nodesAttr.childList():
                srcNameAttr = attr.getChildByName('srcName')
                if srcNameAttr:
                    contributingNodeNames.add(srcNameAttr.getValue())

        genericOpArgs = self._getGenericOpArgs()
        unlockedNodeNames = set()
        if genericOpArgs:
            opArgSearcher = OpArgNodeReferenceSearcher(genericOpArgs, layoutNodeNames)
            unlockedNodeNames |= opArgSearcher.getAddedNodeNames()
        unlockedNodeNames |= contributingNodeNames
        for nodeName in reversed(layoutNodeNames):
            node = self.__shadingNetworkNodes.get(nodeName)
            if not node:
                continue
            nodeType = node.getType()
            lockNode = True
            if nodeType in ('Dot', 'Switch', 'NetworkMaterial', 'VariableSwitch', 'Backdrop'):
                lockNode = False
            elif nodeName in unlockedNodeNames:
                lockNode = False
            elif nodeType == 'ShadingGroup':
                for childNode in node.getChildren():
                    sourceName = self.__nodeSourceNameLookup.get(childNode)
                    if sourceName in unlockedNodeNames:
                        lockNode = False
                        unlockedNodeNames.add(nodeName)

            elif nodeType == 'ShadingNodeArrayConnector':
                outputPort = node.getOutputPort('out')
                shaderPorts = []
                _traverseDownstreamOfOutputPort(outputPort, shaderPorts)
                for port in shaderPorts:
                    srcNode = port.getNode()
                    sourceName = self.__nodeSourceNameLookup.get(srcNode)
                    if sourceName in unlockedNodeNames:
                        lockNode = False

            node.setLocked(lockNode)

    def getScenegraphLocation(self, frameTime=None):
        """
        This implementation ensures that the default value of the
        "sceneGraphLocation" parameter is always used for a
        NetworkMaterialEdit node.

        @type frameTime: C{float} or C{None}
        @rtype: C{str}
        @param frameTime: The frame time at which to evaluate the parameter
            that determines this function's result, or C{None} to evaluate the
            parameter at the current time (meaning the result of
            C{NodegraphAPI.GetCurrentTime()}).
        @return: The path of the scene graph location that this node primarily
            works with.
        """
        networkMaterialNode = self._getNodeFromParam('__node_networkMaterial')
        if not networkMaterialNode:
            return ''
        else:
            sgLocParam = networkMaterialNode.getParameter('sceneGraphLocation')
            if not sgLocParam:
                return ''
            if frameTime is None:
                frameTime = NodegraphAPI.GetCurrentTime()
            return sgLocParam.getValue(frameTime)

    def __isChildNode(self, node):
        """
        Return whether given node is a descendent of this NetworkMaterialEdit.

        @type node: C{NodegraphAPI.Node}
        @rtype: C{bool}
        @param node: Node to check.
        @return: C{True} if C{node} is a descendent, C{False} otherwise.
        """
        if not node:
            return False
        if node.getParent() is self:
            return True
        return self.__isChildNode(node.getParent())

    def __onNodeGraphChanged(self, eventType, eventID, **kwargs):
        """
        Queues relevant C{'nodegraph_changed'} events for later processing.

        @type eventType: C{str}
        @type eventID: C{object}
        @type kwargs: C{dict}
        @param eventType: Ignored.
        @param eventID: Ignored.
        @param kwargs: Event data.
        """
        originalEventType = kwargs.get('originalEventType')
        if self.__isSceneGraphLocationChangeEvent(originalEventType, kwargs):
            self.__lastUpstreamMaterialHash = None
            Utils.EventModule.QueueEvent('nodegraph_nme_invalidate', hash(self), invalidateAll=True)
            return
        else:
            if Utils.UndoStack.IsUndoInProgress():
                if originalEventType == 'node_create':
                    self.__onNodeCreateDuringUndo(kwargs['node'])
                self.__notifyUpdated()
                return
            if not self.__isRelevantEvent(originalEventType):
                return
            node = self.__getNodeFromKwargs(kwargs)
            if node is None:
                return
            if originalEventType == 'node_delete' and node is self:
                self.__unregisterEventHandlers()
                return
            if not self.__isUndoGroupOpened:
                return
            if not self.__shadingNetworkNodes:
                return
            if not self.__isRelevantNodeEvent(node, originalEventType, kwargs):
                return
            kwargs['node'] = node
            self.__queuedNodeGraphEvents.append(kwargs)
            return

    def __onNodeCreateDuringUndo(self, node):
        """
        Handle undoing node deletion in NME.

        Check if created node was deleted in NME and update lookup dicts.

        @type node: C{NodegraphAPI.Node}
        @param node: Newly created node
        """
        if not self.__isChildNode(node):
            return
        else:
            nodeNameParam = node.getParameter('name')
            if nodeNameParam is None:
                return
            nodeName = nodeNameParam.getValue(NodegraphAPI.GetCurrentTime())
            deletedNode = self.__shadingNetworkNodes.get(nodeName)
            if deletedNode is None:
                return
            if not deletedNode.isMarkedForDeletion():
                return
            self.__shadingNetworkNodes[nodeName] = node
            deletedName = self.__nodeSourceNameLookup.get(deletedNode)
            if deletedName == nodeName:
                del self.__nodeSourceNameLookup[deletedNode]
                self.__nodeSourceNameLookup[node] = nodeName
            return

    def __onExternalNodeDelete(self, eventData):
        """
        Collapsed event handler for C{'node_delete'} events.

        If a deleted node is external to the NetworkMaterialEdit, delete
        any op args that refer to it.

        @type eventData: C{list} of C{dict}
        @param eventData: List of event info.
        """
        if self.__isDeletedNodeADescendent:
            return
        else:
            if Utils.UndoStack.IsUndoInProgress():
                return
            nodeNames = [ kwargs.get('oldName') for _, _, kwargs in eventData ]
            genericOpNode = self._getNodeFromParam('__node_genericOp')
            opArgs = self._getGenericOpArgs()
            if opArgs is None:
                return
            nodeReferenceSearcher = OpArgNodeReferenceSearcher(opArgs, nodeNames)
            blackListByArgPath = nodeReferenceSearcher.getReferencesByArgPath()
            if not blackListByArgPath:
                return
            gb = FnAttribute.GroupBuilder()
            gb.update(opArgs)
            nodeReferenceSearcher.deleteFromGroupAttr(gb, blackListByArgPath)
            Utils.UndoStack.OpenGroup('%s updated material' % self.getName())
            try:
                self.__updateOpArgsFromAttr(gb.build())
            finally:
                Utils.UndoStack.CloseGroup()

            return

    def __invalidMaterialLocationMsg(self):
        """
        Trigger a C{'nodegraph_stateLabel'} event with an error message
        payload.

        Use the error reported by at the scene graph location if available,
        otherwise set a message instructing the user to set a valid
        B{sceneGraphLocation} parameter value.
        """
        if self.isLocked(True):
            return
        producer = self.__getEditedGeometryProducer()
        if producer and producer.getType() == 'error':
            msg = producer.getGlobalAttribute('errorMessage').getValue()
        else:
            msg = 'Set the location parameter to the path of a Network Material scene graph location to edit.'
        Utils.EventModule.QueueEvent('nodegraph_stateLabel', hash(self), text=msg)

    def __validMaterialLocationMsg(self):
        """
        Trigger a C{'nodegraph_stateLabel'} event with an empty payload to
        clear any error message.

        Do nothing if this NME is locked.
        """
        if self.isLocked(True):
            return
        else:
            Utils.EventModule.QueueEvent('nodegraph_stateLabel', hash(self), text=None)
            return

    def __isRelevantNodeEvent(self, node, eventType, kwargs):
        """
        Check if the given event should be added to the batch of events for
        processing.

        I.e. the event affects non-hidden child nodes.

        @type node: C{NodegraphAPI.Node}
        @type eventType: C{str}
        @type kwargs: C{dict}
        @rtype: C{bool}
        @param node: Node related to event.
        @param eventType: Type of event.
        @param kwargs: Event data.
        @return: C{True} if this event should be processed, C{False} otherwise.
        """
        excludedNodes = self._getExcludedNodes()
        if node in excludedNodes:
            return False
        if node.getParent() in excludedNodes:
            return False
        if eventType == 'node_delete':
            return self.__isDeletedNodeADescendent
        if eventType == 'parameter_finalizeValue':
            if kwargs['param'].getName() == '__lastValue':
                return False
        if not self.__isChildNode(node):
            return False
        return True

    def __flushNodeGraphChangedEvents(self):
        """
        Iterates over the list of queued C{'nodegraph_changed'} events and
        sends them for processing.
        """
        if not self.__queuedNodeGraphEvents:
            return
        if not self.__isUndoGroupOpened:
            log.warning('NetworkMaterialEdit saving edits without an undo entry')
        try:
            genericOpNode = self._getNodeFromParam('__node_genericOp')
            genericOpArgs = self._getGenericOpArgs()
            gb = FnAttribute.GroupBuilder()
            if genericOpArgs:
                gb.update(genericOpArgs)
            while self.__queuedNodeGraphEvents:
                kwargs = self.__queuedNodeGraphEvents.pop(0)
                originalEventType = kwargs.get('originalEventType')
                if originalEventType == 'parameter_finalizeValue':
                    self.__onParameterFinalize(gb, genericOpArgs, **kwargs)
                elif originalEventType == 'node_create':
                    self.__onNodeCreate(gb, genericOpArgs, **kwargs)
                elif originalEventType == 'port_disconnect':
                    self.__onPortDisconnect(gb, **kwargs)
                elif originalEventType == 'port_connect':
                    self.__onPortConnect(gb, **kwargs)
                elif originalEventType == 'node_delete':
                    self.__onNodeDelete(gb, genericOpArgs, **kwargs)
                elif originalEventType == 'node_setBypassed':
                    self.__onNodeBypassed(gb, **kwargs)
                elif originalEventType == 'node_setName':
                    self.__onNodeSetName(gb, genericOpArgs, **kwargs)

            if self.__constructLayoutArgs(gb, genericOpArgs):
                self.__updateOpArgsFromAttr(gb.build())
        finally:
            self.__closeUndoGroup()
            self.__notifyUpdated()

    def __closeUndoGroup(self):
        if self.__isUndoGroupOpened:
            Utils.EventModule.QueueEvent('undo_closeGroup', 0)
            self.__isUndoGroupOpened = False

    def __onPopulateLayout(self, eventType, eventID):
        """
        Event handler for C{'nodegraph_nme_populate_layout'}.

        Initialise NME op args for C{material.B{layout}} attributes.

        @type eventType: C{str}
        @type eventID: C{object}
        @param eventType: Ignored.
        @param eventID: Ignored.
        """
        self.__initialiseLayoutArgs()

    def __initialiseLayoutArgs(self):
        """
        Initialise NME op args for C{material.B{layout}} attributes.
        """
        if Utils.UndoStack.IsUndoInProgress():
            return
        else:
            oldOpArgs = self._getGenericOpArgs()
            if oldOpArgs is None:
                return
            gb = FnAttribute.GroupBuilder()
            gb.update(oldOpArgs)
            valid = self.__constructLayoutArgs(gb, oldOpArgs)
            if not valid:
                return
            newOpArgs = gb.build()
            if newOpArgs.getHash() == oldOpArgs.getHash():
                self.__isLayoutInitialised = True
                return
            if not self.__isLayoutInitialised:
                Utils.UndoStack.DisableCapture()
            else:
                Utils.UndoStack.OpenGroup('%s source material updated' % self.getName())
            try:
                self.__updateOpArgsFromAttr(newOpArgs)
            finally:
                if not self.__isLayoutInitialised:
                    Utils.UndoStack.EnableCapture()
                    self.__isLayoutInitialised = True
                else:
                    Utils.UndoStack.CloseGroup()

            return

    def __constructLayoutArgs(self, gb, genericOpArgs):
        """
        Construct/augment material layout op args from diff of incoming
        vs. internal network's C{material.B{layout}} attributes.

        @type gb: C{FnAttribute.GroupBuilder}
        @type genericOpArgs: C{FnAttribute.GroupAttribute}
        @rtype: C{bool}
        @param gb: C{GroupBuilder} for constructing NME op args.
        @param genericOpArgs: Previous NME op args.
        @return: C{False} if no valid upstream material, C{True} otherwise.
        """
        incoming = self.__getIncomingMaterialAttributes()
        if not incoming:
            return False
        incomingLayout = incoming.getChildByName('layout').getFnAttr()
        internalLayout = self.getContentsLayoutAttributes()
        opArgAddedLayoutName = ('.').join((
         OpArgPaths.LayoutAdded, 'layout'))
        addedLayout = genericOpArgs.getChildByName(opArgAddedLayoutName)
        self.__cleanLayoutAdditions(gb, internalLayout, addedLayout, opArgAddedLayoutName)
        opArgInsertedLayoutName = ('.').join((
         OpArgPaths.LayoutConnectionsInserted, 'layout'))
        insertedConnections = genericOpArgs.getChildByName(opArgInsertedLayoutName)
        self.__cleanLayoutAdditions(gb, internalLayout, insertedConnections, opArgInsertedLayoutName)
        self.__updateLayoutEdits(gb, genericOpArgs, incomingLayout, internalLayout)
        return True

    def __findEditedNodeNames(self):
        """
        Determines which nodes have been edited & added by the NME in response
        to relevant B{Node Graph} events.

        @rtype: C{tuple} of C{list} of C{str}
        @return: Added, edited, and disconnected nodes by the NME, in that
            order.
        """
        addedNodeNames = set()
        editedNodeNames = set()
        layoutAttrs = self.getContentsLayoutAttributes()
        allNodeNames = [ layoutAttrs.getChildName(nodeIdx) for nodeIdx in xrange(layoutAttrs.getNumberOfChildren())
                       ]
        opArgSearcher = OpArgNodeReferenceSearcher(self._getGenericOpArgs(), allNodeNames)
        addedNodeNames |= opArgSearcher.getAddedNodeNames()
        connectionsEditedNodeNames = opArgSearcher.getConnectedNodeNames()
        editedNodeNames |= connectionsEditedNodeNames
        editedNodeNames |= opArgSearcher.getParameterLocallySetNodeNames()
        editedNodeNames |= opArgSearcher.getBypassedNodeNames()
        disconnectedNodeNames = LayoutNodesSearcher(layoutAttrs).getDisconnectedNodeNames(connectionsEditedNodeNames)
        parents = set()
        for addedNodeName in addedNodeNames:
            addedNode = self.getNodeFromSourceNodeName(addedNodeName)
            if addedNode:
                _GetParents(addedNode, self, parents)

        for editedNodeName in editedNodeNames:
            editedNode = self.getNodeFromSourceNodeName(editedNodeName)
            if editedNode:
                _GetParents(editedNode, self, parents)

        parentNames = {self.__nodeSourceNameLookup.get(p, p.getName()) for p in parents}
        editedNodeNames.update(parentNames)
        disconnectedNodeNames.difference_update(addedNodeNames)
        editedNodeNames.difference_update(addedNodeNames)
        editedNodeNames.difference_update(disconnectedNodeNames)
        return (
         addedNodeNames, editedNodeNames, disconnectedNodeNames)

    @classmethod
    def __cleanLayoutAdditions(cls, gb, internal, edited, location):
        """
        Recursively remove newly added layout attributes that are no longer
        present in the internal NME node graph.

        @type gb: C{FnAttribute.GroupBuilder}
        @type internal: C{FnAttribute.Attribute} or C{None}
        @type edited: C{FnAttribute.Attribute}
        @type location: C{str}
        @param gb: C{GroupBuilder} containing new C{material.B{layout}} op
            args to update.
        @param internal: Sub-attribute of internal network's
            C{material.B{layout}} attribute corresponding to C{location}, as
            it currently stands.
        @param edited: Sub-attribute of internal network's
            C{material.B{layout}} attribute corresponding to C{location}, as
            it was after previous cook.
        @param location: Op arg path to check under.
        """
        if internal is None:
            gb.delete(location)
            return
        else:
            if isinstance(edited, FnAttribute.GroupAttribute):
                numEditedChildren = edited.getNumberOfChildren()
                for childIdx in xrange(numEditedChildren):
                    childName = edited.getChildName(childIdx)
                    childLocation = ('.').join((location, childName))
                    editedChild = edited.getChildByIndex(childIdx)
                    internalChild = internal.getChildByName(childName)
                    cls.__cleanLayoutAdditions(gb, internalChild, editedChild, childLocation)

            return

    def __updateLayoutEdits(self, gb, opArgs, incomingRoot, internalRoot):
        """
        Calculate the op args required to alter the incoming scene graph
        location attrs to match the internal scene graph location attrs.

        Must take care to ensure no edits are lost just because the two scene
        graphs happen to agree at the moment (i.e. if upstream NMC is edited
        to match this NME we do not re-establish syncing between them).

        @type gb: C{FnAttribute.GroupBuilder}
        @type opArgs: C{FnAttribute.GroupAttribute}
        @type incomingRoot: C{FnAttribute.GroupAttribute}
        @type internalRoot: C{FnAttribute.GroupAttribute}
        @param gb: C{GroupBuilder} to store updated op args.
        @param opArgs: Previous op args.
        @param incomingRoot: C{material.B{layout}} attributes of upstream
            network.
        @param internalRoot: C{material.B{layout}} attributes of internal
            network.
        """
        for pathTuple, incoming, internal in self.__layoutLeafs(tuple(), incomingRoot, internalRoot, opArgs):
            argPathTuple = ('layout', ) + pathTuple
            argPath = ('.').join(argPathTuple)
            addedAttrName = ('.').join((
             OpArgPaths.LayoutAdded, argPath))
            replacedAttrName = ('.').join((
             OpArgPaths.LayoutReplaced, argPath))
            deletedAttrName = ('.').join((
             OpArgPaths.LayoutDeleted, argPath))
            insertedAttrName = ('.').join((
             OpArgPaths.LayoutConnectionsInserted, argPath))
            removedAttrName = ('.').join((
             OpArgPaths.LayoutConnectionsRemoved, argPath))
            if self.__isConnectionLayoutAttr(argPath):
                prevDeletedAttr = opArgs.getChildByName(removedAttrName)
                prevEditedAttr = opArgs.getChildByName(insertedAttrName)
                incomingData = set(incoming and incoming.getData() or [])
                internalData = set(internal and internal.getData() or [])
                prevAdded = set(prevEditedAttr and prevEditedAttr.getData() or [])
                prevDeleted = set(prevDeletedAttr and prevDeletedAttr.getData() or [])
                stillAdded = prevAdded.intersection(internalData)
                currAdded = internalData.difference(incomingData)
                currDeleted = incomingData.difference(internalData)
                newlyAdded = currAdded.difference(prevAdded)
                deleted = currDeleted.union(prevDeleted)
                reinstated = internalData.intersection(deleted)
                added = stillAdded.union(newlyAdded).union(reinstated)
                snacNode = self.__getSNACNodeFromAttrLocation(argPath)
                if snacNode:
                    connections = _GetSNACNodeConnections(snacNode)
                    for upstreamPort, snacPort in connections:
                        node = upstreamPort.getNode()
                        nodeName = node.getName()
                        if node in self.__nodeSourceNameLookup:
                            nodeName = self.__nodeSourceNameLookup[node]
                        connStr = '%s:%s@%s' % (
                         snacPort.getName(),
                         upstreamPort.getName(),
                         nodeName)
                        added.add(connStr)

                edited = deleted | added
                gb.set(removedAttrName, FnAttribute.StringAttribute(list(edited)))
                gb.set(insertedAttrName, FnAttribute.StringAttribute(list(added)))
            elif internal is None or isinstance(internal, FnAttribute.NullAttribute):
                gb.set(deletedAttrName, True)
                gb.delete(addedAttrName)
                gb.delete(replacedAttrName)
                gb.delete(insertedAttrName)
                gb.delete(removedAttrName)
            elif incoming is None:
                gb.set(addedAttrName, internal)
            else:
                gb.set(replacedAttrName, internal)
                if self.__isParameterEnableLayoutAttr(argPath):
                    self.__updateParameterEnableLayoutEdit(gb, internalRoot, argPathTuple, opArgs, internal)

        return

    @classmethod
    def __layoutLeafs(cls, pathTuple, incoming, internal, opArgs):
        """
        Generator providing C{material.B{layout}} attribute paths and their
        associated upstream vs. internal values that have changed or need
        checking.

        @type pathTuple: C{tuple} of C{str}
        @type incoming: C{FnAttribute.GroupAttribute}
        @type internal: C{FnAttribute.GroupAttribute}
        @type opArgs: C{FnAttribute.GroupAttribute}
        @rtype: C{collections.Iterable} of C{tuple} of C{tuple} of C{str} and
            C{FnAttribute.GroupAttribute} and C{FnAttribute.GroupAttribute}
        @param pathTuple: Path under C{incoming} and C{internal} to begin
            comparing, as a tuple.
        @param incoming: Upstream network's C{material.B{layout}} sub-attribute
            corresponding to C{pathTuple}.
        @param internal: Internal network's C{material.B{layout}} sub-attribute
            corresponding to C{pathTuple}.
        @param opArgs: Current NME op args, used to check for paths that need
            checking even if their hash is unchanged.
        @return: Tuple of attribute path (as a tuple), upstream attribute, and
            internal attribute, in that order, of attributes that have changed
            or need checking.
        """
        if not cls.__isLayoutEdited(pathTuple, incoming, internal, opArgs):
            return
        if isinstance(incoming, FnAttribute.GroupAttribute) and isinstance(internal, FnAttribute.GroupAttribute):
            childsProcessed = set()
            numIncomingChildren = incoming.getNumberOfChildren()
            for childIdx in xrange(numIncomingChildren):
                childName = incoming.getChildName(childIdx)
                childsProcessed.add(childName)
                childPath = pathTuple + (childName,)
                incomingChild = incoming.getChildByIndex(childIdx)
                internalChild = internal.getChildByName(childName)
                for descendentPath in cls.__layoutLeafs(childPath, incomingChild, internalChild, opArgs):
                    yield descendentPath

            numInternalChildren = internal.getNumberOfChildren()
            for childIdx in xrange(numInternalChildren):
                childName = internal.getChildName(childIdx)
                if childName in childsProcessed:
                    continue
                childPath = pathTuple + (childName,)
                incomingChild = incoming.getChildByName(childName)
                internalChild = internal.getChildByIndex(childIdx)
                for descendentPath in cls.__layoutLeafs(childPath, incomingChild, internalChild, opArgs):
                    yield descendentPath

        else:
            yield (
             pathTuple, incoming, internal)

    __layoutArgPathTuples = [ (opArgPath + '.layout',) for opArgPath in (
     OpArgPaths.LayoutAdded,
     OpArgPaths.LayoutReplaced,
     OpArgPaths.LayoutDeleted,
     OpArgPaths.LayoutConnectionsInserted,
     OpArgPaths.LayoutConnectionsRemoved)
                            ]

    @classmethod
    def __isLayoutEdited(cls, pathTuple, incoming, internal, opArgs):
        """
        Check if a given layout attribute should be or is already edited.

        I.e. if either the incoming vs. internal scene graph location attr
        is different, or this attr has been edited before and needs to be
        checked to see if it's changed (e.g. user altered a previous edit in
        NME to now match the upstream NMC).

        @type pathTuple: C{tuple} of C{str}
        @type incoming: C{FnAttribute.GroupAttribute}
        @type internal: C{FnAttribute.GroupAttribute}
        @type opArgs: C{FnAttribute.GroupAttribute}
        @rtype: C{bool}
        @param pathTuple: Path under C{incoming} and C{internal} to compare,
            as a tuple.
        @param incoming: First attribute to compare.
        @param internal: Second attribute to compare.
        @param opArgs: Current state of NME op args.
        @return: C{True} if C{incoming} and C{internal} hashes differ or if
            C{opArgs} contains edits at C{pathTuple}, C{False} otherwise.
        """
        incomingHash = incoming and incoming.getHash()
        internalHash = internal and internal.getHash()
        if incomingHash != internalHash:
            return True
        return any(opArgs.getChildByName(('.').join(rootPath + pathTuple)) is not None for rootPath in cls.__layoutArgPathTuples)

    @staticmethod
    def __updateParameterEnableLayoutEdit(gb, internalLayout, argPathTuple, opArgs, attr):
        """
        Special case handling for edits to B{enable} parameters.

        If the B{enable} flag is set to "locally edited" (C{1}), set the value
        of the corresponding C{Parameter} in the NME op args, as if it was
        edited, even if the edited value matches the upstream value.

        This effectively prevents auto-updating the parameter in the NME when
        the upstream parameter changes.

        @type gb: C{FnAttribute.GroupBuilder}
        @type internalLayout: C{FnAttribute.GroupAttribute}
        @type argPathTuple: C{tuple} of C{str}
        @type opArgs: C{FnAttribute.GroupAttribute}
        @type attr: C{FnAttribute.IntAttribute}
        @param gb: C{GroupBuilder} to store changes to NME op args.
        @param internalLayout: C{material.B{layout}} attribute of the internal
            network.
        @param argPathTuple: Path in the op args of the parameter, as a tuple.
        @param opArgs: Current state of NME op args.
        @param attr: The parameter's enable flag from the C{internalLayout}.
        """
        enable = attr.getValue()
        if enable != 1:
            return
        else:
            nodeName = argPathTuple[1]
            paramName = argPathTuple[(-2)]
            valueArgPathTuple = argPathTuple[:-1] + ('value', )
            valueLayoutPathTuple = argPathTuple[1:-1] + ('value', )
            valueLayoutPath = ('.').join(valueLayoutPathTuple)
            valueAttr = internalLayout.getChildByName(valueLayoutPath)
            valueArgPath = ('.').join((
             OpArgPaths.LayoutReplaced,) + valueArgPathTuple)
            bakedArgPath = ('.').join((
             OpArgPaths.LayoutReplaced,) + (
             'layout', nodeName, 'parameters', paramName))
            if opArgs.getChildByName(valueArgPath) is None:
                gb.set(valueArgPath, valueAttr)
            if opArgs.getChildByName(bakedArgPath) is None:
                gb.set(bakedArgPath, valueAttr)
            return

    _connectionLayoutAttrNameRegex = re.compile('^layout\\.[^.]+\\.(?:connections|nodeSpecificAttributes\\.(?:returnConnections))$')

    @classmethod
    def __isConnectionLayoutAttr(cls, location):
        """
        Check if a material layout location refers to a list of connection
        strings.

        @type location: C{str}
        @rtype: C{bool}
        @param location: Path in layout attributes to check.
        @return: C{True} if the location is a connection layout attribute,
            C{False} otherwise.
        """
        return cls._connectionLayoutAttrNameRegex.match(location) is not None

    _paramEnableLayoutAttrNameRegex = re.compile('^layout\\.[^.]+\\.parameterVars\\.[^.]+\\.enable$')

    @classmethod
    def __isParameterEnableLayoutAttr(cls, location):
        """
        Check if a material layout location refers to the B{enable} flag on
        a parameter.

        @type location: C{str}
        @rtype: C{bool}
        @param location: Path in layout attributes to check.
        @return: C{True} if the location is an enable flag, C{False} otherwise.
        """
        return cls._paramEnableLayoutAttrNameRegex.match(location) is not None

    def __getSNACNodeFromAttrLocation(self, locationPath):
        """
        If given C{material.B{layout}} path refers to a SNAC node, return that
        node.

        @type locationPath: C{str}
        @rtype: C{NodegraphAPI.Node} or C{None}
        @param locationPath: Path to check.
        @return: Matching SNAC node or C{None}.
        """
        pathTokens = locationPath.split('.')
        if len(pathTokens) != 3:
            return
        else:
            _layout, nodeName, connGroup = pathTokens
            if connGroup != 'connections':
                return
            node = self.__shadingNetworkNodes.get(nodeName)
            if node and node.getType() == 'ShadingNodeArrayConnector':
                return node
            return

    def __onParameterFinalize(self, gb, genericOpArgs, node, param, **_kwargs):
        """
        Handles changes to parameters on nodes within the NME node.

        @type gb: C{FnAttribute.GroupBuilder}
        @type genericOpArgs: C{FnAttribute.GroupAttribute}
        @type node: C{NodegraphAPI.Node}
        @type param: C{NodegraphAPI.Parameter}
        @param gb: A GroupBuilder that will be used to populate the parameters
                   of the internal GenericOp node.
        @param genericOpArgs: The current op args on the GenericOp node.
        @param node: Node associated with parameter.
        @param param: The parameter that has changed.
        @param _kwargs: Unused keyword arguments
        """
        if param.getType() == 'group':
            for leaf in self.__leafEnableParams(param):
                self.__onParameterFinalize(gb, genericOpArgs, node, leaf)

            return
        if param.getNumChildren():
            return
        else:
            sourceNodeName = self.__nodeSourceNameLookup.get(node, node.getName())
            editedParamAttrName = self.__editedParamAttrName(sourceNodeName, param)
            if editedParamAttrName is None:
                return
            if param.getName() == 'enable':
                frameTime = NodegraphAPI.GetCurrentTime()
                targetParamName = param.getParent().getName()
                deletedParams = set()
                deletedParamAttrName = self.__deletedParamAttrName(sourceNodeName)
                deletedParamsAttr = genericOpArgs.getChildByName(deletedParamAttrName)
                if deletedParamsAttr:
                    deletedParams = set(deletedParamsAttr.getData())
                enabledState = param.getValue(frameTime)
                if enabledState == -1:
                    deletedParams.add(targetParamName)
                elif enabledState == 0:
                    deletedParams.discard(targetParamName)
                    gb.delete(editedParamAttrName)
                elif enabledState == 1:
                    deletedParams.discard(targetParamName)
                    parent = param.getParent()
                    dataAttr = self._buildDataAttrFromGroupParam(parent)
                    gb.set(editedParamAttrName, dataAttr)
                if deletedParams:
                    gb.set(deletedParamAttrName, FnAttribute.StringAttribute(list(deletedParams)))
                else:
                    gb.delete(deletedParamAttrName)
            elif param.getType() in ('number', 'string'):
                parent = param.getParent()
                while parent and parent.getType() != 'group':
                    parent = parent.getParent()

                if parent:
                    dataAttr = self._buildDataAttrFromGroupParam(parent)
                    gb.set(editedParamAttrName, dataAttr)
            else:
                gb.set(editedParamAttrName, param.getValue(0))
            return

    @classmethod
    def __leafEnableParams(cls, parent):
        """
        Generator yielding the the leaf "enable" flag parameters from a
        given group.

        @type parent: C{NodegraphAPI.Parameter}
        @rtype: C{NodegraphAPI.Parameter}
        @param parent: Parent param to recurse through to find leaf params.
        @return: Leaf "enable" params.
        """
        if parent.getType() != 'group':
            if cls.__enableParamRegex.match(parent.getFullName(includeNodeName=False)):
                yield parent
            return
        for child in parent.getChildren():
            for leaf in cls.__leafEnableParams(child):
                yield leaf

    __enableParamRegex = re.compile('^parameters\\..*\\.enable$')

    def __registerEventHandlers(self):
        """
        * Register relevant event handlers and filters.
        * Start listening to changes at the NME's scene graph location.
        * Start polling for batched events to process.
        """
        for (eventType, eventID), handler in self.__eventHandlers.iteritems():
            isRegistered = Utils.EventModule.IsHandlerRegisteredAfterEventLoop(handler, eventType=eventType, eventID=eventID)
            if not isRegistered:
                Utils.EventModule.RegisterEventHandler(handler, eventType=eventType, eventID=eventID)

        handlersIter = self.__collapsedHandlers.iteritems()
        for (eventType, eventID), handler in handlersIter:
            isRegistered = Utils.EventModule.IsCollapsedHandlerRegisteredAfterEventLoop(handler, eventType=eventType, eventID=eventID)
            if not isRegistered:
                Utils.EventModule.RegisterCollapsedHandler(handler, eventType=eventType, eventID=eventID)

        Utils.EventModule.RegisterEventFilter(self.__eventFilter)
        if Configuration.get('KATANA_UI_MODE'):
            self.__queuedNodeGraphEvents = []
            UI4.Util.PluginManager.RegisterTimerCallback(self.__flushNodeGraphChangedEvents, interval=0.25, suppressCallbackDurationWarning=True)
            if self.__upstreamListener is None:
                self.__upstreamListener = SceneGraphLocationListener(self._getNodeFromParam('__node_networkMaterial'), self._getNodeFromParam('__node_incoming'), 'nodegraph_nme_invalidate', hash(self))
            self.__upstreamListener.registerEventHandlers()
        return

    def __unregisterEventHandlers(self):
        """
        * Unregister relevant event handlers and filters.
        * Stop listening to changes at the NME's scene graph location.
        * Stop polling for batched events to process.
        """
        for (eventType, eventID), handler in self.__eventHandlers.iteritems():
            isRegistered = Utils.EventModule.IsHandlerRegisteredAfterEventLoop(handler, eventType=eventType, eventID=eventID)
            if isRegistered:
                Utils.EventModule.UnregisterEventHandler(handler, eventType=eventType, eventID=eventID)

        handlersIter = self.__collapsedHandlers.iteritems()
        for (eventType, eventID), handler in handlersIter:
            isRegistered = Utils.EventModule.IsCollapsedHandlerRegisteredAfterEventLoop(handler, eventType=eventType, eventID=eventID)
            if isRegistered:
                Utils.EventModule.UnregisterCollapsedHandler(handler, eventType=eventType, eventID=eventID)

        Utils.EventModule.UnregisterEventFilter(self.__eventFilter)
        if Configuration.get('KATANA_UI_MODE'):
            UI4.Util.PluginManager.UnregisterTimerCallback(self.__flushNodeGraphChangedEvents)
            if self.__upstreamListener is not None:
                self.__upstreamListener.unregisterEventHandlers()
        return

    def __onNodeCreate(self, gb, genericOpArgs, node, **kwargs):
        """
        Update NME op args to add a node to C{material.B{nodes}}.

        Ensure any previous op arg referencing the same name is removed first.

        @type gb: C{FnAttribute.GroupBuilder}
        @type genericOpArgs: C{FnAttribute.GroupAttribute}
        @type node: C{NodegraphAPI.Node}
        @type kwargs: C{dict}
        @param gb: C{GroupBuilder} storing op arg updates.
        @param genericOpArgs: Previous op args.
        @param node: Newly created node.
        @param kwargs: Ignored.
        """
        OpArgNodeReferenceSearcher(genericOpArgs, [node.getName()]).deleteFromGroupAttr(gb)
        self.__shadingNetworkNodes[node.getName()] = node
        self.__addNewShadingNode(gb, node)

    def __addNewShadingNode(self, gb, node):
        """
        Update NME op args to add a shading node to C{material.B{nodes}}
        attribute.

        Handles a C{'node_create'} from batched events.

        Do nothing if C{node} is not a shading node.

        @type gb: C{FnAttribute.GroupBuilder}
        @type node: C{NodegraphAPI.Node}
        @param gb: C{GroupBuilder} storing op arg updates.
        @param node: Newly created node.
        """
        shaderTypeParam = node.getParameter('nodeType')
        if not shaderTypeParam:
            return
        currentTime = NodegraphAPI.GetCurrentTime()
        shaderType = shaderTypeParam.getValue(currentTime)
        name = node.getParameter('name').getValue(currentTime)
        attrName = self.__newNodeAttrName(name)
        srcName = node.getName()
        gb.set('%s.name' % attrName, FnAttribute.StringAttribute(name))
        gb.set('%s.type' % attrName, FnAttribute.StringAttribute(shaderType))
        if isinstance(node, Nodes3DAPI.ShadingNodeBase.ShadingNodeBase):
            gb.set('%s.target' % attrName, FnAttribute.StringAttribute(node.getRendererName()))
            gb.set('%s.srcName' % attrName, FnAttribute.StringAttribute(srcName))

    def __onNodeDelete(self, gb, genericOpArgs, node, oldName, **kwargs):
        """
        Update NME op args to remove a node from C{material.B{nodes}}
        attribute

        Handles a C{'node_delete'} from batched events.

        @type gb: C{FnAttribute.GroupBuilder}
        @type genericOpArgs: C{FnAttribute.GroupAttribute}
        @type node: C{NodegraphAPI.Node}
        @type oldName: C{str}
        @type kwargs: C{dict}
        @param gb: C{GroupBuilder} storing op arg updates.
        @param genericOpArgs: Previous op args.
        @param node: Deleted node.
        @param oldName: Name of node before it was deleted.
        @param kwargs: Ignored.
        """
        deletedNodeName = self.__nodeSourceNameLookup.get(node, oldName)
        newNodeAttrName = self.__newNodeAttrName(deletedNodeName)
        if genericOpArgs.getChildByName(newNodeAttrName) is not None:
            gb.delete('nodes.%s' % deletedNodeName)
        else:
            gb.set('nodes.%s.isDeleted' % deletedNodeName, True)
        return

    def __onNodeSetName(self, gb, genericOpArgs, node=None, newName=None, oldName=None, **kwargs):
        """
        Update NME op args to rename a node within C{material.B{nodes}}
        attribute.

        Handles a C{'node_setName'} from batched events.

        Only allowed for nodes added inside the NME node. Nodes which existed
        inside the original source location are blocked from being renamed.

        @type gb: C{FnAttribute.GroupBuilder}
        @type genericOpArgs: C{FnAttribute.GroupAttribute}
        @type node: C{NodegraphAPI.Node}
        @type newName: C{str}
        @type oldName: C{str}
        @type kwargs: C{dict}
        @param gb: C{GroupBuilder} storing op arg updates.
        @param genericOpArgs: Previous op args.
        @param node: Renamed node.
        @param oldName: Name of node before it was renamed.
        @param newName: Name of node after it was renamed.
        @param kwargs: Ignored.
        """
        attrName = self.__newNodeAttrName(oldName)
        if not genericOpArgs.getChildByName(attrName):
            return
        connectionsAttr = genericOpArgs.getChildByName('nodes.%s.connections' % oldName)
        paramsAttr = genericOpArgs.getChildByName('nodes.%s.parameters' % oldName)
        byPassedAttr = genericOpArgs.getChildByName('nodes.%s.isBypassed' % oldName)
        nodeReferenceSearcher = OpArgNodeReferenceSearcher(genericOpArgs, [oldName])
        nodeReferenceSearcher.updateConnectionNodeName(gb, oldName, newName)
        self.__onNodeDelete(gb, genericOpArgs, node, oldName)
        del self.__shadingNetworkNodes[oldName]
        self.__addNewShadingNode(gb, node)
        self.__shadingNetworkNodes[newName] = node
        self.__nodeSourceNameLookup[node] = newName
        if connectionsAttr:
            newConnectionsAttrName = 'nodes.%s.connections' % newName
            gb.set(newConnectionsAttrName, connectionsAttr)
        if paramsAttr:
            newParamsAttrName = 'nodes.%s.parameters' % newName
            gb.set(newParamsAttrName, paramsAttr)
        if byPassedAttr:
            newParamsAttrName = 'nodes.%s.isBypassed' % newName
            gb.set(newParamsAttrName, byPassedAttr)

    def __onNodeBypassed(self, gb, node, **kwargs):
        """
        Update NME op args to enable/disable a node within C{material.B{nodes}}
        attribute.

        Handles a C{'node_setBypassed'} from batched events.

        @type gb: C{FnAttribute.GroupBuilder}
        @type node: C{NodegraphAPI.Node}
        @type kwargs: C{dict}
        @param gb: C{GroupBuilder} storing op arg updates.
        @param node: Enabled/disabled node.
        @param kwargs: Ignored.
        """
        bypassedNodeName = self.__nodeSourceNameLookup.get(node, node.getName())
        gb.set('nodes.%s.isBypassed' % bypassedNodeName, node.isBypassed())

    def __eventFilter(self, eventType, eventID, **kwargs):
        """
        Event filter to wrap all upcoming relevant events in an undo group.

        We need an event filter in order to catch C{'node_delete_begin'} before
        the C{UndoEntries} filter disables the undo stack.

        @type eventType: C{str}
        @type eventID: C{object}
        @type kwargs: C{dict}
        @rtype: C{bool}
        @param eventType: Type of event.
        @param eventID: Ignored.
        @param kwargs: Event data.
        @return: Always C{True}.
        """
        if eventType == 'node_delete_begin':
            parent = kwargs['parent']
            self.__isDeletedNodeADescendent = parent is self or self.__isChildNode(parent)
        elif eventType == 'node_delete':
            if kwargs['node'] is self:
                self.__isDeletingMe = True
        if self.__shouldOpenUndoGroup(eventType, kwargs):
            undoName = '%s updated material' % self.getName()
            Utils.UndoStack.OpenGroupSync(undoName)
            self.__isUndoGroupOpened = True
        return True

    def __shouldOpenUndoGroup(self, eventType, kwargs):
        """
        Return whether we should open an undo group.

        I.e. we haven't already opened an undo group and we are about to
        queue an event(s) for batch processing.

        @type eventType: C{str}
        @type kwargs: C{dict}
        @rtype: C{bool}
        @param eventType: Event type to check.
        @param kwargs: Event data.
        @return: C{True} if undo group should be created, C{False} otherwise.
        @see: L{__onNodeGraphChanged}
        """
        if NodegraphAPI.IsLoading():
            return False
        else:
            if self.__isDeletingMe:
                return False
            if self.__isUndoGroupOpened:
                return False
            if self.__isSceneGraphLocationChangeEvent(eventType, kwargs):
                return False
            if Utils.UndoStack.IsUndoInProgress():
                return False
            if eventType == 'paste_begin' and (kwargs['parent'] is self or self.__isChildNode(kwargs['parent'])):
                return True
            if not self.__shadingNetworkNodes:
                return False
            if eventType == 'node_delete_begin':
                return self.__isDeletedNodeADescendent
            if not self.__isRelevantEvent(eventType):
                return False
            node = self.__getNodeFromKwargs(kwargs)
            if node is None:
                return False
            if not self.__isRelevantNodeEvent(node, eventType, kwargs):
                return False
            return True

    @staticmethod
    def __isRelevantEvent(eventType):
        """
        Check if given event type should be processed by the NME.

        @type eventType: C{str}
        @rtype: C{bool}
        @param eventType: Event type to check.
        @return: C{True} if event should be processed, C{False} otherwise.
        """
        return eventType in ('parameter_finalizeValue', 'node_create', 'node_setPosition',
                             'port_disconnect', 'port_connect', 'node_delete', 'node_shapeAttrsChanged',
                             'node_setBypassed', 'node_setName')

    def __isSceneGraphLocationChangeEvent(self, eventType, kwargs):
        """
        Check if given event is flagging an updated B{sceneGraphLocation}
        parameter on the internal NetworkMaterial node.

        @type eventType: C{str}
        @type kwargs: C{dict}
        @rtype: C{bool}
        @param eventType: Event to check.
        @param kwargs: Event data.
        @return: C{True} if event flags an updated B{sceneGraphLocation},
            C{False} otherwise.
        """
        return eventType == 'parameter_finalizeValue' and kwargs['param'].getName() == 'sceneGraphLocation' and self.__isInternalNetworkMaterialNode(kwargs['node'])

    @staticmethod
    def __getNodeFromKwargs(kwargs):
        """
        Inspect event data for arguments referring to a node and return that
        node.

        @type kwargs: C{dict}
        @rtype: C{NodegraphAPI.Node} or C{None}
        @param kwargs: Event data.
        @return: Node if C{kwargs} contains (a reference to) one, otherwise
            C{None}.
        """
        node = kwargs.get('node')
        if node is None:
            nodeName = kwargs.get('nodeName', kwargs.get('nodeNameB'))
            if nodeName is not None:
                node = NodegraphAPI.GetNode(nodeName)
        return node

    def __onPortConnect(self, gb, node=None, portB=None, originalEventID=None, **kwargs):
        """
        Update NME op args to connect nodes within C{material.B{nodes}}
        attribute.

        Handles a C{'port_connect'} from batched events.

        @type gb: C{FnAttribute.GroupBuilder}
        @type node: C{NodegraphAPI.Node}
        @type portB: C{NodegraphAPI.Port}
        @type originalEventID: C{object}
        @type kwargs: C{dict}
        @param gb: C{GroupBuilder} storing op arg updates.
        @param node: Node whose input port has been connected.
        @param originalEventID: Original C{'port_connect'} event ID, used to
            ensure we don't double-process the connection.
        @param kwargs: Ignored.
        """
        portB = node.getInputPort(portB.getName()) or node.getReturnPort(portB.getName())
        if originalEventID == hash(portB):
            return
        inputPorts = []
        _traverseDownstreamOfInputPort(portB, inputPorts)
        for inputPort in inputPorts:
            isSidebarConnection = self.__isInternalNetworkMaterialNode(inputPort.getNode())
            outputPorts = []
            isArray = _traverseUpstreamOfInputPort(inputPort, outputPorts)
            if isArray:
                if isSidebarConnection:
                    self.__newTerminalArrayConnections(gb, outputPorts, inputPort)
                else:
                    self.__newArrayConnections(gb, outputPorts, inputPort)
            else:
                for outputPort in outputPorts:
                    if isSidebarConnection:
                        self.__newTerminalConnection(gb, outputPort, inputPort.getName())
                    else:
                        self.__newConnection(gb, outputPort, inputPort)

    def __onPortDisconnect(self, gb, node=None, portB=None, originalEventID=None, **kwargs):
        """
        Update NME op args to disconnect nodes within C{material.B{nodes}}
        attribute.

        Handles a C{'port_disconnect'} from batched events.

        @type gb: C{FnAttribute.GroupBuilder}
        @type node: C{NodegraphAPI.Node}
        @type portB: C{NodegraphAPI.Port}
        @type originalEventID: C{object}
        @type kwargs: C{dict}
        @param gb: C{GroupBuilder} storing op arg updates.
        @param node: Node whose input port has been disconnected.
        @param originalEventID: Original C{'port_connect'} event ID, used to
            ensure we don't double-process the connection.
        @param kwargs: Ignored.
        """
        portB = node.getInputPort(portB.getName()) or node.getReturnPort(portB.getName())
        if originalEventID == hash(portB):
            return
        inputPorts = []
        _traverseDownstreamOfInputPort(portB, inputPorts)
        for inputPort in inputPorts:
            isSidebarConnection = self.__isInternalNetworkMaterialNode(inputPort.getNode())
            argsSoFar = gb.build(1)
            if isSidebarConnection:
                if not self.__removeNewTerminalConnection(gb, argsSoFar, inputPort):
                    self.__deleteTerminalConnection(gb, argsSoFar, inputPort)
                outputPorts = []
                isArray = _traverseUpstreamOfInputPort(inputPort, outputPorts)
                if isArray and outputPorts:
                    self.__newTerminalArrayConnections(gb, outputPorts, inputPort)
            else:
                if not self.__removeNewConnection(gb, argsSoFar, inputPort):
                    self.__deleteConnection(gb, argsSoFar, inputPort)
                outputPorts = []
                isArray = _traverseUpstreamOfInputPort(inputPort, outputPorts)
                if isArray and outputPorts:
                    self.__newArrayConnections(gb, outputPorts, inputPort)

    def __newTerminalArrayConnections(self, gb, arrayOutputPorts, inputPort):
        """
        Add output ports as array input terminal (NM sidebar) connections to
        NME op args C{GroupBuilder} for C{material.B{nodes}}.

        @type gb: C{FnAttribute.GroupBuilder}
        @type arrayOutputPorts: C{list} of C{NodegraphAPI.Port}
        @type inputPort: C{NodegraphAPI.Port}
        @param gb: C{GroupBuilder} storing op arg updates.
        @param arrayOutputPorts: Output ports as traversed through SNAC node.
        @param inputPort: Input port on NetworkMaterial.
        """
        outputs = [ self.__portNodeInfo(port) for port in arrayOutputPorts ]
        if outputs:
            attrName = self.__newTerminalConnectionAttrName(inputPort.getName())
            self.__arrayConnectionOutputs(gb, attrName, outputs)

    def __newArrayConnections(self, gb, arrayOutputPorts, inputPort):
        """
        Add output ports as array input connections to NME op args
        C{GroupBuilder} for C{material.B{nodes}}.

        @type gb: C{FnAttribute.GroupBuilder}
        @type arrayOutputPorts: C{list} of C{NodegraphAPI.Port}
        @type inputPort: C{NodegraphAPI.Port}
        @param gb: C{GroupBuilder} storing op arg updates.
        @param arrayOutputPorts: Output ports as traversed through SNAC node.
        @param inputPort: Input port on target node.
        """
        outputs = [ self.__portNodeInfo(port) for port in arrayOutputPorts ]
        if outputs:
            inputInfo = self.__portNodeInfo(inputPort)
            attrName = self.__newConnectionAttrName(inputInfo.nodeSrcName, inputInfo.portName)
            self.__arrayConnectionOutputs(gb, attrName, outputs)

    @staticmethod
    def __arrayConnectionOutputs(gb, attrName, outputs):
        """
        Update NME op args C{GroupBuilder} for C{material.B{nodes}}
        with array connections for a specific node.

        @type gb: C{FnAttribute.GroupBuilder}
        @type attrName: C{str}
        @type outputs: C{list} of C{_PortInfo}
        @param gb: C{GroupBuilder} storing op arg updates.
        @param attrName: Op arg root path for a specific node.
        @param outputs: Port info to furnish op args with.
        """
        gb.set('%s.isArray' % attrName, FnAttribute.IntAttribute(True))
        gb.set('%s.output.name' % attrName, FnAttribute.StringAttribute(map(operator.attrgetter('nodeName'), outputs)))
        gb.set('%s.output.srcName' % attrName, FnAttribute.StringAttribute(map(operator.attrgetter('nodeSrcName'), outputs)))
        gb.set('%s.output.port' % attrName, FnAttribute.StringAttribute(map(operator.attrgetter('portName'), outputs)))

    def __newTerminalConnection(self, gb, outputPort, inputPortName):
        """
        Update NME op args C{GroupBuilder} for C{material.B{nodes}}
        to add a NetworkMaterial terminal connection.

        @type gb: C{FnAttribute.GroupBuilder}
        @type outputPort: C{NodegraphAPI.Port}
        @type inputPortName: C{str}
        @param gb: C{GroupBuilder} storing op arg updates.
        @param outputPort: Port now connected to NetworkMaterial sidebar.
        @param inputPortName: Name of connected input port on NetworkMaterial.
        """
        outputInfo = self.__portNodeInfo(outputPort)
        attrPrefix = self.__newTerminalConnectionAttrName(inputPortName)
        gb.set('%s.isArray' % attrPrefix, FnAttribute.IntAttribute(False))
        gb.set('%s.output.name' % attrPrefix, FnAttribute.StringAttribute(outputInfo.nodeName))
        gb.set('%s.output.srcName' % attrPrefix, FnAttribute.StringAttribute(outputInfo.nodeSrcName))
        gb.set('%s.output.port' % attrPrefix, FnAttribute.StringAttribute(outputInfo.portName))

    def __removeNewTerminalConnection(self, gb, argsSoFar, inputPort):
        """
        Update NME op args C{GroupBuilder} for C{material.B{nodes}}
        to remove a NetworkMaterial terminal connection that was added in NME.

        @type gb: C{FnAttribute.GroupBuilder}
        @type argsSoFar: C{FnAttribute.GroupAttribute}
        @type inputPort: C{NodegraphAPI.Port}
        @param gb: C{GroupBuilder} storing op arg updates.
        @param argsSoFar: Op args in the process of being constructed. Used
            to ensure any newly added arg is not removed.
        @param inputPort: Port now disconnected on NetworkMaterial sidebar.
        """
        attrName = self.__newTerminalConnectionAttrName(inputPort.getName())
        attr = argsSoFar.getChildByName(attrName)
        if attr is None:
            return False
        else:
            gb.delete(attrName)
            return True

    @classmethod
    def __deleteTerminalConnection(cls, gb, argsSoFar, inputPort):
        """
        Update NME op args C{GroupBuilder} for C{material.B{nodes}}
        to delete a NetworkMaterial terminal connection.

        @type gb: C{FnAttribute.GroupBuilder}
        @type argsSoFar: C{FnAttribute.GroupAttribute}
        @type inputPort: C{NodegraphAPI.Port}
        @param gb: C{GroupBuilder} storing op arg updates.
        @param argsSoFar: Op args in the process of being constructed. Used
            to ensure we don't overwrite previous list of deleted connections.
        @param inputPort: Port now disconnected on NetworkMaterial sidebar.
        """
        inputPortName = inputPort.getName()
        attrName = cls.__deletedTerminalConnectionsAttrName()
        deletedConnections = cls.__attrToList(argsSoFar.getChildByName(attrName))
        if inputPortName in deletedConnections:
            return
        deletedConnections.append(inputPortName)
        deletedConnections.append('%sPort' % inputPortName)
        gb.set(attrName, FnAttribute.StringAttribute(deletedConnections))

    def __isInternalNetworkMaterialNode(self, node):
        """
        Check if given node is the internal NetworkMaterial node.

        @type node: C{NodegraphAPI.Node}
        @rtype: C{bool}
        @param node: Potential NetworkMaterial node.
        @return: C{True} if C{node} is the internal NetworkMaterial, C{False}
            otherwise.
        """
        networkMaterialNode = self._getNodeFromParam('__node_networkMaterial')
        return node is networkMaterialNode

    def __newConnection(self, gb, outputPort, inputPort):
        outputInfo = self.__portNodeInfo(outputPort)
        inputInfo = self.__portNodeInfo(inputPort)
        attrPrefix = self.__newConnectionAttrName(inputInfo.nodeSrcName, inputInfo.portName)
        gb.set('%s.isArray' % attrPrefix, FnAttribute.IntAttribute(False))
        gb.set('%s.output.name' % attrPrefix, FnAttribute.StringAttribute(outputInfo.nodeName))
        gb.set('%s.output.srcName' % attrPrefix, FnAttribute.StringAttribute(outputInfo.nodeSrcName))
        gb.set('%s.output.port' % attrPrefix, FnAttribute.StringAttribute(outputInfo.portName))

    def _getNetworkMaterialLocationExpr(self, networkMaterialNode):
        """
        Returns a parameter expression for the NetworkMaterialEdit node's
        B{sceneGraphLocation} parameter.

        @type networkMaterialNode: C{NodegraphAPI.Node}
        @rtype: C{str}
        @param networkMaterialNode: The internal NetworkMaterial node inside
            this SuperTool.
        @return: A parameter expression pointing to the NetworkMaterialEdit's
            B{sceneGraphLocation} parameter.
        """
        locationExpr = '=%s/sceneGraphLocation' % networkMaterialNode.getName()
        return locationExpr

    def _getIncomingSceneOpAndLocation(self, port, graphState, transaction):
        """
        Allows the node to add Ops to the Op tree used to evaluate the scene
        graph when building the node's UI.

        This implementation is required to drive the B{Material Interface}
        tab on the node. The material interface is generally populated by the
        output port of a NetworkMaterial node, in this case we substitute
        the GenericOp node for it.

        @type port: C{NodegraphAPI.Port}
        @type graphState: C{NodegraphAPI.GraphState}
        @type transaction: C{PyFnGeolib.GeolibRuntimeTransaction}
        @rtype: C{tuple} of C{PyFnGeolib.GeolibRuntimeOp} and C{str}
        @param port: Port to check for updates.
        @param graphState: C{GraphState} to evaluate op with.
        @param transaction: C{GeolibRuntimeTransaction} to dispatch op to.
        @return: Tuple of op chain to evaluate and value of
            B{sceneGraphLocation} parameter.
        """
        genericOpNode = self._getNodeFromParam('__node_genericOp')
        return (
         genericOpNode._getOp(port, graphState, set(), transaction),
         self.getScenegraphLocation())

    def __removeNewConnection(self, gb, argsSoFar, inputPort):
        """
        Update NME op args C{GroupBuilder} for C{material.B{nodes}}
        to remove a connection added within the NME.

        @type gb: C{FnAttribute.GroupBuilder}
        @type argsSoFar: C{FnAttribute.GroupAttribute}
        @type inputPort: C{NodegraphAPI.Port}
        @param gb: C{GroupBuilder} storing op arg updates.
        @param argsSoFar: Op args in the process of being constructed. Used
            to ensure we don't overwrite previous list of deleted connections.
        @param inputPort: Port now disconnected.
        """
        inputInfo = self.__portNodeInfo(inputPort)
        newConnectionAttrName = self.__newConnectionAttrName(inputInfo.nodeSrcName, inputInfo.portName)
        newConnectionAttr = argsSoFar.getChildByName(newConnectionAttrName)
        if newConnectionAttr is None:
            return False
        else:
            gb.delete(newConnectionAttrName)
            return True

    def __deleteConnection(self, gb, argsSoFar, inputPort):
        """
        Update NME op args C{GroupBuilder} for C{material.B{nodes}}
        to delete a connection.

        @type gb: C{FnAttribute.GroupBuilder}
        @type argsSoFar: C{FnAttribute.GroupAttribute}
        @type inputPort: C{NodegraphAPI.Port}
        @param gb: C{GroupBuilder} storing op arg updates.
        @param argsSoFar: Op args in the process of being constructed. Used
            to ensure we don't overwrite previous list of deleted connections.
        @param inputPort: Port now disconnected.
        """
        inputInfo = self.__portNodeInfo(inputPort)
        attrName = self.__deletedConnectionsAttrName(inputInfo.nodeSrcName)
        deletedConnections = self.__attrToList(argsSoFar.getChildByName(attrName))
        connectionAttrName = '%s.connections.%s' % (
         inputInfo.nodeName, inputInfo.portName)
        if connectionAttrName in deletedConnections:
            return
        deletedConnections.append(connectionAttrName)
        gb.set(attrName, FnAttribute.StringAttribute(deletedConnections))

    def __portNodeInfo(self, port):
        """
        Get useful info about a given port for constructing NME op args.

        @type port: C{NodegraphAPI.Port}
        @rtype: C{_PortInfo}
        @param port: Port to query.
        @return: A C{namedtuple} containing the port's name, the node's
            upstream name (or C{None} if it doesn't mirror an upstream node),
            and the node's B{name} parameter value.
        """
        portName = port.getName()
        node = port.getNode()
        nodeSrcName = self.__nodeSourceNameLookup.get(node, node.getName())
        currentTime = NodegraphAPI.GetCurrentTime()
        nodeName = node.getParameter('name').getValue(currentTime)
        return _PortInfo(portName, nodeSrcName, nodeName)

    @staticmethod
    def __attrToList(attr):
        """
        Utility to convert a multi-element C{Attribute} to a Python list of
        values.

        @type attr: C{FnAttribute.DataAttribute}
        @rtype: C{list} of C{object}
        @param attr: Attribute to extract internal data from.
        @return: List of values contained within {attr}.
        """
        if attr is not None:
            attrAsList = list(attr.getData())
        else:
            attrAsList = []
        return attrAsList

    @staticmethod
    def __newNodeAttrName(nodeName):
        """
        Root op arg for creating a new node in C{material.B{nodes}} attribute.

        @type nodeName: C{str}
        @rtype: C{str}
        @param nodeName: Name of created node.
        @return: Root op arg path to create a node with given C{nodeName}.
        """
        return 'nodes.%s.create' % nodeName

    @staticmethod
    def __newTerminalConnectionAttrName(inputPortName):
        """
        Root op arg for adding a connection to the NetworkMaterial sidebar
        terminal in the C{material.B{nodes}} attribute.

        @type inputPortName: C{str}
        @rtype: C{str}
        @param inputPortName: Name of terminal port.
        @return: Root op arg path to add a terminal connection to given
            C{inputPortName} port.
        """
        return 'terminals.new.%s' % inputPortName

    @staticmethod
    def __deletedTerminalConnectionsAttrName():
        """
        Root op arg for deleting a connection to the NetworkMaterial sidebar
        terminal in the C{material.B{nodes}} attribute.
        """
        return 'terminals.deleted'

    @staticmethod
    def __newConnectionAttrName(inputNodeSrcName, inputPortName):
        """
        Root op arg for adding a connection to a node in the
        C{material.B{nodes}} attribute.

        @type inputNodeSrcName: C{str}
        @type inputPortName: C{str}
        @rtype: C{str}
        @param inputNodeSrcName: Name of node as it should appear in
            C{material.B{nodes}}.
        @param inputPortName: Name of input port on node.
        @return: Root op arg path to add a connection to given port.
        """
        return 'nodes.%s.connections.new.%s' % (
         inputNodeSrcName, inputPortName)

    @staticmethod
    def __deletedConnectionsAttrName(inputNodeSrcName):
        """
        Root op arg for deleting a connection to a node in the
        C{material.B{nodes}} attribute.

        @type inputNodeSrcName: C{str}
        @rtype: C{str}
        @param inputNodeSrcName: Name of node as it should appear in
            C{material.B{nodes}}.
        @return: Root op arg path to delete a connection to given node.
        """
        return 'nodes.%s.connections.deleted' % inputNodeSrcName

    @staticmethod
    def __deletedParamAttrName(nodeName):
        """
        Root op arg for deleting a parameter on a node in the
        C{material.B{nodes}} attribute.

        @type nodeName: C{str}
        @rtype: C{str}
        @param nodeName: Name of node as it should appear in
            C{material.B{nodes}}.
        @return: Root op arg path to delete a parameter on given node.
        """
        return 'nodes.%s.parameters.deleted' % nodeName

    @staticmethod
    def __editedParamAttrName(nodeName, param):
        """
        Root op arg for editing a parameter on a node in the
        C{material.B{nodes}} attribute.

        Check first if the parameter is a shading node parameter.

        @type nodeName: C{str}
        @type param: C{NodegraphAPI.Parameter}
        @rtype: C{str} or C{None}
        @param nodeName: Name of node as it should appear in
            C{material.B{nodes}}.
        @param param: C{Parameter} to construct op arg for.
        @return: Root op arg path to edit a parameter on given node.
        """
        paramFullName = param.getFullName(includeNodeName=False)
        if not paramFullName.startswith('parameters.'):
            return None
        else:
            paramName = paramFullName.split('.', 1)[(-1)]
            parent = param.getParent()
            if parent and parent.getType() in ('numberArray', 'stringArray'):
                parent = parent.getParent()
            if not parent:
                return None
            if parent.getChild('enable'):
                paramName = parent.getName()
            return 'nodes.%s.parameters.edited.%s' % (nodeName, paramName)

    def __autoLayoutShadingNetworkNodes(self, nodes, viewState=None):
        """
        Automatically lays out all the shading, switch, snac and ShadingGroup
        nodes spatially in a broadly left to right organisational structure
        and sets their "View State" to "Connected Only"
        @type nodes: C{list}
        @type viewState: C{float} or C{None}
        @param nodes: A list of nodes to be repositioned.
        @param viewState: A view state to be applied to all repositioned nodes.
        """
        try:
            from UI4.Manifest import DrawingModule
        except:
            pass

        lockedNodes = []
        nodesToLayout = []
        for node in nodes:
            if node.getType() == 'NetworkMaterial':
                continue
            nodesToLayout.append(node)
            if node.isLocked():
                lockedNodes.append(node)
                node.setLocked(False)

        DrawingModule.AutoPositionNodes(nodesToLayout, oldStyle=True)
        DrawingModule.AutoPositionNodes(nodesToLayout, oldStyle=True)
        for node in nodesToLayout:
            x, y = NodegraphAPI.GetNodePosition(node)
            NodegraphAPI.SetNodePosition(node, (y * -4, x))
            if viewState is not None:
                NodegraphAPI.SetNodeShapeAttr(node, 'viewState', viewState)
            Utils.EventModule.QueueEvent('node_setShapeAttributes', hash(node), node=node)

        for node in lockedNodes:
            node.setLocked(True)

        return


_PortInfo = collections.namedtuple('PortInfo', ('portName', 'nodeSrcName', 'nodeName'))

def _traverseUpstreamOfInputPort(inputPort, shaderPorts):
    """
    Traverse to shader output port(s) from given input port.

    @type inputPort: C{NodegraphAPI.Port}
    @type shaderPorts: C{list} of C{NodegraphAPI.Port}
    @rtype: C{bool}
    @param inputPort: Input port to begin traversal from.
    @param shaderPorts: List to append collected output ports to.
    @return: C{True} if C{shaderPorts} contains multiple output ports as
        traversed through a SNAC node, C{False} otherwise.
    """
    isArray = False
    for outputPort in inputPort.getConnectedPorts():
        isUpstreamArray = _traverseUpstreamOfOutputPort(outputPort, shaderPorts)
        isArray |= isUpstreamArray

    return isArray


def _traverseUpstreamOfOutputPort(outputPort, shaderPorts):
    """
    Traverse to shader output port(s) from given output port.

    @type outputPort: C{NodegraphAPI.Port}
    @type shaderPorts: C{list} of C{NodegraphAPI.Port}
    @rtype: C{bool}
    @param outputPort: Output port to begin traversal from.
    @param shaderPorts: List to append collected output ports to.
    @return: C{True} if C{shaderPorts} contains multiple output ports as
        traversed through a SNAC node, C{False} otherwise.
    """
    outputNode = outputPort.getNode()
    outputNodeType = outputNode.getType()
    isArray = outputNodeType == 'ShadingNodeArrayConnector'
    if outputNodeType in ('Dot', 'ShadingNodeArrayConnector'):
        for upstreamInputPort in outputNode.getInputPorts():
            upstreamIsArray = _traverseUpstreamOfInputPort(upstreamInputPort, shaderPorts)
            isArray |= upstreamIsArray

    elif outputNodeType in ('Switch', 'VariableSwitch'):
        sourcePort, _ = outputNode.getInputPortAndGraphState(outputPort, NodegraphAPI.GetCurrentGraphState())
        for upstreamOutputPort in sourcePort.getConnectedPorts():
            upstreamIsArray = _traverseUpstreamOfOutputPort(upstreamOutputPort, shaderPorts)
            isArray |= upstreamIsArray

    elif outputNodeType == 'ShadingGroup':
        upstreamPort = _upstreamShadingGroupInputPort(outputPort)
        if upstreamPort is not None:
            upstreamIsArray = _traverseUpstreamOfInputPort(upstreamPort, shaderPorts)
            isArray |= upstreamIsArray
    else:
        shaderPorts.append(outputPort)
    return isArray


def _traverseDownstreamOfOutputPort(outputPort, shaderPorts):
    """
    Traverse to shader input port(s) from given output port.

    @type outputPort: C{NodegraphAPI.Port}
    @type shaderPorts: C{list} of C{NodegraphAPI.Port}
    @param outputPort: Output port to begin traversal from.
    @param shaderPorts: List to append collected input ports to.
    """
    for inputPort in outputPort.getConnectedPorts():
        _traverseDownstreamOfInputPort(inputPort, shaderPorts)


def _traverseDownstreamOfInputPort(inputPort, shaderPorts):
    """
    Traverse to shader input port(s) from given input port.

    @type inputPort: C{NodegraphAPI.Port}
    @type shaderPorts: C{list} of C{NodegraphAPI.Port}
    @param inputPort: Input port to begin traversal from.
    @param shaderPorts: List to append collected input ports to.
    """
    inputNode = inputPort.getNode()
    inputNodeType = inputNode.getType()
    if inputNodeType in ('Dot', 'ShadingNodeArrayConnector'):
        for downstreamOutputPort in inputNode.getOutputPorts():
            _traverseDownstreamOfOutputPort(downstreamOutputPort, shaderPorts)

    elif inputNodeType in ('Switch', 'VariableSwitch'):
        for downstreamOutputPort in inputNode.getOutputPorts():
            sourcePort, _ = inputNode.getInputPortAndGraphState(downstreamOutputPort, NodegraphAPI.GetCurrentGraphState())
            if sourcePort is inputPort:
                _traverseDownstreamOfOutputPort(downstreamOutputPort, shaderPorts)

    elif inputNodeType == 'ShadingGroup':
        downstreamPort = _downstreamShadingGroupOutputPort(inputPort)
        if downstreamPort is not None:
            _traverseDownstreamOfOutputPort(downstreamPort, shaderPorts)
    else:
        shaderPorts.append(inputPort)
    return


def _downstreamShadingGroupOutputPort(inputPort):
    """
    Get output port or send port on ShadingGroup connected to given input port.

    @type inputPort: C{NodegraphAPI.Port}
    @rtype: C{NodegraphAPI.Port}
    @param inputPort: Port to query connection to.
    @return: ShadingGroup send or output port, whichever is connected.
    """
    shadingGroup = inputPort.getNode()
    if shadingGroup.getInputPort(inputPort.getName()) is inputPort:
        downstreamPort = shadingGroup.getSendPort(inputPort.getName())
    else:
        downstreamPort = shadingGroup.getOutputPort(inputPort.getName())
    return downstreamPort


def _upstreamShadingGroupInputPort(outputPort):
    """
    Get input port or return port on ShadingGroup connected to given output
    port.

    @type outputPort: C{NodegraphAPI.Port}
    @rtype: C{NodegraphAPI.Port}
    @param outputPort: Port to query connection to.
    @return: ShadingGroup return or input port, whichever is connected.
    """
    shadingGroup = outputPort.getNode()
    if shadingGroup.getOutputPort(outputPort.getName()) is outputPort:
        upstreamPort = shadingGroup.getReturnPort(outputPort.getName())
    else:
        upstreamPort = shadingGroup.getInputPort(outputPort.getName())
    return upstreamPort


def _ExtractUserParamArray(newUserParamArray, userParamArrayAttr):
    """
    Insert elements into an array parameter from a multi-element attribute.

    @type newUserParamArray: C{NodegraphAPI.Parameter}
    @type userParamArrayAttr: C{PyFnScenegraphAttr.Attr}
    @rtype: C{NodegraphAPI.Parameter}
    @param newUserParamArray: Parameter to update.
    @param userParamArrayAttr: Source attribute to query.
    @return: C{newUserParamArray)
    """
    if userParamArrayAttr:
        attrList = list(userParamArrayAttr.getFnAttr().getData())
        for j, _ in enumerate(attrList):
            newVal = newUserParamArray.insertArrayElement(j)
            newVal.setValue(attrList[j], 0)

    return newUserParamArray


def _ExtractUserParameters(node, nodeUserParamsAttr):
    """
    Extract user parameters from attribute and create corresponding parameters
    on node.

    @type node: C{NodegraphAPI.Node}
    @type nodeUserParamsAttr: C{FnAttribute.GroupAttribute}
    @param node: Node to query and modify.
    @param nodeUserParamsAttr: User parameters as serialised to
        C{material.B{layout}} attributes.
    """
    if nodeUserParamsAttr:
        for i in range(nodeUserParamsAttr.getNumberOfChildren()):
            nodeUserParamAttr = nodeUserParamsAttr.getChildByIndex(i)
            userParamName = nodeUserParamAttr.getChildByName('name')
            userParamType = nodeUserParamAttr.getChildByName('type')
            userParamHints = nodeUserParamAttr.getChildByName('hints')
            userParamValue = nodeUserParamAttr.getChildByName('value')
            newParam = None
            if userParamName and userParamType:
                paramType = userParamType.getValue()
                paramName = userParamName.getValue()
                if paramType == 'string':
                    newParam = NodegraphAPI.UserParameters.CreateString(node, paramName)
                    if userParamValue:
                        newParam.setValue(userParamValue.getValue(), 0)
                elif paramType == 'number':
                    newParam = NodegraphAPI.UserParameters.CreateNumber(node, paramName)
                    if userParamValue:
                        newParam.setValue(userParamValue.getValue(), 0)
                elif paramType == 'stringArray':
                    newParam = NodegraphAPI.UserParameters.CreateStringArray(node, paramName)
                    _ExtractUserParamArray(newParam, userParamValue)
                elif paramType == 'numberArray':
                    newParam = NodegraphAPI.UserParameters.CreateNumberArray(node, paramName)
                    _ExtractUserParamArray(newParam, userParamValue)
                elif paramType == 'floatVector':
                    userParamsAttr = NodegraphAPI.UserParameters.GetUserParameter(node)
                    element = PyXmlIO.Element('floatvector_parameter')
                    element.setAttr('name', paramName)
                    newParam = userParamsAttr.createChildXmlIO(element)
                    if userParamValue:
                        newParam.setValue(list(userParamValue.getFnAttr().getData()), 0)
                elif paramType == 'group':
                    newParam = NodegraphAPI.UserParameters.CreateGroup(node, paramName)
                else:
                    log.warning('Node User Parameter type not recognised: %s, %s', node.getName(), paramType)
                if newParam:
                    if userParamHints:
                        newParam.setHintString(userParamHints.getValue())

    return


def _ExtractShadingGroupPorts(outputPorts, inputPorts, node, nodeName):
    """
    Populate a ShadingGroup node's ports to correspond to
    C{material.B{layout}}.

    @type outputPorts: C{FnAttribute.GroupAttribute}
    @type inputPorts: C{FnAttribute.GroupAttribute}
    @type node: C{NodegraphAPI.GroupNode}
    @type nodeName: C{str}
    @param outputPorts: C{GroupAttribute} extracted from C{material.B{layout}}
        containing the ShadingNode's output port specification.
    @param inputPorts: C{GroupAttribute} extracted from C{material.B{layout}}
        containing the ShadingNode's input port specification.
    @param node: ShadingGroup node
    @param nodeName: Ignored.
    """
    if outputPorts:
        for i in range(outputPorts.getNumberOfChildren()):
            portAttr = outputPorts.getChildByIndex(i)
            portName = portAttr.getChildByName('name').getValue()
            portDisplayName = portAttr.getChildByName('displayName').getValue()
            tags = portAttr.getChildByName('tags')
            if node.getOutputPort(portName):
                continue
            port = node.addOutputPort(portName)
            port.addOrUpdateMetadata('label', portDisplayName)
            if tags:
                tagList = list(tags.getFnAttr().getData())
                port.setTags(tagList)
                color = Nodes3DAPI.ShadingNodeBase.GetPortColor(tags=tagList)
                if color:
                    port.setColor(*color)

    if inputPorts:
        for i in range(inputPorts.getNumberOfChildren()):
            portAttr = inputPorts.getChildByIndex(i)
            portName = portAttr.getChildByName('name').getValue()
            portDisplayName = portAttr.getChildByName('displayName').getValue()
            tags = portAttr.getChildByName('tags')
            if node.getInputPort(portName):
                continue
            port = node.addInputPort(portName)
            port.addOrUpdateMetadata('label', portDisplayName)
            if tags:
                tagList = list(tags.getFnAttr().getData())
                port.setTags(tagList)
                color = Nodes3DAPI.ShadingNodeBase.GetPortColor(tags=tagList)
                if color:
                    port.setColor(*color)


def _GetParents(node, stopAtNode, parents):
    """
    Collects all parents of a given node until it reaches the stop node,
    or no parent is found.

    @type node: C{NodegraphAPI.Node}
    @type stopAtNode: C{NodegraphAPI.GroupNode}
    @type parents: C{set}
    @param node: The node whose parents we require.
    @param stopAtNode: A parent node which if found in the node's hierarchy,
        will stop the process.
    @param parents: A set in which to collect any ancestor nodes into.
    """
    parent = node.getParent()
    if not parent or parent is stopAtNode:
        return
    parents.add(parent)
    _GetParents(parent, stopAtNode, parents)


def _GetUpdateProgressCallback(totalNodes):
    """
    Create and configure a progress dialog to be shown when
    the population of a NetworkMaterialEdit node takes a while to complete.

    @type totalNodes: C{int}
    @rtype: C{Function}
    @param totalNodes: Total number of nodes to be constructed.
    @return: Callback method to update progress dialog.
    """
    mainWindow = UI4.App.MainWindow.GetMainWindow()
    if not mainWindow:

        def dummyCallback(_currentNodeCount):
            return True

        return dummyCallback
    progressDialog = UI4.Widgets.ProgressDialog(mainWindow, titleText='Enter NetworkMaterialEdit Node', labelText='Populating NetworkMaterialEdit contents...', maximumValue=totalNodes, interval=500)

    def progressCallback(currentNodeCount):
        """
        Callback for updating the progress dialog while XML text of nodes
        is being generated.

        @rtype: C{bool}
        @return: C{True} if the process should be continued, or C{False} if
            the process should be aborted.
        """
        return progressDialog.update(currentNodeCount)

    return progressCallback


def _GetSNACNodeConnections(snacNode):
    """
    Returns all the connected ports upstream of a ShadingNodeArrayConnector
    node.

    @type snacNode: C{NodegraphAPI.Node}
    @rtype: C{list} of C{tuple} of C{NodegraphAPI.Port}
    @param snacNode: SNAC node.
    @return: List of 2-tuples containing connected output port and SNAC
        input port.
    """
    upstreamPorts = []
    for inputPort in snacNode.getInputPorts():
        if not inputPort.getNumConnectedPorts():
            continue
        upstreamPorts.append((inputPort.getConnectedPort(0), inputPort))

    return upstreamPorts