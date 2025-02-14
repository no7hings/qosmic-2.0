# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Nov 16 2020, 22:23:17) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: SuperTools/NetworkMaterials/v1/NetworkMaterialEditUtil.py
# Compiled at: 2021-06-28 21:25:19
"""
Module containing utility classes for NetworkMaterialEdit.
"""
import collections, itertools, NodegraphAPI, PyFnScenegraphAttr
from Katana import FnAttribute

class OpArgPaths(object):
    """
    Top-level paths in NetworkMaterialEdit op args.
    """
    LayoutAdded = 'layout.added'
    LayoutReplaced = 'layout.replaced'
    LayoutDeleted = 'layout.deleted'
    LayoutConnectionsInserted = 'layout.connectionsInserted'
    LayoutConnectionsRemoved = 'layout.connectionsRemoved'


class LayoutNodesSorter(object):
    """
    Factory to construct an ordered list of node names from a material layout.

    Creates a list of node names in the order that they must be created so that
    parent-child relationships are possible.

    Uses list operations rather than sets to preserve as much of the original
    ordering as possible.
    """

    def __init__(self, layoutAttr):
        """
        Initializes an instance of this class.

        @type layoutAttr: C{FnAttribute.GroupAttribute}
        @param layoutAttr: C{material.B{layout}} attribute.
        """
        self.__layoutAttr = layoutAttr
        self.__orderedNodeNames = None
        return

    def build(self):
        """
        Build and return a list of node names in construction order.

        @rtype: C{list} of C{str}
        @return: Ordered list of node names.
        """
        population = [ self.__layoutAttr.getChildName(i) for i in xrange(self.__layoutAttr.getNumberOfChildren())
                     ]
        ancestors = [ name for name in population if not self.__isChild(population, name)
                    ]
        descendents = [ name for name in population if name not in ancestors ]
        self.__orderedNodeNames = ancestors[:]
        self.__appendLayoutDescendents(ancestors, descendents)
        return self.__orderedNodeNames

    def __appendLayoutDescendents(self, ancestors, descendents):
        """
        Recurse through descendent attributes, appending to internal list.

        @type ancestors: C{list} of C{str}
        @type descendents: C{list} of C{str}
        @param ancestors: List of attributes representing parent nodes.
        @param descendents: List of attributes representing descendent nodes.
        """
        children = [ name for name in descendents if self.__isChild(ancestors, name) ]
        grandchildren = [ name for name in descendents if name not in children ]
        self.__orderedNodeNames.extend(children)
        if grandchildren:
            self.__appendLayoutDescendents(children, grandchildren)

    def __isChild(self, ancestors, nodeName):
        """
        Check if given node has a parent in list of given ancestors.

        @type ancestors: C{list} of C{str}
        @type nodeName: C{str}
        @rtype: C{bool}
        @param ancestors: List of node name where one of them is potentially
            the parent node of C{nodeName}.
        @param nodeName: Node name to check.
        @return: C{None} C{nodeName} has no B{parent} attribute in the
            C{material.B{layout}} attributes, C{True} if any node in
            C{ancestors} is a direct parent of C{nodeName}, C{False} otherwise.
        """
        parent = self.__layoutAttr.getChildByName(('.').join((nodeName, 'parent')))
        return parent and parent.getValue() in ancestors


