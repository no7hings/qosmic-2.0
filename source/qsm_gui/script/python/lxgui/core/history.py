# coding:utf-8
import copy

import six

import lxbasic.content as bsc_content

from . import base as _base


class GuiHistoryStage(object):
    MAXIMUM = 20

    INSTANCE_DICT = dict()

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        k = kwargs.get('key', 'default')

        if k in cls.INSTANCE_DICT:
            return cls.INSTANCE_DICT[k]

        self = super(GuiHistoryStage, cls).__new__(cls)

        self._k = k
        self._cc_dict = dict()
        self._cc = bsc_content.ContentCache(_base.GuiUtil.get_user_history_file(k))
        cls.INSTANCE_DICT[k] = self
        return self

    def __str__(self):
        return 'GuiHistory({})'.format(self._k)

    def _generate_c(self, k):
        if k == self._k:
            return self._cc.generate()
        else:
            if k in self._cc_dict:
                return self._cc_dict[k].generate()
            else:
                cc = bsc_content.ContentCache(_base.GuiUtil.get_user_history_file(k))
                self._cc_dict[k] = cc
                return cc.generate()

    def _to_key_args(self, key):
        if isinstance(key, six.string_types):
            return self._k, key
        elif isinstance(key, (tuple, list)):
            return '{}.{}'.format(self._k, '.'.join(key[:-1])), key[-1]
        raise RuntimeError()

    def get_one(self, key):
        k, key = self._to_key_args(key)
        c = self._generate_c(k)
        return c.get(key)

    def set_one(self, key, value):
        k, key = self._to_key_args(key)
        c = self._generate_c(k)
        c.set(key, value)
        c.save()

    def set_array(self, key, array):
        k, key = self._to_key_args(key)
        c = self._generate_c(k)
        c.set(key, array)
        c.save()

    def get_array(self, key):
        k, key = self._to_key_args(key)
        c = self._generate_c(k)
        return c.get(key) or []

    def append(self, key, value):
        k, key = self._to_key_args(key)
        c = self._generate_c(k)
        v_old = c.get(key) or []
        # move end
        if value in v_old:
            v_old.remove(value)
        v_old.append(value)

        v_old = v_old[-self.MAXIMUM:]
        c.set(key, v_old)
        c.save()
        return True

    def extend(self, key, values):
        k, key = self._to_key_args(key)
        c = self._generate_c(k)
        v_old = c.get(key) or []
        for i_v in values:
            if i_v in v_old:
                v_old.remove(i_v)
            v_old.append(i_v)

        v_old = v_old[-self.MAXIMUM:]
        c.set(key, v_old)
        c.save()
        return True

    def get_all(self, key):
        k, key = self._to_key_args(key)
        c = self._generate_c(k)
        return copy.copy(c.get(key)) or []

    def get_latest(self, key):
        k, key = self._to_key_args(key)
        c = self._generate_c(k)
        _ = c.get(key)
        if _:
            return _[-1]
