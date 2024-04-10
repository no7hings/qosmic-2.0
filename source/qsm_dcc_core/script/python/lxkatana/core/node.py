# coding:utf-8
import re

import fnmatch

import sys

import six

import lxcontent.core as ctt_core

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core
# katana
from .wrap import *

from . import base as ktn_cor_base


# noinspection PyUnusedLocal
class NGLayoutOpt(object):
    class Orientation(object):
        Horizontal = 'h'
        Vertical = 'v'

    class Direction(object):
        RightToLeft = 'r-l'
        LeftToRight = 'l-r'
        TopToBottom = 't-b'
        BottomToTop = 'b-t'

    def __init__(
            self, graph_data, scheme=(Orientation.Horizontal, Direction.RightToLeft, Direction.TopToBottom),
            size=(320, 80), option=None
    ):
        # branch_leaf_names_dict, leaf_branch_names_dict, size_dict, graph_dict
        self._branch_leaf_names_dict, self._leaf_branch_names_dict, self._size_dict, self._graph_dict = graph_data
        self._branch_leaf_names_dict = bsc_core.DictMtd.deduplication_value_to(self._branch_leaf_names_dict)
        self._leaf_branch_names_dict = bsc_core.DictMtd.deduplication_value_to(self._leaf_branch_names_dict)
        self._scheme = scheme
        self._size = size
        self._option = option or {}
        self._y_query_dict = self._get_y_query_()

    def _get_y_query_(self):
        dict_ = {}
        for i_key, i_data in self._size_dict.items():
            i_indices = i_data.keys()
            i_indices.sort()
            i_hs = [i_data[j] for j in i_indices]
            if i_key not in dict_:
                i_h_dict = {}
                dict_[i_key] = i_h_dict
            else:
                i_h_dict = dict_[i_key]
            #
            for j_index in i_indices:
                i_h_dict[j_index] = sum(i_hs[:j_index])
        return dict_

    def _layout_fnc_(self, name, position):
        #
        x, y = position
        i_atr = dict(
            x=x, y=y,
        )
        obj_opt = NGNodeOpt(name)
        i_atr_ = obj_opt.ktn_obj.getAttributes()
        i_atr_.update(i_atr)
        obj_opt.ktn_obj.setAttributes(i_atr_)
        if isinstance(self._option, dict):
            expanded = self._option.get('expanded')
            collapsed = self._option.get('collapsed')
            if expanded is True:
                obj_opt.set_shader_gui_expanded()
            #
            elif collapsed is True:
                obj_opt.set_shader_gui_collapsed()
            #
            shader_view_state = self._option.get('shader_view_state')
            if isinstance(shader_view_state, (int, float)):
                obj_opt.set_shader_view_state(float(shader_view_state))

    def _get_position_(self, x, y, w, h, root_index, branch_index, root_name, count, leaf_index):
        size_key = (root_index, root_name)
        y_dict = self._y_query_dict[size_key]
        ort, drt_h, drt_v = self._scheme
        if ort == self.Orientation.Horizontal:
            if drt_h == 'r-l':
                s_x = x-branch_index*w*2
            elif drt_h == 'l-r':
                s_x = x+branch_index*w*2
            else:
                raise ValueError()
            #
            if drt_v == 't-b':
                s_y = y+((count-(count%2))*h)/2
            elif drt_v == 'b-t':
                s_y = y-((count-(count%2))*h)/2
            else:
                raise ValueError()
            #
            j_x = s_x
            if drt_v == 't-b':
                j_y = s_y-leaf_index*h
            elif drt_v == 'b-t':
                j_y = s_y+leaf_index*h
            else:
                raise ValueError()
            return j_x, j_y
        elif ort == self.Orientation.Vertical:
            # _y = branch_index * h
            _y = y_dict[branch_index]
            if drt_v == 't-b':
                s_y_ = y-_y*2
            elif drt_v == 'b-t':
                s_y_ = y+_y*2
            else:
                raise ValueError()
            #
            if drt_h == 'r-l':
                s_x_ = x+((count-(count%2))*w)/2
            elif drt_h == 'l-r':
                s_x_ = x-((count-(count%2))*w)/2
            else:
                raise ValueError()
            #
            j_y_ = s_y_
            if drt_h == 'r-l':
                j_x_ = s_x_-leaf_index*w
            elif drt_h == 'l-r':
                j_x_ = s_x_+leaf_index*w
            else:
                raise ValueError()
            return j_x_, j_y_

    def _get_leaf_branch_name_(self, root_index, leaf_branch_names):
        for i_leaf_branch_name in leaf_branch_names:
            i_leaf_branch_key = (root_index, i_leaf_branch_name)
            i_branch_leaf_names = self._branch_leaf_names_dict.get(i_leaf_branch_key, set())
            if len(i_branch_leaf_names) > 1:
                return None

        c = len(leaf_branch_names)
        mid = int(c/2)
        return leaf_branch_names[mid]

    def run(self, depth_maximum=-1):
        if not self._graph_dict:
            return
        #
        use_one_by_one = self._option.get('use_one_by_one', False)
        #
        w, h = self._size
        ort, drt_h, drt_v = self._scheme
        #
        position_dict = {}
        keys = self._graph_dict.keys()
        keys.sort()
        for i_key in keys:
            i_data = self._graph_dict[i_key]
            i_root_index, i_branch_index, i_root_name = i_key
            if i_root_index > 0:
                # node is in group, use origin
                x, y = 0, 0
            else:
                x, y = NGNodeOpt(i_root_name).get_position()
            #
            if i_data:
                i_count = len(i_data)
                for j_leaf_index, j_leaf_name in enumerate(i_data):
                    j_x, j_y = self._get_position_(
                        x, y, w, h, i_root_index, i_branch_index, i_root_name, i_count, j_leaf_index
                    )
                    # check tree is one branch and one leaf in current root
                    j_leaf_key = (i_root_index, j_leaf_name)
                    j_leaf_branch_names = self._leaf_branch_names_dict[j_leaf_key]
                    j_c = len(j_leaf_branch_names)
                    if use_one_by_one is True:
                        if j_c == 1:
                            j_leaf_branch_name = j_leaf_branch_names[0]
                            j_leaf_branch_key = (i_root_index, j_leaf_branch_name)
                            j_branch_leaf_names = self._branch_leaf_names_dict.get(j_leaf_branch_key, set())
                            if len(j_branch_leaf_names) == 1:
                                if j_leaf_branch_key in position_dict:
                                    j_x_, j_y_ = position_dict[j_leaf_branch_key]
                                    if ort == self.Orientation.Horizontal:
                                        j_y = j_y_
                                    elif ort == self.Orientation.Vertical:
                                        j_x = j_x_
                        else:
                            j_leaf_branch_name = self._get_leaf_branch_name_(i_root_index, j_leaf_branch_names)
                            if j_leaf_branch_name is not None:
                                j_leaf_branch_key = (i_root_index, j_leaf_branch_name)
                                if j_leaf_branch_key in position_dict:
                                    j_x_, j_y_ = position_dict[j_leaf_branch_key]
                                    if ort == self.Orientation.Horizontal:
                                        j_y = j_y_
                                    elif ort == self.Orientation.Vertical:
                                        j_x = j_x_
                    #
                    position_dict[j_leaf_key] = (j_x, j_y)
        #
        if position_dict:
            for k, v in position_dict.items():
                i_root_index, i_name = k
                i_position = v
                self._layout_fnc_(i_name, i_position)


# noinspection PyUnusedLocal
class NGNodesMtd(object):
    class MatchMode(object):
        One = 0
        All = 1

    @classmethod
    def find_nodes(cls, type_name, ignore_bypassed=False):
        _ = NodegraphAPI.GetAllNodesByType(type_name) or []
        if ignore_bypassed is False:
            return _
        return [i for i in _ if NGNodeOpt(i).get_is_bypassed(ancestors=True) is False]

    @classmethod
    def filter_fnc(cls, nodes, filters):
        list_ = []
        for i in nodes:
            if filters:
                i_c = len(filters)
                i_results = []
                for j_f_p, j_f_o, j_f_v in filters:
                    if j_f_p == 'node_type':
                        j_v = i.getType()
                    elif j_f_p == 'node_name':
                        j_v = i.getName()
                    elif j_f_p == 'bypassed':
                        j_v = i.isBypassed()
                    else:
                        j_p = i.getParameter(j_f_p)
                        if j_p is None:
                            continue
                        j_v = j_p.getValue(0)
                    #
                    if j_f_o == 'in':
                        j_r = j_v in j_f_v
                    elif j_f_o == 'is':
                        j_r = j_v == j_f_v
                    else:
                        raise RuntimeError()
                    #
                    if j_r is True:
                        i_results.append(1)
                    else:
                        break
                #
                if sum(i_results) == i_c:
                    list_.append(i)
        return list_

    @classmethod
    def filter_nodes(cls, filters, ignore_bypassed=False):
        return cls.filter_fnc(NodegraphAPI.GetAllNodes(), filters)