class LayoutNodesSearcher(object):
    """
    Utility class to search through layout attrs.
    """

    def __init__(self, layoutAttrs):
        """
        Initializes an instance of this class.

        @type layoutAttrs: C{FnAttribute.GroupAttribute}
        @param layoutAttrs: C{material.B{layout}} attributes.
        """
        self.__layoutAttrs = layoutAttrs

    def getDisconnectedNodeNames(self, checkNodeNames):
        """
        Get nodes in given iterable that have no connections to/from them.

        @type checkNodeNames: C{set} of C{str}
        @rtype: C{set} of C{str}
        @param checkNodeNames: Iterable of node names to check.
        @return: Iet of node names
        """
        disconnectedInputNodeNames = {nodeName for nodeName in checkNodeNames if self.__layoutAttrs.getChildByName('%s.connections' % nodeName) is None}
        connectedOutputNodeNames = self.__connectedNodeNames()
        disconnectedInputNodeNames.difference_update(connectedOutputNodeNames)
        return disconnectedInputNodeNames

    def __connectedNodeNames(self):
        """
        Find nodes where the C{material.B{layout}} attributes indicate they
        have at least one output port connected.

        @rtype: C{set} of C{str}
        @return: Set of node names that have at least one output port
            connected.
        """
        nodeNames = set()
        for nodeIdx in xrange(self.__layoutAttrs.getNumberOfChildren()):
            nodeAttr = self.__layoutAttrs.getChildByIndex(nodeIdx)
            parentName = nodeAttr.getChildByName('parent').getValue()
            for connectionsAttrName in ('connections', 'nodeSpecificAttributes.returnConnections'):
                connectionsAttr = nodeAttr.getChildByName(connectionsAttrName)
                if connectionsAttr is None:
                    continue
                for connectionStr in connectionsAttr.getData():
                    upstreamNodeName = connectionStr.split('@')[(-1)]
                    if upstreamNodeName == parentName:
                        continue
                    nodeNames.add(upstreamNodeName)

        return nodeNames


