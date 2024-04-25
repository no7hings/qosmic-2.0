# coding:utf-8
import six

import os

import types

import lxbasic.resource as bsc_resource

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgeneral.dcc.objects as gnl_dcc_objects

import lxgeneral.dcc.abstracts as gnl_dcc_abstracts

import lxuniverse.core as unr_core

import lxuniverse.objects as unv_objects

import lxgui.core as gui_core
# maya
from ...core.wrap import *

from ... import core as mya_core
# maya dcc objects
from . import node as _mya_dcc_obj_node

from . import node_for_dag as _mya_dcc_obj_node_for_dag


class Namespace(
    gnl_dcc_abstracts.AbsDccBaseDef,
    gnl_dcc_abstracts.AbsGuiExtraDef,
):
    PATHSEP = ':'
    Obj_CLS = _mya_dcc_obj_node.Node

    # noinspection PyMissingConstructor
    def __init__(self, path):
        self._init_gui_extra_def_()

        self._path = path
        self._name = self._path.split(self.PATHSEP)[-1]

    @property
    def type(self):
        return 'namespace'

    @property
    def icon(self):
        return bsc_resource.RscExtendIcon.get('name')

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    def get_is_exists(self):
        return cmds.namespace(self.path, exists=1)

    def get_is_reference(self):
        _ = cmds.namespaceInfo(self.path, listOnlyDependencyNodes=1, dagPath=1) or []
        for i in _:
            if cmds.referenceQuery(i, isNodeReferenced=1):
                return True
        return False

    def get_objs(self):
        _ = cmds.namespaceInfo(self.path, listOnlyDependencyNodes=1, dagPath=1) or []
        return [self.Obj_CLS(i) for i in _]

    def do_delete(self):
        cmds.namespace(removeNamespace=self.name, mergeNamespaceWithRoot=1)
        bsc_log.Log.trace_method_result(
            'namespace-clear',
            u'unused-namespace: "{}"'.format(self.path)
        )


