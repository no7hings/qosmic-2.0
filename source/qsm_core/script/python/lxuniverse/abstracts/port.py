# coding:utf-8
import six

import lxcontent.core as ctt_core
# universe
from .. import core as unr_core

from . import base as unr_abs_base


# port/def
class AbsPortBaseDef(object):
    OBJ_TOKEN = None
    PATHSEP = None

    def _init_port_base_def_(self, obj, type_path, port_path, port_assign):
        self._obj = obj
        if isinstance(type_path, six.string_types):
            _type = self.obj.universe._get_type(type_path)
        else:
            _type = type_path
        #
        self._type = _type
        self._port_path = port_path
        self._port_name = port_path.split(self.PATHSEP)[-1]
        self._port_assign = port_assign
        #
        self._is_custom = False

    # obj
    @property
    def obj(self):
        return self._obj

    @property
    def obj_path(self):
        return self.obj.path

    @property
    def category(self):
        return self.type.category

    @property
    def category_name(self):
        return self.category.name

    @property
    def type(self):
        return self._type

    @property
    def type_path(self):
        return self.type.path

    @property
    def type_name(self):
        return self.type.name

    @property
    def name(self):
        return self._port_name

    # obj
    @property
    def path(self):
        return self.PATHSEP.join(
            (self.obj.path, self.port_path)
        )

    @property
    def token(self):
        return self.PATHSEP.join(
            (self.obj.path, self.port_token)
        )

    @property
    def query_path(self):
        return ''

    # port
    @property
    def port_path(self):
        return self._port_path

    @property
    def port_name(self):
        return self._port_name

    @property
    def port_token(self):
        port_assign = self.port_assign
        port_path = self.port_path
        return self.OBJ_TOKEN._get_port_token_(
            port_assign, port_path
        )

    @property
    def pathsep(self):
        return self.PATHSEP

    # port_assign
    @property
    def port_assign(self):
        return self._port_assign

    def get_is_element(self):
        raise NotImplementedError

    def get_is_channel(self):
        raise NotImplementedError

    # port_assign
    def get_is_input_port(self):
        return self.port_assign == unr_core.UnrPortAssign.INPUTS

    def get_is_output_port(self):
        return self.port_assign == unr_core.UnrPortAssign.OUTPUTS

    # gain
    def _get_stack_key_(self):
        return self.port_token

    #
    def _get_element_port_path_(self, element_index):
        format_dict = {
            'pathsep': self.PATHSEP,
            'port_path': self.port_path,
            'element_index': element_index
        }
        return unr_core.UnrPort.ELEMENT_PATH_FORMAT.format(**format_dict)

    def _get_channel_port_path_(self, channel_name):
        format_dict = {
            'pathsep': self.PATHSEP,
            'port_path': self.port_path,
            'channel_name': channel_name
        }
        return unr_core.UnrPort.CHANNEL_PATH_FORMAT.format(**format_dict)

    def set_custom(self, boolean):
        self._is_custom = boolean

    def get_is_custom(self):
        return self._is_custom

    def _format_dict_(self):
        return {
            'obj': self.obj,
            'parent': self.parent,
            'type': self.type,
            'name': self.name,
            'port_assign': self.port_assign,
            'path': self.path,
            'port_path': self.port_path,
            'token': self.token,
            'port_token': self.port_token
        }

    @classmethod
    def _get_port_token_(cls, port_path, port_assign):
        format_dict = {
            'port_assign_pathsep': cls.PATHSEP,
            'port_path': port_path,
            'port_assign': port_assign
        }
        return unr_core.UnrPort.PORT_TOKEN_FORMAT.format(**format_dict)

    @classmethod
    def _get_channel_path_(cls, port_path, channel_name):
        format_dict = {
            'pathsep': cls.PATHSEP,
            'port_path': port_path,
            'channel_name': channel_name
        }
        return unr_core.UnrPort.CHANNEL_PATH_FORMAT.format(**format_dict)

    @property
    def parent(self):
        raise NotImplementedError()

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.type.path,
            self.path,
        )

    def __repr__(self):
        return self.__str__()


