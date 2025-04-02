# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from .. import core as _mya_core


class AdvControlSet(object):

    @classmethod
    def find_set(cls, namespace):
        _ = cmds.ls('{}:ControlSet'.format(namespace), long=1)
        if _:
            return _[0]

    @classmethod
    def find_controls(cls, namespace):
        _ = cls.find_set(namespace)
        if _:
            return [_mya_core.DagNode.to_path(x) for x in cmds.sets(_, query=1) or []]
        return []

    @classmethod
    def generate(cls, namespace):
        return cls(
            cls.find_controls(namespace)
        )

    def __init__(self, paths):
        super(AdvControlSet, self).__init__()

        self._paths = paths
        self._namespace = _mya_core.DagNode.extract_namespace(self._paths[0])

        self._cache_dict = {}
        self._cache_all()

    def _cache_all(self):
        self._cache_dict.clear()

        for i_path in self._paths:
            i_control_key = _mya_core.DagNode.to_name_without_namespace(i_path)
            self._cache_dict[i_control_key] = i_path

    def get(self, control_key):
        return self._cache_dict.get(control_key)

    def get_all(self):
        return list(self._cache_dict.values())


class AdvChrControlSet(AdvControlSet):
    @classmethod
    def find_face_set(cls, namespace):
        _ = cmds.ls('{}:FaceControlSet'.format(namespace), long=1)
        if _:
            return _[0]

    @classmethod
    def find_controls(cls, namespace):
        sets = filter(None, [cls.find_set(namespace), cls.find_face_set(namespace)])
        list_ = []
        for i in sets:
            list_.extend(
                [_mya_core.DagNode.to_path(x) for x in cmds.sets(i, query=1) or []]
            )
        return list_

    def __init__(self, *args, **kwargs):
        super(AdvChrControlSet, self).__init__(*args, **kwargs)
