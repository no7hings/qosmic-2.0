# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core

from . import sketch_set as _sketch_set


class MocapResource(object):
    def __init__(self, namespace):
        self._namespace = namespace

        self._sketch_set = _sketch_set.MocapSketchSet.generate(self._namespace)

    def find_root(self):
        _ = cmds.ls('|{}:*'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_root_location(self):
        _ = cmds.ls('|{}:*'.format(self._namespace), long=1)
        if _:
            return _[0]

    @property
    def sketch_set(self):
        return self._sketch_set

    def get_root_height(self):
        self._sketch_set.zero_out()
        return self._sketch_set.compute_root_height()

    def get_height(self):
        self._sketch_set.zero_out()
        return self._sketch_set.compute_height()

    def fit_master_layer_scale(self, master_layer):
        # source height
        root_height = self.get_root_height()
        master_lower_height = self._sketch_set.DEFAULT_MASTER_LOWER_HEIGHT

        scale = root_height/master_lower_height
        master_layer.apply_root_scale(scale)

    def constraint_from_master_layer(self, master_layer):
        self._sketch_set.constraint_from_master_layer(master_layer)

    def connect_from_master_layer(self, master_layer):
        self.fit_master_layer_scale(master_layer)
        self.constraint_from_master_layer(master_layer)

    def find_sketch(self, sketch_key):
        return self._sketch_set.find_one(sketch_key)

    def get_frame_range(self):
        return self._sketch_set.get_frame_range()


