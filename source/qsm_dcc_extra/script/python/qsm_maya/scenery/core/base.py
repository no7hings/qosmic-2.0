# coding:utf-8
import lxbasic.core as bsc_core

from ... import core as _mya_core


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

    @classmethod
    def find(cls, path):
        if _mya_core.Node.is_transform(path):
            return None

        path_opt = bsc_core.PthNodeOpt(path)
        paths = path_opt.get_ancestor_paths()
        for i_path in paths[:3]:
            if i_path != _mya_core.DagNode.PATHSEP:
                if _mya_core.Attribute.is_exists(i_path, 'qsm_type') is True:
                    return i_path
