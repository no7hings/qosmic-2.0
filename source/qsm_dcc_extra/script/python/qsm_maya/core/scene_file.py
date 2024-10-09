# coding:utf-8
import six

import types

import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core


class SceneFile(object):
    FILE_TYPE_ASCII = 'mayaAscii'
    FILE_TYPE_BINARY = 'mayaBinary'
    FILE_TYPE_ALEMBIC = 'Alembic'

    FILE_TYPE_DICT = {
        '.ma': FILE_TYPE_ASCII,
        '.mb': FILE_TYPE_BINARY,
        '.abc': FILE_TYPE_ALEMBIC
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
            ra=1,
            mergeNamespacesOnClash=1,
            returnNewNodes=1,
            namespace=namespace,
        )

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
    def export_file(cls, file_path, location=None, keep_reference=False):
        kwargs = dict(
            type=cls.get_file_type(file_path),
            options='v=0;',
            force=True,
            defaultExtensions=True,
            # keep reference
            preserveReferences=keep_reference,
        )
        selected_mark = []
        if location is not None:
            selected_mark = cmds.ls(selection=1, long=1) or []
            cmds.select(location)
            kwargs['exportSelected'] = True
        else:
            kwargs['exportAll'] = True

        bsc_storage.StgFileOpt(file_path).create_directory()
        results = cmds.file(file_path, **kwargs)
        if 'exportSelected' in kwargs:
            if selected_mark:
                cmds.select(selected_mark)
            else:
                cmds.select(clear=1)
        return results

    @classmethod
    def new(cls):
        cmds.file(new=1, force=1)

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
            result = gui_core.GuiApplication.exec_message_dialog(
                six.u('Save changed to: {}?').format(
                    cls.get_current()
                ),
                title='Open Scene',
                show_no=True,
                show_cancel=True,
                size=(320, 120),
                status='warning'
            )
            if result is True:
                cls.save_to(cls.get_current())
                cls.open(file_path)
                return True
            elif result is False:
                cls.open(file_path)
                return True
        else:
            cls.open(file_path)
            return True
        return False

    @classmethod
    def new_with_dialog(cls):
        if cls.is_dirty() is True:
            result = gui_core.GuiApplication.exec_message_dialog(
                six.u('Save changed to: {}?').format(
                    cls.get_current()
                ),
                title='New Scene',
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

            gui_core.GuiApplication.exec_message_dialog(
                'No changed to save.',
                title='Save Scene',
                size=(320, 120),
                status='warning',
            )
            return False
        cls.save_to(file_path)
        return True

    @classmethod
    def open(cls, file_path, ignore_format=True):
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
                type=cls.get_file_type(file_path)
            )

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
        name = bsc_core.RandomName().next()
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
