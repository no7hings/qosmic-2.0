# coding:utf-8
import six
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core

import qsm_maya.motion.core as qsm_mya_mtn_core

from ..core import sketch as _cor_sketch


class MixamoSketchSet(_cor_sketch.AbsSketchSet):
    @classmethod
    def find_root(cls, namespace):
        _ = cmds.ls('|{}:*'.format(namespace, long=1))
        if _:
            return _[0]

    @classmethod
    def generate(cls, namespace):
        return cls(
            cmds.ls(cls.find_root(namespace), type='joint', long=1, dag=1) or []
        )

    def __init__(self, *args, **kwargs):
        super(MixamoSketchSet, self).__init__(*args, **kwargs)
        self._sketch_map = self.generate_sketch_map()

    def zero_out(self):
        for i in self._paths:
            for j_atr_name in ['rotateX', 'rotateY', 'rotateZ']:
                cmds.setAttr(i+'.'+j_atr_name, 0)

        distance = self.compute_root_height()
        root = self.get('Hips')
        cmds.setAttr(root+'.translateY', distance)

    def compute_root_height(self):
        toe = self.get('RightToe_End')
        point_0 = qsm_mya_core.Transform.get_world_translation(toe)
        root = self.get('Hips')
        point_1 = qsm_mya_core.Transform.get_world_translation(root)
        distance = qsm_mya_core.Transform.compute_distance(point_0, point_1)
        return distance

    def get_all_keys(self):
        return self._sketch_map.keys()

    def generate_sketch_map(self):
        dict_ = {}
        for i_key, v in self.ChrMasterSketchMap.Mixamo.items():
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

    def connect_to_master(self, sketch_set):
        for i_key, v in self._sketch_map.items():
            i_src = v
            i_tgt = sketch_set.get(i_key)

            if i_key == self.ChrMasterSketches.Root_M:
                qsm_mya_core.PointConstraint.create(
                    i_src, i_tgt
                )

            qsm_mya_core.OrientConstraint.create(
                i_src, i_tgt, maintain_offset=1
            )

    def compute_height(self):
        pass

    def generate_bbox(self):
        self.zero_out()
        # start_frame, end_frame = self.get_frame_range()
        # print start_frame, end_frame
        # count = end_frame-start_frame+1
        # middle = count/2
        # print qsm_mya_core.BBox.exact_for_many(
        #     self._paths
        # )
