# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ... import core as _mya_core


class AdvControl(object):
    @classmethod
    def find_control_set(cls, namespace):
        _ = cmds.ls('{}:ControlSet'.format(namespace), long=1)
        if _:
            return _[0]

    @classmethod
    def find_body_controls(cls, namespace):
        _ = cls.find_control_set(namespace)
        if _:
            return [_mya_core.DagNode.to_path(x) for x in cmds.sets(_, query=1) or []]
        return []

    @classmethod
    def find_face_control_set(cls, namespace):
        _ = cmds.ls('{}:FaceControlSet'.format(namespace), long=1)
        if _:
            return _[0]

    @classmethod
    def find_face_controls(cls, namespace):
        _ = cls.find_face_control_set(namespace)
        if _:
            return [_mya_core.DagNode.to_path(x) for x in cmds.sets(_, query=1) or []]
        return []

    @classmethod
    def find_all_controls(cls, namespace):
        return cls.find_body_controls(namespace)+cls.find_face_controls(namespace)


class AdvNamespaceExtra(object):
    def _init_namespace_extra(self, namespace):
        self._namespace = namespace

    @property
    def namespace(self):
        return self._namespace
    
    # control
    def find_one_control(self, control_key):
        _ = cmds.ls('{}:{}'.format(self._namespace, control_key), long=1)
        if _:
            return _[0]

    def find_many_controls(self, regex):
        return cmds.ls('{}:{}'.format(self._namespace, regex), long=1) or []

    def find_main_control(self):
        return self.find_one_control('Main')

    def find_control_set(self):
        """
        ControlSet
        """
        _ = cmds.ls('{}:ControlSet'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_all_controls(self):
        _ = self.find_control_set()
        if _:
            return [_mya_core.DagNode.to_path(x) for x in cmds.sets(_, query=1) or []]
        return []

    def find_all_curve_controls(self):
        list_ = []
        for i in self.find_all_controls():
            if _mya_core.Transform.check_is_transform(i) is True:
                i_shape = _mya_core.Transform.get_shape(i)
                if _mya_core.Node.is_curve(i_shape) is True:
                    list_.append(i)
        return list_

    def find_all_transform_controls(self):
        list_ = []
        for i in self.find_all_controls():
            if _mya_core.Transform.check_is_transform(i) is True:
                list_.append(i)
        return list_
