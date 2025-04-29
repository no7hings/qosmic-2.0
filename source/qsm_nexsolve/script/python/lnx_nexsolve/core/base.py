# coding:utf-8
import six

import json

import collections

import re

import enum

import lxbasic.core as bsc_core


class DataTypes:
    String = 'String'
    StringArray = 'StringArray'

    Integer = 'Integer'
    IntegerArray = 'IntegerArray'

    Float = 'Float'
    FloatArray = 'FloatArray'

    Boolean = 'Boolean'
    BooleanArray = 'BooleanArray'

    Dict = 'Dict'


class EntityTypes(enum.IntEnum):
    Node = 0x00

    Port = 0x01
    InputPort = 0x02
    OutputPort = 0x03

    Parameter = 0x04

    Connection = 0x05
    Backdrop = 0x06
    Aux = 0x07


class ParamTypes:
    Group = 'Group'

    Custom = 'Custom'

    String = 'String'
    StringArray = 'StringArray'

    Integer = 'Integer'
    IntegerArray = 'IntegerArray'

    Float = 'Float'
    FloatArray = 'FloatArray'

    Boolean = 'Boolean'
    BooleanArray = 'BooleanArray'

    Dict = 'Dict'


class _ToJson(object):
    @staticmethod
    def ensure_string(s):
        if isinstance(s, six.text_type):
            if six.PY2:
                return s.encode('utf-8')
        elif isinstance(s, six.binary_type):
            if six.PY3:
                return s.decode('utf-8')
        return s

    def __init__(self, value):
        self._indent = 4
        self._default_quotes = self.ensure_string('"')
        self._data = value

        self._lines = self._next_prc(value, 0, None, True)

    def _key_prc(self, value):
        if isinstance(value, bool):
            return self.ensure_string(str(value).lower())
        elif isinstance(value, (int, float)):
            return self.ensure_string(str(value))
        elif isinstance(value, six.string_types):
            return self._default_quotes+self.ensure_string(value)+self._default_quotes
        elif isinstance(value, tuple):
            return self._tuple_key_prc(value)
        return self._default_quotes+str(type(value))+self._default_quotes

    def _tuple_key_prc(self, value):
        return '({})'.format(', '.join([self._subkey_prc(i) for i in value]))

    def _subkey_prc(self, value):
        if isinstance(value, bool):
            return self.ensure_string(str(value).lower())
        elif isinstance(value, (int, float)):
            return self.ensure_string(str(value))
        elif isinstance(value, six.string_types):
            return self._default_quotes+self.ensure_string(value)+self._default_quotes
        return str(type(value))

    def _indent_prc(self, depth):
        return depth*self._indent*' '

    def _next_prc(self, value, depth, key=None, is_itr_end=False):
        if value is None:
            return self._none_value_prc(value, depth, key, is_itr_end)
        elif isinstance(value, bool):
            return self._bool_prc(value, depth, key, is_itr_end)
        elif isinstance(value, (int, float)):
            return self._num_prc(value, depth, key, is_itr_end)
        elif isinstance(value, six.string_types):
            return self._txt_prc(value, depth, key, is_itr_end)
        elif isinstance(value, tuple):
            return self._tuple_prc(value, depth, key, is_itr_end)
        elif isinstance(value, list):
            return self._list_prc(value, depth, key, is_itr_end)
        elif isinstance(value, set):
            return self._list_prc(value, depth, key, is_itr_end)
        elif isinstance(value, dict):
            return self._dict_prc(value, depth, key, is_itr_end)
        elif isinstance(value, _Dict):
            return self._dict_prc(value._dict, depth, key, is_itr_end)
        elif isinstance(value, (_SbjBase, _ParamBase, _StageBase)):
            return self._dict_prc(value._data._dict, depth, key, is_itr_end)
        else:
            return self._error_value_prc(value, depth, key, is_itr_end)

    def _none_value_prc(self, value, depth, key=None, is_itr_end=False):
        if key is None:
            line = self.ensure_string(self._indent_prc(depth)+'null')
        else:
            line = self.ensure_string(self._indent_prc(depth)+self._key_prc(key)+': '+'null')

        if is_itr_end is True:
            line += '\n'
        else:
            line += ',\n'
        return [line]

    def _error_value_prc(self, value, depth, key=None, is_itr_end=False):
        value_str = self._default_quotes+str(type(value))+self._default_quotes
        if key is None:
            line = self.ensure_string(self._indent_prc(depth)+value_str)
        else:
            line = self.ensure_string(self._indent_prc(depth)+self._key_prc(key)+': '+value_str)

        if is_itr_end is True:
            line += '\n'
        else:
            line += ',\n'
        return [line]

    def _tuple_prc(self, value, depth, key=None, is_itr_end=False):
        lines = []
        if value:
            if key is None:
                lines.append(
                    self.ensure_string(self._indent_prc(depth)+'[\n')
                )
            else:
                lines.append(
                    self.ensure_string(self._indent_prc(depth)+self._key_prc(key)+': '+'[\n')
                )

            c = len(value)
            for i_idx, i in enumerate(value):
                lines.extend(
                    self._next_prc(i, depth+1, None, i_idx == (c-1))
                )

            end_line = self.ensure_string(self._indent_prc(depth)+']')
        else:
            if key is None:
                end_line = self.ensure_string(self._indent_prc(depth)+'[]')
            else:
                end_line = self.ensure_string(self._indent_prc(depth)+self._key_prc(key)+': '+'[]')

        if is_itr_end is True:
            end_line += '\n'
        else:
            end_line += ',\n'

        lines.append(end_line)
        return lines

    def _list_prc(self, value, depth, key=None, is_itr_end=False):
        lines = []

        if value:
            if key is None:
                lines.append(
                    self.ensure_string(self._indent_prc(depth)+'[\n')
                )
            else:
                lines.append(
                    self.ensure_string(self._indent_prc(depth)+self._key_prc(key)+': '+'[\n')
                )

            c = len(value)
            for i_idx, i in enumerate(value):
                lines.extend(
                    self._next_prc(i, depth+1, None, i_idx == (c-1))
                )

            end_line = self.ensure_string(self._indent_prc(depth)+']')
        else:
            if key is None:
                end_line = self.ensure_string(self._indent_prc(depth)+'[]')
            else:
                end_line = self.ensure_string(self._indent_prc(depth)+self._key_prc(key)+': '+'[]')

        if is_itr_end is True:
            end_line += '\n'
        else:
            end_line += ',\n'

        lines.append(end_line)
        return lines

    def _dict_prc(self, value, depth, key=None, is_itr_end=False):
        lines = []

        if value:
            if key is None:
                lines.append(
                    self.ensure_string(self._indent_prc(depth)+'{\n')
                )
            else:
                lines.append(
                    self.ensure_string(self._indent_prc(depth)+self._key_prc(key)+': '+'{\n')
                )

            c = len(value)
            for i_idx, (k, v) in enumerate(value.items()):
                lines.extend(
                    self._next_prc(v, depth+1, k, i_idx == (c-1))
                )

            end_line = self.ensure_string(self._indent_prc(depth)+'}')
        else:
            if key is None:
                end_line = self.ensure_string(self._indent_prc(depth)+'{}')
            else:
                end_line = self.ensure_string(self._indent_prc(depth)+self._key_prc(key)+': '+'{}')

        if is_itr_end is True:
            end_line += '\n'
        else:
            end_line += ',\n'

        lines.append(end_line)
        return lines

    def _bool_prc(self, value, depth, key=None, is_itr_end=False):
        value_str = json.dumps(value)
        if key is None:
            line = self.ensure_string(self._indent_prc(depth)+value_str)
        else:
            line = self.ensure_string(self._indent_prc(depth)+self._key_prc(key)+': '+value_str)

        if is_itr_end is True:
            line += '\n'
        else:
            line += ',\n'
        return [line]

    def _num_prc(self, value, depth, key=None, is_itr_end=False):
        value_str = json.dumps(value)
        if key is None:
            line = self.ensure_string(self._indent_prc(depth)+value_str)
        else:
            line = self.ensure_string(self._indent_prc(depth)+self._key_prc(key)+': '+value_str)

        if is_itr_end is True:
            line += '\n'
        else:
            line += ',\n'
        return [line]

    def _txt_prc(self, value, depth, key=None, is_itr_end=False):
        value_str = json.dumps(value)
        if key is None:
            line = self.ensure_string(self._indent_prc(depth)+value_str)
        else:
            line = self.ensure_string(self._indent_prc(depth)+self._key_prc(key)+': '+value_str)

        if is_itr_end is True:
            line += '\n'
        else:
            line += ',\n'
        return [line]

    def generate(self):
        return self.ensure_string(''.join(self._lines))


