# coding:utf-8
import json
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from . import control as _control


class AdvMotionOpt(object):

    @classmethod
    def to_control_key(cls, path):
        return path.split('|')[-1].split(':')[-1]
    
    def __init__(self, namespace):
        self._namespace = namespace

        self._root = qsm_mya_core.Namespace

    def find_control_set(self):
        _ = cmds.ls('{}:ControlSet'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_control(self, control_key):
        _ = cmds.ls('{}:{}'.format(self._namespace, control_key), long=1)
        if _:
            return _[0]

    def get_animations(self):
        dict_ = {}
        control_set = self.find_control_set()
        if control_set:
            control_paths = cmds.sets(control_set, query=1) or []
            if control_paths:
                # todo, dict order error if not use sort
                control_paths.sort()
                for i_path in control_paths:
                    i_control_opt = _control.ControlOpt(i_path)
                    i_motion = i_control_opt.get_animation()
                    i_key = self.to_control_key(i_path)
                    dict_[i_key] = i_motion
        return dict_

    def apply_animations(self, motions, **kwargs):
        for i_control_key, i_motion in motions.items():
            i_control_path = self.find_control(i_control_key)
            if i_control_path is not None:
                _control.ControlOpt(i_control_path).apply_animation(i_motion, **kwargs)

    def transfer_animations_to(self, namespace, **kwargs):
        motions = self.get_animations()
        self.__class__(namespace).apply_animations(
            motions, **kwargs
        )

    def get_animations_uuid(self):
        return bsc_core.UuidMtd.generate_by_hash_value(
            bsc_core.HashMtd.to_hash_key(self.get_animations())
        )

    def export_animations_to(self, file_path):
        bsc_storage.StgFileOpt(file_path).set_write(self.get_animations())

    def import_animations_from(self, file_path, **kwargs):
        self.apply_animations(
            bsc_storage.StgFileOpt(file_path).set_read(), **kwargs
        )
