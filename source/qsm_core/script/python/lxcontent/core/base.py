# coding:utf-8
import os

import six

import re

import json

import yaml

import fnmatch

import collections


class ContentUtil(object):
    PATTERN_KEYWORD = r'[<](.*?)[>]'
    PATTERN_KEYWORD_ESCAPE = r'[\\][<](.*?)[\\][>]'

    PATHSEP = '.'

    FILTER_CACHE = dict()
    FILTER_CACHE_MAXIMUM = 1000

    # convert to dag path
    @classmethod
    def key_path_to_dag_path(cls, key):
        return '/'+key.replace('.', '/')

    @classmethod
    def __find_children(cls, path, paths):
        list_ = []
        pathsep = cls.PATHSEP
        # etc. r'/shl/chr/test_0/[^/]*'
        if path == pathsep:
            ptn = r'{1}[^{1}]*'.format(path, pathsep)
        else:
            ptn = r'{0}{1}[^{1}]*'.format(path, pathsep)
        #
        for i_path in paths:
            if i_path != pathsep:
                _ = re.match(
                    ptn, i_path
                )
                if _ is not None:
                    if _.group() == i_path:
                        list_.append(i_path)
        return list_

    @classmethod
    def get_absolute_key_name(cls, key_relative, key_local):
        _ = key_relative.split('.')
        es = len([i for i in _ if i == ''])
        return key_local.split('.')[-es]

    @classmethod
    def get_absolute_key_index(cls, key_relative, key_local, keys_all):
        _ = key_relative.split('.')
        es = len([i for i in _ if i == ''])
        k = '.'.join(key_local.split('.')[:-es+1])
        p = '.'.join(key_local.split('.')[:-es])
        cs = cls.__find_children(p, keys_all)
        return cs.index(k)

    @classmethod
    def get_absolute_key(cls, key_relative, key_local):
        _ = key_relative.split('.')
        es = len([i for i in _ if i == ''])
        p = '.'.join(key_local.split('.')[:-es])
        if p:
            return '{}.{}'.format(p, '.'.join(_[es:]))
        return '.'.join(_[es:])

    @classmethod
    def unfold_fnc(cls, key, keys_all, keys_exclude, get_fnc):
        def rcs_fnc_(key_, value_):
            if isinstance(value_, six.string_types):
                _value_unfold = value_
                # collection excludes, etc. "\\<a\\>"
                _v_ks_0 = re.findall(re.compile(cls.PATTERN_KEYWORD_ESCAPE, re.S), _value_unfold)
                if _v_ks_0:
                    for _i_v_k_0 in _v_ks_0:
                        keys_exclude.append(_i_v_k_0)
                        _value_unfold = _value_unfold.replace('\\<', '<').replace('\\>', '>')
                # etc. "<a>"
                else:
                    _v_ks_1 = re.findall(re.compile(cls.PATTERN_KEYWORD, re.S), _value_unfold)
                    # break when "\n" in key
                    for _i in _v_ks_1:
                        if '\n' in _i:
                            return value_
                    if _v_ks_1:
                        for _i_v_k_1 in set(_v_ks_1):
                            # etc. <a | b>, value=a or b
                            if '|' in _i_v_k_1:
                                _i_v_ks_2 = map(lambda x: x.strip(), _i_v_k_1.split('|'))
                                for _j_v_k_2 in _i_v_ks_2:
                                    if _j_v_k_2 not in keys_all:
                                        raise KeyError('key="{}" is non-exists'.format(_j_v_k_2))
                                    _j_v = get_fnc(_j_v_k_2)
                                    if _j_v is not None:
                                        _value_unfold = _j_v
                                        break
                            # etc. <a % str(x).lower()>, value=str(a).lower()
                            elif '%' in _i_v_k_1:
                                _i_v_ks_2 = map(lambda x: x.strip(), _i_v_k_1.split('%'))
                                _i_v_k_2 = _i_v_ks_2[0]
                                if fnmatch.filter([_i_v_k_2], '*.key'):
                                    _i_v_2 = cls.get_absolute_key_name(_i_v_k_2, key_)
                                elif fnmatch.filter([_i_v_k_2], '*.key_index'):
                                    _i_v_2 = cls.get_absolute_key_index(_i_v_k_2, key_, keys_all)
                                elif fnmatch.filter([_i_v_k_2], '.*'):
                                    _i_v_k_2_ = cls.get_absolute_key(_i_v_k_2, key_)
                                    if _i_v_k_2_ in keys_exclude:
                                        continue
                                    #
                                    if _i_v_k_2_ not in keys_all:
                                        raise KeyError('key="{}" is non-exists'.format(_i_v_k_2_))
                                    #
                                    _i_v_2 = get_fnc(_i_v_k_2_)
                                else:
                                    if _i_v_k_2 not in keys_all:
                                        raise KeyError('key="{}" is non-exists'.format(_i_v_k_2))
                                    _i_v_2 = get_fnc(_i_v_k_2)
                                _i_v_2_fnc = eval('lambda x: {}'.format(_i_v_ks_2[1]))
                                _value_unfold = _value_unfold.replace('<{}>'.format(_i_v_k_1), _i_v_2_fnc(_i_v_2))
                            # etc. <a>, value=a
                            else:
                                # catch value
                                # etc. <a.key>
                                if fnmatch.filter([_i_v_k_1], '*.key'):
                                    _i_v_1 = cls.get_absolute_key_name(_i_v_k_1, key_)
                                elif fnmatch.filter([_i_v_k_1], '*.key_index'):
                                    _i_v_1 = cls.get_absolute_key_index(_i_v_k_1, key_, keys_all)
                                # etc. <.a>
                                elif fnmatch.filter([_i_v_k_1], '.*'):
                                    _i_v_k_1_ = cls.get_absolute_key(_i_v_k_1, key_)
                                    #
                                    if _i_v_k_1_ in keys_exclude:
                                        continue
                                    #
                                    if _i_v_k_1_ not in keys_all:
                                        raise KeyError('key="{}" is non-exists'.format(_i_v_k_1_))

                                    _i_v_1 = get_fnc(_i_v_k_1_)
                                    #
                                    _i_v_1 = rcs_fnc_(_i_v_k_1_, _i_v_1)
                                else:
                                    #
                                    if _i_v_k_1 in keys_exclude:
                                        continue
                                    if _i_v_k_1 not in keys_all:
                                        raise KeyError('key="{}" is non-exists'.format(_i_v_k_1))
                                    _i_v_1 = get_fnc(_i_v_k_1)
                                    #
                                    _i_v_1 = rcs_fnc_(_i_v_k_1, _i_v_1)
                                #
                                if isinstance(_i_v_1, six.string_types):
                                    _value_unfold = _value_unfold.replace('<{}>'.format(_i_v_k_1), _i_v_1)
                                elif isinstance(_i_v_1, (int, float, bool)):
                                    _value_unfold = _value_unfold.replace('<{}>'.format(_i_v_k_1), str(_i_v_1))
                    else:
                        _v_ks_0 = re.findall(re.compile(cls.PATTERN_KEYWORD_ESCAPE, re.S), _value_unfold)
                # etc: "=0+1"
                if fnmatch.filter([_value_unfold], '=*'):
                    cmd = _value_unfold[1:]
                    _value_unfold = eval(cmd)
                return _value_unfold
            elif isinstance(value_, (tuple, list)):
                return [rcs_fnc_(key_, _i) for _i in value_]
            return value_

        value = get_fnc(key)
        return rcs_fnc_(key, value)

    @classmethod
    def filter(cls, texts, p):
        list_ = []
        try:
            re_pat = cls.FILTER_CACHE[p]
        except KeyError:
            res = fnmatch.translate(p)
            if len(cls.FILTER_CACHE) >= cls.FILTER_CACHE_MAXIMUM:
                cls.FILTER_CACHE.clear()
            cls.FILTER_CACHE[p] = re_pat = re.compile(res, re.IGNORECASE)

        match = re_pat.match
        for i_text in texts:
            if match(i_text):
                list_.append(i_text)
        return list_


