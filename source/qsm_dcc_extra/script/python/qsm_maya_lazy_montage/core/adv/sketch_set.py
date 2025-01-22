# coding:utf-8
import six
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import qsm_maya.core as qsm_mya_core

from ..base import sketch as _bsc_sketch

from ..base import sketch_set as _bsc_sketch_set


# set
class AdvSketchSet(_bsc_sketch_set.AbsSketchSet):
    @classmethod
    def find_deform_set(cls, namespace):
        _ = cmds.ls('{}:DeformSet'.format(namespace), long=1)
        if _:
            return _[0]

    @classmethod
    def find_sketches(cls, namespace):
        _ = cls.find_deform_set(namespace)
        if _:
            return [qsm_mya_core.DagNode.to_path(x) for x in cmds.sets(_, query=1) or []]
        return []

    @classmethod
    def generate(cls, namespace):
        return cls(
            cls.find_sketches(namespace)
        )

    def __init__(self, *args, **kwargs):
        super(AdvSketchSet, self).__init__(*args, **kwargs)


class AdvChrSketchSet(AdvSketchSet):
    @classmethod
    def generate(cls, namespace):
        return cls(
            cls.find_sketches(namespace)
        )

    def __init__(self, *args, **kwargs):
        super(AdvChrSketchSet, self).__init__(*args, **kwargs)
        self._sketch_map = self.generate_sketch_map()

    def get_all_keys(self):
        return self._sketch_map.keys()

    def generate_sketch_map(self):
        dict_ = {}
        adv_sketch_key_query = self._configure.adv_sketch_key_query

        for k, v in adv_sketch_key_query.items():
            if isinstance(v, six.string_types):
                i_key_dst = v
                i_path = self.get(i_key_dst)
                if i_path:
                    dict_[k] = i_path
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

    def get_data_at_frame(self, frame):
        qsm_mya_core.Frame.set_current(frame)

        dict_ = {}
        root_sketch_key = self._configure.root_sketch_key
        extra_sketch_key_query = self._configure.extra_sketch_key_query
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
                if i_sketch_key in extra_sketch_key_query:
                    i_sketch_key_upper = extra_sketch_key_query[i_sketch_key]
                    i_sketch_path_upper = self.get(i_sketch_key_upper)
                    dict_[i_sketch_key] = i_sketch.get_rotation_between(i_sketch_path_upper)
                else:
                    dict_[i_sketch_key] = i_sketch.get_data(
                        [
                            'rotateX', 'rotateY', 'rotateZ'
                        ]
                    )
        return dict_

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

    def find_one(self, sketch_key):
        return self._sketch_map.get(sketch_key)
