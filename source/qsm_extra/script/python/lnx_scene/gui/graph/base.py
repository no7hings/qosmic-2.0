# coding:utf-8
import six

import enum

from lxgui.qt.core.wrap import *


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
        elif isinstance(value, _SbjBase):
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
                    self.ensure_string(self._indent_prc(depth)+'(\n')
                )
            else:
                lines.append(
                    self.ensure_string(self._indent_prc(depth)+self._key_prc(key)+': '+'(\n')
                )

            c = len(value)
            for i_idx, i in enumerate(value):
                lines.extend(
                    self._next_prc(i, depth+1, None, i_idx==(c-1))
                )

            end_line = self.ensure_string(self._indent_prc(depth)+')')
        else:
            if key is None:
                end_line = self.ensure_string(self._indent_prc(depth)+'()')
            else:
                end_line = self.ensure_string(self._indent_prc(depth)+self._key_prc(key)+': '+'()')

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
                    self._next_prc(i, depth+1, None, i_idx==(c-1))
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
                    self._next_prc(v, depth+1, k, i_idx==(c-1))
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
        if key is None:
            line = self.ensure_string(self._indent_prc(depth)+str(value).lower())
        else:
            line = self.ensure_string(self._indent_prc(depth)+self._key_prc(key)+': '+str(value).lower())

        if is_itr_end is True:
            line += '\n'
        else:
            line += ',\n'
        return [line]

    def _num_prc(self, value, depth, key=None, is_itr_end=False):
        if key is None:
            line = self.ensure_string(self._indent_prc(depth)+str(value))
        else:
            line = self.ensure_string(self._indent_prc(depth)+self._key_prc(key)+': '+str(value))

        if is_itr_end is True:
            line += '\n'
        else:
            line += ',\n'
        return [line]

    def _txt_prc(self, value, depth, key=None, is_itr_end=False):
        value_str = self._default_quotes+self.ensure_string(value)+self._default_quotes
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


class _Dict(object):
    def __init__(self, **kwargs):
        self._dict = dict(**kwargs)

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

    def __str__(self):
        return str(self._dict)

    def __repr__(self):
        return '\n'+self.__str__()

    def get(self, *args, **kwargs):
        return self._dict.get(*args, **kwargs)

    def items(self):
        return self._dict.items()


class _ActionFlags(enum.IntEnum):
    GraphTrackClick = 0x00
    GraphTrackMove = 0x01

    NodePressClick = 0x10
    NodePressMove = 0x11
    NodeViewedClick = 0x12
    NodeEditedClick = 0x13

    PortSourcePressClick = 0x20
    PortSourcePressMove = 0x21
    PortSourceHoverMove = 0x22
    PortTargetPressClick = 0x23
    PortTargetPressMove = 0x24
    PortTargetHoverMove = 0x25

    ConnectionSourcePressClick = 0x30
    ConnectionSourcePressMove = 0x31
    ConnectionSourceHoverMove = 0x32
    ConnectionTargetPressClick = 0x33
    ConnectionTargetPressMove = 0x34
    ConnectionTargetHoverMove = 0x35

    GroupPressClick = 0x40
    GroupPressMove = 0x41
    GroupResizePressClick = 0x42
    GroupResizePressMove = 0x43

    RectSelectPressClick = 0x50
    RectSelectPressMove = 0x51


class _QtSbjTypes(enum.IntEnum):
    Node = 0x00
    InputPort = 0x02
    OutputPort = 0x01
    Connection = 0x04
    Backdrop = 0x05
    Aux = 0x06


class _QtSbjBase:
    SBJ_TYPE = None


class _QtColors:
    NodeBorder = QtGui.QColor(191, 191, 191, 255)
    NodeBackground = QtGui.QColor(95, 95, 95, 255)
    NodeBackgroundBypass = QtGui.QColor(71, 71, 71, 255)

    BackdropBorder = QtGui.QColor(95, 95, 95, 255)
    BackdropBackground = QtGui.QColor(63, 63, 127, 31)
    BackdropName = QtGui.QColor(95, 95, 95, 255)

    PortBorder = QtGui.QColor(71, 71, 71, 255)
    PortBackground = QtGui.QColor(71, 71, 71, 255)

    TypeText = QtGui.QColor(191, 191, 191, 255)
    Text = QtGui.QColor(223, 223, 223)
    TextHover = QtGui.QColor(255, 255, 255)


class _SbjBase(object):
    def __init__(self, item):
        self._item = item

        self._data = _Dict()
        self._gui_data = _Dict()

        self._data.category = ''

        # type
        self._data.type = ''

        # path
        self._data.path = ''

        # name
        self._data.name = ''

    @property
    def data(self):
        return self._data

    @property
    def gui_data(self):
        return self._gui_data

    @property
    def scene(self):
        return self._item.scene()

    @property
    def scene_model(self):
        return self._item.scene()._model

    def get_category(self):
        return self._data.category

    # type
    def set_type(self, text):
        if text is not None:
            self._data.type = text
            return True
        return False

    def get_type(self):
        return self._data.type

    # path
    def set_path(self, path):
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
