# coding:utf-8
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


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
    def _get_file_type_name_(cls, file_path):
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
                type=cls._get_file_type_name_(file_path)
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
                type=cls._get_file_type_name_(file_path),
                ra=True,
                mergeNamespacesOnClash=True,
                namespace=namespace,
            )