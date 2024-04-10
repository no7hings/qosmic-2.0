# coding:utf-8
import fnmatch

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core
# maya
from .wrap import *


class MyaUtil(object):
    OBJ_PATHSEP = '|'
    PORT_PATHSEP = '.'
    NAMESPACE_PATHSEP = ':'

    @classmethod
    def get_all_group_paths(cls):
        return [
            i
            for i in cmds.ls(exactType='transform', long=1) or []
            if i and cmds.listRelatives(i, children=1, shapes=1, noIntermediate=0) is None
        ]

    @classmethod
    def get_all_shape_paths(cls):
        return [
            i
            for i in cmds.ls(shapes=1, long=1, noIntermediate=1) or []
            if i and cmds.listRelatives(i, children=1, shapes=1, noIntermediate=0) is None
        ]

    @classmethod
    def get_all_namespace_paths(cls):
        list_ = []
        except_list = ['UI', 'shared']
        _ = cmds.namespaceInfo(recurse=1, listOnlyNamespaces=1, fullName=1)
        if _:
            _.reverse()
            for namespace in _:
                if namespace not in except_list:
                    list_.append(namespace)
        return list_

    @classmethod
    def get_all_naming_overlapped_paths(cls, reference=True):
        _ = [x for x in cmds.ls() if '|' in x]
        if reference is True:
            return _
        return [i for i in _ if not cmds.referenceQuery(i, isNodeReferenced=1)]

    @classmethod
    def get_name_with_namespace_clear(cls, name):
        return bsc_core.PthNodeMtd.get_dag_name_with_namespace_clear(
            name, cls.NAMESPACE_PATHSEP
        )

    @classmethod
    def get_path_with_namespace_clear(cls, path):
        return bsc_core.PthNodeMtd.get_dag_path_with_namespace_clear(
            path, cls.OBJ_PATHSEP, cls.NAMESPACE_PATHSEP
        )

    @staticmethod
    def get_is_ui_mode():
        return not cmds.about(batch=1)

    @staticmethod
    def set_stack_trace_enable(boolean=False):
        cmds.stackTrace(state=boolean)

    @staticmethod
    def get_shape_path(path):
        if cmds.objExists(path):
            if cmds.nodeType(path) == 'transform':
                shape_paths = cmds.listRelatives(path, children=1, shapes=1, noIntermediate=1, fullPath=1)
                if shape_paths:
                    return shape_paths[0]
            return path

    @classmethod
    def get_selected_paths(cls, shape=0):
        list_ = []
        data = cmds.ls(selection=1, long=1)
        if data:
            if shape:
                list_ = [cls.get_shape_path(i) for i in data]
            else:
                list_ = data
        return list_

    @staticmethod
    def move_node(path, x, y, z):
        cmds.move(x, y, z, path, relative=1)

    @classmethod
    def move_selected_nodes_to_origin(cls, mode=0):
        paths = cmds.ls(selection=1, long=1)
        if paths:
            bbox = cmds.polyEvaluate(paths, boundingBox=1)
            (x, _x), (y, _y), (z, _z) = bbox
            cx = (x+_x)/2
            cy = (y+_y)/2
            cz = (z+_z)/2
            for i in paths:
                if mode == 0:
                    cls.move_node(i, -cx, -cy, -cz)
                elif mode == 1:
                    cls.move_node(i, -cx, -y, -cz)


class MyaNodeUtil(object):
    @classmethod
    def get_all_history_paths(cls, path):
        types_exclude = ['shadingEngine', 'groupId', 'set']
        list_ = []
        for i in cmds.listHistory(path, pruneDagObjects=1) or []:
            if cmds.nodeType(i) not in types_exclude:
                list_.append(i)
        return list_


class MyaNodeReference(object):
    @classmethod
    def get(cls, node_type):
        dic = {}
        PORT_PATHSEP = MyaUtil.PORT_PATHSEP
        directory_paths = cmds.filePathEditor(query=True, listDirectories='') or []
        for directory_path in directory_paths:
            raw = cmds.filePathEditor(query=True, listFiles=directory_path, withAttribute=True, byType=node_type) or []
            for i in range(len(raw)/2):
                file_name = raw[i*2]
                attribute_path = raw[i*2+1]
                _ = attribute_path.split(PORT_PATHSEP)
                file_path = '{}/{}'.format(directory_path, file_name)
                node_path = cmds.ls(_[0], long=1)[0]
                port_path = PORT_PATHSEP.join(_[1:])
                dic.setdefault(node_path, []).append((port_path, file_path))
        return dic


class MyaScriptJob(object):
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
    @classmethod
    def get_all(cls):
        return cmds.scriptJob(listJobs=1) or []

    @classmethod
    def do_delete(cls, pattern):
        _ = fnmatch.filter(cls.get_all(), pattern)
        if _:
            for i in _:
                index = i.split(': ')[0]
                cmds.scriptJob(kill=int(index), force=1)
                bsc_log.Log.trace_method_result(
                    'job-script kill',
                    'job-script="{}"'.format(i.lstrip().rstrip())
                )


class MyaModifier(object):
    @staticmethod
    def undo_run(fnc):
        def sub_fnc_(*args, **kwargs):
            cmds.undoInfo(openChunk=1, undoName=fnc.__name__)
            # noinspection PyBroadException
            try:
                _method = fnc(*args, **kwargs)
                return _method
            except Exception:
                bsc_core.ExceptionMtd.set_print()
            #
            finally:
                cmds.undoInfo(closeChunk=1, undoName=fnc.__name__)

        return sub_fnc_

    @staticmethod
    def undo_debug_run(fnc):
        def sub_fnc_(*args, **kwargs):
            cmds.undoInfo(openChunk=1, undoName=fnc.__name__)
            # noinspection PyBroadException
            try:
                _method = fnc(*args, **kwargs)
                return _method
            except Exception:
                bsc_log.LogException.trace()
                raise
            #
            finally:
                cmds.undoInfo(closeChunk=1, undoName=fnc.__name__)

        return sub_fnc_

    @staticmethod
    def set_undo_mark_mdf(method):
        def sub_method(*args, **kwargs):
            cmds.undoInfo(openChunk=1, undoName=method.__name__)
            # noinspection PyBroadException
            try:
                _method = method(*args, **kwargs)
                return _method
            except Exception:
                bsc_log.LogException.trace()
                raise
            #
            finally:
                cmds.undoInfo(closeChunk=1, undoName=method.__name__)

        return sub_method


class CallbackOpt(object):
    def __init__(self, function, callback_type):
        self._function = function
        self._callback_type = callback_type

    def register(self):
        _index = cmds.scriptJob(
            parent='modelPanel4', event=[self._callback_type, self._function]
        )
        bsc_log.Log.trace_method_result(
            'callback',
            'add as "{}" at "{}"'.format(self._callback_type, _index)
        )

    def deregister(self):
        pass
