# coding:utf-8
import sys

import inspect

import six

import copy

import os

import collections

import json

import hashlib

import yaml

from . import base as _base


# operate for dict, value must be dict or file.
# file format only support "yaml" or "json", file must exist and data must be a dict.
class AbsContent(object):
    VALUE_DEFAULT = collections.OrderedDict()
    PATHSEP = None

    # key use quote, etc. "$a", "$.a", quote do not support nested
    def __unfold_quote(self, key_path, keys_all):
        value = self.get(key_path)
        filter_fnc = _base.ContentUtil.filter
        if isinstance(value, six.string_types):
            if filter_fnc([value], '$*'):
                key_ = value[1:].lstrip()
                # check is use relative path, etc. "..a"
                if filter_fnc([key_], '.*'):
                    _ = key_.split('.')
                    d_c = len([i for i in _ if i == ''])
                    k_p_2 = six.u('.').join(key_path.split('.')[:-d_c])
                    if k_p_2:
                        key_real = six.u('{}.{}').format(k_p_2, '.'.join(_[d_c:]))
                    else:
                        key_real = six.u('.').join(_[d_c:])
                else:
                    key_real = key_
                #
                if key_real not in keys_all:
                    raise KeyError('key is not found: "{}"'.format(key_real))
                # must use copy
                self.set(key_path, copy.deepcopy(self.get(key_real)))
            # real "$"
            elif filter_fnc([value], '\\$*'):
                self.set(key_path, value.replace('\\$', '$'))

    def __unfold_inherit_and_override(self, key_path, keys_all):
        # etc. $: <key-path>
        filter_fnc = _base.ContentUtil.filter
        if filter_fnc([key_path], '*$'):
            value = self.get(key_path)
            if filter_fnc([value], '.*'):
                key_inherit = _base.ContentUtil.get_absolute_key(value, key_path)
            else:
                key_inherit = value
            #
            if key_inherit not in keys_all:
                raise KeyError('key="{}" is non-exists'.format(key_inherit))
            #
            k = '.'.join(key_path.split('.')[:-1])
            inherit_dict = copy.deepcopy(
                self.get(key_inherit)
            )
            override_dict = copy.deepcopy(
                self.get(k)
            )
            override_dict.pop('$')
            inherit_dict.update(override_dict)
            self.set(k, inherit_dict)

    def __init__(self, key=None, value=None):
        self.__key = key
        self.__file_path = None
        # check value type
        # when value is file, auto read file
        if isinstance(value, six.string_types):
            file_path = value
            if os.path.isfile(file_path):
                self.__file_path = value
                _ = _base.ContentFile(self.__file_path).read()
                if isinstance(_, dict):
                    self.__value = _
                else:
                    self.__value = self.VALUE_DEFAULT
            else:
                raise IOError(
                    'file is not found: "{}"'.format(value)
                )

        elif isinstance(value, dict):
            self.__value = value
        else:
            self.__value = self.VALUE_DEFAULT

        self.__key_unfold_excludes = []

    def __str__(self):
        return _base.ToString(
            self.get_value()
        ).generate()

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self.__file_path
        )

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __copy__(self):
        return self.__class__(
            self.__key, copy.copy(self.__value)
        )

    def __deepcopy__(self, memo=None):
        return self.__class__(
            self.__key, copy.deepcopy(self.__value, memo)
        )

    def __hash__(self):
        s = hashlib.md5(
            json.dumps(self.__value)
        ).hexdigest()
        return s.upper()

    def save_to(self, file_path):
        _base.ContentFile(file_path).write(self.__value)

    def save(self):
        _base.ContentFile(self.__file_path).write(self.__value)

    def get_key(self):
        return self.__key

    key = property(get_key)

    def get_value(self):
        return self.__value

    value = property(get_value)

    def set_value(self, value):
        self.__value = value

    def get_value_as_copy(self):
        return copy.deepcopy(self.__value)

    value_as_copy = property(get_value_as_copy)

    def get_file_path(self):
        return self.__file_path

    file_path = property(get_file_path)

    def get_is_empty(self):
        return not self.__value

    def get_all_keys(self):
        def rcs_fnc_(k_, v_):
            for _k, _v in v_.items():
                if k_ is not None:
                    _key = six.u('{}.{}').format(k_, _k)
                else:
                    _key = _k
                list_.append(_key)
                if isinstance(_v, dict):
                    rcs_fnc_(_key, _v)

        list_ = []
        rcs_fnc_(self.__key, self.__value)
        return list_

    def get_all_leaf_keys(self):
        def rcs_fnc_(k_, v_):
            for _k, _v in v_.items():
                if k_ is not None:
                    _key = six.u('{}.{}').format(k_, _k)
                else:
                    _key = _k
                #
                if isinstance(_v, dict):
                    rcs_fnc_(_key, _v)
                    if not _v:
                        list_.append(_key)
                else:
                    list_.append(_key)

        list_ = []
        rcs_fnc_(self.__key, self.__value)
        return list_

    def get_all_leaf_values(self):
        def rcs_fnc_(k_, v_):
            for _k, _v in v_.items():
                if k_ is not None:
                    _key = six.u('{}.{}').format(k_, _k)
                else:
                    _key = _k
                #
                if isinstance(_v, dict):
                    rcs_fnc_(_key, _v)
                else:
                    list_.append(_v)

        list_ = []
        rcs_fnc_(self.__key, self.__value)
        return list_

    def get_keys(self, regex=None):
        _ = self.get_all_keys()
        if regex is not None:
            return _base.ContentUtil.filter(_, regex)
        return _

    def get_key_names_at(self, key_path=None):
        if key_path:
            value = self.get(key_path)
            if isinstance(value, dict):
                return value.keys()
            return []
        return self.value.keys()

    def get_all_leaf_key_as_dag_paths(self):
        keys = self.get_all_leaf_keys()
        if keys:
            return [_base.ContentUtil.key_path_to_dag_path(i) for i in keys]
        return []

    def get_all_key_as_dag_paths(self):
        keys = self.get_all_keys()
        if keys:
            return ['/']+[_base.ContentUtil.key_path_to_dag_path(i) for i in keys]
        return []

    def get_top_keys(self):
        return self.__value.keys()

    def get_keys_by_value(self):
        pass

    def get(self, key_path, default_value=None):
        ks = key_path.split(self.PATHSEP)
        v = self.__value
        for k in ks:
            if isinstance(v, dict):
                if k in v:
                    v = v[k]
                else:
                    return default_value
            else:
                return default_value
        return v

    def get_as_content(self, key_path, relative=False):
        key = key_path.split(self.PATHSEP)[-1]
        value = self.get(key_path)
        if isinstance(value, dict):
            if relative is True:
                return self._create_fnc(None, value)
            return self._create_fnc(key, value)

    def _create_fnc(self, key, value):
        if isinstance(value, dict) is False:
            raise TypeError()
        return self.__class__(
            key, value
        )

    def set(self, key_path, value):
        ks = key_path.split(self.PATHSEP)
        v = self.__value
        #
        maximum = len(ks)-1
        for seq, k in enumerate(ks):
            if seq == maximum:
                v[k] = value
            else:
                if k not in v:
                    v[k] = collections.OrderedDict()
                #
                v = v[k]

    def append_element(self, key_path, value):
        v = self.get(key_path)
        if isinstance(v, (tuple, list)):
            es = v
        else:
            es = []
            self.set(key_path, es)
        #
        es.append(value)

    def get_key_is_exists(self, key_path):
        return key_path in self.get_all_keys()

    def do_clear(self):
        self.__value = collections.OrderedDict()

    def update_from_content(self, content):
        if isinstance(content, self.__class__):
            for i_key in content.get_all_leaf_keys():
                self.set(i_key, content.get(i_key))

    def update_from(self, arg):
        if isinstance(arg, self.__class__):
            self.__value.update(arg.get_value())
        elif isinstance(arg, dict):
            self.__value.update(arg)

    def get_str_as_yaml_style(self):
        return _base.ContentYamlBase.dump(
            self.value,
            indent=4,
            default_flow_style=False
        )

    def print_as_yaml_style(self):
        sys.stdout.write(
            self.get_str_as_yaml_style()+'\n'
        )

    def do_flatten(self):
        keys_all = self.get_keys()
        #
        for i_key in keys_all:
            i_value = self.get(i_key)
            if isinstance(i_value, dict) is False:
                self.__unfold_inherit_and_override(i_key, keys_all)
        #
        for i_key in keys_all:
            i_value = self.get(i_key)
            if isinstance(i_value, dict) is False:
                self.__unfold_quote(i_key, keys_all)
        #
        keys_all = self.get_keys()
        for i_key in keys_all:
            i_value = self.get(i_key)
            if isinstance(i_value, dict) is False:
                i_value = _base.ContentUtil.unfold_fnc(
                    i_key,
                    keys_all=keys_all,
                    keys_exclude=self.__key_unfold_excludes,
                    get_fnc=self.get
                )
                self.set(i_key, i_value)

    def reload(self):
        if self.__file_path is not None:
            if os.path.isfile(self.__file_path):
                _ = _base.ContentFile(self.__file_path).read()
                if isinstance(_, dict):
                    self.__value = _
                else:
                    self.__value = collections.OrderedDict()

    @classmethod
    def serialize(cls, data, indent=0, level=0):
        """ Recursively serialize a complex structure with custom indentation. """
        ind = ' '*indent*level  # Current indentation
        if isinstance(data, dict):
            # Handle dictionaries
            items = []
            for key, value in six.iteritems(data):  # Compatible way to iterate dicts in both Py2 and Py3
                items.append(u"%s%r: %s"%(ind, key, cls.serialize(value, indent, level+1)))
            return u'{\n'+u',\n'.join(items)+u'\n'+(' '*indent*(level-1))+u'}'
        elif isinstance(data, list):
            # Handle lists
            items = [u"%s%s"%(ind, cls.serialize(item, indent, level+1)) for item in data]
            return u'[\n'+u',\n'.join(items)+u'\n'+(' '*indent*(level-1))+u']'
        elif isinstance(data, tuple):
            # Handle tuples
            items = [u"%s%s"%(ind, cls.serialize(item, indent, level+1)) for item in data]
            return u'(\n'+u',\n'.join(items)+u'\n'+(' '*indent*(level-1))+u')'
        elif isinstance(data, six.text_type):
            # Handle Unicode strings explicitly (six.text_type is 'unicode' in Py2, 'str' in Py3)
            return u"u'%s'"%data
        elif isinstance(data, six.binary_type):
            # Handle byte strings explicitly (six.binary_type is 'str' in Py2, 'bytes' in Py3)
            return repr(data)
        else:
            if six.PY2:
                # Ensure proper handling of non-ASCII characters in Python 2
                return unicode(repr(data), 'utf-8')
            else:
                return str(repr(data))

    def items(self):
        return self.__value.items()