# noinspection PyUnusedLocal
class NGNodeOpt(object):
    PATHSEP = '/'
    PORT_PATHSEP = '.'

    @classmethod
    def _get_path_(cls, name):
        def _rcs_fnc(name_):
            _ktn_obj = NodegraphAPI.GetNode(name_)
            if _ktn_obj is not None:
                _parent = _ktn_obj.getParent()
                if _parent is None:
                    list_.append('')
                else:
                    _parent_name = _parent.getName()
                    list_.append(_parent_name)
                    _rcs_fnc(_parent_name)

        #
        list_ = [name]
        _rcs_fnc(name)
        list_.reverse()
        return cls.PATHSEP.join(list_)

    @classmethod
    def _set_create_(cls, path, type_name):
        path_opt = bsc_core.PthNodeOpt(path)
        name = path_opt.name
        parent_opt = path_opt.get_parent()
        parent_name = parent_opt.get_name()
        ktn_obj = NodegraphAPI.GetNode(name)
        if ktn_obj is None:
            parent = cls(parent_name)
            parent_ktn_obj = parent.ktn_obj
            if parent_ktn_obj is not None:
                ktn_obj = NodegraphAPI.CreateNode(type_name, parent_ktn_obj)
                if ktn_obj is None:
                    raise RuntimeError('type="{}" is unknown'.format(type_name))
                #
                name_ktn_port = ktn_obj.getParameter('name')
                if name_ktn_port is not None:
                    name_ktn_port.setValue(str(name), 0)
                #
                ktn_obj.setName(name)
                return ktn_obj
            else:
                raise RuntimeError('obj="{}" is non-exists'.format(parent_name))
        return ktn_obj

    @classmethod
    def _get_is_parent_for_(cls, parent_ktn_obj, child_ktn_obj):
        return child_ktn_obj.getParent().getName() == parent_ktn_obj.getName()

    @classmethod
    def _generate_node_create_args(cls, path, type_name):
        path_opt = bsc_core.PthNodeOpt(path)
        name = path_opt.name
        parent_opt = path_opt.get_parent()
        parent_name = parent_opt.get_name()
        ktn_obj = NodegraphAPI.GetNode(name)
        if ktn_obj is None:
            parent = cls(parent_name)
            parent_ktn_obj = parent.ktn_obj
            if parent_ktn_obj is not None:
                ktn_obj = NodegraphAPI.CreateNode(type_name, parent_ktn_obj)
                if ktn_obj is None:
                    raise RuntimeError('type="{}" is unknown'.format(type_name))
                #
                name_ktn_port = ktn_obj.getParameter('name')
                if name_ktn_port is not None:
                    name_ktn_port.setValue(str(name), 0)
                #
                if hasattr(ktn_obj, 'checkDynamicParameters'):
                    ktn_obj.checkDynamicParameters()
                #
                ktn_obj.setName(name)
                return ktn_obj, True
            else:
                raise RuntimeError('obj="{}" is non-exists'.format(parent_name))
        return ktn_obj, False

    @classmethod
    def _generate_group_child_create_args(cls, path, type_name):
        path_opt = bsc_core.PthNodeOpt(path)
        name = path_opt.name
        parent_opt = path_opt.get_parent()
        parent_name = parent_opt.get_name()
        ktn_obj = NodegraphAPI.GetNode(name)
        if ktn_obj is None:
            parent = cls(parent_name)
            parent_ktn_obj = parent.ktn_obj
            if parent_ktn_obj is not None:
                if parent_ktn_obj.getType() in ['GroupStack']:
                    ktn_obj = NodegraphAPI.CreateNode(type_name, parent_ktn_obj)
                    if ktn_obj is None:
                        raise RuntimeError('type="{}" is unknown'.format(type_name))
                    #
                    parent_ktn_obj.buildChildNode(ktn_obj)
                    #
                    name_ktn_port = ktn_obj.getParameter('name')
                    if name_ktn_port is not None:
                        name_ktn_port.setValue(str(name), 0)
                    ktn_obj.setName(name)
                    return ktn_obj, True
                elif parent_ktn_obj.getType() in ['GroupMerge']:
                    ktn_obj = NodegraphAPI.CreateNode(type_name, parent_ktn_obj)
                    if ktn_obj is None:
                        raise RuntimeError('type="{}" is unknown'.format(type_name))
                    #
                    parent_ktn_obj.buildChildNode(ktn_obj)
                    #
                    name_ktn_port = ktn_obj.getParameter('name')
                    if name_ktn_port is not None:
                        name_ktn_port.setValue(str(name), 0)
                    ktn_obj.setName(name)
                    return ktn_obj, True
            else:
                raise RuntimeError('obj="{}" is non-exists'.format(parent_name))
        return ktn_obj, False

    @classmethod
    def _generate_material_node_graph_create_args(cls, path, type_name, shader_type_name=None):
        path_opt = bsc_core.PthNodeOpt(path)
        name = path_opt.name
        parent_opt = path_opt.get_parent()
        parent_name = parent_opt.get_name()
        ktn_obj = NodegraphAPI.GetNode(name)
        if ktn_obj is None:
            parent_opt = cls(parent_name)
            if type_name in {'NetworkMaterial'}:
                materials_exists = parent_opt.get_children(type_includes=['NetworkMaterial'])
                # when had default "NetworkMaterial" auto rename exists to new name
                if len(materials_exists) == 1:
                    material_default = materials_exists[0]
                    if fnmatch.filter([material_default.getName()], 'NetworkMaterial*'):
                        cls(material_default).set_rename(name)
                        return material_default, True
                    else:
                        parent_opt._ktn_obj.addNetworkMaterialNode()
                else:
                    parent_opt._ktn_obj.addNetworkMaterialNode()
                #
                materials_exists = parent_opt.get_children(type_includes=['NetworkMaterial'])
                material_new = materials_exists[-1]
                material_new_opt = cls(material_new)
                # auto layout new material
                # material_new_opt.set_position(
                #     0, -(len(materials_exists))-1*320
                # )
                material_new_opt.set_rename(name)
                return material_new, True
            elif type_name in {'ArnoldShadingNode'}:
                return cls._generate_shader_create_args(path, type_name, shader_type_name)
            return ktn_obj, True
        return ktn_obj, False

    @classmethod
    def _generate_shader_create_args(cls, path, type_name, shader_type_name=None):
        ktn_obj, is_create = cls._generate_node_create_args(path, type_name)
        if is_create is True:
            type_ktn_port = ktn_obj.getParameter('nodeType')
            if type_ktn_port is not None:
                type_ktn_port.setValue(str(shader_type_name), 0)
                ktn_obj.checkDynamicParameters()
        return ktn_obj, is_create

    @classmethod
    def _generate_usd_shader_create_args(cls, path, shader_type_name):
        ktn_obj, is_create = cls._generate_node_create_args(path, 'UsdShadingNode')
        if is_create is True:
            type_ktn_port = ktn_obj.getParameter('nodeType')
            if type_ktn_port is not None:
                type_ktn_port.setValue(str(shader_type_name), 0)
                ktn_obj.checkDynamicParameters()
        return ktn_obj, is_create

    @classmethod
    def _create_connections_by_data(
        cls,
        connections_data,
        extend_kwargs=None,
        auto_create_source=False,
        auto_create_target=False,
        ignore_non_exists=False,
    ):
        """
        :param connections_data: etc. [
            'node_a.a.b',
            'node_b.a.b'
        ]
        :return:
        """
        for seq, i in enumerate(connections_data):
            if not (seq+1)%2:
                i_source_attr_path = connections_data[seq-1]
                i_target_attr_path = i
                if isinstance(extend_kwargs, dict):
                    i_source_attr_path = i_source_attr_path.format(**extend_kwargs)
                    i_target_attr_path = i_target_attr_path.format(**extend_kwargs)
                #
                i_args_src = i_source_attr_path.split('.')
                i_obj_path_src, i_port_path_src = i_args_src[0], '.'.join(i_args_src[1:])
                i_args_tgt = i_target_attr_path.split('.')
                i_obj_path_tgt, i_port_path_tgt = i_args_tgt[0], '.'.join(i_args_tgt[1:])
                #
                i_obj_src = cls._generate_ktn_obj(i_obj_path_src)
                if i_obj_src is None:
                    if ignore_non_exists is True:
                        return False
                    raise RuntimeError(
                        'node: "{}" is non-exists'.format(i_obj_path_src)
                    )
                #
                i_obj_tgt = cls._generate_ktn_obj(i_obj_path_tgt)
                if i_obj_tgt is None:
                    if ignore_non_exists is True:
                        return False
                    raise RuntimeError(
                        'node: "{}" is non-exists'.format(i_obj_path_tgt)
                    )
                #
                if i_obj_src.getName() == i_obj_tgt.getName():
                    source_fnc, target_fnc = 'getSendPort', 'getReturnPort'
                else:
                    i_condition = (
                        cls._get_is_parent_for_(i_obj_src, i_obj_tgt), cls._get_is_parent_for_(i_obj_tgt, i_obj_src)
                    )
                    # same index
                    if i_condition == (False, False):
                        source_fnc, target_fnc = 'getOutputPort', 'getInputPort'
                    # parent to children
                    elif i_condition == (True, False):
                        source_fnc, target_fnc = 'getSendPort', 'getInputPort'
                    # children to parent
                    elif i_condition == (False, True):
                        source_fnc, target_fnc = 'getOutputPort', 'getReturnPort'
                    else:
                        raise RuntimeError()
                #
                i_port_src = i_obj_src.__getattribute__(source_fnc)(i_port_path_src)
                if i_port_src is None:
                    if auto_create_source is True:
                        if source_fnc == 'getOutputPort':
                            i_port_src = i_obj_src.addOutputPort(i_port_path_src)
                        elif source_fnc == 'getSendPort':
                            i_obj_src.addInputPort(i_port_path_src)
                            i_port_src = i_obj_src.__getattribute__(source_fnc)(i_port_path_src)
                        else:
                            raise RuntimeError()
                    else:
                        raise RuntimeError(
                            'method="{}", attribute="{}" is non-exists'.format(source_fnc, i_source_attr_path)
                        )
                #
                i_port_tgt = i_obj_tgt.__getattribute__(target_fnc)(i_port_path_tgt)
                if i_port_tgt is None:
                    if auto_create_target is True:
                        if target_fnc == 'getInputPort':
                            i_port_tgt = i_obj_tgt.addInputPort(i_port_path_tgt)
                        elif target_fnc == 'getReturnPort':
                            i_obj_tgt.addOutputPort(i_port_path_tgt)
                            i_port_tgt = i_obj_tgt.__getattribute__(target_fnc)(i_port_path_tgt)
                        else:
                            raise RuntimeError()
                    else:
                        raise RuntimeError(
                            'method="{}", attribute="{}" is non-exists'.format(target_fnc, i_target_attr_path)
                        )
                #
                i_port_src.connect(
                    i_port_tgt
                )

    @classmethod
    def _get_is_exists_(cls, string_arg):
        return cls._generate_ktn_obj(string_arg) is not None

    @classmethod
    def _generate_ktn_obj(cls, string_arg):
        if string_arg.startswith(cls.PATHSEP):
            return NodegraphAPI.GetNode(
                bsc_core.PthNodeOpt(string_arg).get_name()
            )
        else:
            return NodegraphAPI.GetNode(string_arg)

    def __init__(self, ktn_obj):
        if isinstance(ktn_obj, six.string_types):
            if ktn_obj.startswith(self.PATHSEP):
                self._ktn_obj = NodegraphAPI.GetNode(
                    bsc_core.PthNodeOpt(ktn_obj).get_name()
                )
            else:
                self._ktn_obj = NodegraphAPI.GetNode(ktn_obj)
        else:
            self._ktn_obj = ktn_obj

    def get_ktn_obj(self):
        return self._ktn_obj

    ktn_obj = property(get_ktn_obj)

    def get_type(self):
        return self.ktn_obj.getType()

    type = property(get_type)

    def get_type_name(self):
        return self.get_type()

    type_name = property(get_type_name)

    def get_is(self, type_arg):
        if isinstance(type_arg, six.string_types):
            return self.get_type_name() == type_arg
        elif isinstance(type_arg, (set, tuple, list)):
            return self.get_type_name() in type_arg
        raise TypeError(
            'type_args must be a string or list'
        )

    def get_shader_type_name(self):
        return self.get('nodeType')

    shader_type_name = property(get_shader_type_name)

    def get_path(self):
        return self._get_path_(self.get_name())

    path = property(get_path)

    def get_name(self):
        return self._ktn_obj.getName()

    name = property(get_name)

    def set_rename(self, new_name):
        if isinstance(new_name, unicode):
            new_name = str(new_name)
        #
        name_ktn_port = self._ktn_obj.getParameter('name')
        if name_ktn_port is not None:
            name_ktn_port.setValue(new_name, 0)
        self._ktn_obj.setName(new_name)

    def set_shader_gui_expanded(self):
        attributes = self.ktn_obj.getAttributes()
        if 'ns_expandedPages' in attributes and 'ns_collapsedPages' in attributes:
            attributes['ns_expandedPages'] = 'Outputs##BUILTIN | Parameters##BUILTIN | '
            attributes['ns_collapsedPages'] = 'Outputs | Parameters | '
            self.ktn_obj.setAttributes(attributes)

    def set_shader_gui_collapsed(self):
        attributes = self.ktn_obj.getAttributes()
        if 'ns_expandedPages' in attributes:
            attributes['ns_expandedPages'] = 'Outputs | Parameters | '
            attributes['ns_collapsedPages'] = 'Outputs##BUILTIN | Parameters##BUILTIN | '
            self.ktn_obj.setAttributes(attributes)

    def set_shader_view_state(self, value):
        self.set_attributes(dict(ns_viewState=value))

    def get_sources(self, **kwargs):
        list_ = []
        _ = self.ktn_obj.getInputPorts() or []
        for i_ktn_port in _:
            i_ktn_ports_src = i_ktn_port.getConnectedPorts()
            if i_ktn_ports_src:
                list_.extend(i_ktn_ports_src)
        return list_

    def get_source_objs(self, **kwargs):
        list_ = []
        if 'inner' in kwargs:
            _ = self._get_sources_inner_(self._ktn_obj)
        else:
            _ = self.get_sources(**kwargs)
        for i_ktn_port in _:
            i_ktn_obj = i_ktn_port.getNode()
            if i_ktn_obj not in list_:
                list_.append(i_ktn_obj)
        return list_

    @classmethod
    def _get_sources_inner_(cls, ktn_obj):
        list_ = []
        _ = ktn_obj.getOutputPorts() or []
        for i_ktn_port in _:
            i_ktn_ports_rtn = ktn_obj.getReturnPort(i_ktn_port.getName())
            i_ktn_ports_src = i_ktn_ports_rtn.getConnectedPorts()
            if i_ktn_ports_src:
                list_.extend(i_ktn_ports_src)
        return list_

    @classmethod
    def _get_source_objs_inner_(cls, ktn_obj):
        list_ = []
        _ = cls._get_sources_inner_(ktn_obj)
        for i_ktn_port in _:
            i_ktn_obj = i_ktn_port.getNode()
            if i_ktn_obj not in list_:
                list_.append(i_ktn_obj)
        return list_

    def get_all_source_objs(self, **kwargs):
        def rcs_fnc_(list__, ktn_obj_):
            _ktn_objs = self.__class__(ktn_obj_).get_source_objs(**kwargs)
            for _i_ktn_obj in _ktn_objs:
                if _i_ktn_obj not in list__:
                    if hasattr(_i_ktn_obj, 'getChildren'):
                        _i_ktn_objs = self._get_source_objs_inner_(_i_ktn_obj)
                        for _j_ktn_obj in _i_ktn_objs:
                            if _j_ktn_obj not in list__:
                                list__.append(_j_ktn_obj)
                                rcs_fnc_(list__, _j_ktn_obj)
                    else:
                        list__.append(_i_ktn_obj)
                        rcs_fnc_(list__, _i_ktn_obj)

        #
        inner = kwargs.get('inner', False)
        #
        list_ = []
        rcs_fnc_(list_, self._ktn_obj)
        return list_

    def get_all_source_objs_(self, **kwargs):
        def rcs_fnc_(ktn_obj_, root_name_, root_index_, branch_index_):
            if skip_base_type_names:
                base_type_name = ktn_obj_.getBaseType()
                if base_type_name in skip_base_type_names:
                    return
            #
            if hasattr(ktn_obj_, 'getChildren'):
                outer_fnc_(ktn_obj_, root_name_, root_index_, branch_index_)
                # inner
                if inner is True:
                    # reset start to 0
                    _root_name = ktn_obj_.getName()
                    if _root_name not in exclude_names:
                        inner_fnc_(ktn_obj_, _root_name, root_index_, branch_index_)
            else:
                outer_fnc_(ktn_obj_, root_name_, root_index_, branch_index_)

        #
        def outer_fnc_(ktn_obj_, root_name_, root_index_, branch_index_):
            _source_ktn_objs = self.__class__(ktn_obj_).get_source_objs()
            #
            if _source_ktn_objs:
                branch_index_ += 1
                add_fnc_(_source_ktn_objs, root_name_, root_index_, branch_index_)

        #
        def inner_fnc_(ktn_obj_, root_name_, root_index_, branch_index_):
            root_index_ += 1
            #
            _source_ktn_objs = self._get_source_objs_inner_(ktn_obj_)
            if _source_ktn_objs:
                branch_index_ += 1
                add_fnc_(_source_ktn_objs, root_name_, root_index_, branch_index_)

        #
        def add_fnc_(ktn_objs_, root_name_, root_index_, branch_index_):
            for _i_sub_index, _i_ktn_obj in enumerate(ktn_objs_):
                _i_leaf_name = _i_ktn_obj.getName()
                if _i_leaf_name not in index_dict_:
                    index_dict_[_i_leaf_name] = (root_index_, branch_index_, _i_sub_index, len(index_dict_))
                    rcs_fnc_(_i_ktn_obj, root_name_, root_index_, branch_index_)

        #
        name = self._ktn_obj.getName()
        exclude_names = [
            name,
        ]
        if self._ktn_obj.getParent():
            exclude_names.append(self._ktn_obj.getParent().getName())
        #
        index_dict_ = {
            name: (0, 0, 0, 0)
        }
        inner = kwargs.get('inner', False)
        skip_base_type_names = kwargs.get('skip_base_type_names', [])
        type_includes = kwargs.get('type_includes', [])
        rcs_fnc_(self._ktn_obj, name, 0, 0)
        list_ = bsc_core.DictMtd.sort_key_by_value_to(index_dict_).keys()
        list_.reverse()
        if type_includes:
            _ = [i for i in list_ if NodegraphAPI.GetNode(i).getType() in type_includes]
            return _
        return list_

    def get_gui_layout_data(self, **kwargs):
        def rcs_fnc_(ktn_obj_, root_name_, root_index_, branch_index_):
            if skip_base_type_names:
                base_type_name = ktn_obj_.getBaseType()
                if base_type_name in skip_base_type_names:
                    return
            if hasattr(ktn_obj_, 'getChildren'):
                _branch_name = ktn_obj_.getName()
                outer_fnc_(ktn_obj_, root_name_, _branch_name, root_index_, branch_index_)
                # inner
                if inner is True:
                    # reset start to 0
                    _root_name = ktn_obj_.getName()
                    _start_index = 0
                    inner_fnc_(ktn_obj_, _root_name, _branch_name, root_index_, _start_index)
            else:
                _branch_name = ktn_obj_.getName()
                outer_fnc_(ktn_obj_, root_name_, _branch_name, root_index_, branch_index_)

        def outer_fnc_(ktn_obj_, root_name_, branch_name_, root_index_, branch_index_):
            _source_ktn_objs = self.__class__(ktn_obj_).get_source_objs()
            #
            if _source_ktn_objs:
                branch_index_ += 1
                add_fnc_(_source_ktn_objs, root_name_, branch_name_, root_index_, branch_index_)

        def inner_fnc_(ktn_obj_, root_name_, branch_name_, root_index_, branch_index_):
            root_index_ += 1
            #
            _source_ktn_objs = self._get_source_objs_inner_(ktn_obj_)
            if _source_ktn_objs:
                branch_index_ += 1
                add_fnc_(_source_ktn_objs, root_name_, branch_name_, root_index_, branch_index_)

        def add_fnc_(ktn_objs_, root_name_, branch_name_, root_index_, branch_index_):
            _graph_key_cur = (root_index_, branch_index_, root_name_)
            _size_key_cur = (root_index_, root_name_)
            #
            if _size_key_cur not in size_dict:
                _h_in_cur = {}
                size_dict[_size_key_cur] = _h_in_cur
            else:
                _h_in_cur = size_dict[_size_key_cur]
            #
            if _graph_key_cur not in graph_dict:
                _graph_data_in_cur = []
                graph_dict[_graph_key_cur] = _graph_data_in_cur
            else:
                _graph_data_in_cur = graph_dict[_graph_key_cur]
            #
            _branch_key = (root_index_, branch_name_)
            for _i_sub_index, _i_ktn_obj in enumerate(ktn_objs_):
                _i_ktn_obj_opt = NGNodeOpt(_i_ktn_obj)
                _i_type_name = _i_ktn_obj.getType()
                _i_leaf_name = _i_ktn_obj.getName()
                _i_w = _i_ktn_obj_opt.get('gui_layout.size.w') or w
                _i_h = _i_ktn_obj_opt.get('gui_layout.size.h') or h
                #
                if branch_index_ in _h_in_cur:
                    _i_h_pre = _h_in_cur[branch_index_]
                    if _i_h > _i_h_pre:
                        _h_in_cur[branch_index_] = _i_h
                else:
                    _h_in_cur[branch_index_] = _i_h
                #
                _i_branch_index_key_cur = (root_index_, _i_leaf_name)
                if _i_branch_index_key_cur not in leaf_branch_name_dict:
                    leaf_branch_name_dict[_i_branch_index_key_cur] = branch_name_
                #
                _i_graph_key_cur = _graph_key_cur
                # break the self-cycle
                if _i_leaf_name != root_name_:
                    # try move to end
                    _i_leaf_key = (root_index_, _i_leaf_name)
                    leaf_branch_names_dict.setdefault(
                        _i_leaf_key, []
                    ).append(branch_name_)
                    branch_leaf_names_dict.setdefault(
                        _branch_key, []
                    ).append(_i_leaf_name)
                    if _i_leaf_key in leaf_branch_index_dict:
                        _i_branch_index_cur = branch_index_
                        _i_index_pre = leaf_branch_index_dict[_i_leaf_key]
                        if _i_index_pre < _i_branch_index_cur:
                            _i_graph_key_pre = (root_index_, _i_index_pre, root_name_)
                            if _i_graph_key_pre in graph_dict:
                                _graph_data_in_index_pre = graph_dict[_i_graph_key_pre]
                                _graph_data_in_index_pre.remove(_i_leaf_name)
                                _graph_data_in_cur.append(_i_leaf_name)
                                leaf_branch_index_dict[_i_leaf_key] = _i_branch_index_cur
                    else:
                        leaf_branch_index_dict[_i_leaf_key] = branch_index_
                        #
                        _graph_data_in_cur.append(_i_leaf_name)
                    #
                    rcs_fnc_(_i_ktn_obj, root_name_, root_index_, branch_index_)

        inner = kwargs.get('inner', False)
        skip_base_type_names = kwargs.get('skip_base_type_names', [])
        w, h = kwargs.get('size', [320, 40])
        #
        leaf_branch_name_dict = {
            # (root_index, leaf_name): branch_name
        }
        #
        branch_leaf_names_dict = {
            # (root_index, branch_name): [leaf_name, ...]
        }
        leaf_branch_names_dict = {
            # (root_index, leaf_name): [branch_name, ...]
        }
        #
        leaf_branch_index_dict = {
            # (root_index, leaf_name): branch_index
        }
        size_dict = {

        }
        graph_dict = {
            # (root_index, branch_index, root_name): [name, ...]
        }
        #
        name = self._ktn_obj.getName()
        start_depth = 0
        start_index = 0
        #
        rcs_fnc_(self._ktn_obj, name, start_depth, start_index)
        return branch_leaf_names_dict, leaf_branch_names_dict, size_dict, graph_dict

    @ktn_cor_base.Modifier.undo_run
    def gui_layout_shader_graph(
        self,
        scheme=(
            NGLayoutOpt.Orientation.Horizontal,
            NGLayoutOpt.Direction.RightToLeft,
            NGLayoutOpt.Direction.TopToBottom
        ),
        size=(320, 80), expanded=False, collapsed=False, shader_view_state=None
    ):
        graph_dara = self.get_gui_layout_data(
            inner=True,
            size=size
        )
        #
        NGLayoutOpt(
            graph_dara,
            scheme=scheme,
            size=size,
            option=dict(
                expanded=expanded,
                collapsed=collapsed,
                shader_view_state=shader_view_state,
                # use_one_by_one=True
            )
        ).run()

    @ktn_cor_base.Modifier.undo_run
    def gui_layout_node_graph(
        self,
        scheme=(
            NGLayoutOpt.Orientation.Vertical,
            NGLayoutOpt.Direction.LeftToRight,
            NGLayoutOpt.Direction.BottomToTop
        ),
        size=(320, 40)
    ):
        graph_dara = self.get_gui_layout_data(
            inner=True,
            size=size,
            skip_base_type_names=['SuperTool']
        )
        NGLayoutOpt(
            graph_dara,
            scheme=scheme,
            size=size,
            option=dict(
                use_one_by_one=True
            )
        ).run()

    def get_port_is_exists(self, port_path):
        return self.ktn_obj.getParameter(port_path) is not None

    def get_port_raw(self, port_path):
        port = self.ktn_obj.getParameter(port_path)
        if port:
            return NGPortOpt(port).get()

    def set_port_raw(self, port_path, raw, ignore_changed=False):
        p = self.ktn_obj.getParameter(port_path)
        if p:
            NGPortOpt(p).set(raw)

    def set(self, key, value, ignore_changed=False):
        key = key.replace('/', '.')
        self.set_port_raw(key, value, ignore_changed)

    def get(self, key):
        key = key.replace('/', '.')
        return self.get_port_raw(key)

    def set_parameters_by_data(self, data, extend_kwargs=None):
        for i_port_path, i_args in data.items():
            #
            i_port_path = i_port_path.replace('/', '.')
            #
            i_p = self.ktn_obj.getParameter(i_port_path)
            if i_p is None:
                raise RuntimeError(
                    bsc_log.Log.trace_warning(
                        'port="{}" is non-exists'.format(i_port_path)
                    )
                )
            #
            i_value = i_args
            if isinstance(i_args, dict):
                #
                i_size = i_args.get('size')
                if i_size is not None:
                    i_p.resizeArray(i_size)
                #
                i_tuple_size = i_args.get('tuple_size')
                if i_tuple_size is not None:
                    i_p.setTupleSize(i_tuple_size)
                #
                i_value = i_args.get('value')
                if i_value is None:
                    return
            #
            if isinstance(extend_kwargs, dict):
                if isinstance(i_value, (unicode, str)):
                    i_value = i_value.format(**extend_kwargs)
            # turn off the expression-flag
            if self.get_is_expression(i_port_path) is True:
                self.set_expression_enable(i_port_path, False)
            #
            self.set(i_port_path, i_value)

    def set_proxy_parameters_by_data(self, data, extend_kwargs=None):
        for i_port_path, i_data in data.items():
            #
            i_port_path = i_port_path.replace('/', '.')
            #
            i_p = self.ktn_obj.getParameter(i_port_path)
            if i_p is None:
                raise RuntimeError(
                    bsc_log.Log.trace_warning(
                        'port="{}" is non-exists'.format(i_port_path)
                    )
                )
            self.set_for_proxy(i_port_path, i_data, extend_kwargs)

    def set_for_proxy(self, key, data, extend_kwargs):
        port = self.ktn_obj.getParameter(key)
        if port:
            _ = NGPortOpt(port).get()
            if _:
                name = _.split('.')[0]
                NGNodeOpt(name).set_parameters_by_data(
                    data, extend_kwargs
                )

    def set_shader_parameters_by_data(self, data, extend_kwargs=None):
        """
        :param data: {
            <port_path>: <value>
        }
        :param extend_kwargs:
        :return:
        """
        for i_port_path, i_value in data.items():
            #
            i_port_path = i_port_path.replace('/', '.')
            if isinstance(extend_kwargs, dict):
                if isinstance(i_value, (unicode, str)):
                    i_value = i_value.format(**extend_kwargs)
            # turn on enable first
            i_enable_key = 'parameters.{}.enable'.format(i_port_path)
            self.set(i_enable_key, True)
            #
            i_value_key = 'parameters.{}.value'.format(i_port_path)
            # turn off the expression-flag
            if self.get_is_expression(i_value_key) is True:
                self.set_expression_enable(i_value_key, False)
            #
            self.set(i_value_key, i_value)

    def set_arnold_geometry_properties_by_data(self, data, extend_kwargs=None):
        convert_dict = dict(
            subdiv_iterations='iterations',
            disp_zero_value='zero_value'
        )
        for i_port_path, i_value in data.items():
            i_port_path = i_port_path.replace('/', '.')
            #
            if i_port_path in convert_dict:
                i_port_path = convert_dict[i_port_path]
            if isinstance(extend_kwargs, dict):
                if isinstance(i_value, (unicode, str)):
                    i_value = i_value.format(**extend_kwargs)
            #
            i_enable_key = 'args.arnoldStatements.{}.enable'.format(i_port_path)
            self.set(i_enable_key, True)
            #
            i_value_key = 'args.arnoldStatements.{}.value'.format(i_port_path)
            # turn off the expression-flag
            if self.get_is_expression(i_value_key) is True:
                self.set_expression_enable(i_value_key, False)
            self.set(i_value_key, i_value)

    def set_expressions_by_data(self, data, extend_kwargs=None):
        for i_port_path, i_expression in data.items():
            i_port_path = i_port_path.replace('/', '.')
            #
            i_p = self.ktn_obj.getParameter(i_port_path)
            if i_p is None:
                raise RuntimeError(
                    bsc_log.Log.trace_warning(
                        'port="{}" is non-exists'.format(i_port_path)
                    )
                )
            #
            if isinstance(extend_kwargs, dict):
                if isinstance(i_expression, (unicode, str)):
                    i_expression = i_expression.format(**extend_kwargs)
            #
            self.set_expression_enable(i_port_path, True)
            self.set_expression(i_port_path, i_expression)

    def create_proxy_ports_by_data(self, data, extend_kwargs=None):
        for i_port_path_src, i_arg_tgt in data.items():
            i_port_path_src = i_port_path_src.replace('/', '.')
            i_obj_path_tgt, i_port_path_tgt = i_arg_tgt
            #
            self.set_port_hint(
                i_port_path_src, dict(
                    text=bsc_core.RawStrUnderlineOpt(
                        bsc_core.PthPortMtd.get_dag_name(i_port_path_src)
                    ).to_prettify(capitalize=False)
                )
            )
            #
            i_obj_opt_tgt = NGNodeOpt(i_obj_path_tgt)
            i_port_path_tgt = i_port_path_tgt.replace('/', '.')
            i_p_tgt = i_obj_opt_tgt.get_port(i_port_path_tgt)
            if i_p_tgt is None:
                raise RuntimeError(
                    bsc_log.Log.trace_warning(
                        'port="{}" is non-exists'.format(i_port_path_tgt)
                    )
                )
            #
            i_obj_opt_tgt.set_expression(
                i_port_path_tgt, 'getParam(\'{}.{}\').param.getFullName()'.format(
                    self.get_name(), i_port_path_src
                )
            )

    def set_expand_groups_by_data(self, data, extend_kwargs=None):
        for i_port_path in data:
            #
            i_port_path = i_port_path.replace('/', '.')
            #
            i_p = self.ktn_obj.getParameter(i_port_path)
            if i_p is None:
                raise RuntimeError(
                    bsc_log.Log.trace_warning(
                        'port="{}" is non-exists'.format(i_port_path)
                    )
                )
            #
            i_hint_string = i_p.getHintString()
            if i_hint_string:
                i_hint_dict = eval(i_hint_string)
            else:
                i_hint_dict = {}
            #
            i_hint_dict['open'] = 1

            self.get_port(i_port_path).setHintString(str(i_hint_dict))

    def set_shader_expressions_by_data(self, data, extend_kwargs=None):
        for i_port_path, i_expression in data.items():
            #
            i_port_path = i_port_path.replace('/', '.')
            if isinstance(extend_kwargs, dict):
                if isinstance(i_expression, (unicode, str)):
                    i_expression = i_expression.format(**extend_kwargs)
            # turn on enable first
            i_enable_key = 'parameters.{}.enable'.format(i_port_path)
            self.set(i_enable_key, True)
            #
            i_value_key = 'parameters.{}.value'.format(i_port_path)
            # turn on the expression-flag
            self.set_expression_enable(i_value_key, True)
            self.set_expression(i_value_key, i_expression)

    def set_port_hints_by_data(self, data, extend_kwargs=None):
        for i_port_path, i_value in data.items():
            #
            i_port_path = i_port_path.replace('/', '.')
            i_p = self.ktn_obj.getParameter(i_port_path)
            if i_p is None:
                raise RuntimeError(
                    bsc_log.Log.trace_warning(
                        'port="{}" is non-exists'.format(i_port_path)
                    )
                )
            i_hint_string = i_p.getHintString()
            if i_hint_string:
                i_hint_dict = eval(i_hint_string)
            else:
                i_hint_dict = {}
            #
            if isinstance(i_value, six.string_types):
                i_hint_dict_ = eval(i_value)
            elif isinstance(i_value, dict):
                i_hint_dict_ = i_value
            else:
                raise RuntimeError()
            #
            i_hint_dict.update(i_hint_dict_)
            #
            if 'conditionalVisOps' in i_hint_dict:
                i_hint_dict['conditionalVisOps'] = dict(i_hint_dict['conditionalVisOps'])
            #
            i_p.setHintString(str(i_hint_dict))

    def set_port_hint(self, port_path, hint_dict):
        p = self.ktn_obj.getParameter(port_path)
        if p is None:
            raise RuntimeError(
                bsc_log.Log.trace_warning(
                    'port="{}" is non-exists'.format(port_path)
                )
            )
        hint_string = p.getHintString()
        if hint_string:
            hint_dict_ = eval(hint_string)
        else:
            hint_dict_ = {}

        hint_dict_.update(hint_dict)
        p.setHintString(str(hint_dict))

    def set_capsules_by_data(self, data, extend_kwargs=None):
        for i_port_path, i_value in data.items():
            #
            i_port_path = i_port_path.replace('/', '.')
            i_p = self.ktn_obj.getParameter(i_port_path)
            if i_p is None:
                raise RuntimeError(
                    bsc_log.Log.trace_warning(
                        'port="{}" is non-exists'.format(i_port_path)
                    )
                )
            self.set_capsule_strings(i_port_path, i_value)

    def set_shader_hints_by_data(self, data, extend_kwargs=None):
        for i_port_path, i_value in data.items():
            #
            i_port_path = i_port_path.replace('/', '.')
            # if isinstance(extend_kwargs, dict):
            #     if isinstance(i_value, (unicode, str)):
            #         i_value = i_value.format(**extend_kwargs)
            #
            i_hints_key = 'parameters.{}.hints'.format(i_port_path)
            #
            self.create_port(i_hints_key, 'string', i_value)

    def set_expression_enable(self, key, boolean):
        p = self.ktn_obj.getParameter(key)
        if p:
            p.setExpressionFlag(boolean)

    def set_expression(self, key, value):
        p = self.ktn_obj.getParameter(key)
        if p:
            p.setExpression(value)

    def get_is_expression(self, key):
        p = self.ktn_obj.getParameter(key)
        if p:
            return p.isExpression()

    def get_as_enumerate(self, key):
        port = self.ktn_obj.getParameter(key)
        if port:
            return NGPortOpt(port).get_enumerate_strings()
        return []

    def set_enumerate_strings(self, port_path, raw):
        port = self.ktn_obj.getParameter(port_path)
        if port:
            NGPortOpt(port).set_enumerate_strings(raw)

    def set_as_enumerate(self, key, value):
        self.set_enumerate_strings(key, value)

    def set_capsule_strings(self, key, data):
        port = self.ktn_obj.getParameter(key)
        if port:
            NGPortOpt(port).set_capsule_strings(data)

    def set_capsule_data(self, key, data):
        port = self.ktn_obj.getParameter(key)
        if port:
            NGPortOpt(port).set_capsule_data(data)

    def get_port(self, port_path):
        return self.ktn_obj.getParameter(port_path)

    def get_input_port(self, port_path):
        return self._ktn_obj.getInputPort(port_path)

    def create_input_port(self, port_path, **create_kwargs):
        _ = self._ktn_obj.getInputPort(port_path)
        if _ is not None:
            return _
        return self._ktn_obj.addInputPort(port_path, **create_kwargs)

    def create_input_ports_by_data(self, ports_data):
        for i in ports_data:
            if isinstance(i, six.string_types):
                i_name = i
                self.create_input_port(i_name)
            elif isinstance(i, dict):
                i_name = i.keys()[0]
                i_metadata = i.values()[0]
                self.create_input_port(i_name)
                i_port = self._ktn_obj.getInputPort(i_name)
                for j_k, j_v in i_metadata.items():
                    i_port.addOrUpdateMetadata(
                        j_k, j_v
                    )

    def get_input_ports(self):
        return self._ktn_obj.getInputPorts()

    def get_input_port_names(self):
        return [i.getName() for i in self.get_input_ports()]

    def connect_input_from(self, port_path, atr_arg):
        if isinstance(atr_arg, tuple):
            node_path_src, port_path_src = atr_arg
            if port_path_src is None:
                port_path_src = self.__class__(node_path_src).get_output_port_names()[0]

            atr_path_src = bsc_core.PthAttributeMtd.join_by(node_path_src, port_path_src)
            atr_path_tgt = bsc_core.PthAttributeMtd.join_by(self.get_path(), port_path)
            self._create_connections_by_data(
                [atr_path_src, atr_path_tgt]
            )
        elif isinstance(atr_arg, six.string_types):
            atr_path_src = atr_arg
            atr_path_tgt = bsc_core.PthAttributeMtd.join_by(self.get_path(), port_path)
            self._create_connections_by_data(
                [atr_path_src, atr_path_tgt]
            )

    def connect_output_to(self, port_path, atr_arg):
        if isinstance(atr_arg, tuple):
            node_path_tgt, port_path_tgt = atr_arg
            atr_path_src = bsc_core.PthAttributeMtd.join_by(self.get_path(), port_path)
            atr_path_tgt = bsc_core.PthAttributeMtd.join_by(node_path_tgt, port_path_tgt)
            self._create_connections_by_data(
                [atr_path_src, atr_path_tgt]
            )
        elif isinstance(atr_arg, six.string_types):
            atr_path_src = bsc_core.PthAttributeMtd.join_by(self.get_path(), port_path)
            atr_path_tgt = atr_arg
            self._create_connections_by_data(
                [atr_path_src, atr_path_tgt]
            )

    # output
    def get_output_port(self, port_path):
        return self._ktn_obj.getOutputPort(port_path)

    def get_output_ports(self):
        return self._ktn_obj.getOutputPorts()

    def get_output_port_names(self):
        return [i.getName() for i in self.get_output_ports()]

    def get_return_ports(self):
        return [self._ktn_obj.getReturnPort(i.getName()) for i in self._ktn_obj.getOutputPorts()]

    # send and return
    def get_send_port(self, port_path):
        return self._ktn_obj.getSendPort(port_path)

    def get_return_port(self, port_path):
        return self._ktn_obj.getReturnPort(port_path)

    def get_targets(self, port_path):
        p = self.get_output_port(port_path)
        if p:
            return p.getConnectedPorts()

    def create_port(self, port_path, port_type, default_value):
        _ = self.get_port(port_path)
        port_parent = bsc_core.PthPortMtd.get_dag_parent_path(
            path=port_path, pathsep=self.PORT_PATHSEP
        )
        port_name = bsc_core.PthPortMtd.get_dag_name(
            path=port_path, pathsep=self.PORT_PATHSEP
        )
        if _ is None:
            if port_parent is not None:
                parent_ktn_port = self.ktn_obj.getParameter(port_parent)
            else:
                parent_ktn_port = self.ktn_obj.getParameters()
            #
            if parent_ktn_port is not None:
                if port_type == 'string':
                    parent_ktn_port.createChildString(port_name, str(default_value))
        else:
            self.set(port_path, default_value)

    def do_delete(self):
        self.ktn_obj.delete()

    def get_position(self):
        return NodegraphAPI.GetNodePosition(self.ktn_obj)

    def set_position(self, x, y):
        atr = self._ktn_obj.getAttributes()
        atr.update(
            dict(
                x=x,
                y=y
            )
        )
        self._ktn_obj.setAttributes(atr)

    def set_color(self, rgb):
        r, g, b = rgb
        atr = self._ktn_obj.getAttributes()
        atr.update(
            dict(
                ns_colorr=r,
                ns_colorg=g,
                ns_colorb=b
            )
        )
        self._ktn_obj.setAttributes(atr)

    def move_to_view_center(self):
        ktn_cor_base.GuiNodeGraphOpt().move_node_to_view_center(
            self._ktn_obj
        )

    def clear_ports(self, port_path=None):
        if port_path is None:
            ktn_root_port = self._ktn_obj.getParameters()
            for i in ktn_root_port.getChildren():
                ktn_root_port.deleteChild(i)
        else:
            port_path = port_path.replace('/', '.')
            ktn_root_port = self._ktn_obj.getParameter(port_path)
        #
        if ktn_root_port is not None:
            for i in ktn_root_port.getChildren():
                ktn_root_port.deleteChild(i)

    def get_children(self, type_includes=None):
        _ = self._ktn_obj.getChildren()
        if isinstance(type_includes, (set, tuple, list)):
            return [i for i in _ if i.getType() in type_includes]
        return _

    def filter_children(self, filters):
        return NGNodesMtd.filter_fnc(self._ktn_obj.getChildren(), filters)

    def clear_children(self, type_includes=None):
        for i in self.get_children(type_includes):
            i.delete()

    def has_children(self):
        return not not self._ktn_obj.getChildren()

    def execute_port(self, port_path, index=None):
        ktn_port = self._ktn_obj.getParameter(port_path)
        if ktn_port:
            hint_string = ktn_port.getHintString()
            if hint_string:
                hint_dict = eval(hint_string)
                widget = hint_dict['widget']
                if widget in {'scriptButton'}:
                    script = hint_dict['scriptText']
                    # noinspection PyUnusedLocal
                    node = self._ktn_obj
                    exec script
                elif widget in {'scriptToolbar'}:
                    tools = hint_dict['buttonData']
                    if isinstance(index, int):
                        script = tools[index]['scriptText']
                        # noinspection PyUnusedLocal
                        node = self._ktn_obj
                        exec script

    def create_output_port(self, port_path):
        _ = self._ktn_obj.getOutputPort(port_path)
        if _ is None:
            self._ktn_obj.addOutputPort(port_path)

    def create_output_ports_by_data(self, ports_data):
        for i in ports_data:
            self.create_output_port(i)

    def get_parent(self):
        return self._ktn_obj.getParent()

    def get_parent_opt(self):
        parent = self.get_parent()
        if parent:
            return self.__class__(parent)

    def get_ancestors(self, type_includes=None):
        def rcs_fnc_(n_):
            _p = n_.getParent()
            if _p is not None:
                list_.append(_p)
                rcs_fnc_(_p)

        list_ = []

        rcs_fnc_(self._ktn_obj)

        if isinstance(type_includes, (set, tuple, list)):
            return [i for i in list_ if i.getType() in type_includes]
        return list_

    def get_attributes(self):
        return self._ktn_obj.getAttributes()

    def set_attributes(self, attributes):
        attributes_ = self._ktn_obj.getAttributes()
        attributes_.update(attributes)
        self._ktn_obj.setAttributes(attributes_)

    def set_edited(self, boolean):
        NodegraphAPI.SetNodeEdited(
            self._ktn_obj,
            edited=boolean, exclusive=True
        )

    def create_ports_by_data(self, data):
        for k, v in data.items():
            k = k.replace('/', '.')
            self.create_port_by_data(k, v)

    def create_port_by_data(self, port_path, data, expand_all_group=False):
        root_ktn_port = self._ktn_obj.getParameters()

        _port_path = port_path.split('.')
        group_names = _port_path[:-1]
        port_name = _port_path[-1]
        current_group_port = root_ktn_port
        for i_group_name in group_names:
            i_ktn_group_port = current_group_port.getChild(i_group_name)
            if i_ktn_group_port is None:
                i_ktn_group_port = current_group_port.createChildGroup(i_group_name)
                i_group_label = bsc_core.RawStrUnderlineOpt(i_group_name).to_prettify(capitalize=False)

                i_group_hint_dict = dict(
                    label=i_group_label,
                    help='...'
                )
                if expand_all_group is True:
                    i_group_hint_dict['open'] = 1

                i_ktn_group_port.setHintString(
                    str(i_group_hint_dict)
                )

            current_group_port = i_ktn_group_port

        group_ktn_obj = current_group_port

        widget = data.get('widget')
        if widget in {'group'}:
            ktn_group = group_ktn_obj.createChildGroup(port_name)
            label = data.get('label', None)
            if label is None:
                label = bsc_core.RawStrUnderlineOpt(port_name).to_prettify(capitalize=False)
            #
            hint_dict = {'label': label}
            lock = data.get('lock')
            if lock is True:
                hint_dict['readOnly'] = True
            tool_tip = data.get('tool_tip')
            if tool_tip:
                hint_dict['help'] = tool_tip
            else:
                hint_dict['help'] = '...'

            expand = data.get('expand')
            if expand:
                hint_dict['open'] = 1

            if expand_all_group is True:
                hint_dict['open'] = 1

            visible_condition_hint = data.get('visible_condition_hint')
            if visible_condition_hint:
                hint_dict['conditionalVisOps'] = dict(visible_condition_hint)

            ktn_group.setHintString(
                str(hint_dict)
            )
        else:
            self._create_port_by_data(
                group_ktn_obj,
                dict(
                    widget=data.get('widget'),
                    name=port_name,
                    label=data.get('label', None),
                    value=data.get('value'),
                    default=data.get('default'),
                    expression=data.get('expression'),
                    tool_tip=data.get('tool_tip'),
                    lock=data.get('lock'),
                    visible_condition_hint=data.get('visible_condition_hint'),
                    expand=data.get('expand'),
                    range=data.get('range')
                )
            )

    @classmethod
    def _create_port_by_data(cls, group_ktn_obj, data):
        name = data['name']
        label = data['label']
        widget = data['widget']
        value = data['value']
        default = data['default']
        expression = data['expression']
        tool_tip = data['tool_tip']
        lock = data['lock']
        if label is None:
            label = bsc_core.RawStrUnderlineOpt(name).to_prettify(capitalize=False)

        ktn_port = group_ktn_obj.getChild(name)
        if ktn_port is None:
            if widget in {'proxy'}:
                ktn_port = group_ktn_obj.createChildString(name, '')
                ktn_port.setHintString(
                    str({'widget': 'teleparam'})
                )
            else:
                if isinstance(value, (bool,)):
                    ktn_port = group_ktn_obj.createChildNumber(name, value)
                    ktn_port.setHintString(str({'widget': 'checkBox', 'constant': 'True'}))
                #
                elif isinstance(value, six.string_types):
                    ktn_port = group_ktn_obj.createChildString(name, value)
                    if expression:
                        ktn_port.setExpression(expression)
                    if widget in {'path'}:
                        ktn_port.setHintString(
                            str({'widget': 'scenegraphLocation'})
                        )
                    elif widget in {'CEL'}:
                        ktn_port.setHintString(
                            str({'widget': 'cel'})
                        )
                    elif widget in {'file'}:
                        ktn_port.setHintString(
                            str({'widget': 'fileInput'})
                        )
                    elif widget in {'script'}:
                        ktn_port.setHintString(
                            str({'widget': 'scriptEditor'})
                        )
                    elif widget in {'resolution'}:
                        ktn_port.setHintString(
                            str({'widget': 'resolution'})
                        )
                    elif widget in {'button'}:
                        ktn_port.setHintString(
                            str({'widget': 'scriptButton', 'buttonText': label, 'scriptText': value})
                        )
                    elif widget in {'node'}:
                        ktn_port.setHintString(
                            str({'widget': 'nodeDropProxy'})
                        )
                        if value:
                            ktn_port.setExpression(
                                'getNode(\'{}\').getNodeName()'.format(
                                    value
                                )
                            )
                elif isinstance(value, (int, float)):
                    ktn_port = group_ktn_obj.createChildNumber(name, value)
                    if widget in {'boolean'}:
                        ktn_port.setHintString(
                            str({'widget': 'boolean'})
                        )
                    elif widget in {'integer'}:
                        value_range = data['range']
                        if value_range is not None:
                            minimum, maximum = value_range
                            ktn_port.setHintString(
                                str({'int': True, 'slider': True, 'slidermin': minimum, 'slidermax': maximum})
                            )
                        else:
                            ktn_port.setHintString(
                                str({'int': True})
                            )
                elif isinstance(value, (list,)):
                    if widget in {'enumerate'}:
                        ktn_port = group_ktn_obj.createChildString(name, value[0])
                        ktn_port.setHintString(
                            str(
                                dict(
                                    widget='popup',
                                    options=list(value)
                                )
                            )
                        )
                        if default is not None:
                            ktn_port.setValue(default, 0)
                    elif widget in {'color3'}:
                        c = 3
                        ktn_port = group_ktn_obj.createChildNumberArray(name, c)
                        for i in range(c):
                            i_ktn_port = ktn_port.getChildByIndex(i)
                            i_ktn_port.setValue(value[i], 0)
                        #
                        ktn_port.setHintString(
                            str(dict(widget='color'))
                        )
                    elif widget in {'float3'}:
                        c = 3
                        ktn_port = group_ktn_obj.createChildNumberArray(name, c)
                        for i in range(c):
                            i_ktn_port = ktn_port.getChildByIndex(i)
                            i_ktn_port.setValue(value[i], 0)
                    elif widget in {'string2'}:
                        c = 2
                        ktn_port = group_ktn_obj.createChildStringArray(name, c)
                        for i in range(c):
                            i_ktn_port = ktn_port.getChildByIndex(i)
                            i_ktn_port.setValue(value[i], 0)
                    elif widget in {'string3'}:
                        c = 3
                        ktn_port = group_ktn_obj.createChildStringArray(name, c)
                        for i in range(c):
                            i_ktn_port = ktn_port.getChildByIndex(i)
                            i_ktn_port.setValue(value[i], 0)
                    elif widget in {'capsule_string'}:
                        if value:
                            v = value[0]
                        else:
                            v = ''
                        ktn_port = group_ktn_obj.createChildString(name, v)
                        ktn_port.setHintString(
                            str(
                                dict(
                                    widget='capsule',
                                    options=list(value),
                                    displayText=map(
                                        lambda x: bsc_core.RawStrUnderlineOpt(x).to_prettify(), list(value)
                                    ),
                                    exclusive=True,
                                    colors=[bsc_core.RawTextOpt(i).to_rgb__(s_p=50, v_p=100) for i in list(value)],
                                    equalPartitionWidths=True,
                                )
                            )
                        )
                        if default is not None:
                            ktn_port.setValue(default, 0)
                    elif widget in {'capsule_strings'}:
                        sep = ', '
                        v = sep.join(value)
                        ktn_port = group_ktn_obj.createChildString(name, v)
                        ktn_port.setHintString(
                            str(
                                dict(
                                    widget='capsule',
                                    options=list(value),
                                    displayText=map(
                                        lambda x: bsc_core.RawStrUnderlineOpt(x).to_prettify(), list(value)
                                    ),
                                    exclusive=False,
                                    colors=[bsc_core.RawTextOpt(i).to_rgb__(s_p=50, v_p=100) for i in list(value)],
                                    equalPartitionWidths=True,
                                    delimiter=sep
                                )
                            )
                        )
                        if default is not None:
                            default_v = sep.join(default)
                            ktn_port.setValue(default_v, 0)
                    elif widget in {'buttons'}:
                        ktn_port = group_ktn_obj.createChildString(name, '')
                        hint_dict = dict(
                            widget='scriptToolbar',
                            buttonData=[dict(text=i.get('name', ''), scriptText=i.get('script', ''), flat=0) for i in
                                        value]
                        )
                        ktn_port.setHintString(
                            str(
                                hint_dict
                            )
                        )
                    elif widget in {'integer_array'}:
                        c_c = 1
                        c = c_c*10
                        ktn_port = group_ktn_obj.createChildNumberArray(name, c)
                        ktn_port.setTupleSize(c_c)
                        for i in range(c):
                            i_ktn_port = ktn_port.getChildByIndex(i)
                            i_ktn_port.setValue(0, 0)
                        ktn_port.setHintString(
                            str({'int': True})
                        )
                    elif widget in {'vector_array', 'color_array'}:
                        c_c = 3
                        c = c_c*2
                        ktn_port = group_ktn_obj.createChildNumberArray(name, c)
                        ktn_port.setTupleSize(c_c)
                        for i in range(c):
                            i_ktn_port = ktn_port.getChildByIndex(i)
                            i_ktn_port.setValue(0, 0)
                    else:
                        c = len(value)
                        if isinstance(value[0], six.string_types):
                            ktn_port = group_ktn_obj.createChildStringArray(name, c)
                        elif isinstance(value[0], (int, float)):
                            ktn_port = group_ktn_obj.createChildNumberArray(name, c)
                        else:
                            raise TypeError()
                        #
                        for i in range(c):
                            i_ktn_port = ktn_port.getChildByIndex(i)
                            i_ktn_port.setValue(value[i], 0)
                else:
                    raise TypeError()
            #
            hint_string = ktn_port.getHintString()
            if hint_string:
                hint_dict = eval(hint_string)
            else:
                hint_dict = {'constant': 'True'}
            #
            if tool_tip is not None:
                hint_dict['help'] = tool_tip
            else:
                hint_dict['help'] = '...'
            #
            if lock is True:
                hint_dict['readOnly'] = True
            #
            visible_condition_hint = data.get('visible_condition_hint')
            if visible_condition_hint:
                hint_dict['conditionalVisOps'] = dict(visible_condition_hint)
            #
            expand = data.get('expand')
            if expand:
                hint_dict['open'] = 1
            #
            hint_dict['label'] = label
            ktn_port.setHintString(
                str(hint_dict)
            )

    def save_as_macro(self, file_path):
        UserNodes.PublishNode(
            self._ktn_obj, file_path
        )

    def get_variable_data(self):
        pass

    def get_is_bypassed(self, ancestors=False):
        if self._ktn_obj.isBypassed() is True:
            return True
        #
        if ancestors is False:
            return False
        #
        _ = self.get_ancestors()
        if _:
            for i in _:
                if i.isBypassed():
                    return True
        return False

    def update_cell(self, key, value):
        p = '[(](.*?)[)]'
        value_pre = self.get(key)
        if value_pre:
            _ = re.findall(p, value_pre)
            if _:
                value_cur = '({} {})'.format(_[0], value)
            else:
                value_cur = '({} {})'.format(value_pre, value)
        else:
            value_cur = value
        #
        self.set(key, value_cur)

    def __str__(self):
        return '{}(path="{}")'.format(
            self.get_type_name(), self.get_path()
        )


