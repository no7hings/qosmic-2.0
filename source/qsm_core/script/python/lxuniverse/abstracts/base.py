# coding:utf-8
import six

import fnmatch

import lxcontent.core as ctt_core

import lxbasic.storage as bsc_storage
# universe
from .. import core as unr_core


# stack
class AbsObjStack(object):
    """
    abstract for <obj-stack>
        obj-register
        obj-query
        obj-gain
    """

    def __init__(self):
        self._key_dict = {}
        self._count = 0
        #
        self._key_list = []
        self._obj_list = []

    def get_key(self, obj):
        """
        :param obj: instance(<obj>)
        :return: str(<obj-key>)
        """
        raise NotImplementedError()

    def get_index(self, key):
        """
        :param key: str(<obj-key>)
        :return: int(<obj-index>)
        """
        return self._key_dict[key]

    def get_object(self, key):
        """
        :param key: str(<obj-key>)
        :return: instance(<obj>)
        """
        if key in self._key_dict:
            index = self._key_dict[key]
            return self._obj_list[index]

    def get_object_at(self, index):
        """
        :param index: int(<obj-index>)
        :return: instance(<obj>)
        """
        return self._obj_list[index]

    def get_keys(self, regex=None):
        """
        key is sorted by add order
        :param regex: str(<fnmatch-pattern>)
        :return: list[str(<obj-key>), ...]
        """
        if regex:
            _ = fnmatch.filter(self._key_dict.keys(), regex)
            _.sort(key=self._key_list.index)
            return _
        return self._key_list

    def get_objects(self, regex=None):
        """
        :param regex: str(<fnmatch-pattern>)
        :return: list[instance(<obj>), ...]
        """
        if regex:
            keys = self.get_keys(regex)
            if keys:
                return [self._obj_list[self._key_dict[i_key]] for i_key in keys]
            return []
        return self._obj_list

    def get_all_objects(self):
        return self._obj_list

    def get_object_exists(self, key):
        """
        :param key: str(<obj-key>)
        :return: bool
        """
        return key in self._key_dict

    def get_objects_exists(self, regex=None):
        """
        :param regex: str(<fnmatch-pattern>)
        :return: bool
        """
        if regex:
            keys = self.get_keys(regex)
            return keys != []
        return self._count > 0

    def set_object_add(self, obj):
        """
        add object
        :param obj: instance(<obj>)
        :return: bool
        """
        key = self.get_key(obj)
        if key not in self._key_dict:
            index = self._count
            #
            self._key_dict[key] = index
            #
            self._key_list.append(key)
            self._obj_list.append(obj)
            #
            self._count += 1
            return True
        return False

    def set_object_del(self, obj):
        """
        delete object
        :param obj: instance(<obj>)
        :return: bool
        """
        key = self.get_key(obj)
        if key in self._key_dict:
            self._key_dict.pop(key)
            #
            self._key_list.remove(key)
            self._obj_list.remove(obj)
            #
            self._count -= 1
            return True
        return False

    def set_object_override(self, old_obj, new_obj):
        """
        override object
        :param old_obj: instance(<obj>)
        :param new_obj: instance(<obj>)
        :return:
        """
        old_key = self.get_key(old_obj)
        if old_key in self._key_dict:
            old_index = self._key_dict[old_key]
            new_key = self.get_key(new_obj)
            self._key_dict.pop(old_key)
            self._key_dict[new_key] = old_index
            #
            self._key_list[old_index] = new_key
            self._obj_list[old_index] = new_obj

    def restore_all(self):
        """
        clear all register <obj>
        :return: None
        """
        self._key_dict = {}
        self._count = 0
        #
        self._key_list = []
        self._obj_list = []

    def _set_object_register_(self, obj):
        """
        if <obj> is exists return exists <obj> else add it
        :param obj: instance(<obj>)
        :return: instance(<obj>)
        """
        key = self.get_key(obj)
        if self.get_object_exists(key) is True:
            return self.get_object(key)
        self.set_object_add(obj)
        return obj

    def get_count(self):
        """
        :return: int
        """
        return self._count

    def get_maximum(self):
        if self._count > 0:
            return self._count-1
        return 0

    def get_object_indices(self):
        """
        :return: list[int(<obj-index>), ...]
        """
        return range(len(self.get_object_indices()))

    def __getitem__(self, index):
        """
        :param index: int(<obj-index>)
        :return: instance(<obj>)
        """
        return self.get_object_at(index)

    def __contains__(self, key):
        """
        :param key: str(<obj-key>)
        :return: bool
        """
        return self.get_object_exists(key)


