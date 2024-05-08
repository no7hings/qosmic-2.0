# coding:utf-8
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.storage as bsc_storage


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
    def get_file_type(cls, file_path):
        ext = os.path.splitext(file_path)[-1]
        return cls.FILE_TYPE_DICT.get(ext, cls.FILE_TYPE_ASCII)

    @classmethod
    def reference_file(cls, file_path, namespace=':'):
        if os.path.isfile(file_path) is True:
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
    def get_current_file_path(cls):
        """
        :return: str(path)
        """
        return cmds.file(query=1, expandName=1)

    @classmethod
    def import_file(cls, file_path, namespace=':'):
        if os.path.isfile(file_path) is True:
            return cmds.file(
                file_path,
                i=True,
                options='v=0;',
                type=cls.get_file_type(file_path),
                ra=True,
                mergeNamespacesOnClash=True,
                returnNewNodes=True,
                namespace=namespace,
            )
    
    @classmethod
    def export_file(cls, file_path, location=None):
        option = dict(
            type=cls.get_file_type(file_path),
            options='v=0;',
            force=True,
            defaultExtensions=True,
            preserveReferences=False,
        )
        _selected_paths = []
        if location is not None:
            _selected_paths = cmds.ls(selection=1, long=1) or []
            cmds.select(location)
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
    def new(cls):
        cmds.file(new=1, force=1)

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