class NGGuiLayout(object):
    def __init__(self, ktn_objs):
        self._ktn_objs = ktn_objs

    def layout_shader_graph(
        self, scheme=(
            NGLayoutOpt.Orientation.Horizontal,
            NGLayoutOpt.Direction.RightToLeft,
            NGLayoutOpt.Direction.TopToBottom
        ),
        size=(320, 80), expanded=False, collapsed=False, shader_view_state=None
    ):
        graph_dara = self.get_gui_layout_data(inner=False, size=size)
        #
        NGLayoutOpt(
            graph_dara,
            scheme=scheme,
            size=size,
            option=dict(
                expanded=expanded,
                collapsed=collapsed,
                shader_view_state=shader_view_state,
            )
        ).run()

    def get_gui_layout_data(self, **kwargs):
        def rcs_fnc_(ktn_obj_, root_name_, root_index_, branch_index_):
            if skip_base_type_names:
                base_type_name = ktn_obj_.getBaseType()
                if base_type_name in skip_base_type_names:
                    return
            if hasattr(ktn_obj_, 'getChildren'):
                _branch_name = ktn_obj_.getName()
                outer_fnc_(ktn_obj_, root_name_, _branch_name, root_index_, branch_index_)
                # inner
                if inner is True:
                    # reset start to 0
                    _root_name = ktn_obj_.getName()
                    _start_index = 0
                    inner_fnc_(ktn_obj_, _root_name, _branch_name, root_index_, _start_index)
            else:
                _branch_name = ktn_obj_.getName()
                outer_fnc_(ktn_obj_, root_name_, _branch_name, root_index_, branch_index_)

        #
        def outer_fnc_(ktn_obj_, root_name_, branch_name_, root_index_, branch_index_):
            _source_ktn_objs = NGNodeOpt(ktn_obj_).get_source_objs()
            #
            if _source_ktn_objs:
                branch_index_ += 1
                add_fnc_(_source_ktn_objs, root_name_, branch_name_, root_index_, branch_index_)

        #
        def inner_fnc_(ktn_obj_, root_name_, branch_name_, root_index_, branch_index_):
            root_index_ += 1
            #
            _source_ktn_objs = NGNodeOpt._get_source_objs_inner_(ktn_obj_)
            if _source_ktn_objs:
                branch_index_ += 1
                add_fnc_(_source_ktn_objs, root_name_, branch_name_, root_index_, branch_index_)

        #
        def add_fnc_(ktn_objs_, root_name_, branch_name_, root_index_, branch_index_):
            _graph_key_cur = (root_index_, branch_index_, root_name_)
            _size_key_cur = (root_index_, root_name_)
            #
            if _size_key_cur not in size_dict:
                _h_in_cur = {}
                size_dict[_size_key_cur] = _h_in_cur
            else:
                _h_in_cur = size_dict[_size_key_cur]
            #
            if _graph_key_cur not in graph_dict:
                _graph_data_in_cur = []
                graph_dict[_graph_key_cur] = _graph_data_in_cur
            else:
                _graph_data_in_cur = graph_dict[_graph_key_cur]
            #
            _branch_key = (root_index_, branch_name_)
            for _i_sub_index, _i_ktn_obj in enumerate(ktn_objs_):
                _i_ktn_obj_opt = NGNodeOpt(_i_ktn_obj)
                _i_type_name = _i_ktn_obj.getType()
                _i_leaf_name = _i_ktn_obj.getName()
                _i_w = _i_ktn_obj_opt.get('gui_layout.size.w') or w
                _i_h = _i_ktn_obj_opt.get('gui_layout.size.h') or h
                #
                if branch_index_ in _h_in_cur:
                    _i_h_pre = _h_in_cur[branch_index_]
                    if _i_h > _i_h_pre:
                        _h_in_cur[branch_index_] = _i_h
                else:
                    _h_in_cur[branch_index_] = _i_h
                #
                _i_branch_index_key_cur = (root_index_, _i_leaf_name)
                if _i_branch_index_key_cur not in leaf_branch_name_dict:
                    leaf_branch_name_dict[_i_branch_index_key_cur] = branch_name_
                #
                _i_graph_key_cur = _graph_key_cur
                # break the self-cycle
                if _i_leaf_name != root_name_:
                    # try move to end
                    _i_leaf_key = (root_index_, _i_leaf_name)
                    leaf_branch_names_dict.setdefault(
                        _i_leaf_key, []
                    ).append(branch_name_)
                    branch_leaf_names_dict.setdefault(
                        _branch_key, []
                    ).append(_i_leaf_name)
                    if _i_leaf_key in leaf_branch_index_dict:
                        _i_branch_index_cur = branch_index_
                        _i_index_pre = leaf_branch_index_dict[_i_leaf_key]
                        if _i_index_pre < _i_branch_index_cur:
                            _i_graph_key_pre = (root_index_, _i_index_pre, root_name_)
                            if _i_graph_key_pre in graph_dict:
                                _graph_data_in_index_pre = graph_dict[_i_graph_key_pre]
                                if _i_leaf_name in _graph_data_in_index_pre:
                                    _graph_data_in_index_pre.remove(_i_leaf_name)
                                    _graph_data_in_cur.append(_i_leaf_name)
                                    leaf_branch_index_dict[_i_leaf_key] = _i_branch_index_cur
                    else:
                        leaf_branch_index_dict[_i_leaf_key] = branch_index_
                        #
                        _graph_data_in_cur.append(_i_leaf_name)
                    #
                    rcs_fnc_(_i_ktn_obj, root_name_, root_index_, branch_index_)

        #
        inner = kwargs.get('inner', False)
        skip_base_type_names = kwargs.get('skip_base_type_names', [])
        w, h = kwargs.get('size', [320, 40])
        #
        leaf_branch_name_dict = {
            # (root_index, leaf_name): branch_name
        }
        #
        branch_leaf_names_dict = {
            # (root_index, branch_name): [leaf_name, ...]
        }
        leaf_branch_names_dict = {
            # (root_index, leaf_name): [branch_name, ...]
        }
        #
        leaf_branch_index_dict = {
            # (root_index, leaf_name): branch_index
        }
        size_dict = {

        }
        graph_dict = {
            # (root_index, branch_index, root_name): [name, ...]
        }
        #
        for i_ktn_obj in self._ktn_objs:
            i_name = i_ktn_obj.getName()
            i_start_depth = 0
            i_start_index = 0
            #
            rcs_fnc_(i_ktn_obj, i_name, i_start_depth, i_start_index)
        return branch_leaf_names_dict, leaf_branch_names_dict, size_dict, graph_dict


