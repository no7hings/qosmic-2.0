# coding:utf-8
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.model as bsc_model

import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

import qsm_maya.core as qsm_mya_core

import qsm_maya.general.core as qsm_mya_gnl_core

import qsm_maya.assembly.core as qsm_mya_asb_core

import qsm_maya.scenery.core as qsm_mya_scn_core


class AssetUnitAssemblyOpt(object):
    TASK_KEY = 'unit_assembly_generate'

    CACHE_ROOT = qsm_mya_gnl_core.ResourceCacheNodes.UnitAssemblyRoot
    CACHE_NAME = qsm_mya_gnl_core.ResourceCacheNodes.UnitAssemblyName

    @classmethod
    def create_cache_root_auto(cls):
        if cmds.objExists(cls.CACHE_ROOT) is False:
            name = cls.CACHE_ROOT.split('|')[-1]
            # cmds.container(type='dagContainer', name=name)
            cmds.createNode(
                'dagContainer', name=name, shared=1, skipSelect=1
            )
            cmds.setAttr(cls.CACHE_ROOT+'.iconName', 'folder-closed.png', type='string')

    @classmethod
    def load_cache(cls, namespace, cache_path):
        cls.create_cache_root_auto()

        cache_location_new = '{}|{}:{}'.format(cls.CACHE_ROOT, namespace, cls.CACHE_NAME)
        cache_location = '|{}:{}'.format(namespace, cls.CACHE_NAME)
        if cmds.objExists(cache_location) is False and cmds.objExists(cache_location_new) is False:
            if os.path.isfile(cache_path) is True:
                qsm_mya_core.SceneFile.import_container_file(
                    cache_path, namespace=namespace
                )
                cmds.parent(cache_location, cls.CACHE_ROOT)

        statistics = bsc_storage.Statistics.generate()
        statistics.update_at_time(
            dict(
                method='unit_assembly_cache_load',
                cache=cache_path
            )
        )


