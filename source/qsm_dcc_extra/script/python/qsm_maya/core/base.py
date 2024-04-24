# coding:utf-8
import lxbasic.core as bsc_core


class AbsNodeOpt(object):
    Type = None

    def __init__(self, path):
        self._path = path
        self._path_opt = bsc_core.PthNodeOpt(self._path)
        self._name = self._path_opt.get_name()

    def __str__(self):
        return '{}(path="{}")'.format(
            self.Type, self._path,
        )

    def __repr__(self):
        return self.__str__()

    @property
    def type(self):
        return self.Type

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._path_opt.get_name()

    @property
    def path_opt(self):
        return self._path_opt
