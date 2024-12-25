# coding:utf-8
import qsm_maya.core as qsm_mya_core

from ..base import abc as _bsc_abc


class AbsControlSet(_bsc_abc.AbsMontage):
    def __init__(self, paths):
        self._paths = paths
        self._namespace = qsm_mya_core.DagNode.to_namespace(self._paths[0])

        self._cache_dict = {}
        self._cache_all()

    def _cache_all(self):
        self._cache_dict.clear()

        for i_path in self._paths:
            i_control_key = qsm_mya_core.DagNode.to_name_without_namespace(i_path)
            self._cache_dict[i_control_key] = i_path

    def get(self, control_key):
        return self._cache_dict.get(control_key)

    def get_all(self):
        return self._cache_dict.values()