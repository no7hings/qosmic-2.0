# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ..base import abc as _bsc_abc

from ..mocap import sketch_set as _mcp_sketch_set

from . import sketch_set as _sketch_set


class TransferResource(_bsc_abc.AbsMontage):
    def __init__(self, namespace):
        self._namespace = namespace

        self._sketch_set = _sketch_set.TransferSketchSet.generate(self._namespace)

    @classmethod
    def create_sketches(cls):
        _sketch_set.TransferSketchSet.create(
            cls.Namespaces.Transfer
        )

    @classmethod
    def find_mocap_namespaces(cls):
        return _mcp_sketch_set.MocapSketchSet.find_valid_namespaces()

    def find_root_location(self):
        _ = cmds.ls('|{}:*'.format(self._namespace, long=1))
        if _:
            return _[0]

    def get_root_height(self):
        # is a constant value now
        return self._sketch_set.DEFAULT_MASTER_LOWER_HEIGHT

    def get_height(self):
        return self._sketch_set.DEFAULT_MASTER_HEIGHT

    @classmethod
    def test(cls):
        pass

