# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

from .. import motion as _mya_motion

from .. import core as _mya_core

from . import base as _base

from . import sketch_set as _sketch_set

from . import control_set as _control_set


class AdvOpt(_base.AdvNamespaceExtra):
    LOG_KEY = 'adv rig motion'

    CONTROL_SET_CLS = _control_set.AdvControlSet

    @classmethod
    def check_is_valid(cls, namespace):
        _ = cmds.ls('{}:DeformSet'.format(namespace), long=1)
        if _:
            return True
        return False

    def __init__(self, namespace):
        self._init_namespace_extra(namespace)

        self._sketch_set = _sketch_set.AdvSketchSet.generate(self._namespace)
        self._control_set = self.CONTROL_SET_CLS.generate(self._namespace)

    def find_root_location(self):
        _ = cmds.ls('|{}:*'.format(self._namespace), long=1)
        if _:
            return _[0]

    # control motion
    def generate_controls_motion_dict(self):
        controls = self.find_all_controls()
        if controls:
            return _mya_motion.ControlSetMotionOpt(self._namespace, controls).generate_motion_dict()
        return {}

    def generate_controls_pose_dict(self):
        controls = self.find_all_controls()
        if controls:
            return _mya_motion.ControlSetMotionOpt(self._namespace, controls).generate_pose_dict()
        return {}

    def apply_controls_motion_dict(self, data, **kwargs):
        controls = self.find_all_controls()
        if controls:
            _mya_motion.ControlSetMotionOpt(self._namespace, controls).apply_motion_dict(data, **kwargs)

    def apply_controls_pose_dict(self, data, **kwargs):
        controls = self.find_all_controls()
        if controls:
            _mya_motion.ControlSetMotionOpt(self._namespace, controls).apply_pose_dict(data, **kwargs)
    
    # control motion file
    def export_controls_motion_to(self, file_path):
        bsc_storage.StgFileOpt(file_path).set_write(
            self.generate_controls_motion_dict()
        )

    def export_controls_pose_to(self, file_path):
        bsc_storage.StgFileOpt(file_path).set_write(
            self.generate_controls_pose_dict()
        )

    def load_controls_motion_from(self, file_path, **kwargs):
        self.apply_controls_motion_dict(
            bsc_storage.StgFileOpt(file_path).set_read(), **kwargs
        )

    def load_controls_pose_from(self, file_path, **kwargs):
        self.apply_controls_pose_dict(
            bsc_storage.StgFileOpt(file_path).set_read(), **kwargs
        )

    def transfer_controls_motion(self, namespace, **kwargs):
        self.__class__(namespace).apply_controls_motion_dict(
            self.generate_controls_motion_dict(), **kwargs
        )

    # mirror
    def mirror_controls_motion_left_to_right(self, **kwargs):
        controls = self.find_all_controls()
        if controls:
            _mya_motion.ControlSetMotionOpt(self._namespace, controls).mirror_motion_left_to_right(**kwargs)
            
    def mirror_controls_pose_left_to_right(self, **kwargs):
        controls = self.find_all_controls()
        if controls:
            _mya_motion.ControlSetMotionOpt(self._namespace, controls).mirror_pose_left_to_right(**kwargs)

    def mirror_controls_motion_middle(self, **kwargs):
        controls = self.find_all_controls()
        if controls:
            _mya_motion.ControlSetMotionOpt(self._namespace, controls).mirror_motion_middle(**kwargs)
    
    def mirror_controls_pose_middle(self, **kwargs):
        controls = self.find_all_controls()
        if controls:
            _mya_motion.ControlSetMotionOpt(self._namespace, controls).mirror_pose_middle(**kwargs)

    def mirror_controls_motion_right_to_left(self, **kwargs):
        controls = self.find_all_controls()
        if controls:
            _mya_motion.ControlSetMotionOpt(self._namespace, controls).mirror_motion_right_to_left(**kwargs)
            
    def mirror_controls_pose_right_to_left(self, **kwargs):
        controls = self.find_all_controls()
        if controls:
            _mya_motion.ControlSetMotionOpt(self._namespace, controls).mirror_pose_right_to_left(**kwargs)
    
    # flip
    def flip_controls_motion(self, **kwargs):
        controls = self.find_all_controls()
        if controls:
            _mya_motion.ControlSetMotionOpt(self._namespace, controls).flip_motion(**kwargs)

    def flip_controls_pose(self, **kwargs):
        controls = self.find_all_controls()
        if controls:
            _mya_motion.ControlSetMotionOpt(self._namespace, controls).flip_pose(**kwargs)

    def rest_controls_transformation(self, **kwargs):
        if 'reset_scheme' in kwargs:
            reset_scheme = kwargs.pop('reset_scheme')
        else:
            reset_scheme = 'default'
        if reset_scheme == 'transform':
            controls = self.find_all_transform_controls()
        elif reset_scheme == 'curve':
            controls = self.find_all_curve_controls()
        else:
            controls = self.find_all_controls()

        if controls:
            return _mya_motion.ControlSetMotionOpt(self._namespace, controls).reset_transformation(**kwargs)
        return False

    def generate_controls_axis_vector_dict(self, **kwargs):
        controls = self.find_all_controls()

        if controls:
            return _mya_motion.ControlSetMotionOpt(self._namespace, controls).generate_axis_vector_dict()
        return {}

    # joint
    def find_joint_set(self):
        """
        """
        _ = cmds.ls('{}:DeformSet'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_all_joints(self):
        _ = self.find_joint_set()
        if _:
            return [_mya_core.DagNode.to_path(x) for x in cmds.sets(_, query=1) or []]
        return []

    # geometry

    def find_geometry_location(self):
        """
        """
        _ = cmds.ls('{}:Geometry'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_all_meshes(self):
        """
        """
        _ = self.find_geometry_location()
        if _:
            return cmds.ls(
                _, type='mesh', long=1, noIntermediate=1, dag=1
            ) or []
        return []

    def find_geo_lower_location(self):
        """
        """
        _ = cmds.ls('{}:Low_Grp'.format(self._namespace), long=1)
        if _:
            return _[0]
        _1 = cmds.ls('{}:Group'.format(self._namespace), long=1)
        if _1:
            return _1[0]

    def find_all_lower_meshes(self):
        """
        """
        _ = self.find_geo_lower_location()
        if _:
            return cmds.ls(
                _, type='mesh', long=1, noIntermediate=1, dag=1
            ) or []
        return []

    @_mya_core.Undo.execute
    def duplicate(self, **kwargs):
        """
        """
        namespace_new = _mya_core.Reference.duplicate(
            _mya_core.ReferencesCache().get(self._namespace)
        )
        self.transfer_controls_motion(
            namespace_new, **kwargs
        )
        _mya_core.Selection.set(
            self.__class__(namespace_new).find_main_control()
        )

    @_mya_core.Undo.execute
    def bake_all_controls(self, *args, **kwargs):
        controls = self.find_all_curve_controls()
        _mya_motion.ControlSetBake(controls).execute(*args, **kwargs)

    def compute_main_control_to_toe_offset(self):
        toes = filter(None, [self._sketch_set.get('ToesEnd_L'), self._sketch_set.get('ToesEnd_R')])

        xs, ys, zs = [], [], []
        for i in toes:
            i_x, i_y, i_z = _mya_core.Transform.get_world_translation(i)
            xs.append(i_x)
            ys.append(i_y)
            zs.append(i_z)

        x, y, z = sum(xs)/2, min(ys), sum(zs)/2

        main_control = self._control_set.get('Main')
        x_0, y_0, z_0 = _mya_core.Transform.get_world_translation(main_control)
        return x-x_0, y-y_0, z-z_0

    @_mya_core.Undo.execute
    def move_main_control_to_toe(self):
        """
        support FK only
        """

        x, y, z = self.compute_main_control_to_toe_offset()

        # move root
        root_control = self._control_set.get('RootX_M')
        root_locator = _mya_motion.ControlMove.create_locator_fnc(root_control)
        x_0, y_0, z_0 = _mya_core.Transform.get_translate(root_locator)
        _mya_core.Transform.set_translate(root_locator, (x_0-x, y_0-y, z_0-z))
        _mya_motion.ControlMove.remove_locator_fnc(root_control)

        # move ik leg
        leg_fkik_blend_controls = [
            self._control_set.get('FKIKLeg_R'), self._control_set.get('FKIKLeg_L')
        ]
        for i in leg_fkik_blend_controls:
            # check is IK
            if _mya_core.NodeAttribute.get_value(i, 'FKIKBlend') == 10:
                i_direction = i[-1]
                i_ik_control = self._control_set.get('IKLeg_{}'.format(i_direction))
                i_ik_locator = _mya_motion.ControlMove.create_locator_fnc(i_ik_control)
                i_x_0, i_y_0, i_z_0 = _mya_core.Transform.get_translate(i_ik_locator)
                _mya_core.Transform.set_translate(i_ik_locator, (i_x_0-x, i_y_0-y, i_z_0-z))
                _mya_motion.ControlMove.remove_locator_fnc(i_ik_control)

        # move main
        main_control = self._control_set.get('Main')
        main_locator = _mya_motion.ControlMove.create_locator_fnc(main_control)
        x_0, y_0, z_0 = _mya_core.Transform.get_translate(main_locator)
        _mya_core.Transform.set_translate(main_locator, (x_0+x, y_0+y, z_0+z))
        _mya_motion.ControlMove.remove_locator_fnc(main_control)


class AdvChrOpt(AdvOpt):
    LOG_KEY = 'adv rig motion'

    CONTROL_SET_CLS = _control_set.AdvChrControlSet

    def __init__(self, *args, **kwargs):
        super(AdvChrOpt, self).__init__(*args, **kwargs)

    def find_body_controls(self):
        _ = self.find_control_set()
        if _:
            return [_mya_core.DagNode.to_path(x) for x in cmds.sets(_, query=1) or []]
        return []

    def find_face_control_set(self):
        _ = cmds.ls('{}:FaceControlSet'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_face_controls(self):
        _ = self.find_face_control_set()
        if _:
            return [_mya_core.DagNode.to_path(x) for x in cmds.sets(_, query=1) or []]
        return []

    def find_all_controls(self):
        return self.find_body_controls()+self.find_face_controls()

    def find_all_basic_curve_controls(self):
        list_ = []
        all_curve_controls = self.find_all_curve_controls()
        for i_key in qsm_gnl_core.AdvCharacterControlConfigure().get_all_curve_control_keys():
            i_results = bsc_core.BscFnmatch.filter(all_curve_controls, '*|{}:{}'.format(self._namespace, i_key))
            list_.extend(i_results)
        return list_

    def find_all_secondary_curve_controls(self):
        return list(
            set(self.find_all_curve_controls())-set(self.find_all_basic_curve_controls())
        )

    def find_all_anm_curves(self):
        controls = self.find_all_controls()
        return _mya_core.AnmCurveNodes.get_all_from(controls)