class _RegionPrc(object):
    @classmethod
    def _compute_grid_size(cls, mesh_paths):
        mesh_count_data = qsm_mya_core.Meshes.get_evaluate(mesh_paths)
        width, depth = mesh_count_data['width'], mesh_count_data['depth']
        size = max(width, depth)
        m = 100
        # 10K
        if size <= m*10000:
            # 10
            grid_size = m*10
        # 100K
        elif size <= m*100000:
            # 100
            grid_size = m*100
        # 1M
        elif size <= m*1000000:
            # 1K
            grid_size = m*1000
        # 10M
        elif size <= m*10000000:
            # 10K
            grid_size = m*10000
        # 100M
        elif size <= m*10000000:
            # 100K
            grid_size = m*100000
        else:
            grid_size = m*500000
        return grid_size

    @classmethod
    def _compute_grid_size_0(cls, roots):
        bbox = qsm_mya_core.BBox.exact_for_many(roots)
        _x, _y, _z, x, y, z = bbox
        w, h, d = x-_x, y-_y, z-_z
        size = max(w, d)
        return int(size/32.0)

    def __init__(self, mesh_paths, cache_directory_path, exists_roots, tag):
        self._mesh_paths = mesh_paths
        self._cache_directory_path = cache_directory_path
        self._exists_roots = exists_roots
        self._tag = tag

    def execute(self):
        mesh_paths = self._mesh_paths
        if not mesh_paths:
            return

        # compute grid size
        grid_size = self._compute_grid_size_0(self._exists_roots)
        region_paths = []

        if mesh_paths:
            grid_map = qsm_mya_asb_core.GridSpace(mesh_paths, grid_size).generate()
            keys = grid_map.keys()
            keys.sort()
            for i_seq, i_key in enumerate(keys):
                # fixme: comp maybe grid again
                i_shape_paths = grid_map[i_key]
                print qsm_mya_core.Meshes.get_triangle_number(i_shape_paths), 'AAAA'
                i_ar_path_new = self.prc(i_key, i_seq, i_shape_paths)
                # fixme: maybe None
                if i_ar_path_new:
                    region_paths.append(i_ar_path_new)
        return region_paths

    def prc(self, key, seq, shape_paths):
        hash_key = bsc_core.BscHash.to_hash_key(shape_paths)
        directory_path = '{}/region_{}/{}'.format(
            self._cache_directory_path, self._tag, hash_key
        )
        ad_file_path = '{}/AD.ma'.format(
            directory_path
        )
        if bsc_storage.StgFileOpt(ad_file_path).get_is_file() is False:
            gpu_file_path = '{}/gpu.abc'.format(
                directory_path
            )
            mesh_file_path = '{}/mesh.ma'.format(
                directory_path
            )

            group_path = '|region_{}_{}_GRP'.format(self._tag, seq)
            group_path_new = qsm_mya_core.Group.create(group_path)
            for j_shape_path in shape_paths:
                # fixme: mesh parent mesh
                if qsm_mya_core.DagNode.is_exists(j_shape_path) is False:
                    continue

                j_transform_path = qsm_mya_core.Shape.get_transform(j_shape_path)
                qsm_mya_core.Group.add(group_path_new, j_transform_path)

            if not qsm_mya_core.Group.get_children(group_path_new):
                return

            # export to gpu and mesh
            qsm_mya_core.GpuCache.export_frame_(
                gpu_file_path, group_path_new
            )
            qsm_mya_core.SceneFile.export_file(
                mesh_file_path, group_path_new
            )
            qsm_mya_core.Node.delete(group_path_new)
            # create AD
            ad_path = '|region_{}_{}_AD'.format(self._tag, seq)
            # ad
            qsm_mya_core.AssemblyDefinition.create(ad_path)
            qsm_mya_core.AssemblyDefinition.add_cache(
                ad_path, gpu_file_path, 'gpu'
            )
            qsm_mya_core.AssemblyDefinition.add_scene(
                ad_path, mesh_file_path, 'mesh'
            )
            qsm_mya_core.SceneFile.export_file(
                ad_file_path, ad_path
            )
            qsm_mya_core.Node.delete(ad_path)
        else:
            # remove exists
            for j_shape_path in shape_paths:
                # fixme: mesh parent mesh
                if qsm_mya_core.DagNode.is_exists(j_shape_path) is False:
                    continue

                j_transform_path = qsm_mya_core.Shape.get_transform(j_shape_path)
                qsm_mya_core.Node.delete(j_transform_path)

        ar_path = '|region_{}_{}_AR'.format(self._tag, seq)
        ar_path_new = qsm_mya_core.AssemblyReference.create(
            ad_file_path, ar_path
        )
        qsm_mya_core.NodeAttribute.create_as_string(
            ar_path_new, 'qsm_type', 'unit_assembly'
        )
        qsm_mya_core.NodeAttribute.create_as_string(
            ar_path_new, 'qsm_hash_key', hash_key
        )
        qsm_mya_core.NodeDrawOverride.set_enable(
            ar_path_new, True
        )
        qsm_mya_core.NodeDrawOverride.set_color(
            ar_path_new, (1.0, .5, .25)
        )
        return ar_path_new


