# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import sketch as _sketch


class MixamoResource(object):
    def __init__(self, namespace):
        self._namespace = namespace
        self._sketch_set = _sketch.MixamoSketchSet.generate(self._namespace)

    @property
    def sketch_set(self):
        return self._sketch_set

    def get_root_height(self):
        self._sketch_set.zero_out()
        return self._sketch_set.compute_root_height()


