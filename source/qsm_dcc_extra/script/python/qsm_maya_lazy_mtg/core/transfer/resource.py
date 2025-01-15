# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core

from ..base import abc as _bsc_abc

from ..base import sketch as _bsc_sketch

from ..mocap import sketch_set as _mcp_sketch_set

from . import sketch_set as _sketch_set


class TransferResource(_bsc_abc.AbsMontage):
    def __init__(self, namespace):
        self._namespace = namespace

        self._sketch_set = _sketch_set.TransferSketchSet.generate(self._namespace)

    @classmethod
    def create_sketches(cls):
        _sketch_set.TransferSketchSet.create(
            cls.Namespaces.Transfer
        )

    @classmethod
    def find_mocap_namespaces(cls):
        return _mcp_sketch_set.MocapSketchSet.find_valid_namespaces()

    def find_root_location(self):
        _ = cmds.ls('|{}:*'.format(self._namespace, long=1))
        if _:
            return _[0]

    def apply_root_scale(self, scale):
        location = self.find_root_location()
        qsm_mya_core.NodeAttribute.set_as_tuple(
            location, 'scale', (scale, scale, scale)
        )

    def get_root_height(self):
        # is a constant value now
        return self._sketch_set.DEFAULT_MASTER_LOWER_HEIGHT

    def get_height(self):
        return self._sketch_set.DEFAULT_MASTER_HEIGHT

    def fit_scale_from_mocap(self, mocap_resource):
        height_0 = mocap_resource.get_root_height()
        height_1 = self.get_root_height()

        scale = height_0/height_1

        root_location = self.find_root_location()

        cmds.setAttr(root_location+'.scale', scale, scale, scale)

    def fit_sketches_from_mocap(self, mocap_resource):
        for i_sketch_key in self._sketch_set.ChrMasterSketches.Basic:
            # mocap
            i_sketch_src = mocap_resource.find_sketch(i_sketch_key)
            # transfer
            i_sketch_tgt = self.find_sketch(i_sketch_key)
            if i_sketch_src is not None and i_sketch_tgt is not None:
                _bsc_sketch.Sketch(i_sketch_tgt).match_rotations_from(i_sketch_src)
                _bsc_sketch.Sketch(i_sketch_tgt).match_orients_from(i_sketch_src)

    def constraint_from_mocap(self, mocap_resource):
        mocap_resource.sketch_set.constraint_to_transfer_sketch(
            self._sketch_set, break_parent_inverse=True
        )

    def connect_from_mocap(self, mocap_resource):
        self.fit_scale_from_mocap(mocap_resource)
        # do not math sketch to mocap
        # self.fit_sketches_from_mocap(mocap_resource)
        self.constraint_from_mocap(mocap_resource)

    def find_sketch(self, sketch_key):
        return self._sketch_set.find_one(sketch_key)

    def bake_sketches_keyframes(self, start_frame, end_frame):
        self._sketch_set.bake_all_keyframes(
            start_frame, end_frame,
            attributes=[
                'translateX', 'translateY', 'translateZ',
                'rotateX', 'rotateY', 'rotateZ',
            ]
        )

    def do_delete(self):
        location = self.find_root_location()
        qsm_mya_core.Node.delete(location)

    @classmethod
    def test(cls):
        pass