class NGNodesOpt(object):
    def __init__(self, type_name=None):
        self._type_name = type_name

    def get_obj_names(self, pattern=None):
        if self._type_name is not None:
            _ = NodegraphAPI.GetAllNodesByType(self._type_name) or []
        else:
            _ = NodegraphAPI.GetAllNodes() or []
        #
        obj_names = [i.getName() for i in _]
        if pattern is not None:
            return fnmatch.filter(
                obj_names, pattern
            )
        return obj_names


class NGGroupStackOpt(NGNodeOpt):
    def __init__(self, ktn_obj):
        super(NGGroupStackOpt, self).__init__(ktn_obj)

    def _get_last_(self):
        ktn_obj = self._ktn_obj
        _ = ktn_obj.getReturnPort('out').getConnectedPorts()
        if _:
            return _[0].getNode()
        return ktn_obj

    def set_child_create(self, name):
        src_ktn_obj = self._ktn_obj
        type_name = src_ktn_obj.getChildNodeType()
        tgt_ktn_obj = NodegraphAPI.GetNode(name)
        if tgt_ktn_obj is not None:
            return tgt_ktn_obj, False
        #
        tgt_ktn_obj = NodegraphAPI.CreateNode(type_name, src_ktn_obj)
        if tgt_ktn_obj is None:
            raise TypeError('unknown-obj-type: "{}"'.format(type_name))
        name_ktn_port = tgt_ktn_obj.getParameter('name')
        if name_ktn_port is not None:
            name_ktn_port.setValue(str(name), 0)
        tgt_ktn_obj.setName(name)
        #
        last_ktn_obj = self._get_last_()
        if last_ktn_obj.getName() == self.name:
            src_ktn_obj.getSendPort('in').connect(
                tgt_ktn_obj.getInputPorts()[0]
            )
        else:
            x, y = NodegraphAPI.GetNodePosition(last_ktn_obj)
            NodegraphAPI.SetNodePosition(tgt_ktn_obj, (x, y-48))
            #
            last_ktn_obj.getOutputPorts()[0].connect(
                tgt_ktn_obj.getInputPorts()[0]
            )
        #
        tgt_ktn_obj.getOutputPorts()[0].connect(src_ktn_obj.getReturnPort('out'))
        return tgt_ktn_obj, True


