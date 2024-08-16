# coding:utf-8
import math

import os

import sys

import six

import collections
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.resource as bsc_resource

import lxbasic.content as bsc_content

import lxbasic.storage as bsc_storage

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxgui.core as gui_core

import qsm_general.core as qsm_gnl_core

import qsm_maya.core as qsm_mya_core

from .. import process as _process


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
    """
import qsm_maya_lazy
qsm_maya_lazy.do_reload()

import qsm_maya_lazy.validation as c

c.RigValidationTemplate.test()
    """

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
        if qsm_gnl_core.scheme_is_new():
            cls('LuoFeng_XL_Skin').generate(
                'Y:/deploy/.configures/rig/adv_validation_template_new.yml'
            )
        else:
            cls('lily_Skin').generate(
                'E:/myworkspace/qosmic-2.0/source/qsm_dcc_extra/configures/rig/adv_validation_template.yml'
            )


class RigValidationOpt(RigValidationBase):
    """
import qsm_maya_lazy
qsm_maya_lazy.do_reload()

import qsm_maya_lazy.validation as c

c.RigValidationOpt.test()

    """
    def __init__(self, namespace):
        self._namespace = namespace
        self._file_path = qsm_mya_core.ReferenceNamespacesCache().get_file(namespace)

        self._adv_cfg = bsc_resource.RscExtendConfigure.get_as_content('rig/adv_validation')
        if qsm_gnl_core.scheme_is_new():
            self._template_cfg = bsc_resource.RscExtendConfigure.get_as_content('rig/adv_validation_template_new')
        else:
            self._template_cfg = bsc_resource.RscExtendConfigure.get_as_content('rig/adv_validation_template')

        self._result_content = bsc_content.Dict()

        self._validation_options = qsm_gnl_core.DccValidationOptions('rig/adv_validation_options')

        self._language = bsc_core.EnvBaseMtd.get_ui_language()

        self._kwargs = dict(
            namespace=self._namespace,
            result_content=self._result_content,
            validation_options=self._validation_options
        )

        self._joint_data = {}
        self._control_data = {}

    def update_options(self, options):
        pass

    def execute(self, cache_file_path=None):
        process_options = self._validation_options.generate_process_options()
        with bsc_log.LogProcessContext.create(maximum=len(process_options)) as l_p:
            for i_branch, i_leafs in process_options.items():
                if i_branch == 'joint':
                    self.joints_prc(i_branch, i_leafs)
                elif i_branch == 'control':
                    self.controls_prc(i_branch, i_leafs)
                elif i_branch == 'mesh':
                    self.meshes_prc(i_branch, i_leafs)

                l_p.do_update()

        results = self._result_content.value
        data = dict(
            file=self._file_path,
            results=results
        )
        if cache_file_path is not None:
            bsc_storage.StgFileOpt(cache_file_path).set_write(data)

        sys.stdout.write(
            bsc_core.auto_unicode(
                self._validation_options.to_text(data)
            )+'\n'
        )

    def joints_prc(self, branch, leafs):
        self.update_joint_data_map()
        for i_name, (i_main_key, i_data) in self._joint_data.items():
            self.joint_prc(branch, leafs, i_main_key, i_name, i_data)

        if 'name_overlapping' in leafs:
            _process.JointNameOverlapping(
                **self._kwargs
            ).execute()

        if 'completeness' in leafs:
            _process.JointCompleteness(
                **self._kwargs
            ).execute()

    def joint_prc(self, branch, leafs, main_key, name, data):
        if 'rotate_order' in leafs:
            self.rotate_order_prc(branch, main_key, name, data)
        if 'axis_vector' in leafs:
            self.axis_vector_prc(branch, 'axis_vector', main_key, name, data)

    def update_joint_data_map(self):
        self._joint_data.clear()
        joint_keys = self._adv_cfg.get('joint')
        for i_main_key in joint_keys:
            i_joints = self.find_many(self._namespace, i_main_key, 'joint')
            for j_joint in i_joints:
                j_name = self.to_key(j_joint)
                j_data = self.get_data_for(j_joint)
                self._joint_data[j_name] = (i_main_key, j_data)

    def controls_prc(self, branch, leafs):
        self.update_control_data_map()
        for i_name, (i_main_key, i_data) in self._control_data.items():
            self.control_prc(branch, leafs, i_main_key, i_name, i_data)

        if 'name_overlapping' in leafs:
            _process.ControlNameOverlapping(
                **self._kwargs
            ).execute()

        if 'reset_transformations' in leafs:
            _process.ControlResetTransformations(
                **self._kwargs
            ).execute()

    def update_control_data_map(self):
        self._control_data.clear()
        controls_keys = self._adv_cfg.get('control')
        for i_main_key in controls_keys:
            i_controls = self.find_many(self._namespace, i_main_key, 'transform')
            for j_control in i_controls:
                j_name = self.to_key(j_control)
                j_data = self.get_data_for(j_control)
                self._control_data[j_name] = (i_main_key, j_data)

    def control_prc(self, branch, leafs, main_key, name, data):
        if 'rotate_order' in leafs:
            self.rotate_order_prc(branch, main_key, name, data)
        if 'axis_vector' in leafs:
            self.axis_vector_prc(branch, 'axis_vector', main_key, name, data)

    def meshes_prc(self, branch, leafs):
        if 'face_count' in leafs:
            _process.MeshFaceCount(
                **self._kwargs
            ).execute()

    def rotate_order_prc(self, branch, main_key, name, data):
        data_key = 'rotate_order'
        key = '{}.{}'.format(branch, data_key)
        value = data[data_key]
        value_src = self._template_cfg.get('{}.{}.{}'.format(branch, main_key, data_key))
        if value_src is not None:
            if value != value_src:
                description_kwargs = dict(
                    value=RotateOrder.to_string(value), value_src=RotateOrder.to_string(value_src)
                )
                self._result_content.add_element(
                    key, (name, [description_kwargs])
                )

    def axis_vector_prc(self, branch, leaf, main_key, name, data):
        data_key = 'axis_vector'
        key = '{}.{}'.format(branch, data_key)
        value = data[data_key]
        options = self._validation_options.get_leaf_options_at(branch, leaf)
        limit_value = options['limit_value']
        value_src = self._template_cfg.get('{}.{}.{}'.format(branch, main_key, data_key))
        if value_src is not None:
            x_axis, y_axis, z_axis = value['x_axis'], value['y_axis'], value['z_axis']
            x_axis_src, y_axis_src, z_axis_src = value_src['x_axis'], value_src['y_axis'], value_src['z_axis']
            x_angle = AxisVector.compute_angle(x_axis_src, x_axis)
            description_kwargs_list = []
            if x_angle > limit_value:
                description_kwargs_x = dict(axis='X', angle=x_angle)
                description_kwargs_list.append(description_kwargs_x)
            y_angle = AxisVector.compute_angle(y_axis_src, y_axis)
            if y_angle > limit_value:
                description_kwargs_y = dict(axis='Y', angle=y_angle)
                description_kwargs_list.append(description_kwargs_y)
            z_angle = AxisVector.compute_angle(z_axis_src, z_axis)
            if z_angle > limit_value:
                description_kwargs_z = dict(axis='Z', angle=z_angle)
                description_kwargs_list.append(description_kwargs_z)
            if description_kwargs_list:
                self._result_content.add_element(
                    key, (name, description_kwargs_list)
                )

    @classmethod
    def test(cls):
        cls('lily_Skin').execute()


class RigValidationProcess(object):
    def __init__(self, file_path, cache_file_path, process_options):
        self._file_path = file_path
        self._cache_file_path = cache_file_path
        self._process_options = process_options
        self._namespace = 'rig_validation'

    def execute(self):
        with bsc_log.LogProcessContext.create(maximum=4) as l_p:
            # step 1
            qsm_mya_core.SceneFile.new()
            l_p.do_update()
            # step 2
            if os.path.isfile(self._file_path) is False:
                raise RuntimeError()
            qsm_mya_core.SceneFile.reference_file(
                self._file_path, namespace=self._namespace
            )
            l_p.do_update()
            # step 3
            RigValidationOpt(self._namespace).execute(self._cache_file_path)
            l_p.do_update()
