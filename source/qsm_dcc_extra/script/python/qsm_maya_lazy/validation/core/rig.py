# coding:utf-8
import math

import collections
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.resource as bsc_resource

import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

import qsm_maya.core as qsm_mya_core


class VectorLocator(object):
    @classmethod
    def create(cls, path):
        name = qsm_mya_core.DagNode.to_name(path)
        t = qsm_mya_core.DagNode.create_transform(path)
        for i_key, i_vector in [
            ('X', (1, 0, 0)),
            ('Y', (0, 1, 0)),
            ('Z', (0, 0, 1))
        ]:
            i_shape = cmds.createNode('locator', name=name+i_key, parent=t, skipSelect=1)
            cmds.setAttr(i_shape+'.localPosition', *i_vector)
            cmds.setAttr(i_shape+'.localScale', *i_vector)
            qsm_mya_core.NodeDrawOverride.set_color(i_shape, i_vector)

    def __init__(self, path):
        pass


class RotateOrder(object):
    """
    kXYZ = 0
    kYZX = 1
    kZXY = 2
    kXZY = 3
    kYXZ = 4
    kZYX = 5
    """
    ORDERS = [
        'XYZ',
        'YZX',
        'ZXY',
        'XZY',
        'YXZ',
        'ZYX',
    ]

    @classmethod
    def to_string(cls, index):
        return '{}({})'.format(cls.ORDERS[index], index)

    @classmethod
    def to_index(cls, string):
        return cls.ORDERS.index(string)


class AxisVector(object):
    @classmethod
    def compute_angle(cls, vector_1, vector_2):
        """
        {
            'x_axis': [1.0, 0.0, 0.0],
            'y_axis': [0.0, 1.0, 0.0],
            'z_axis': [0.0, 0.0, 1.0]
        }
        OrderedDict(
            [
                ('x_axis', [0.0, 0.996, -0.085]),
                ('y_axis', [-0.0, 0.085, 0.996]),
                ('z_axis', [1.0, -0.0, 0.0])
            ]
        )
        """
        dot_product = sum(v1*v2 for v1, v2 in zip(vector_1, vector_2))
        magnitude_v1 = math.sqrt(sum(v**2 for v in vector_1))
        magnitude_v2 = math.sqrt(sum(v**2 for v in vector_2))
        cos_theta = dot_product/(magnitude_v1*magnitude_v2)
        cos_theta = max(min(cos_theta, 1.0), -1.0)
        theta_radians = math.acos(cos_theta)
        return round(math.degrees(theta_radians), 2)


class RigValidationBase(object):
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
