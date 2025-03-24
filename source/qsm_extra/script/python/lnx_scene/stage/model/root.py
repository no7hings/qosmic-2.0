# coding:utf-8
import collections

import json

from ...core import base as _scn_cor_base

from ...core import path as _scn_cor_path

from ..core import cel as _cor_cel


class _TypedValue(_scn_cor_base._StageBase):
    def __init__(self, data_type, data):
        self._data = _scn_cor_base._Dict(
            type=data_type,
            data=data,
        )

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._data == other._data
        return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self._data != other._data
        return True

    def set(self, data):
        if data != self._data.data:
            self._data.data = data

    def get(self):
        return self._data.data


class AttrFactory:
    @staticmethod
    def add(data_type):
        def decorator(fnc):
            def wrapper(self, data, *args, **kwargs):
                self.set_value(
                    _TypedValue(data_type, data)
                )
                fnc(self, data, *args, **kwargs)
            return wrapper
        return decorator


class _Attr(_scn_cor_base._StageBase):
    def __init__(self, node_path, key):
        self._data = _scn_cor_base._Dict(
            value=None
        )

        self._node_path = node_path
        self._atr_key = key

        self._path = '{}.{}'.format(self._node_path, key)

    @property
    def path(self):
        return self._path

    def get_value(self):
        return self._data.value

    def set_value(self, typed_value):
        if typed_value != self._data.value:
            self._data.value = typed_value
            return True
        return False

    def set_data(self, data):
        return self._data.value.set(data)

    def get_data(self):
        return self._data.value.get()

    def create_auto(self, data_type, data):
        self.set_value(
            _TypedValue(data_type, data)
        )

    @AttrFactory.add(_scn_cor_base.DataTypes.String)
    def create_string(self, data):
        pass

    @AttrFactory.add(_scn_cor_base.DataTypes.Integer)
    def create_integer(self, data):
        pass

    @AttrFactory.add(_scn_cor_base.DataTypes.Float)
    def create_float(self, data):
        pass

    @AttrFactory.add(_scn_cor_base.DataTypes.StringArray)
    def create_string_array(self, data):
        pass

    @AttrFactory.add(_scn_cor_base.DataTypes.Dict)
    def create_dict(self, data):
        pass

    @AttrFactory.add(_scn_cor_base.DataTypes.IntegerArray)
    def create_integer_array(self, data):
        pass

    @AttrFactory.add(_scn_cor_base.DataTypes.FloatArray)
    def create_float_array(self, data):
        pass


class _Node(_scn_cor_base._StageBase):
    def __init__(self, node_type, path):
        self._data = _scn_cor_base._Dict(
            type=node_type,
            attrs=collections.OrderedDict()
        )

        self._path = path

    def __str__(self):
        return '{}({})'.format(
            self._data.type,
            self._path
        )

    def __repr__(self):
        return '\n'+self.__str__()

    @property
    def path(self):
        return self._path

    def add_attr(self, key):
        if key in self._data.attrs:
            return self._data.attrs[key]

        attr = _Attr(self._path, key)
        self._data.attrs[key] = attr
        return attr

    def set_attr(self, key, typed_value):
        return self.add_attr(key).set_value(typed_value)

    def get_attr(self, key):
        return self._data.attrs.get(key)

    def set_data(self, key, data):
        attr = self.get_attr(key)
        if attr:
            return attr.set_data(data)
        return False

    def get_data(self, key):
        attr = self.get_attr(key)
        if attr:
            return attr.get_data()

    @classmethod
    def create_from_data(cls, stage, path, data):
        node_type = data['type']
        node = stage.add_node(node_type, path)
        attrs = data['attrs']
        for k, v in attrs.items():
            i_attr = node.add_attr(k)
            i_value = v['value']
            i_attr.create_auto(i_value['type'], i_value['data'])
        return node

    def get(self, key):
        if key == 'type':
            return self._data.type
        else:
            return self.get_data(key)

    def exist(self, key):
        if key == 'type':
            return True
        else:
            return bool(self.get_attr(key))

    def match_exp(self, exp):
        # noinspection PyUnusedLocal
        attr = self.get
        # noinspection PyUnusedLocal,PyShadowingBuiltins
        hasattr = self.exist
        # noinspection PyBroadException
        try:
            return eval(exp)
        except Exception:
            return False


class StageRoot(_scn_cor_base._StageBase):
    def __init__(self):
        self._data = _scn_cor_base._Dict(
            nodes=collections.OrderedDict()
        )

    def __str__(self):
        return _scn_cor_base._ToJson(
            self._data._dict
        ).generate()

    def __repr__(self):
        return '\n'+self.__str__()

    def _auto_complete(self, path):
        ancestors = _scn_cor_path.PathOpt(path).get_ancestors()
        if ancestors:
            ancestors.reverse()
        for i in ancestors:
            if i not in self._data.nodes:
                self._add_group(i)

    def _add_group(self, path):
        node = _Node('group', path)
        self._data.nodes[path] = node

    def add_node(self, node_type, path):
        if path in self._data.nodes:
            return self._data.nodes[path]

        self._auto_complete(path)

        node = _Node(node_type, path)
        self._data.nodes[path] = node
        return node

    def to_json(self):
        return _scn_cor_base._ToJson(
            self._data._dict
        ).generate()

    def to_data(self):
        return json.loads(
            self.to_json(),
            object_pairs_hook=collections.OrderedDict
        )
    
    @classmethod
    def create_from_json(cls, json_str):
        return cls.create_from_data(
            json.loads(
                json_str,
                object_pairs_hook=collections.OrderedDict
            )
        )
    
    @classmethod
    def create_from_data(cls, data):
        nodes = data['nodes']
        stage = cls()
        for k, v in nodes.items():
            _Node.create_from_data(stage, k, v)
        return stage

    def get_node_paths(self):
        return list(self._data.nodes.keys())

    def get_nodes(self):
        return list(self._data.nodes.values())

    def get_node(self, path):
        return self._data.nodes.get(path)

    def find_nodes(self, cel_str):
        return _cor_cel.CEL(self, cel_str).fetchall()
