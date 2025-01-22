# coding:utf-8
import math

import collections

import re

import _abc


class _Matrix:
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
        sy = math.sqrt(matrix[2][1]**2+matrix[2][2]**2)
        singular = sy < 1e-6

        if not singular:
            x = math.atan2(matrix[2][1], matrix[2][2])  # Roll
            y = math.atan2(-matrix[2][0], sy)  # Pitch
            z = math.atan2(matrix[1][0], matrix[0][0])  # Yaw
        else:
            x = math.atan2(-matrix[1][2], matrix[1][1])
            y = math.atan2(-matrix[2][0], sy)
            z = 0

        return [math.degrees(x), math.degrees(y), math.degrees(z)]

    @classmethod
    def extract_translate_and_rotate(cls, matrix):
        rotation_matrix = [row[:3] for row in matrix[:3]]
        translate = matrix[3]

        rotate = cls.rotation_matrix_to_euler_angles(rotation_matrix)
        return translate, rotate


class DotAcd(_abc.AbsDotfile):
    """
    CSF0f<0,1>(matrix3 [-0.8921042680740356,-0.02059752680361271,0.4513603150844574] [-0.04932306334376335,0.9974299073219299,-0.05196893587708473] [-0.4491298794746399,-0.06862417608499527,-0.8908274173736572] [-0.034841522574424744,23.60810089111328,0.007131293416023254])<0,2>(matrix3 [-0.04181754216551781,0.9971072673797607,0.06347089260816574] [0.35092809796333313,-0.044820912182331085,0.9353294372558594] [0.9354686141014099,0.06138698384165764,-0.34803855419158936])
    CSF1f<0,1>(matrix3 [-0.8921042680740356,-0.02059752680361271,0.4513603150844574] [-0.04932306334376335,0.9974299073219299,-0.05196893587708473] [-0.4491298794746399,-0.06862417608499527,-0.8908274173736572] [-0.034841522574424744,23.60810089111328,0.007131293416023254])<0,2>(matrix3 [-0.04181754216551781,0.9971072673797607,0.06347089260816574] [0.35092809796333313,-0.044820912182331085,0.9353294372558594] [0.9354686141014099,0.06138698384165764,-0.34803855419158936])
    """
    SEP = '\n'

    def __init__(self, *args, **kwargs):
        super(DotAcd, self).__init__(*args, **kwargs)

    def get_dict(self):
        dict_ = collections.OrderedDict()
        p_0_0 = r'CSF(\d+)f.*'
        p_0_1 = r'CSF(\d+)f(.*?)'+self.SEP
        p_0_1_0 = r'<(\d),(\d)>\(matrix3 (.*?)\)'

        p_1_0 = r'(\d+)f.*'
        p_1_1 = r'(\d+)f(.*?)'+self.SEP
        p_1_1_0 = r'<(\d),(\d)>\(matrix3 (.*?)\)\{(.*?)\}'

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
                            j_key = int(j_key_0), int(j_key_1)
                            j_matrix_str = j_data[2]
                            j_matrix = [
                                [float(y.strip()) for y in x.strip('[]').split(',')]
                                for x in j_matrix_str.split(' ')
                            ]
                            j_translate, j_rotate = _Matrix.extract_translate_and_rotate(
                                j_matrix
                            )
                            dict_.setdefault(
                                j_key, []
                            ).append(
                                (i_frame, j_translate, j_rotate)
                            )
            # todo: same data?
            # elif re.match(p_1_0, i_line, re.DOTALL):
            #     i_r_1_1 = re.search(p_1_1, i_line)
            #     if i_r_1_1:
            #         i_frame = i_r_1_1.group(1)
            #         i_data = i_r_1_1.group(2)
            #         i_r_1_1_0 = re.findall(p_1_1_0, i_data)
            #         if i_r_1_1_0:
            #             print i_r_1_1_0
        return dict_
