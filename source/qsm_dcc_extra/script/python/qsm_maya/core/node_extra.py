# coding:utf-8
import collections

import six
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

from . import node_category as _node_category

from . import node_query as _node_query

from . import node_port_extra as _node_port_extra

from . import material as _material

from . import attribute as _attribute

from . import keyframe as _keyframe


class BscNodeOpt(object):
    PATHSEP = '|'

    def _flatten_port_paths(self, port_paths):
        def rcs_fnc_(port_path_):
            _port_query = node_query.get_port_query(
                port_path_
            )
            _condition = _port_query.is_array(node_path), _port_query.has_channels(node_path)
            # array and channel
            if _condition == (True, True):
                _array_indices = _node_port_extra.BscNodePortOpt(node_path, port_path_).get_array_indices()
                _child_port_names = _port_query.get_channel_names()
                for _i_array_index in _array_indices:
                    for _i_child_port_name in _child_port_names:
                        _i_port_path = '{}[{}].{}'.format(port_path_, _i_array_index, _i_child_port_name)
                        list_.append(_i_port_path)
                        rcs_fnc_(_i_port_path)
            # array
            elif _condition == (True, False):
                _array_indices = _node_port_extra.BscNodePortOpt(node_path, port_path_).get_array_indices()
                for _i_array_index in _array_indices:
                    _i_port_path = '{}[{}]'.format(port_path_, _i_array_index)
                    list_.append(_i_port_path)
                    rcs_fnc_(_i_port_path)
            # channel
            elif _condition == (False, True):
                _child_port_names = _port_query.get_channel_names()
                for _i_child_port_name in _child_port_names:
                    _i_port_path = '{}.{}'.format(port_path_, _i_child_port_name)
                    list_.append(_i_port_path)
                    rcs_fnc_(_i_port_path)
            # all not
            elif _condition == (False, False):
                list_.append(port_path_)

        list_ = []
        node_path = self.get_path()
        node_query = self.get_node_query()
        port_paths.sort()
        for i_port_path in port_paths:
            i_port_query = node_query.get_port_query(
                i_port_path
            )
            if _node_port_extra.BscNodePortOpt.check_exists(node_path, i_port_path) is True:
                # check port is top level
                if i_port_query.has_parent(node_path) is False:
                    # list_.append(i_port_path)
                    rcs_fnc_(i_port_path)
        return list_

    def _filter_port_paths_by_keyable(self, port_paths):
        list_ = []
        node_query = self.get_node_query()
        for i_port_path in port_paths:
            if node_query.get_port_query(i_port_path).is_keyable(self._path) is True:
                list_.append(i_port_path)
        return list_

    @classmethod
    def check_exists(cls, node_path):
        return cmds.objExists(node_path)

    @classmethod
    def create(cls, node_path, type_name):
        if type_name == _node_query.NodeQuery.Types.Material:
            cls.create_material(node_path, type_name)
        elif type_name in _node_category.ShaderCategory.is_shader_type(type_name):
            cls.create_shader(node_path, type_name)
        else:
            _ = cmds.createNode(
                type_name, name=node_path, skipSelect=1
            )

    def __init__(self, name_or_path):
        self._path = _node_query.NodeQuery._to_node_path(name_or_path)
        self._uuid = cmds.ls(self._path, uuid=1)[0]

        self._name = None
        self._type_name = None
        self._node_query = None

    def __str__(self):
        return '{}(type={}, path="{}")'.format(
            self.__class__.__name__,
            self.get_type_name(), self.get_path()
        )

    def __repr__(self):
        return self.__str__()

    @classmethod
    def create_shader(cls, name_or_path, type_name):
        if cls.check_exists(name_or_path) is False:
            category = _node_category.ShaderCategory.get(type_name, 'utility')
            kwargs = dict(
                name=name_or_path,
                skipSelect=1
            )
            if category == 'shader':
                kwargs['asShader'] = 1
            elif category == 'texture':
                kwargs['asTexture'] = 1
            elif category == 'light':
                kwargs['asLight'] = 1
            elif category == 'utility':
                kwargs['asUtility'] = 1
            #
            _ = cmds.shadingNode(type_name, **kwargs)

    @classmethod
    def create_material(cls, name_or_path, type_name):
        if cls.check_exists(name_or_path) is False:
            result = cmds.shadingNode(
                type_name,
                name=name_or_path,
                asUtility=1,
                skipSelect=1
            )
            _material.MaterialLightLink.create(result)

    def clear_array_ports(self):
        ports = self.get_all_ports()
        for port in ports:
            if port.get_port_query().is_array(self.get_path()) is True:
                array_indices = port.get_array_indices()
                for array_index in array_indices:
                    cmds.removeMultiInstance('{}[{}]'.format(port.get_path(), array_index), b=True)

    def get_node_query(self):
        if self._node_query:
            return self._node_query

        _ = _node_query.NodeQuery(
            self.get_type_name()
        )
        self._node_query = _
        return _

    def get_port_query(self, port_path):
        return self.get_node_query().get_port_query(port_path)

    def get_type_name(self):
        if self._type_name is not None:
            return self._type_name

        _ = cmds.nodeType(self.get_path())
        self._type_name = _
        return _

    type_name = property(get_type_name)

    def get_path(self):
        return self._path

    path = property(get_path)

    def get_name(self):
        if self._name is not None:
            return self._name

        _ = bsc_core.BscPathOpt(
            self.get_path()
        ).get_name()
        self._name = _
        return _

    name = property(get_name)

    def update_path(self):
        _ = cmds.ls(self._uuid, long=1)
        if _:
            self._path = _[0]

    def get_parent_path(self):
        _ = cmds.listRelatives(self.get_path(), parent=1, fullPath=1)
        if _:
            return _[0]

    def parent_to_path(self, path):
        if path == self.PATHSEP:
            if cmds.listRelatives(self.get_path(), parent=1):
                cmds.parent(self.get_path(), world=1)
        else:
            if cmds.objExists(path) is True:
                if self.get_parent_path() != path:
                    cmds.parent(self.get_path(), path)

    def get_all_port_paths(self):
        _ = cmds.listAttr(
            self.get_path(),
            read=1,
            write=1,
            inUse=1,
            # fixme: use multi?
            # multi=1
        ) or []
        if _:
            _.sort()
            return self._flatten_port_paths(_)
        return []

    def get_all_keyable_port_paths(self):
        _ = self.get_all_port_paths()
        return self._filter_port_paths_by_keyable(
            self.get_all_port_paths()
        )

    def get_all_ports(self, includes=None):
        if isinstance(includes, (tuple, list)):
            _ = list(includes)
        else:
            _ = self.get_all_port_paths()
        return [
            self.get_port(i) for i in _
        ]

    def get_all_customize_port_paths(self):
        return self._flatten_port_paths(
            cmds.listAttr(self.get_path(), userDefined=1) or []
        )

    def get_all_customize_ports(self, includes=None):
        _ = self.get_all_customize_port_paths()
        if isinstance(includes, (tuple, list)):
            _ = includes
        return [
            self.get_port(i) for i in _ if _node_port_extra.BscNodePortOpt.check_exists(
                self.get_path(), i
            )
        ]

    def create_customize_attributes(self, attributes):
        # 'message',
        # 'bool',
        # 'byte',
        # 'enum',
        # 'typed',
        # 'short',
        # 'float',
        # 'float3',
        # 'compound',
        # 'double',
        # 'time',
        # 'generic',
        # 'doubleLinear',
        # 'doubleAngle',
        # 'matrix',
        # 'long',
        # 'double3',
        # 'lightData',
        # 'addr',
        # 'float2',
        # 'double2',
        # 'double4',
        # 'fltMatrix',
        # 'char',
        # 'floatAngle',
        # 'floatLinear',
        # 'long3',
        # 'short2',
        # 'polyFaces',
        # 'long2'
        node_path = self.get_path()
        for i_port_path, i_value in attributes.items():
            if isinstance(i_value, six.string_types):
                type_name = 'string'
            elif isinstance(i_value, bool):
                type_name = 'bool'
            elif isinstance(i_value, int):
                type_name = 'long'
            elif isinstance(i_value, float):
                type_name = 'double'
            else:
                raise RuntimeError()
            #
            _node_port_extra.BscNodePortOpt.create(
                node_path=node_path,
                port_path=i_port_path,
                type_name=type_name
            )
            #
            port = _node_port_extra.BscNodePortOpt(node_path, i_port_path)
            if i_value is not None:
                port.set(i_value)

    def create_customize_attribute(self, port_path, value):
        if value is not None:
            node_path = self.get_path()
            if isinstance(value, six.string_types):
                type_name = 'string'
            elif isinstance(value, bool):
                type_name = 'bool'
            elif isinstance(value, int):
                type_name = 'long'
            elif isinstance(value, float):
                type_name = 'double'
            else:
                raise RuntimeError()
            #
            _node_port_extra.BscNodePortOpt.create(
                node_path=node_path,
                port_path=port_path,
                type_name=type_name
            )
            #
            port = _node_port_extra.BscNodePortOpt(node_path, port_path)
            port.set(value)

    def get_port(self, port_path):
        return _node_port_extra.BscNodePortOpt(self._path, port_path)

    def reset(self):
        for i_port in self.get_all_ports():
            i_port.set_disconnect()

        for i_port in self.get_all_ports():
            # noinspection PyBroadException
            try:
                i_port.set_default()
            except Exception:
                bsc_core.BscException.set_print()

    def set(self, key, value):
        self.get_port(key).set(value)

    def get(self, key):
        if _node_port_extra.BscNodePortOpt.check_exists(self.get_path(), key) is True:
            return self.get_port(key).get()

    def delete(self):
        cmds.delete(self.get_path())

    def to_dict(self):
        pass

    def get_node_properties(self, includes=None):
        if isinstance(includes, (tuple, list)):
            atr_names = [x for x in includes if _attribute.NodeAttribute.is_exists(self._path, x) is True]
        else:
            atr_names = self.get_all_port_paths()

        dict_ = collections.OrderedDict()
        node_path = self.get_path()
        for i_atr_name in atr_names:
            if _attribute.NodeAttribute.is_exists(node_path, i_atr_name) is False:
                continue

            i_curve_name = _attribute.NodeAttribute.get_source_node(node_path, i_atr_name, 'animCurve')
            if i_curve_name is not None:
                i_curve_type = cmds.nodeType(i_curve_name)
                i_infinities = [
                    _attribute.NodeAttribute.get_value(i_curve_name, 'preInfinity'),
                    _attribute.NodeAttribute.get_value(i_curve_name, 'postInfinity')
                ]
                i_curve_points = _keyframe.NodeAttributeKeyframeOpt(node_path, i_atr_name).get_points()
                dict_[i_atr_name] = dict(
                    flag='animation_curve',
                    data=[
                        i_atr_name, i_curve_type, i_infinities, i_curve_points
                    ]
                )
            else:
                i_value = self.get(i_atr_name)
                dict_[i_atr_name] = dict(
                    flag='value',
                    data=i_value
                )
        return dict_

    def apply_node_properties(self, data, frame_offset=0, force=True, excludes=None):
        for i_atr_name, i_v in data.items():
            if excludes is not None:
                if i_atr_name in excludes:
                    continue

            i_flag = i_v['flag']
            if i_flag == 'value':
                self.set(i_atr_name, i_v['data'])
            elif i_flag == 'animation_curve':
                _keyframe.NodeKeyframe.apply_curve(
                    self._path, i_v['data'], frame_offset=frame_offset, force=force
                )


