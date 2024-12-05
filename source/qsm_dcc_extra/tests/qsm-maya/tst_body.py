# coding:utf-8
import collections

import maya.cmds as cmds

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

cmds.file(save=1, f=1)

dict_ = collections.OrderedDict()

for i in qsm_mya_core.Scene.find_all_dag_nodes(type_includes=['mesh']):
    i_coords = []
    i_mesh_opt = qsm_mya_core.MeshShapeOpt(i)
    i_transform_path = i_mesh_opt.transform_path
    i_x = qsm_mya_core.NodeAttribute.get_value(i_transform_path, 'scaleX')
    i_indices = i_mesh_opt.get_face_vertices()
    i_points = i_mesh_opt.get_points()

    for j_index in i_indices[1]:
        j_point = i_points[j_index]
        i_coords.append((j_point[0]*i_x, 100-j_point[1]))

    i_key = i_mesh_opt.transform_name
    dict_[i_key] = i_coords

bsc_storage.StgFileOpt(
    'E:/myworkspace/qosmic-2.0/source/qsm_extra/resources/gui/adv-picker/v1.json'
).set_write(dict_)