class Content(AbsContent):
    PATHSEP = '.'

    def __init__(self, key=None, value=None):
        super(Content, self).__init__(key, value)


class Dict(AbsContent):
    PATHSEP = '.'

    def __init__(self, key=None, value=None):
        super(Dict, self).__init__(
            key=key, value=value or collections.OrderedDict()
        )


class YmlDict(AbsContent):
    PATHSEP = '.'

    def __init__(self, key=None, value=None):
        super(YmlDict, self).__init__(
            key=key, value=value or collections.OrderedDict()
        )

    def __str__(self):
        return _base.ToString(
            self.get_value()
        ).generate()


class Property(object):
    def __init__(self, properties, key):
        self.__properties = properties
        self.__key = key

    def get_key(self):
        return self.__key

    key = property(get_key)

    def get_value(self):
        return self.__properties.get(self.__key)

    value = property(get_value)

    @value.setter
    def value(self, value):
        self.__properties.get(self.__key, value)

    def __str__(self):
        return '{}={}'.format(
            self.__key, self.get_value()
        )


class Properties(AbsContent):
    PATHSEP = '.'
    PROPERTY_CLS = Property

    def __init__(self, obj, raw=None):
        self.__obj = obj
        super(Properties, self).__init__(value=raw or collections.OrderedDict())

    def get_property(self, key):
        return self.PROPERTY_CLS(self, key)


