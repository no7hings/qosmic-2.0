# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.resource as bsc_resource

import qsm_maya.core as qsm_mya_core

import qsm_maya.motion.core as qsm_mya_mtn_core


class AdvValidationBase(object):
    BRANCH = None
    LEAF = None

    def __init__(self, namespace, result_content, validation_options):
        self._key = '{}.{}'.format(self.BRANCH, self.LEAF)
        self._namespace = namespace
        self._adv_cfg = bsc_resource.RscExtendConfigure.get_as_content('rig/adv_validation')
        self._result_content = result_content
        self._validation_options = validation_options

    def find_all_controls(self):
        return qsm_mya_mtn_core.AdvCharacterMotionOpt(self._namespace).find_all_controls()

    def find_all_joints(self):
        return qsm_mya_mtn_core.AdvCharacterMotionOpt(self._namespace).find_all_joints()

    def find_all_meshes(self):
        return qsm_mya_mtn_core.AdvCharacterMotionOpt(self._namespace).find_all_meshes()

    @classmethod
    def get_axis_vector(cls, path):
        dict_ = {}

        world_mat = cmds.xform(path, matrix=1, worldSpace=1, query=1)
        # Rounding the values in the world matrix
        for i, value in enumerate(world_mat):
            rounded_value = round(value, 3)
            world_mat[i] = rounded_value

        dict_['x_axis'] = world_mat[0:3]
        dict_['y_axis'] = world_mat[4:7]
        dict_['z_axis'] = world_mat[8:11]
        return dict_

    @classmethod
    def get_data_for(cls, path):
        return dict(
            rotate_order=cmds.getAttr(path+'.'+'rotateOrder'),
            axis_vector=cls.get_axis_vector(path)
        )

    @classmethod
    def to_key(cls, path):
        return qsm_mya_core.DagNode.to_name_without_namespace(path)

    @classmethod
    def find_many(cls, namespace, key, type_name):
        return cmds.ls('{}:{}'.format(namespace, key), type=type_name, long=1) or []

    @classmethod
    def find_one(cls, namespace, key, type_name):
        _ = cmds.ls('{}:{}'.format(namespace, key), type=type_name, long=1)
        if _:
            return _[0]