class NGMaterialGroupOpt(NGNodeOpt):
    def __init__(self, ktn_obj):
        super(NGMaterialGroupOpt, self).__init__(ktn_obj)


class NGPortOpt(object):
    PATHSEP = '.'

    def __init__(self, ktn_port):
        self.__ktn_port = ktn_port
        self._atr_path = self._to_atr_path_(self.__ktn_port)

    @property
    def ktn_port(self):
        return self.__ktn_port

    @property
    def ktn_obj(self):
        return self.ktn_port.getNode()

    @property
    def type(self):
        return self.ktn_port.getType()

    @property
    def path(self):
        return self._atr_path

    def get_name(self):
        return self.__ktn_port.getName()

    name = property(get_name)

    @classmethod
    def _to_atr_path_(cls, ktn_port):
        def rcs_fnc_(p_):
            if p_ is not None:
                list_.append(p_.getName())
                rcs_fnc_(p_.getParent())

        list_ = []
        rcs_fnc_(ktn_port)
        list_.reverse()
        return cls.PATHSEP.join(list_)

    def get(self, frame=0):
        _children = self.ktn_port.getChildren() or []
        if _children:
            return [i.getValue(frame) for i in _children]
        return self.ktn_port.getValue(frame)

    def set(self, value, frame=0):
        if isinstance(value, (tuple, list)):
            size = len(value)
            self.ktn_port.resizeArray(size)
            [self.ktn_port.getChildByIndex(i).setValue(value[i], frame) for i in range(size)]
        else:
            _value = value
            if isinstance(value, unicode):
                _value = str(value)
            #
            if self.get_is_enumerate() is True:
                if isinstance(value, int):
                    strings = self.get_enumerate_strings()
                    index = max(min(value, len(strings)-1), 0)
                    _value = strings[index]
            #
            self.ktn_port.setValue(_value, frame)

    def set_tool_tip(self, value):
        hint_string = self.ktn_port.getHintString()
        if hint_string:
            hint_dict = eval(hint_string)
        else:
            hint_dict = {}
        #
        hint_dict['help'] = value
        #
        self.ktn_port.setHintString(
            str(hint_dict)
        )

    def get_is_enumerate(self):
        hint_string = self.ktn_port.getHintString()
        if hint_string:
            hint_dict = eval(hint_string)
            return hint_dict.get('widget') == 'popup'

    def set_enumerate_strings(self, value, frame=0):
        hint_string = self.ktn_port.getHintString()
        if hint_string:
            hint_dict = eval(hint_string)
        else:
            hint_dict = {}
        #
        hint_dict['options'] = list(value)
        #
        self.ktn_port.setHintString(
            str(hint_dict)
        )
        self.ktn_port.setValue(
            str(value[0]), frame
        )

    def get_enumerate_strings(self):
        hint_string = self.ktn_port.getHintString()
        if hint_string:
            hint_dict = eval(hint_string)
            return map(str, hint_dict.get('options', []))
        return []

    def set_capsule_strings(self, strings):
        hint_string = self.ktn_port.getHintString()
        if hint_string:
            hint_dict = eval(hint_string)
        else:
            hint_dict = {}
        #
        hint_dict.update(
            dict(
                options=list(strings),
                displayText=map(lambda x: bsc_core.RawStrUnderlineOpt(x).to_prettify(word_count_limit=12), list(strings)),
                colors=[bsc_core.RawTextOpt(i).to_rgb__(s_p=50, v_p=100) for i in list(strings)],
            )
        )
        #
        self.ktn_port.setHintString(
            str(hint_dict)
        )
        self.ktn_port.setValue(
            str(strings[0]), 0
        )

    def set_capsule_data(self, data):
        hint_string = self.ktn_port.getHintString()
        if hint_string:
            hint_dict = eval(hint_string)
        else:
            hint_dict = {}
        #
        options = []
        display_texts = []
        colors = []
        for i in data:
            i_0, i_1 = i
            options.append(i_0)
            display_texts.append(i_1)
            colors.append(bsc_core.RawTextOpt(i_1).to_rgb__(s_p=50, v_p=50))
        #
        hint_dict.update(
            dict(
                options=options,
                displayText=display_texts,
                colors=colors,
            )
        )
        #
        self.ktn_port.setHintString(
            str(hint_dict)
        )

    def connect_to(self, input_port):
        self.__ktn_port.connect(
            input_port
        )

    def set_target(self, input_port):
        self.__ktn_port.connect(
            input_port
        )

    def set_expression(self, raw):
        self.__ktn_port.setExpression(raw)

    def get_expression(self):
        return self.__ktn_port.getExpression()

    def get_is_expression(self):
        return self.__ktn_port.isExpression()

    def get_children(self):
        return self.__ktn_port.getChildren()

    def clear_children(self):
        [self.__ktn_port.deleteChild(i) for i in self.get_children()]


