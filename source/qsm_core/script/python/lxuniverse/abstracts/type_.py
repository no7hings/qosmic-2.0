# coding:utf-8
import six
# universe
from .. import core as unr_core


# type/def
class AbsCategoryBaseDef(object):
    """
    abstract for <category>/<obj-category> definition
        type-register
        type-query
        type-gain
    """
    # str(<type-pathsep>/<obj-type-pathsep>)
    PATHSEP = None
    # class(<type>/<obj-type>)
    TYPE_CLS = None

    def _init_category_base_def_(self, universe, name, type_stack):
        """
        :param universe: instance(<obj-universe>)
        :param name: str(<category-name>/<obj-category-name>)
        :param type_stack: instance(<type-stack>/<obj-type-stack>)
        :return:
        """
        self._universe = universe
        self._name = name
        self._type_stack = type_stack

    @property
    def universe(self):
        """
        :return: instance(<obj-universe>)
        """
        return self._universe

    @property
    def name(self):
        """
        :return: str(<category-name>/<obj-category-name>)
        """
        return self._name

    @property
    def path(self):
        """
        :return: str(<category-path>/<obj-category-path>)
        """
        return self.name

    @property
    def pathsep(self):
        """
        :return: str(<type-pathsep>/<obj-type-pathsep>)
        """
        return self.TYPE_CLS.PATHSEP

    #
    def _new_type_(self, type_name):
        """
        :param type_name: str(<type-name>/<obj-type-name>)
        :return: instance(<type>)
        """
        return self.TYPE_CLS(self, type_name)

    def generate_type(self, type_name):
        category = self
        category_name = self.name
        stack = self._type_stack
        key = self._get_type_path_(category_name, type_name)
        if stack.get_object_exists(key) is True:
            return stack.get_object(key)
        #
        type_ = category._new_type_(type_name)
        stack.set_object_add(type_)
        return type_

    def get_type(self, type_name):
        """
        :param type_name: str(<type-name>)
        :return:
        """
        category_name = self.name
        return self._type_stack.get_object(
            self._get_type_path_(category_name, type_name)
        )

    def get_types(self):
        """
        :return: list[instance(<type>), ...]
        """
        category_name = self.name
        type_name = '*'
        regex = self._get_type_path_(category_name, type_name)
        return self._type_stack.get_objects(regex=regex)

    def _get_stack_key_(self):
        """
        method for <obj-stack>
        :return: str
        """
        return self.path

    def _format_dict_(self):
        """
        method for variant-convert
        :return: dict
        """
        return {
            'self': self,
            'category': self
        }

    @classmethod
    def _get_type_path_(cls, category_name, type_name):
        """
        :param category_name: str(<category-name>/<obj-category-name>)
        :param type_name: str(<type-name>/<obj-type-name>)
        :return: str(<type-path>/<obj-type-path>)
        """
        type_pathsep = cls.TYPE_CLS.PATHSEP
        return type_pathsep.join(
            [category_name, type_name]
        )

    @classmethod
    def _get_type_path_args_(cls, type_path):
        type_pathsep = cls.TYPE_CLS.PATHSEP
        return type_path.split(type_pathsep)

    def __str__(self):
        return '{}(path="{}")'.format(
            self.__class__.__name__,
            self.path
        )

    def __repr__(self):
        return self.__str__()


class AbsTypeBaseDef(object):
    """
    abstract for <type>/<obj-type> definition
    """
    # str(<type-pathsep>/<obj-type-pathsep>)
    PATHSEP = None

    def _init_type_base_def_(self, category, name):
        """
        :param category: instance(<category>/<obj-category>)
        :param name: str(<type-name>)
        :return:
        """
        self._category = category
        self._name = name

    @property
    def category(self):
        """
        :return: instance(<category>/<obj-category>)
        """
        return self._category

    @property
    def category_name(self):
        return self.category.name

    @property
    def universe(self):
        """
        :return: instance(<obj-universe>)
        """
        return self.category.universe

    @property
    def name(self):
        """
        :return: str(<category-name>/<obj-category-name>)
        """
        return self._name

    @property
    def path(self):
        """
        :return: str(<category-path>/<obj-category-path>)
        """
        return self.category._get_type_path_(
            self.category.name, self.name
        )

    @property
    def pathsep(self):
        """
        :return: str(<type-pathsep>/<obj-type-pathsep>)
        """
        return self.PATHSEP

    def _get_stack_key_(self):
        """
        method for <obj-stack>
        :return: str
        """
        return self.path

    def _format_dict_(self):
        """
        method for variant-convert
        :return: dict
        """
        return {
            'self': self,
            'category': self._category,
            'type': self,
        }

    def __str__(self):
        return '{}(path="{}")'.format(
            self.__class__.__name__,
            self.path
        )

    def __repr__(self):
        return self.__str__()


