# uncompyle6 version 3.8.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Oct 30 2018, 23:45:53) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Warning: this version of Python has problems handling the Python 3 byte type in constants properly.

# Embedded file name: SuperTools/NetworkMaterials/v1/NetworkMaterialCreateNode.py
# Compiled at: 2022-08-18 19:44:51
"""
Module defining the L{NetworkMaterialCreateNode} class.
"""
from __future__ import absolute_import
import functools, logging, operator, posixpath, re, Utils
from Katana import Configuration, FnAttribute, NodegraphAPI, UniqueName
from NodegraphAPI_cmodule import PythonNode
from .NetworkMaterialBaseNode import GetNodeFromParam, NetworkMaterialBaseNode, SanitizeSceneGraphLocationString
log = logging.getLogger('NetworkMaterialCreate.Node')
NodegraphAPI.AddNodeFlavor('NetworkMaterialCreate', '3d')

class NetworkMaterialCreateNode(NetworkMaterialBaseNode):
    """
    Class implementing the NetworkMaterialCreate SuperTool node type.
    """

    def __init__(self):
        """
        Initializes an instance of this class.
        """
        NetworkMaterialBaseNode.__init__(self)
        paramsGroup = self.getParameters()
        prefixParam = paramsGroup.createChildString('rootLocation', '/root/materials')
        prefixParam.setHintString("{'widget': 'scenegraphLocation','help': 'The root location under which the material locations will be created.'}")
        networkMaterials = self.getNetworkMaterials()
        for networkMaterialNode in networkMaterials:
            networkMaterialNode.setAutoRenameAllowed(False)
            self.__setSceneGraphLocation(networkMaterialNode)

    def _setupInternalNetwork(self):
        """
        Construct the hidden utility nodes for this SuperTool.

        Create internal Merge for merging NetworkMaterials.
        """
        mergeNode = NodegraphAPI.CreateNode('Merge', self)
        mergeNodeParam = self.getParameters().createChildString('__node_merge', '')
        mergeNodeParam.setExpression('@%s' % mergeNode.getName())
        mergeNode.getParameters().createChildNumber('__hidden', 1.0).setHintString('{"widget": "null"}')
        mergeNode.getOutputPort('out').connect(self.getReturnPort('out'))

    def getScenegraphLocation(self):
        """
        This function allows for older scenes with sceneGraphLocationFromNode
        expressions to this NMC node to continue to work, however this
        function is @deprecated and should not be used in new scenes.
        @return: the first NetworkMaterial location managed by this
        NetworkMaterial node
        """
        networkMaterialLocations = self.getNodesCreatingSceneGraphLocations()
        if not networkMaterialLocations:
            return ''
        return networkMaterialLocations[0].getScenegraphLocation()

    def handleNetworkMaterialNodeCreate(self, networkMaterialNode):
        """
        Handles the creation of a NetworkMaterial node's utility nodes
        (GroupStack and Material), connects the result up to the internal
        Merge node, and creates any required namespace nodes.

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
            if networkMaterialNode not in self.getNetworkMaterials():
                namespaceParam = networkMaterialNode.getParameter('namespace')
                eventualNamespace = namespaceParam.getValue(0)
                Utils.UndoStack.DisableCapture()
                try:
                    namespaceParam.setValue('', 0)
                    self.__createUtilNodesAndMergeNetworkMaterial(networkMaterialNode)
                    self.__setSceneGraphLocation(networkMaterialNode)
                    if networkMaterialNode.getNumInputPorts() == 0:
                        self.addInputTerminals(networkMaterialNode)
                finally:
                    Utils.UndoStack.EnableCapture()

                if eventualNamespace and (Utils.UndoStack.IsUndoEnabled() or not Configuration.get('KATANA_UI_MODE')):
                    Utils.UndoStack.OpenGroup('Ensure namespace %s for %s' % (
                     eventualNamespace,
                     networkMaterialNode.getParameter('name').getValue(0)))
                    try:
                        leafNamespaceNode = self.addNamespace(eventualNamespace, makeUnique=False)
                        self.reparentNamespace(networkMaterialNode, leafNamespaceNode)
                    finally:
                        Utils.UndoStack.CloseGroup()

            else:
                self.__refreshNetworkMaterialParameters(networkMaterialNode)
            Utils.EventModule.QueueEvent('nodegraph_nmc_nm_create', hash(self), node=networkMaterialNode)
            return

    def getRootLocation(self):
        """
        @rtype: C{str}
        @return: The path of the scene graph location under which material
            locations are created by this node.
        @since: Katana 4.0v1
        """
        param = self.getParameter('rootLocation')
        if param:
            return param.getValue(0)
        else:
            return ''

    def getNetworkMaterials(self):
        """
        Return a list of NetworkMaterial nodes connected to the internal Merge.

        @rtype: C{list} of C{NodegraphAPI.Node}
        @return: NetworkMaterial nodes.
        @since: Katana 4.0v1
        """
        return [ node for node in self.getMaterialLocationNodesInMergeOrder() if node.getType() == 'NetworkMaterial'
               ]

    def getNamespaceNodes(self):
        """
        Return a list of LocationCreate nodes connected to the internal Merge.

        @rtype: C{list} of C{NodegraphAPI.Node}
        @return: LocationCreate namepsace nodes.
        @since: Katana 4.0v1
        """
        return [ node for node in self.getMaterialLocationNodesInMergeOrder() if node.getType() == 'LocationCreate'
               ]

    def getMaterialLocationNodesInMergeOrder(self):
        """
        Get NetworkMaterial / LocationCreate nodes in order of Merge
        connection.

        @rtype: C{list} of C{NodegraphAPI.Node}
        @return: List of nodes.
        @since: Katana 4.0v1
        """
        mergeNode = GetNodeFromParam(self, '__node_merge')
        namespaceNodes = []
        self.__traverseToNamespaceNodes(mergeNode, namespaceNodes)
        return namespaceNodes

    @classmethod
    def __traverseToNamespaceNodes(cls, downstreamNode, namespaceNodes):
        """
        Recursively traverse through all input ports of C{downstreamNode} to
        the nearest connected NetworkMaterial or LocationCreate nodes.

        @type downstreamNode: C{NodegraphAPI.Node}
        @type namespaceNodes: C{list} of C{NodegraphAPI.Node}
        @param downstreamNode: Node to start searching from.
        @param namespaceNodes: List of namespace nodes to append to.
        """
        for downstreamInputPort in downstreamNode.getInputPorts():
            for upstreamOutputPort in downstreamInputPort.getConnectedPorts():
                upstreamNode = upstreamOutputPort.getNode()
                if upstreamNode.getType() in ('LocationCreate', 'NetworkMaterial'):
                    namespaceNodes.append(upstreamNode)
                else:
                    cls.__traverseToNamespaceNodes(upstreamNode, namespaceNodes)

    def getContentsLayoutAttributes(self, forNetworkMaterial=None, **kwargs):
        """
        Construct the layout attributes of child nodes (and their descendents)

        @type forNetworkMaterial: C{NodegraphAPI.Node} or C{None}
        @rtype: C{FnAttribute.GroupAttribute}
        @param forNetworkMaterial: Exclude all NetworkMaterial nodes from the
            attributes except for this one.
        @param kwargs: Ignored
        @return: Layout attributes.
        """
        layoutAttrs = NetworkMaterialBaseNode.getContentsLayoutAttributes(self)
        if forNetworkMaterial is None:
            return layoutAttrs
        else:
            gb = FnAttribute.GroupBuilder()
            gb.update(layoutAttrs)
            otherNetworkMaterialNames = (nm.getName() for nm in self.getNetworkMaterials() if nm is not forNetworkMaterial)
            for nodeName in otherNetworkMaterialNames:
                gb.delete(nodeName)

            return gb.build()

    def _getExcludedNodes(self):
        """
        Get the list of nodes that should be excluded from
        C{material.B{layout}} attributes.

        Augment base class list with internal Merge and LocationCreate nodes.

        @rtype: C{set} of C{NodegraphAPI.Node}
        @return: List of internal hidden nodes.
        """
        excludedNodes = NetworkMaterialBaseNode._getExcludedNodes(self)
        excludedNodes.add(self._getNodeFromParam('__node_merge'))
        excludedNodes |= set(self.getNamespaceNodes())
        return excludedNodes

    def makeNamespaceUnique(self, namespaceName, forNode=None):
        """
        Get a unique scene graph location string within this
        NetworkMaterialCreate.

        @type namespaceName: C{str}
        @type forNode: C{NodegraphAPI.Node}
        @rtype: C{str}
        @param namespaceName: A sanitized string representing a scene graph
            location.
        @param forNode: The node that represents this namespace or C{None}.
        @return: A sanitized string representing a scene graph location that
            is unique to this network material create node.
        @since: Katana 4.0v1
        """
        locationNodes = self.getMaterialLocationNodesInMergeOrder()
        if forNode is not None:
            isNotNode = functools.partial(operator.is_not, forNode)
            locationNodes = filter(isNotNode, locationNodes)
        namespaceLocations = [ MaterialLocation(node).path for node in locationNodes ]
        isAlreadyUsed = functools.partial(operator.contains, namespaceLocations)
        return UniqueName.GetUniqueName(namespaceName, isAlreadyUsed)

    def __setSceneGraphLocation(self, networkMaterialNode):
        """
        Set the B{sceneGraphLocation} parameter on a NetworkMaterial node to an
        expression combining this NetworkMaterialCreate's B{rootLocation}
        and the NetworkMaterial's B{namespace} and B{name} parameters.

        @type networkMaterialNode: C{NodegraphAPI.Node}
        @param networkMaterialNode: NetworkMaterial node to edit.
        """
        if not networkMaterialNode:
            return
        locationParam = networkMaterialNode.getParameter('sceneGraphLocation')
        if locationParam:
            locationParam.setExpression("=^/rootLocation+~/namespace+'/'+~/name")

    def addNetworkMaterialNode(self, namespace=None):
        """
        Add a new NetworkMaterial node, potentially constructing LocationCreate
        namespace nodes, ensuring proper ordering in the internal Merge.

        @type namespace: C{str} or C{None}
        @param namespace: Namespace to create NetworkMaterial under.
            LocationCreate nodes will be constructed for missing namespace
            branches.
        @since: Katana 4.0v1
        """
        Utils.UndoStack.OpenGroup('Create NetworkMaterial')
        try:
            leafNamespaceNode = None
            if namespace is not None:
                leafNamespaceNode = self.addNamespace(namespace, makeUnique=False)
            newNode = NodegraphAPI.CreateNode('NetworkMaterial', self)
            newNode.setAutoRenameAllowed(False)
            self.__setSceneGraphLocation(newNode)
            newNode.getParameter('name').setValue('NetworkMaterial', 0)
            self.__createUtilNodesAndMergeNetworkMaterial(newNode)
            self.addInputTerminals(newNode)
            self.reparentNamespace(newNode, leafNamespaceNode, isNewNode=True)
        finally:
            Utils.UndoStack.CloseGroup()

        return

    def __createUtilNodesAndMergeNetworkMaterial(self, networkMaterialNode):
        """
        Create and connect Material and GroupStack nodes for a given
        NetworkMaterial and hook it all up to the internal Merge.

        @type networkMaterialNode: C{NodegraphAPI.Node}
        @param networkMaterialNode: a NetworkMaterial node.
        @raise TypeError: if a non-NetworkMaterial node is provided.
        """
        if not isinstance(networkMaterialNode, PythonNode) or networkMaterialNode.getType() != 'NetworkMaterial':
            raise TypeError('This function Requires a NetworkMaterial node')
        _groupStack, materialNode = self._createNetworkMaterialUtilNodes(networkMaterialNode)
        mergeNode = self._getNodeFromParam('__node_merge')
        if mergeNode is None:
            log.warning('No Merge node found in NetworkMaterial Super Tool')
            return
        else:
            materialNode.getOutputPort('out').connect(mergeNode.addInputPort('i'))
            nmParams = networkMaterialNode.getParameters()
            nmParams.createChildNumber('__disableDefaultsTab', 1)
            return

    def duplicateNetworkMaterialNode(self, networkMaterial, namespace=None):
        """
        Duplicate a given internal NetworkMaterial node, including it's utility
        Material and GroupStack nodes.

        @type networkMaterial: C{NodegraphAPI.Node}
        @type namespace: C{str} or C{None}
        @param networkMaterial: Internal NetworkMaterial node to duplicate.
        @param namespace: Optionally override scene graph location namespace
            for the new node.
        @raise TypeError: If a non-NetworkMaterial node is given.
        @since: Katana 4.0v1
        """
        if not isinstance(networkMaterial, PythonNode) or networkMaterial.getType() != 'NetworkMaterial':
            raise TypeError('This function Requires a NetworkMaterial node')
        Utils.UndoStack.OpenGroup('Duplicate material "%s"' % networkMaterial.getParameter('name').getValue(0))
        try:
            if not namespace:
                namespace = networkMaterial.getParameter('namespace').getValue(0)
            mergeNode = GetNodeFromParam(self, '__node_merge')
            groupStack = GetNodeFromParam(networkMaterial, '__node_groupStack')
            materialNode = GetNodeFromParam(networkMaterial, '__node_materialEdit')
            if not mergeNode or not groupStack or not materialNode:
                raise Exception('Attempting to duplicate a NetworkMaterial that is either outside of NMC or is otherwise badly formed.')
            nodesToCopy = {
             networkMaterial, groupStack, materialNode}
            inputPorts = networkMaterial.getInputPorts()
            for port in inputPorts:
                connectedPorts = port.getConnectedPorts()
                for connectedPort in connectedPorts:
                    nodesToCopy.add(connectedPort.getNode())

            nodesToCopy = list(nodesToCopy)
            NodegraphAPI.SetAllSelectedNodes([])
            pastedNodes = NodegraphAPI.Util.DuplicateNodes(nodesToCopy)
            newNetworkMaterial = None
            for node in pastedNodes:
                offset = 30
                x, y = NodegraphAPI.GetNodePosition(node)
                NodegraphAPI.SetNodePosition(node, (x + offset, y - offset))
                if node.getType() == 'NetworkMaterial':
                    newNetworkMaterial = node
                elif node.getType() == 'Material':
                    node.getOutputPort('out').connect(mergeNode.addInputPort('i'))
                elif node.getType() != 'GroupStack':
                    NodegraphAPI.SetNodeSelected(node, True)

            namespaceNode = self.findNamespaceNode(namespace)
            newNetworkMaterial.getParameter('namespace').setValue('', 0)
            self.reparentNamespace(newNetworkMaterial, namespaceNode, isNewNode=True)
            _PageShapeAttrs(self).copy(MaterialLocation(networkMaterial).path, MaterialLocation(newNetworkMaterial).path)
        finally:
            Utils.UndoStack.CloseGroup()

        return

    def setNetworkMaterialNodeName(self, networkMaterialNode, proposedName):
        """
        Set the name of a NetworkMaterial, ensuring a unique scene graph
        location.

        @type networkMaterialNode: C{NodegraphAPI.Node}
        @type proposedName: C{str}
        @param networkMaterialNode: NetworkMaterial node.
        @param proposedName: Name to set.
        @since: Katana 4.0v1
        """
        proposedName = self.__sanitiseLocationLeafName(proposedName)
        location = MaterialLocation(networkMaterialNode)
        proposedPath = location.renamed(proposedName)
        newPath = self.makeNamespaceUnique(proposedPath, forNode=networkMaterialNode)
        newName = posixpath.basename(newPath)
        Utils.UndoStack.OpenGroup('Rename material "%s" to "%s"' % (location.leafPath, newName))
        try:
            networkMaterialNode.setName(newName)
            location.setPath(newPath)
        finally:
            Utils.UndoStack.CloseGroup()

    def duplicateNamespace(self, namespaceNode):
        """
        Duplicate a LocationCreate namespace node and all it's children.

        @type namespaceNode: C{NodegraphAPI.Node}
        @param namespaceNode: LocationCreate node to duplicate.
        @raise TypeError: If given node is not a LocationCreate.
        @since: Katana 4.0v1
        """
        if not isinstance(namespaceNode, PythonNode) or namespaceNode.getType() != 'LocationCreate':
            raise TypeError('This function Requires a LocationCreate node')
        srcLocation = MaterialLocation(namespaceNode)
        pageShapeAttrs = _PageShapeAttrs(self)
        Utils.UndoStack.OpenGroup('Duplicate group "%s"' % srcLocation.path)
        try:
            destNode = self.addNamespace(srcLocation.path)
            destLocation = MaterialLocation(destNode)
            pageShapeAttrs.copy(srcLocation.path, destLocation.path)
            for otherNode in self.getMaterialLocationNodesInMergeOrder():
                srcChildLocation = MaterialLocation(otherNode)
                if not srcLocation.isAncestorOf(srcChildLocation.path):
                    continue
                destChildPath = srcChildLocation.reparented(srcLocation.path, destLocation.path)
                if srcChildLocation.node.getType() == 'NetworkMaterial':
                    destNamespace = posixpath.dirname(destChildPath)
                    self.duplicateNetworkMaterialNode(srcChildLocation.node, namespace=destNamespace)
                elif srcChildLocation.node.getType() == 'LocationCreate':
                    self.addNamespace(destChildPath, False)
                pageShapeAttrs.copy(srcChildLocation.path, destChildPath)

        finally:
            Utils.UndoStack.CloseGroup()

    def setNamespaceLeafName(self, namespaceNode, proposedName):
        """
        Set the leaf part of the namespace of a LocationCreate, ensuring a
        unique scene graph location.

        Also scan through child NetworkMaterial and LocationCreate nodes
        updating their namespaces.

        @type namespaceNode: C{NodegraphAPI.Node}
        @type proposedName: C{str}
        @param namespaceNode: LocationCreate node.
        @param proposedName: Name to set.
        @since: Katana 4.0v1
        """
        proposedName = self.__sanitiseLocationLeafName(proposedName)
        location = MaterialLocation(namespaceNode)
        proposedPath = location.renamed(proposedName)
        newPath = self.makeNamespaceUnique(proposedPath, forNode=namespaceNode)
        Utils.UndoStack.OpenGroup('Rename group "%s" to "%s"' % (
         location.leafPath, posixpath.basename(newPath)))
        try:
            for otherNode in self.getMaterialLocationNodesInMergeOrder():
                if otherNode is namespaceNode:
                    continue
                otherLocation = MaterialLocation(otherNode)
                if otherLocation.isDescendentOf(location.path):
                    newLocation = otherLocation.reparented(location.path, newPath)
                    otherLocation.setPath(newLocation)

            location.setPath(newPath)
        finally:
            Utils.UndoStack.CloseGroup()

    def reparentNamespace(self, node, parent, offset=-1, isNewNode=False):
        """
        Update namespace of given node and it's children to be under given
        parent, with order among siblings given by offset

        @type node: C{NodegraphAPI.Node}
        @type parent: C{NodegraphAPI.Node} or C{None}
        @type offset: C{int}
        @type isNewNode: C{bool}
        @param node: NetworkMaterial or LocationCreate node to re-parent.
        @param parent: LocationCreate node to be new parent, or C{None} to
            place at root.
        @param offset: Offset among new siblings to place node, or C{-1} to
            place at end.
        @param isNewNode: Flag that C{node} is newly created.
        @raise TypeError: If incorrect parent node type given.
        @raise ValueError: If attempting to re-parent node under itself.
        @since: Katana 4.0v1
        """
        if parent is not None and parent.getType() != 'LocationCreate':
            raise TypeError('%s node %s cannot be used as a namespace' % (
             parent.getType(), parent.getName()))
        if node == parent:
            raise ValueError('Cannot reparent node %s under itself' % node.getName())
        nodeLocation = MaterialLocation(node)
        newParentLocation = MaterialLocation(parent)
        if nodeLocation.isAncestorOf(newParentLocation.path):
            raise ValueError('Cannot reparent node %s under itself' % node.getName())
        locationNodes = self.getMaterialLocationNodesInMergeOrder()
        locations = [ MaterialLocation(otherNode) for otherNode in locationNodes ]
        childLocations = [ location for location in locations if location.isDescendentOf(nodeLocation.path)
                         ]
        proposedPath = nodeLocation.reparented(nodeLocation.parentPath, newParentLocation.path)
        newPath = self.makeNamespaceUnique(proposedPath, forNode=node)
        fromIdxStart = locationNodes.index(node)
        if childLocations:
            fromIdxEnd = locationNodes.index(childLocations[(-1)].node) + 1
        else:
            fromIdxEnd = fromIdxStart + 1
        if parent is None:
            toIdxStart = 0
        else:
            toIdxStart = locationNodes.index(parent) + 1
        for toIdxStart in xrange(toIdxStart, len(locations)):
            location = locations[toIdxStart]
            if offset == -1:
                if location.isAncestorOf(newPath):
                    break
            else:
                if offset == 0:
                    break
                if location.isSiblingOf(newPath):
                    offset -= 1
        else:
            toIdxStart += 1

        for toIdxStart in xrange(toIdxStart, len(locations)):
            location = locations[toIdxStart]
            if location.isSiblingOf(newPath):
                break

        if toIdxStart == fromIdxStart and nodeLocation.parentPath == newParentLocation.path:
            return
        else:
            mergeNode = GetNodeFromParam(self, '__node_merge')
            mergeNodeInputPorts = mergeNode.getInputPorts()
            upstreamPorts = [ port.getConnectedPorts()[0] if port.getConnectedPorts() else None for port in mergeNodeInputPorts
                            ]
            if toIdxStart > fromIdxStart:
                shiftDistance = toIdxStart - fromIdxStart - 1
                newUpstreamPorts = upstreamPorts[:fromIdxStart] + upstreamPorts[fromIdxEnd:fromIdxEnd + shiftDistance] + upstreamPorts[fromIdxStart:fromIdxEnd] + upstreamPorts[fromIdxEnd + shiftDistance:]
            elif toIdxStart < fromIdxStart:
                shiftDistance = fromIdxStart - toIdxStart
                newUpstreamPorts = upstreamPorts[:toIdxStart] + upstreamPorts[fromIdxStart:fromIdxEnd] + upstreamPorts[toIdxStart:toIdxStart + shiftDistance] + upstreamPorts[fromIdxEnd:]
            else:
                newUpstreamPorts = upstreamPorts
            Utils.UndoStack.OpenGroup('Move %s location "%s" to "%s"' % (
             'material' if node.getType() == 'NetworkMaterial' else 'group',
             nodeLocation.leafPath, newParentLocation.path))
            try:
                for portNum, upstreamPort in enumerate(newUpstreamPorts):
                    if upstreamPort is None:
                        continue
                    for downstreamPort in upstreamPort.getConnectedPorts():
                        upstreamPort.disconnect(downstreamPort)

                    upstreamPort.connect(mergeNodeInputPorts[portNum])

                for childLocation in childLocations:
                    proposedPath = childLocation.reparented(nodeLocation.path, newPath)
                    newChildPath = self.makeNamespaceUnique(proposedPath, forNode=childLocation.node)
                    childLocation.setPath(newChildPath)

                nodeLocation.setPath(newPath, isNewNode=isNewNode)
            finally:
                Utils.UndoStack.CloseGroup()

            return

    def findNamespaceNode(self, namespaceName):
        """
        Returns a node that represents a namespace or C{None} depending on if
        one exists to represent it or not.

        @type namespaceName: C{str}
        @rtype: C{NodegraphAPI.Node} or C{None}
        @param namespaceName: Namespace string to match against.
        @return: LocationCreate node matching namespace, or C{None} if not
            found.
        @since: Katana 4.0v1
        """
        nsNodes = self.getNamespaceNodes()
        for node in nsNodes:
            namespaceParam = node.getParameter('namespaceName')
            if namespaceParam:
                namespaceVal = namespaceParam.getValue(NodegraphAPI.GetCurrentTime())
                if namespaceVal == namespaceName:
                    return node

        return

    def __addNamespaceUnique(self, name, parent):
        """
        Adds a LocationCreate namespace node if it does not already exist.

        Note: only handles the namespace matching C{name}, not its parents.

        @rtype: C{NodegraphAPI.Node}
        @type name: C{str}
        @type parent: C{NodegraphAPI.Node} or C{None}
        @param name: A scene graph location string.
        @param parent: Parent LocationCreate namespace node, or None for root.
        @return: Newly created or found LocationCreate namespace node.
        """
        node = self.findNamespaceNode(name)
        if not node:
            node = NodegraphAPI.CreateNode('LocationCreate', self)
            node.setName(name)
            self.handleNamespaceCreate(node, '/__TEMPORARY_NAME__', True)
            self.reparentNamespace(node, parent, isNewNode=True)
            node.getParameter('namespaceName').setValue(name, 0)
        return node

    def addNamespace(self, name='/namespace', makeUnique=True):
        """
        Ensure a hierarchy of LocationCreate namespace nodes exists
        representing given scene graph location name.

        @type name: C{str}
        @type makeUnique: C{bool}
        @rtype: C{NodegraphAPI.Node}
        @param name: Scene graph location name.
        @param makeUnique: If C{True} then modify given C{name} to ensure it
            produces a unique scene graph location within this
            NetworkMaterialCreate.
        @return: Leaf LocationCreate node in constructed hierarchy.
        @since: Katana 4.0v1
        """
        namespaceName = SanitizeSceneGraphLocationString(name)
        if makeUnique:
            namespaceName = self.makeNamespaceUnique(namespaceName)
        Utils.UndoStack.OpenGroup('Create group "%s"' % namespaceName)
        try:
            leaf = None
            locationSplit = filter(None, namespaceName.split('/'))
            locationAsBuilt = ''
            for locationComponent in locationSplit:
                locationAsBuilt = locationAsBuilt + '/' + locationComponent
                leaf = self.__addNamespaceUnique(locationAsBuilt, leaf)

            return leaf
        finally:
            Utils.UndoStack.CloseGroup()

        return

    def deleteNamespace(self, node):
        """
        Delete a NetworkMaterial or LocationCreate namespace, including all
        descendents, from this NetworkMaterialCreate.

        Also cleans up internal utility nodes.

        @type node: C{NodegraphAPI.Node}
        @param node: LocationCreate or NetworkMaterial node to delete.
        @since: Katana 4.0v1
        """
        if node.isMarkedForDeletion():
            return
        location = MaterialLocation(node)
        locations = [ MaterialLocation(otherNode) for otherNode in self.getMaterialLocationNodesInMergeOrder()
                    ]
        Utils.UndoStack.OpenGroup('Delete %s' % location.path)
        try:
            self.__deleteNamespaceRecursively(location, locations)
            self._cleanMergeNodePorts()
        finally:
            Utils.UndoStack.CloseGroup()

    def __deleteNamespaceRecursively(self, location, locations):
        """
        Recursively delete NetworkMaterial / LocationCreate hierarchy.

        @type location: L{MaterialLocation}
        @type locations: C{list} of L{MaterialLocation}
        @param location: Wrapper around node to delete.
        @param locations: Potential descendent locations.
        """
        descendents = [ child for child in locations if location.isAncestorOf(child.path) ]
        children = (child for child in descendents if child.isChildOf(location.path))
        for child in children:
            self.__deleteNamespaceRecursively(child, descendents)

        location.node.delete()
        if location.node.getType() == 'NetworkMaterial':
            self._cleanUpDeletedNetworkMaterial(location.node)

    def __refreshNetworkMaterialParameters(self, node):
        """
        Refreshes the B{__node_groupStack} and B{__node_materialEdit}
        parameters to point at the nodes that are connected to the output port
        of a given NetworkMaterial node.

        @type node: C{NodegraphAPI.Node}
        @param node: A NetworkMaterial node that is part of this NMC super
           tool that already has GroupStack and Material utility nodes
           connected to it.
        """
        if node is None:
            return
        else:
            if node.getType() != 'NetworkMaterial':
                return
            if node.getParent() != self:
                return
            Utils.UndoStack.DisableCapture()
            try:
                groupStackNode = None
                materialEditNode = None
                groupStackPort = node.getOutputPort('out').getConnectedPort(0)
                if groupStackPort:
                    groupStackNode = groupStackPort.getNode()
                    materialEditPort = groupStackNode.getOutputPort('out').getConnectedPort(0)
                    if materialEditPort:
                        materialEditNode = materialEditPort.getNode()
                groupStackParam = node.getParameter('__node_groupStack')
                materialEditParam = node.getParameter('__node_materialEdit')
                if groupStackParam and groupStackNode:
                    groupStackParam.setExpression('@%s' % groupStackNode.getName())
                if materialEditParam and materialEditNode:
                    materialEditParam.setExpression('@%s' % materialEditNode.getName())
            finally:
                Utils.UndoStack.EnableCapture()

            return

    __invalidNameCharsRegexp = re.compile('[^a-zA-Z0-9]')

    def __sanitiseLocationLeafName(self, proposedName):
        proposedName = self.__invalidNameCharsRegexp.sub('_', proposedName)
        if proposedName == '':
            proposedName = '_'
        return proposedName


class MaterialLocation(object):
    """
    Utility class to wrap a NetworkMaterial or LocationCreate node and provide
    common queries and actions on their namespace.
    """

    def __init__(self, node):
        """
        Initializes an instance of this class.

        @type node: C{NodegraphAPI.Node}
        @param node: NetworkMaterial or Location create node to wrap.
        """
        self.__node = node
        self.__path = None
        self.__parentPath = None
        self.__leafPath = None
        self.__namespaceParam = None
        return

    def reparented(self, fromPath, toPath):
        """
        Get scene graph location path of node if initial part of path was
        changed.

        @type fromPath: C{str}
        @type toPath: C{str}
        @rtype: C{str}
        @param fromPath: Parent path part to replace.
        @param toPath: New parent path.
        @return: Proposed new path.
        """
        newNamespace = posixpath.normpath(posixpath.join(fromPath, posixpath.relpath(toPath, fromPath), posixpath.relpath(self.path, fromPath)))
        return newNamespace

    def renamed(self, name):
        """
        Get scene graph location path of node if leaf part of path was changed.

        @type name: C{str}
        @rtype: C{str}
        @param name: New leaf location name.
        @return: Proposed new path.
        """
        return posixpath.join(self.parentPath, name)

    def setPath(self, path, isNewNode=False):
        """
        Update namespace/name parameter(s) with given path.

        Also update page expanded/collapsed state IDs.

        @type path: C{str}
        @type isNewNode: C{bool}
        @param path: New scene graph location path.
        @param isNewNode: Flag that this is a new node (so page state will not
            be moved under new ID).
        """
        if not isNewNode:
            _PageShapeAttrs(self.node.getParent()).updateID(self.path, path)
        if self.__node.getType() == 'NetworkMaterial':
            path, name = posixpath.split(path)
            self.__node.getParameter('name').setValue(name, 0)
            if path == '/':
                path = ''
        self.namespaceParam.setValue(path, 0)
        self.__path = None
        self.__parentPath = None
        self.__leafPath = None
        return

    def isAncestorOf(self, namespace):
        """
        Check whether this location is an ancestor of given namespace.

        @type namespace: C{str}
        @rtype: C{bool}
        @param namespace: namespace to check.
        @return: C{True} if is ancestor, C{False} otherwise.
        """
        if namespace == self.path:
            return False
        return self.__commonPrefixEqual(self.path, namespace, self.path)

    def isDescendentOf(self, namespace):
        """
        Check whether this location is a descendent of given namespace.

        @type namespace: C{str}
        @rtype: C{bool}
        @param namespace: namespace to check.
        @return: C{True} if is descendent, C{False} otherwise.
        """
        if namespace == self.path:
            return False
        return self.__commonPrefixEqual(self.path, namespace, namespace)

    def isChildOf(self, namespace):
        """
        Check whether this location is a direct child of given namespace.

        @type namespace: C{str}
        @rtype: C{bool}
        @param namespace: namespace to check.
        @return: C{True} if is descendent, C{False} otherwise.
        """
        if namespace == self.path:
            return False
        return posixpath.relpath(self.path, namespace) == self.leafPath

    def isSiblingOf(self, namespace):
        """
        Check whether this location is a sibling of (or is equal to) namespace.

        @type namespace: C{str}
        @rtype: C{bool}
        @param namespace: namespace to check.
        @return: C{True} if is sibling, C{False} otherwise.
        """
        return posixpath.relpath(namespace, self.parentPath) == posixpath.basename(namespace)

    @property
    def node(self):
        """
        @rtype: C{NodegraphAPI.Node}
        @return: Wrapped node.
        """
        return self.__node

    @property
    def parentPath(self):
        """
        @rtype: C{str}
        @return: Parent scene graph location path.
        """
        if self.__node is None:
            return ''
        else:
            if self.__parentPath is None:
                self.__parentPath = posixpath.dirname(self.path)
            return self.__parentPath

    @property
    def leafPath(self):
        """
        @rtype: C{str}
        @return: Leaf part of scene graph location path.
        """
        if self.__node is None:
            return ''
        else:
            if self.__leafPath is None:
                self.__leafPath = posixpath.basename(self.path)
            return self.__leafPath

    @property
    def path(self):
        """
        @rtype: C{str}
        @return: Full scene graph location path.
        """
        if self.__node is None:
            return '/'
        else:
            if self.__path is None:
                self.__path = self.namespaceParam.getValue(0)
                if self.__node.getType() == 'NetworkMaterial':
                    self.__path = posixpath.join(self.__path, self.__node.getParameter('name').getValue(0))
                self.__path = SanitizeSceneGraphLocationString(self.__path)
            return self.__path

    @property
    def namespaceParam(self):
        """
        @rtype: C{NodegraphAPI.Parameter}
        @return: B{namespaceName} parameter if wrapping a LocationCreate node,
            B{namespace} parameter if wrapping a NetworkMaterial node.
        """
        if self.__node is None:
            return
        else:
            if self.__namespaceParam is None:
                if self.__node.getType() == 'LocationCreate':
                    paramName = 'namespaceName'
                else:
                    paramName = 'namespace'
                self.__namespaceParam = self.__node.getParameter(paramName)
            return self.__namespaceParam

    @staticmethod
    def __commonPrefixEqual(lhs, rhs, prefix):
        """
        Check if given prefix is equivalent to the common path part of two
        given paths.

        @type lhs: C{str}
        @type rhs: C{str}
        @rtype: C{bool}
        @param lhs: First path.
        @param rhs: Second path.
        @param prefix: Path prefix to compare.
        @return: C{True} if C{prefix} matches the largest common prefix of
            C{lhs} and C{rhs}, C{False} otherwise.
        """
        return posixpath.dirname(posixpath.commonprefix([lhs + '/', rhs + '/'])) == prefix


class _PageShapeAttrs(object):
    """
    Utility class to perform common functions on the expanded/collapsed page
    state of NetworkMaterials and their namespaces.
    """

    def __init__(self, nmc):
        """
        Initializes an instance of this class.

        @type nmc: C{NodegraphAPI.Node}
        @param nmc: NetworkMaterialCreate node.
        """
        self.__nmc = nmc

    def updateID(self, oldPath, newPath):
        """
        Update the page state ID for a renamed/moved location path.

        @type oldPath: C{str}
        @type newPath: C{str}
        @param oldPath: Previous scene graph location path.
        @param newPath: Updated scene graph location path.
        """
        oldPageID = self.__id(oldPath)
        newPageID = self.__id(newPath)
        oldPageRegExp = re.compile('(?<!> )%s\\b' % oldPageID)
        shapeAttrs = self.__getShapeAttrs()
        for stateType in ('expandedPages', 'collapsedPages'):
            shapeAttrForState = shapeAttrs.get(stateType)
            if shapeAttrForState is None:
                continue
            shapeAttrs[stateType] = oldPageRegExp.sub(newPageID, shapeAttrForState)

        self.__setShapeAttrs(shapeAttrs)
        return

    def copy(self, srcPath, destPath):
        """
        Copy page state of one location path to another.

        @type srcPath: C{str}
        @type destPath: C{str}
        @param srcPath: Source scene graph location path to copy from.
        @param destPath: Destination scene graph location path to copy to.
        """
        srcID = self.__id(srcPath)
        destID = self.__id(destPath)
        shapeAttrs = self.__getShapeAttrs()
        srcPageRegExp = re.compile('\\b%s\\b' % srcID)
        for stateType in ('expandedPages', 'collapsedPages'):
            shapeAttrForState = shapeAttrs.get(stateType)
            if shapeAttrForState is None:
                continue
            newPages = []
            shapeAttrForState = shapeAttrForState.rstrip(' |')
            pages = shapeAttrForState.split(' | ')
            for page in pages:
                if srcPageRegExp.search(page) is not None:
                    newPages.append(srcPageRegExp.sub(destID, page))

            if newPages:
                shapeAttrs[stateType] = (' | ').join(pages) + ' | ' + (' | ').join(newPages) + ' | '

        self.__setShapeAttrs(shapeAttrs)
        return

    def __id(self, path):
        """
        Get the page state ID of given scene graph location path.

        @type path: C{str}
        @rtype: C{str}
        @param path: Scene graph location path to construct page ID for.
        @return: Page state ID for given location path.
        """
        return (' > ').join(path.lstrip('/').split('/'))

    def __getShapeAttrs(self):
        """
        Get shape attrs of wrapped NetworkMaterialCreate node.

        @rtype: C{dict}
        @return: NetworkMaterialCreate shape attrs.
        """
        return NodegraphAPI.GetNodeShapeAttrs(self.__nmc)

    def __setShapeAttrs(self, shapeAttrs):
        """
        Set the shape attrs of the wrapped NetworkMaterialCreate node.

        @type shapeAttrs: C{dict}
        @param shapeAttrs: Shape attrs to set.
        """
        NodegraphAPI.SetNodeShapeNodeAttrs(self.__nmc, shapeAttrs)
        Utils.EventModule.QueueEvent('node_setShapeAttributes', hash(self.__nmc), node=self.__nmc)