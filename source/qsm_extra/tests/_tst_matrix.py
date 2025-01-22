# coding:utf-8
import math
import numpy as np

def normalize_angle(angle):
    """Normalize angle to [-180, 180]."""
    return (angle + 180) % 360 - 180

def rotation_matrix_to_euler_angles_xyz(matrix):
    sy = math.sqrt(matrix[2][2] ** 2 + matrix[2][1] ** 2)
    singular = sy < 1e-6

    if not singular:
        x = math.atan2(-matrix[2][1], matrix[2][2])  # Roll
        y = math.atan2(matrix[2][0], sy)             # Pitch
        z = math.atan2(-matrix[1][0], matrix[0][0])  # Yaw
    else:
        x = math.atan2(-matrix[1][2], matrix[1][1])
        y = math.atan2(matrix[2][0], sy)
        z = 0

    return [normalize_angle(math.degrees(x)), normalize_angle(math.degrees(y)), normalize_angle(math.degrees(z))]

def transform_matrix_to_new_basis(matrix, basis):
    """将矩阵转换到新坐标系中."""
    return np.dot(basis, np.array(matrix)).tolist()

# 输入旋转矩阵 (Y 轴向上)
# rotation_matrix = [
#     [0.7071067811865475, 0.0, -0.7071067811865476],
#     [0.0, 1.0, 0.0],
#     [0.7071067811865476, 0.0, 0.7071067811865475]
# ]

rotation_matrix = [
    [
        -0.8921042680740356, -0.02059752680361271, 0.4513603150844574
    ],
    [
        -0.04932306334376335, 0.9974299073219299, -0.05196893587708473
    ],
    [
        -0.4491298794746399, -0.06862417608499527, -0.8908274173736572
    ]
]

# 转换矩阵：Y 向上 -> Z 向上
y_up_to_z_up = [
    [1, 0, 0],
    [0, 0, 1],
    [0, -1, 0]
]

z_up_to_y_up = [
    [1, 0, 0],
    [0, 0, -1],
    [0, 1, 0]
]

# 转换旋转矩阵
# transformed_matrix = transform_matrix_to_new_basis(rotation_matrix, y_up_to_z_up)
#
# # 计算欧拉角 (XYZ 顺序)
# euler_angles_xyz = rotation_matrix_to_euler_angles_xyz(transformed_matrix)
# print(euler_angles_xyz)

print rotation_matrix_to_euler_angles_xyz(rotation_matrix)

transformed_matrix = transform_matrix_to_new_basis(rotation_matrix, z_up_to_y_up)
print transformed_matrix
euler_angles_xyz = rotation_matrix_to_euler_angles_xyz(transformed_matrix)
print (euler_angles_xyz)
