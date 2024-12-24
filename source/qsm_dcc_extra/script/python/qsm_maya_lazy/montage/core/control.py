# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

import qsm_maya.motion.core as qsm_mya_mtn_core

import qsm_maya.adv as qsm_mya_adv

from . import base as _base


class AbsControlSet(_base.MotionBase):
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


class AdvControlSet(AbsControlSet):

    @classmethod
    def generate(cls, namespace):
        return cls(
            qsm_mya_adv.AdvOpt(namespace).find_all_controls()
        )

    def __init__(self, *args, **kwargs):
        super(AdvControlSet, self).__init__(*args, **kwargs)

    def get_frame_range(self):
        curve_nodes = []
        for i in self._paths:
            i_curve_nodes = qsm_mya_mtn_core.ControlMotionOpt(i).get_all_curve_nodes()
            curve_nodes.extend(i_curve_nodes)

        if curve_nodes:
            return qsm_mya_core.AnimCurveNodes.get_range(curve_nodes)
        return qsm_mya_core.Frame.get_frame_range()

    def generate_motion_dict(self):
        return qsm_mya_mtn_core.ControlSetMotionOpt(
            self._namespace, self._paths
        ).generate_motion_dict()

    def export_motion_to(self, file_path):
        bsc_storage.StgFileOpt(file_path).set_write(
            self.generate_motion_dict()
        )

    def bake_all_keyframes(self, start_frame, end_frame, attributes=None):
        # do not mark undo here
        qsm_mya_mtn_core.ControlSetBake(self._paths).execute(
            start_frame, end_frame,
            attributes=attributes
        )


class AdvChrControlSet(AdvControlSet):
    @classmethod
    def generate(cls, namespace):
        return cls(
            qsm_mya_adv.AdvChrOpt(namespace).find_all_controls()
        )

    def __init__(self, *args, **kwargs):
        super(AdvChrControlSet, self).__init__(*args, **kwargs)
