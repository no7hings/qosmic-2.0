# coding:utf-8
import math

# 定义向量
vector1 = (0, 1, 0)
vector_2 = (0, 0, 1)

# 计算点积
dot_product = sum(v1 * v2 for v1, v2 in zip(vector1, vector_2))

# 计算模长
magnitude_v1 = math.sqrt(sum(v ** 2 for v in vector1))
magnitude_v2 = math.sqrt(sum(v ** 2 for v in vector_2))

# 计算夹角的余弦值
cos_theta = dot_product / (magnitude_v1 * magnitude_v2)

# 计算角度（弧度）
theta_radians = math.acos(cos_theta)

# 转换为角度
theta_degrees = math.degrees(theta_radians)

print("夹角（角度）：", theta_degrees)
