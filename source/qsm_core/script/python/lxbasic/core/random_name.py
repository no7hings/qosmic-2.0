# coding:utf-8
import six

import os as _os

import threading as _threading

from random import Random as _Random

_allocate_lock = _threading.Lock


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