# cache for content, auto generate when timestamp is changed
class ContentCache(object):
    def __init__(self, file_path):
        self.__file_path = file_path
        if os.path.isfile(file_path) is False:
            _base.ContentFile(file_path).write({})

        self.__timestamp = os.stat(self.__file_path).st_mtime
        self.__content = Content(
            value=file_path
        )

    def generate(self):
        ts = os.stat(self.__file_path).st_mtime
        if ts == self.__timestamp:
            return self.__content
        self.__timestamp = ts
        self.__content = Content(
            value=self.__file_path
        )
        return self.__content


class NodeProperties(dict):
    def __init__(self, *args, **kwargs):
        super(NodeProperties, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        return self.__getitem__(item)  # = self[item]


class DictProperties(dict):
    def __init__(self, *args, **kwargs):
        super(DictProperties, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        return self.__getitem__(item)  # = self[item]

    def __str__(self):
        return '(\n{}\n)'.format(
            '\n'.join(
                ['    {}={}'.format(k, v) for k, v in self.items()]
            )
        )


class Configure(object):
    def __init__(self, *args, **kwargs):
        pass

    def _get_subclass_file_path(self):
        frame = inspect.currentframe().f_back
        subclass = frame.f_locals.get('self', None)
        if subclass and isinstance(subclass, self.__class__):
            file_path = inspect.getfile(type(subclass))
            return os.path.abspath(file_path)
        return None

    def generate_local_configure(self):
        self._configure_local_flag = True

        file_path = self._get_subclass_file_path()
        cfg_file_path = '{}.yml'.format(os.path.splitext(file_path)[0].replace('\\', '/'))
        if os.path.isfile(cfg_file_path):
            return Dict(value=cfg_file_path)
        else:
            raise RuntimeError()
