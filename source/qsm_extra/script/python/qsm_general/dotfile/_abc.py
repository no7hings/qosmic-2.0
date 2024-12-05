# coding:utf-8
import collections

import re

import os

import lxbasic.core as bsc_core


class AbsDotfile(object):
    SEP = '\n'

    def __init__(self, file_path):
        self._file_path = bsc_core.ensure_unicode(file_path)

        if os.path.isfile(self._file_path) is False:
            raise RuntimeError()

        self._load_lines()

    def _load_lines(self):
        self._lines = []
        if self._file_path is not None:
            with open(self._file_path) as f:
                data = f.read()
                sep = self.SEP
                self._lines = map(lambda x: r'{}{}'.format(x.rstrip(), sep), data.split(sep))