class ContentYamlBase(object):
    @classmethod
    def dump(cls, raw, stream=None, **kwargs):
        class _Cls(yaml.SafeDumper):
            pass

        # noinspection PyUnresolvedReferences
        def _fnc(dumper_, data_):
            return dumper_.represent_mapping(
                yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                data_.items(),
            )

        _Cls.add_representer(collections.OrderedDict, _fnc)
        return yaml.dump(raw, stream, _Cls, **kwargs)

    @classmethod
    def load(cls, stream):
        class _Cls(yaml.SafeLoader):
            pass

        # noinspection PyArgumentList
        def _fnc(loader_, node_):
            loader_.flatten_mapping(node_)
            return collections.OrderedDict(loader_.construct_pairs(node_))

        # noinspection PyUnresolvedReferences
        _Cls.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _fnc)
        return yaml.load(stream, _Cls)


class ContentYamlFile(object):
    def __init__(self, file_path):
        self.__file_path = file_path

    def write(self, raw):
        with open(self.__file_path, 'w') as y:
            ContentYamlBase.dump(
                raw,
                y,
                indent=4,
                default_flow_style=False,
            )

    def read(self):
        with open(self.__file_path) as y:
            raw = ContentYamlBase.load(y)
            y.close()
            return raw


class ContentFile(object):
    def __init__(self, file_path):
        self.__file_path = file_path

    def read(self):
        path = self.__file_path
        ext = os.path.splitext(path)[-1]
        if os.path.isfile(path):
            if ext in {'.json'}:
                with open(path) as j:
                    raw = json.load(j, object_pairs_hook=collections.OrderedDict)
                    j.close()
                    return raw
            elif ext in {'.yml'}:
                with open(path) as y:
                    raw = ContentYamlBase.load(y)
                    y.close()
                    return raw
            else:
                with open(path) as f:
                    raw = f.read()
                    f.close()
                    return raw

    def write(self, raw):
        path = self.__file_path
        ext = os.path.splitext(path)[-1]
        directory = os.path.dirname(path)
        if os.path.isdir(directory) is False:
            # noinspection PyBroadException
            try:
                os.makedirs(directory)
            except Exception:
                return

        if ext in {'.json'}:
            with open(path, 'w') as j:
                json.dump(
                    raw,
                    j,
                    indent=4
                )
        elif ext in {'.yml'}:
            with open(path, 'w') as y:
                ContentYamlBase.dump(
                    raw,
                    y,
                    indent=4,
                    default_flow_style=False,
                )
        else:
            with open(path, 'w') as f:
                if isinstance(raw, six.text_type):
                    raw = raw.encode('utf-8')
                f.write(raw)