# <category>
class AbsCategory(AbsCategoryBaseDef):
    """
    abstract for <category>
    """

    def __init__(self, universe, name):
        """
        :param universe: instance(<obj-universe>)
        :param name: str(<category-name>)
        """
        self._init_category_base_def_(universe, name, universe._type_stack)


# <type>
class AbsType(AbsTypeBaseDef):
    """
    abstract for <type>
    """

    def __init__(self, category, name):
        """
        :param category: instance(<obj-universe>)
        :param name: str(<type-name>)
        """
        self._init_type_base_def_(category, name)

    # <type-constant>
    def get_is_constant(self):
        return self.category.name == unr_core.UnrCategory.CONSTANT

    def get_is_boolean(self):
        type_name = self.name
        return unr_core.UnrType.get_is_boolean(type_name)

    # <type-tuple>
    def get_is_color(self):
        type_name = self.name
        return unr_core.UnrType.get_is_color(type_name)

    def get_is_vector(self):
        type_name = self.name
        return unr_core.UnrType.get_is_vector(type_name)

    def get_is_tuple(self):
        type_name = self.name
        return unr_core.UnrType.get_is_tuple(type_name)

    #
    def get_tuple_size(self):
        if self.get_is_array() is False:
            type_name = self.name
            return unr_core.UnrType.get_tuple_size(type_name)
        return -1

    # <type-matrix>
    def get_is_matrix(self):
        type_name = self.name
        return unr_core.UnrType.get_is_matrix(type_name)

    def get_channel_type(self):
        if self.get_is_array() is False:
            category_name = self.category.name
            if self.get_is_vector() or self.get_is_color():
                channel_category_name = unr_core.UnrCategory.CONSTANT
            elif self.get_is_matrix():
                channel_category_name = unr_core.UnrCategory.VECTOR
            else:
                return None
            type_name = unr_core.UnrType.get_channel_type_name(category_name)
            category = self.universe.get_category(channel_category_name)
            return category.generate_type(type_name)

    # <type-array>
    def get_is_array(self):
        return self.category.name == unr_core.UnrCategory.ARRAY

    def get_element_type(self):
        if self.get_is_array():
            if self.get_is_color():
                element_category_name = unr_core.UnrCategory.COLOR
            elif self.get_is_vector():
                element_category_name = unr_core.UnrCategory.VECTOR
            elif self.get_is_matrix():
                element_category_name = unr_core.UnrCategory.MATRIX
            else:
                element_category_name = unr_core.UnrCategory.CONSTANT
            type_name = self.name
            category = self.universe.get_category(element_category_name)
            return category.generate_type(type_name)

    def set_value_create(self, raw):
        type_name = self.name
        is_array = self.get_is_array()
        #
        cls = self._get_value_class_(type_name, is_array)
        return cls(self, raw)

    @classmethod
    def get_raw_flatten(cls, raw):
        def _rcs_fnc(i_):
            if isinstance(i_, (tuple, list)):
                for _j in i_:
                    _rcs_fnc(_j)
            else:
                lis.append(i_)

        lis = []
        _rcs_fnc(raw)
        return lis

    def _get_stack_key_(self):
        return self.path

    def _get_value_class_(self, type_name, is_array):
        raise NotImplementedError()


