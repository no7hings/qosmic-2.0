# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import qsm_maya.core as qsm_mya_core

import qsm_maya.motion as qsm_mya_motion

from ..base import abc as _bsc_abc


class AbsSketchSet(_bsc_abc.AbsMontage):
    def __init__(self, paths):
        super(AbsSketchSet, self).__init__()

        self._paths = paths
        self._namespace = qsm_mya_core.DagNode.extract_namespace(self._paths[0])

        self._cache_dict = {}
        self._cache_all()

    def _cache_all(self):
        self._cache_dict.clear()

        for i_path in self._paths:
            i_sketch_key = qsm_mya_core.DagNode.to_name_without_namespace(i_path)
            self._cache_dict[i_sketch_key] = i_path

    def get(self, sketch_key):
        return self._cache_dict.get(sketch_key)

    def get_all(self):
        return self._cache_dict.values()

    def bake_all_keyframes(self, start_frame, end_frame, attributes=None):
        # do not mark undo here
        qsm_mya_motion.ControlSetBake(self._paths).execute(
            start_frame, end_frame,
            attributes=attributes, reduce_filter=False
        )

    def create_all_keyframe_at(self, frame):
        atr_names = [
            'translateX', 'translateY', 'translateZ',
            'rotateX', 'rotateY', 'rotateZ',
        ]
        for i_sketch in self._paths:
            for j_atr_name in atr_names:
                qsm_mya_core.NodeAttributeKeyframe.create_at(
                    i_sketch, j_atr_name, frame
                )
