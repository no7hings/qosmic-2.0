# coding:utf-8
import sys

from .wrap import *

from . import _root

__all__ = [
    'Stage',
]


class Stage(object):
    INSTANCE = None

    SWAP_FLAG = 'CGT'

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.INSTANCE is not None:
            return cls.INSTANCE

        self = super(Stage, cls).__new__(cls)
        if CGT_FLAG is True:
            # noinspection PyUnresolvedReferences
            self._api = cgtw2.tw()
        else:
            raise RuntimeError()

        self._root_dict = dict()

        cls.INSTANCE = self

        sys.stdout.write('resolve entity from {}.\n'.format(self.SWAP_FLAG))
        return self

    def root(self, location='X:'):
        if location in self._root_dict:
            return self._root_dict[location]

        instance = _root.Root(self, location)
        self._root_dict[location] = instance
        return instance
