# coding:utf-8
import enum
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class ScriptJobEventTypes(enum.EnumMeta):
    # dbTraceChanged
    # resourceLimitStateChange
    # linearUnitChanged
    # timeUnitChanged
    # angularUnitChanged
    # Undo
    # undoSupressed
    # Redo
    # customEvaluatorChanged
    # serialExecutorFallback
    # timeChanged
    # currentContainerChange
    # quitApplication
    # idleHigh
    # idle
    # idleVeryLow
    # RecentCommandChanged
    # ToolChanged
    # PostToolChanged
    # ToolDirtyChanged
    # ToolSettingsChanged
    # DisplayRGBColorChanged
    # animLayerRebuild
    # animLayerRefresh
    # animLayerAnimationChanged
    # animLayerLockChanged
    # animLayerBaseLockChanged
    # animLayerGhostChanged
    # cteEventKeyingTargetForClipChanged
    # cteEventKeyingTargetForLayerChanged
    # cteEventKeyingTargetForInvalidChanged
    # teClipAdded
    # teClipModified
    # teClipRemoved
    # teCompositionAdded
    # teCompositionRemoved
    # teCompositionActiveChanged
    # teCompositionNameChanged
    # teMuteChanged
    # cameraChange
    # cameraDisplayAttributesChange
    # SelectionChanged
    # PreSelectionChangedTriggered
    # LiveListChanged
    # ActiveViewChanged
    # SelectModeChanged
    # SelectTypeChanged
    # SelectPreferenceChanged
    # DisplayPreferenceChanged
    # DagObjectCreated
    # transformLockChange
    # renderLayerManagerChange
    # renderLayerChange
    # displayLayerManagerChange
    # displayLayerAdded
    # displayLayerDeleted
    # displayLayerVisibilityChanged
    # displayLayerChange
    # renderPassChange
    # renderPassSetChange
    # renderPassSetMembershipChange
    # passContributionMapChange
    # DisplayColorChanged
    # lightLinkingChanged
    # lightLinkingChangedNonSG
    # UvTileProxyDirtyChangeTrigger
    # preferredRendererChanged
    # polyTopoSymmetryValidChanged
    # SceneSegmentChanged
    # PostSceneSegmentChanged
    # SequencerActiveShotChanged
    # ColorIndexChanged
    # deleteAll
    # NameChanged
    # symmetricModellingOptionsChanged
    # softSelectOptionsChanged
    # SetModified
    # xformConstraintOptionsChanged
    # metadataVisualStatusChanged
    # undoXformCmd
    # redoXformCmd
    # freezeOptionsChanged
    # linearToleranceChanged
    # angularToleranceChanged
    # nurbsToPolygonsPrefsChanged
    # nurbsCurveRebuildPrefsChanged
    # constructionHistoryChanged
    # threadCountChanged
    # SceneSaved
    # NewSceneOpened
    # SceneOpened
    # SceneImported
    # PreFileNewOrOpened
    # PreFileNew
    # PreFileOpened
    # PostSceneRead
    # renderSetupAutoSave
    # workspaceChanged
    # PolyUVSetChanged
    # PolyUVSetDeleted
    # selectionConstraintsChanged
    # nurbsToSubdivPrefsChanged
    # startColorPerVertexTool
    # stopColorPerVertexTool
    # start3dPaintTool
    # stop3dPaintTool
    # DragRelease
    # ModelPanelSetFocus
    # modelEditorChanged
    # MenuModeChanged
    # gridDisplayChanged
    # interactionStyleChanged
    # axisAtOriginChanged
    # CurveRGBColorChanged
    # SelectPriorityChanged
    # snapModeChanged
    # texWindowEditorImageBaseColorChanged
    # texWindowEditorCheckerDensityChanged
    # texWindowEditorCheckerDisplayChanged
    # texWindowEditorDisplaySolidMapChanged
    # texWindowEditorShowup
    # texWindowEditorClose
    # profilerSelectionChanged
    # activeHandleChanged
    # ChannelBoxLabelSelected
    # colorMgtOCIORulesEnabledChanged
    # colorMgtUserPrefsChanged
    # RenderSetupSelectionChanged
    # colorMgtEnabledChanged
    # colorMgtConfigFileEnableChanged
    # colorMgtConfigFilePathChanged
    # colorMgtConfigChanged
    # colorMgtWorkingSpaceChanged
    # colorMgtPrefsViewTransformChanged
    # colorMgtPrefsReloaded
    # colorMgtOutputChanged
    # colorMgtPlayblastOutputChanged
    # colorMgtRefreshed
    # selectionPipelineChanged
    # currentSoundNodeChanged
    # graphEditorChanged
    # graphEditorParamCurveSelected
    # graphEditorOutlinerHighlightChanged
    # graphEditorOutlinerListChanged
    # glFrameTrigger
    # EditModeChanged
    # playbackRangeAboutToChange
    # playbackSpeedChanged
    # playbackModeChanged
    # playbackRangeSliderChanged
    # playbackByChanged
    # playbackRangeChanged
    # RenderViewCameraChanged
    # texScaleContextOptionsChanged
    # texRotateContextOptionsChanged
    # texMoveContextOptionsChanged
    # polyCutUVSteadyStrokeChanged
    # polyCutUVEventTexEditorCheckerDisplayChanged
    # polyCutUVShowTextureBordersChanged
    # polyCutUVShowUVShellColoringChanged
    # shapeEditorTreeviewSelectionChanged
    # poseEditorTreeviewSelectionChanged
    # sculptMeshCacheBlendShapeListChanged
    # sculptMeshCacheCloneSourceChanged
    # RebuildUIValues
    # cacheDestroyed
    # cachingPreferencesChanged
    # cachingSafeModeChanged
    # cachingEvaluationModeChanged
    # teTrackAdded
    # teTrackRemoved
    # teTrackNameChanged
    # teTrackModified
    # cteEventClipEditModeChanged
    # teEditorPrefsChanged

    SelectionChanged = 'SelectionChanged'
    FrameChanged = 'timeChanged'
    FrameRangeChanged = 'playbackRangeChanged'

    SceneOpened = 'SceneOpened'
    SceneNew = 'NewSceneOpened'

    CameraChanged = ''


class ScriptJob(object):
    EventTypes = ScriptJobEventTypes

    def __init__(self, name):
        self._window_name = '{}_script_job_window'.format(name)
        self.destroy()

    def register(self, method, event_type):
        if not cmds.window(self._window_name, exists=1):
            cmds.window(self._window_name, title='script gob window', sizeable=1, resizeToFitChildren=1)

        if isinstance(method, list):
            for i_method in method:
                cmds.scriptJob(parent=self._window_name, event=[event_type, i_method])
        else:
            cmds.scriptJob(parent=self._window_name, event=[event_type, method])

    def destroy(self):
        # noinspection PyUnresolvedReferences
        import maya.cmds as cmds

        if cmds.window(self._window_name, exists=1):
            cmds.deleteUI(self._window_name)
