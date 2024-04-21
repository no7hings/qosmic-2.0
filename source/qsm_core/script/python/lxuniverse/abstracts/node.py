# coding:utf-8
import six

import platform

import fnmatch

import os

import shutil

import subprocess

import lxbasic.content as bsc_content

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import lxbasic.core as bsc_core
# universe
from .. import core as unr_core

from . import base as unr_abs_base


# obj/type/def
class AbsObjTypeExtraDef(object):
    """
    abstract for <obj-type> definition
    """

    def _init_obj_type_extra_def_(self, obj_type):
        """
        :param obj_type: instance(<obj-type>)
        :return: None
        """
        self._obj_type = obj_type

    @property
    def universe(self):
        """
        :return: instance(<obj-universe>)
        """
        return self.type.universe

    def get_category(self):
        """
        :return: instance(<obj-category>)
        """
        return self.get_type().category

    category = property(get_category)

    def get_category_name(self):
        """
        :return: str
        """
        return self.get_category().name

    category_name = property(get_category_name)

    def get_type(self):
        return self._obj_type

    type = property(get_type)

    def get_type_path(self):
        return self.get_type().path

    type_path = property(get_type_path)

    def get_type_name(self):
        return self.get_type().name

    type_name = property(get_type_name)


# obj/dag/def
class AbsObjDagExtraDef(object):
    """
    abstract for <obj-dag>
        parent(s) gain
        child(s) gain
    """
    # str(<obj-pathsep>), etc: "/"
    PATHSEP = None

    def _init_obj_dag_extra_def_(self, path):
        """
        :param path: str(<obj-path>), etc: "/obj"
        :return: None
        """
        self._path = path

    @classmethod
    def _get_path_args_(cls, path):
        """
        :param path: str(<obj-path>)
        :return: list[str(<obj-name>), ...]
        """
        if cls.PATHSEP is None:
            raise TypeError()
        # is <root-obj>, etc: "/"
        if path == cls.PATHSEP:
            return [cls.PATHSEP, ]
        # is <obj>, etc: "/obj"
        return path.split(cls.PATHSEP)

    @classmethod
    def _get_obj_name_(cls, path):
        """
        :param path:
        :return:
        """
        # is <root-obj>, etc: "/"
        if path == cls.PATHSEP:
            return cls.PATHSEP
        # is <obj>, etc: "/obj"
        return cls._get_path_args_(path)[-1]

    @classmethod
    def _get_parent_path_(cls, path):
        """
        :param path:
        :return:
        """
        pathsep = cls.PATHSEP
        path_args = cls._get_path_args_(path)
        # windows file-path-root etc: "D:/directory"
        if ':' in path_args[0]:
            if len(path_args) == 1:
                return None
            else:
                return pathsep.join(path_args[:-1])
        else:
            if len(path_args) == 1:
                return None
            elif len(path_args) == 2:
                return pathsep
            else:
                return pathsep.join(path_args[:-1])

    @classmethod
    def _get_dag_paths_(cls, path):
        def _rcs_fnc(lis_, path_):
            if path_ is not None:
                lis_.append(path_)
                _parent_path = cls._get_parent_path_(path_)
                if _parent_path:
                    _rcs_fnc(lis_, _parent_path)

        lis = []
        _rcs_fnc(lis, path)
        return lis

    @property
    def pathsep(self):
        """
        :return: str(<obj-pathsep>)
        """
        return self.PATHSEP

    def get_path(self):
        return self._path

    @property
    def path(self):
        """
        :return: str(<obj-path>)
        """
        return self._path

    #
    def get_root(self):
        return self.create_dag_fnc(self.PATHSEP)

    #
    def get_is_root(self):
        return self.path == self.PATHSEP

    # branch
    def get_dag_component_paths(self):
        """
        :return: list[str(<obj-path>)]
        """

        def _rcs_fnc(lis_, path_):
            if path_ is not None:
                lis_.append(path_)
                _parent_path = self._get_parent_path_(path_)
                if _parent_path:
                    _rcs_fnc(lis_, _parent_path)

        lis = []
        _rcs_fnc(lis, self.path)
        return lis

    def get_dag_components(self):
        return [self.create_dag_fnc(i) for i in self.get_dag_component_paths()]

    def get_dag_element_objs(self):
        """
        :return: list[instance(<obj>), ...]
        """
        return [self.create_dag_fnc(i) for i in self.get_dag_component_paths()]

    #
    def create_ancestors(self):
        """
        :return: None
        """
        [self.create_dag_fnc(i) for i in self.get_ancestor_paths()]

    def set_dag_components_create(self):
        pass

    def create_dag_fnc(self, path):
        raise NotImplementedError()

    def get_parent_path(self):
        """
        :return: str(<obj-path>)
        """
        return self._get_parent_path_(self.path)

    def get_parent_exists(self):
        """
        :return: bool
        """
        return self.get_parent_path() is not None

    def get_parent(self):
        """
        :return: instance(<obj>)
        """
        parent_path = self.get_parent_path()
        if parent_path is not None:
            return self.create_dag_fnc(self.get_parent_path())

    def get_ancestor_paths(self):
        """
        :return: list[str(<obj-path>), ...]
        """
        return self.get_dag_component_paths()[1:]

    def get_ancestors(self):
        """
        :return: list[instance(<obj>), ...]
        """
        return [self.create_dag_fnc(i) for i in self.get_ancestor_paths()]

    # child
    def _get_child_paths_(self, *args, **kwargs):
        raise NotImplementedError()

    def _get_child_(self, path):
        raise NotImplementedError()

    def get_child_paths(self):
        """
        :return: list[str(<obj-path>), ...]
        """
        return self._get_child_paths_(self.path)

    # list of all child <obj-path>
    def get_descendant_paths(self, *args, **kwargs):
        """
        :return: list[str(<obj-path>), ...]
        """

        def _rcs_fnc(lis_, path_):
            if path_ is not None:
                _child_paths = self._get_child_paths_(path_)
                if _child_paths:
                    for _child_path in _child_paths:
                        lis_.append(_child_path)
                        _rcs_fnc(lis_, _child_path)

        lis = []
        _rcs_fnc(lis, self.path)
        return lis

    #
    def get_children_exists(self):
        """
        :return: bool
        """
        return self.get_child_paths() != []

    # list of child <obj>
    def get_children(self):
        """
        :return: list[instance(<obj>), ...]
        """
        return [self._get_child_(i) for i in self.get_child_paths()]

    # list of all child <obj>
    def get_descendants(self, *args, **kwargs):
        """
        :return: list[instance(<obj>), ...]
        """
        return [self._get_child_(i) for i in self.get_descendant_paths()]

    def get_path_is_matched(self, p):
        return fnmatch.filter(
            [self.path], p
        ) != []

    def get_as_new_name(self, new_name):
        return self.__class__(
            '{}/{}'.format(
                self.get_parent_path(), new_name
            )
        )

    def __eq__(self, other):
        if other is not None:
            return self._path == other._path

    def __ne__(self, other):
        if other is not None:
            return self._path != self._path


