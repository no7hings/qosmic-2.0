# coding:utf-8
import math
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class RotateToTranslate(object):
    class Axis:
        X = 'x'
        Y = 'y'
        Z = 'z'

    @classmethod
    def get_rotate_axis_z(cls, vector):
        x, y, z = vector
        angle_radians = math.atan2(x, z)

        angle_degrees = math.degrees(angle_radians)
        return angle_degrees

    def __init__(self, path):
        self._path = path

    def get_vector_for(self, axis='z'):
        world_mat = cmds.xform(self._path, matrix=True, worldSpace=True, query=True)
        if axis == 'x':
            return world_mat[0:3]
        elif axis == 'y':
            return world_mat[4:7]
        elif axis == 'z':
            return world_mat[8:11]

    def get_translate(self):
        return cmds.xform(self._path, translation=1, worldSpace=0, query=1)

    def move_by_rotate_y(self, rotate_y):
        initial_translate = self.get_translate()
        initial_rotate = [0, rotate_y, 0]

        angle = math.radians(initial_rotate[1])
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)

        rotation_matrix = [
            [cos_angle, 0, sin_angle],
            [0, 1, 0],
            [-sin_angle, 0, cos_angle]
        ]

        translate_vector = [0, 0, 1]

        new_translate_vector = [
            rotation_matrix[0][0]*translate_vector[0]+rotation_matrix[0][1]*translate_vector[1]+rotation_matrix[0][2]*
            translate_vector[2],
            rotation_matrix[1][0]*translate_vector[0]+rotation_matrix[1][1]*translate_vector[1]+rotation_matrix[1][2]*
            translate_vector[2],
            rotation_matrix[2][0]*translate_vector[0]+rotation_matrix[2][1]*translate_vector[1]+rotation_matrix[2][2]*
            translate_vector[2]
        ]

        for frame in range(1, 11):
            cmds.currentTime(frame)
            new_translate = [
                initial_translate[0]+new_translate_vector[0]*frame,
                initial_translate[1]+new_translate_vector[1]*frame,
                initial_translate[2]+new_translate_vector[2]*frame
            ]
            cmds.setAttr(
                '{}.translate'.format(self._path), new_translate[0], new_translate[1], new_translate[2]
            )
            cmds.setKeyframe(
                self._path, attribute='translate'
            )