class NGNodeTypeOpt(object):
    def __init__(self, obj_type_name):
        self._obj_type_name = obj_type_name

    def get_objs(self):
        return NodegraphAPI.GetAllNodesByType(self._obj_type_name)


class NGAndNodeTypeOpt(object):
    def __init__(self, type_name):
        self._obj_type_name = type_name

    def get_ktn_objs(self):
        list_ = []
        for i_ktn_obj in NodegraphAPI.GetAllNodesByType('ArnoldShadingNode') or []:
            i_ktn_obj_opt = NGNodeOpt(i_ktn_obj)
            i_shader_type_name = i_ktn_obj_opt.get_port_raw('nodeType')
            if i_shader_type_name in [self._obj_type_name]:
                list_.append(i_ktn_obj)
        return list_

    def get_obj_opts(self):
        list_ = []
        for i_ktn_obj in NodegraphAPI.GetAllNodesByType('ArnoldShadingNode') or []:
            i_ktn_obj_opt = NGNodeOpt(i_ktn_obj)
            i_shader_type_name = i_ktn_obj_opt.get_port_raw('nodeType')
            if i_shader_type_name in [self._obj_type_name]:
                list_.append(i_ktn_obj_opt)
        return list_


# noinspection PyPep8Naming
class NGNmeOpt(object):
    STATE_DICT = {}

    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    @classmethod
    def _set_status_(cls, key):
        cls.STATE_DICT[key] = True

    @classmethod
    def _get_status_(cls, key):
        return cls.STATE_DICT.get(key, False)

    def set_contents_update(self):
        key = self._ktn_obj.getName()
        pre_status = self._get_status_(key)
        if pre_status is False:
            cls = self._ktn_obj.__class__
            mod = sys.modules[cls.__module__]
            status = mod.UpdateStatus
            #
            if ktn_cor_base.KtnUtil.get_is_ui_mode() is False:
                print('update "NetworkMaterialEdit" "{}" events is ignored'.format(self._ktn_obj.getName()))
                self._ktn_obj.__dict__['_NetworkMaterialEditNode__queuedNodeGraphEvents'] = []
            #
            updateStatus = self._ktn_obj._NetworkMaterialEditNode__updateContents()
            if updateStatus == status.Succeeded:
                print('update "NetworkMaterialEdit" "{}" completed'.format(self._ktn_obj.getName()))
                self._set_status_(key)
                return True
            elif updateStatus == status.UserCancelled:
                print('update "NetworkMaterialEdit" "{}" is cancelled by the user'.format(self._ktn_obj.getName()))
            #
            print('update "NetworkMaterialEdit" "{}" is failed'.format(self._ktn_obj.getName()))
            return False
        return False

    def set_contents_update_(self):
        key = self._ktn_obj.getName()
        pre_status = self._get_status_(key)
        if pre_status is False:
            mod = sys.modules[self._ktn_obj.__class__.__module__]
            status = mod.UpdateStatus
            #
            updateStatus = self._set_contents_update_(self._ktn_obj)
            if updateStatus == status.Succeeded:
                print('update "NetworkMaterialEdit" "{}" completed'.format(self._ktn_obj.getName()))
                self._set_status_(key)
                return True
            elif updateStatus == status.UserCancelled:
                print('update "NetworkMaterialEdit" "{}" is cancelled by the user'.format(self._ktn_obj.getName()))
            #
            print('update "NetworkMaterialEdit" "{}" is failed'.format(self._ktn_obj.getName()))
            return False
        return False

    @classmethod
    def _set_contents_update_(cls, ktn_obj):
        """
        from katana: __plugins2__.NetworkMaterials.v1.NetworkMaterialEditNode.NetworkMaterialEditNode
        :param ktn_obj:
        :return:
        """
        mod = sys.modules[ktn_obj.__class__.__module__]
        UpdateStatus = mod.UpdateStatus
        with ktn_obj._NetworkMaterialEditNode__ignoreChanges():
            upstreamMaterial = ktn_obj._NetworkMaterialEditNode__getIncomingMaterialAttributes()
            producer = ktn_obj._NetworkMaterialEditNode__getEditedGeometryProducer()
            materialAttr = None
            if producer is not None:
                materialAttr = producer.getGlobalAttribute('material')
            status = UpdateStatus.Succeeded
            if not upstreamMaterial or not materialAttr or producer.getType() == 'error':
                ktn_obj._NetworkMaterialEditNode__clearContents()
                status = UpdateStatus.Failed
            elif upstreamMaterial.getHash() != ktn_obj._NetworkMaterialEditNode__lastUpstreamMaterialHash:
                ktn_obj._NetworkMaterialEditNode__clearContents()
                if ktn_cor_base.KtnUtil.get_is_ui_mode() is True:
                    populated = ktn_obj._NetworkMaterialEditNode__populateFromInputMaterial(
                        upstreamMaterial, materialAttr
                    )
                else:
                    populated = cls._populate_from_input_material(ktn_obj, upstreamMaterial, materialAttr)
                if not populated:
                    status = UpdateStatus.UserCancelled
            if status == UpdateStatus.UserCancelled:
                ktn_obj._NetworkMaterialEditNode__lastUpstreamMaterialHash = None
            else:
                ktn_obj._NetworkMaterialEditNode__lastUpstreamMaterialHash = materialAttr and upstreamMaterial and upstreamMaterial.getHash()
            #
            if ktn_cor_base.KtnUtil.get_is_ui_mode() is True:
                ktn_obj._NetworkMaterialEditNode__notifyUpdated()
            return status

    @classmethod
    def _populate_from_input_material(cls, ktn_obj, incoming_material, material_attr):
        mod = sys.modules[ktn_obj.__class__.__module__]
        #
        ktn_obj._NetworkMaterialEditNode__reconstructionInProgress = True
        nmcNetworkMaterialNodeNameAttr = material_attr.getChildByName('info.name')
        if nmcNetworkMaterialNodeNameAttr is None:
            return False
        else:
            nmcNetworkMaterialNodeName = nmcNetworkMaterialNodeNameAttr.getValue()
            layoutAttr = material_attr.getChildByName('layout')
            if layoutAttr is None:
                return False
            parentAttr = layoutAttr.getChildByName('%s.parent'%nmcNetworkMaterialNodeName)
            if parentAttr is None:
                return False
            nmcName = parentAttr.getValue()
            ktn_obj._NetworkMaterialEditNode__nodeSourceNameLookup[ktn_obj] = nmcName
            opArgs = ktn_obj._getGenericOpArgs()
            layoutAttr = material_attr.getChildByName('layout')
            totalNodes = layoutAttr.getNumberOfChildren()
            progressCallback = mod._GetUpdateProgressCallback(totalNodes)
            orderedNodeNames = mod.LayoutNodesSorter(layoutAttr).build()
            paramExtractor = mod.LayoutParameterExtractor(opArgs, orderedNodeNames)
            try:
                for i in range(totalNodes):
                    nodeName = orderedNodeNames[i]
                    nodeLayoutAttr = layoutAttr.getChildByName(nodeName)
                    node = ktn_obj._NetworkMaterialEditNode__createNodeFromLayoutAttr(
                        paramExtractor, nodeName, nodeLayoutAttr
                    )
                    if node:
                        ktn_obj._NetworkMaterialEditNode__shadingNetworkNodes[nodeName] = node
                        ktn_obj._NetworkMaterialEditNode__nodeSourceNameLookup[node] = nodeName
                #
                ktn_obj._NetworkMaterialEditNode__connectNodes(layoutAttr)
                ktn_obj._NetworkMaterialEditNode__setMaterialLocationCallbackOnNodes(incoming_material)
                ktn_obj._NetworkMaterialEditNode__lockNonContributingNodes(material_attr, orderedNodeNames)
                ktn_obj._NetworkMaterialEditNode__reconstructionInProgress = False
                ktn_obj.invalidateLayout()
                sourceLayoutVersionAttr = material_attr.getChildByName('info.sourceLayoutVersion')
                nodesToLayout = paramExtractor.getSparseNodes('position')
                viewState = None
                if sourceLayoutVersionAttr is not None and sourceLayoutVersionAttr.getValue() == 0:
                    nodesToLayout = ktn_obj._NetworkMaterialEditNode__shadingNetworkNodes.values()
                    viewState = 1.0
                if nodesToLayout:
                    ktn_obj._NetworkMaterialEditNode__autoLayoutShadingNetworkNodes(nodesToLayout, viewState)
                return True
            finally:
                ktn_obj._NetworkMaterialEditNode__reconstructionInProgress = False
                progressCallback(totalNodes)

    def _test_(self):
        self._set_contents_update_(
            self._ktn_obj
        )


