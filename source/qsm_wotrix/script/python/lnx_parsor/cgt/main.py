# coding:utf-8
import sys

import lxbasic.log as bsc_log

from .wrap import *

from . import _root


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
            # noinspection PyUnresolvedReferences
            self._address = cgtw2.G_tw_http_ip
            self._host = self._address.split(':')[0]
        else:
            raise RuntimeError()

        self._root_dict = dict()

        cls.INSTANCE = self

        bsc_log.Log.trace_result('resolve entity from {}.'.format(self.SWAP_FLAG))
        return self

    @property
    def address(self):
        return self._address

    @property
    def host(self):
        return self._host

    @property
    def api(self):
        return self._api

    def root(self, location='X:'):
        if location in self._root_dict:
            return self._root_dict[location]

        instance = _root.Root(self, location)
        self._root_dict[location] = instance
        return instance