class _UnitPrc(object):
    LOG_KEY = 'mesh assembly'

    @classmethod
    def filter_prc(cls, shape_path):
        face_count = qsm_mya_core.Mesh.get_face_number(shape_path)
        if face_count > qsm_mya_scn_core.Assembly.FACE_COUNT_MAXIMUM:
            pass

    def __init__(self, cache_directory_path):
        self._cache_directory_path = cache_directory_path

    def filter_execute_for(self, shape_path):
        face_count = qsm_mya_core.Mesh.get_face_number(shape_path)
        if face_count < qsm_mya_scn_core.Assembly.FACE_COUNT_MAXIMUM:
            return

        self.execute_for(shape_path)

    def execute_for(self, shape_path):
        mesh_opt = qsm_mya_core.MeshOpt(shape_path)
        face_count = qsm_mya_core.Mesh.get_face_number(shape_path)
        if face_count == 0:
            return

        hash_key = mesh_opt.to_hash()
        transform_path = mesh_opt.transform_path
        transform_name = mesh_opt.transform_name

        unit_directory_path = '{}/unit/{}'.format(
            self._cache_directory_path, hash_key
        )
        ad_file_path = '{}/AD.ma'.format(
            unit_directory_path
        )

        if bsc_storage.StgPath.get_is_file(ad_file_path) is False:
            file_dict = {}

            transform_path_copy = qsm_mya_core.DagNode.copy_to_world(transform_path)

            transform_new_name = '{}_mesh'.format(transform_name)
            transform_path_new = qsm_mya_core.DagNode.rename(transform_path_copy, transform_new_name)

            ad_path = '|{}_AD'.format(transform_name)

            qsm_mya_core.Transform.zero_transformations(transform_path_new)
            # gpu
            gpu_key = qsm_mya_scn_core.Assembly.Keys.GPU
            gpu_file_path = '{}/{}.abc'.format(
                unit_directory_path, gpu_key
            )
            qsm_mya_core.GpuCache.export_frame(
                gpu_file_path, transform_path_new
            )
            file_dict[gpu_key] = gpu_file_path
            # mesh
            mesh_key = qsm_mya_scn_core.Assembly.Keys.Mesh
            mesh_file_path = '{}/{}.ma'.format(
                unit_directory_path, mesh_key
            )
            qsm_mya_core.SceneFile.export_file(
                mesh_file_path, transform_path_new
            )
            file_dict[mesh_key] = mesh_file_path
            qsm_mya_core.AssemblyDefinition.create(
                ad_path
            )

            shape_path_new = qsm_mya_core.Transform.get_shape(transform_path_new)
            # memory error when face more than 25000000
            if face_count <= 25000000:
                bsc_log.Log.trace_method_result(
                    self.LOG_KEY, 'try create lod for: "{}", face count is {}'.format(
                        shape_path_new, face_count
                    )
                )

                cmds.select(shape_path_new)
                mel.eval(
                    (
                        'expandPolyGroupSelection; '
                        'polyCleanupArgList 4 '
                        '{ "0","1","0","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","1","1","0" };'
                    )
                )
                for i_seq in range(2):
                    i_level = i_seq+1
                    # todo: may be mesh had lamina or non-manifold
                    # noinspection PyBroadException
                    try:
                        qsm_mya_core.MeshReduce.reduce_off(shape_path_new, 50)
                    except Exception:
                        bsc_log.Log.trace_method_error(
                            'mesh reduce', 'mesh "{}" had lamina or non-manifold faces or vertices'.format(
                                shape_path_new
                            )
                        )
                    # gpu
                    i_gpu_key = qsm_mya_scn_core.Assembly.Keys.GPU_LOD.format(i_level)
                    i_gpu_file_path_lod = '{}/{}.abc'.format(
                        unit_directory_path, i_gpu_key
                    )
                    qsm_mya_core.GpuCache.export_frame(
                        i_gpu_file_path_lod, transform_path_new
                    )
                    file_dict[i_gpu_key] = i_gpu_file_path_lod
                    # mesh
                    i_mesh_key = qsm_mya_scn_core.Assembly.Keys.Mesh_LOD.format(i_level)
                    i_mesh_file_path_lod = '{}/{}.ma'.format(
                        unit_directory_path, i_mesh_key
                    )
                    qsm_mya_core.SceneFile.export_file(
                        i_mesh_file_path_lod, transform_path_new
                    )
                    file_dict[i_mesh_key] = i_mesh_file_path_lod

            # add attribute
            for i_key in qsm_mya_scn_core.Assembly.Keys.All:
                if i_key in file_dict:
                    i_file_path = file_dict[i_key]
                    if i_key.startswith(qsm_mya_scn_core.Assembly.Keys.Mesh):
                        qsm_mya_core.AssemblyDefinition.add_scene(
                            ad_path, i_file_path, i_key
                        )
                    elif i_key.startswith(qsm_mya_scn_core.Assembly.Keys.GPU):
                        qsm_mya_core.AssemblyDefinition.add_cache(
                            ad_path, i_file_path, i_key
                        )

            qsm_mya_core.Node.delete(transform_path_new)

            qsm_mya_core.SceneFile.export_file(
                ad_file_path, ad_path
            )

            qsm_mya_core.Node.delete(ad_path)
        # clean exists
        qsm_mya_core.Transform.delete_all_shapes(transform_path)

        ar_path = '{}|{}_AR'.format(transform_path, transform_name)

        ar_path_new = qsm_mya_core.AssemblyReference.create(
            ad_file_path, ar_path
        )
        qsm_mya_core.NodeAttribute.create_as_string(
            ar_path_new, 'qsm_type', 'unit_assembly'
        )
        qsm_mya_core.NodeAttribute.create_as_string(
            ar_path_new, 'qsm_hash_key', hash_key
        )
        qsm_mya_core.NodeDrawOverride.set_enable(
            ar_path_new, True
        )
        qsm_mya_core.NodeDrawOverride.set_color(
            ar_path_new, (1.0, .5, .25)
        )
        return ar_path_new


