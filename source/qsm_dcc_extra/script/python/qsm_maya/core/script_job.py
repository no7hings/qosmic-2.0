# coding:utf-8
import enum
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class ScriptJobEventTypes(enum.EnumMeta):
    # ActiveViewChanged
    # ChannelBoxLabelSelected
    # ColorIndexChanged
    # CurveRGBColorChanged
    # DagObjectCreated
    # DisplayColorChanged
    # DisplayPreferenceChanged
    # DisplayRGBColorChanged
    # DragRelease
    # EditModeChanged
    # LiveListChanged
    # MenuModeChanged
    # ModelPanelSetFocus
    # NameChanged
    # NewSceneOpened
    # PolyUVSetChanged
    # PolyUVSetDeleted
    # PostSceneRead
    # PostSceneSegmentChanged
    # PostToolChanged
    # PreFileNew
    # PreFileNewOrOpened
    # PreFileOpened
    # PreSelectionChangedTriggered
    # RebuildUIValues
    # RecentCommandChanged
    # Redo
    # RenderSetupSelectionChanged
    # RenderViewCameraChanged
    # SceneImported
    # SceneOpened
    # SceneSaved
    # SceneSegmentChanged
    # SelectModeChanged
    # SelectPreferenceChanged
    # SelectPriorityChanged
    # SelectTypeChanged
    # SelectionChanged
    # SequencerActiveShotChanged
    # SetModified
    # SoundNodeAdded
    # SoundNodeRemoved
    # ToolChanged
    # ToolDirtyChanged
    # ToolSettingsChanged
    # Undo
    # UvTileProxyDirtyChangeTrigger
    # activeHandleChanged
    # angularToleranceChanged
    # angularUnitChanged
    # animLayerAnimationChanged
    # animLayerBaseLockChanged
    # animLayerGhostChanged
    # animLayerLockChanged
    # animLayerRebuild
    # animLayerRefresh
    # axisAtOriginChanged
    # cacheDestroyed
    # cachingEvaluationModeChanged
    # cachingPreferencesChanged
    # cachingSafeModeChanged
    # cameraChange
    # cameraDisplayAttributesChange
    # colorMgtConfigChanged
    # colorMgtConfigFileEnableChanged
    # colorMgtConfigFilePathChanged
    # colorMgtEnabledChanged
    # colorMgtOCIORulesEnabledChanged
    # colorMgtOutputChanged
    # colorMgtPlayblastOutputChanged
    # colorMgtPrefsReloaded
    # colorMgtPrefsViewTransformChanged
    # colorMgtRefreshed
    # colorMgtUserPrefsChanged
    # colorMgtWorkingSpaceChanged
    # constructionHistoryChanged
    # cteEventClipEditModeChanged
    # cteEventKeyingTargetForClipChanged
    # cteEventKeyingTargetForInvalidChanged
    # cteEventKeyingTargetForLayerChanged
    # currentContainerChange
    # currentSoundNodeChanged
    # customEvaluatorChanged
    # dbTraceChanged
    # deleteAll
    # displayLayerAdded
    # displayLayerChange
    # displayLayerDeleted
    # displayLayerManagerChange
    # displayLayerVisibilityChanged
    # freezeOptionsChanged
    # glFrameTrigger
    # graphEditorChanged
    # graphEditorOutlinerHighlightChanged
    # graphEditorOutlinerListChanged
    # graphEditorParamCurveSelected
    # gridDisplayChanged
    # idle
    # idleHigh
    # idleVeryLow
    # interactionStyleChanged
    # lightLinkingChanged
    # lightLinkingChangedNonSG
    # linearToleranceChanged
    # linearUnitChanged
    # metadataVisualStatusChanged
    # modelEditorChanged
    # nurbsCurveRebuildPrefsChanged
    # nurbsToPolygonsPrefsChanged
    # nurbsToSubdivPrefsChanged
    # passContributionMapChange
    # playbackByChanged
    # playbackModeChanged
    # playbackRangeAboutToChange
    # playbackRangeChanged
    # playbackRangeSliderChanged
    # playbackSpeedChanged
    # polyCutUVEventTexEditorCheckerDisplayChanged
    # polyCutUVShowTextureBordersChanged
    # polyCutUVShowUVShellColoringChanged
    # polyCutUVSteadyStrokeChanged
    # polyTopoSymmetryValidChanged
    # poseEditorTreeviewSelectionChanged
    # preferredRendererChanged
    # profilerSelectionChanged
    # quitApplication
    # redoXformCmd
    # renderLayerChange
    # renderLayerManagerChange
    # renderPassChange
    # renderPassSetChange
    # renderPassSetMembershipChange
    # renderSetupAutoSave
    # resourceLimitStateChange
    # sculptMeshCacheBlendShapeListChanged
    # sculptMeshCacheCloneSourceChanged
    # selectionConstraintsChanged
    # selectionPipelineChanged
    # serialExecutorFallback
    # shapeEditorTreeviewSelectionChanged
    # snapModeChanged
    # softSelectOptionsChanged
    # start3dPaintTool
    # startColorPerVertexTool
    # stop3dPaintTool
    # stopColorPerVertexTool
    # symmetricModellingOptionsChanged
    # tabletModeChanged
    # teClipAdded
    # teClipModified
    # teClipRemoved
    # teCompositionActiveChanged
    # teCompositionAdded
    # teCompositionNameChanged
    # teCompositionRemoved
    # teEditorPrefsChanged
    # teMuteChanged
    # teTrackAdded
    # teTrackModified
    # teTrackNameChanged
    # teTrackRemoved
    # texMoveContextOptionsChanged
    # texRotateContextOptionsChanged
    # texScaleContextOptionsChanged
    # texWindowEditorCheckerDensityChanged
    # texWindowEditorCheckerDisplayChanged
    # texWindowEditorClose
    # texWindowEditorDisplaySolidMapChanged
    # texWindowEditorImageBaseColorChanged
    # texWindowEditorShowup
    # threadCountChanged
    # timeChanged
    # timeUnitChanged
    # transformLockChange
    # undoSupressed
    # undoXformCmd
    # workspaceChanged
    # xformConstraintOptionsChanged

    SelectionChanged = 'SelectionChanged'

    FrameChanged = 'timeChanged'
    FrameRangeChanged = 'playbackRangeChanged'
    FPSChanged = 'timeUnitChanged'

    SceneOpened = 'SceneOpened'
    SceneNew = 'NewSceneOpened'
    SceneSaved = 'SceneSaved'

    Undo = 'Undo'
    Redo = 'Redo'

    CameraChanged = 'cameraChange'

    ViewPortChanged = 'ModelPanelSetFocus'
    Test = 'ActiveViewChanged'