class AbsObjToken(object):
    """
    abstract for <obj-token>
    """
    TYPE_PATHSEP = None
    OBJ_PATHSEP = None
    PORT_PATHSEP = None
    PORT_ASSIGN_PATHSEP = None

    @classmethod
    def _get_port_source_token_(cls, source_port_path):
        return cls._get_port_token_(
            unr_core.UnrPortAssign.OUTPUTS, source_port_path
        )

    @classmethod
    def _get_obj_source_token_(cls, source_obj_path, source_port_path):
        return cls.PORT_PATHSEP.join(
            [source_obj_path, cls._get_port_source_token_(source_port_path)]
        )

    @classmethod
    def _get_port_target_token_(cls, target_port_path):
        return cls._get_port_token_(
            unr_core.UnrPortAssign.INPUTS, target_port_path
        )

    @classmethod
    def _get_obj_target_token_(cls, target_obj_path, target_port_path):
        return cls.PORT_PATHSEP.join(
            [target_obj_path, cls._get_port_target_token_(target_port_path)]
        )

    @classmethod
    def _get_obj_connection_token_(cls, source_obj_path, source_port_path, target_obj_path, target_port_path):
        source_token = cls._get_obj_source_token_(source_obj_path, source_port_path)
        target_token = cls._get_obj_target_token_(target_obj_path, target_port_path)
        return ' >> '.join(
            [source_token, target_token]
        )

    @classmethod
    def _get_port_token_(cls, port_assign, port_path):
        return cls.PORT_ASSIGN_PATHSEP.join(
            [port_assign, port_path]
        )


# obj/def
class AbsObjBaseDef(object):
    """
    abstract for <obj> definition
        etc: <dcc-obj>, <plf-obj>("file", "directory"), ...
    """

    def _init_obj_base_def_(self, name):
        """
        :param name:
        :return: None
        """
        self._name = name

    def get_name(self):
        return self._name

    @property
    def name(self):
        return self._name

    def get_is_naming_match(self, pattern):
        return fnmatch.filter(
            [self.name], pattern
        ) != []

    def get_name_is_matched(self, p):
        return fnmatch.filter(
            [self.name], p
        ) != []


# obj/gui/def
class AbsGuiExtraDef(object):

    @property
    def pathsep(self):
        raise NotImplementedError()

    @property
    def path(self):
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()

    def _init_gui_extra_def_(self):
        self._language = 'english'
        self._custom_raw = {}

    @property
    def gui_attributes(self):
        return self._custom_raw

    @gui_attributes.setter
    def gui_attributes(self, raw):
        if isinstance(raw, dict):
            self._custom_raw = raw
        else:
            raise TypeError()

    @property
    def label(self):
        return self.get_gui_attribute('label')

    @property
    def description(self):
        return self.get_gui_attribute('description')

    def set_description(self, text):
        self.set_gui_attribute('description', text)

    @property
    def icon(self):
        return self.get_gui_attribute('icon')

    @property
    def icon_file(self):
        return self.icon

    def get_path_prettify(self):
        p = self.path
        pathsep = self.pathsep
        #
        _ = p.split(pathsep)
        if len(_) > 6:
            if bsc_storage.StgPathMtd.get_path_is_windows(p):
                return u'{0}{2}...{2}{1}'.format(pathsep.join(_[:3]), pathsep.join(_[-3:]), pathsep)
            elif bsc_storage.StgPathMtd.get_path_is_linux(p):
                return u'{0}{2}...{2}{1}'.format(pathsep.join(_[:2]), pathsep.join(_[-3:]), pathsep)
            else:
                return p
        else:
            return p

    def get_path_prettify_(self, maximum=24):
        p = self.path
        n = self.name
        #
        maximum_ = max(min(maximum-len(n), maximum), 8)
        #
        d = p[:-len(n)-1]
        c = len(d)
        if c > maximum_:
            return u'{}...{}/{}'.format(d[:(int(maximum_/2))], d[-(int(maximum_/2)+3):], n)
        return p

    def set_gui_attribute(self, key, value):
        self._custom_raw[key] = value

    def get_gui_attribute(self, key):
        return self._custom_raw.get(key)

    def set_obj_gui(self, gui):
        self.set_gui_attribute('gui_obj', gui)

    def get_obj_gui(self):
        return self.get_gui_attribute('gui_obj')

    def set_gui_ng_graph_node(self, gui):
        self.set_gui_attribute('gui_ng_graph_node', gui)

    def get_gui_ng_graph_node(self):
        return self.get_gui_attribute('gui_ng_graph_node')

    def set_gui_ng_tree_node(self, gui):
        self.set_gui_attribute('gui_ng_tree_node', gui)

    def get_gui_ng_tree_node(self):
        return self.get_gui_attribute('gui_ng_tree_node')

    def set_gui_menu_raw(self, raw):
        self.set_gui_attribute('gui_menu', raw)

    def set_gui_menu_raw_append(self, raw):
        pre_raw = self.get_gui_attribute('gui_menu') or []
        pre_raw.append(raw)
        self.set_gui_menu_raw(pre_raw)

    def set_gui_menu_raw_extend(self, raw):
        pre_raw = self.get_gui_attribute('gui_menu') or []
        pre_raw.extend(raw)
        self.set_gui_menu_raw(pre_raw)

    def get_gui_menu_raw(self):
        return self.get_gui_attribute('gui_menu')

    def set_gui_extra_menu_raw(self, raw):
        self.set_gui_attribute('gui_extra_menu', raw)

    def get_gui_extra_menu_raw(self):
        return self.get_gui_attribute('gui_extra_menu')

    #
    def set_gui_extend_menu_raw(self, raw):
        self.set_gui_attribute('gui_extend_menu', raw)

    def get_gui_extend_menu_raw(self):
        return self.get_gui_attribute('gui_extend_menu')

    def set_gui_menu_content(self, content):
        self.set_gui_attribute('gui_menu_content', content)

    def get_gui_menu_content(self):
        return self.get_gui_attribute('gui_menu_content')


