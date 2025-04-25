# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

import qsm_maya.motion as qsm_mya_motion

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
            i_curve_nodes = qsm_mya_motion.ControlMotionOpt(i).get_all_curve_nodes()
            curve_nodes.extend(i_curve_nodes)

        if curve_nodes:
            return qsm_mya_core.AnmCurveNodes.get_range(curve_nodes)
        return qsm_mya_core.Frame.get_frame_range()

    def generate_motion_dict(self):
        return qsm_mya_motion.ControlSetMotionOpt(
            self._namespace, self._paths
        ).generate_motion_dict()

    def export_motion_to(self, file_path):
        bsc_storage.StgFileOpt(file_path).set_write(
            self.generate_motion_dict()
        )

    def bake_all_keyframes(self, start_frame, end_frame, attributes=None):
        # do not mark undo here
        qsm_mya_motion.ControlSetBake(self._paths).execute(
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

    def zero_out(self):
        # make sure auto keyframe is disable
        with qsm_mya_core.auto_keyframe_context(False):
            data = {}
            atr_names = [
                'translateX', 'translateY', 'translateZ',
                'rotateX', 'rotateY', 'rotateZ'
            ]

            for i_path in self._paths:
                i_attrs = {}
                data[i_path] = i_attrs
                for j_atr_name in atr_names:
                    j_atr = '{}.{}'.format(i_path, j_atr_name)

                    # ignore non exists
                    if cmds.objExists(j_atr) is False:
                        continue

                    # ignore non settable
                    if qsm_mya_core.NodeAttribute.is_settable(i_path, j_atr_name) is False:
                        continue

                    j_value = round(cmds.getAttr(j_atr), 4)
                    i_attrs[j_atr_name] = j_value
                    if j_value != 0:
                        cmds.setAttr(j_atr, 0)
            return data

    @classmethod
    def apply_data(cls, data):
        for i_path, v in data.items():
            for j_atr_name, j_value in v.items():
                j_atr = '{}.{}'.format(i_path, j_atr_name)

                # ignore non exists
                if cmds.objExists(j_atr) is False:
                    continue

                # ignore non settable
                if qsm_mya_core.NodeAttribute.is_settable(i_path, j_atr_name) is False:
                    continue

                cmds.setAttr(j_atr, j_value)
