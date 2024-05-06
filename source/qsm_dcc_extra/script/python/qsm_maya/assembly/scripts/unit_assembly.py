# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from ... import core as _mya_core

from ...asset import core as _ast_core


class UnitAssemblyGenerate(object):
    def __init__(self, namespace):
        self._namespace = namespace


class UnitProcess(object):
    pass


class UnitAssemblyProcess(object):
    def __init__(self, file_path, cache_file_path):
        self._file_path = file_path

        self._directory_path = bsc_storage.StgFileOpt(
            self._file_path
        ).directory_path
        self._cache_file_path = cache_file_path
        # print _ast_core.AssetCache.generate_unit_assembly_file(
        #     self._file_path
        # )
        self._cache_directory_path = bsc_storage.StgFileOpt(
            self._cache_file_path
        ).directory_path

    def mesh_prc(self, shape_path):
        mesh_opt = _mya_core.MeshOpt(shape_path)
        hash_key = mesh_opt.to_hash()
        transform_path = mesh_opt.transform_path
        transform_name = mesh_opt.transform_name

        unit_directory_path = '{}/unit/{}'.format(
            self._cache_directory_path, hash_key
        )
        ad_file_path = '{}/AD.ma'.format(
            unit_directory_path
        )

        if bsc_storage.StgPathMtd.get_is_file(ad_file_path) is False:
            gpu_file_path = '{}/gpu.abc'.format(
                unit_directory_path
            )
            scene_file_path = '{}/scene.ma'.format(
                unit_directory_path
            )

            transform_path_copy = _mya_core.NodeDag.copy_to_world(transform_path)

            ad_path = '|{}_AD'.format(transform_name)

            _mya_core.Transform.reset_transformation(transform_path_copy)

            _mya_core.GpuCache.export_frame(
                gpu_file_path, transform_path_copy
            )
            _mya_core.SceneFile.export_file(
                scene_file_path, transform_path_copy
            )

            _mya_core.AssemblyDefinition.create(
                ad_path
            )
            _mya_core.AssemblyDefinition.add_cache(
                ad_path, gpu_file_path, 'GPU'
            )
            _mya_core.AssemblyDefinition.add_scene(
                ad_path, scene_file_path, 'Mesh'
            )

            for i_seq in range(2):
                i_lod_level = str(i_seq+1).zfill(2)
                shape_path_copy = _mya_core.Transform.get_shape_path(transform_path_copy)
                _mya_core.MeshReduce.reduce_off(shape_path_copy, 50)
                i_gpu_file_path_lod = '{}/gpu.lod{}.abc'.format(
                    unit_directory_path, i_lod_level
                )
                i_scene_file_path_lod = '{}/scene.lod{}.ma'.format(
                    unit_directory_path, i_lod_level
                )
                _mya_core.GpuCache.export_frame(
                    i_gpu_file_path_lod, transform_path_copy
                )
                _mya_core.SceneFile.export_file(
                    i_scene_file_path_lod, transform_path_copy
                )
                _mya_core.AssemblyDefinition.add_cache(
                    ad_path, i_gpu_file_path_lod, 'GPU-LOD{}'.format(i_lod_level)
                )
                _mya_core.AssemblyDefinition.add_scene(
                    ad_path, i_scene_file_path_lod, 'Mesh-LOD{}'.format(i_lod_level)
                )

            _mya_core.Node.delete(transform_path_copy)

            _mya_core.SceneFile.export_file(
                ad_file_path, ad_path
            )

            _mya_core.Node.delete(ad_path)

        _mya_core.Transform.delete_all_shapes(transform_path)

        ar_path = '{}|{}_AR'.format(transform_path, transform_name)

        _mya_core.AssemblyReference.create(
            ad_file_path, ar_path
        )

    def gpu_prc(self, shape_path):
        gpu_file_path = _mya_core.Attribute.get_as_string(
            shape_path, 'cacheFileName'
        )
        shape_opt = _mya_core.ShapeOpt(shape_path)
        transform_path = shape_opt.transform_path
        transform_name = shape_opt.transform_name
        if bsc_storage.StgPathMtd.get_is_file(gpu_file_path):
            paths = _mya_core.SceneFile.import_file(
                gpu_file_path
            )

            roots = _mya_core.NodeDag.find_roots(paths)

            _mya_core.Transform.delete_all_shapes(transform_path)

            if roots:
                for i_path in roots:
                    if _mya_core.Node.is_transform(i_path):
                        _mya_core.NodeDag.parent_to(i_path, transform_path)

        mesh_paths = _mya_core.NodeDag.find_siblings(
            transform_path, ['mesh']
        )
        for i_path in mesh_paths:
            self.mesh_prc(i_path)

    def execute(self):
        _mya_core.SceneFile.new()

        assembly_file_path = '{}/assembly.ma'.format(
            self._cache_directory_path
        )
        paths = _mya_core.SceneFile.import_file(
            self._file_path
        )
        # assembly
        roots = _mya_core.NodeDag.find_roots(paths)
        # find lost reference first
        _mya_core.FileReferences.search_all_from(
            [self._directory_path]
        )
        # create assembly
        for i_path in paths:
            if _mya_core.Node.is_mesh(i_path) is True:
                self.mesh_prc(i_path)
            elif _mya_core.Node.is_gpu(i_path) is True:
                self.gpu_prc(i_path)
        # export assembly
        roots = [i for i in roots if _mya_core.Node.is_exists(i)]
        _mya_core.SceneFile.export_file(
            assembly_file_path, roots
        )

        _mya_core.SceneFile.new()
        file_name = bsc_storage.StgFileOpt(self._file_path).name_base
        ad_path = '|{}_AD'.format(file_name)
        _mya_core.AssemblyDefinition.create(ad_path)

        _mya_core.AssemblyDefinition.add_scene(ad_path, assembly_file_path, 'Assembly')
        _mya_core.AssemblyDefinition.add_scene(ad_path, self._file_path, 'Scene')

        _mya_core.SceneFile.export_file(
            self._cache_file_path, ad_path
        )
