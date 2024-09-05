# coding:utf-8
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

import qsm_maya.scenery.core as qsm_mya_scn_core


class GpuImport(object):
    @classmethod
    def execute(cls, namespace):
        mark_set = set()
        shape_paths = cmds.ls(type='gpuCache', long=1)
        for i_shape_path in shape_paths:
            cls.gpu_prc(namespace, i_shape_path, mark_set)

    @classmethod
    def gpu_prc(cls, namespace, shape_path, mark_set):
        shape_opt = qsm_mya_core.ShapeOpt(shape_path)
        transform_path = shape_opt.transform_path
        gpu_group_path = '{}|{}:GPU_GRP'.format(transform_path, namespace)
        gpu_cache_path = qsm_mya_core.NodeAttribute.get_as_string(
            shape_path, 'cacheFileName'
        )
        if bsc_storage.StgPath.get_is_file(gpu_cache_path) is False:
            return

        if qsm_mya_core.Node.is_exists(gpu_group_path) is True:
            mark_set.add(gpu_cache_path)
            return

        if gpu_cache_path in mark_set:
            return

        mark_set.add(gpu_cache_path)

        qsm_mya_core.Group.create(gpu_group_path)
        paths = qsm_mya_core.SceneFile.import_file(
            gpu_cache_path, namespace=namespace
        )
        roots = qsm_mya_core.DagNode.find_roots(paths)
        if roots:
            for i_path in roots:
                if qsm_mya_core.Node.is_transform(i_path):
                    i_shape_paths = qsm_mya_core.Group.find_siblings(i_path, ['mesh'])
                    for j_shape_path in i_shape_paths:
                        j_transform_path = qsm_mya_core.Shape.get_transform(j_shape_path)
                        qsm_mya_core.DagNode.parent_to(j_transform_path, gpu_group_path, relative=True)

                    if qsm_mya_core.Node.is_exists(i_path):
                        qsm_mya_core.Node.delete(i_path)


class ProcessUtils(object):
    @classmethod
    def pre_process_0(cls, file_path):
        # find lost
        directory_path = bsc_storage.StgFileOpt(file_path).directory_path
        qsm_mya_scn_core.GpuImport.find_all_gpu_files(directory_path)
        qsm_mya_core.FileReferences.search_all_from(
            [directory_path], ignore_exists=True
        )

    @classmethod
    def pre_process_1(cls, namespace):
        # import gpu
        GpuImport.execute(namespace)

    @classmethod
    def pre_process(cls, namespace, file_path):
        # find lost
        directory_path = bsc_storage.StgFileOpt(file_path).directory_path
        qsm_mya_scn_core.GpuImport.find_all_gpu_files(directory_path)
        qsm_mya_core.FileReferences.search_all_from(
            [directory_path], ignore_exists=True
        )
        # import gpu
        GpuImport.execute(namespace)