class AbsPortSourceExtraDef(object):
    """
    <output-port> >> self
    """
    OBJ_TOKEN = None

    def _init_port_source_extra_def_(self):
        pass

    @property
    def obj(self):
        raise NotImplementedError()

    @property
    def obj_path(self):
        return self.obj.path

    @property
    def port_path(self):
        raise NotImplementedError()

    # source
    def get_source_exists(self):
        universe = self.obj.universe
        #
        source_obj_path = '*'
        source_port_path = '*'
        target_obj_path = self.obj.path
        target_port_path = self.port_path
        regex = self.OBJ_TOKEN._get_obj_connection_token_(
            source_obj_path, source_port_path, target_obj_path, target_port_path
        )
        return universe.get_connections_exists(regex=regex)

    def get_source_connection(self):
        universe = self.obj.universe
        #
        source_obj_path = '*'
        source_port_path = '*'
        target_obj_path = self.obj.path
        target_port_path = self.port_path
        regex = self.OBJ_TOKEN._get_obj_connection_token_(
            source_obj_path, source_port_path, target_obj_path, target_port_path
        )
        connections = universe.get_connections(regex=regex)
        if connections:
            return connections[-1]

    def get_source(self):
        source_connection = self.get_source_connection()
        if source_connection:
            return source_connection.source

    def connect_from(self, output_port):
        source_obj_args = output_port.obj_path
        source_port_args = output_port.port_path
        target_obj_args = self.obj_path
        target_port_args = self.port_path
        #
        return self.obj.universe.set_connection_create(
            source_obj_args, source_port_args,
            target_obj_args, target_port_args
        )

    def set_source(self, output_port):
        self.connect_from(output_port)

    def _format_dict_(self):
        raise NotImplementedError()


class AbsPortTargetExtraDef(object):
    """
    self >> [<input-port>, ...]
    """
    OBJ_TOKEN = None

    def _init_port_target_extra_def_(self):
        pass

    @property
    def obj(self):
        raise NotImplementedError()

    @property
    def obj_path(self):
        return self.obj.path

    @property
    def port_path(self):
        raise NotImplementedError()

    # target
    def get_targets_exists(self):
        universe = self.obj.universe
        #
        source_obj_path = self.obj.path
        source_port_path = self.port_path
        target_obj_path = '*'
        target_port_path = '*'
        regex = self.OBJ_TOKEN._get_obj_connection_token_(
            source_obj_path, source_port_path, target_obj_path, target_port_path
        )
        return universe.get_connections_exists(regex=regex)

    def get_target_connections(self):
        universe = self.obj.universe
        #
        source_obj_path = self.obj.path
        source_port_path = self.port_path
        target_obj_path = '*'
        target_port_path = '*'
        regex = self.OBJ_TOKEN._get_obj_connection_token_(
            source_obj_path, source_port_path, target_obj_path, target_port_path
        )
        return universe.get_connections(regex=regex)

    def get_targets(self):
        target_connections = self.get_target_connections()
        return [i.target for i in target_connections]

    def connect_to(self, input_port):
        source_obj_args = self.obj_path
        source_port_args = self.port_path
        target_obj_args = input_port.obj_path
        target_port_args = input_port.port_path
        #
        return self.obj.universe.set_connection_create(
            source_obj_args, source_port_args,
            target_obj_args, target_port_args
        )

    def set_target(self, input_port):
        self.connect_to(input_port)

    def _format_dict_(self):
        raise NotImplementedError()


