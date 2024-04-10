# coding:utf-8
import copy

import lxbasic.core as bsc_core


class AbsDccExporter(object):
    OPTION = dict()

    def __init__(self, file_path, root=None, option=None):
        #
        self._file_path = file_path
        #
        self._root = root
        if root is not None:
            self._root_dat_opt = bsc_core.PthNodeOpt(root)
        else:
            self._root_dat_opt = None
        #
        self._option = copy.copy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                if k in self.OPTION:
                    self._option[k] = v
        #
        self._results = []

    def set_run(self):
        raise NotImplementedError()

    def get_results(self):
        return self._results


class AbsFncOptionBase(object):
    OPTION = dict()

    def __init__(self, option=None):
        self._option = copy.copy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                self._option[k] = v

    def get_option(self):
        return self._option

    option = property(get_option)

    def get(self, key):
        return self._option.get(key)