class NGNodeCustomizePortOpt(object):
    def __init__(self, ktn_port):
        self._ktn_obj = ktn_port

    def set_ports_add(self, raw):
        # etc:
        # collections.OrderedDict(
        #     [
        #         ('render_settings.camera', ''),
        #         ('render_settings.resolution', '512x512'),
        #         ('render_settings.frame', 1),
        #         #
        #         ('arnold_render_settings.stats_file', ''),
        #         ('arnold_render_settings.profile_file', '')
        #     ]
        # )
        ps = self._ktn_obj.getParameters()
        for k, v in raw.items():
            if isinstance(k, six.string_types):
                i_port_path = k
                scheme = None
            elif isinstance(k, (tuple,)):
                scheme, i_port_path, = k
            else:
                raise TypeError()
            #
            i_ps = i_port_path.split('.')
            i_gs = i_ps[:-1]
            i_p = i_ps[-1]
            c_g = ps
            for i_p_n in i_gs:
                i_g = c_g.getChild(i_p_n)
                if i_g is None:
                    i_g = c_g.createChildGroup(i_p_n)
                #
                i_g_l = bsc_core.RawStrUnderlineOpt(i_p_n).to_prettify(capitalize=False)
                i_g.setHintString(
                    str(
                        str({'label': i_g_l})
                    )
                )
                c_g = i_g
            #
            i_ktn_group_port = c_g
            self._set_type_port_add_(
                i_ktn_group_port, scheme=scheme, name=i_p, value=v, default=v
            )

    def add_port(self, key, value):
        pass

    @classmethod
    def _set_port_add_as_enable_(cls):
        pass

    @classmethod
    def _set_type_port_add_(cls, group_ktn_obj, name, scheme, value, default):
        label = bsc_core.RawStrUnderlineOpt(name).to_prettify(capitalize=False)
        ktn_port = group_ktn_obj.getChild(name)
        if ktn_port is None:
            if isinstance(default, (bool,)):
                ktn_port = group_ktn_obj.createChildNumber(name, value)
                ktn_port.setHintString(str({'widget': 'checkBox', 'constant': 'True'}))
            elif isinstance(default, six.string_types):
                ktn_port = group_ktn_obj.createChildString(name, value)
                if scheme in ['path']:
                    ktn_port.setHintString(
                        str({'widget': 'scenegraphLocation'})
                    )
                elif scheme in ['file']:
                    ktn_port.setHintString(
                        str({'widget': 'fileInput'})
                    )
                elif scheme in ['script']:
                    ktn_port.setHintString(
                        str({'widget': 'scriptEditor'})
                    )
                elif scheme in ['resolution']:
                    ktn_port.setHintString(
                        str({'widget': 'resolution'})
                    )
                elif scheme in ['button']:
                    ktn_port.setHintString(
                        str({'widget': 'scriptButton', 'buttonText': label, 'scriptText': value})
                    )
            elif isinstance(default, (int, float)):
                ktn_port = group_ktn_obj.createChildNumber(name, value)
            elif isinstance(default, (tuple,)):
                if scheme in ['enumerate']:
                    ktn_port = group_ktn_obj.createChildString(name, value[0])
                    ktn_port.setHintString(
                        str(dict(widget='popup', options=list(value)))
                    )
                else:
                    c = len(default)
                    if isinstance(default[0], six.string_types):
                        ktn_port = group_ktn_obj.createChildStringArray(name, c)
                    elif isinstance(default[0], (int, float)):
                        ktn_port = group_ktn_obj.createChildNumberArray(name, c)
                    else:
                        raise TypeError()
                    #
                    for i in range(c):
                        i_ktn_port = ktn_port.getChildByIndex(i)
                        i_ktn_port.setValue(default[i], 0)
            else:
                raise TypeError()
            #
            hint_string = ktn_port.getHintString()
            if hint_string:
                hint_dict = eval(hint_string)
            else:
                hint_dict = {'constant': 'True'}
            #
            hint_dict['label'] = label
            ktn_port.setHintString(
                str(hint_dict)
            )


