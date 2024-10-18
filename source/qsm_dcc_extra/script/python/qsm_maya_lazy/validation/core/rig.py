# coding:utf-8
import math

import collections
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.resource as bsc_resource

import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

import qsm_maya.core as qsm_mya_core


class RigValidationBase(object):

    @classmethod
    def get_data_for(cls, path):
        return dict(
            rotate_order=cmds.getAttr(path+'.'+'rotateOrder'),
            axis_vector=qsm_mya_core.AxisVector.generate_for(path)
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


class RigValidationTemplate(RigValidationBase):
    def __init__(self, namespace):
        self._namespace = namespace
        self._adv_cfg = bsc_resource.RscExtendConfigure.get_as_content('rig/adv_validation')

    def generate(self, file_path):
        joint_dict = collections.OrderedDict()
        joint_keys = self._adv_cfg.get('joint')
        for i_joint_key in joint_keys:
            i_joint = self.find_one(self._namespace, i_joint_key, 'joint')
            if i_joint is not None:
                joint_dict[i_joint_key] = self.get_data_for(i_joint)

        control_dict = collections.OrderedDict()
        controls_keys = self._adv_cfg.get('control')
        for i_control_key in controls_keys:
            i_control = self.find_one(self._namespace, i_control_key, 'transform')
            if i_control is not None:
                control_dict[i_control_key] = self.get_data_for(i_control)

        dict_ = dict(
            joint=joint_dict,
            control=control_dict
        )

        bsc_storage.StgFileOpt(
            file_path
        ).set_write(dict_)

    @classmethod
    def test(cls):
        if qsm_gnl_core.scheme_is_release():
            cls('LuoFeng_XL_Skin').generate(
                'Y:/deploy/.configures/rig/adv_validation_template_new.yml'
            )
        else:
            cls('lily_Skin').generate(
                'E:/myworkspace/qosmic-2.0/source/qsm_dcc_extra/configures/rig/adv_validation_template.yml'
            )