class ContentVariant(object):
    class OptTypes(object):
        Set = 'set'
        Append = 'append'
        Prepend = 'prepend'
        Remove = 'remove'

    PATHSEP = os.pathsep

    OPT_STACK = []
    OPT_CACHE = dict()

    class _Value(str):
        def __init__(self, value):
            super(ContentVariant._Value, self).__init__(value)
            self._key = ''
            self._value = value
            self._environ = None

        # env.TEST += 'test'
        def __iadd__(self, value):
            if isinstance(value, (set, tuple, list)):
                [self._append_fnc(i) for i in list(value)]
            else:
                self._append_fnc(value)
            return self

        # env.TEST -= 'test'
        def __isub__(self, value):
            if isinstance(value, (set, tuple, list)):
                [self._remove_fnc(i) for i in list(value)]
            else:
                self._remove_fnc(value)
            return self

        # env.TEST == 'test'
        def __eq__(self, other):
            return self._eq_fnc(other)

        def _get_args(self):
            return (
                [i.lstrip().rstrip() for i in self._value.split(ContentVariant.PATHSEP)],
                [i.lstrip().rstrip() for i in self._value.lower().split(ContentVariant.PATHSEP)]
            )

        def _get_fnc(self):
            return self._environ._opt_cache_get_fnc(self._key)

        def _set_fnc(self, value):
            if value != self._value:
                self._value = value
                self._update_opt_stack_fnc(
                    self._key, value, ContentVariant.OptTypes.Set
                )

        def _append_fnc(self, value):
            if self._value:
                list_origin, list_lower = self._get_args()
                if value.lower() not in list_lower:
                    list_origin.append(value)
                    self._value = ContentVariant.PATHSEP.join(list_origin)
                    self._update_opt_stack_fnc(
                        self._key, value, ContentVariant.OptTypes.Append
                    )
            else:
                self._set_fnc(value)

        def _prepend_fnc(self, value):
            if self._value:
                list_origin, list_lower = self._get_args()
                if value.lower() not in list_lower:
                    list_origin.insert(0, value)
                    self._value = ContentVariant.PATHSEP.join(list_origin)
                    self._update_opt_stack_fnc(
                        self._key, value, ContentVariant.OptTypes.Prepend
                    )

        def _remove_fnc(self, value):
            if self._value:
                list_origin, list_lower = self._get_args()
                if value.lower() in list_lower:
                    list_origin.remove(list_origin[list_lower.index(value.lower())])
                    self._value = ContentVariant.PATHSEP.join(list_origin)
                    self._update_opt_stack_fnc(
                        self._key, value, ContentVariant.OptTypes.Remove
                    )
                    return True
            return False

        def _update_opt_stack_fnc(self, key, value, opt_type):
            self._environ._update_opt_stack_fnc(key, value, opt_type, {self._key: self._value})

        def _eq_fnc(self, value):
            return self._value == str(value)

        @property
        def parent(self):
            return self._environ

        @parent.setter
        def parent(self, parent):
            self._environ = parent

        @property
        def key(self):
            return self._key

        @key.setter
        def key(self, key):
            self._key = key

        def get(self):
            return self._get_fnc()

        def set(self, value):
            self._set_fnc(value)

        def append(self, value):
            return self._append_fnc(value)

        def prepend(self, value):
            return self._prepend_fnc(value)

        def remove(self, value):
            return self._remove_fnc(value)

        def __str__(self):
            return self._value

        def __repr__(self):
            return self.__str__()

    def __init__(self, cache=None):
        self._environ_opt_stack = ContentVariant.OPT_STACK
        self._environ_opt_cache = ContentVariant.OPT_CACHE
        if isinstance(cache, dict):
            for k, v in cache.items():
                self._set_fnc(k, v)

    @staticmethod
    def restore_cache():
        ContentVariant.OPT_STACK = []
        ContentVariant.OPT_CACHE = dict()

    def accept(self):
        pass

    # env.TEST
    def __getattr__(self, key):
        if key in ['_environ_opt_stack', '_environ_opt_cache', '_environ_variants']:
            return self.__dict__[key]
        else:
            return self._get_fnc(key)

    # env.TEST = 'test'
    def __setattr__(self, key, value):
        if key in {'_environ_opt_stack', '_environ_opt_cache', '_environ_variants'}:
            self.__dict__[key] = value
        else:
            self._set_fnc(key, value)

    def _update_opt_stack_fnc(self, key, value, opt_type, data):
        self._environ_opt_stack.append(
            (key, value, opt_type, data)
        )

    def _opt_cache_has_key_fnc(self, key):
        return key in self._environ_opt_cache

    def _opt_cache_get_fnc(self, key):
        return self._environ_opt_cache[key]

    def _opt_cache_get_all_fnc(self):
        return self._environ_opt_cache

    def _get_fnc(self, key):
        key = key.upper()
        if key in self._environ_opt_cache:
            return self._environ_opt_cache[key]
        environ_value = ContentVariant._Value('')
        environ_value.key = key
        environ_value.parent = self
        self._environ_opt_cache[key] = environ_value
        return environ_value

    def _set_fnc(self, key, value):
        key = key.upper()
        if key not in self._environ_opt_cache:
            environ_value = ContentVariant._Value('')
            environ_value.key = key
            environ_value.parent = self
            environ_value.set(value)
            self._environ_opt_cache[key] = environ_value

    def has_key(self, key):
        return self._opt_cache_has_key_fnc(key)

    def has_value(self, key, value):
        value_ = self._opt_cache_get_fnc(key)
        if value_ is not None:
            _ = [i.lstrip().rstrip() for i in value_.lower().split(ContentVariant.PATHSEP)]
            return value.lower() in _
        return False

    def __str__(self):
        list_ = []
        for k, v in self._opt_cache_get_all_fnc().items():
            list_.append('{}={}'.format(k, v))
        list_.sort()
        return '\r\n'.join(list_)

    def __repr__(self):
        return self.__str__()


class ContentEnvironment(ContentVariant):
    OPT_STACK = []

    OPT_CACHE = dict()

    def __init__(self):
        super(ContentEnvironment, self).__init__(
            {str(k): str(v) for k, v in dict(os.environ).items()}
        )

    def accept(self):
        pass


if __name__ == '__main__':
    env = ContentVariant()

    print 'set "a" to PATH'
    env.PATH = 'a'
    print 'append a to PATH'
    env.PATH += 'b'
    print 'set "A" to TEST'
    env.TEST = 'A'
    print 'append "a" to TEST'
    env.TEST += 'B'
    print 'remove "B" to TEST'
    env.TEST -= 'B'

    print env.PATH

    print env.OPT_STACK
    print env.OPT_CACHE
    print env