# obf/port/def
class AbsObjPortExtraDef(object):
    OBJ_TOKEN = None
    #
    DCC_PORT_CLS = None
    PORT_STACK_CLS = None

    def _init_obj_port_extra_def_(self):
        self._port_stack = self.PORT_STACK_CLS()

    @property
    def universe(self):
        raise NotImplementedError()

    def _build_ports_(self, ports_raw, raw_convert_method=None):
        for k, v in ports_raw.items():
            self._build_port_(k, v, raw_convert_method)

    def _build_port_(self, key, value, raw_convert_method=None):
        port_path = key.replace('/', unr_core.UnrPort.PATHSEP)
        if isinstance(value, dict):
            type_path = value.get(
                'type',
                unr_core.UnrType.CONSTANT_RAW_
            ).replace('/', unr_core.UnrType.PATHSEP)
            port_assign = value.get(
                'port_assign',
                unr_core.UnrPortAssign.VARIANTS
            )
            if raw_convert_method is not None:
                raw = raw_convert_method(value.get('raw'))
            else:
                raw = value.get('raw')
        else:
            port_assign = unr_core.UnrPortAssign.VARIANTS
            type_path = unr_core.UnrType.CONSTANT_RAW_
            raw = value
        #
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        if self._port_stack.get_object_exists(port_token) is True:
            port = self._port_stack.get_object(port_token)
        else:
            port = self._create_port_(
                type_path, port_path, port_assign
            )
            self._port_stack.set_object_add(port)
        #
        port.set(raw)

    def generate_port(self, type_args, port_path, port_assign):
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        if self._port_stack.get_object_exists(port_token) is True:
            port = self._port_stack.get_object(port_token)
        else:
            port = self._create_port_(
                type_args, port_path, port_assign
            )
            self._port_stack.set_object_add(port)
        return port

    def generate_variant_port(self, type_args, port_path):
        return self.generate_port(type_args, port_path, unr_core.UnrPortAssign.VARIANTS)

    def create_input_port(self, type_args, port_path):
        return self.generate_port(type_args, port_path, unr_core.UnrPortAssign.INPUTS)

    def create_output_port(self, type_args, port_path):
        return self.generate_port(type_args, port_path, unr_core.UnrPortAssign.OUTPUTS)

    def _create_port_(self, type_args, port_path, port_assign):
        port = self.DCC_PORT_CLS(
            self, type_args, port_path, port_assign
        )
        return port

    def _add_port_(self, port):
        self._port_stack.set_object_add(port)

    # port
    def get_port(self, port_string):
        if self.OBJ_TOKEN.PORT_ASSIGN_PATHSEP in port_string:
            port_token = port_string
            return self._port_stack.get_object(port_token)
        else:
            port_assigns = unr_core.UnrPortAssign.ALL
            port_path = port_string
            for port_assign in port_assigns:
                port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
                _ = self._port_stack.get_object(port_token)
                if _ is not None:
                    return _

    def get_port_is_exists(self, port_token):
        return self._port_stack.get_object_exists(port_token)

    def get_ports(self, regex=None):
        return self._port_stack.get_objects(regex)

    def get_ports_exists(self, regex=None):
        return self._port_stack.get_objects_exists(regex)

    # input
    def get_input_port_exists(self, port_path):
        port_assign = unr_core.UnrPortAssign.INPUTS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port_is_exists(port_token)

    def get_input_port(self, port_path):
        port_assign = unr_core.UnrPortAssign.INPUTS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port(port_token)

    def get_input(self, port_path):
        port = self.get_input_port(port_path)
        if port is not None:
            return port.get()

    def get_input_ports(self):
        port_assign = unr_core.UnrPortAssign.INPUTS
        port_path = '*'
        regex = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self._port_stack.get_objects(regex=regex)

    # output
    def get_output_port_exists(self, port_path):
        port_assign = unr_core.UnrPortAssign.OUTPUTS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port_is_exists(port_token)

    def get_output_port(self, port_path):
        port_assign = unr_core.UnrPortAssign.OUTPUTS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port(port_token)

    def get_output(self, port_path):
        port = self.get_output_port(port_path)
        if port is not None:
            return port.get()

    def get_output_ports(self):
        port_assign = unr_core.UnrPortAssign.OUTPUTS
        port_path = '*'
        regex = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self._port_stack.get_objects(regex=regex)

    # bind
    def get_bind_port_exists(self, port_path):
        port_assign = unr_core.UnrPortAssign.BINDS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port_is_exists(port_token)

    def get_bind_port(self, port_path):
        port_assign = unr_core.UnrPortAssign.BINDS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port(port_token)

    def get_bind(self, port_path):
        port = self.get_bind_port(port_path)
        if port is not None:
            return port.get()

    def get_bind_ports(self):
        port_assign = unr_core.UnrPortAssign.BINDS
        port_path = '*'
        regex = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self._port_stack.get_objects(regex=regex)

    # variant
    def get_variant_port_exists(self, port_path):
        port_assign = unr_core.UnrPortAssign.VARIANTS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port_is_exists(port_token)

    def get_variant_port(self, port_path):
        port_assign = unr_core.UnrPortAssign.VARIANTS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port(port_token)

    # noinspection PyUnusedLocal
    def get_variant_ports(self, regex=None):
        port_assign = unr_core.UnrPortAssign.VARIANTS
        port_path = '*'
        regex = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self._port_stack.get_objects(regex=regex)

    def get_variant(self, port_path):
        port_path = port_path.replace('/', self.DCC_PORT_CLS.PATHSEP)
        port = self.get_variant_port(port_path)
        if port is not None:
            return port.get()

    def set_variant(self, port_path, raw):
        port_path = port_path.replace('/', self.DCC_PORT_CLS.PATHSEP)
        port = self.get_variant_port(port_path)
        if port:
            return port.set(raw)

    def get(self, key):
        return self.get_variant(key)

    def set(self, key, value):
        self.set_variant(key, value)

    def _format_dict_(self):
        raise NotImplementedError()


