# coding:utf-8
import abc as _abc

import sys as _sys

import six as _six

import platform as _platform

import getpass as _getpass

import collections as _collections

import threading as _threading

import re as _re

import os as _os

import fnmatch as _fnmatch

import time as _time

ENVIRON_MARK = None


class LRUCache:
    """
    Least Recently Used (LRU) cache
    """
    def __init__(self, maximum=64):
        self._dict = _collections.OrderedDict()
        # make thread safe
        self._lock = _threading.Lock()
        self._maximum = maximum

    def __contains__(self, key):
        with self._lock:
            return key in self._dict

    def __str__(self):
        with self._lock:
            return "{}({})".format(
                self.__class__.__name__, self._dict.items()
            )

    def __repr__(self):
        return '\n'+self.__str__()

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def get(self, key):
        with self._lock:
            if key in self._dict:
                # move to last
                value = self._dict.pop(key)
                self._dict[key] = value
                return value
            return None

    def set(self, key, value):
        with self._lock:
            if key in self._dict:
                # move to last
                self._dict.pop(key)
            # remove first
            elif len(self._dict) >= self._maximum:
                self._dict.popitem(last=False)
            self._dict[key] = value

    def pop(self, key):
        with self._lock:
            self._dict.pop(key)


class Fnmatch(object):
    FILTER_CACHE = LRUCache(1024)
    FILTER_CACHE_MAXIMUM = 1000

    MAGIC_CHECK = _re.compile('[*?[]')

    @classmethod
    def filter(cls, texts, p):
        list_ = []
        try:
            re_pat = cls.FILTER_CACHE[p]
        except KeyError:
            res = _fnmatch.translate(p)
            cls.FILTER_CACHE[p] = re_pat = _re.compile(res, _re.IGNORECASE)

        match = re_pat.match
        for i_text in texts:
            if match(i_text):
                list_.append(i_text)
        return list_

    @classmethod
    def is_match(cls, text, p):
        try:
            re_pat = cls.FILTER_CACHE[p]
        except KeyError:
            res = _fnmatch.translate(p)
            cls.FILTER_CACHE[p] = re_pat = _re.compile(res, _re.IGNORECASE)

        match = re_pat.match
        return match(text)


def ensure_string(s):
    # make any type(byte/unicode) to str type
    if isinstance(s, _six.text_type):
        if _six.PY2:
            return s.encode('utf-8')
    elif isinstance(s, _six.binary_type):
        if _six.PY3:
            return s.decode('utf-8')
    return s


def ensure_unicode(s):
    # make any type(byte/str) to unicode type
    if isinstance(s, _six.text_type):
        return s
    elif isinstance(s, _six.binary_type):
        return s.decode('utf-8')
    return s


def ensure_mbcs(s):
    # encode to 'mbcs' for command line execute
    if isinstance(s, _six.text_type):
        if _six.PY2:
            return s.encode('mbcs')
    return s


def is_linux():
    return _platform.system() == 'Linux'


def is_windows():
    return _platform.system() == 'Windows'


def get_user_name():
    return _getpass.getuser()


# when we are in one dcc, use subprocess open another dcc, we must use a clear environment
def get_env_mark():
    global ENVIRON_MARK

    if ENVIRON_MARK is not None:
        return ENVIRON_MARK

    dict_ = {}

    # the env mark from other tool, etc. desktop-kit, workspace
    _ = '{}/qosmic.env_mark.txt'.format(_os.environ['TEMP'])
    if _os.path.isfile(_):
        with open(_, 'r') as f:
            for i in f:
                i = i.strip()
                if '=' in i:
                    k, v = i.split('=', 1)
                    dict_[k] = v

        ENVIRON_MARK = dict_
        return dict_

    # when env mark is not found, use current
    return dict(_os.environ)


class AbsStack(object):
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

    # must override this method
    @_abc.abstractmethod
    def get_key(self, obj):
        """
        :param obj: instance(<obj>)
        :return: str(<obj-key>)
        """
        pass

    def get_index(self, key):
        """
        :param key: str(<obj-key>)
        :return: int(<obj-index>)
        """
        return self._key_dict[key]

    def get_one(self, key):
        """
        :param key: str(<obj-key>)
        :return: instance(<obj>)
        """
        if key in self._key_dict:
            index = self._key_dict[key]
            return self._obj_list[index]

    def get_one_at(self, index):
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
            _ = Fnmatch.filter(self._key_dict.keys(), regex)
            _.sort(key=self._key_list.index)
            return _
        return self._key_list

    def get_many(self, regex=None):
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

    def get_all(self):
        return self._obj_list

    def exists_one(self, key):
        """
        :param key: str(<obj-key>)
        :return: bool
        """
        return key in self._key_dict

    def exists_many(self, regex=None):
        """
        :param regex: str(<fnmatch-pattern>)
        :return: bool
        """
        if regex:
            keys = self.get_keys(regex)
            return keys != []
        return self._count > 0

    def add_one(self, obj):
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

    def remove_one(self, obj):
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

    def override_one(self, old_obj, new_obj):
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

    def get_count(self):
        """
        :return: int
        """
        return self._count

    def get_maximum(self):
        if self._count > 0:
            return self._count-1
        return 0

    def get_indices(self):
        """
        :return: list[int(<obj-index>), ...]
        """
        return range(self._count)

    def __getitem__(self, index):
        """
        :param index: int(<obj-index>)
        :return: instance(<obj>)
        """
        return self.get_one_at(index)

    def __contains__(self, key):
        """
        :param key: str(<obj-key>)
        :return: bool
        """
        return self.exists_one(key)


class Debug:
    @staticmethod
    def run(name):
        def decorator(fnc):
            def wrapper(*args, **kwargs):
                st = _time.time()
                result = fnc(*args, **kwargs)
                et = _time.time()
                _sys.stdout.write('run "{name}", cost: {second}.s\n'.format(
                    name=name, second=round(et-st, 3))
                )
                return result
            return wrapper
        return decorator

    @staticmethod
    def get_error_stack():
        import sys

        import traceback

        exc_texts = []
        exc_type, exc_value, exc_stack = sys.exc_info()
        if exc_type:
            value = repr(exc_value)
            for i_stk in traceback.extract_tb(exc_stack):
                i_file_path, i_line, i_fnc, i_fnc_line = i_stk
                exc_texts.append(
                    '    file "{}" line {} in {}\n        {}'.format(
                        i_file_path.replace('\\', '/'),
                        i_line,
                        i_fnc,
                        i_fnc_line
                    )
                )

            # convert chinese word to right view
            value = ensure_string(value.decode('unicode_escape', 'ignore'))

            text = '\n'.join(['*'*80]+['traceback:']+exc_texts+[value]+['*'*80])
            return text

    @staticmethod
    def trace():
        text = Debug.get_error_stack()
        if text:
            _sys.stderr.write(text+'\n')
