# coding:utf-8
import math

import maya.cmds as cmds

import maya.OpenMaya as om

# 定义两个locator的名字
locator1 = 'joint1'
locator2 = 'nurbsCircle1'

# 获取初始旋转值和旋转顺序
rot1_initial = cmds.getAttr(locator1 + '.rotate')[0]
rot1_order = cmds.getAttr(locator1 + '.rotateOrder')
rot2_initial = cmds.getAttr(locator2 + '.rotate')[0]
rot2_order = cmds.getAttr(locator2 + '.rotateOrder')

# 将旋转值转换为矩阵
def rotation_to_matrix(rotation, order):
    euler_rot = om.MEulerRotation(om.MVector(*[math.radians(x) for x in rotation]), order)
    return euler_rot.asMatrix()

matrix1_initial = rotation_to_matrix(rot1_initial, rot1_order)
matrix2_initial = rotation_to_matrix(rot2_initial, rot2_order)

# 计算初始旋转差值矩阵
rotation_offset_matrix = matrix2_initial * matrix1_initial.inverse()

# 定义一个函数来应用旋转并保持初始偏移
def apply_rotation_with_initial_offset(target, source, offset_matrix, source_order, target_order):
    source_rot = cmds.getAttr(source + '.rotate')[0]
    om.MMatrix()
    source_matrix = rotation_to_matrix(source_rot, source_order)
    new_matrix = source_matrix*offset_matrix
    new_euler = om.MTransformationMatrix(new_matrix).rotation().asEulerRotation()
    new_rot = new_euler.asVector()
    cmds.setAttr(target + '.rotate', math.degrees(new_rot.x), math.degrees(new_rot.y), math.degrees(new_rot.z))
    cmds.setAttr(target + '.rotateOrder', target_order)

# 每次更新旋转时调用这个函数
apply_rotation_with_initial_offset(locator2, locator1, rotation_offset_matrix, rot1_order, rot2_order)