# <obj-source/target>
class AbsObjSourceExtraDef(object):
    """
    abstract for <obj-source> definition
        <input-port>
    """
    OBJ_TOKEN = None
    # str(<connection-pattern>)
    OBJ_SOURCE_CONNECTION_GAIN_REGEX = u'* >> {obj.path}.*'

    def _init_obj_source_extra_def_(self):
        """
        :return: None
        """
        pass

    @property
    def universe(self):
        raise NotImplementedError()

    @property
    def path(self):
        raise NotImplementedError()

    #
    def _get_source_connections_(self, obj_path):
        source_obj_path = '*'
        source_port_path = '*'
        target_obj_path = obj_path
        target_port_path = '*'
        regex = self.OBJ_TOKEN._get_obj_connection_token_(
            source_obj_path, source_port_path, target_obj_path, target_port_path
        )
        return self.universe.get_connections(
            regex=regex
        )

    @classmethod
    def _get_source_(cls, obj_connection):
        return obj_connection.source

    @classmethod
    def _get_source_obj_(cls, obj_connection):
        return obj_connection.source_obj

    def get_source_connections(self):
        """
        :return: list[instance(<obj-connection>), ...]
        """
        return self._get_source_connections_(self.path)

    def get_sources(self):
        """
        :return: list[instance(<port>), ...]
        """
        return [self._get_source_(i) for i in self.get_source_connections()]

    def get_source_objs(self):
        return [self._get_source_obj_(i) for i in self.get_source_connections()]

    def _get_all_source_connections_(self, obj_path):
        def _rcs_fnc(obj_path_):
            _obj_connections = self._get_source_connections_(obj_path_)
            for _i in _obj_connections:
                lis.append(_i)
                _rcs_fnc(self._get_source_obj_(_i).path)

        lis = []
        _rcs_fnc(obj_path)
        return lis

    def get_all_source_connections(self):
        return self._get_all_source_connections_(self.path)

    def get_all_sources(self):
        return [self._get_source_(i) for i in self.get_all_source_connections()]

    def get_all_source_objs(self):
        return [self._get_source_obj_(i) for i in self.get_all_source_connections()]

    def _format_dict_(self):
        raise NotImplementedError()