class _SbjGuiBase:
    ENTITY_TYPE = None

    MODEL_CLS = None


class _Base(object):
    ENTITY_TYPE = None
    
    ATTR_SEP = '.'
    CONNECT_SEP = '->'

    @classmethod
    def _find_next_node_path(cls, path_set, prefix, parent_path=None, **kwargs):
        parent_path = parent_path or ''
        path = '{}/{}'.format(parent_path, prefix)
        if path not in path_set:
            return path

        text, number = cls._to_name_args(prefix)
        if number:
            idx = int(number)
        else:
            idx = 1

        new_path = path
        while new_path in path_set:
            new_path = '{}/{}{}'.format(parent_path, text, idx)
            idx += 1

        if new_path not in path_set:
            return new_path

    @classmethod
    def _find_next_port_path(cls, paths, prefix, parent_path=None):
        if parent_path is None:
            port_path = prefix
        else:
            port_path = '{}.{}'.format(parent_path, prefix)

        if port_path not in paths:
            return port_path

        text, number = cls._to_name_args(prefix)
        if number:
            idx = int(number)
        else:
            idx = 1

        new_path = port_path
        while new_path in paths:
            if parent_path is None:
                new_path = '{}{}'.format(text, idx)
            else:
                new_path = '{}.{}'.format(parent_path, text)

            idx += 1

        if new_path not in paths:
            return new_path

    @classmethod
    def _find_next_param_path(cls, paths, prefix, parent_path=None):
        if parent_path is None:
            port_path = prefix
        else:
            port_path = '{}.{}'.format(parent_path, prefix)

        if port_path not in paths:
            return port_path

        text, number = cls._to_name_args(prefix)
        if number:
            idx = int(number)
        else:
            idx = 1

        new_path = port_path
        while new_path in paths:
            if parent_path is None:
                new_path = '{}{}'.format(text, idx)
            else:
                new_path = '{}.{}'.format(parent_path, text)

            idx += 1

        if new_path not in paths:
            return new_path

    @classmethod
    def _json_str_to_data(cls, json_str):
        # print(json_str)
        return json.loads(
            json_str, object_pairs_hook=collections.OrderedDict
        )

    # connection
    @classmethod
    def _join_to_connection_path(cls, source_path, target_path):
        return cls.CONNECT_SEP.join([source_path, target_path])

    @classmethod
    def _split_to_connection_args(cls, path):
        return path.split(cls.CONNECT_SEP)

    @classmethod
    def _get_connection_source(cls, root_model, path):
        source_path, _ = path.split(cls.CONNECT_SEP)
        node_path, port_path = bsc_core.BscAttributePath.split_by(source_path)
        return root_model.get_node(node_path).get_output(port_path)

    @classmethod
    def _get_connection_target(cls, root_model, path):
        _, target_path = path.split(cls.CONNECT_SEP)
        node_path, port_path = bsc_core.BscAttributePath.split_by(target_path)
        return root_model.get_node(node_path).get_input(port_path)

    # attribute
    @classmethod
    def _join_to_attr_path(cls, node_path, port_path):
        return cls.ATTR_SEP.join([node_path, port_path])

    @classmethod
    def _to_name_args(cls, name):
        match = re.match(r'([^\d]*)(\d*)$', name)
        if match:
            return match.group(1), match.group(2)
        return name, ''