class AbsPortElementExtraDef(object):
    PORT_ELEMENT_STACK_CLS = None
    PORT_ELEMENT_CLS = None

    # init
    def _init_port_element_extra_def_(self):
        self._port_element_stack = self.PORT_ELEMENT_STACK_CLS()

    @property
    def obj(self):
        raise NotImplementedError()

    @property
    def port_assign(self):
        raise NotImplementedError()

    # method
    def _set_element_add_(self, port_element):
        self._port_element_stack.set_object_add(port_element)
        # add to obj
        self.obj._add_port_(port_element)

    def _set_element_create_(self, index):
        port_element = self.PORT_ELEMENT_CLS(self, index)
        self._set_element_add_(port_element)
        return port_element

    def get_elements_exists(self, regex=None):
        return self._port_element_stack.get_objects_exists(regex)

    def get_element_indices(self):
        return self._port_element_stack.get_object_indices()

    def get_elements(self, regex=None):
        return self._port_element_stack.get_objects(regex)

    def get_element_exists(self, index):
        return self._port_element_stack.get_object_exists(index)

    def get_element(self, index):
        return self._port_element_stack.get_object_at(index)

    def get_element_at(self, index):
        return self._port_element_stack.get_object_at(index)

    def __getitem__(self, index):
        return self.get_element(index)


class AbsPortChannelExtraDef(object):
    PORT_CHANNEL_STACK_CLS = None
    PORT_CHANNEL_CLS = None

    # init
    def _init_port_channel_extra_def_(self):
        self._channel_stack = self.PORT_CHANNEL_STACK_CLS()

    @property
    def obj(self):
        raise NotImplementedError()

    @property
    def port_assign(self):
        raise NotImplementedError()

    # method
    def _set_channel_add_(self, channel):
        # add to parent
        self._channel_stack.set_object_add(channel)
        # add to obj
        self.obj._add_port_(channel)

    def _set_channel_create_(self, name):
        channel = self.PORT_CHANNEL_CLS(self, name)
        self._set_channel_add_(channel)
        return channel

    def get_channels_exists(self, regex=None):
        return self._channel_stack.get_objects_exists(regex)

    def get_channel_names(self):
        return self._channel_stack.get_keys()

    def get_channels(self, regex=None):
        return self._channel_stack.get_objects(regex)

    def get_channel_exists(self, channel_name):
        return self._channel_stack.get_object_exists(channel_name)

    def get_channel(self, channel_name):
        """
        :param channel_name: str(channel_name)
        :return: instance(Channel)
        """
        return self._channel_stack.get_object(channel_name)

    def get_channel_index(self, channel_name):
        """
        :param channel_name: str(channel_name)
        :return: int(index)
        """
        return self._channel_stack.get_index(channel_name)

    def get_channel_at(self, index):
        return self._channel_stack.get_object_at(index)

    def __getitem__(self, index):
        return self.get_channel_at(index)


class AbsPortValueExtraDef(object):
    def _init_port_value_extra_def_(self):
        self._value = self.type.set_value_create(None)
        self._value_default = self.type.set_value_create(None)
        #
        self._is_enumerate = False
        self._enumerate_raw = []

    @property
    def parent(self):
        raise NotImplementedError()

    @property
    def type(self):
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()

    def get_value(self):
        return self._value

    # <value-default>
    def get_value_default(self):
        return self._value_default

    def set(self, raw):
        self.get_value().set(raw)

    def set_default(self, raw):
        self.get_value_default().set(raw)

    def get(self):
        return self.get_value().get()

    def get_as_string(self):
        return self.get_value().get_as_string()

    def get_as_obj(self):
        return self.get_value().get_as_obj()

    def get_default(self):
        return self.get_default().get()

    def get_is_value_changed(self):
        return self._value != self._value_default

    def set_enumerate(self, boolean):
        self._is_enumerate = boolean

    def get_is_enumerate(self):
        return self._is_enumerate

    def set_enumerate_raw(self, enumerate_raw):
        self._enumerate_raw = enumerate_raw

    def get_enumerate_strings(self):
        return self._enumerate_raw

    def get_as_index(self):
        if self.get_is_enumerate():
            raw = self.get()
            return self.get_enumerate_strings().index(raw)


