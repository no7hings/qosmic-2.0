# coding:utf-8
import sys

import six
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core

import qsm_maya.motion as qsm_mya_motion

from ..base import sketch_set as _bsc_sketch_set


class MocapSketchSet(_bsc_sketch_set.AbsSketchSet):
    @classmethod
    def find_roots(cls, namespace):
        return cmds.ls('|{}:*'.format(namespace, long=1))

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
    def find_valid_locations(cls):
        list_ = []
        for i_ptn in ['Hips', '*:Hips']:
            i_results = cmds.ls(i_ptn, long=1) or []
            if i_results:
                list_.extend(i_results)
        return list_

    @classmethod
    def find_valid_location(cls, namespace):
        _ = cmds.ls('{}:Hips'.format(namespace), long=1) or []
        if _:
            return _[0]

    @classmethod
    def generate(cls, namespace):
        # todo, may has more than one root
        paths = []
        for i_location in cls.find_roots(namespace):
            i_paths = cmds.ls(i_location, type='joint', long=1, dag=1) or []
            if i_paths:
                paths.extend(i_paths)
        return cls(paths)

    @classmethod
    def generate_by_location(cls, location, include_transform_type=False):
        if include_transform_type is True:
            type_includes = ['joint', 'transform']
        else:
            type_includes = ['joint']
        return cls(cmds.ls(location, type=type_includes, long=1, dag=1) or [])

    def __init__(self, *args, **kwargs):
        super(MocapSketchSet, self).__init__(*args, **kwargs)
        self._sketch_map = self.generate_sketch_map()

    def zero_out(self):
        dict_ = {}
        root_sketch = self._sketch_map.get('Root_M')

        root_rotate = cmds.getAttr(root_sketch+'.rotate')[0]
        root_rotate = [round(x, 3) for x in root_rotate]
        if root_rotate == [0, 0, 0]:
            sys.stdout.write(
                'Root is zero, ignore zero out action.\n'
            )
            return

        for i in self._paths:
            i_dict = {}
            dict_[i] = i_dict
            for j_atr_name in ['rotateX', 'rotateY', 'rotateZ']:
                i_atr = i+'.'+j_atr_name
                i_dict[j_atr_name] = cmds.getAttr(i_atr)
                cmds.setAttr(i_atr, 0)

        # to floor
        distance = self.compute_root_height()
        cmds.setAttr(root_sketch+'.translateY', distance)
        return dict_

    def compute_root_height(self):
        bottom_sketch = self._sketch_map.get('ToesEnd_R')
        # may do not had toes end
        if bottom_sketch is None:
            sys.stdout.write(
                'Toes end is not found.\n'
            )
            bottom_sketch = self._sketch_map.get('Toes_R')

        point_0 = qsm_mya_core.Transform.get_world_translation(bottom_sketch)
        root_sketch = self._sketch_map.get('Root_M')
        point_1 = qsm_mya_core.Transform.get_world_translation(root_sketch)
        distance = qsm_mya_core.Transform.compute_distance(point_0, point_1)
        return distance

    def compute_height(self):
        bottom_sketch = self._sketch_map.get('ToesEnd_R')
        # may do not had toes end
        if bottom_sketch is None:
            sys.stdout.write(
                'Toes end is not found.\n'
            )
            bottom_sketch = self._sketch_map.get('Toes_R')

        point_0 = qsm_mya_core.Transform.get_world_translation(bottom_sketch)
        head = self._sketch_map.get('HeadEnd_M')
        point_1 = qsm_mya_core.Transform.get_world_translation(head)
        distance = qsm_mya_core.Transform.compute_distance(point_0, point_1)
        return distance

    def compute_upper_height(self):
        head = self._sketch_map.get('HeadEnd_M')
        point_0 = qsm_mya_core.Transform.get_world_translation(head)
        root_sketch = self._sketch_map.get('Root_M')
        point_1 = qsm_mya_core.Transform.get_world_translation(root_sketch)
        distance = qsm_mya_core.Transform.compute_distance(point_0, point_1)
        return distance

    def get_all_keys(self):
        return list(self._sketch_map.keys())

    def generate_sketch_map(self):
        dict_ = {}
        mocap_sketch_key_query = self._configure.mocap_sketch_key_query

        for i_key, v in mocap_sketch_key_query.items():
            if isinstance(v, six.string_types):
                i_key_dst = v
                i_path = self.get(i_key_dst)
                if i_path:
                    dict_[i_key] = i_path
            # many target keys available
            elif isinstance(v, (tuple, list)):
                for j_key_dst in v:
                    j_path = self.get(j_key_dst)
                    if j_path:
                        dict_[i_key] = j_path
                        break
        return dict_

    def get_frame_range(self):
        curve_nodes = []
        for i in self._paths:
            i_curve_nodes = qsm_mya_motion.ControlMotionOpt(i).get_all_curve_nodes()
            curve_nodes.extend(i_curve_nodes)
        if curve_nodes:
            return qsm_mya_core.AnmCurveNodes.get_range(curve_nodes)
        return qsm_mya_core.Frame.get_frame_range()

    def constraint_to_transfer_sketch(self, sketch_set, break_parent_inverse=False):
        root_sketch_key = self._configure.root_sketch_key
        for i_sketch_key, v in self._sketch_map.items():
            i_src = v
            i_tgt = sketch_set.get(i_sketch_key)

            if i_sketch_key == root_sketch_key:
                qsm_mya_core.PointConstraint.create(
                    i_src, i_tgt, break_parent_inverse=break_parent_inverse
                )

            qsm_mya_core.OrientConstraint.create(
                i_src, i_tgt, maintain_offset=1
            )
            i_pair_blend = qsm_mya_core.NodeAttribute.get_source_node(
                i_tgt, 'rotateX', 'pairBlend'
            )
            if i_pair_blend:
                # set rotation interpolation to quaternions
                qsm_mya_core.NodeAttribute.set_value(
                    i_pair_blend, 'rotInterpolation', 1
                )

    def constraint_from_master_layer(self, mtg_master_layer):
        root_sketch_key = self._configure.root_sketch_key
        for i_sketch_key, v in self._sketch_map.items():
            i_sketch_src = mtg_master_layer.get_sketch(i_sketch_key)
            i_sketch_tgt = v

            if i_sketch_key == root_sketch_key:
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
