# coding:utf-8
import functools

import collections

from ... import core as _gui_core
# qt
from ...qt.core.wrap import *


class _Data(object):
    def __init__(self, **kwargs):
        self._dict = dict(**kwargs)

    def __getattr__(self, key):
        return self._dict[key]

    def __setattr__(self, key, value):
        if key in {'_dict'}:
            self.__dict__[key] = value
        else:
            self._dict[key] = value

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __str__(self):
        return str(self._dict)

    def __repr__(self):
        return '\n'+self.__str__()

    def get(self, *args, **kwargs):
        return self._dict.get(*args, **kwargs)


class AbsView(object):
    item_check_changed = qt_signal()
    item_select_changed = qt_signal()

    press_released = qt_signal()
    info_text_accepted = qt_signal(str)