class _GpuPrc(object):
    def __init__(self, cache_directory_path):
        self._cache_directory_path = cache_directory_path

    def execute(self):
        region_paths = []
        gpu_paths = cmds.ls(type='gpuCache', long=1)
        for i_idx, i_gpu_path in enumerate(gpu_paths):
            i_gpu_cache_path = qsm_mya_core.NodeAttribute.get_as_string(
                i_gpu_path, 'cacheFileName'
            )
            if bsc_storage.StgPath.get_is_file(i_gpu_cache_path) is False:
                continue

            _ = self.prc(i_gpu_path, i_gpu_cache_path)
            if _:
                i_transform_path, i_mesh_paths = _
                i_tag = 'gpu_{}_{}'.format(
                    bsc_storage.StgFileOpt(i_gpu_cache_path).name_base.lower(), i_idx
                )
                i_region_paths = _RegionPrc(
                    i_mesh_paths, self._cache_directory_path, [i_transform_path], i_tag
                ).execute()
                region_paths.extend(i_region_paths)
        return region_paths

    @classmethod
    def prc(cls, gpu_path, gpu_cache_path):
        shape_opt = qsm_mya_core.ShapeOpt(gpu_path)
        transform_path = shape_opt.transform_path

        paths = qsm_mya_core.SceneFile.import_file(
            gpu_cache_path
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
        return transform_path, cmds.ls(transform_path, dag=1, long=1, type='mesh')


class _GpuImportPrc(object):
    def execute(self):
        gpu_paths = cmds.ls(type='gpuCache', long=1)
        for i_idx, i_gpu_path in enumerate(gpu_paths):
            i_gpu_cache_path = qsm_mya_core.NodeAttribute.get_as_string(
                i_gpu_path, 'cacheFileName'
            )
            if bsc_storage.StgPath.get_is_file(i_gpu_cache_path) is False:
                continue

            self.prc(i_gpu_path, i_gpu_cache_path)

    @classmethod
    def prc(cls, gpu_path, gpu_cache_path):
        shape_opt = qsm_mya_core.ShapeOpt(gpu_path)
        transform_path = shape_opt.transform_path

        paths = qsm_mya_core.SceneFile.import_file(
            gpu_cache_path
        )

        roots = qsm_mya_core.DagNode.find_roots(paths)
        # remove gpu shape
        qsm_mya_core.Transform.delete_all_shapes(transform_path)
        # parent to transform
        if roots:
            for i_path in roots:
                if qsm_mya_core.Node.is_transform_type(i_path):
                    i_shape_paths = qsm_mya_core.Group.find_siblings(i_path, ['mesh'])
                    for j_shape_path in i_shape_paths:
                        j_transform_path = qsm_mya_core.Shape.get_transform(j_shape_path)
                        qsm_mya_core.DagNode.parent_to(j_transform_path, transform_path, relative=True)
                    if qsm_mya_core.Node.is_exists(i_path):
                        qsm_mya_core.Node.delete(i_path)


class _ScenePrc(object):
    def __init__(self, cache_directory_path, exists_roots):
        self._cache_directory_path = cache_directory_path
        self._exists_roots = exists_roots

    def execute(self):
        unit_prc = _UnitPrc(self._cache_directory_path)
        mesh_paths = qsm_mya_core.Scene.find_all_dag_nodes(type_includes=['mesh'])
        for i_mesh_path in mesh_paths:
            unit_prc.filter_execute_for(i_mesh_path)

        mesh_paths_less = qsm_mya_core.Scene.find_all_dag_nodes(type_includes=['mesh'])
        return _RegionPrc(
            mesh_paths_less,
            self._cache_directory_path,
            self._exists_roots,
            'scene'
        ).execute()


class AssetUnitAssemblyProcess(object):
    LOG_KEY = 'unit assembly'
    PLUG_NAMES = [
        'sceneAssembly',
        'gpuCache',
        'AbcImport',
        'AbcExport',
    ]

    @classmethod
    def _load_plugs(cls):
        for i in cls.PLUG_NAMES:
            cmds.loadPlugin(i, quiet=1)

    def __init__(self, file_path, cache_path=None):
        self._load_plugs()

        self._file_path = file_path

        self._directory_path = bsc_storage.StgFileOpt(
            self._file_path
        ).directory_path

        if cache_path is None:
            self._cache_file_path = qsm_gnl_core.MayaCache.generate_asset_unit_assembly_file_new(self._file_path)
        else:
            self._cache_file_path = cache_path

        self._cache_directory_path = bsc_storage.StgFileOpt(
            self._cache_file_path
        ).directory_path

    def _pre_prc(self):
        qsm_mya_core.SceneFile.new()

        self._container = '|{}'.format(AssetUnitAssemblyOpt.CACHE_NAME)

        qsm_mya_core.Container.create_as_default(self._container)
        qsm_mya_core.NodeAttribute.create_as_string(
            self._container, 'qsm_file', self._file_path
        )
        qsm_mya_core.NodeAttribute.create_as_string(
            self._container, 'qsm_cache', self._cache_file_path
        )

        bsc_log.Log.trace_method_result(
            self.LOG_KEY, 'load scene: {}'.format(self._file_path)
        )

        import_paths = qsm_mya_core.SceneFile.import_file(
            self._file_path
        )
        qsm_mya_core.Scene.clear_unknown_nodes()
        self._all_roots = qsm_mya_core.DagNode.find_roots(import_paths)
        qsm_mya_scn_core.GpuImport.find_all_gpu_caches(self._directory_path)
        # find lost reference first
        qsm_mya_core.FileReferences.search_all_from(
            [self._directory_path], ignore_exists=True
        )
        # repair all instanced
        qsm_mya_core.Scene.remove_all_instanced(type_includes=['mesh', 'gpuCache'])

    def _post_prc(self):
        # remove empty
        qsm_mya_core.Scene.remove_all_empty_groups()

        exists_roots = [i for i in self._all_roots if qsm_mya_core.Node.is_exists(i)]
        qsm_mya_core.Container.add_dag_nodes(self._container, exists_roots)

        qsm_mya_core.SceneFile.export_file(
            self._cache_file_path, self._container
        )

    def _scene_prc(self):
        exists_roots = [i for i in self._all_roots if qsm_mya_core.Node.is_exists(i)]
        region_paths = _ScenePrc(
            self._cache_directory_path, exists_roots
        ).execute()
        if region_paths:
            qsm_mya_core.Container.add_dag_nodes(self._container, region_paths)

    def _gpu_prc(self):
        region_paths = _GpuPrc(
            self._cache_directory_path
        ).execute()
        if region_paths:
            qsm_mya_core.Container.add_dag_nodes(self._container, region_paths)

    def _gpu_import_prc(self):
        _GpuImportPrc().execute()

    def execute(self):
        with bsc_log.LogProcessContext.create(maximum=4) as l_p:
            # step 1
            self._pre_prc()
            l_p.do_update()
            # step 2
            # process gpu first
            # fixme: use gpu import instance
            # self._gpu_prc()
            self._gpu_import_prc()
            l_p.do_update()
            # step 3
            # scene
            self._scene_prc()
            l_p.do_update()
            # step 4
            self._post_prc()
            l_p.do_update()

    @classmethod
    def test(cls):
        cls(
            'X:/QSM_TST/Assets/scn/test_assembly/Maya/Final/test_assembly.ma'
        ).execute()
