# coding:utf-8
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from . import asset_general as _asset_general


class AssetGpuMeshCountData(object):
    def __init__(self, namespace):
        self._namespace = namespace

    def generate(self):
        gpu_paths = qsm_mya_core.Namespace.find_all_dag_nodes(self._namespace, ['gpuCache'])
        if gpu_paths:
            mark_set = set()
            cache_dict = {}
            component_dict = {}
            for i_idx, i_gpu_path in enumerate(gpu_paths):
                i_gpu_cache_path = qsm_mya_core.NodeAttribute.get_as_string(
                    i_gpu_path, 'cacheFileName'
                )
                if bsc_storage.StgPath.get_is_file(i_gpu_cache_path) is False:
                    continue

                if i_gpu_cache_path in mark_set:
                    continue

                i_group_path = self.import_prc(i_gpu_path, i_gpu_cache_path)
                i_data = self.generate_prc(i_group_path, i_gpu_cache_path)
                if i_data:
                    i_cache_dict, i_component_dict = i_data
                    cache_dict.update(i_cache_dict)
                    component_dict.update(i_component_dict)

                mark_set.add(i_gpu_cache_path)
                # delete when finish
                qsm_mya_core.Node.delete(i_group_path)
            return cache_dict, component_dict

    @classmethod
    def generate_prc(cls, group_path, gpu_cache_path):
        mesh_paths = cmds.ls(group_path, dag=1, long=1, type='mesh')
        if mesh_paths:
            cache_dict = {}
            component_dict = {}
            cache_data = qsm_mya_core.MeshShapes.get_evaluate(mesh_paths)
            cache_data['geometry_all'] = len(mesh_paths)
            cache_data['geometry_visible'] = len(mesh_paths)
            cache_dict[gpu_cache_path] = cache_data
            for i_mesh_path in mesh_paths:
                i_data = qsm_mya_core.Mesh.get_evaluate(i_mesh_path)
                i_data['visible'] = True
                i_data['gpu_cache'] = gpu_cache_path
                j_key = '{}@{}'.format(
                    qsm_mya_core.DagNode.to_path_without_namespace(i_mesh_path).replace('|', '/'),
                    bsc_storage.StgFileOpt(gpu_cache_path).name
                )
                component_dict[j_key] = i_data
            return cache_dict, component_dict

    @classmethod
    def import_prc(cls, gpu_path, gpu_cache_path):
        shape_opt = qsm_mya_core.ShapeOpt(gpu_path)
        transform_path = shape_opt.transform_path
        group_path = '|GPU_GRP'.format(transform_path)

        qsm_mya_core.Group.create(group_path)
        paths = qsm_mya_core.SceneFile.import_file(
            gpu_cache_path
        )
        import_root = qsm_mya_core.DagNode.find_roots(paths)
        if import_root:
            for i_path in import_root:
                if qsm_mya_core.Node.is_transform_type(i_path):
                    i_shape_paths = qsm_mya_core.Group.find_siblings(i_path, ['mesh'])
                    for j_shape_path in i_shape_paths:
                        j_transform_path = qsm_mya_core.Shape.get_transform(j_shape_path)
                        qsm_mya_core.DagNode.parent_to(j_transform_path, group_path, relative=True)

                    if qsm_mya_core.Node.is_exists(i_path):
                        qsm_mya_core.Node.delete(i_path)
        return group_path

    @classmethod
    def test(cls):
        # _asset_general.ProcessUtils.find_all_gpu_caches_and_textures_from(
        #     'X:/QSM_TST/Assets/scn/test_gpu_assembly/Maya/Final/test_gpu_assembly.ma'
        # )
        print cls('test_gpu_assembly').generate()


