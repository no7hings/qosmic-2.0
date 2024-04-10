# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Nov 16 2020, 22:23:17) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: SuperTools/NetworkMaterials/v1/SceneGraphLocationListener.py
# Compiled at: 2021-06-28 21:25:19
"""
Classes watching for scene graph attribute changes
"""
from UI4.Util.ClientManager import ClientManager
from Katana import Utils

class SceneGraphLocationListener(object):
    """
    Listener for NetworkMaterial scene graph location attribute changes.

    Watches parameters used to construct a NetworkMaterial's scene graph
    location and in turn watches for attribute changes on the scene graph
    location and it's ancestors, triggering a given event whenever a change
    is detected.
    """

    def __init__(self, paramNode, viewNode, eventType, eventID):
        """
        Initializes an instance of this class.

        @type paramNode: C{NodegraphAPI.Node}
        @type viewNode: C{NodegraphAPI.Node}
        @type eventType: C{str}
        @type eventID: C{object}
        @param paramNode: NetworkMaterial node.
        @param viewNode: Node to cook at.
        @param eventType: Event type to dispatch when attributes change.
        @param eventID: Event ID to dispatch along with event.
        """
        self.__paramNode = paramNode
        self.__paramNodeParent = paramNode.getParent()
        self.__eventType = eventType
        self.__eventID = eventID
        self._sceneGraphLocation = None
        self.__attrHashes = {}
        self.__isActivated = False
        self.__key = str(id(self))
        self.__manager = ClientManager()
        self.__manager.setViewNode(viewNode)
        self.__manager.createClient(self.__key)
        self.__manager.setAddOrUpdateLocationCallback(self.__onLocationUpdate)
        self.__manager.setDeleteLocationCallback(self.__onLocationUpdate)
        return

    def registerEventHandlers(self):
        """
        Start watching for attribute and parameter changes.
        """
        if self._sceneGraphLocation is None:
            self.__updateSceneGraphLocation()
        self.__manager.thaw()
        Utils.EventModule.RegisterEventHandler(self.__onParameterFinalizeValue, eventType='parameter_finalizeValue', eventID=hash(self.__paramNode))
        Utils.EventModule.RegisterEventHandler(self.__onParentParameterFinalizeValue, eventType='parameter_finalizeValue', eventID=hash(self.__paramNodeParent))
        return

    def unregisterEventHandlers(self):
        """
        Stop watching for attribute and parameter changes.
        """
        self.__manager.freeze()
        Utils.EventModule.UnregisterEventHandler(self.__onParameterFinalizeValue, eventType='parameter_finalizeValue', eventID=hash(self.__paramNode))
        Utils.EventModule.UnregisterEventHandler(self.__onParentParameterFinalizeValue, eventType='parameter_finalizeValue', eventID=hash(self.__paramNodeParent))

    def __onParameterFinalizeValue(self, eventID, eventType, param=None, **kwargs):
        """
        Event handler for C{'parameter_finalizeValue'}.

        Update watched scene graph location when a parameter is updated on the
        NetworkMaterial that changes the location written to by the
        NetworkMaterial.

        @type eventID: C{object}
        @type eventType: C{str}
        @type param: C{NodegraphAPI.Parameter}
        @type kwargs: C{dict}
        @param eventID: Ignored.
        @param eventType: Ignored.
        @param param: Updated parameter.
        @param kwargs: Ignored.
        """
        if param.getName() in ('sceneGraphLocation', 'name', 'namespace'):
            self.__updateSceneGraphLocation()

    def __onParentParameterFinalizeValue(self, eventID, eventType, param=None, **kwargs):
        """
        Event handler for C{'parameter_finalizeValue'}.

        Update watched scene graph location when a parameter is updated on the
        parent of the NetworkMaterial (NetworkMaterialCreate or
        NetworkMaterialEdit) that changes the location written to by the
        NetworkMaterial.

        @type eventID: C{object}
        @type eventType: C{str}
        @type param: C{NodegraphAPI.Parameter}
        @type kwargs: C{dict}
        @param eventID: Ignored.
        @param eventType: Ignored.
        @param param: Updated parameter.
        @param kwargs: Ignored.
        """
        if param.getName() == 'rootLocation':
            self.__updateSceneGraphLocation()

    def __updateSceneGraphLocation(self):
        """
        Update watched scene graph location to the value of NetworkMaterial
        node's C{getScenegraphLocation()}.
        """
        self.__isActivated = False
        if self._sceneGraphLocation is not None:
            self.__manager.deactivateSceneGraphLocation(self._sceneGraphLocation, self.__key)
        self._sceneGraphLocation = self.__paramNode.getScenegraphLocation()
        if self._sceneGraphLocation is not None:
            self.__manager.activateSceneGraphLocation(self._sceneGraphLocation, self.__key)
        return

    def __onLocationUpdate(self, locationEvent, key):
        """
        Callback for internal L{ClientManager} on scene graph location update.

        Do nothing if attributes haven't changed or if L{ClientManager} is
        still initializing.

        @type locationEvent: C{PyFnGeolib.LocationEvent}
        @type key: C{str}
        @param locationEvent: C{LocationEvent} providing updated attributes.
        @param key: Ignored.
        """
        location = locationEvent.getLocationPath()
        newAttrsHash = locationEvent.getLocationData().getAttrsHash()
        prevAttrHash = self.__attrHashes.get(location)
        if newAttrsHash == prevAttrHash:
            return
        self.__attrHashes[location] = newAttrsHash
        if location == self._sceneGraphLocation and not self.__isActivated:
            self.__isActivated = True
            return
        if not self.__isActivated:
            return
        self._onLocationAttrsChanged(locationEvent)

    def _onLocationAttrsChanged(self, locationEvent):
        """
        Callback for when attributes have changed.

        Dispatch event.

        @type locationEvent: C{PyFnGeolib.LocationEvent}
        @param locationEvent: Ignored.
        """
        Utils.EventModule.QueueEvent(self.__eventType, self.__eventID)


class LeafSceneGraphLocationListener(SceneGraphLocationListener):
    """
    Listener for NetworkMaterial scene graph location attribute changes.

    Watches parameters used to construct a NetworkMaterial's scene graph
    location and in turn watches for attribute changes on the scene graph
    location, triggering a given event whenever a change is detected.
    """

    def _onLocationAttrsChanged(self, locationEvent):
        """
        Callback for when attributes have changed.

        Override base class to ignore parent scene graph location paths.

        @type locationEvent: C{PyFnGeolib.LocationEvent}
        @param locationEvent: C{LocationEvent} containing scene graph location
            path to check.
        """
        if not locationEvent.getLocationPath() == self._sceneGraphLocation:
            return
        SceneGraphLocationListener._onLocationAttrsChanged(self, locationEvent)