# <port-query>
class AbsPortQuery(object):
    OBJ_TOKEN = None
    #
    PATHSEP = None

    def __init__(self, obj, type_path, port_path, port_assign, raw):
        self._obj = obj
        self._type = self.obj.universe._get_type(type_path)
        self._port_path = port_path
        self._port_assign = port_assign
        #
        self._value = self.type.set_value_create(raw)
        self._raw = raw

    # type
    @property
    def obj(self):
        return self._obj

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

    def get_path(self):
        return self.PATHSEP.join(
            [self.obj.path, self.port_path]
        )

    # obj
    @property
    def path(self):
        return self.PATHSEP.join(
            [self.obj.path, self.port_path]
        )

    @property
    def pathsep(self):
        return self.PATHSEP

    # port
    @property
    def port_path(self):
        return self._port_path

    # stack
    @property
    def token(self):
        port_assign = self.port_assign
        port_path = self.port_path
        return self.OBJ_TOKEN._get_port_token_(port_assign, port_path)

    @property
    def port_assign(self):
        return self._port_assign

    def get_value(self):
        return self._value

    def set(self, raw):
        self.get_value().set(raw)

    def get(self):
        return self.get_value().get()

    def _get_stack_key_(self):
        return self.token

    def __str__(self):
        return '{}(path="{}", type="{}", raw="{}")'.format(
            self.__class__.__name__,
            self.path,
            self.type.path,
            self.get()
        )

    def __repr__(self):
        return self.__str__()


# value
class AbsValue(object):
    def __init__(self, type_, raw):
        self._type = type_
        self._raw = raw

    @property
    def universe(self):
        return self.type.universe

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
    def category(self):
        """
        :return: instance(<obj-category>)
        """
        return self.type.category

    @property
    def category_name(self):
        return self.category.name

    # <type-constant>
    def get_is_constant(self):
        return self.type.get_is_constant()

    def get_is_boolean(self):
        return self.type.get_is_boolean()

    # <type-tuple>
    def get_is_vector(self):
        return self.type.get_is_vector()

    def get_is_color(self):
        return self.type.get_is_color()

    def get_is_tuple(self):
        return self.type.get_is_tuple()

    def get_tuple_size(self):
        return self.type.get_tuple_size()

    def get_channel(self, index):
        if self.get_is_array() is False:
            channel_type = self.type.get_channel_type()
            tuple_size = self.get_tuple_size()
            if tuple_size > 0:
                if index > tuple_size:
                    return channel_type.set_value_create(None)
                return channel_type.set_value_create(self.get()[index])
            return channel_type.set_value_create(None)

    # <type-matrix>
    def get_is_matrix(self):
        return self.type.get_is_matrix()

    # <type-array>
    def get_is_array(self):
        return self.type.get_is_array()

    def get_array_size(self):
        if self.get_is_array():
            return len(self.get())
        return 0

    def get_element(self, index):
        if self.get_is_array():
            element_type = self.type.get_element_type()
            array_size = self.get_array_size()
            if array_size > 0:
                if index > array_size:
                    return element_type.set_value_create(None)
                return element_type.set_value_create(self.get()[index])
            return element_type.set_value_create(None)

    #
    def get(self):
        return self._raw

    def set(self, raw):
        self._raw = raw

    def get_as_string(self):
        if self.get_is_array():
            return u', '.join([self.get_element(i).get_as_string() for i in range(self.get_array_size())])
        elif self.type.get_is_vector() or self.type.get_is_color():
            return u','.join([self.get_channel(i).get_as_string() for i in range(self.get_tuple_size())])
        elif self.type.get_is_matrix():
            return u', '.join([self.get_channel(i).get_as_string() for i in range(self.get_tuple_size())])
        else:
            if self.get_is_boolean():
                return [u'false', u'true'][self.get()]
            else:
                return unicode(self.get())

    def get_as_obj(self):
        obj_string = self.get()
        if isinstance(obj_string, six.string_types):
            return self.universe.get_obj(obj_string)

    def _format_dict_(self):
        return {
            'category': self.type.category,
            'type': self.type
        }

    def to_properties(self):
        p = ctt_core.Properties(self)
        p.set(
            'category', self.category_name
        )
        p.set(
            'type', self.type_name
        )
        p.set(
            'raw', self.get()
        )
        return p

    def __str__(self):
        return 'Value(type="{}", raw="{}")'.format(
            self.type.path,
            self.get_as_string(),
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if other is not None:
            return self.get() == other.get()
        return False

    def __ne__(self, other):
        return self.get() != other.get()