# <port-query>
class AbsTypePortQueryExtraDef(object):
    OBJ_TOKEN = None
    #
    PORT_QUERY_CLS = None
    PORT_QUERY_STACK_CLS = None

    def _init_type_port_query_extra_def_(self):
        self._port_query_stack = self.PORT_QUERY_STACK_CLS()

    def _build_port_queries_(self, port_query_raw, raw_convert_method=None):
        for k, v in port_query_raw.items():
            self._build_port_query_(k, v, raw_convert_method)

    def _build_port_query_(self, key, value, raw_convert_method=None):
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
            raw = value.get('raw')
        else:
            port_assign = unr_core.UnrPortAssign.VARIANTS
            type_path = unr_core.UnrType.CONSTANT_RAW_
            raw = value
        #
        if raw_convert_method is not None:
            raw = raw_convert_method(value.get('raw'))
        #
        token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        if self._port_query_stack.get_object_exists(token) is True:
            port_query = self._port_query_stack.get_object(token)
        else:
            port_query = self._create_port_query_(
                type_path, port_path, port_assign, raw
            )
            self._port_query_stack.set_object_add(port_query)
        #
        port_query.set(raw)

    def _create_port_query_(self, type_path, port_path, port_assign, raw):
        return self.PORT_QUERY_CLS(
            self, type_path, port_path, port_assign, raw
        )

    def _inherit_port_query_(self, port_query):
        type_path = port_query.type.path
        port_path = port_query.port_path
        port_assign = port_query.port_assign
        raw = port_query.get()
        port_query = self.PORT_QUERY_CLS(
            self, type_path, port_path, port_assign, raw
        )
        self._port_query_stack.set_object_add(port_query)

    def get_port_queries(self, regex=None):
        return self._port_query_stack.get_objects(regex)

    def get_port_query(self, token):
        return self._port_query_stack.get_object(token)

    def get_port_query_is_exists(self, token):
        return self._port_query_stack.get_object_exists(token)

    #
    def get_input_port_query(self, port_path):
        port_assign = unr_core.UnrPortAssign.INPUTS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port_query(port_token)

    def get_input_port_queries(self):
        format_dict = {
            'port_assign': unr_core.UnrPortAssign.INPUTS,
            'port_assign_pathsep': unr_core.UnrPortAssign.PATHSEP
        }
        return self._port_query_stack.get_objects(
            regex=unr_core.UnrObj.PORTS_GAIN_REGEX.format(**format_dict)
        )

    def get_output_port_query(self, port_path):
        port_assign = unr_core.UnrPortAssign.OUTPUTS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port_query(port_token)

    def get_output_port_queries(self):
        format_dict = {
            'port_assign': unr_core.UnrPortAssign.OUTPUTS,
            'port_assign_pathsep': unr_core.UnrPortAssign.PATHSEP
        }
        return self._port_query_stack.get_objects(
            regex=unr_core.UnrObj.PORTS_GAIN_REGEX.format(**format_dict)
        )

    def get_variant_port_query(self, port_path):
        port_assign = unr_core.UnrPortAssign.VARIANTS
        port_token = self.OBJ_TOKEN._get_port_token_(port_assign, port_path)
        return self.get_port_query(port_token)

    # noinspection PyUnusedLocal
    def get_variant_port_queries(self, regex=None):
        format_dict = dict(
            port_assign=unr_core.UnrPortAssign.VARIANTS,
            port_assign_pathsep=unr_core.UnrPortAssign.PATHSEP,
            regex_extra=regex
        )
        if regex is not None:
            return self._port_query_stack.get_objects(
                regex=unr_core.UnrObj.PORTS_GAIN_REGEX_EXTRA.format(**format_dict)
            )
        return self._port_query_stack.get_objects(
            regex=unr_core.UnrObj.PORTS_GAIN_REGEX.format(**format_dict)
        )

    def get_variant(self, port_path):
        port_path = port_path.replace('/', self.PORT_QUERY_CLS.PATHSEP)
        port_query = self.get_variant_port_query(port_path)
        if port_query:
            return port_query.get()

    def set_variant(self, port_path, raw):
        port_path = port_path.replace('/', self.PORT_QUERY_CLS.PATHSEP)
        port_query = self.get_variant_port_query(port_path)
        if port_query:
            return port_query.set(raw)