class _SbjBase(_Base):

    def __init__(self, gui):
        self._gui_language = bsc_core.BscEnviron.get_gui_language()

        self._root_model = None

        self._gui = gui

        self._data = _Dict()
        self._builtin_data = _Dict()
        self._gui_data = _Dict()

        # category
        self._data.category = ''

        # type
        self._data.type = ''

        # path
        self._data.path = ''

        # name
        self._data.name = ''

        # version
        self._data.version = '0.0.0'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.get_path() == other.get_path()
        return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.get_path() != other.get_path()
        return True

    @property
    def data(self):
        return self._data

    @property
    def gui_data(self):
        return self._gui_data

    @property
    def scene(self):
        return self._gui.scene()

    def _set_root_model(self, model):
        self._root_model = model

    def get_root_model(self):
        if self._root_model is not None:
            return self._root_model
        return self._gui.scene()._model

    @property
    def root_model(self):
        if self._root_model is not None:
            return self._root_model
        return self._gui.scene()._model

    def update_root_gui(self):
        self.root_model._gui.update()

    def get_category(self):
        return self._data.category

    # type
    def _set_type(self, text, *args, **kwargs):
        if text is not None:
            self._data.type = text
            return True
        return False

    def get_type(self):
        return self._data.type

    def _set_version(self, text):
        if text is not None:
            self._data.version = text
            return True
        return False

    def get_version(self):
        return self._data.version

    # path
    def _set_path(self, path):
        self._data.path = path

    def get_path(self):
        return self._data.path

    # name
    def set_name(self, text):
        if text is not None:
            self._data.name = text
            return True
        return False

    def get_name(self):
        return self._data.name