class BscNodeGraph(object):
    def __init__(self, name_or_path):
        self._path = name_or_path

        self._data_dict = {}
        self._name_dict = {}

    def _node_graph_rcs_fnc(self, node_path):
        dict_ = collections.OrderedDict()
        node_opt = BscNodeOpt(node_path)
        atr_names = node_opt.get_all_port_paths()
        for i_atr_name in atr_names:
            i_curve_name = _attribute.NodeAttribute.get_source_node(node_path, i_atr_name, 'animCurve')
            if i_curve_name:
                i_curve_type = cmds.nodeType(i_curve_name)
                i_infinities = [
                    _attribute.NodeAttribute.get_value(i_curve_name, 'preInfinity'),
                    _attribute.NodeAttribute.get_value(i_curve_name, 'postInfinity')
                ]
                i_curve_points = _keyframe.NodeAttributeKeyframeOpt(node_path, i_atr_name).get_points()
                dict_[i_atr_name] = dict(
                    flag='animation_curve',
                    data=[
                        i_atr_name, i_curve_type, i_infinities, i_curve_points
                    ]
                )
            else:
                i_source_args = node_opt.get_port(i_atr_name).get_source_args()
                if i_source_args:
                    i_source_node, i_source_port_path = i_source_args
                    # print i_source_node
                else:
                    i_value = node_opt.get(i_atr_name)
                    dict_[i_atr_name] = dict(
                        flag='value',
                        data=i_value
                    )

        self._data_dict[node_path] = dict_

    def generate(self):
        self._data_dict = {}
        self._name_dict = {}

        self._node_graph_rcs_fnc(self._path)
        return self._data_dict