class AbsObjTargetExtraDef(object):
    """
    abstract for <obj-target> definition
        <output-port>
    """
    OBJ_TOKEN = None
    # str(<connection-pattern>)
    OBJ_TARGET_CONNECTION_GAIN_REGEX = u'{obj.path}.* >> *'

    def _init_obj_target_extra_def_(self):
        pass

    @property
    def universe(self):
        raise NotImplementedError()

    @property
    def path(self):
        raise NotImplementedError()

    def _get_target_connections_(self, obj_path):
        """
        :return: list[instance(<obj-connection>), ...]
        """
        source_obj_path = obj_path
        source_port_path = '*'
        target_obj_path = '*'
        target_port_path = '*'
        regex = self.OBJ_TOKEN._get_obj_connection_token_(
            source_obj_path, source_port_path, target_obj_path, target_port_path
        )
        return self.universe.get_connections(
            regex=regex
        )

    @classmethod
    def _get_target_(cls, obj_connection):
        return obj_connection.target

    @classmethod
    def _get_target_obj_(cls, obj_connection):
        return obj_connection.target_obj

    def get_target_connections(self):
        """
        :return: list[instance(<obj-connection>), ...]
        """
        return self._get_target_connections_(self.path)

    def get_targets(self):
        return [self._get_target_(i) for i in self.get_target_connections()]

    def get_target_objs(self):
        return [self._get_target_obj_(i) for i in self.get_target_connections()]

    def _get_all_target_connections_(self, obj_path):
        def _rcs_fnc(obj_path_):
            _obj_connections = self._get_target_connections_(obj_path_)
            for _i in _obj_connections:
                lis.append(_i)
                _rcs_fnc(self._get_target_obj_(_i).path)

        lis = []
        _rcs_fnc(obj_path)
        return lis

    def get_all_target_connections(self):
        return self._get_all_target_connections_(self.path)

    def get_all_targets(self):
        return [self._get_target_(i) for i in self.get_all_target_connections()]

    def get_all_target_objs(self):
        return [self._get_target_obj_(i) for i in self.get_all_target_connections()]

    def _format_dict_(self):
        raise NotImplementedError()