class OpArgNodeReferenceSearcher(object):
    """
    Utility to find NetworkMaterialEdit op arg paths referencing given nodes.

    Checks root arg paths as well as parsing connection args.
    """

    def __init__(self, opArgs, nodeNames):
        """
        Initializes an instance of this class.

        @type opArgs: C{FnAttribute.GroupAttribute}
        @type nodeNames: C{list} of C{str}
        @param opArgs: NetworkMaterialEdit op args.
        @param nodeNames: List of node names to query op args for.
        """
        self.__opArgs = opArgs
        self.__nodeNames = nodeNames

    def deleteFromGroupAttr(self, gb, nodeReferencesByArgPath=None):
        """
        Delete found paths in given C{GroupBuilder}.

        @type gb: C{FnAttribute.GroupBuilder}
        @type nodeReferencesByArgPath: C{dict} or C{None}
        @param nodeReferencesByArgPath: Arg paths and values at that path to
            remove.
        @param gb: C{GroupBuilder} to delete elements from.
        """
        if nodeReferencesByArgPath is None:
            nodeReferencesByArgPath = self.getReferencesByArgPath()
        for argPath, blackList in nodeReferencesByArgPath.iteritems():
            if blackList is None:
                gb.delete(argPath)
            else:
                currList = self.__opArgs.getChildByName(argPath).getData()
                newList = [ val for val in currList if val not in blackList ]
                if not newList:
                    gb.delete(argPath)
                else:
                    gb.set(argPath, FnAttribute.StringAttribute(newList))

        return

    def getReferencesByArgPath(self):
        """
        Get the arg paths that reference given node names.

        @rtype: C{dict}
        @return: Dictionary mapping arg paths to either
            (a) C{None} if the arg path itself references a node; or
            (b) a list of values at that arg path that reference a node (i.e.
            C{StringAttribute} elements).
        """
        referencesByArgPath = collections.defaultdict(list)
        for _nodeName, argPath, value in self.__all():
            if value is None:
                referencesByArgPath[argPath] = None
            else:
                referencesByArgPath[argPath].append(value)

        return referencesByArgPath

    def updateConnectionNodeName(self, gb, oldName, newName):
        """
        Updates node name references in NME op args for C{material.B{nodes}}
        connections.

        Required following a C{'node_setName'} event.

        @type gb: C{FnAttribute.GroupBuilder}
        @type oldName: C{str}
        @type newName: C{str}
        @param gb: C{GroupBuilder} storing op arg updates.
        @param oldName: Previous node name.
        @param newName: New node name.
        """
        for sourceOldName, argPath, _value in self.__nodesConnected():
            outputArgPath = '%s.%s' % (argPath, 'output')
            attr = self.__opArgs.getChildByName(outputArgPath)
            if not attr or oldName != sourceOldName:
                continue
            gb.set('%s.name' % outputArgPath, FnAttribute.StringAttribute(newName))
            gb.set('%s.srcName' % outputArgPath, FnAttribute.StringAttribute(newName))
            gb.set('%s.port' % outputArgPath, attr.getChildByName('port'))

    def getAddedNodeNames(self):
        """
        Get a set of all the matching nodes that were created by the op.

        @rtype: C{set} of C{str}
        @return: Names of nodes created by the op.
        """
        return {nodeName for nodeName, argPath, _ in self.__layoutAdded() if self.__opArgs.getChildByName(('.').join((argPath, 'parent')))}

    def getConnectedNodeNames(self):
        """
        Get a set of all the matching nodes that have a connection added
        or removed to or from them by the op.

        @rtype: C{set} of C{str}
        @return: Names of nodes connected by the op.
        """
        return {nodeName for nodeName, _, _ in self.__layoutConnected()}

    def getParameterLocallySetNodeNames(self):
        """
        Get a set of all the matching nodes that have a parameter set as
        locally edited or forced default.

        @rtype: C{set} of C{str}
        @return: Names of nodes with locally set parameters.
        """
        nodeNames = set()
        for nodeName, argPath, _ in itertools.chain(self.__layoutReplaced(), self.__layoutAdded()):
            paramVars = self.__opArgs.getChildByName(('.').join((argPath, 'parameterVars')))
            if paramVars is None:
                continue
            for paramIdx in xrange(paramVars.getNumberOfChildren()):
                param = paramVars.getChildByIndex(paramIdx)
                enable = param.getChildByName('enable')
                if enable is None:
                    continue
                if enable.getValue() != 0:
                    nodeNames.add(nodeName)
                    break

        return nodeNames

    def getBypassedNodeNames(self):
        """
        Get a set of all matching nodes that have been (un)bypassed.

        @rtype: C{set} of C{str}
        @return: Names of nodes that have been (un)bypassed.
        """
        nodeNames = set()
        for nodeName, argPath, _ in self.__nodes():
            bypassedAttr = self.__opArgs.getChildByName(('.').join((argPath, 'isBypassed')))
            if bypassedAttr is not None:
                nodeNames.add(nodeName)

        return nodeNames

    def __all(self):
        """
        Generator over all op args referencing a relevant node.

        @rtype: C{collections.Iterable} of C{tuple} of C{str}, C{str},
            C{object}
        @return: An iteratable over all matching op args yielding node name,
            op arg path, and a data element at that path (if attribute is
            an array) or C{None}.
        """
        return itertools.chain(self.__layoutAdded(), self.__layoutReplaced(), self.__layoutDeleted(), self.__layoutConnected(), self.__nodes(), self.__nodesConnected())

    def __layoutAdded(self):
        """
        Generator over C{layout.B{added}} op args referencing a relevant node.

        @rtype: C{collections.Iterable} of C{tuple} of C{str}, C{str}, C{None}
        @return: An iteratable over all matching op args yielding node name,
            op arg path, and C{None}.
        """
        parentArgPath = ('.').join((OpArgPaths.LayoutAdded, 'layout'))
        for argPathRef in self.__argPathMatches(parentArgPath):
            yield argPathRef

    def __layoutReplaced(self):
        """
        Generator over C{layout.B{replaced}} op args referencing a relevant
        node.

        @rtype: C{collections.Iterable} of C{tuple} of C{str}, C{str}, C{None}
        @return: An iteratable over all matching op args yielding node name,
            op arg path, and C{None}.
        """
        parentArgPath = ('.').join((OpArgPaths.LayoutReplaced, 'layout'))
        for argPathRef in self.__argPathMatches(parentArgPath):
            yield argPathRef

    def __layoutDeleted(self):
        """
        Generator over C{layout.B{deleted}} op args referencing a relevant
        node.

        @rtype: C{collections.Iterable} of C{tuple} of C{str}, C{str}, C{None}
        @return: An iteratable over all matching op args yielding node name,
            op arg path, and C{None}.
        """
        parentArgPath = ('.').join((OpArgPaths.LayoutDeleted, 'layout'))
        for argPathRef in self.__argPathMatches(parentArgPath):
            yield argPathRef

    def __layoutConnected(self):
        """
        Generator over
        * C{layout.B{connectionsInserted}}
        * C{layout.B{connectionsRemoved}}
        * C{layout.connectionsInserted.layout.*.B{connections}}
        * C{layout.connectionsRemoved.layout.*.B{connections}}
        * C{layout.connectionsInserted.layout.*.nodeSpecificAttributes.
            B{returnConnections}}
        * C{layout.connectionsRemoved.layout.*.nodeSpecificAttributes.
            B{returnConnections}}
        op args referencing a relevant node.

        @rtype: C{collections.Iterable} of C{tuple} of C{str}, C{str},
            C{object}
        @return: An iteratable over all matching op args yielding node name,
            op arg path, and C{None} for input connections or a C{str}
            containing the connection string where the node name was found for
            an output connection .
        """
        for parentArgPath in self.__layoutConnectionsArgPaths:
            for argPathRef in self.__argPathMatches(parentArgPath):
                yield argPathRef

        for parentArgPath in self.__layoutConnectionsArgPaths:
            connectionsArg = self.__opArgs.getChildByName(parentArgPath)
            if connectionsArg is None:
                continue
            for nodeIdx in xrange(connectionsArg.getNumberOfChildren()):
                nodeAttr = connectionsArg.getChildByIndex(nodeIdx)
                inputNodeName = connectionsArg.getChildName(nodeIdx)
                for childPath in ('connections', 'nodeSpecificAttributes.returnConnections'):
                    argPath = ('.').join((
                     parentArgPath, inputNodeName, childPath))
                    matches = self.__findConnectionsInLayout(nodeAttr, childPath)
                    for outputNodeName, connectionStr in matches:
                        yield (
                         outputNodeName, argPath, connectionStr)

        return

    def __nodes(self):
        """
        Generator over C{B{nodes}} op args referencing a relevant node.

        @rtype: C{collections.Iterable} of C{tuple} of C{str}, C{str}, C{None}
        @return: An iteratable over all matching op args yielding node name,
            op arg path, and C{None}.
        """
        parentArgPath = 'nodes'
        for argPathRef in self.__argPathMatches(parentArgPath):
            yield argPathRef

    def __argPathMatches(self, parentArgPath):
        """
        Generator over child op args at given path that correspond to a
        relevant node.

        @rtype: C{collections.Iterable} of C{tuple} of C{str}, C{str}, C{None}
        @type parentArgPath: C{str}
        @param parentArgPath: Op arg path search.
        @return: An iteratable over all matching op args yielding node name,
            op arg path, and C{None}.
        """
        for nodeName in self.__nodeNames:
            argPath = ('.').join((parentArgPath, nodeName))
            if self.__opArgs.getChildByName(argPath):
                yield (
                 nodeName, argPath, None)

        return

    def __nodesConnected(self):
        """
        Generator over C{nodes.*.B{connections}} and C{B{terminals}} op args
        referencing a relevant node.

        @rtype: C{collections.Iterable} of C{tuple} of C{str}, C{str}, C{None}
        @return: An iteratable over all matching op args yielding node name,
            op arg path, and C{None}.
        """
        nodesArg = self.__opArgs.getChildByName('nodes')
        if nodesArg is not None:
            for nodeIdx in xrange(nodesArg.getNumberOfChildren()):
                nodeAttr = nodesArg.getChildByIndex(nodeIdx)
                nodeConnectionsArg = nodeAttr.getChildByName('connections.new')
                connectedPortsNames = self.__findConnectionsInPortArgs(nodeConnectionsArg)
                for outputNodeName, inputPortName in connectedPortsNames:
                    inputNodeName = nodesArg.getChildName(nodeIdx)
                    argPath = ('.').join((
                     'nodes', inputNodeName, 'connections.new',
                     inputPortName))
                    yield (outputNodeName, argPath, None)

        terminalsArg = self.__opArgs.getChildByName('terminals.new')
        connectedPortsNames = self.__findConnectionsInPortArgs(terminalsArg)
        for outputNodeName, inputPortName in connectedPortsNames:
            argPath = ('.').join(('terminals.new', inputPortName))
            yield (outputNodeName, argPath, None)

        return

    __layoutConnectionsArgPaths = [ ('.').join((opArgPath, 'layout')) for opArgPath in (
     OpArgPaths.LayoutConnectionsInserted,
     OpArgPaths.LayoutConnectionsRemoved)
                                  ]

    def __findConnectionsInLayout(self, inputNodeAttr, connectionArgPath):
        """
        Generator over an attribute representing connections, yielding matching
        node name and connection string.

        @type inputNodeAttr: C{FnAttribute.GroupAttribute}
        @type connectionArgPath: C{str}
        @rtype: C{collections.Iterable} of C{tuple} of C{str}, C{str}
        @param inputNodeAttr: Op arg attribute to query.
        @param connectionArgPath: Path in C{inputNodeAttr} to a
            C{StringAttribute} containing a list of connection strings.
        @return: An iterable over C{StringAttribute} in C{inputNodeAttr}
            at C{connectionArgPath} yielding C{tuple}s of node name and
            connection string.
        """
        nodeConnectionsArg = inputNodeAttr.getChildByName(connectionArgPath)
        if nodeConnectionsArg is None:
            return
        else:
            connectionArgStrs = nodeConnectionsArg.getData()
            for connectionStr in connectionArgStrs:
                outputNodeName = connectionStr.rsplit('@', 1)[(-1)]
                if outputNodeName not in self.__nodeNames:
                    continue
                yield (
                 outputNodeName, connectionStr)

            return

    def __findConnectionsInPortArgs(self, nodeConnectionsArg):
        """
        Generator over a C{nodes.*.B{connections}} or B{terminals} op arg
        yielding node name and port name of connections referencing
        relevant nodes.

        @type nodeConnectionsArg: C{FnAttribute.GroupAttribute}
        @rtype: C{tuple} of C{str}, C{str}
        @param nodeConnectionsArg: Op arg attribute to query.
        @return: An iterable yielding C{tuple}s of output node name and input
            port name.
        """
        if nodeConnectionsArg is None:
            return
        else:
            for portIdx in xrange(nodeConnectionsArg.getNumberOfChildren()):
                portAttr = nodeConnectionsArg.getChildByIndex(portIdx)
                if portAttr is None:
                    continue
                outputNodeNameAttr = portAttr.getChildByName('output.srcName')
                outputNodeName = outputNodeNameAttr.getValue()
                if outputNodeName not in self.__nodeNames:
                    continue
                yield (
                 outputNodeName, nodeConnectionsArg.getChildName(portIdx))

            return


