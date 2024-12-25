# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import sketch_set as _sketch_set


class MixamoResource(object):
    def __init__(self, namespace):
        self._namespace = namespace
        self._sketch_set = _sketch_set.MixamoSketchSet.generate(self._namespace)

    def get_root(self):
        _ = cmds.ls('|{}:*'.format(self._namespace), long=1)
        if _:
            return _[0]

    @property
    def sketch_set(self):
        return self._sketch_set

    def get_root_height(self):
        self._sketch_set.zero_out()
        return self._sketch_set.compute_root_height()

    def fit_master_layer_scale(self, layer):
        root_height = self.get_root_height()
        master_root_height = self._sketch_set.DEFAULT_MASTER_ROOT_HEIGHT
        scale = root_height/master_root_height
        layer.apply_root_scale(scale)

    def connect_from_master_layer(self, layer):
        self._sketch_set.connect_from_master_layer(layer)


