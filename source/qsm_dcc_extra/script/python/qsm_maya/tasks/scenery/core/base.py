# coding:utf-8
import os.path

# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core


class Assembly(object):
    class Keys(object):
        GPU = 'gpu'
        GPU_LOD = 'gpu_lod{}'
        GPU_LOD_1 = 'gpu_lod1'
        GPU_LOD_2 = 'gpu_lod2'
        Mesh = 'mesh'
        Mesh_LOD = 'mesh_lod{}'
        Mesh_LOD_1 = 'mesh_lod1'
        Mesh_LOD_2 = 'mesh_lod2'

        All = [
            GPU,
            GPU_LOD_1,
            GPU_LOD_2,
            Mesh,
            Mesh_LOD_1,
            Mesh_LOD_2
        ]
        GPUs = [
            GPU,
            GPU_LOD_1,
            GPU_LOD_2,
        ]

    class Types(object):
        UnitAssembly = 'unit_assembly'
        GpuInstance = 'gpu_instance'

    FACE_COUNT_MAXIMUM = 50000

    DIMENSION_MINIMUM = 1000

    @classmethod
    def find_assembly_reference(cls, path):
        _0 = qsm_mya_core.NodeAttribute.get_target_nodes(
            path, 'message', 'hyperLayout'
        )
        if _0:
            _1 = qsm_mya_core.NodeAttribute.get_target_nodes(
                _0[0], 'message', 'assemblyReference'
            )
            if _1:
                return _1[0]

    @classmethod
    def find_any_by_shape(cls, shape_path, depth_maximum=3):
        path_opt = bsc_core.BscNodePathOpt(shape_path)
        paths = path_opt.get_ancestor_paths()
        for i_path in paths[:depth_maximum]:
            if i_path != qsm_mya_core.DagNode.PATHSEP:
                if qsm_mya_core.NodeAttribute.is_exists(i_path, 'qsm_type') is True:
                    return i_path


class MeshInstance(object):
    def __init__(self, material=False):
        self._material = material
        self._hash_key_dict = {}

    def execute(self):
        shape_paths = cmds.ls(type='mesh', noIntermediate=1, long=1)
        for i_shape_path in shape_paths:
            self.mesh_prc(i_shape_path)

    def mesh_prc(self, shape_path):
        mesh_opt = qsm_mya_core.MeshShapeOpt(shape_path)
        hash_key = mesh_opt.to_hash()
        if self._material is True:
            hash_key_1 = mesh_opt.get_material_assign_as_hash_key()
            hash_key = hash_key+hash_key_1

        if hash_key not in self._hash_key_dict:
            self._hash_key_dict[hash_key] = shape_path
        else:
            shape_path_src = self._hash_key_dict[hash_key]
            transform_path = mesh_opt.transform_path
            qsm_mya_core.Transform.delete_all_shapes(transform_path)
            qsm_mya_core.Shape.instance_to(
                shape_path_src, transform_path
            )


class GpuImport(object):

    # fixme: this is holly shit
    @classmethod
    def find_all_gpu_caches(cls, directory_path):
        for i in cmds.ls(type='gpuCache', long=1):
            i_file_path = qsm_mya_core.NodeAttribute.get_as_string(i, 'cacheFileName')
            if i_file_path.startswith('O:/ABCWrite/'):
                i_file_path_new = '{}/ABCWrite/{}'.format(
                    directory_path, i_file_path.replace('O:/ABCWrite/', '')
                )
                if os.path.exists(i_file_path_new):
                    qsm_mya_core.NodeAttribute.set_as_string(
                        i, 'cacheFileName', i_file_path_new
                    )

    def __init__(self):
        pass

    @classmethod
    def execute(cls):
        shape_paths = cmds.ls(type='gpuCache', long=1)
        for i_shape_path in shape_paths:
            cls.gpu_prc(i_shape_path)

    @classmethod
    def gpu_prc(cls, shape_path):
        gpu_file_path = qsm_mya_core.NodeAttribute.get_as_string(
            shape_path, 'cacheFileName'
        )
        shape_opt = qsm_mya_core.ShapeOpt(shape_path)
        transform_path = shape_opt.transform_path
        if bsc_storage.StgPath.get_is_file(gpu_file_path):
            paths = qsm_mya_core.SceneFile.import_file(
                gpu_file_path
            )

            roots = qsm_mya_core.DagNode.find_roots(paths)

            qsm_mya_core.Transform.delete_all_shapes(transform_path)

            if roots:
                for i_path in roots:
                    if qsm_mya_core.Node.is_transform_type(i_path):
                        i_shape_paths = qsm_mya_core.Group.find_siblings(i_path, ['mesh'])
                        for j_shape_path in i_shape_paths:
                            j_transform_path = qsm_mya_core.Shape.get_transform(j_shape_path)
                            qsm_mya_core.DagNode.parent_to(j_transform_path, transform_path, relative=True)

                        if qsm_mya_core.Node.is_exists(i_path):
                            qsm_mya_core.Node.delete(i_path)


class ShitFixer(object):
    def __init__(self):
        pass

    def execute(self):
        shape_paths = qsm_mya_core.Scene.find_all_dag_nodes(type_includes=['mesh'])
        for i_shape_path in shape_paths:
            i_transform_path = qsm_mya_core.Shape.get_transform(i_shape_path)
            _ = cmds.ls(i_transform_path, type='mesh', noIntermediate=0, dag=1, long=1)
            print _
