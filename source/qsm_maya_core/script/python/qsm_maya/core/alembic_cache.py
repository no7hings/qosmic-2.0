# coding:utf-8
import six

import copy
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from . import time_ as _time

from . import node_for_dag as _node_for_dag

from . import attribute as _attribute


class AlembicCacheExport(object):
    FILE = 'file'
    FRAME_RANGE = 'frameRange'
    FRAME_RELATIVE_SAMPLE = 'frameRelativeSample'
    STEP = 'step'
    ROOT = 'root'
    ATTR = 'attr'
    #
    DATA_FORMAT = 'dataFormat'
    #
    NO_NORMAL = 'noNormals'
    RENDER_ONLY = 'ro'
    STRIP_NAMESPACE = 'stripNamespaces'
    UV_WRITE = 'uvWrite'
    WRITE_FACE_SETS = 'writeFaceSets'
    WHOLE_FRAME_GEO = 'wholeFrameGeo'
    WORLD_SPACE = 'worldSpace'
    WRITE_VISIBILITY = 'writeVisibility'
    EULER_FILTER = 'eulerFilter'
    WRITE_CREASES = 'writeCreases'
    WRITE_UV_SETS = 'writeUVSets'
    #
    ATTR_PREFIX = 'attrPrefix'
    #
    DEFAULT_OPTIONS = {
        NO_NORMAL: False,
        RENDER_ONLY: False,
        STRIP_NAMESPACE: True,
        UV_WRITE: True,
        WRITE_FACE_SETS: False,
        WHOLE_FRAME_GEO: False,
        WORLD_SPACE: True,
        WRITE_VISIBILITY: True,
        EULER_FILTER: False,
        WRITE_CREASES: False,
        WRITE_UV_SETS: True,
    }
    #
    OGAWA = 'ogawa'
    HDF = 'hdf'
    #
    DATA_FORMATS = [
        OGAWA,
        HDF
    ]
    PLUG_NAME = 'AbcExport'

    def __init__(
        self,
        file_path,
        location=None,
        frame_range=None,
        frame_step=None,
        attribute=None,
        attribute_prefix=None,
        data_format=None,
        options=None,
    ):
        self._file_path = file_path
        self._locations = self._to_locations(location)
        
        self._star_frame, self._end_frame = _time.Frame.to_frame_range(frame_range)
        self._frame_step = frame_step
        self._attribute = attribute
        self._attribute_prefix = attribute_prefix
        self._option = copy.copy(self.DEFAULT_OPTIONS)
        if isinstance(options, dict):
            for k, v in options.items():
                if k in self.DEFAULT_OPTIONS:
                    self._option[k] = v
                else:
                    raise KeyError()
        self._data_format = data_format

        self._results = []

    @classmethod
    def _to_locations(cls, arg):
        if arg is not None:
            if isinstance(arg, six.string_types):
                return [_node_for_dag.DagNode.to_path(arg)]
            elif isinstance(arg, (tuple, list)):
                return list([_node_for_dag.DagNode.to_path(x) for x in arg])
            else:
                raise TypeError()
        return []

    @classmethod
    def _get_file_arg(cls, file_path):
        return '-{0} {1}'.format(cls.FILE, file_path.replace('\\', '/'))

    @classmethod
    def _get_options_arg(cls, options):
        if isinstance(options, dict):
            list_ = ['-{0}'.format(k) for k, v in options.items() if v is True]
            if list_:
                return ' '.join(list_)

    @classmethod
    def _get_data_format_arg(cls, data_format):
        if isinstance(data_format, six.string_types):
            if data_format in cls.DATA_FORMATS:
                return '-{0} {1}'.format(cls.DATA_FORMAT, data_format)
            return '-{0} {1}'.format(cls.DATA_FORMAT, cls.OGAWA)
        return '-{0} {1}'.format(cls.DATA_FORMAT, cls.OGAWA)

    @classmethod
    def _get_frame_range_arg(cls, start_frame, end_frame):
        return '-{0} {1} {2}'.format(cls.FRAME_RANGE, start_frame, end_frame)

    @classmethod
    def _get_frame_step_arg(cls, frame_step):
        if isinstance(frame_step, (int, float)):
            return '-{0} {1}'.format(cls.STEP, frame_step)

    @classmethod
    def _get_locations_arg(cls, location):
        list_ = cls._to_get_exists_paths(location)
        if list_:
            return ' '.join(['-{0} {1}'.format(cls.ROOT, i) for i in list_])

    @classmethod
    def _to_get_exists_paths(cls, obj_path_args):
        if isinstance(obj_path_args, six.string_types):
            if cmds.objExists(obj_path_args):
                return [cmds.ls(obj_path_args, long=1)[0]]
        elif isinstance(obj_path_args, (tuple, list)):
            return [cmds.ls(i, long=1)[0] for i in obj_path_args if cmds.objExists(i)]

    @classmethod
    def _to_strings(cls, string, includes=None):
        list_ = []
        if isinstance(string, six.string_types):
            if includes:
                if string in includes:
                    list_ = [string]
            else:
                list_ = [string]
        elif isinstance(string, (tuple, list)):
            for i in string:
                if includes:
                    if i in includes:
                        list_.append(i)
                else:
                    list_.append(i)
        return list_

    @classmethod
    def _get_attribute_arg(cls, attr_name):
        list_ = cls._to_strings(attr_name)
        #
        if list_:
            _ = ' '.join(['-{0} {1}'.format(cls.ATTR, i) for i in list_])
        else:
            _ = None
        return _

    @classmethod
    def _get_attribute_prefix_arg(cls, attr_name):
        list_ = cls._to_strings(attr_name)
        #
        if list_:
            _ = ' '.join(['-{0} {1}'.format(cls.ATTR_PREFIX, i) for i in list_])
        else:
            _ = None
        return _

    @staticmethod
    def _generate_j(js):
        _ = list(filter(None, js))
        if _:
            return ' '.join(_)

    @classmethod
    def _execute_cmd_script(cls, j):
        """
        :param j: str
        :return: None
        """
        cmds.loadPlugin(cls.PLUG_NAME, quiet=1)
        return cmds.AbcExport(j=j)

    def execute(self):
        js = [
            self._get_frame_range_arg(self._star_frame, self._end_frame),
            self._get_frame_step_arg(self._frame_step),
            self._get_attribute_arg(self._attribute),
            self._get_attribute_prefix_arg(self._attribute_prefix),
            self._get_options_arg(self._option),
            self._get_data_format_arg(self._data_format),
            self._get_locations_arg(self._locations),
            self._get_file_arg(self._file_path)
        ]

        file_opt = bsc_storage.StgFileOpt(self._file_path)
        directory_ = file_opt.directory
        if directory_.get_is_exists() is False:
            directory_.do_create()

        j = self._generate_j(js)
        if j:
            self._results = self._execute_cmd_script(j)
            bsc_log.Log.trace_method_result(
                'alembic export',
                'file="{}"'.format(file_opt.path)
            )
            if self._results:
                for i in self._results:
                    bsc_log.Log.trace_result(
                        'export ".abc": "{}"'.format(i)
                    )
        return self._results

    def get_outputs(self):
        return self._results


class AlembicNode:

    @classmethod
    def repath_to(cls, node, file_path):
        file_path_old = cls.get_file(node)
        if file_path_old != file_path:
            _attribute.NodeAttribute.set_as_string(
                node, 'abc_File', file_path
            )

    @classmethod
    def get_file(cls, node):
        return _attribute.NodeAttribute.get_as_string(node, 'abc_File')

    @classmethod
    def collection_to(cls, node, file_path):
        pass


class AlembicNodes:
    PLUG_NAME = 'AbcImport'
    NODE_TYPE_NAME = 'AlembicNode'

    @classmethod
    def get_all(cls):
        cmds.loadPlugin(cls.PLUG_NAME, quiet=1)
        return cmds.ls(
            type=cls.NODE_TYPE_NAME
        ) or []
