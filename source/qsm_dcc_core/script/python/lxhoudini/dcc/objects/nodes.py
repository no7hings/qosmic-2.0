# coding:utf-8
import os

import re

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import lxbasic.dcc.objects as bsc_dcc_objects
# houdini
from ...core.wrap import *

from ... import core as hou_core

from ... import abstracts as hou_abstracts

from . import node as hou_dcc_obj_node


class AbsFileReferences(object):
    DCC_FILE_REFERENCE_NODE_CLS = None
    SCENE_CLS = None
    # file type
    INCLUDE_DCC_FILE_TYPES = []
    EXCLUDE_DCC_FILE_TYPES = []
    # file ext
    INCLUDE_FILE_TYPES = []

    def __init__(self, *args):
        pass

    @classmethod
    def get_houdini_absolutely_path_with_parm(cls, hou_parm, path):
        re_pattern = r'.*?(\$F.*?)[\.]'
        re_results = re.findall(re_pattern, path)
        if re_results:
            frame = 9527
            sequence_path = hou_parm.evalAsStringAtFrame(frame)
            _path = sequence_path.replace(str(frame), re_results[0])
            is_sequence = True
        else:
            _path = hou_parm.eval()
            is_sequence = False
        return _path, is_sequence

    def _get_type_is_valid(self, dcc_file_type):
        raise NotImplementedError()

    def _get_type_is_used(self, file_type):
        raise NotImplementedError()

    def get_objs(self):
        list_ = []
        PORT_PATHSEP = hou_core.HouUtil.PORT_PATHSEP
        for i_hou_parm, i_hou_path in hou.fileReferences():
            if i_hou_parm is not None:
                if i_hou_path.startswith('op:'):
                    _reference_hou_node = i_hou_parm.evalAsNode()
                else:
                    i_file_path, _ = self.get_houdini_absolutely_path_with_parm(i_hou_parm, i_hou_path)
                    i_file_type = i_hou_parm.parmTemplate().fileType()
                    if self._get_type_is_valid(i_file_type) is True:
                        i_node_path = i_hou_parm.node().path()
                        i_node = self.DCC_FILE_REFERENCE_NODE_CLS(i_node_path)
                        # attribute name
                        i_attribute_path = i_hou_parm.path()
                        i_port_path = i_attribute_path.split(PORT_PATHSEP)[-1]
                        # file path
                        i_reference_file_path = bsc_storage.StgPathOpt(i_file_path).__str__()
                        i_node.register_file(i_port_path, i_reference_file_path)
                        list_.append(i_node)
        return list_


class FileReferences(AbsFileReferences):
    DCC_FILE_REFERENCE_NODE_CLS = hou_dcc_obj_node.FileReference
    INCLUDE_DCC_FILE_TYPES = [
        hou.fileType.Any,
        hou.fileType.Geometry,
    ]

    def __init__(self, *args):
        super(FileReferences, self).__init__(*args)

    def _get_type_is_valid(self, dcc_file_type):
        return dcc_file_type in self.INCLUDE_DCC_FILE_TYPES

    def _get_type_is_used(self, file_type):
        return True


class FileReferencesOld(object):
    DCC_NODE_CLS_DICT = {
        'custom': hou_dcc_obj_node.FileReference,
        'arnold::Driver/materialx': hou_dcc_obj_node.AndMaterialx,
    }
    CUSTOM_SEARCH_KEYS = [
        'arnold::Driver/materialx.filename',
    ]

    def __init__(self, *args):
        self._node_raw = {}

    def _get_obj_cls(self, obj_type_path):
        if obj_type_path in self.DCC_NODE_CLS_DICT:
            return self.DCC_NODE_CLS_DICT[obj_type_path]
        return self.DCC_NODE_CLS_DICT['custom']

    # noinspection PyBroadException
    def __get_by_definition(self):
        for hou_port, plf_path in hou.fileReferences():
            if hou_port is not None:
                if hou_port is not None:
                    port_path = hou_port.path()
                    hou_obj = hou_port.node()
                    dcc_path = hou_port.node().path()
                    obj_type_path = hou_obj.type().nameWithCategory()
                    try:
                        file_path = hou_port.unexpandedString()
                    except Exception:
                        file_path = hou_port.eval()
                    #
                    if dcc_path in self._node_raw:
                        dcc_obj = self._node_raw[dcc_path]
                    else:
                        obj_class = self._get_obj_cls(obj_type_path)
                        dcc_obj = obj_class(dcc_path)
                        self._node_raw[dcc_path] = dcc_obj
                    #
                    dcc_obj.register_file(
                        port_path, file_path
                    )

    def __get_by_custom(self):
        pass

    def get_objs(self):
        self._node_raw = {}
        self.__get_by_definition()
        self.__get_by_custom()
        return self._node_raw.values()


class TextureReferences(AbsFileReferences):
    DCC_FILE_REFERENCE_NODE_CLS = hou_dcc_obj_node.ImageReference
    INCLUDE_DCC_FILE_TYPES = [
        hou.fileType.Image
    ]

    def __init__(self, *args):
        super(TextureReferences, self).__init__(*args)

    def _get_type_is_valid(self, dcc_file_type):
        return dcc_file_type in self.INCLUDE_DCC_FILE_TYPES

    def _get_type_is_used(self, file_type):
        return True


class References(object):
    STG_FILE_CLS = bsc_dcc_objects.StgFile

    def __init__(self, *args):
        pass

    @classmethod
    def get_houdini_absolutely_path_with_path(cls, path):
        path_ = path
        if '$' in path_:
            # noinspection RegExpRedundantEscape
            re_pattern = re.compile(r'[\$](.*?)[\/]', re.S)
            results = re.findall(re_pattern, path_)
            for environ_key in results:
                variant = '${}'.format(environ_key)
                if environ_key in os.environ:
                    environ_value = os.environ[environ_key]
                    path_ = path_.replace(variant, environ_value)
                else:
                    bsc_log.Log.trace_warning('Variant "{}" in "{}" is Not Available.'.format(variant, path_))
        return path_

    def get_stg_files(self):
        list_ = []
        for hou_parm, path in hou.fileReferences():
            if hou_parm is None:
                plf_path = self.get_houdini_absolutely_path_with_path(path)
                os_file = self.STG_FILE_CLS(plf_path)
                list_.append(os_file)
        return list_


# node stack ********************************************************************************************************* #
class Alembics(hou_abstracts.AbsHouObjs):
    DCC_TYPES_INCLUDE = [
        'Sop/alembic',
    ]
    DCC_NODE_CLS = hou_dcc_obj_node.Alembic
    FILE_REFERENCE_FILE_PORT_PATHS_DICT = {
        'Sop/alembic': ['fileName']
    }

    def __init__(self, *args):
        super(Alembics, self).__init__(*args)


class Materialxs(hou_abstracts.AbsHouObjs):
    DCC_TYPES_INCLUDE = [
        'arnold::Driver/materialx',
    ]
    DCC_NODE_CLS = hou_dcc_obj_node.AndMaterialx
    FILE_REFERENCE_FILE_PORT_PATHS_DICT = {
        'arnold::Driver/materialx': ['filename']
    }

    def __init__(self, *args):
        super(Materialxs, self).__init__(*args)
