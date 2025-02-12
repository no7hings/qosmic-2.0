# coding:utf-8
import math

import collections

import re

try:
    import numpy as np
except ImportError:
    pass

from . import abc_


class _Matrix:
    Y2Z = [
        [1, 0, 0],
        [0, 0, 1],
        [0, -1, 0]
    ]

    Z2Y = [
        [1, 0, 0],
        [0, 0, -1],
        [0, 1, 0]
    ]

    @staticmethod
    def rotate_x(angle_deg):
        angle_rad = np.radians(angle_deg)
        return np.array([
            [1, 0, 0],
            [0, np.cos(angle_rad), -np.sin(angle_rad)],
            [0, np.sin(angle_rad), np.cos(angle_rad)]
        ])

    @staticmethod
    def rotate_y(angle_deg):
        angle_rad = np.radians(angle_deg)
        return np.array([
            [np.cos(angle_rad), 0, np.sin(angle_rad)],
            [0, 1, 0],
            [-np.sin(angle_rad), 0, np.cos(angle_rad)]
        ])

    @staticmethod
    def rotate_z(angle_deg):
        angle_rad = np.radians(angle_deg)
        return np.array([
            [np.cos(angle_rad), -np.sin(angle_rad), 0],
            [np.sin(angle_rad), np.cos(angle_rad), 0],
            [0, 0, 1]
        ])

    @classmethod
    def fix_fnc(cls, matrix):
        r_initial = matrix

        r_correction = np.transpose(r_initial)

        result = np.dot(r_correction, r_initial)
        return result

    @classmethod
    def rotation_matrix_to_euler_angles(cls, matrix):
        """
        sy = math.sqrt(matrix[0][0] * matrix[0][0] + matrix[1][0] * matrix[1][0])
        singular = sy < 1e-6

        if not singular:
            x = math.atan2(matrix[2][1], matrix[2][2])  # Roll
            y = math.atan2(-matrix[2][0], sy)          # Pitch
            z = math.atan2(matrix[1][0], matrix[0][0]) # Yaw
        else:
            x = math.atan2(-matrix[1][2], matrix[1][1])
            y = math.atan2(-matrix[2][0], sy)
            z = 0

        return [math.degrees(z), math.degrees(y), math.degrees(x)]
        """
        rotate_matrix = matrix[:3]
        rotate_matrix.reverse()
        rotate_matrix[0][0] = -rotate_matrix[0][0]
        # rotate_matrix = cls.rotate_x_fnc(rotate_matrix, 90)
        # rotate_matrix = cls.rotate_y_fnc(rotate_matrix, -90)
        # rotate_matrix = cls.rotate_z_fnc(rotate_matrix, 90)

        sy = math.sqrt(rotate_matrix[2][2]**2+rotate_matrix[2][1]**2)
        singular = sy < 1e-6

        if not singular:
            x = math.atan2(-rotate_matrix[2][1], rotate_matrix[2][2])  # Roll
            y = math.atan2(rotate_matrix[2][0], sy)  # Pitch
            z = math.atan2(-rotate_matrix[1][0], rotate_matrix[0][0])  # Yaw
        else:
            x = math.atan2(-rotate_matrix[1][2], rotate_matrix[1][1])
            y = math.atan2(rotate_matrix[2][0], sy)
            z = 0
        return [math.degrees(x), math.degrees(y), math.degrees(z)]

    @classmethod
    def extract_translate_and_rotate(cls, matrix):
        rotation_matrix = [row[:3] for row in matrix[:3]]
        translate = matrix[3][:3]

        rotate = cls.rotation_matrix_to_euler_angles(rotation_matrix)
        return translate, rotate

    @classmethod
    def transform_matrix_to_new_basis(cls, matrix, basis):
        return list(np.dot(basis, np.array(matrix)).tolist())

    @classmethod
    def rotate_x_fnc(cls, matrix, angle_deg):
        return np.dot(cls.rotate_x(angle_deg), matrix)

    @classmethod
    def rotate_y_fnc(cls, matrix, angle_deg):
        return np.dot(cls.rotate_y(angle_deg), matrix)

    @classmethod
    def rotate_z_fnc(cls, matrix, angle_deg):
        return np.dot(cls.rotate_z(angle_deg), matrix)


class DotAcd(abc_.AbsDotfile):
    SEP = '\n'

    def __init__(self, *args, **kwargs):
        super(DotAcd, self).__init__(*args, **kwargs)

    def get_dict(self):
        dict_ = collections.OrderedDict()
        p_0_0 = r'CSF(\d+)f.*'
        p_0_1 = r'CSF(\d+)f(.*?)'+self.SEP
        p_0_1_0 = r'<(\d+),(\d+)>\(matrix3 (.*?)\)'
        p_0_1_1 = r'\[(.*?)\]'

        p_1_0 = r'(\d+)f.*'
        p_1_1 = r'(\d+)f(.*?)'+self.SEP
        p_1_1_0 = r'<(\d+),(\d+)>\(matrix3 (.*?)\)\{(.*?)\}'

        for i_idx, i_line in enumerate(self._lines):
            if re.match(p_0_0, i_line, re.DOTALL):
                i_r_0_1 = re.search(p_0_1, i_line)
                if i_r_0_1:
                    i_frame = int(i_r_0_1.group(1))
                    i_data = i_r_0_1.group(2)
                    i_r_0_1_0 = re.findall(p_0_1_0, i_data)
                    if i_r_0_1_0:
                        for j_data in i_r_0_1_0:
                            j_key_0, j_key_1 = j_data[:2]
                            j_key = '{}_{}'.format(j_key_0, j_key_1)
                            j_matrix_str = j_data[2]
                            i_r_0_1_1 = re.findall(p_0_1_1, j_matrix_str)
                            if len(i_r_0_1_1) != 4:
                                raise RuntimeError()

                            j_matrix = [[float(y.strip()) for y in x.split(',')] for x in i_r_0_1_1]

                            j_translate, j_rotate = _Matrix.extract_translate_and_rotate(
                                j_matrix
                            )
                            dict_.setdefault(
                                j_key, []
                            ).append(
                                (i_frame, j_matrix, j_translate, j_rotate)
                            )
            # todo: same data?
            # elif re.match(p_1_0, i_line, re.DOTALL):
            #     i_r_1_1 = re.search(p_1_1, i_line)
            #     if i_r_1_1:
            #         i_frame = i_r_1_1.group(1)
            #         i_data = i_r_1_1.group(2)
            #         i_r_1_1_0 = re.findall(p_1_1_0, i_data)
            #         if i_r_1_1_0:
            #             print(i_r_1_1_0)
        return dict_
