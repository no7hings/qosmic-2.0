# coding:utf-8
import six

import collections

import lxcontent.core as ctt_core
# universe
from .. import core as unr_core

from . import base as unr_abs_base


# <obj-universe>
class AbsObjUniverseBaseDef(object):
    ROOT = None
    # <type>
    CATEGORY_STACK_CLS = None
    CATEGORY_CLS = None
    TYPE_STACK_CLS = None
    # <obj-type>
    OBJ_CATEGORY_STACK_CLS = None
    OBJ_CATEGORY_CLS = None
    OBJ_TYPE_STACK_CLS = None
    #
    OBJ_STACK_CLS = None
    OBJ_STACK_CLS_TEST = None
    #
    OBJ_CONNECTION_STACK_CLS = None
    OBJ_CONNECTION_CLS = None
    #
    OBJ_BIND_STACK_CLS = None
    OBJ_BIND_CLS = None
    #
    Category = unr_core.UnrCategory
    Type = unr_core.UnrType
    PortAssign = unr_core.UnrPortAssign

    #
    def _init_obj_universe_base_def_(self):
        # <type>
        self._category_stack = self.CATEGORY_STACK_CLS()
        self._type_stack = self.TYPE_STACK_CLS()
        # <obj-type>
        self._obj_category_stack = self.OBJ_CATEGORY_STACK_CLS()
        self._obj_type_stack = self.OBJ_TYPE_STACK_CLS()
        # <obj>
        self._obj_stack = self.OBJ_STACK_CLS()
        self._obj_stack_test = self.OBJ_STACK_CLS_TEST()
        # <obj-connection>
        self._obj_connection_stack = self.OBJ_CONNECTION_STACK_CLS()
        self._obj_bind_stack = self.OBJ_BIND_STACK_CLS()
        #
        self._custom_raw = {}
        #
        for obj_category_name in unr_core.UnrObjCategory.ALL:
            obj_category = self.generate_obj_category(obj_category_name)
            obj_category._build_port_queries_(unr_core.UnrObjCategory.PORT_QUERY_RAW)
        #
        for obj_category_name, obj_type_name in unr_core.UnrObjType.ALL:
            obj_type = self.generate_obj_type(obj_category_name, obj_type_name)
            obj_type._build_port_queries_(unr_core.UnrObjType.PORT_QUERY_RAW)
        #
        root_type = self.get_obj_type(unr_core.UnrObjType.ROOT)
        root_type.create_obj(root_type.obj_pathsep)

    def set_gui_attribute(self, key, value):
        self._custom_raw[key] = value

    def get_gui_attribute(self, key, default=None):
        return self._custom_raw.get(key, default)

    # <category>
    def __create_category(self, category_name):
        return self.CATEGORY_CLS(self, category_name)

    def generate_category(self, category_name):
        stack = self._category_stack
        if stack.get_object_exists(category_name) is True:
            return stack.get_object(category_name)
        obj_category = self.__create_category(category_name)
        stack.set_object_add(obj_category)
        return obj_category

    def get_categories(self):
        return self._category_stack.get_objects()

    def get_category(self, category_name):
        return self._category_stack.get_object(category_name)

    # <type>
    def generate_type(self, category_name, type_name):
        category = self.generate_category(category_name)
        return category.generate_type(type_name)

    def _get_type(self, type_path):
        stack = self._type_stack
        if stack.get_object_exists(type_path) is True:
            return stack.get_object(type_path)
        #
        category_name, type_name = self.CATEGORY_CLS._get_type_path_args_(type_path)
        category = self.generate_category(category_name)
        type_ = category._new_type_(type_name)
        stack.set_object_add(type_)
        return type_

    def get_types(self):
        return self._type_stack.get_objects()

    def get_type(self, type_string):
        pathsep = self.CATEGORY_CLS.PATHSEP
        if pathsep in type_string:
            regex = '{}'.format(type_string)
        else:
            regex = '*{}{}'.format(pathsep, type_string)
        #
        _ = self._type_stack.get_objects(
            regex=regex
        )
        if _:
            return _[-1]

    # <obj-category>
    def __create_obj_category(self, obj_category_name):
        return self.OBJ_CATEGORY_CLS(self, obj_category_name)

    def generate_obj_category(self, obj_category_name):
        stack = self._obj_category_stack
        if stack.get_object_exists(obj_category_name) is True:
            return stack.get_object(obj_category_name)
        obj_category = self.__create_obj_category(obj_category_name)
        stack.set_object_add(obj_category)
        return obj_category

    def get_obj_categories(self):
        return self._obj_category_stack.get_objects()

    def get_obj_category(self, obj_category_name):
        return self._obj_category_stack.get_object(obj_category_name)

    # <obj-type>
    def generate_obj_type(self, obj_category_name, obj_type_name):
        category = self.generate_obj_category(obj_category_name)
        return category.generate_type(obj_type_name)

    def get_obj_types(self):
        return self._obj_type_stack.get_objects()

    def get_obj_type(self, obj_type_string):
        pathsep = self.OBJ_CATEGORY_CLS.PATHSEP
        if pathsep in obj_type_string:
            regex = '{}'.format(obj_type_string)
        else:
            regex = '*{}{}'.format(pathsep, obj_type_string)
        #
        _ = self._obj_type_stack.get_objects(
            regex=regex
        )
        if _:
            return _[-1]

    # <obj>
    def _add_obj_(self, obj):
        self._obj_stack.set_object_add(obj)
        self._obj_stack_test.set_object_add(obj)

    def _override_obj_(self, old_obj, new_obj):
        """
        override <obj> by new <obj>
        :param old_obj: instance(<obj>)
        :param new_obj: instance(<obj>)
        :return:
        """
        self._obj_stack.set_object_override(old_obj, new_obj)
        self._obj_stack_test.set_object_override(old_obj, new_obj)

    # noinspection PyMethodMayBeStatic
    def _copy_obj_to_(self, source_obj, target_path):
        """
        copy a <obj> to a new <obj-path>
        :param source_obj: str(<obj-path>)
        :param target_path: str(<obj-path>)
        :return: None
        """
        obj_type = source_obj.type
        new_obj = obj_type.create_obj(target_path)
        port_dict = {}
        for port in source_obj.get_ports():
            key = port.port_path
            value = port.get()
            port_dict[key] = value
        [new_obj._build_port_(k, v) for k, v in port_dict.items()]

    def get_root(self):
        return self.get_obj(self.ROOT)

    def get_objs(self, regex=None):
        """
        :param regex: str("fnmatch regex-pattern")
        :return: list[instance(<obj>), ...]
        """
        if regex is not None:
            obj_pathsep = unr_core.UnrObj.PATHSEP
            obj_category_name = '*'
            obj_type_name = '*'
            if regex.startswith(obj_pathsep):
                obj_path = regex
            else:
                obj_path = '*{}{}'.format(obj_pathsep, regex)
            #
            regex = self.OBJ_CATEGORY_CLS._get_obj_token_(
                obj_category_name, obj_type_name, obj_path
            )
            return self._obj_stack.get_objects(regex=regex)
        return self._obj_stack.get_objects()

    def get_obj(self, obj_string):
        """
        :param obj_string: str(<obj-path>) or str(<obj-name>)
        :return: instance(<obj>) or None
        """
        obj_pathsep = unr_core.UnrObj.PATHSEP
        if obj_string.startswith(obj_pathsep):
            obj_path = obj_string
            return self._obj_stack_test.get_object(obj_path)
        # must join pathsep
        regex = '*{}{}'.format(obj_pathsep, obj_string)
        _ = self._obj_stack_test.get_objects(regex=regex)
        if _:
            return _[-1]

    def get_obj_exists(self, obj_string):
        """
        :param obj_string: str(<obj-path>) or str(<obj-name>)
        :return: bool
        """
        obj_pathsep = unr_core.UnrObj.PATHSEP
        if obj_string.startswith(obj_pathsep):
            obj_path = obj_string
            return self._obj_stack_test.get_object_exists(obj_path)
        #
        regex = '*{}{}'.format(obj_pathsep, obj_string)
        return self._obj_stack_test.get_objects_exists(regex=regex)

    # <obj-connection>
    def set_connection_create(self, source_obj_args, source_port_args, target_obj_args, target_port_args):
        obj_connection = self._set_connection_create_(
            source_obj_args, source_port_args, target_obj_args, target_port_args
        )
        self._obj_connection_stack._set_object_register_(obj_connection)
        return obj_connection

    #
    def _set_connection_create_(self, source_obj_args, source_port_args, target_obj_args, target_port_args):
        def get_obj_path_fnc_(obj_args_):
            if isinstance(obj_args_, six.string_types):
                return obj_args_
            elif isinstance(obj_args_, (tuple, list)):
                return self.OBJ_CONNECTION_CLS.OBJ_PATHSEP.join(obj_args_)

        #
        def get_port_path_fnc_(port_args_):
            if isinstance(port_args_, six.string_types):
                return port_args_
            elif isinstance(port_args_, (tuple, list)):
                return self.OBJ_CONNECTION_CLS.PORT_PATHSEP.join(port_args_)

        #
        obj_connection = self.OBJ_CONNECTION_CLS(
            self,
            get_obj_path_fnc_(source_obj_args), get_port_path_fnc_(source_port_args),
            get_obj_path_fnc_(target_obj_args), get_port_path_fnc_(target_port_args)
        )
        return obj_connection

    def get_connections(self, regex=None):
        return self._obj_connection_stack.get_objects(regex)

    def get_connections_exists(self, regex=None):
        return self._obj_connection_stack.get_objects_exists(regex)

    def set_bind_create(self):
        pass

    def _set_bind_create_(self):
        pass

    def get_as_dict(self):
        content = ctt_core.Content()
        for i_obj in self.get_objs():
            i_key = i_obj.path
            #
            content.set(
                i_key,
                collections.OrderedDict()
            )
            content.set(
                '{}.properties.type'.format(i_key),
                i_obj.type.path
            )
            if hasattr(i_obj, '_temp_attributes'):
                content.set(
                    '{}.properties.attributes'.format(i_key), i_obj._temp_attributes
                )
            if hasattr(i_obj, '_temp_customize_attributes'):
                content.set(
                    '{}.properties.customize-attributes'.format(i_key), i_obj._temp_customize_attributes
                )
        #
        return content

    def get_basic_source_objs(self, objs=None):
        if isinstance(objs, (tuple, list)):
            return [i for i in objs if not i.get_target_connections()]
        else:
            return [i for i in self.get_objs() if not i.get_target_connections()]

    def to_properties(self):
        p = ctt_core.Properties(self)
        for i_obj in self.get_objs():
            p.set(
                i_obj.path, i_obj.to_properties().get_value()
            )
        return p

    def set_save(self, file_path):
        dict_ = collections.OrderedDict()
        for i_obj in self._obj_stack:
            pass


class AbsObjUniverse(
    unr_abs_base.AbsObjBaseDef,
    AbsObjUniverseBaseDef
):
    def __init__(self):
        self._init_obj_base_def_('default')
        self._init_obj_universe_base_def_()


class AbsObjScene(object):
    FILE_CLS = None
    UNIVERSE_CLS = None

    def __init__(self, *args, **kwargs):
        self._universe = self.UNIVERSE_CLS()
        self._path_lstrip = None

    def get_universe(self):
        return self._universe

    universe = property(get_universe)

    @property
    def path_lstrip(self):
        return self._path_lstrip

    def restore_all(self):
        self._universe = self.UNIVERSE_CLS()
        self._path_lstrip = None