class LayoutParameterExtractor(object):
    """
    Utility class for setting node parameters from layout attributes.
    """

    def __init__(self, opArgs, layoutNodeNames):
        """
        Initializes an instance of this class.

        @type opArgs: C{FnAttribute.GroupAttribute}
        @type layoutNodeNames: C{list} of C{str}
        @param opArgs: NetworkMaterialEdit op args.
        @param layoutNodeNames: List of nodes to extract parameters for.
        """
        self.__layoutReplaced = opArgs.getChildByName('layout.replaced.layout')
        self.__addedNodeNames = OpArgNodeReferenceSearcher(opArgs, layoutNodeNames).getAddedNodeNames()
        self.__sparseNodes = {}

    def extractAndSetOnNode(self, node, nodeLayoutAttr, nodeLayoutName):
        """
        Extract parameters from layout attributes and set on given node.

        @type node: C{NodegraphAPI.Node}
        @type nodeLayoutAttr: C{PyFnScenegraphAttr.GroupAttr}
        @type nodeLayoutName: C{str}
        @param node: Node whose parameters to update.
        @param nodeLayoutAttr:  Layout attributes corresponding to node.
        @param nodeLayoutName: Name of node in layout attributes.
        """
        self.__extractNodePosition(node, nodeLayoutAttr, nodeLayoutName)
        self.__extractShaderType(node, nodeLayoutAttr, nodeLayoutName)
        self.__extractNodeName(node, nodeLayoutAttr, nodeLayoutName)
        self.__extractParameters(node, nodeLayoutAttr, nodeLayoutName)

    def getSparseNodes(self, attrPath=None):
        """
        Returns any sparsely populated nodes,
        optionally filtered by a given attribute name.
        """
        if attrPath:
            return self.__sparseNodes.get(attrPath, [])
        sparseNodes = set()
        for _attr, nodes in self.__sparseNodes.items():
            sparseNodes.update(nodes)

        return list(sparseNodes)

    def __logSparseNode(self, missingAttr, node):
        """
        Mark a node as having an expected attribute missing
        from its layout definition.
        """
        if missingAttr not in self.__sparseNodes:
            self.__sparseNodes[missingAttr] = []
        self.__sparseNodes[missingAttr].append(node)

    def __extractNodePosition(self, node, nodeLayoutAttr, _nodeLayoutName):
        """
        Extracts and sets the node position.
        """
        positionAttr = nodeLayoutAttr.getChildByName('position')
        if positionAttr:
            position = positionAttr.getData()
        else:
            position = (0, 0)
            self.__logSparseNode('position', node)
        NodegraphAPI.SetNodePosition(node, position)

    def __extractShaderType(self, node, nodeLayoutAttr, nodeLayoutName):
        """
        Set the B{nodeType} parameter on given node.

        Ensure the parameter is not editable on newly added nodes.

        @type node: C{NodegraphAPI.Node}
        @type nodeLayoutAttr: C{FnAttribute.GroupAttribute}
        @type nodeLayoutName: C{str}
        @param node: Node to update.
        @param nodeLayoutAttr: C{material.B{layout}} attribute corresponding to
            C{node}.
        @param nodeLayoutName: Node name as it appears in C{material.B{layout}}
            attribute.
        """
        shaderType = nodeLayoutAttr.getChildByName('nodeSpecificAttributes.shaderType')
        if shaderType is None:
            return
        else:
            nodeTypeParam = node.getParameter('nodeType')
            if nodeTypeParam is None:
                return
            nodeTypeParam.setValue(shaderType.getValue(), 0)
            node.checkDynamicParameters()
            if nodeLayoutName not in self.__addedNodeNames:
                nodeTypeParam.setHintString("{'readOnly': True}")
            return

    def __extractNodeName(self, node, nodeLayoutAttr, nodeLayoutName):
        """
        Set the B{name} parameter on given node.

        Ensure the parameter is not editable on newly added nodes.

        @type node: C{NodegraphAPI.Node}
        @type nodeLayoutAttr: C{FnAttribute.GroupAttribute}
        @type nodeLayoutName: C{str}
        @param node: Node to update.
        @param nodeLayoutAttr: C{material.B{layout}} attribute corresponding to
            C{node}.
        @param nodeLayoutName: Node name as it appears in C{material.B{layout}}
            attribute.
        """
        nameParam = node.getParameter('name')
        if nameParam is None:
            return
        else:
            nameParamValue = nodeLayoutAttr.getChildByName('nodeSpecificAttributes.name')
            if nameParamValue:
                nameParamValue = nameParamValue.getValue()
            if not nameParamValue:
                nameParamValue = nodeLayoutName
            if nodeLayoutName not in self.__addedNodeNames:
                node.setAutoRenameAllowed(False)
                node.setRenameAllowed(False)
                nameParam.setHintString("{'readOnly': True}")
            nameParam.setValue(nameParamValue, 0)
            return

    def __extractParameters(self, node, nodeLayoutAttr, nodeLayoutName):
        """
        Set node parameters from C{material.B{layout}} attributes.

        Prefer baked parameters (e.g. resulting from expressions) to raw
        values.

        Initialise B{enable} parameter flag to C{0} (inherited) if it's not yet
        been overridden in the NetworkMaterialEdit.

        @type node: C{NodegraphAPI.Node}
        @type nodeLayoutAttr: C{FnAttribute.GroupAttribute}
        @type nodeLayoutName: C{str}
        @param node: Node to update.
        @param nodeLayoutAttr: C{material.B{layout}} attribute corresponding to
            C{node}.
        @param nodeLayoutName: Node name as it appears in C{material.B{layout}}
            attribute.
        """
        parameterVars = nodeLayoutAttr.getChildByName('parameterVars')
        if not parameterVars:
            return
        else:
            for paramPathTuple in self.__leafs(tuple(), parameterVars):
                paramPath = ('.').join(paramPathTuple)
                parentParam = node.getParameter(('.').join(('parameters', paramPath)))
                if parentParam is None:
                    continue
                paramAttr = parameterVars.getChildByName(paramPath)
                enable = paramAttr.getChildByName('enable').getValue()
                valueAttr = paramAttr.getChildByName('value')
                bakedAttr = nodeLayoutAttr.getChildByName(('.').join(('parameters', paramPath)))
                hintsAttr = paramAttr.getChildByName('hints')
                if bakedAttr is not None:
                    valueAttr = bakedAttr
                isEnableEdited = nodeLayoutName in self.__addedNodeNames
                if not isEnableEdited and self.__layoutReplaced is not None:
                    isEnableEdited = self.__layoutReplaced.getChildByName(('.').join((
                     nodeLayoutName, 'parameterVars', paramPath, 'enable')))
                if not isEnableEdited and enable == 1:
                    enable = 0
                self.__set(parentParam.getChild('value'), paramAttr, valueAttr)
                parentParam.getChild('enable').setValue(enable, 0)
                if hintsAttr is not None:
                    hints = hintsAttr.getValue()
                    paramHints = parentParam.getChild('hints')
                    if paramHints is None:
                        parentParam.createChildString('hints', hints)
                    else:
                        paramHints.setValue(hints, 0)

            return

    @classmethod
    def __leafs(cls, pathTuple, parent):
        """
        Recursive generator over paths to child attributes corresponding to
        individual parameters.

        A leaf is signalled by the presence of a child B{enable} attribute.

        @type pathTuple: C{tuple} of C{str}
        @type parent: C{PyFnScenegraphAttr.GroupAttr}
        @rtype: C{collections.Iterable} of {tuple} of C{str}
        @param pathTuple: Path (as a C{tuple}) within C{parent} to yield or
            recurse down.
        @param parent: Attribute to start searching from.
        @return: Iterable of paths (as C{tuple}s) within C{parent}
            corresponding to an individual parameter.
        """
        if not isinstance(parent, PyFnScenegraphAttr.GroupAttr):
            return
        enableAttr = parent.getChildByName('enable')
        if enableAttr:
            yield pathTuple
        else:
            for childIdx in xrange(parent.getNumberOfChildren()):
                child = parent.getChildByIndex(childIdx)
                childName = parent.getChildName(childIdx)
                for childPath in cls.__leafs(pathTuple + (childName,), child):
                    yield childPath

    @staticmethod
    def __set(parentParam, paramAttr, valueAttr):
        """
        Set parameter from attribute representing it.

        Handles single values as well as array parameters.

        @type parentParam: C{NodegraphAPI.Parameter}
        @type paramAttr: C{PyFnScenegraphAttr.GroupAttr}
        @type valueAttr: C{PyFnScenegraphAttr.Attr}
        @param parentParam: An individual C{Parameter}, from the perspective of
            the UI.
        @param paramAttr: Attribute representing the parameter and it's
            metadata.
        @param valueAttr: Value to set on parameter.
        """
        isDynamicArrayAttr = paramAttr.getChildByName('isDynamicArray')
        isDynamicArray = isDynamicArrayAttr and isDynamicArrayAttr.getValue(0)
        numValues = valueAttr.getNumberOfValues()
        if numValues > 1 or isDynamicArray:
            valueTuple = valueAttr.getNearestSample(0)
            for valueIdx, value in enumerate(valueTuple):
                childParamName = 'i%s' % valueIdx
                childParam = parentParam.getChild(childParamName)
                if childParam is None:
                    if not isDynamicArray:
                        break
                    childParam = parentParam.insertArrayElement(valueIdx)
                childParam.setValue(value, 0)

        elif numValues == 1:
            parentParam.setValue(valueAttr.getValue(), 0)
        return