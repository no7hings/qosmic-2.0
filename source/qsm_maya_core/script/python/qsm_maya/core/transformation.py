# coding:utf-8
import math
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.api.OpenMaya as om2


class Rotation:
    ATR_NAMES = [
        'rotateX', 'rotateY', 'rotateZ'
    ]

    ATR_NAME_SET = set(
        ATR_NAMES
    )

    @classmethod
    def decompose(cls, rotation):
        return (
            math.degrees(rotation.x),
            math.degrees(rotation.y),
            math.degrees(rotation.z)
        )

    @classmethod
    def to_rotation(cls, rotate, rotate_order):
        return om2.MEulerRotation(
            om2.MVector(*[math.radians(x) for x in rotate]),
            rotate_order
        )


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

    @classmethod
    def generate_for(cls, path, world_space=1):
        """
        generate for mirror
        """
        dict_ = {}
        mtx = cmds.xform(path, matrix=1, worldSpace=world_space, query=1)
        # Rounding the values in the world matrix
        for i, i_value in enumerate(mtx):
            mtx[i] = round(i_value, 3)

        dict_['x_axis'] = mtx[0:3]
        dict_['y_axis'] = mtx[4:7]
        dict_['z_axis'] = mtx[8:11]
        return dict_

    @classmethod
    def generate_angle(cls, path):
        data_0 = {'y_axis': [0.0, 1.0, 0.0], 'x_axis': [1.0, 0.0, 0.0], 'z_axis': [0.0, 0.0, 1.0]}
        data_1 = cls.generate_for(path)
        x_axis, y_axis, z_axis = data_1['x_axis'], data_1['y_axis'], data_1['z_axis']
        x_axis_src, y_axis_src, z_axis_src = data_0['x_axis'], data_0['y_axis'], data_0['z_axis']
        x_angle = cls.compute_angle(x_axis_src, x_axis)
        y_angle = cls.compute_angle(y_axis_src, y_axis)
        z_angle = cls.compute_angle(z_axis_src, z_axis)
        return x_angle, y_angle, z_angle
