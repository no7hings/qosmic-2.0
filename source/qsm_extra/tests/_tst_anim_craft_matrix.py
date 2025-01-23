# coding:utf-8
import numpy as np

# 初始矩阵
R_initial = np.array([
    [0, 0, 1],
    [0, 1, 0],
    [-1, 0, 0]
])

# 单位矩阵
R_target = np.eye(3)

# 计算修正矩阵（旋转矩阵的逆等于转置）
R_correction = np.transpose(R_initial)

# 验证：修正矩阵乘以初始矩阵是否得到单位矩阵
result = np.dot(R_correction, R_initial)

print("修正矩阵 R_correction:")
print(R_correction)

print("\n验证结果 (R_correction * R_initial):")
print(result)