class ScriptJobOpt(object):
    EventTypes = ScriptJobEventTypes

    def __init__(self, name):
        self._window_name = '{}_script_job_window'.format(name)
        self.destroy()

    def register(self, method, event_type):
        if not cmds.window(self._window_name, exists=1):
            cmds.window(self._window_name, title='Script Job Window', sizeable=1, resizeToFitChildren=1)

        if isinstance(method, list):
            for i_method in method:
                cmds.scriptJob(parent=self._window_name, event=[event_type, i_method])
        else:
            cmds.scriptJob(parent=self._window_name, event=[event_type, method])

    def register_as_attribute_change(self, method, atr_path):
        if not cmds.window(self._window_name, exists=1):
            cmds.window(self._window_name, title='Script Job Window', sizeable=1, resizeToFitChildren=1)

        if isinstance(method, list):
            for i_method in method:
                cmds.scriptJob(
                    parent=self._window_name,
                    # fixme: do not use "replacePrevious"
                    # replacePrevious=True,
                    attributeChange=[atr_path, i_method]
                )
        else:
            cmds.scriptJob(
                parent=self._window_name,
                # replacePrevious=True,
                attributeChange=[atr_path, method]
            )

    def destroy(self):
        # noinspection PyUnresolvedReferences
        import maya.cmds as cmds

        if cmds.window(self._window_name, exists=1):
            cmds.deleteUI(self._window_name)
