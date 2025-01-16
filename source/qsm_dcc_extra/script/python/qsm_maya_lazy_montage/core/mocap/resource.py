# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core

from . import sketch_set as _sketch_set


class MocapResource(object):
    @classmethod
    def check_is_valid(cls, namespace):
        _ = cmds.ls('{}:Hips'.format(namespace), long=1)
        if _:
            return True
        return False

    def __init__(self, namespace=None, location=None):
        if namespace is not None:
            self._sketch_location = _sketch_set.MocapSketchSet.find_valid_location(namespace)
        elif location is not None:
            self._sketch_location = location
        else:
            raise RuntimeError()

        if qsm_mya_core.Node.is_exists(self._sketch_location) is False:
            raise RuntimeError(
                'No valid location found.'
            )

        self._sketch_set = _sketch_set.MocapSketchSet.generate_by_location(self._sketch_location)

    def find_root_location(self):
        return self._sketch_location

    @property
    def sketch_set(self):
        return self._sketch_set

    def get_root_height(self):
        self._sketch_set.zero_out()
        return self._sketch_set.compute_root_height()

    def get_height(self):
        self._sketch_set.zero_out()
        return self._sketch_set.compute_height()

    def fit_scale_to_master_layer(self, master_layer):
        # source height
        root_height = self.get_root_height()
        master_lower_height = self._sketch_set.DEFAULT_MASTER_LOWER_HEIGHT

        scale = root_height/master_lower_height
        master_layer.apply_root_scale(scale)

    def constraint_from_master_layer(self, master_layer):
        self._sketch_set.constraint_from_master_layer(master_layer)

    def connect_from_master_layer(self, master_layer):
        self.fit_scale_to_master_layer(master_layer)
        self.constraint_from_master_layer(master_layer)

    def find_sketch(self, sketch_key):
        return self._sketch_set.find_one(sketch_key)

    def get_frame_range(self):
        return self._sketch_set.get_frame_range()