# noinspection PyMethodMayBeStatic
class NGMacro(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def create_input_port(self, port_path):
        _ = self._ktn_obj.getInputPort(port_path)
        if _ is None:
            self._ktn_obj.addInputPort(port_path)

    def create_output_port(self, port_path):
        _ = self._ktn_obj.getOutputPort(port_path)
        if _ is None:
            self._ktn_obj.addOutputPort(port_path)

    @ktn_cor_base.Modifier.undo_debug_run
    def create_by_configure_file(self, file_path, clear_start=None):
        NGNodeOpt(self._ktn_obj).clear_ports(clear_start)
        #
        configure = ctt_core.Content(value=file_path)
        input_ports = configure.get('input_ports') or []
        #
        NGNodeOpt(self._ktn_obj).set_color(
            configure.get('color')
        )
        #
        for i_input_port_path in input_ports:
            NGNodeOpt(self._ktn_obj).create_input_port(i_input_port_path)
        #
        output_ports = configure.get('output_ports') or []
        for i_output_port_path in output_ports:
            NGNodeOpt(self._ktn_obj).create_output_port(i_output_port_path)
        #
        parameters = configure.get('parameters') or {}
        for k, v in parameters.items():
            k = k.replace('/', '.')
            NGNodeOpt(self._ktn_obj).create_port_by_data(k, v)

    @ktn_cor_base.Modifier.undo_debug_run
    def set_create_to_op_script_by_configure_file(self, file_path, paths=None):
        if paths is not None:
            ktn_op_scripts = [NodegraphAPI.GetNode(i) for i in paths]
        else:
            ktn_op_scripts = NGNodeOpt(self._ktn_obj).get_children(type_includes=['OpScript'])
        for i_ktn_op_script in ktn_op_scripts:
            configure = ctt_core.Content(value=file_path)
            parameters = configure.get('parameters') or {}
            NGNodeOpt(i_ktn_op_script).clear_ports('user')
            for k, v in parameters.items():
                i_k_s = k.replace('/', '.')
                i_k_t = k.replace('/', '__')
                if v.get('widget') != 'button':
                    i_k_t = 'user.{}'.format(i_k_t)
                    NGNodeOpt(i_ktn_op_script).create_port_by_data(i_k_t, v)
                    NGPortOpt(NGNodeOpt(i_ktn_op_script).get_port(i_k_t)).set_expression('getParent().{}'.format(i_k_s))

    def set_sub_op_script_create_by_configure_file(self, file_path, key, paths):
        ktn_op_scripts = [NodegraphAPI.GetNode(i) for i in paths]
        for i_ktn_op_script in ktn_op_scripts:
            configure = ctt_core.Content(value=file_path)
            parameters = configure.get('op_script.{}.parameters'.format(key)) or {}
            NGNodeOpt(i_ktn_op_script).clear_ports('user')
            for k, v in parameters.items():
                k = k.replace('/', '.')
                NGNodeOpt(i_ktn_op_script).create_port_by_data(k, v)
            #
            script = configure.get('op_script.{}.script'.format(key))
            NGNodeOpt(i_ktn_op_script).set('script.lua', script)
