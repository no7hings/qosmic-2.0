# coding:utf-8
import lxbasic.log as bsc_log

from .. core import base as _cor_base

from . import _root


class Stage(object):
    INSTANCE = None

    SWAP_FLAG = 'SCAN'

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.INSTANCE is not None:
            return cls.INSTANCE

        self = super(Stage, cls).__new__(cls)
        self._root_dict = dict()
        cls.INSTANCE = self

        bsc_log.Log.trace_result('resolve entity from {}.'.format(self.SWAP_FLAG))
        return self

    @property
    def address(self):
        return None

    @property
    def host(self):
        return None

    @property
    def api(self):
        return None

    def root(self, location='X:'):
        if location in self._root_dict:
            return self._root_dict[location]

        instance = _root.Root(self, location)
        self._root_dict[location] = instance
        return instance
    
    @staticmethod
    def set_sync_cache_flag(boolean):
        _cor_base.GlobalVar.SYNC_CACHE_FLAG = boolean

