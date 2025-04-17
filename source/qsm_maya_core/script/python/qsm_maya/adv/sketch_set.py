# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from .. import core as _mya_core


class AdvSketchSet(object):

    @classmethod
    def find_root_location(cls, namespace):
        _ = cmds.ls('{}:DeformationSystem'.format(namespace), long=1)
        if _:
            return _[0]

    @classmethod
    def find_sketches(cls, namespace):
        _ = cls.find_root_location(namespace)
        # print(namespace, _, 'AAAA')
        if _:
            return cmds.ls(_, type='joint', long=1, dag=1) or []
        return []

    @classmethod
    def generate(cls, namespace):
        return cls(
            cls.find_sketches(namespace)
        )

    def __init__(self, paths):
        super(AdvSketchSet, self).__init__()

        self._paths = paths
        self._namespace = _mya_core.DagNode.extract_namespace(self._paths[0])

        self._cache_dict = {}
        self._cache_all()

    def _cache_all(self):
        self._cache_dict.clear()

        for i_path in self._paths:
            i_sketch_key = _mya_core.DagNode.to_name_without_namespace(i_path)
            self._cache_dict[i_sketch_key] = i_path

    def get(self, sketch_key):
        return self._cache_dict.get(sketch_key)

    def get_all(self):
        return self._cache_dict.values()
