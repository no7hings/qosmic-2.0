# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.log as bsc_log

from ... import core as _mya_core

from . import control as _control


class AdvRigMotionOpt(object):
    KEY = 'adv rig motion'
    
    def __init__(self, namespace):
        self._namespace = namespace

    def find_control_set(self):
        _ = cmds.ls('{}:ControlSet'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_controls(self):
        _ = self.find_control_set()
        if _:
            return cmds.sets(_, query=1) or []
        return []

    def find_face_control_set(self):
        _ = cmds.ls('{}:FaceControlSet'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_face_controls(self):
        _ = self.find_face_control_set()
        if _:
            return cmds.sets(_, query=1) or []
        return []

    def find_all_controls(self):
        return self.find_controls() + self.find_face_controls()

    def find_control(self, control_key):
        _ = cmds.ls('{}:{}'.format(self._namespace, control_key), long=1)
        if _:
            return _[0]

    def find_main_control(self):
        return self.find_control('Main')

    def get_data(self, control_set_includes):
        controls = []
        if 'body' in control_set_includes:
            controls += self.find_controls()
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

        for i_control_key, i_motion in data.items():
            if control_key_excludes:
                if i_control_key in control_key_excludes:
                    continue

            i_control_path = self.find_control(i_control_key)
            if i_control_path is not None:
                _control.ControlMotionOpt(i_control_path).apply_data(i_motion, **kwargs)

    def transfer_to(self, namespace, **kwargs):
        motions = self.get_data(control_set_includes=['body', 'face'])
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

    def create_transformation_locator(self, root=None):
        main_control = self.find_main_control()
        if main_control is None:
            return

        self.create_transformation_locator_fnc(main_control, root)

    @classmethod
    def create_transformation_locator_fnc(cls, main_control, root=None):
        name = _mya_core.DagNode.to_name(main_control)

        locator_name = '{}_loc'.format(name)
        if root is not None:
            locator_path = '{}|{}'.format(root, locator_name)
        else:
            locator_path = '|{}'.format(locator_name)

        if cmds.objExists(locator_path) is False:
            locator_path = _mya_core.DagNode.create_locator(locator_path)

            w, h, d = _mya_core.Transform.get_dimension(main_control)
            locator_shape = _mya_core.Transform.get_shape(
                locator_path
            )
            _mya_core.NodeAttribute.set_as_tuple(
                locator_shape, 'localScale', (w/2, 0, d/2)
            )
            _mya_core.NodeDrawOverride.set_color(
                locator_path, (1.0, .0, .0)
            )
            _mya_core.NodeAttribute.create_as_string(
                locator_path, 'qsm_mark', 'move_locator'
            )

            _mya_core.ParentConstraint.create(
                main_control, locator_path
            )
            _mya_core.ParentConstraint.clear_all(locator_path)

            _control.ControlMotionOpt(main_control).create_transformation_locator(
                locator_path
            )

        return locator_path

    def remove_transformation_locator(self):
        main_control = self.find_main_control()
        if main_control is None:
            return

        self.remove_transformation_locator_fnc(main_control)

    @classmethod
    def remove_transformation_locator_fnc(cls, main_control):
        _control.ControlMotionOpt(main_control).remove_transformation_locator()


