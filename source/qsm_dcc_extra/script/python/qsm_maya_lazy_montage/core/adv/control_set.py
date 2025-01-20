# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

import qsm_maya.motion.core as qsm_mya_mtn_core

import qsm_maya.adv as qsm_mya_adv

from ..base import control_set as _bsc_control_set


class AdvControlSet(_bsc_control_set.AbsControlSet):

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
            return qsm_mya_core.AnmCurveNodes.get_range(curve_nodes)
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
