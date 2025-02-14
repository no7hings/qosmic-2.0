# coding:utf-8
import six

import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core


class SceneFile:
    FILE_TYPE_ASCII = 'mayaAscii'
    FILE_TYPE_BINARY = 'mayaBinary'
    FILE_TYPE_ALEMBIC = 'Alembic'

    FILE_TYPE_DICT = {
        '.ma': FILE_TYPE_ASCII,
        '.mb': FILE_TYPE_BINARY,
        '.abc': FILE_TYPE_ALEMBIC,
        '.fbx': 'FBX',
    }

    @classmethod
    def get_namespace(cls, file_path):
        # noinspection PyBroadException
        try:
            parent_namespaces = cmds.file(file_path, q=True, parentNamespace=True)
            namespace = cmds.file(file_path, q=True, namespace=True)
            # when parent namespace is [''], then is from root return self namespace
            if parent_namespaces == ['']:
                return namespace
            return ':'.join(parent_namespaces+[namespace])
        except Exception:
            return None

    @classmethod
    def get_reference_node(cls, file_path):
        # noinspection PyBroadException
        try:
            return cmds.file(file_path, q=True, referenceNode=True)
        except Exception:
            return None

    @classmethod
    def get_reference_args(cls, file_path):
        # noinspection PyBroadException
        try:
            return cmds.file(file_path, q=True, namespace=True), cmds.file(file_path, q=True, referenceNode=True)
        except Exception:
            return None

    @classmethod
    def get_file_type(cls, file_path):
        ext = os.path.splitext(file_path)[-1]
        return cls.FILE_TYPE_DICT.get(ext, cls.FILE_TYPE_ASCII)

    @classmethod
    def reference_file(cls, file_path, namespace=':'):
        if os.path.isfile(file_path) is False:
            return None
        return cmds.file(
            file_path,
            ignoreVersion=1,
            reference=1,
            mergeNamespacesOnClash=0,
            namespace=namespace,
            options='v=0;',
            type=cls.get_file_type(file_path)
        )

    @classmethod
    def get_current(cls):
        """
        :return: str(path)
        """
        return cmds.file(query=1, expandName=1)

    @classmethod
    def import_file(cls, file_path, namespace=':'):
        """
    Set/query the currently set file options. file options are used while saving a maya file. Two file option flags supported in current file command are v and p.
    v(verbose) indicates whether long or short attribute names and command flags names are used when saving the file. Used by both maya ascii and maya binary file formats.
    It only can be 0 or 1.
    Setting v=1 indicates that long attribute names and command flag names will be used. By default, or by setting v=0, short attribute names will be used.
    p(precision) defines the maya file IO's precision when saving the file. Only used by maya ascii file format.
    It is an integer value. The default value is 17.
    The option format is "flag1=XXX;flag2=XXX".Maya uses the last v and p as the final result.
    Note:
    1. Use a semicolon(";") to separate several flags. 2. No blank space(" ") in option string.
        """
        if os.path.isfile(file_path) is False:
            raise RuntimeError()

        return cmds.file(
            file_path,
            i=1,
            force=1,
            options='v=0;',
            type=cls.get_file_type(file_path),
            ignoreVersion=1,
            ra=1,
            mergeNamespacesOnClash=1,
            returnNewNodes=1,
            namespace=namespace,
        )

    @classmethod
    def import_scene(cls, file_path, namespace=':'):
        """
        file -import -type "mayaAscii"  -ignoreVersion -ra true -mergeNamespacesOnClash true -namespace ":" -options "v=0;p=17;f=0"  -pr  -importFrameRate true  -importTimeRange "override" "X:/QSM_TST/A001/A001_001/动画/通过文件/A001_001_001.ma";
        """
        cmds.file(
            file_path,
            i=1,
            type=cls.get_file_type(file_path),
            ignoreVersion=1,
            ra=1,
            mergeNamespacesOnClash=1,
            namespace=namespace,
            options='v=1;',
            pr=1,
            importFrameRate=1,
            importTimeRange='override'
        )

    @classmethod
    def import_fbx(cls, file_path, namespace=':'):
        """
        file
        -import
        -type "FBX"
        -ignoreVersion
        -ra true
        -mergeNamespacesOnClash false
        -namespace "Fast_Run__1_"
        -options "fbx"
        -pr
        -importFrameRate true
        -importTimeRange "override" "C:/Users/nothings/Downloads/Fast Run (1).fbx";
        """
        cmds.loadPlugin('fbxmaya', quiet=1)
        nodes = cmds.file(
            file_path,
            i=1,
            force=1,
            type=cls.get_file_type(file_path),
            ignoreVersion=1,
            ra=1,
            mergeNamespacesOnClash=1,
            namespace=namespace,
            options='fbx',
            pr=1,
            importFrameRate=1,
            importTimeRange='override',
            returnNewNodes=1,
        )
        if namespace != ':':
            if cmds.namespace(exists=namespace) is False:
                cmds.namespace(add=namespace)

            # remove from leaf
            if nodes:
                nodes.reverse()

            for i in nodes:
                i_name = i.split('|')[-1]
                if ':' in i_name:
                    i_name_new = '{}:{}'.format(namespace, i_name.split(':')[-1])
                else:
                    i_name_new = '{}:{}'.format(namespace, i_name)

                cmds.rename(i, i_name_new)

    @classmethod
    def import_file_ignore_error(cls, file_path, namespace=':'):
        # noinspection PyBroadException
        try:
            return cls.import_file(file_path, namespace)
        except Exception:
            import traceback
            traceback.print_exc()

    @classmethod
    def import_container_file(cls, file_path, namespace=':'):
        """
file -import -type "mayaAscii"  -ignoreVersion -ra true -mergeNamespacesOnClash false -namespace "gpu" -options "v=1;"  -pr  -importFrameRate true  -importTimeRange "override" "Z:/caches/temporary/.asset-cache/unit-assembly/10E/B0768C98-5DF4-3D31-AA9D-AAE3BF84651E/gpu.ma";
        """
        if os.path.isfile(file_path) is False:
            raise RuntimeError()

        return cmds.file(
            file_path,
            i=1,
            type=cls.get_file_type(file_path),
            ignoreVersion=1,
            ra=1,
            mergeNamespacesOnClash=1,
            namespace=namespace,
            # todo: why v=1???, pr=1?
            options='v=1;',
            pr=1,
        )
    
    @classmethod
    def export_file(cls, file_path, location=None, keep_reference=False, locations_extend=None):
        kwargs = dict(
            type=cls.get_file_type(file_path),
            options='v=0;',
            force=True,
            defaultExtensions=True,
            # keep reference
            preserveReferences=keep_reference,
        )
        sel_mask = []
        if location is not None:
            sel_mask = cmds.ls(selection=1, long=1) or []
            cmds.select(location)
            if locations_extend is not None:
                for i in locations_extend:
                    if cmds.objExists(i):
                        cmds.select(i, noExpand=1, add=1)

            kwargs['exportSelected'] = True
        else:
            kwargs['exportAll'] = True

        bsc_storage.StgFileOpt(file_path).create_directory()
        results = cmds.file(file_path, **kwargs)
        if 'exportSelected' in kwargs:
            if sel_mask:
                cmds.select(sel_mask)
            else:
                cmds.select(clear=1)
        return results

    @classmethod
    def new(cls):
        cmds.file(new=1, force=1)

    @classmethod
    def refresh(cls):
        cmds.refresh(force=True)

    @classmethod
    def repath_to(cls, file_path, with_create_directory=False):
        if with_create_directory is True:
            f = bsc_storage.StgFileOpt(file_path)
            f.create_directory()
        #
        cmds.file(rename=file_path)

    @classmethod
    def is_dirty(cls):
        return cmds.file(query=1, modified=1)

    @classmethod
    def save(cls):
        file_path = cls.get_current()
        cmds.file(
            save=1,
            options='v=0;',
            force=1,
            type=cls.get_file_type(file_path)
        )

    @classmethod
    def open_with_dialog(cls, file_path):
        if cls.is_dirty() is True:
            if gui_core.GuiUtil.language_is_chs():
                result = gui_core.GuiApplication.exec_message_dialog(
                    u'保存修改到: {}?'.format(
                        cls.get_current()
                    ),
                    title='保存文件？',
                    show_no=True,
                    show_cancel=True,
                    size=(320, 120),
                    status='warning'
                )
            else:
                result = gui_core.GuiApplication.exec_message_dialog(
                    u'Save changes to: {}?'.format(
                        cls.get_current()
                    ),
                    title='Save Scene?',
                    show_no=True,
                    show_cancel=True,
                    size=(320, 120),
                    status='warning'
                )

            if result is True:
                cls.save_to(cls.get_current())
                cls.open(file_path, add_to_recent=True)
                return True
            elif result is False:
                cls.open(file_path, add_to_recent=True)
                return True
        else:
            cls.open(file_path, add_to_recent=True)
            return True
        return False

    @classmethod
    def add_to_recent_files(cls, file_path):
        pass
        # recent_files = cmds.optionVar(query="RecentFilesList") or []
        # if file_path not in recent_files:
        #     cmds.optionVar(stringValueAppend=("RecentFilesList", file_path))

    @classmethod
    def new_with_dialog(cls):
        if cls.is_dirty() is True:
            if gui_core.GuiUtil.language_is_chs():
                result = gui_core.GuiApplication.exec_message_dialog(
                    u'保存修改到: {}?'.format(
                        cls.get_current()
                    ),
                    title='保存文件？',
                    show_no=True,
                    show_cancel=True,
                    size=(320, 120),
                    status='warning',
                )
            else:
                result = gui_core.GuiApplication.exec_message_dialog(
                    u'Save changes to: {}?'.format(
                        cls.get_current()
                    ),
                    title='Save Scene?',
                    show_no=True,
                    show_cancel=True,
                    size=(320, 120),
                    status='warning',
                )
            if result is True:
                cls.save_to(cls.get_current())
                cls.new()
                return True
            elif result is False:
                cls.new()
                return True
        else:
            cls.new()
            return True
        return False

    @classmethod
    def save_with_dialog(cls, file_path):
        # check file directory is changed, when changed save to.
        if os.path.dirname(file_path) == os.path.dirname(cls.get_current()):
            if cls.is_dirty() is True:
                cls.save_to(file_path)
                return True

            if gui_core.GuiUtil.language_is_chs():
                gui_core.GuiApplication.exec_message_dialog(
                    '沒有需要保存的更改。',
                    title='保存文件',
                    size=(320, 120),
                    status='warning',
                )
            else:
                gui_core.GuiApplication.exec_message_dialog(
                    'No changes to save.',
                    title='Save Scene',
                    size=(320, 120),
                    status='warning',
                )
            return False
        cls.save_to(file_path)
        return True

    @classmethod
    def increment_and_save_with_dialog(cls, file_path, force=False):
        if cls.is_dirty() is True:
            cls.save_to(file_path)
            return True

        if force is True:
            cls.save_to(file_path)
            return True
        else:
            if gui_core.GuiUtil.language_is_chs():
                gui_core.GuiApplication.exec_message_dialog(
                    '沒有需要保存的更改。',
                    title='加存',
                    size=(320, 120),
                    status='warning',
                )
            else:
                gui_core.GuiApplication.exec_message_dialog(
                    'No changes to save.',
                    title='Increment and Save',
                    size=(320, 120),
                    status='warning',
                )
        return False

    @classmethod
    def ensure_save_width_dialog(cls):
        if cls.is_dirty() is True:
            if gui_core.GuiUtil.language_is_chs():
                result = gui_core.GuiApplication.exec_message_dialog(
                    u'有未保存的修改：{}，点击“Ok”以继续。'.format(
                        cls.get_current()
                    ),
                    title='保存修改到文件',
                    show_no=True,
                    show_cancel=True,
                    size=(320, 120),
                    status='warning',
                )
            else:
                result = gui_core.GuiApplication.exec_message_dialog(
                    u'There are unsaved edits: {}, click "Ok" to continue.'.format(
                        cls.get_current()
                    ),
                    title='Save Changes to Scene',
                    show_no=True,
                    show_cancel=True,
                    size=(320, 120),
                    status='warning',
                )
            if result is True:
                cls.save()
                return True
            return False
        return True

    @classmethod
    def open(cls, file_path, ignore_format=True, add_to_recent=False, load_no_references=False):
        if ignore_format is True:
            kwargs = dict(
                open=1,
                options='v=0;',
                force=1,
            )
        else:
            kwargs = dict(
                open=1,
                options='v=0;',
                force=1,
                type=cls.get_file_type(file_path)
            )

        if load_no_references is True:
            kwargs['loadNoReferences'] = True

        cmds.file(
            file_path,
            **kwargs
        )

        if add_to_recent is True:
            cls.add_to_recent_files(file_path)

    @classmethod
    def save_to(cls, file_path):
        file_opt = bsc_storage.StgFileOpt(file_path)
        file_opt.create_directory()
        cmds.file(rename=file_path)
        cmds.file(
            save=1,
            options='v=0;',
            force=1,
            type=cls.get_file_type(file_path)
        )

    @classmethod
    def export_as_node_graph(cls, file_path, location):
        """
            file -force
            -exportSelected
            -constructionHistory true
            -channels true
            -expressions true
            -constraints true
            -shader true
            -type $fileType
            $filePath;
        """
        bsc_storage.StgFileOpt(file_path).create_directory()
        cmds.select(location)
        kwargs = dict(
            exportSelected=1,
            force=1,
            constructionHistory=1,
            channels=1,
            expressions=1,
            constraints=1,
            shader=1,
            type=cls.get_file_type(file_path)
        )
        return cmds.file(file_path, **kwargs)

    @classmethod
    def import_as_node_graph(cls, file_path):
        """
        string $newTransforms[] = `file -force
            -import
            -renameAll true
            -renamingPrefix "pasted_"
            -groupReference
            -returnNewNodes
            $filePath`;

        select -replace `ls -dag -head 1 $newTransforms`;
        """
        name = bsc_core.BscRandomName().next()
        kwargs = dict(
            i=True,
            force=True,
            renameAll=True,
            renamingPrefix='QSM_{}'.format(name.upper()),
            groupReference=1,
            returnNewNodes=1,
            groupName='QSM_{}_GRP'.format(name.upper())
        )
        _ = cmds.file(file_path, **kwargs)
        cmds.select(_)
        cmds.sets(name='QSM_{}_SET'.format(name.upper()))
        cmds.select(cmds.ls(_, dag=1, head=1), replace=1)
        return _

    @classmethod
    def collection_alembic_caches_auto(cls):
        """
        just use for simulation scene release
        """
        from . import alembic_cache as _alembic_cache

        scene_path = cls.get_current()

        directory_path = os.path.dirname(scene_path)
        file_base_name = os.path.splitext(os.path.basename(scene_path))[0]

        nodes = _alembic_cache.AlembicNodes.get_all()

        for i_node in nodes:
            i_file_path = _alembic_cache.AlembicNode.get_file(i_node)
            i_file_name = os.path.basename(i_file_path)
            i_file_path_new = u'{}/{}__{}'.format(
                directory_path, file_base_name, i_file_name
            )
            if os.path.isfile(i_file_path_new) is False:
                bsc_storage.StgFileOpt(i_file_path).copy_to_file(i_file_path_new)

            _alembic_cache.AlembicNode.repath_to(i_node, i_file_path_new)

    @classmethod
    def collection_alembic_caches_to(cls, cache_directory_path):
        from . import alembic_cache as _alembic_cache

        nodes = _alembic_cache.AlembicNodes.get_all()

        for i_node in nodes:
            i_file_path = _alembic_cache.AlembicNode.get_file(i_node)
            i_file_name = os.path.basename(i_file_path)
            i_file_path_new = u'{}/{}'.format(
                cache_directory_path, i_file_name
            )

            if os.path.isfile(i_file_path_new) is False:
                bsc_storage.StgFileOpt(i_file_path).copy_to_file(i_file_path_new)

            _alembic_cache.AlembicNode.repath_to(i_node, i_file_path_new)


class Workspace:
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

    @classmethod
    def create(cls, directory_path):
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
                'source setProject; sp_setLocalWorkspaceCallback "{}";'.format(directory_path)
            )
        except Exception:
            bsc_core.BscException.set_print()
