# coding:utf-8
import _base

import _root


class Stage(object):
    INSTANCE = None

    def __new__(cls, *args, **kwargs):
        if cls.INSTANCE is not None:
            return cls.INSTANCE

        self = super(Stage, cls).__new__(cls)
        self._root_dict = dict()
        cls.INSTANCE = self
        return self

    def get_root(self, location='X:'):
        if location in self._root_dict:
            return self._root_dict[location]

        root_instance = _root.Root()
        self._root_dict[location] = root_instance
        return root_instance
    
    @staticmethod
    def set_sync_cache_flag(boolean):
        _base.GlobalVar.SYNC_CACHE_FLAG = boolean
