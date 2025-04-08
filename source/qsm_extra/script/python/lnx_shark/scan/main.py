# coding:utf-8
# do not remove it
# noinspection PyUnresolvedReferences
from ._base import *

from . import _base

from . import _root


class Stage(object):
    INSTANCE = None

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.INSTANCE is not None:
            return cls.INSTANCE

        self = super(Stage, cls).__new__(cls)
        self._root_dict = dict()
        cls.INSTANCE = self
        return self

    def root(self, location='X:'):
        if location in self._root_dict:
            return self._root_dict[location]

        instance = _root.Root(location)
        self._root_dict[location] = instance
        return instance
    
    @staticmethod
    def set_sync_cache_flag(boolean):
        _base.GlobalVar.SYNC_CACHE_FLAG = boolean

