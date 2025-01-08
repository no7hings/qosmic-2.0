# coding:utf-8
import six
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core

import qsm_maya.motion.core as qsm_mya_mtn_core

from ..base import sketch_set as _bsc_sketch_set


class MocapSketchSet(_bsc_sketch_set.AbsSketchSet):
    @classmethod
    def find_root(cls, namespace):
        _ = cmds.ls('|{}:*'.format(namespace, long=1))
        if _:
            return _[0]

    @classmethod
    def find_valid_namespaces(cls):
        list_ = []
        _ = cmds.ls('*:Hips', long=1)
        if _:
            for i in _:
                i_namespace = qsm_mya_core.Namespace.extract_from_path(i)
                list_.append(i_namespace)
        return list_

    @classmethod
    def generate(cls, namespace):
        return cls(
            cmds.ls(cls.find_root(namespace), type='joint', long=1, dag=1) or []
        )

    def __init__(self, *args, **kwargs):
        super(MocapSketchSet, self).__init__(*args, **kwargs)
        self._sketch_map = self.generate_sketch_map()

    def zero_out(self):
        for i in self._paths:
            for j_atr_name in ['rotateX', 'rotateY', 'rotateZ']:
                cmds.setAttr(i+'.'+j_atr_name, 0)

        # to floor
        distance = self.compute_root_height()
        root = self._sketch_map.get('Root_M')
        cmds.setAttr(root+'.translateY', distance)

    def compute_root_height(self):
        toe = self._sketch_map.get('ToesEnd_R')
        point_0 = qsm_mya_core.Transform.get_world_translation(toe)
        root = self._sketch_map.get('Root_M')
        point_1 = qsm_mya_core.Transform.get_world_translation(root)
        distance = qsm_mya_core.Transform.compute_distance(point_0, point_1)
        return distance

    def compute_height(self):
        toe = self._sketch_map.get('ToesEnd_R')
        point_0 = qsm_mya_core.Transform.get_world_translation(toe)
        head = self._sketch_map.get('HeadEnd_M')
        point_1 = qsm_mya_core.Transform.get_world_translation(head)
        distance = qsm_mya_core.Transform.compute_distance(point_0, point_1)
        return distance

    def compute_upper_height(self):
        head = self._sketch_map.get('HeadEnd_M')
        point_0 = qsm_mya_core.Transform.get_world_translation(head)
        root = self._sketch_map.get('Root_M')
        point_1 = qsm_mya_core.Transform.get_world_translation(root)
        distance = qsm_mya_core.Transform.compute_distance(point_0, point_1)
        return distance

    def get_all_keys(self):
        return self._sketch_map.keys()

    def generate_sketch_map(self):
        dict_ = {}
        for i_key, v in self.ChrMasterSketchMap.MoCap.items():
            if isinstance(v, six.string_types):
                i_key_dst = v
                i_path = self.get(i_key_dst)
                if i_path:
                    dict_[i_key] = i_path
        return dict_

    def get_frame_range(self):
        curve_nodes = []
        for i in self._paths:
            i_curve_nodes = qsm_mya_mtn_core.ControlMotionOpt(i).get_all_curve_nodes()
            curve_nodes.extend(i_curve_nodes)
        if curve_nodes:
            return qsm_mya_core.AnimCurveNodes.get_range(curve_nodes)
        return qsm_mya_core.Frame.get_frame_range()

    def constraint_to_transfer_sketch(self, sketch_set, break_parent_inverse=False):
        for i_sketch_key, v in self._sketch_map.items():
            i_src = v
            i_tgt = sketch_set.get(i_sketch_key)

            if i_sketch_key == self.ChrMasterSketches.Root_M:
                qsm_mya_core.PointConstraint.create(
                    i_src, i_tgt, break_parent_inverse=break_parent_inverse
                )

            qsm_mya_core.OrientConstraint.create(
                i_src, i_tgt, maintain_offset=1
            )

    def constraint_from_master_layer(self, master_layer):
        for i_sketch_key, v in self._sketch_map.items():
            i_sketch_src = master_layer.get_sketch(i_sketch_key)
            i_sketch_tgt = v

            if i_sketch_key == self.ChrMasterSketches.Root_M:
                qsm_mya_core.PointConstraint.create(
                    i_sketch_src, i_sketch_tgt
                )

            qsm_mya_core.OrientConstraint.create(
                i_sketch_src, i_sketch_tgt, maintain_offset=1
            )

    def generate_bbox(self):
        self.zero_out()

    def find_one(self, sketch_key):
        return self._sketch_map.get(sketch_key)