class _PortBase(_SbjBase):
    ENTITY_TYPE = EntityTypes.Port

    def __init__(self, *args, **kwargs):
        super(_PortBase, self).__init__(*args, **kwargs)

        self._node = None

        self._data.port_path = ''

    def set_name(self, text):
        if super(_PortBase, self).set_name(text) is True:
            self._gui._name_aux.setPlainText(text)
            self._gui._update()

    def _set_port_path(self, port_path):
        self._data.port_path = port_path

    def get_port_path(self):
        return self._data.port_path

    def _set_node(self, node):
        self._node = node

    @property
    def node(self):
        return self._node

    def get_node(self):
        return self._node

    def get_root_model(self):
        return self._node.get_root_model()

    @property
    def root_model(self):
        return self._node.get_root_model()


class _ParamBase(_Base):
    PARAM_TYPE = None

    ENTITY_TYPE = EntityTypes.Parameter

    def __init__(self, root_model, node_path):
        self._gui_language = bsc_core.BscEnviron.get_gui_language()

        self._root_model = root_model
        self._node_path = node_path

        self._data = _Dict()

        # category
        self._data.category = ''

        # type
        self._data.type = ''

        # port path
        self._data.param_path = ''

        # name
        self._data.name = ''

    @property
    def data(self):
        return self._data

    # category
    def get_category(self):
        return self._data.category

    # type
    def _set_type(self, text, *args, **kwargs):
        if text is not None:
            self._data.type = text
            return True
        return False

    def get_type(self):
        return self._data.type

    def get_path(self):
        return bsc_core.BscAttributePath.join_by(self._node_path, self._data.param_path)

    # name
    def set_name(self, text):
        if text is not None:
            self._data.name = text
            return True
        return False

    def get_name(self):
        return self._data.name

    def _set_param_path(self, param_path):
        self._data.param_path = param_path

    def get_param_path(self):
        return self._data.param_path

    @property
    def node(self):
        return self._root_model.get_node(self._node_path)

    def get_node(self):
        return self._root_model.get_node(self._node_path)

    def get_root_model(self):
        return self._root_model

    @property
    def root_model(self):
        return self._root_model


class _StageBase(object):
    pass


class _Dict(object):
    def __init__(self, **kwargs):
        self._dict = collections.OrderedDict(**kwargs)

    def __getattr__(self, key):
        return self._dict[key]

    def __setattr__(self, key, value):
        if key in {'_dict'}:
            self.__dict__[key] = value
        else:
            self._dict[key] = value

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __contains__(self, item):
        return item in self._dict

    def __str__(self):
        return _ToJson(self._dict)

    def __repr__(self):
        return '\n'+self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._dict == other._dict
        return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self._dict != other._dict
        return True

    def get(self, *args, **kwargs):
        return self._dict.get(*args, **kwargs)

    def items(self):
        return self._dict.items()

    def update(self, **kwargs):
        self._dict.update(**kwargs)


class _ActionBase(object):
    NAME = 'DropMayaScene'

    INSTANCE_DICT = dict()

    def __new__(cls, *args, **kwargs):
        name, root_model = args[:2]
        if name in cls.INSTANCE_DICT:
            return cls.INSTANCE_DICT[name]

        self = super(_ActionBase, cls).__new__(cls)

        self._name = name
        self._root_model = root_model

        cls.INSTANCE_DICT[name] = self
        return self

    def __str__(self):
        return 'DropAction({})'.format(
            self._name
        )

    def __repr__(self):
        return '\n'+self.__str__()

    def filter_file(self, file_path):
        # use for check file path is match this action
        return False

    def accept_file(self, file_path, index=0):
        # do something
        return False
