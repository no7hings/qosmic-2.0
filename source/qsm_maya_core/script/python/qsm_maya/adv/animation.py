# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

from ..motion import core as _motion_core

from .. import core as _mya_core

from . import base as _base


class AdvOpt(_base.AdvNamespaceExtra):
    LOG_KEY = 'adv rig motion'

    @classmethod
    def check_is_valid(cls, namespace):
        _ = cmds.ls('{}:DeformSet'.format(namespace), long=1)
        if _:
            return True
        return False

    def __init__(self, namespace):
        self._init_namespace_extra(namespace)

    # control motion
    def generate_controls_motion_dict(self):
        controls = self.find_all_controls()
        if controls:
            return _motion_core.ControlSetMotionOpt(self._namespace, controls).generate_motion_dict()
        return {}

    def generate_controls_pose_dict(self):
        controls = self.find_all_controls()
        if controls:
            return _motion_core.ControlSetMotionOpt(self._namespace, controls).generate_pose_dict()
        return {}

    def apply_controls_motion_dict(self, data, **kwargs):
        controls = self.find_all_controls()
        if controls:
            _motion_core.ControlSetMotionOpt(self._namespace, controls).apply_motion_dict(data, **kwargs)

    def apply_controls_pose_dict(self, data, **kwargs):
        controls = self.find_all_controls()
        if controls:
            _motion_core.ControlSetMotionOpt(self._namespace, controls).apply_pose_dict(data, **kwargs)
    
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

    # mirror and flip
    # mirror, do not mark undo, "ControlSetMotionOpt" is already using
    def mirror_controls_left_to_right(self, **kwargs):
        controls = self.find_all_controls()
        if controls:
            _motion_core.ControlSetMotionOpt(self._namespace, controls).mirror_all_left_to_right(**kwargs)

    # mirror, do not mark undo, "ControlSetMotionOpt" is already using
    def mirror_controls_middle(self, **kwargs):
        controls = self.find_all_controls()
        if controls:
            _motion_core.ControlSetMotionOpt(self._namespace, controls).mirror_all_middle(**kwargs)

    # mirror, do not mark undo, "ControlSetMotionOpt" is already using
    def mirror_controls_right_to_left(self, **kwargs):
        controls = self.find_all_controls()
        if controls:
            _motion_core.ControlSetMotionOpt(self._namespace, controls).mirror_all_right_to_left(**kwargs)

    # flip, do not mark undo, "ControlSetMotionOpt" is already using
    def flip_controls(self, **kwargs):
        controls = self.find_all_controls()
        if controls:
            _motion_core.ControlSetMotionOpt(self._namespace, controls).flip_all(**kwargs)

    # reset, do not mark undo, "ControlSetMotionOpt" is already using
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
            return _motion_core.ControlSetMotionOpt(self._namespace, controls).reset_transformation(**kwargs)
        return False

    def generate_controls_axis_vector_dict(self, **kwargs):
        controls = self.find_all_controls()

        if controls:
            return _motion_core.ControlSetMotionOpt(self._namespace, controls).generate_axis_vector_dict()
        return {}

    # joint
    def find_joint_set(self):
        """
        DeformSet：是ADV的默认设置
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
        Geometry：是ADV的默认设置
        """
        _ = cmds.ls('{}:Geometry'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_all_meshes(self):
        """
        默认忽略中间对象
        """
        _ = self.find_geometry_location()
        if _:
            return cmds.ls(
                _, type='mesh', long=1, noIntermediate=1, dag=1
            ) or []
        return []

    def find_geo_lower_location(self):
        """
        Low_Grp：ADV没有这个设置，这是个临时设置，后面会使用配置控制
        """
        _ = cmds.ls('{}:Low_Grp'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_all_lower_meshes(self):
        """
        默认忽略中间对象
        """
        _ = self.find_geo_lower_location()
        if _:
            return cmds.ls(
                _, type='mesh', long=1, noIntermediate=1, dag=1
            ) or []
        return []

    @_mya_core.Undo.execute
    def duplicate(self, **kwargs):
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
        _motion_core.ControlSetBake(controls).execute(*args, **kwargs)


class AdvChrOpt(AdvOpt):
    LOG_KEY = 'adv rig motion'

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