class Scene(gnl_dcc_abstracts.AbsDccNodeScene):
    FILE_CLS = gnl_dcc_objects.StgFile
    UNIVERSE_CLS = unv_objects.ObjUniverse
    #
    NAMESPACE_CLS = Namespace
    RENDER_ATTR_DICT = {
        'renderer': 'defaultRenderGlobals.currentRenderer',
        'imagePrefix': 'defaultRenderGlobals.imageFilePrefix',
        #
        'start_frame': 'defaultRenderGlobals.startFrame',
        'end_frame': 'defaultRenderGlobals.endFrame',
        #
        'animation': 'defaultRenderGlobals.animation',
        'imageFormat': 'defaultRenderGlobals.imfPluginKey',
        'periodInExt': 'defaultRenderGlobals.periodInExt',
        'putFrameBeforeExt': 'defaultRenderGlobals.putFrameBeforeExt',
        'extensionPadding': 'defaultRenderGlobals.extensionPadding',
        'renderVersion': 'defaultRenderGlobals.renderVersion',
        #
        'width': 'defaultResolution.width',
        'height': 'defaultResolution.height',
        #
        'preMel': 'defaultRenderGlobals.preMel'
    }
    FILE_TYPE_ASCII = 'mayaAscii'
    FILE_TYPE_BINARY = 'mayaBinary'
    FILE_TYPE_ALEMBIC = 'Alembic'
    FILE_TYPE_DICT = {
        '.ma': FILE_TYPE_ASCII,
        '.mb': FILE_TYPE_BINARY,
        '.abc': FILE_TYPE_ALEMBIC
    }
    WORKSPACE_RULE = {
        'scene': 'scenes',
        'templates': 'assets',
        'images': 'images',
        'sourceImages': 'sourceimages',
        'renderData': 'renderData',
        'clips': 'clips',
        'sound': 'sound',
        'scripts': 'scripts',
        'diskCache': 'data',
        'movie': 'movies',
        'translatorData': 'data',
        'timeEditor': 'Time Editor',
        'autoSave': 'autosave',
        'sceneAssembly': 'sceneAssembly',
        'offlineEdit': 'scenes/edits',
        '3dPaintTextures': 'sourceimages/3dPaintTextures',
        'depth': 'renderData/depth',
        'iprImages': 'renderData/iprImages',
        'shaders': 'renderData/shaders',
        'furFiles': 'renderData/fur/furFiles',
        'furImages': 'renderData/fur/furImages',
        'furEqualMap': 'renderData/fur/furEqualMap',
        'furAttrMap': 'renderData/fur/furAttrMap',
        'furShadowMap': 'renderData/fur/furShadowMap',
        'particles': 'cache/particles',
        'fluidCache': 'cache/nCache/fluid',
        'fileCache': 'cache/nCache',
        'bifrostCache': 'cache/bifrost',
        'teClipExports': 'Time Editor/Clip Exports',
        'mayaAscii': 'scenes',
        'mayaBinary': 'scenes',
        'mel': 'scripts',
        'OBJ': 'data',
        'audio': 'sound',
        'move': 'data',
        'eps': 'data',
        'illustrator': 'data',
        'IGES_ATF': 'data',
        'JT_ATF': 'data',
        'SAT_ATF': 'data',
        'STEP_ATF': 'data',
        'STL_ATF': 'data',
        'WIRE_ATF': 'data',
        'INVENTOR_ATF': 'data',
        'CATIAV4_ATF': 'data',
        'CATIAV5_ATF': 'data',
        'NX_ATF': 'data',
        'PROE_ATF': 'data',
        'IGES_ATF Export': 'data',
        'JT_ATF Export': 'data',
        'SAT_ATF Export': 'data',
        'STEP_ATF Export': 'data',
        'STL_ATF Export': 'data',
        'WIRE_ATF Export': 'data',
        'INVENTOR_ATF Export': 'data',
        'CATIAV5_ATF Export': 'data',
        'NX_ATF Export': 'data',
        'OBJexport': 'data',
        'BIF': 'data',
        'FBX': 'data',
        'FBX export': 'data',
        'DAE_FBX': 'data',
        'DAE_FBX export': 'data',
        'ASS Export': 'data',
        'ASS': 'data',
        'Alembic': 'data',
        'animImport': 'data',
        'animExport': 'data'
    }

    def __init__(self, *args, **kwargs):
        super(Scene, self).__init__(*args, **kwargs)

    @classmethod
    def get_namespace_paths(cls):
        return mya_core.MyaUtil.get_all_namespace_paths()

    @classmethod
    def get_namespaces(cls):
        return [cls.NAMESPACE_CLS(i) for i in cls.get_namespace_paths()]

    @classmethod
    def set_current_frame(cls, frame):
        cmds.currentTime(frame)

    @classmethod
    def get_current_frame(cls):
        return cmds.currentTime(query=1)

    @classmethod
    def set_frame_range(cls, star_frame, end_frame):
        cmds.playbackOptions(minTime=star_frame), cmds.playbackOptions(animationStartTime=int(star_frame)-5)
        cmds.playbackOptions(maxTime=end_frame), cmds.playbackOptions(animationEndTime=int(end_frame)+5)
        #
        cls.set_current_frame(star_frame)

    @classmethod
    def get_frame_range(cls, frame=None):
        if isinstance(frame, (tuple, list)):
            star_frame, end_frame = frame
        elif isinstance(frame, (int, float)):
            star_frame = end_frame = frame
        else:
            star_frame = end_frame = cls.get_current_frame()
        return float(star_frame), float(end_frame)

    @classmethod
    def _get_file_type_name_(cls, file_path):
        ext = os.path.splitext(file_path)[-1]
        return cls.FILE_TYPE_DICT.get(ext, cls.FILE_TYPE_ASCII)

    @classmethod
    def import_from_file(cls, file_path, namespace=':'):
        return cmds.file(
            file_path,
            i=True,
            options='v=0;',
            type=cls._get_file_type_name_(file_path),
            ra=True,
            mergeNamespacesOnClash=True,
            namespace=namespace,
        )

    @classmethod
    def export_to_file(cls, file_path, root=None):
        option = dict(
            type=cls._get_file_type_name_(file_path),
            options='v=0;',
            force=True,
            defaultExtensions=True,
            preserveReferences=False,
        )
        _selected_paths = []
        if root is not None:
            _selected_paths = cmds.ls(selection=1, long=1) or []
            cmds.select(root)
            option['exportSelected'] = True
        else:
            option['exportAll'] = True

        bsc_storage.StgFileOpt(file_path).create_directory()
        results = cmds.file(file_path, **option)
        if 'exportSelected' in option:
            if _selected_paths:
                cmds.select(_selected_paths)
            else:
                cmds.select(clear=1)
        return results

    @classmethod
    def get_current_file_path(cls):
        """
        :return: str(path)
        """
        return cmds.file(query=1, expandName=1)

    @classmethod
    def get_current_directory_path(cls):
        file_path = cls.get_current_file_path()
        return os.path.dirname(file_path)

    @classmethod
    def new_file(cls):
        cmds.file(new=1, force=1)

    @classmethod
    def set_file_path(cls, file_path, with_create_directory=False):
        if with_create_directory is True:
            f = gnl_dcc_objects.StgFile(file_path)
            f.create_directory()
        #
        cmds.file(rename=file_path)

    @classmethod
    def set_file_path_as_project(cls, file_path, with_create_directory=False):
        cls.set_file_path(file_path, with_create_directory)
        workspace_directory = gnl_dcc_objects.StgFile(file_path).directory.get_parent()
        cls.set_workspace_create(workspace_directory.path)

    # noinspection PyUnusedLocal
    @classmethod
    def new_file_with_dialog(cls, file_path, post_method):
        def pos_method_run_fnc_():
            if isinstance(post_method, (types.FunctionType, types.MethodType)):
                post_method(file_path)

        #
        def yes_fnc_():
            cls.save_file()
            #
            cls.new_file()
            #
            f = gnl_dcc_objects.StgFile(file_path)
            f.create_directory()
            #
            pos_method_run_fnc_()
            #
            cls.set_file_path(file_path)

        #
        def no_fnc_():
            cls.new_file()
            #
            f = gnl_dcc_objects.StgFile(file_path)
            f.create_directory()
            #
            pos_method_run_fnc_()
            #
            cls.set_file_path(file_path)

        #
        if cls.get_scene_is_dirty() is True:
            w = gui_core.GuiDialog.create(
                label='New',
                content='Scene has been modified, Do you want to save changed to "{}"'.format(
                    cls.get_current_file_path()
                ),
                window_size=(480, 160),
                #
                yes_method=yes_fnc_,
                no_method=no_fnc_,
                #
                yes_label='Save and new',
                no_label='Don\'t save and new'
            )
        else:
            no_fnc_()

    @classmethod
    def open_file(cls, file_path, ignore_format=True):
        """
        :param file_path: str,
        :param ignore_format: bool, etc. for save ".mb" but rename to ".ma"
        :return:
        """
        bsc_log.Log.trace_method_result(
            'scene open',
            u'file="{}" is started'.format(file_path)
        )
        if ignore_format is True:
            cmds.file(
                file_path,
                open=1,
                options='v=0;',
                force=1,
            )
        else:
            cmds.file(
                file_path,
                open=1,
                options='v=0;',
                force=1,
                type=cls._get_file_type_name_(file_path)
            )
        bsc_log.Log.trace_method_result(
            'scene open',
            u'file="{}" is completed'.format(file_path)
        )

    @classmethod
    def set_file_open_as_project(cls, file_path):
        cls.open_file(file_path)
        workspace_directory = gnl_dcc_objects.StgFile(file_path).directory.get_parent()
        cls.set_workspace_create(workspace_directory.path)

    @classmethod
    def save_to_file(cls, file_path):
        file_obj = gnl_dcc_objects.StgFile(file_path)
        file_obj.create_directory()
        #
        cmds.file(rename=file_path)
        cmds.file(
            save=1,
            options='v=0;',
            force=1,
            type=cls._get_file_type_name_(file_path)
        )
        bsc_log.Log.trace_method_result(
            'scene save',
            u'file="{}"'.format(file_path)
        )

    @classmethod
    def save_file(cls):
        file_path = cls.get_current_file_path()
        cmds.file(
            save=1,
            options='v=0;',
            force=1,
            type=cls._get_file_type_name_(file_path)
        )
        bsc_log.Log.trace_method_result(
            'scene save',
            u'file="{}"'.format(file_path)
        )

    @classmethod
    def get_scene_is_dirty(cls):
        return cmds.file(query=1, modified=1)

    @classmethod
    def reference_file_from(cls, file_path, namespace=None):
        f = gnl_dcc_objects.StgFile(file_path)
        if f.get_is_exists() is True:
            if namespace is None:
                namespace = f.base
            #
            bsc_log.Log.trace_method_result(
                'file-reference',
                u'file="{}"'.format(file_path)
            )
            return cmds.file(
                file_path,
                ignoreVersion=1,
                reference=1,
                mergeNamespacesOnClash=0,
                namespace=namespace,
                options='v=0;',
                type=cls._get_file_type_name_(file_path)
            )

    @classmethod
    def get_file_reference_node(cls, file_path):
        return cmds.referenceQuery(file_path, referenceNode=True, topReference=True) or None

    @classmethod
    def get_file_is_reference_exists(cls, file_path):
        return cls.get_file_reference_node(file_path) is not None

    @classmethod
    def _set_viewport_shader_display_mode_(cls, panel):
        cmds.modelEditor(
            panel,
            edit=1,
            useDefaultMaterial=0,
            displayAppearance='smoothShaded',
            displayTextures=0,
            displayLights='default',
            shadows=0
        )
        bsc_log.Log.trace_method_result(
            'viewport-set',
            u'mode="{}"'.format(
                'shader'
            )
        )

    @classmethod
    def _set_viewport_texture_display_mode_(cls, panel):
        cmds.modelEditor(
            panel,
            edit=1,
            useDefaultMaterial=0,
            displayAppearance='smoothShaded',
            displayTextures=1,
            displayLights='default',
            shadows=0
        )
        bsc_log.Log.trace_method_result(
            'viewport-set',
            u'mode="{}"'.format(
                'texture'
            )
        )

    @classmethod
    def _set_viewport_light_display_mode_(cls, panel):
        cmds.modelEditor(
            panel,
            edit=1,
            useDefaultMaterial=0,
            displayAppearance='smoothShaded',
            displayTextures=1,
            displayLights='all',
            shadows=1
        )
        bsc_log.Log.trace_method_result(
            'viewport-set',
            u'mode="{}"'.format(
                'light'
            )
        )

    @classmethod
    def set_display_mode(cls, display_mode):
        viewports = cmds.getPanel(type='modelPanel') or []
        for viewport in viewports:
            if display_mode == 5:
                cls._set_viewport_shader_display_mode_(viewport)
            elif display_mode == 6:
                cls._set_viewport_texture_display_mode_(viewport)
            elif display_mode == 7:
                cls._set_viewport_light_display_mode_(viewport)

    @classmethod
    def set_window_delete(cls, window):
        if isinstance(window, six.string_types):
            if cmds.window(window, query=1, exists=1):
                cmds.deleteUI(window, window=1)

    @classmethod
    def set_viewport(cls):
        pass

    @classmethod
    def _set_preview_viewport_setup_(cls, viewport, mode=0):
        # Render Name [<vp2Renderer>, ]
        current_viewport = viewport
        rendererName = 'base_OpenGL_Renderer'
        if mode == 1:
            rendererName = 'vp2Renderer'
        #
        panelType = cmds.getPanel(typeOf=current_viewport)
        if panelType == 'modelPanel':
            cmds.modelEditor(current_viewport, edit=1, rendererName=rendererName, rom='myOverride')
            if rendererName == 'vp2Renderer':
                cmds.setAttr('hardwareRenderingGlobals.lineAAEnable', 1)
                cmds.setAttr('hardwareRenderingGlobals.multiSampleEnable', 1)
                cmds.setAttr('hardwareRenderingGlobals.ssaoEnable', 1)

    def _load_from_location_fnc(self, root, include_obj_type):
        self.restore_all()
        #
        root_dag_path = bsc_core.PthNodeOpt(root)
        root_mya_dag_path = root_dag_path.translate_to(mya_core.MyaUtil.OBJ_PATHSEP)
        mya_root = _mya_dcc_obj_node_for_dag.Group(root_mya_dag_path.path)
        if mya_root.get_is_exists() is True:
            objs = mya_root.get_descendants()
            for i_obj in objs:
                if i_obj.type in {'mesh'}:
                    if i_obj.get_port('intermediateObject').get() is False:
                        self._create_obj_(i_obj)
                elif i_obj.get_api_type() in mya_core.MyaNodeApiTypes.Transforms:
                    self._create_obj_(i_obj)

    def _create_obj_(self, mya_obj):
        obj_category_name = unr_core.UnrObjCategory.MAYA
        obj_type_name = mya_obj.type
        mya_obj_path = mya_obj.path
        mya_dag_path = bsc_core.PthNodeOpt(mya_obj_path)
        dcc_dag_path = mya_dag_path.translate_to('/')
        dcc_obj_path = dcc_dag_path.path
        #
        obj_category = self.universe.generate_obj_category(obj_category_name)
        obj_type = obj_category.generate_type(obj_type_name)
        obj = obj_type.create_obj(dcc_obj_path)
        if mya_core.MyaUtil.get_is_ui_mode():
            import lxgui.qt.core as gui_qt_core

            obj.set_gui_attribute(
                'icon', gui_qt_core.GuiQtMaya.generate_qt_icon_by_name(obj_type_name)
            )
        return obj

    # clear
    @classmethod
    @bsc_core.MdfBaseMtd.run_with_result_trace
    def set_unused_scripts_clear(cls):
        for i in cmds.scriptJob(listJobs=1):
            for k in ['leukocyte.antivirus()']:
                if k in i:
                    bsc_log.Log.trace_result(
                        'unused-script-job-remove: "{}"'.format(k)
                    )
                    index = i.split(': ')[0]
                    cmds.scriptJob(kill=int(index), force=1)
        #
        for i in cmds.ls(type='script'):
            if i in ['breed_gene', 'vaccine_gene']:
                bsc_log.Log.trace_result(
                    'unused-script-remove: "{}"'.format(i)
                )
                cmds.delete(i)

    @classmethod
    @bsc_core.MdfBaseMtd.run_with_result_trace
    def set_unused_shaders_clear(cls):
        mel.eval('MLdeleteUnused;')

    # noinspection PyUnusedLocal
    @classmethod
    @bsc_core.MdfBaseMtd.run_with_result_trace
    def set_unused_windows_clear(cls, exclude_window_names=None):
        for panel in cmds.getPanel(visiblePanels=1) or []:
            if cmds.panel(panel, query=1, exists=1):
                window = panel+'Window'
                if cmds.window(window, query=1, exists=1):
                    cmds.deleteUI(window, window=1)
                    bsc_log.Log.trace_method_result(
                        'unused-window-clear',
                        u'window="{}"'.format(window)
                    )

    @classmethod
    @bsc_core.MdfBaseMtd.run_with_result_trace
    def set_unknown_plug_ins_clear(cls):
        _ = cmds.unknownPlugin(query=1, list=1) or []
        if _:
            with bsc_log.LogProcessContext.create(maximum=len(_), label='clean unknown-plug') as g_p:
                for i in _:
                    g_p.do_update()
                    cmds.unknownPlugin(i, remove=1)
                    bsc_log.Log.trace_method_result(
                        'unknown-plug-in-clear',
                        u'plug-in="{}"'.format(i)
                    )

    @classmethod
    @bsc_core.MdfBaseMtd.run_with_result_trace
    def set_unused_namespaces_clear(cls):
        def get_obj_parent_path_fnc_(path_):
            parent = cmds.listRelatives(path_, parent=1, fullPath=1)
            if parent:
                return parent[0]

        #
        def get_namespaces_fnc_():
            lis = []
            _exclude_namespace = ['UI', 'shared']
            _ = cmds.namespaceInfo(recurse=1, listOnlyNamespaces=1)
            if _:
                _.reverse()
                for _namespace in _:
                    if _namespace not in _exclude_namespace:
                        _obj_paths = cmds.namespaceInfo(_namespace, listOnlyDependencyNodes=1, dagPath=1)
                        _is_assembly_reference = False
                        if _obj_paths:
                            for _obj_path in _obj_paths:
                                _obj_parent_path = get_obj_parent_path_fnc_(_obj_path)
                                if _obj_parent_path is not None:
                                    if cmds.nodeType(_obj_parent_path) == 'assemblyReference':
                                        _is_assembly_reference = True
                                        break
                        #
                        if _is_assembly_reference is False:
                            lis.append(_namespace)
            return lis

        #
        def set_remove_fnc(namespace_):
            cmds.namespace(removeNamespace=namespace_)
            bsc_log.Log.trace_method_result(
                'scene-clear',
                u'unused-namespace: "{}"'.format(namespace_)
            )

        #
        def fnc_1_():
            _namespaces = get_namespaces_fnc_()
            if _namespaces:
                for _namespace in _namespaces:
                    cmds.namespace(setNamespace=_namespace)
                    child_namespaces = cmds.namespaceInfo(recurse=1, listOnlyNamespaces=1)
                    _obj_paths = cmds.namespaceInfo(listOnlyDependencyNodes=1, dagPath=1)
                    #
                    _namespace_parent = cmds.namespaceInfo(parent=1)
                    cmds.namespace(setNamespace=':')
                    if not child_namespaces:
                        if not _obj_paths:
                            set_remove_fnc(_namespace)
                        else:
                            _is_reference = False
                            #
                            for _obj_path in _obj_paths:
                                if cmds.referenceQuery(_obj_path, isNodeReferenced=1):
                                    _is_reference = True
                                    break
                            #
                            if _is_reference is False:
                                cmds.namespace(force=1, moveNamespace=(_namespace, _namespace_parent))
                                set_remove_fnc(_namespace)

        #
        fnc_1_()

    @classmethod
    @bsc_core.MdfBaseMtd.run_with_result_trace
    def set_unknown_nodes_clear(cls):
        _ = cmds.ls(type='unknown', long=1) or []
        if _:
            with bsc_log.LogProcessContext.create(maximum=len(_), label='clean unknown-node') as g_p:
                for i in _:
                    g_p.do_update()
                    if cmds.objExists(i) is True:
                        if cmds.referenceQuery(i, isNodeReferenced=1) is False:
                            cmds.lockNode(i, lock=0)
                            cmds.delete(i)
                            bsc_log.Log.trace_method_result(
                                'scene-clear',
                                u'unknown-node: "{}"'.format(i)
                            )

    @classmethod
    @bsc_core.MdfBaseMtd.run_with_result_trace
    def set_unload_references_clear(cls):
        for reference_node in cmds.ls(type='reference'):
            # noinspection PyBroadException
            try:
                is_loaded = cmds.referenceQuery(reference_node, isLoaded=1)
            except Exception:
                is_loaded = False
            #
            if is_loaded is False:
                cmds.lockNode(reference_node, lock=0)
                cmds.delete(reference_node)
                bsc_log.Log.trace_method_result(
                    'scene-clear',
                    u'unload-reference-node: "{}"'.format(reference_node)
                )

    @classmethod
    @bsc_core.MdfBaseMtd.run_with_result_trace
    def set_unused_names_clear(cls):
        _ = cmds.ls('pasted__*', long=1) or []
        if _:
            with bsc_log.LogProcessContext.create(maximum=len(_), label='clean unused-name') as g_p:
                for i in _:
                    g_p.do_update()
                    if cmds.objExists(i) is True:
                        if cmds.referenceQuery(i, isNodeReferenced=1) is False:
                            name = i.split('|')[-1]
                            new_name = str(name).replace('pasted__', '')
                            cmds.rename(
                                i, new_name
                            )

    @classmethod
    @bsc_core.MdfBaseMtd.run_with_result_trace
    def set_unused_display_layers_clear(cls):
        _ = cmds.ls(type='displayLayer', long=1) or []
        if _:
            with bsc_log.LogProcessContext.create(maximum=len(_), label='clean unknown-plug') as g_p:
                for i in _:
                    g_p.do_update()
                    #
                    if i in ['defaultLayer']:
                        continue
                    #
                    if cmds.objExists(i) is True:
                        if cmds.referenceQuery(i, isNodeReferenced=1) is False:
                            cmds.lockNode(i, lock=0)
                            cmds.delete(i)
                            bsc_log.Log.trace_method_result(
                                'scene-clear',
                                u'display-layer: "{}"'.format(i)
                            )

    @classmethod
    def set_workspace(cls, directory_path):
        pass

    @classmethod
    def get_workspace_rule(cls, key):
        return cmds.workspace(fileRuleEntry=key)

    @classmethod
    def set_workspace_create(cls, directory_path):
        # create directory
        cmds.workspace(create=directory_path)
        # create workspace
        cmds.workspace(directory_path, openWorkspace=1)
        # create default rule
        for k, v in cls.WORKSPACE_RULE.items():
            cmds.workspace(fileRule=[k, v])
        # save
        cmds.workspace(saveWorkspace=1)
        # noinspection PyBroadException
        try:
            mel.eval(
                'sp_setLocalWorkspaceCallback "{}";'.format(directory_path)
            )
        except Exception:
            bsc_core.ExceptionMtd.set_print()

    @classmethod
    def get_workspace_directory_path(cls):
        _ = cmds.workspace(query=1, rootDirectory=1)
        if _:
            if _.endswith('/'):
                return _[:-1]

    @classmethod
    def set_file_open_with_dialog(cls, file_path):
        file_type_name = cls._get_file_type_name_(file_path)
        mel_cmd = 'openRecentFile("{}", "{}");'.format(
            file_path,
            file_type_name
        )
        mel.eval(mel_cmd)
        workspace_directory = gnl_dcc_objects.StgFile(file_path).directory.get_parent()
        cls.set_workspace_create(workspace_directory.path)

    # render
    @classmethod
    def get_render_cameras(cls):
        lis = []
        _ = cmds.ls(type='camera', long=1)
        for camera_path in _:
            camera = _mya_dcc_obj_node_for_dag.Camera(camera_path)
            if camera.get_is_renderable():
                lis.append(camera)
        return lis

    @classmethod
    def get_current_render_camera_path(cls, camera_path=None):
        if camera_path is None:
            _ = cls.get_render_cameras()
            if _:
                return _[0].path
            return '|persp|perspShape'
        return camera_path

    @classmethod
    def set_render_resolution(cls, width, height):
        cmds.setAttr(cls.RENDER_ATTR_DICT['width'], width)
        cmds.setAttr(cls.RENDER_ATTR_DICT['height'], height)
        if width == height:
            cmds.setAttr('defaultResolution.deviceAspectRatio', 1)
        cmds.setAttr('defaultResolution.pixelAspect', 1)

    @classmethod
    def get_render_resolution(cls):
        width = cmds.getAttr(cls.RENDER_ATTR_DICT['width'])
        height = cmds.getAttr(cls.RENDER_ATTR_DICT['height'])
        return int(width), int(height)

    @classmethod
    def set_render_frame_range(cls, star_frame=None, end_frame=None):
        if not star_frame:
            star_frame = int(cmds.playbackOptions(query=1, minTime=1))
        if not end_frame:
            end_frame = int(cmds.playbackOptions(query=1, maxTime=1))
        #
        cmds.setAttr(cls.RENDER_ATTR_DICT['start_frame'], star_frame)
        cmds.setAttr(cls.RENDER_ATTR_DICT['end_frame'], end_frame)

    @classmethod
    def get_render_frame_range(cls):
        start_frame = cmds.getAttr(cls.RENDER_ATTR_DICT['start_frame'])
        end_frame = cmds.getAttr(cls.RENDER_ATTR_DICT['end_frame'])
        return int(start_frame), int(end_frame)

    @classmethod
    def show_message(cls, message, keyword, position='topCenter', fade=1, drag_kill=0, alpha=.5):
        # topLeft topCenter topRight
        # midLeft midCenter midCenterTop midCenterBot midRight
        # botLeft botCenter botRight
        assistMessage = '%s <hl>%s</hl>'%(message, keyword)
        cmds.inViewMessage(
            assistMessage=assistMessage,
            fontSize=12,
            position=position,
            fade=fade,
            dragKill=drag_kill,
            alpha=alpha
        )

    @classmethod
    def get_tag_as_36(cls):
        file_path = cls.get_current_file_path()
        file_opt = bsc_storage.StgFileOpt(file_path)
        timestamp = file_opt.get_modify_timestamp()
        time_tag = bsc_core.RawIntegerOpt(int(timestamp*10)).set_encode_to_36()
        size = file_opt.get_size()
        size_tag = bsc_core.RawIntegerOpt(int(size)).set_encode_to_36()
        return '{}{}'.format(time_tag, size_tag)
