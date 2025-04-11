# coding:utf-8
import six as _six

import platform as _platform

import getpass as _getpass

import collections as _collections

import re as _re

import fnmatch as _fnmatch


class LRUCache:
    def __init__(self, maximum=64):
        self._dict = _collections.OrderedDict()
        self._maximum = maximum

    def __contains__(self, key):
        return key in self._dict

    def __str__(self):
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
        if key in self._dict:
            # move to last
            value = self._dict.pop(key)
            self._dict[key] = value
            return value
        return None

    def set(self, key, value):
        if key in self._dict:
            # move to last
            self._dict.pop(key)
        # remove first
        elif len(self._dict) >= self._maximum:
            self._dict.popitem(last=False)
        self._dict[key] = value

    def pop(self, key):
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
    else:
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