class AbsObjPropertiesExtraDef(object):
    PROPERTIES_CLS = None

    def _init_obj_properties_extra_def_(self):
        self._obj_properties = bsc_content.Properties(
            self
        )

    @property
    def properties(self):
        return self._obj_properties

    @properties.setter
    def properties(self, raw):
        if isinstance(raw, dict):
            self._obj_properties = self.PROPERTIES_CLS(self, raw)
        elif isinstance(raw, self.PROPERTIES_CLS):
            self._obj_properties = raw
        else:
            raise TypeError()


class AbsObjAttributesExtraDef(object):
    ATTRIBUTES_CLS = None

    def _init_obj_attributes_extra_def_(self):
        self._obj_attributes = {}

    @property
    def attributes(self):
        return self._obj_attributes

    @attributes.setter
    def attributes(self, raw):
        if isinstance(raw, dict):
            self._obj_attributes = self.ATTRIBUTES_CLS(self, raw)
        elif isinstance(raw, self.ATTRIBUTES_CLS):
            self._obj_attributes = raw
        else:
            raise TypeError()


# <obj>
class AbsObj(
    # base
    unr_abs_base.AbsObjBaseDef,
    # type
    AbsObjTypeExtraDef,
    # path
    AbsObjDagExtraDef,
    # port
    AbsObjPortExtraDef,
    # relationship
    AbsObjSourceExtraDef,
    AbsObjTargetExtraDef,
    #
    AbsObjPropertiesExtraDef,
    AbsObjAttributesExtraDef,
    # gui
    unr_abs_base.AbsGuiExtraDef,
):
    """
    abstract for <obj>
    """

    def __init__(self, obj_type, path):
        self._init_obj_type_extra_def_(obj_type)
        self._init_obj_dag_extra_def_(path)
        self._init_obj_base_def_(
            self._get_obj_name_(path)
        )
        self._init_obj_port_extra_def_()
        self._init_gui_extra_def_()
        self._init_obj_properties_extra_def_()
        self._init_obj_attributes_extra_def_()

    def create_dag_fnc(self, path):
        """
        :param path: str(<obj-path>)
        :return:
        """
        obj = self.universe.get_obj(path)
        if obj is not None:
            return obj
        else:
            obj = self.universe.get_obj_type(unr_core.UnrObjType.NULL)._create_obj_(path)
            self.universe._add_obj_(obj)
            return obj

    def _get_child_paths_(self, path):
        lis = []
        obj_pathsep = self.PATHSEP
        regex = '{}{}*'.format(self.path, obj_pathsep)
        #
        pattern = '{}{}*{}*'.format(path, obj_pathsep, obj_pathsep)
        _ = self.universe._obj_stack_test.get_objects(regex=regex)
        for i in _:
            match = fnmatch.filter([i.path], pattern)
            if match:
                continue
            lis.append(i.path)
        return lis

    def _get_child_(self, path):
        return self.universe.get_obj(path)

    def get_descendant_paths(self):
        return [i.path for i in self.get_descendants()]

    def get_descendants(self):
        obj_pathsep = self.PATHSEP
        regex = '{}{}*'.format(self.path, obj_pathsep)
        return self.universe._obj_stack_test.get_objects(regex=regex)

    def _format_dict_(self):
        return {
            'self': self,
            'category': self.category,
            'type': self.type,
            'obj': self
        }

    def _get_stack_key_(self):
        obj_category_name = self.category.name
        obj_type_name = self.type.name
        obj_string = self.path
        return self.category._get_obj_token_(
            obj_category_name, obj_type_name, obj_string
        )

    def to_properties(self):
        p = bsc_content.Properties(self)
        p.set(
            'type', self.type_path
        )
        for i_port in self.get_input_ports():
            if i_port.get_is_element() is False and i_port.get_is_channel() is False:
                p.set(
                    i_port.port_token, i_port.to_properties().get_value()
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


class AbsObjStgExtraDef(object):
    PATHSEP = '/'

    @staticmethod
    def get_is_linux():
        return platform.system() == 'Linux'

    @staticmethod
    def get_is_windows():
        return platform.system() == 'Windows'

    def _init_obj_storage_extra_def_(self):
        self._root = bsc_storage.StgPathMtd.get_root(
            self.path
        )

    @classmethod
    def create_symlink_fnc(cls, path_src, path_tgt):
        tgt_dir_path = os.path.dirname(path_tgt)
        src_rel_path = os.path.relpath(path_src, tgt_dir_path)
        if os.path.exists(path_tgt) is False:
            os.symlink(src_rel_path, path_tgt)

    @property
    def root_name(self):
        return self._root

    @property
    def normcase_root_name(self):
        return os.path.normcase(self._root)

    @property
    def path(self):
        """
        :return: str(<plf-path>)
        """
        raise NotImplementedError()

    @property
    def normcase_path(self):
        """
        get path as normal case
        :return: str(path)
        """
        return os.path.normcase(self.path)

    @property
    def name(self):
        """
        :return: str(<plf-name>)
        """
        raise NotImplementedError()

    @property
    def normcase_name(self):
        return os.path.basename(self.name)

    def get_is_directory(self):
        raise NotImplementedError()

    def get_is_file(self):
        raise NotImplementedError

    def get_is_driver(self):
        # windows
        return ':' in self.name

    def get_is_exists(self):
        raise NotImplementedError()

    def get_is_exists_file(self):
        return os.path.isfile(self.path)

    def set_create(self):
        raise NotImplementedError()

    def set_open(self):
        if os.path.exists(self.path):
            if self.get_is_windows():
                cmd = 'explorer /select,"{}"'.format(self.path.replace('/', '\\'))
                subprocess.Popen(cmd, shell=True)
            elif self.get_is_linux():
                cmd = 'nautilus "{}" --select'.format(self.path)
                subprocess.Popen(cmd, shell=True)

    def get_is_same_to(self, file_path):
        return os.path.normpath(self.path) == os.path.normpath(file_path)

    def get_permission(self):
        return bsc_storage.StgPathMtd.get_permission(self.path)

    def get_is_writable(self):
        return bsc_storage.StgPathMtd.get_is_writable(self.path)

    def get_is_readable(self):
        return bsc_storage.StgPathMtd.get_is_readable(self.path)

    def link_to(self, *args, **kwargs):
        pass


class AbsStgDirectory(
    unr_abs_base.AbsObjBaseDef,
    AbsObjDagExtraDef,
    AbsObjStgExtraDef
):
    # <obj-pathsep>
    PATHSEP = '/'

    STG_FILE_CLS = None

    def __init__(self, path):
        self._init_obj_dag_extra_def_(path)
        self._init_obj_base_def_(
            self._get_obj_name_(path)
        )
        self._init_obj_storage_extra_def_()

    # dag
    def create_dag_fnc(self, path):
        return self.__class__(path)

    def _get_child_paths_(self, path, includes=None):
        return bsc_storage.StgDirectoryMtd.get_directory_paths__(
            path
        )

    def _get_child_(self, path):
        return self.__class__(path)

    @property
    def type(self):
        return 'directory'

    def get_type_name(self):
        return 'directory'

    type_name = property(get_type_name)

    @property
    def type_path(self):
        return 'storage/{}'.format(self.type_name)

    def get_is_root(self):
        return self._path == self._root

    def get_root(self):
        return self.create_dag_fnc(self._root)

    # os
    def get_is_directory(self):
        return True

    def get_is_file(self):
        return False

    def get_is_exists(self):
        if self.path is not None:
            return os.path.isdir(self.path)
        return False

    def set_create(self):
        raise NotImplementedError()

    def get_child_file_paths(self):
        return bsc_storage.StgDirectoryMtd.get_file_paths__(
            self.path
        )

    def set_copy_to(self, directory_path_tgt):
        if os.path.exists(directory_path_tgt) is False:
            shutil.copytree(
                self.path, directory_path_tgt
            )

    def get_file_paths(self, ext_includes=None):
        return bsc_storage.StgDirectoryMtd.get_file_paths__(
            self.path, ext_includes
        )

    def get_files(self, ext_includes=None):
        return [self.STG_FILE_CLS(i) for i in self.get_file_paths(ext_includes)]

    def get_all_file_paths(self, ext_includes=None):
        return bsc_storage.StgDirectoryMtd.get_all_file_paths__(
            self.path, ext_includes
        )

    def copy_to_directory(self, directory_path_tgt):
        def copy_fnc_(src_file_path_, tgt_file_path_):
            shutil.copy2(src_file_path_, tgt_file_path_)
            bsc_log.Log.trace_method_result(
                'file copy',
                u'file="{}" >> "{}"'.format(src_file_path_, tgt_file_path_)
            )

        #
        src_directory_path = self.path
        file_paths = self.get_all_file_paths()
        #
        threads = []
        for i_src_file_path in file_paths:
            i_local_file_path = i_src_file_path[len(src_directory_path):]
            #
            i_tgt_file_path = directory_path_tgt+i_local_file_path
            if os.path.exists(i_tgt_file_path) is False:
                i_tgt_dir_path = os.path.dirname(i_tgt_file_path)
                if os.path.exists(i_tgt_dir_path) is False:
                    os.makedirs(i_tgt_dir_path)
                    bsc_log.Log.trace_method_result(
                        'directory create',
                        u'directory="{}"'.format(i_tgt_dir_path)
                    )
                #
                i_thread = bsc_core.TrdFnc(
                    copy_fnc_, i_src_file_path, i_tgt_file_path
                )
                threads.append(i_thread)
        #
        [i.start() for i in threads]
        [i.join() for i in threads]

    def set_open(self):
        if self.get_path():
            bsc_storage.StgSystem.open_directory(self.get_path())

    def __str__(self):
        return u'{}(path="{}")'.format(
            self.__class__.__name__,
            self.path
        ).encode('utf-8')

    def __repr__(self):
        return self.__str__()


class AbsStgFile(
    unr_abs_base.AbsObjBaseDef,
    AbsObjDagExtraDef,
    AbsObjStgExtraDef
):
    # dag
    PATHSEP = '/'
    # os
    STG_DIRECTORY_CLS = None
    #
    LOG = None

    def __init__(self, path):
        self._init_obj_dag_extra_def_(path)
        self._init_obj_base_def_(
            self._get_obj_name_(path)
        )
        self._init_obj_storage_extra_def_()

    @classmethod
    def _get_ext_split_(cls, text):
        return os.path.splitext(text)

    def get_ext_split(self):
        return self._get_ext_split_(self.path)

    # dag
    def create_dag_fnc(self, path):
        return self.STG_DIRECTORY_CLS(path)

    def _get_child_(self, path):
        raise RuntimeError(
            'file has no child'
        )

    # child
    def _get_child_paths_(self, path):
        return []

    @property
    def type(self):
        if self.ext:
            return self.ext[1:]
        return '*'

    @property
    def type_path(self):
        return 'storage/{}'.format(self.type_name)

    def get_type_name(self):
        if self.ext:
            return self.ext[1:]
        return '*'

    type_name = property(get_type_name)

    def get_is_root(self):
        return self._path == self._root

    #
    def get_root(self):
        if self._root is not None:
            return self.create_dag_fnc(self._root)

    # os
    def get_is_directory(self):
        return False

    def get_is_file(self):
        return True

    def get_is_exists(self):
        if self.path is not None:
            return os.path.isfile(self.path)
        return False

    def set_create(self):
        pass

    # file
    @property
    def base(self):
        return os.path.splitext(self.name)[0]

    def get_name_base(self):
        return os.path.splitext(self.name)[0]

    name_base = property(get_name_base)

    def get_path_base(self):
        return os.path.splitext(self.path)[0]

    @property
    def path_base(self):
        return os.path.splitext(self.path)[0]

    @property
    def ext(self):
        return os.path.splitext(self.path)[-1]

    def get_extension(self):
        return os.path.splitext(self.path)[-1]

    extension = property(get_extension)

    @property
    def directory(self):
        return self.get_parent()

    def open_directory_in_system(self):
        if self.get_is_exists_file() is True:
            if self.get_is_windows():
                cmd = 'explorer /select,"{}"'.format(self.path.replace('/', '\\'))
                subprocess.Popen(cmd, shell=True)
            elif self.get_is_linux():
                cmd = 'nautilus "{}" --select'.format(self.path)
                subprocess.Popen(cmd, shell=True)
        elif self.directory.get_is_exists() is True:
            if self.get_is_windows():
                cmd = 'explorer "{}"'.format(self.directory.path.replace('/', '\\'))
                subprocess.Popen(cmd, shell=True)
            elif self.get_is_linux():
                cmd = 'gio open "{}"'.format(self.directory.path)
                subprocess.Popen(cmd, shell=True)

    def set_copy_to(self, target_dir_path, ignore_structure=True):
        if self.get_is_exists() is True:
            if isinstance(target_dir_path, six.string_types):
                target_dir_path = [target_dir_path]
            #
            for i_directory_path_tgt in target_dir_path:
                target_file_path = self.get_target_file_path(i_directory_path_tgt, ignore_structure=ignore_structure)
                if os.path.exists(target_file_path) is False:
                    target_directory = os.path.dirname(target_file_path)
                    if os.path.exists(target_directory) is False:
                        os.makedirs(target_directory)
                        bsc_log.Log.trace_result(
                            'directory create: "{}"'.format(target_directory)
                        )
                    shutil.copy2(self.path, target_file_path)
                    bsc_log.Log.trace_result(
                        'file copy: "{}" >> "{}"'.format(self.path, target_file_path)
                    )
                else:
                    bsc_log.Log.trace_warning('file copy: target "{}" is exist.'.format(target_file_path))
        else:
            bsc_log.Log.trace_warning('file copy: source "{}" is Non-exist.'.format(self.path))

    def get_target_file_path(self, directory_path_tgt, fix_name_blank=False, ignore_structure=True, ext_override=None):
        directory_path_tgt = bsc_storage.StgPathOpt(directory_path_tgt).__str__()
        if ignore_structure is True:
            name = self.name
            if fix_name_blank is True:
                if ' ' in name:
                    name = name.replace(' ', '_')
            if ext_override is not None:
                base, ext = os.path.splitext(name)
                name = '{}{}'.format(base, ext_override)
            return u'{}/{}'.format(directory_path_tgt, name)
        else:
            return u'{}/{}'.format(directory_path_tgt, self.path)

    def get_target_file(self, directory_path_tgt):
        return self.__class__(
            self.get_target_file_path(directory_path_tgt)
        )

    def create_directory(self):
        self.directory.set_create()

    def do_delete(self):
        if self.get_is_exists() is True:
            if self.get_is_writable() is True:
                os.remove(self.path)
                bsc_log.Log.trace_method_result(
                    'file delete',
                    'file="{}"'.format(self.path)
                )
            else:
                bsc_log.Log.trace_method_error(
                    'file delete',
                    'file="{}" is not writable'.format(self.path)
                )

    def copy_to_file(self, file_path_tgt, replace=False):
        if self.get_is_exists() is True:
            file_tgt = self.__class__(file_path_tgt)
            if replace is True:
                if bsc_storage.StgPathMtd.get_is_exists(file_path_tgt) is True:
                    if bsc_storage.StgPathMtd.get_is_writable(file_path_tgt) is True:
                        os.remove(file_tgt.path)
                        shutil.copy2(self.path, file_tgt.path)
                        return True, bsc_log.Log.trace_method_result(
                            'file copy replace',
                            'relation="{}" >> "{}"'.format(self.path, file_path_tgt)
                        )
                    #
                    return False, bsc_log.Log.trace_method_error(
                        'file copy replace',
                        'file="{}" is not writable'.format(file_tgt.path)
                    )
            #
            if file_tgt.get_is_exists() is False:
                file_tgt.create_directory()
                # noinspection PyBroadException
                try:
                    if self.get_is_readable() is True:
                        shutil.copy2(self.path, file_path_tgt)
                        return True, bsc_log.Log.trace_method_result(
                            'file copy',
                            'relation="{}" >> "{}"'.format(self.path, file_path_tgt)
                        )
                    else:
                        bsc_storage.StgPathPermissionMtd.unlock(
                            self.path
                        )
                        shutil.copy2(self.path, file_path_tgt)
                        return True, bsc_log.Log.trace_method_result(
                            'file copy',
                            'relation="{}" >> "{}"'.format(self.path, file_path_tgt)
                        )
                except Exception:
                    bsc_core.ExceptionMtd.set_print()
                    return False, bsc_log.Log.trace_method_error(
                        'file copy',
                        'file="{}" is exception'.format(self.path)
                    )
        return False, None

    def copy_to_directory(self, directory_path_tgt, replace=False):
        file_path_tgt = '{}/{}'.format(
            directory_path_tgt, self.name
        )
        self.copy_to_file(
            file_path_tgt, replace=replace
        )

    def get_orig_file(self, ext):
        if self.ext == ext:
            base, ext = os.path.splitext(self.path)
            glob_pattern = '{}.*'.format(base)
            _ = bsc_storage.StgDirectoryMtd.find_file_paths(
                glob_pattern
            )
            lis = []
            if _:
                for i in _:
                    if i == self.path:
                        continue
                    lis.append(i)
            if lis:
                return lis[0]

    def get_ext_is(self, ext):
        return self.ext == ext

    def __str__(self):
        return '{}(path="{}")'.format(
            self.__class__.__name__,
            bsc_core.auto_encode(self.get_path())
        )

    def __repr__(self):
        return self.__str__()