# obj/type/def
class AbsTypeObjExtraDef(object):
    # class(<obj>)
    DCC_NODE_CLS = None

    def _init_type_obj_extra_def_(self):
        pass

    @property
    def universe(self):
        raise NotImplementedError()

    @property
    def category(self):
        raise NotImplementedError()

    @property
    def category_name(self):
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()

    def generate_obj(self, obj_path_args, **kwargs):
        # etc: /a/b/c
        if isinstance(obj_path_args, six.string_types):
            obj_path = obj_path_args
        # etc: [a, b, c, ...]
        elif isinstance(obj_path_args, (tuple, list)):
            obj_path = self._get_obj_path_(obj_path_args)
        else:
            raise TypeError()

        obj = self.universe.get_obj(obj_path)
        if obj is not None:
            if obj.type.name == unr_core.UnrObjType.NULL:
                old_obj = obj
                new_obj = self._create_obj_(obj_path)
                self.universe._override_obj_(old_obj, new_obj)
                return new_obj
            return obj
        obj = self._create_obj_(obj_path)
        self.universe._add_obj_(obj)
        return obj

    def create_obj(self, obj_oath):
        obj = self.DCC_NODE_CLS(self, obj_oath)
        self.universe._add_obj_(obj)
        return obj

    @property
    def obj_pathsep(self):
        return self.DCC_NODE_CLS.PATHSEP

    @classmethod
    def _get_obj_path_(cls, obj_path_args):
        return cls.DCC_NODE_CLS.PATHSEP.join(obj_path_args)

    def _create_obj_(self, obj_path, **kwargs):
        new_obj = self.DCC_NODE_CLS(self, obj_path)
        new_obj.create_ancestors()
        return new_obj

    def get_objs(self):
        """
        regex-etc: "obj_category_name/obj_type_name@*"
        :return: list[instance(<obj>), ...]
        """
        obj_category_name = self.category.name
        obj_type_name = self.name
        obj_string = '*'
        regex = self.category._get_obj_token_(
            obj_category_name, obj_type_name, obj_string
        )
        return self.universe._obj_stack.get_objects(regex=regex)


# <obj-category>
class AbsObjCategory(
    AbsCategoryBaseDef,
    AbsTypePortQueryExtraDef
):
    def __init__(self, universe, name):
        self._init_category_base_def_(universe, name, universe._obj_type_stack)
        self._init_type_port_query_extra_def_()

    def _new_type_(self, type_name):
        obj_type = self.TYPE_CLS(self, type_name)
        for port_query in self.get_port_queries():
            obj_type._inherit_port_query_(port_query)
        return obj_type

    def get_objs(self):
        obj_category_name = self.name
        obj_type_name = '*'
        obj_string = '*'
        regex = self._get_obj_token_(
            obj_category_name, obj_type_name, obj_string
        )
        return self.universe._obj_stack.get_objects(regex=regex)

    @classmethod
    def _get_obj_token_(cls, obj_category_name, obj_type_name, obj_string):
        """
        :param obj_category_name:
        :param obj_type_name:
        :param obj_string:
        :return:
        """
        return '@'.join(
            [cls._get_type_path_(obj_category_name, obj_type_name), obj_string]
        )


# <obj-type>
class AbsObjType(
    AbsTypeBaseDef,
    #
    AbsTypeObjExtraDef,
    AbsTypePortQueryExtraDef
):
    def __init__(self, category, name):
        self._init_type_base_def_(category, name)
        self._init_type_obj_extra_def_()
        self._init_type_port_query_extra_def_()

    def _create_obj_(self, obj_path_args, **kwargs):
        if isinstance(obj_path_args, six.string_types):
            obj_path = obj_path_args
        elif isinstance(obj_path_args, (tuple, list)):
            obj_path = self._get_obj_path_(obj_path_args)
        else:
            raise TypeError()

        new_obj = self.DCC_NODE_CLS(self, obj_path)
        for i_port_query in self.get_port_queries():
            i_type_path = i_port_query.type.path
            i_port_path = i_port_query.port_path
            i_port_assign = i_port_query.port_assign
            i_port = new_obj._create_port_(
                i_type_path, i_port_path, i_port_assign
            )
            i_port.set(i_port_query.get())
            new_obj._add_port_(i_port)
        #
        new_obj.create_ancestors()
        return new_obj
