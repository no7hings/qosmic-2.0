# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from ..base import sketch as _bsc_sketch

from . import sketch_set as _sketch_set

from . import control_set as _control_set


class AdvResource(object):
    """
    """
    def __init__(self, namespace):
        self._namespace = namespace
        self._sketch_set = _sketch_set.AdvChrSketchSet.generate(self._namespace)
        self._control_set = _control_set.AdvChrControlSet.generate(self._namespace)

    def export_to(self, file_path):
        bsc_storage.StgFileOpt(file_path).set_write(
            self.get_data()
        )

    def get_root(self):
        _ = cmds.ls('|{}:*'.format(self._namespace), long=1)
        if _:
            return _[0]

    def get_data(self):
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
            fps=qsm_mya_core.Frame.get_fps()
        )
        return data

    def get_control_by_sketch_key(self, sketch_key):
        if sketch_key in self._sketch_set.ChrMasterControlMap.Default:
            control_key = self._sketch_set.ChrMasterControlMap.Default[sketch_key]
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
        # [0.0, 8.476478501911147, 0.04798655039699984]
        root_x_control = self._control_set.get('RootX_M')
        main_control = self._control_set.get('Main')
        translate_0 = cmds.xform(root_x_control, translation=1, worldSpace=0, query=1)
        world_translate_0 = cmds.xform(root_x_control, translation=1, worldSpace=1, query=1)
        world_translate_1 = cmds.xform(main_control, translation=1, worldSpace=1, query=1)
        t_0 = [world_translate_0[x]-translate_0[x] for x in range(3)]
        return qsm_mya_core.Transform.compute_distance(t_0, world_translate_1)

    def get_root_translate(self):
        pass

    def connect_from_master_layer(self, master_layer):
        self.switch_all_controls_to_fk()
        # match
        orients = self.get_sketch_master_orients()
        for i_sketch_key, v in orients.items():
            i_sketch_src = master_layer.get(i_sketch_key)
            _bsc_sketch.Sketch(i_sketch_src).apply_orients(v)

        for i_sketch_key, v in orients.items():
            i_sketch_src = master_layer.get(i_sketch_key)
            i_control_dst = self.get_control_by_sketch_key(i_sketch_key)
            if i_control_dst is not None:
                if i_sketch_key == master_layer.ChrMasterSketches.Root_M:
                    _bsc_sketch.Sketch(i_sketch_src).create_point_constraint_to_resource(i_control_dst)
                    _bsc_sketch.Sketch(i_sketch_src).create_orient_constraint_to_resource(i_control_dst, clear_offset=False)
                else:
                    _bsc_sketch.Sketch(i_sketch_src).create_orient_constraint_to_resource(i_control_dst)

    def fit_master_layer_scale(self, layer):
        root_height = self.get_root_height()
        master_root_height = self._sketch_set.DEFAULT_MASTER_ROOT_HEIGHT
        scale = root_height/master_root_height
        layer.apply_root_scale(scale)

    def fit_layer_sketches(self, layer):
        for i_sketch_key in self._sketch_set.ChrMasterSketches.Basic:
            i_sketch_src = self._sketch_set.get(i_sketch_key)
            i_sketch_tgt = layer.get(i_sketch_key)
            if i_sketch_src is not None and i_sketch_tgt is not None:
                _bsc_sketch.Sketch(i_sketch_tgt).match_rotations_from(i_sketch_src)
                _bsc_sketch.Sketch(i_sketch_tgt).match_orients_from(i_sketch_src)

    def find_reference_file(self):
        return qsm_mya_core.ReferencesCache().get_file(self._namespace)

    @classmethod
    def test(cls):
        cls('sam_Skin')._control_set.bake_all_keyframes(
            1, 24, ['translateX', 'translateY']
        )