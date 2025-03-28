# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from ..base import abc as _bsc_abc

from ..base import sketch as _bsc_sketch

from . import sketch_set as _sketch_set

from . import control_set as _control_set


class AdvResource(_bsc_abc.AbsMontage):
    def __init__(self, namespace):
        super(AdvResource, self).__init__()
        if qsm_mya_core.Namespace.is_exists(namespace) is False:
            raise RuntimeError()

        self._namespace = namespace

        self._sketch_set = _sketch_set.AdvChrSketchSet.generate(self._namespace)
        self._control_set = _control_set.AdvChrControlSet.generate(self._namespace)

    @property
    def sketch_set(self):
        return self._sketch_set

    def find_main_control(self):
        _ = cmds.ls('{}:Main'.format(self._namespace), long=1)
        if _:
            return _[0]

    def export_to(self, file_path, frame_range=None):
        bsc_storage.StgFileOpt(file_path).set_write(
            self.get_data(frame_range)
        )

    def find_root_location(self):
        _ = cmds.ls('|{}:*'.format(self._namespace), long=1)
        if _:
            return _[0]

    def get_frame_range(self):
        return self._control_set.get_frame_range()

    def get_data(self, frame_range=None):
        if frame_range is not None:
            start_frame, end_frame = frame_range
        else:
            start_frame, end_frame = self._control_set.get_frame_range()

        # sketch motion
        data = self._sketch_set.get_data(start_frame, end_frame)
        data['root_height'] = self.get_root_height()
        # control motion
        data['controls'] = self._control_set.generate_motion_dict()

        data['metadata'] = dict(
            ctime=bsc_core.BscSystem.generate_timestamp(),
            user=bsc_core.BscSystem.get_user_name(),
            host=bsc_core.BscSystem.get_host(),
            reference=dict(
                file=self.find_reference_file(),
                namespace=self._namespace
            ),
            start_frame=start_frame,
            end_frame=end_frame,
            fps=qsm_mya_core.Frame.get_fps(),
            api_version='1.0.1'
        )
        return data

    def find_control_by_sketch_key(self, sketch_key):
        control_key_query = self._configure.control_key_query
        if sketch_key in control_key_query:
            control_key = control_key_query[sketch_key]
            return self._control_set.get(control_key)

    def get_sketch_master_orients(self):
        return self._sketch_set.get_orients()

    def switch_all_controls_to_fk(self):
        switch_control_keys = [
            'FKIKArm_R', 'FKIKArm_L',
            'FKIKLeg_R', 'FKIKLeg_L'
        ]

        for i_control_key in switch_control_keys:
            i_control = self._control_set.get(i_control_key)
            cmds.setAttr(i_control+'.'+'FKIKBlend', 0)

    def get_root_height(self):
        # to zero and mark
        old_data = self.zero_all_controls()
        h = self._sketch_set.compute_root_height()
        self.apply_control_data(old_data)
        return h
    
    def zero_all_controls(self):
        return self._control_set.zero_out()

    def apply_control_data(self, data):
        self._control_set.apply_data(data)

    def get_height(self):
        return self._sketch_set.compute_height()

    # to master layer
    def fit_scale_to_master_layer(self, mtg_master_layer):
        root_height = self.get_root_height()
        master_lower_height = self._sketch_set.DEFAULT_MASTER_LOWER_HEIGHT
        scale = root_height/master_lower_height
        mtg_master_layer.apply_root_scale(scale)

    def fit_sketches_to_master_layer(self, mtg_master_layer):
        basic_sketch_keys = self._configure.basic_sketch_keys
        for i_sketch_key in basic_sketch_keys:
            # adv sketch
            i_sketch_src = self._sketch_set.get(i_sketch_key)
            # other
            i_sketch_tgt = mtg_master_layer.get_sketch(i_sketch_key)
            if i_sketch_src is not None and i_sketch_tgt is not None:
                _bsc_sketch.Sketch(i_sketch_tgt).match_rotations_from(i_sketch_src)
                _bsc_sketch.Sketch(i_sketch_tgt).match_orients_from(i_sketch_src)
    
    def constraint_from_master_layer(self, mtg_master_layer):
        self.switch_all_controls_to_fk()
        # match
        orients = self.get_sketch_master_orients()
        for i_sketch_key, v in orients.items():
            i_sketch_src = mtg_master_layer.get_sketch(i_sketch_key)
            _bsc_sketch.Sketch(i_sketch_src).apply_orients(v)

        root_sketch_key = self._configure.root_sketch_key
        for i_sketch_key, v in orients.items():
            i_sketch_src = mtg_master_layer.get_sketch(i_sketch_key)
            i_control_dst = self.find_control_by_sketch_key(i_sketch_key)
            if i_control_dst is not None:
                if i_sketch_key == root_sketch_key:
                    # must use this method to constraint
                    _bsc_sketch.Sketch(i_sketch_src).create_point_constraint_to_resource(i_control_dst)
                    _bsc_sketch.Sketch(i_sketch_src).create_orient_constraint_to_resource(
                        i_control_dst, clear_offset=False
                    )
                else:
                    _bsc_sketch.Sketch(i_sketch_src).create_orient_constraint_to_resource(i_control_dst)

    def connect_from_master_layer(self, mtg_master_layer):
        self.fit_scale_to_master_layer(mtg_master_layer)
        self.fit_sketches_to_master_layer(mtg_master_layer)
        self.constraint_from_master_layer(mtg_master_layer)

    # to transfer
    def fit_scale_to_transfer_resource(self, transfer_resource):
        root_height = self.get_root_height()
        master_lower_height = self._sketch_set.DEFAULT_MASTER_LOWER_HEIGHT
        scale = root_height/master_lower_height
        transfer_resource.apply_root_scale(scale)

    def fit_sketches_to_transfer_resource(self, transfer_resource):
        basic_sketch_keys = self._configure.basic_sketch_keys
        for i_sketch_key in basic_sketch_keys:
            # adv sketch
            i_sketch_src = self._sketch_set.get(i_sketch_key)
            # other
            i_sketch_tgt = transfer_resource.find_sketch(i_sketch_key)
            if i_sketch_src is not None and i_sketch_tgt is not None:
                _bsc_sketch.Sketch(i_sketch_tgt).match_rotations_from(i_sketch_src)
                _bsc_sketch.Sketch(i_sketch_tgt).match_orients_from(i_sketch_src)

    def constraint_from_transfer_resource(self, transfer_resource):
        self.switch_all_controls_to_fk()
        # match
        orients = self.get_sketch_master_orients()
        for i_sketch_key, v in orients.items():
            i_sketch_src = transfer_resource.find_sketch(i_sketch_key)
            _bsc_sketch.Sketch(i_sketch_src).apply_orients(v)

        root_sketch_key = self._configure.root_sketch_key
        for i_sketch_key, v in orients.items():
            i_sketch_src = transfer_resource.find_sketch(i_sketch_key)
            i_control_dst = self.find_control_by_sketch_key(i_sketch_key)
            if i_control_dst is not None:
                if i_sketch_key == root_sketch_key:
                    _bsc_sketch.Sketch(i_sketch_src).create_point_constraint_to_resource(i_control_dst)
                    _bsc_sketch.Sketch(i_sketch_src).create_orient_constraint_to_resource(
                        i_control_dst, clear_offset=False
                    )
                else:
                    _bsc_sketch.Sketch(i_sketch_src).create_orient_constraint_to_resource(i_control_dst)

    def connect_from_transfer_resource(self, transfer_resource):
        self.fit_scale_to_transfer_resource(transfer_resource)
        self.fit_sketches_to_transfer_resource(transfer_resource)
        self.constraint_from_transfer_resource(transfer_resource)

    def find_reference_file(self):
        return qsm_mya_core.ReferencesCache().get_file(self._namespace)

    def find_sketch(self, sketch_key):
        return self._sketch_set.find_one(sketch_key)

    def bake_controls_keyframes(self, start_frame, end_frame):
        control_key_query = self._configure.control_key_query
        control_keys = control_key_query.values()

        controls = [self._control_set.get(x) for x in control_keys]
        controls = list(filter(None, controls))

        # fixme: face control is ignore?
        control_set = _control_set.AdvControlSet(controls)
        control_set.bake_all_keyframes(
            start_frame, end_frame,
            attributes=[
                'translateX', 'translateY', 'translateZ',
                'rotateX', 'rotateY', 'rotateZ',
            ]
        )

    @classmethod
    def test(cls):
        cls('sam_Skin')._control_set.bake_all_keyframes(
            1, 24, ['translateX', 'translateY']
        )
