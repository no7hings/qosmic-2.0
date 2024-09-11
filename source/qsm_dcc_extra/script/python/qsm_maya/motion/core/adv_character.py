# coding:utf-8
import re

# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.log as bsc_log

import qsm_general.core as qsm_gnl_core

from ... import core as _mya_core

from . import control as _control


class AdvCharacterMotionOpt(object):
    KEY = 'adv rig motion'
    
    def __init__(self, namespace):
        self._namespace = namespace

    def find_control_set(self):
        """
        ControlSet
        """
        _ = cmds.ls('{}:ControlSet'.format(self._namespace), long=1)
        if _:
            return _[0]

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
        return self.find_body_controls() + self.find_face_controls()

    def find_all_curve_controls(self):
        list_ = []
        for i in self.find_all_controls():
            if _mya_core.Transform.check_is_transform(i) is True:
                i_shape = _mya_core.Transform.get_shape(i)
                if _mya_core.Node.is_curve(i_shape) is True:
                    list_.append(i)
        return list_

    def find_one_control(self, control_key):
        _ = cmds.ls('{}:{}'.format(self._namespace, control_key), long=1)
        if _:
            return _[0]
    
    def find_many_controls(self, regex):
        return cmds.ls('{}:{}'.format(self._namespace, regex), long=1) or []

    def find_main_control(self):
        return self.find_one_control('Main')

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

    def find_joint_set(self):
        """
        DeformSet
        """
        _ = cmds.ls('{}:DeformSet'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_all_joints(self):
        _ = self.find_joint_set()
        if _:
            return [_mya_core.DagNode.to_path(x) for x in cmds.sets(_, query=1) or []]
        return []

    def find_geometry_location(self):
        """
        Geometry
        """
        _ = cmds.ls('{}:Geometry'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_all_meshes(self):
        _ = self.find_geometry_location()
        if _:
            return cmds.ls(
                _, type='mesh', long=1, noIntermediate=1, dag=1
            )

    def get_data(self, control_set_includes):
        controls = []
        if 'body' in control_set_includes:
            controls += self.find_body_controls()
        if 'face' in control_set_includes:
            controls += self.find_face_controls()

        if controls:
            # todo, dict order error if not use sort
            controls.sort()
            return _control.ControlsMotionOpt(self._namespace, controls).get_data()
        return {}

    @_mya_core.Undo.execute
    def apply_data(self, data, **kwargs):
        bsc_log.Log.trace_method_result(
            self.KEY,
            'apply data: "{}"'.format(', '.join(['{}={}'.format(k, v) for k, v in kwargs.items()]))
        )

        control_key_excludes = kwargs.pop('control_key_excludes') if 'control_key_excludes' in kwargs else None

        with bsc_log.LogProcessContext.create(maximum=len(data)) as l_p:
            for i_control_key, i_motion in data.items():
                if control_key_excludes:
                    if i_control_key in control_key_excludes:
                        continue

                i_control_path = self.find_one_control(i_control_key)
                if i_control_path is not None:
                    _control.ControlMotionOpt(i_control_path).apply_data(i_motion, **kwargs)

                l_p.do_update()

    def transfer_to(self, namespace, **kwargs):
        if 'control_set_includes' in kwargs:
            control_set_includes = kwargs.pop('control_set_includes')
        else:
            control_set_includes = ['body', 'face']

        motions = self.get_data(control_set_includes)
        self.__class__(namespace).apply_data(
            motions, **kwargs
        )

    def get_data_as_uuid(self):
        return bsc_core.BscUuid.generate_by_hash_value(
            bsc_core.BscHash.to_hash_key(
                self.get_data(control_set_includes=['body', 'face'])
            )
        )

    def export_to(self, file_path, control_set_includes):
        bsc_storage.StgFileOpt(file_path).set_write(self.get_data(control_set_includes))

    def load_from(self, file_path, **kwargs):
        self.apply_data(
            bsc_storage.StgFileOpt(file_path).set_read(), **kwargs
        )

    def find_all_anm_curves(self):
        controls = self.find_all_controls()
        return _mya_core.AnimCurves.get_all_from(controls)

    # do not mark undo, "ControlsMotionOpt" is already using
    def mirror_left_to_right(self, control_set_includes, **kwargs):
        controls = []
        if 'body' in control_set_includes:
            controls += self.find_body_controls()
        if 'face' in control_set_includes:
            controls += self.find_face_controls()

        if controls:
            _control.ControlsMotionOpt(self._namespace, controls).mirror_left_to_right(**kwargs)

    # do not mark undo, "ControlsMotionOpt" is already using
    def mirror_middle(self, control_set_includes, **kwargs):
        controls = []
        if 'body' in control_set_includes:
            controls += self.find_body_controls()
        if 'face' in control_set_includes:
            controls += self.find_face_controls()

        if controls:
            _control.ControlsMotionOpt(self._namespace, controls).mirror_middle(**kwargs)

    # do not mark undo, "ControlsMotionOpt" is already using
    def mirror_right_to_left(self, control_set_includes, **kwargs):
        controls = []
        if 'body' in control_set_includes:
            controls += self.find_body_controls()
        if 'face' in control_set_includes:
            controls += self.find_face_controls()

        if controls:
            _control.ControlsMotionOpt(self._namespace, controls).mirror_right_to_left(**kwargs)

    # do not mark undo, "ControlsMotionOpt" is already using
    def flip(self, control_set_includes, **kwargs):
        controls = []
        if 'body' in control_set_includes:
            controls += self.find_body_controls()
        if 'face' in control_set_includes:
            controls += self.find_face_controls()

        if controls:
            _control.ControlsMotionOpt(self._namespace, controls).flip(**kwargs)

    @_mya_core.Undo.execute
    def duplicate(self, **kwargs):
        namespace_new = _mya_core.Reference.duplicate(
            _mya_core.ReferenceNamespacesCache().get(self._namespace)
        )
        self.transfer_to(
            namespace_new, **kwargs
        )
        _mya_core.Selection.set(
            self.__class__(namespace_new).find_main_control()
        )

    @_mya_core.Undo.execute
    def bake_all_controls(self, *args, **kwargs):
        controls = self.find_all_curve_controls()
        _control.ControlsBake(controls).execute(*args, **kwargs)


class AdvCharacterMotionSystemOpt(object):
    @classmethod
    def find_control_keys_fnc(cls, root):
        key_set = set()
        if root:
            curves = cmds.ls(root, dag=1, type='nurbsCurve', long=1) or []
            for i_shape in curves:
                i_transform = _mya_core.Shape.get_transform(i_shape)
                i_name = _mya_core.DagNode.to_name_without_namespace(i_transform)
                i_key = re.sub(r'\d+', '*', i_name)
                key_set.add(i_key)

        if key_set:
            keys = list(key_set)
            keys.sort()
            return keys
        return []

    def __init__(self, namespace):
        self._namespace = namespace

    def find_body_root(self):
        _ = cmds.ls('{}:MotionSystem'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_face_root(self):
        _ = cmds.ls('{}:FaceGroup'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_body_all_control_keys(self):
        return self.find_control_keys_fnc(self.find_body_root())

    def find_face_all_control_keys(self):
        return self.find_control_keys_fnc(self.find_face_root())

    def find_all_control_keys(self):
        return self.find_body_all_control_keys()+self.find_face_all_control_keys()
    
    def test(self):
        k_0 = qsm_gnl_core.AdvCharacterControlConfigure().get_all_curve_control_keys()
        k_1 = self.find_body_all_control_keys()

        print set(k_1) - set(k_0)


