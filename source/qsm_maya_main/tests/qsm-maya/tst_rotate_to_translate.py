import maya.cmds as cmds
import math

# 初始平移和旋转
initial_translate = [0, 0, 0]
initial_rotate = [0, 45, 0]  # rotateY = 45 degrees

# 计算旋转矩阵
angle = math.radians(initial_rotate[1])  # 转换角度为弧度
cos_angle = math.cos(angle)
sin_angle = math.sin(angle)

# Y轴旋转矩阵
rotation_matrix = [
    [cos_angle, 0, sin_angle],
    [0, 1, 0],
    [-sin_angle, 0, cos_angle]
]

# 初始平移向量（沿Z轴）
translate_vector = [0, 0, 1]

# 计算新的平移向量
new_translate_vector = [
    rotation_matrix[0][0] * translate_vector[0] + rotation_matrix[0][1] * translate_vector[1] + rotation_matrix[0][2] * translate_vector[2],
    rotation_matrix[1][0] * translate_vector[0] + rotation_matrix[1][1] * translate_vector[1] + rotation_matrix[1][2] * translate_vector[2],
    rotation_matrix[2][0] * translate_vector[0] + rotation_matrix[2][1] * translate_vector[1] + rotation_matrix[2][2] * translate_vector[2]
]

# 从帧1到帧10设置关键帧
for frame in range(1, 11):
    cmds.currentTime(frame)
    new_translate = [initial_translate[0] + new_translate_vector[0] * frame,
                     initial_translate[1] + new_translate_vector[1] * frame,
                     initial_translate[2] + new_translate_vector[2] * frame]
    cmds.setAttr('yourObject.translate', new_translate[0], new_translate[1], new_translate[2])
    cmds.setKeyframe('yourObject', attribute='translate')
