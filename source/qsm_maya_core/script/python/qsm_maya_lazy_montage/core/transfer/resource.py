# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from ..base import abc as _bsc_abc

from ..base import sketch as _bsc_sketch

from ..mocap import sketch_set as _mcp_sketch_set

from . import sketch_set as _sketch_set


class TransferResource(_bsc_abc.AbsMontage):
    def __init__(self, namespace):
        super(TransferResource, self).__init__()

        self._namespace = namespace

        self._sketch_set = _sketch_set.TransferSketchSet.generate(self._namespace)

    @classmethod
    def create_sketches(cls, namespace):
        _sketch_set.TransferSketchSet.create(namespace)

    @classmethod
    def find_mocap_namespaces(cls):
        return _mcp_sketch_set.MocapSketchSet.find_valid_namespaces()

    @classmethod
    def find_mocap_locations(cls):
        return _mcp_sketch_set.MocapSketchSet.find_valid_locations()

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

    def fit_scale_from_mocap_resource(self, mocap_resource):
        # zero sketch in get_root_height method
        height_0 = mocap_resource.get_root_height()
        height_1 = self.get_root_height()

        scale = height_0/height_1

        root_location = self.find_root_location()

        cmds.setAttr(root_location+'.scale', scale, scale, scale)

    def fit_sketches_from_mocap(self, mocap_resource):
        basic_sketch_keys = self._configure.basic_sketch_keys
        for i_sketch_key in basic_sketch_keys:
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
        start_frame, end_frame = mocap_resource.get_frame_range()
        qsm_mya_core.Frame.set_current(start_frame)
        self.fit_scale_from_mocap_resource(mocap_resource)
        # todo: create keyframe for default?
        self._sketch_set.create_all_keyframe_at(start_frame)
        self.constraint_from_mocap(mocap_resource)

    def fit_scale_from_adv_resource(self, adv_resource):
        height_0 = adv_resource.get_root_height()
        height_1 = self.get_root_height()

        scale = height_0/height_1

        root_location = self.find_root_location()
        cmds.setAttr(root_location+'.scale', scale, scale, scale)

    def constraint_from_adv(self, adv_resource):
        adv_resource.sketch_set.constraint_to_transfer_sketch(
            self._sketch_set, break_parent_inverse=True
        )

    def connect_from_adv(self, adv_resource):
        start_frame, end_frame = adv_resource.get_frame_range()
        # qsm_mya_core.Frame.set_current(start_frame)
        # old_data = adv_resource.zero_all_controls()
        self.fit_scale_from_adv_resource(adv_resource)
        # # adv_resource.apply_control_data(old_data)
        self.constraint_from_adv(adv_resource)

    def fit_scale_to_master_resource(self, master_resource):
        height_0 = master_resource.get_root_height()
        height_1 = self.get_root_height()

        scale = height_0/height_1

        root_location = self.find_root_location()

        cmds.setAttr(root_location+'.scale', scale, scale, scale)
        
    def connect_to_master_resource(self, master_resource):
        basic_sketch_keys = self._configure.basic_sketch_keys
        root_sketch_key = self._configure.root_sketch_key
        for i_sketch_key in basic_sketch_keys:
            i_sketch_src = self.find_sketch(i_sketch_key)

            i_sketch_dst = master_resource.find_sketch(i_sketch_key)
            if i_sketch_key == root_sketch_key:
                _bsc_sketch.Sketch(i_sketch_src).create_point_constraint_to_master(
                    i_sketch_dst, break_parent_inverse=True
                )
                _bsc_sketch.Sketch(i_sketch_src).create_orient_constraint_to_master(
                    i_sketch_dst, break_parent_inverse=True
                )
            else:
                _bsc_sketch.Sketch(i_sketch_src).create_orient_constraint_to_master(
                    i_sketch_dst
                )

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

    def export_motion_to(self, start_frame, end_frame, motion_json_path):
        self.bake_sketches_keyframes(start_frame, end_frame)
        bsc_storage.StgFileOpt(motion_json_path).set_write(
            self.get_motion_data(start_frame, end_frame)
        )

    def get_motion_data(self, start_frame, end_frame):
        data = self._sketch_set.get_data(start_frame, end_frame)
        data['root_height'] = self.get_root_height()
        data['scale'] = self.get_scale()
        data['metadata'] = dict(
            ctime=bsc_core.BscSystem.generate_timestamp(),
            user=bsc_core.BscSystem.get_user_name(),
            host=bsc_core.BscSystem.get_host(),
            start_frame=start_frame,
            end_frame=end_frame,
            fps=qsm_mya_core.Frame.get_fps(),
            api_version='1.0.1'
        )
        return data

    def do_delete(self):
        location = self.find_root_location()
        qsm_mya_core.Node.delete(location)

    def get_scale(self):
        location = self.find_root_location()
        return cmds.getAttr(location+'.scaleX')

    @classmethod
    def test(cls):
        pass
