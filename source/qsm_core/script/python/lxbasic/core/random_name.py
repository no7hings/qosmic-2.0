# coding:utf-8
import six

import os as _os

from random import Random as _Random

if six.PY2:
    # python 2
    import dummy_thread as _thread
else:
    # python 3
    # noinspection PyUnresolvedReferences
    import _dummy_thread as _thread

_allocate_lock = _thread.allocate_lock


class BscRandomName:
    CHATS = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789_"
    )

    def __init__(self):
        self.mutex = _allocate_lock()
        self.normcase = _os.path.normcase

    @property
    def rng(self):
        cur_pid = _os.getpid()
        if cur_pid != getattr(self, '_rng_pid', None):
            self._rng = _Random()
            self._rng_pid = cur_pid
        return self._rng

    def __iter__(self):
        return self

    def next(self):
        m = self.mutex
        c = self.CHATS
        choose = self.rng.choice

        m.acquire()
        try:
            letters = [choose(c) for _ in "123456"]
        finally:
            m.release()

        return self.normcase(''.join(letters))