class AssetMeshCountData(object):
    SUM_KEYS = [
        'geometry_all',
        'geometry_visible',
        'vertex',
        'edge',
        'face',
        'triangle',
        'uv_coord',
        'area',
        'world_area',
        'shell',
    ]

    def __init__(self, namespace):
        self._namespace = namespace

    def generate(self):
        dict_ = {}
        all_data = {}
        meshes = qsm_mya_core.Namespace.find_all_dag_nodes(self._namespace, type_includes=['mesh'])
        meshes_no_intermediate = [x for x in meshes if qsm_mya_core.Shape.is_intermediate(x) is False]
        if meshes:
            all_data = qsm_mya_core.MeshShapes.get_evaluate(meshes_no_intermediate)
            all_data['geometry_all'] = len(meshes)
            all_data['geometry_visible'] = len(meshes_no_intermediate)
            dict_['all'] = all_data

        component_dict = {}
        for i_mesh in meshes:
            # ignore mesh from gpu cache
            if '|{}:GPU_GRP|'.format(self._namespace) in i_mesh:
                continue

            i_key = qsm_mya_core.DagNode.to_path_without_namespace(i_mesh).replace('|', '/')
            i_data = qsm_mya_core.Mesh.get_evaluate(i_mesh)
            if i_mesh in meshes_no_intermediate:
                i_data['visible'] = True
            else:
                i_data['visible'] = False
            component_dict[i_key] = i_data

        dict_['components'] = component_dict
        # get gpu data later, and update it.
        gpu_data = AssetGpuMeshCountData(self._namespace).generate()
        if gpu_data:
            gpu_cache_dict, gpu_component_dict = gpu_data
            dict_['gpu_caches'] = gpu_cache_dict
            dict_['gpu_cache_components'] = gpu_component_dict
            for k, v in gpu_cache_dict.items():
                for j_key in self.SUM_KEYS:
                    all_data[j_key] += v[j_key]
        # recompute per area
        if all_data['world_area']:
            all_data['face_per_world_area'] = qsm_mya_core.Mesh.compute_count_per_area(
                all_data['face'], all_data['world_area']
            )
            all_data['triangle_per_world_area'] = qsm_mya_core.Mesh.compute_count_per_area(
                all_data['triangle'], all_data['world_area']
            )
        else:
            all_data['face_per_world_area'] = 0.0
            all_data['triangle_per_world_area'] = 0.0
        return dict_

    @classmethod
    def test(cls):
        print cls('test_gpu_assembly').generate()


class AssetMeshCountGenerate(object):
    def __init__(self, namespace):
        self._namespace = namespace
        self._file_path = qsm_mya_core.ReferenceNamespacesCache().get_file(self._namespace)

    def generate(self):
        return dict(
            mesh_count=AssetMeshCountData(self._namespace).generate()
        )

    def execute(self, cache_path):
        # import all gpu
        bsc_storage.StgFileOpt(cache_path).set_write(
            self.generate()
        )

    @classmethod
    def test(cls):
        namespace = 'test_gpu_assembly1'
        file_path = qsm_mya_core.ReferenceNamespacesCache().get_file(namespace)
        _asset_general.ProcessUtils.pre_process(namespace, file_path)
        data = cls(namespace).generate()
        print data['mesh_count']['gpu_caches']


class AssetMeshCountProcess(object):
    def __init__(self, file_path, cache_path, image_path):
        self._file_path = file_path
        self._cache_path = cache_path
        self._image_path = image_path
        self._namespace = 'MESH_COUNT'

    def execute(self):
        with bsc_log.LogProcessContext.create(maximum=5) as l_p:
            # step 1
            qsm_mya_core.SceneFile.new()
            l_p.do_update()
            # step 2
            if os.path.isfile(self._file_path) is False:
                raise RuntimeError()
            qsm_mya_core.SceneFile.reference_file(
                self._file_path, namespace=self._namespace
            )
            l_p.do_update()
            # step 3
            _asset_general.ProcessUtils.find_all_gpu_caches_and_textures_from(self._file_path)
            l_p.do_update()
            # step 4
            locations = qsm_mya_core.Namespace.find_roots(self._namespace)
            qsm_mya_core.Snapshot.create(
                locations, self._image_path
            )
            l_p.do_update()
            # step 5
            bsc_storage.StgFileOpt(self._cache_path).set_write(
                AssetMeshCountGenerate(self._namespace).generate()
            )
            l_p.do_update()
