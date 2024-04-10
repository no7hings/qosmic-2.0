# coding:utf-8
import six

import os

import lxbasic.log as bsc_log
# maya
from ...core.wrap import *

from ... import core as mya_core

from ... import abstracts as mya_abstracts


class Port(mya_abstracts.AbsMyaPort):
    def __init__(self, node, name, port_assign=None):
        super(Port, self).__init__(node, name, port_assign=port_assign)


class Connection(mya_abstracts.AbsMyaNodeConnection):
    PORT_PATHSEP = mya_core.MyaUtil.PORT_PATHSEP

    def __init__(self, source, target):
        super(Connection, self).__init__(source, target)


class SceneFile(object):
    FILE_TYPE_ASCII = 'mayaAscii'
    FILE_TYPE_BINARY = 'mayaBinary'
    FILE_TYPE_ALEMBIC = 'Alembic'
    FILE_TYPE_DICT = {
        '.ma': FILE_TYPE_ASCII,
        '.mb': FILE_TYPE_BINARY,
        '.abc': FILE_TYPE_ALEMBIC
    }

    def __init__(self, file_path=None):
        self._file_path = file_path

    @classmethod
    def get_type(cls, file_path=None):
        """
        :param file_path: str(path)
        :return: str(type)
        """
        ext = os.path.splitext(file_path)[-1]
        return cls.FILE_TYPE_DICT.get(ext, cls.FILE_TYPE_ASCII)

    @classmethod
    def get_current_file_path(cls):
        """
        :return: str(path)
        """
        _ = cmds.file(query=1, expandName=1)
        if isinstance(_, six.string_types):
            return _.replace('\\', '/')

    @classmethod
    def get_current_directory_path(cls):
        file_path = cls.get_current_file_path()
        return os.path.dirname(file_path)

    @classmethod
    def set_open(cls, file_path=None, ignore_format=True):
        """
        :param file_path: str,
        :param ignore_format: bool, etc. for save ".mb" but rename to ".ma"
        :return:
        """
        if ignore_format is True:
            cmds.file(
                file_path,
                open=1,
                options='v=0',
                force=1,
                # type=cls.get_type(file_path)
            )
        else:
            cmds.file(
                file_path,
                open=1,
                options='v=0',
                force=1,
                type=cls.get_type(file_path)
            )
        #
        bsc_log.Log.trace_result(
            'open file: {}'.format(file_path)
        )

    @classmethod
    def set_reference_create(cls, file_path, namespace=':'):
        return cmds.file(
            file_path,
            ignoreVersion=1,
            reference=1,
            mergeNamespacesOnClash=0,
            namespace=namespace,
            options='v=0;p=17;f=0',
            type=cls.get_type(file_path)
        )


class Selection(object):
    def __init__(self, *args):
        self._paths = args[0]

    def select_all(self):
        exist_paths = [i for i in self._paths if cmds.objExists(i)]
        cmds.select(exist_paths)

    @classmethod
    def set_clear(cls):
        cmds.select(clear=1)

    @classmethod
    def get_current(cls):
        _ = cmds.ls(selection=1, long=1)
        if _:
            return _[0]

    @classmethod
    def get_selected_paths(cls, include=None):
        if include is not None:
            return cmds.ls(selection=1, type=include, long=1, dag=1, noIntermediate=1)
        return cmds.ls(selection=1, long=1, dag=1, noIntermediate=1)


class TextureWorkspace(object):
    pass


class ConfirmDialog(object):
    def __init__(self, title, message):
        self._title = title
        self._message = message

    def show(self):
        cmds.confirmDialog(
            title=self._title,
            message=self._message
        )

    @classmethod
    def show_warning(cls, message):
        cmds.confirmDialog(
            title='Warning',
            message=message
        )

    @classmethod
    def show_result(cls, message):
        cmds.confirmDialog(
            title='Result',
            message=message
        )

    @classmethod
    def show_error(cls, message):
        cmds.confirmDialog(
            title='Error',
            message=message
        )
