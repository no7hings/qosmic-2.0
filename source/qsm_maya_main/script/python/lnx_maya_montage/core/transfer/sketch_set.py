# coding:utf-8
import six
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.resource as bsc_resource

import qsm_maya.core as qsm_mya_core

import qsm_maya.graph as qsm_mya_graph

import qsm_maya.motion as qsm_mya_motion

from ..base import sketch as _bsc_sketch

from ..base import sketch_set as _bsc_sketch_set


class _SketchGraph(qsm_mya_graph.GraphBase):
    def __init__(self, namespace, cfg_key):
        self._namespace = namespace
        self._cfg_key = cfg_key

    def create_all(self):
        qsm_mya_core.Namespace.create(self._namespace)
        self._cfg = bsc_resource.BscConfigure.get_as_content(self._cfg_key)
        self._cfg.set('options.namespace', self._namespace)
        self._cfg.do_flatten()
        dag_nodes = self._create_dag_nodes_fnc(self._namespace, self._cfg)


class TransferSketchSet(_bsc_sketch_set.AbsSketchSet):
    @classmethod
    def create(cls, namespace):
        graph = _SketchGraph(
            namespace, 'maya/montage/mtg_sketch'
        )
        graph.create_all()

    @classmethod
    def find_root_location(cls, namespace):
        _ = cmds.ls('|{}:*'.format(namespace, long=1))
        if _:
            return _[0]

    @classmethod
    def find_sketches(cls, namespace):
        _ = cls.find_root_location(namespace)
        if _:
            return cmds.ls(_, type='joint', long=1, dag=1) or []
        return []

    def __init__(self, *args, **kwargs):
        super(TransferSketchSet, self).__init__(*args, **kwargs)
        self._sketch_map = self.generate_sketch_map()

    def zero_out(self):
        # make sure auto keyframe is disable
        with qsm_mya_core.auto_keyframe_context(False):
            for i in self._paths:
                for j_atr_name in ['rotateX', 'rotateY', 'rotateZ']:
                    cmds.setAttr(i+'.'+j_atr_name, 0)

            distance = self.compute_root_height()
            root = self.get('Root_M')
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
        return list(self._sketch_map.keys())

    def generate_sketch_map(self):
        dict_ = {}
        all_sketch_keys = self._configure.all_sketch_keys
        for i_key in all_sketch_keys:
            i_path = self.get(i_key)
            dict_[i_key] = i_path
        return dict_

    def get_data_at_frame(self, frame):
        qsm_mya_core.Frame.set_current(frame)

        dict_ = {}
        root_sketch_key = self._configure.root_sketch_key
        for i_sketch_key, i_sketch_path in self._sketch_map.items():
            i_sketch = _bsc_sketch.Sketch(i_sketch_path)
            if i_sketch_key == root_sketch_key:
                dict_[i_sketch_key] = i_sketch.get_data(
                    [
                        'translateX', 'translateY', 'translateZ',
                        'rotateX', 'rotateY', 'rotateZ'
                    ]
                )
            else:
                dict_[i_sketch_key] = i_sketch.get_data(
                    [
                        'rotateX', 'rotateY', 'rotateZ'
                    ]
                )
        return dict_

    def get_orients(self):
        dict_ = {}
        for i_sketch_key, i_path in self._sketch_map.items():
            dict_[i_sketch_key] = _bsc_sketch.Sketch(i_path).get_orients()
        return dict_

    def get_data(self, start_frame, end_frame):
        dict_0_ = {}
        all_keys = self.get_all_keys()
        for i_frame in range(start_frame, end_frame+1):
            i_data = self.get_data_at_frame(i_frame)
            for j_key in all_keys:
                dict_0_.setdefault(
                    j_key, []
                ).append(
                    i_data[j_key]
                )

        orient_data = self.get_orients()

        sketch_data = {}
        for i_sketch_key, i_v in dict_0_.items():
            i_time_samples = {}
            for j_frame in i_v:
                for k_atr_name, k_value in j_frame.items():
                    i_time_samples.setdefault(k_atr_name, []).append(k_value)

            sketch_data[i_sketch_key] = dict(
                time_samples=i_time_samples,
                orients=orient_data[i_sketch_key]
            )

        return dict(
            sketches=sketch_data,
            frame_count=end_frame-start_frame+1
        )

    def get_frame_range(self):
        curve_nodes = []
        for i in self._paths:
            i_curve_nodes = qsm_mya_motion.ControlMotionOpt(i).get_all_curve_nodes()
            curve_nodes.extend(i_curve_nodes)
        if curve_nodes:
            return qsm_mya_core.AnmCurveNodes.get_range(curve_nodes)
        return qsm_mya_core.Frame.get_frame_range()

    def find_one(self, sketch_key):
        return self._sketch_map.get(sketch_key)
