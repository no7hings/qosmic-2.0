# coding:utf-8
import os
import sys

# noinspection PyUnresolvedReferences
from xml.etree import ElementTree as etree

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage


class DotfileCache:
    @staticmethod
    def get(scheme='default'):
        def decorator(fnc):
            def wrapper(self, *args, **kwargs):
                key = fnc.__name__
                if key in self._cache_dict:
                    return self._cache_dict[key]
                result = fnc(self, *args, **kwargs)
                self._cache_dict[key] = result
                return result
            return wrapper
        return decorator


class AbsDotfile(object):
    INSTANCE_DICT = bsc_core.LRUCache(maximum=64)

    SEP = '\n'

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if args:
            file_path = args[0]
        else:
            file_path = kwargs['file_path']

        file_path = bsc_core.ensure_unicode(file_path)
        if os.path.isfile(file_path) is False:
            raise RuntimeError()

        key = bsc_core.BscUuid.generate_by_file(file_path)
        # when is large file, cost lost time.
        # key = bsc_storage.StgFileOpt(file_path).to_hash_uuid()
        if key in cls.INSTANCE_DICT:
            return cls.INSTANCE_DICT[key]

        self = super(AbsDotfile, cls).__new__(cls)
        self._file_path = file_path

        self._load_lines()
        
        self._cache_dict = {}

        sys.stdout.write(u'load file: {}\n'.format(file_path))

        cls.INSTANCE_DICT[key] = self
        return self

    def _load_lines(self):
        self._lines = []
        if self._file_path is not None:
            with open(self._file_path) as f:
                data = f.read()
                sep = self.SEP
                self._lines = list(map(lambda x: r'{}{}'.format(x.rstrip(), sep), data.split(sep)))


class AbsDotXml(object):
    INSTANCE_DICT = bsc_core.LRUCache(maximum=64)

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if args:
            file_path = args[0]
        else:
            file_path = kwargs['file_path']

        file_path = bsc_core.ensure_unicode(file_path)
        if os.path.isfile(file_path) is False:
            raise RuntimeError()

        key = bsc_storage.StgFileOpt(file_path).to_hash_uuid()
        if key in cls.INSTANCE_DICT:
            return cls.INSTANCE_DICT[key]

        self = super(AbsDotXml, cls).__new__(cls)
        self._file_path = file_path

        self._etree = etree.parse(self._file_path)

        self._cache_dict = {}

        cls.INSTANCE_DICT[key] = self
        return self
