# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core

import qsm_maya.motion.core as qsm_mya_mtn_core

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
    def find_control_set(cls, namespace):
        _ = cmds.ls('{}:ControlSet'.format(namespace), long=1)
        if _:
            return _[0]

    @classmethod
    def find_body_controls(cls, namespace):
        _ = cls.find_control_set(namespace)
        if _:
            return [qsm_mya_core.DagNode.to_path(x) for x in cmds.sets(_, query=1) or []]
        return []

    @classmethod
    def find_face_control_set(cls, namespace):
        _ = cmds.ls('{}:FaceControlSet'.format(namespace), long=1)
        if _:
            return _[0]

    @classmethod
    def find_face_controls(cls, namespace):
        _ = cls.find_face_control_set(namespace)
        if _:
            return [qsm_mya_core.DagNode.to_path(x) for x in cmds.sets(_, query=1) or []]
        return []

    @classmethod
    def find_controls(cls, namespace):
        return cls.find_body_controls(namespace)+cls.find_face_controls(namespace)

    @classmethod
    def generate(cls, namespace):
        return cls(
            cls.find_controls(namespace)
        )

    def __init__(self, *args, **kwargs):
        super(AdvControlSet, self).__init__(*args, **kwargs)

    def get_frame_range(self):
        curve_nodes = []
        for i in self._paths:
            i_curve_nodes = qsm_mya_mtn_core.ControlMotionOpt(i).get_all_curve_nodes()
            curve_nodes.extend(i_curve_nodes)
        if curve_nodes:
            return qsm_mya_core.AnimCurves.get_range(curve_nodes)
        return qsm_mya_core.Frame.get_frame_range()

    def get_data(self):
        return qsm_mya_mtn_core.ControlsMotionOpt(self._namespace, self._paths).get_data()


class AdvChrControlSet(AdvControlSet):
    def __init__(self, *args, **kwargs):
        super(AdvChrControlSet, self).__init__(*args, **kwargs)

