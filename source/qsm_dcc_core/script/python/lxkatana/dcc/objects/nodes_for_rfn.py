# coding:utf-8
import collections

import copy

import os

import parse

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core
# katana
from ... import core as ktn_core
# katana dcc
from . import node_for_rfn as ktn_dcc_obj_node_for_rfn

from . import nodes_for_look as ktn_dcc_obj_nodes_for_look


class AbsTextureReferences(object):
    OBJ_CLS_DICT = {
        'image': ktn_dcc_obj_node_for_rfn.TextureReference,
        'osl_file_path': ktn_dcc_obj_node_for_rfn.TextureReference,
        'osl_window_box': ktn_dcc_obj_node_for_rfn.TextureReference,
        'osl_window_box_s': ktn_dcc_obj_node_for_rfn.TextureReference,
        'jiWindowBox_Arnold': ktn_dcc_obj_node_for_rfn.TextureReference,
        #
        'custom': ktn_dcc_obj_node_for_rfn.FileReference,
    }
    PORT_PATHSEP = ktn_core.KtnUtil.PORT_PATHSEP
    OPTION = dict(
        with_reference=True
    )
    PORT_QUERY_DICT = {
        'image': [
            'parameters.filename'
        ],
        'osl_file_path': [
            'parameters.filename'
        ],
        'osl_window_box': [
            'parameters.filename'
        ],
        'osl_window_box_s': [
            'parameters.filename'
        ],
        'jiWindowBox_Arnold': [
            'parameters.filename'
        ]
    }
    EXPRESSION_PATTERNS_SRC = [
        # etc. "/temp/tx/texture_name.<udim>.%04d.tx'%(frame)"
        "'{base}'%{argument}",
        # etc. "extra.texture_directory+'/tx'+'/texture_name.<udim>.%04d.tx'%(frame)"
        "{extra}'{base}'%{argument}"
    ]
    EXPRESSION_PATTERN_TGT = '\'{file}\'%{argument}'

    def __init__(self, *args, **kwargs):
        self._raw = collections.OrderedDict()
        #
        self._option = copy.deepcopy(self.OPTION)
        if 'option' in kwargs:
            option = kwargs['option']
            if isinstance(option, dict):
                for k, v in option.items():
                    if k in self.OPTION:
                        self._option[k] = v

    def _get_obj_type_is_available_(self, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def _get_real_file_value(cls, port):
        ktn_port = port.ktn_port
        if ktn_port.isExpression() is True:
            e = ktn_port.getExpression()
            for i_pattern in cls.EXPRESSION_PATTERNS_SRC:
                i_p = parse.parse(
                    i_pattern, e
                )
                if i_p:
                    i_file_path_old = ktn_port.getValue(0)
                    i_base = i_p['base']
                    i_file_name = i_base.split('/')[-1]
                    i_file_path_new = '{}/{}'.format(
                        os.path.dirname(i_file_path_old), i_file_name
                    )
                    return i_file_path_new
        return ktn_port.getValue(0)

    @classmethod
    def _set_real_file_value(cls, port, file_path, remove_expression=False):
        file_path = str(file_path)
        ktn_port = port.ktn_port
        if ktn_port.isExpression() is True:
            e = ktn_port.getExpression()
            for i_pattern in cls.EXPRESSION_PATTERNS_SRC:
                i_p = parse.parse(
                    i_pattern, e
                )
                if i_p:
                    i_kwargs = dict(
                        file=file_path,
                        argument=i_p['argument']
                    )
                    i_e_new = cls.EXPRESSION_PATTERN_TGT.format(**i_kwargs)
                    if not e == i_e_new:
                        ktn_port.setExpression(i_e_new)
                        bsc_log.Log.trace_method_result(
                            'file repath',
                            u'attribute="{}", expression="{}"'.format(port.path, i_e_new)
                        )
                        return True
            #
            if remove_expression is True:
                ktn_port.setExpressionFlag(False)
                ktn_port.setValue(file_path, 0)
                bsc_log.Log.trace_method_result(
                    'file repath',
                    u'attribute="{}", file="{}"'.format(port.path, file_path)
                )
                return True
        else:
            v = ktn_port.getValue(0)
            if not v == file_path:
                ktn_port.setValue(file_path, 0)
                bsc_log.Log.trace_method_result(
                    'file repath',
                    u'attribute="{}", file="{}"'.format(port.path, file_path)
                )
                return True
        return False

    @classmethod
    def _get_expression_(cls, port):
        ktn_port = port.ktn_port
        if ktn_port.isExpression() is True:
            e = ktn_port.getExpression()
            if e:
                return e

    @classmethod
    def _set_real_file_path_by_atr_path_(cls, atr_path, file_path):
        atr_path_opt = bsc_core.PthAttributeOpt(atr_path)
        obj_path, port_path = atr_path_opt.obj_path, atr_path_opt.port_path
        obj_path_opt = bsc_core.PthNodeOpt(obj_path)
        obj_name = obj_path_opt.name
        ktn_obj_opt = ktn_core.NGNodeOpt(obj_name)
        shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
        obj_cls = cls._get_obj_cls(shader_type_name)
        obj = obj_cls(obj_path)
        port = obj.get_port(port_path)
        #
        cls._set_real_file_value(port, file_path)

    @classmethod
    def _get_obj_cls(cls, shader_type_name):
        if shader_type_name in cls.OBJ_CLS_DICT:
            return cls.OBJ_CLS_DICT[shader_type_name]
        return cls.OBJ_CLS_DICT['custom']

    def _set_customize_update_(self, paths_exclude=None, include_paths=None):
        objs = ktn_dcc_obj_nodes_for_look.AndShaders.get_objs()
        for i_obj in objs:
            i_obj_path = i_obj.path
            i_obj_type_name = i_obj.get_port('nodeType').get()
            # filter by include type
            if self._get_obj_type_is_available_(i_obj_type_name) is False:
                continue
            #
            if isinstance(paths_exclude, (tuple, list)):
                if i_obj_path in paths_exclude:
                    continue
            # filter by include
            if isinstance(include_paths, (tuple, list)):
                if i_obj_path not in include_paths:
                    continue
            #
            i_ktn_obj = i_obj.ktn_obj
            # filter by bypassed
            if i_ktn_obj.isBypassed() is True:
                continue
            #
            if i_obj_type_name in self.PORT_QUERY_DICT:
                i_port_paths = self.PORT_QUERY_DICT[i_obj_type_name]
                for j_port_path in i_port_paths:
                    j_enable = i_obj.get_port('{}.enable'.format(j_port_path)).get()
                    if j_enable:
                        if i_obj_path in self._raw:
                            j_file_reference_obj = self._raw[i_obj_path]
                        else:
                            j_obj_cls = self._get_obj_cls(i_obj_type_name)
                            j_file_reference_obj = j_obj_cls(i_obj_path)
                            self._raw[i_obj_path] = j_file_reference_obj
                        #
                        j_value_port_path = '{}.value'.format(j_port_path)
                        #
                        j_value_port = j_file_reference_obj.get_port(j_value_port_path)
                        j_value = self._get_real_file_value(j_value_port)
                        j_file_reference_obj.register_file(
                            j_value_port_path, j_value
                        )

    def get_objs(self, paths_exclude=None, include_paths=None):
        self._set_customize_update_(paths_exclude=paths_exclude, include_paths=include_paths)
        return self._raw.values()

    @classmethod
    def repath_fnc(cls, obj, port_path, file_path_new, remove_expression=False):
        cls._set_real_file_value(
            obj.get_port(port_path), file_path_new, remove_expression
        )


class TextureReferences(AbsTextureReferences):
    INCLUDE_TYPES = [
        'image',
        'osl_file_path',
        'osl_window_box',
        'osl_window_box_s',
        'jiWindowBox_Arnold'
    ]

    def __init__(self, *args, **kwargs):
        super(TextureReferences, self).__init__(*args, **kwargs)

    def _get_obj_type_is_available_(self, obj_type_name):
        return obj_type_name in self.INCLUDE_TYPES

    @classmethod
    def _set_obj_reference_update_(cls, obj):
        ktn_obj_opt = ktn_core.NGNodeOpt(bsc_core.PthNodeOpt(obj.path).name)
        shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
        if shader_type_name in cls.PORT_QUERY_DICT:
            port_keys = cls.PORT_QUERY_DICT[shader_type_name]
            obj.restore()
            for i_port_key in port_keys:
                i_port_path = '{}.value'.format(i_port_key)
                #
                i_port = obj.get_port(i_port_path)
                i_value = cls._get_real_file_value(i_port)
                #
                obj.register_file(
                    i_port_path, i_value
                )