class AbsPortChannelValueExtraDef(object):
    @property
    def type(self):
        raise NotImplementedError()

    @property
    def parent(self):
        raise NotImplementedError()

    @property
    def index(self):
        raise NotImplementedError()

    def get_value(self):
        return self.parent.get_value().get_channel(self.index)

    def get(self):
        return self.get_value().get()

    def get_as_string(self):
        return self.get_value().get_as_string()

    def get_as_obj(self):
        return self.get_value().get_as_obj()


class AbsPortElementValueExtraDef(object):
    @property
    def type(self):
        raise NotImplementedError()

    @property
    def parent(self):
        raise NotImplementedError()

    @property
    def index(self):
        raise NotImplementedError()

    def get_value(self):
        return self.parent.get_value().get_element(self.index)

    def get(self):
        return self.get_value().get()

    def get_as_string(self):
        return self.get_value().get_as_string()

    def get_as_obj(self):
        return self.get_value().get_as_obj()


class AbsPortChannel(
    # <port>
    AbsPortBaseDef,
    # <port-source>
    AbsPortSourceExtraDef,
    # <port-target>
    AbsPortTargetExtraDef,
    # <port-value>
    AbsPortChannelValueExtraDef
):
    def __init__(self, parent, name):
        self._parent = parent
        # port
        self._init_port_base_def_(
            parent.obj, parent.type,
            name, parent.port_assign
        )
        self._init_port_source_extra_def_()
        self._init_port_target_extra_def_()

    @property
    def obj(self):
        return self.parent.obj

    @property
    def type(self):
        return self.parent.type

    #
    @property
    def parent(self):
        return self._parent

    @property
    def port_path(self):
        return self.parent._get_channel_port_path_(
            self.name
        )

    @property
    def index(self):
        return self.parent.get_channel_index(self.name)

    def get_is_element(self):
        return False

    def get_is_channel(self):
        return True


class AbsPortElement(
    # <port>
    AbsPortBaseDef,
    # <port-channel>
    AbsPortChannelExtraDef,
    # <port-source>
    AbsPortSourceExtraDef,
    # <port-target>
    AbsPortTargetExtraDef,
    # <port-value>
    AbsPortElementValueExtraDef,
):
    def __init__(self, parent, index):
        self._parent = parent
        # port
        self._init_port_base_def_(
            parent.obj, parent.type,
            str(index), parent.port_assign
        )
        # <port-channel>
        self._init_port_channel_extra_def_()
        # <port-input>
        self._init_port_source_extra_def_()
        # <port-output>
        self._init_port_target_extra_def_()

    @property
    def parent(self):
        return self._parent

    @property
    def obj(self):
        return self.parent.obj

    @property
    def type(self):
        return self.parent.type

    @property
    def port_path(self):
        return self.parent._get_element_port_path_(
            self.index
        )

    @property
    def index(self):
        return int(self.name)

    def get_is_element(self):
        return True

    def get_is_channel(self):
        return False


class AbsPort(
    # <port>
    AbsPortBaseDef,
    # <port-element>
    AbsPortElementExtraDef,
    # <port-channel>
    AbsPortChannelExtraDef,
    # <port-source>
    AbsPortSourceExtraDef,
    # <port-target>
    AbsPortTargetExtraDef,
    # <port-value>
    AbsPortValueExtraDef,
    # <obj-gui>
    unr_abs_base.AbsGuiExtraDef,
):
    def __init__(self, obj, type_path, port_path, port_assign):
        self._init_port_base_def_(
            obj, type_path,
            port_path, port_assign
        )
        self._init_port_element_extra_def_()
        self._init_port_channel_extra_def_()
        self._init_port_value_extra_def_()
        self._init_port_source_extra_def_()
        self._init_port_target_extra_def_()
        self._init_gui_extra_def_()

    @property
    def parent(self):
        return None

    def get_is_element(self):
        return False

    def get_is_channel(self):
        return False

    def to_properties(self):
        p = ctt_core.Properties(self)
        p.set(
            'type', self.type_path
        )
        p.set(
            'value', self.get()
        )
        return p

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.type.path,
            self.path
        )

    def __repr__(self):
        return self.__str__()
