# coding:utf-8
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

import qsm_general.process as qsm_gnl_process

import qsm_maya.core as qsm_mya_core

import qsm_maya.general.core as qsm_mya_gnl_core

import qsm_maya.assembly.core as qsm_mya_asb_core

import qsm_maya.resource.core as qsm_mya_rsc_core

from .. import core as _core


class GpuInstanceOpt(qsm_mya_rsc_core.AssetCacheOpt):
    CACHE_ROOT = qsm_mya_gnl_core.ResourceCacheNodes.GpuInstanceRoot
    CACHE_NAME = qsm_mya_gnl_core.ResourceCacheNodes.GpuInstanceName

    def __init__(self, *args, **kwargs):
        super(GpuInstanceOpt, self).__init__(*args, **kwargs)

        cmds.loadPlugin('gpuCache', quiet=1)

    def load_cache(self, cache_file_path, hide_scenery=True):
        self.create_cache_root_auto()

        namespace = self._namespace
        cache_location_new = '{}|{}:{}'.format(self.CACHE_ROOT, namespace, self.CACHE_NAME)
        cache_location = '|{}:{}'.format(namespace, self.CACHE_NAME)
        if cmds.objExists(cache_location) is False and cmds.objExists(cache_location_new) is False:
            if os.path.isfile(cache_file_path) is True:
                qsm_mya_core.SceneFile.import_container_file(
                    cache_file_path, namespace=namespace
                )
                cmds.parent(cache_location, self.CACHE_ROOT)

                self.remove_resource_auto(hide_scenery)

    def remove_resource_auto(self, hide_scenery=True):
        if hide_scenery is True:
            cache_location = '{}|{}:{}'.format(self.CACHE_ROOT, self._namespace, self.CACHE_NAME)
            layer_name = '{}_dynamic_gpu_hide'.format(self._namespace)
            layer_path = cmds.createDisplayLayer(name=layer_name, number=1, empty=True)

            roots = qsm_mya_core.Namespace.find_roots(
                self._namespace
            )
            cmds.editDisplayLayerMembers(layer_path, *roots)
            cmds.setAttr(layer_path+'.visibility', False)

            cmds.container(cache_location, edit=1, force=1, addNode=[layer_path])
        else:
            self._resource.reference_opt.do_unload()

    def generate_args(self):
        file_path = self._resource.file
        cache_file_path = qsm_gnl_core.MayaCache.generate_asset_gpu_instance_file(
            file_path
        )
        if os.path.isfile(cache_file_path) is False:
            cmd_script = qsm_gnl_process.MayaCacheProcess.generate_cmd_script(
                'method=gpu-instance-cache-generate&file={}&cache_file={}'.format(
                    file_path,
                    cache_file_path,
                )
            )
            return cmd_script, cache_file_path
        return None, cache_file_path


class GpuInstanceProcess(object):
    LOG_KEY = 'gpu instance'

    @classmethod
    def create_gpu_transform(cls, path, hash_key):
        name = qsm_mya_core.DagNode.to_name(path)
        gpu_path = '{}|{}_GPU'.format(
            path, name
        )
        gpu_path_new = qsm_mya_core.Transform.create(
            gpu_path
        )
        qsm_mya_core.NodeAttribute.create_as_string(
            gpu_path_new, 'qsm_type', 'gpu_instance'
        )
        qsm_mya_core.NodeAttribute.create_as_string(
            gpu_path_new, 'qsm_hash_key', hash_key
        )
        qsm_mya_core.NodeDrawOverride.set_enable(
            gpu_path_new, True
        )
        qsm_mya_core.NodeDrawOverride.set_color(
            gpu_path_new, (.25, .5, 1.0)
        )
        return gpu_path_new

    def __init__(self, file_path, cache_file_path=None, gpu_unpack=True, auto_instance=True):
        cmds.loadPlugin('gpuCache', quiet=1)

        self._file_path = file_path

        self._directory_path = bsc_storage.StgFileOpt(
            self._file_path
        ).directory_path

        if cache_file_path is None:
            self._cache_file_path = qsm_gnl_core.MayaCache.generate_asset_gpu_instance_file(
                self._file_path
            )
        else:
            self._cache_file_path = cache_file_path

        self._cache_directory_path = bsc_storage.StgFileOpt(
            self._cache_file_path
        ).directory_path

        self._hash_key_dict = {}

        self._gpu_unpack = gpu_unpack
        self._auto_instance = auto_instance

    def grid_mesh_prc(self):
        paths = qsm_mya_core.Scene.find_all_dag_nodes(['mesh'])
        nodes = []
        list_for_grid = []
        for i_shape_path in paths:
            if qsm_mya_core.Node.is_mesh_type(i_shape_path) is True:
                i_mesh_opt = qsm_mya_core.MeshShapeOpt(i_shape_path)
                i_w, i_h, i_d = i_mesh_opt.get_dimension()
                i_s = max(i_w, i_h, i_d)
                if i_s < _core.Assembly.DIMENSION_MINIMUM:
                    list_for_grid.append(i_shape_path)

        if list_for_grid:
            mapper = qsm_mya_asb_core.GridSpace(list_for_grid, _core.Assembly.DIMENSION_MINIMUM).generate()
            keys = mapper.keys()
            keys.sort()
            for i_seq, i_key in enumerate(keys):
                i_hash_key = bsc_core.BscHash.to_hash_key(i_key)
                i_directory_path = '{}/region/{}'.format(
                    self._cache_directory_path, i_hash_key
                )
                i_group_path = '|region_{}_GRP'.format(i_seq)
                i_group_path_new = qsm_mya_core.Group.create(i_group_path)
                i_shape_paths = mapper[i_key]
                for j_shape_path in i_shape_paths:
                    # fixme: mesh parent mesh
                    if qsm_mya_core.DagNode.is_exists(j_shape_path) is False:
                        continue

                    j_transform_path = qsm_mya_core.Shape.get_transform(j_shape_path)
                    qsm_mya_core.Group.add(i_group_path_new, j_transform_path)

                i_gpu_file_path = '{}/gpu.abc'.format(
                    i_directory_path
                )
                if bsc_storage.StgFileOpt(i_gpu_file_path).get_is_file() is False:
                    i_mesh_file_path = '{}/mesh.mb'.format(
                        i_directory_path
                    )
                    # export to gpu and mesh
                    i_children = qsm_mya_core.Group.get_children(i_group_path_new)
                    qsm_mya_core.GpuCache.export_frame_(
                        i_gpu_file_path, i_children
                    )
                    qsm_mya_core.SceneFile.export_file(
                        i_mesh_file_path, i_children
                    )
                    qsm_mya_core.Node.delete(i_group_path_new)
                # create GPU
                i_gpu_transform_path = '|region_{}_GPU'.format(i_seq)
                i_gpu_transform_path_new = qsm_mya_core.Transform.create(i_gpu_transform_path)
                # create gpu
                qsm_mya_core.GpuCache.create(
                    i_gpu_file_path, i_gpu_transform_path_new
                )
                qsm_mya_core.NodeAttribute.create_as_string(
                    i_gpu_transform_path_new, 'qsm_type', 'gpu_instance'
                )
                qsm_mya_core.NodeAttribute.create_as_string(
                    i_gpu_transform_path_new, 'qsm_hash_key', i_hash_key
                )
                qsm_mya_core.NodeDrawOverride.set_enable(
                    i_gpu_transform_path_new, True
                )
                qsm_mya_core.NodeDrawOverride.set_color(
                    i_gpu_transform_path_new, (.25, .5, 1.0)
                )
                nodes.append(i_gpu_transform_path_new)

        return nodes

    def mesh_prc(self, shape_path):
        mesh_opt = qsm_mya_core.MeshShapeOpt(shape_path)
        face_count = qsm_mya_core.Mesh.get_face_number(shape_path)
        if face_count == 0:
            return

        if face_count < _core.Assembly.FACE_COUNT_MAXIMUM:
            return

        transform_path = mesh_opt.transform_path
        transform_name = mesh_opt.transform_name

        hash_key = mesh_opt.to_hash()
        unit_directory_path = '{}/unit/{}'.format(
            self._cache_directory_path, hash_key
        )
        gpu_transform_path = self.create_gpu_transform(
            transform_path, hash_key
        )

        if hash_key not in self._hash_key_dict:
            gpu_key = _core.Assembly.Keys.GPU
            gpu_file_path = '{}/{}.abc'.format(
                unit_directory_path, gpu_key
            )
            mesh_key = _core.Assembly.Keys.Mesh
            mesh_file_path = '{}/{}.ma'.format(
                unit_directory_path, mesh_key
            )
            # export gpu
            if bsc_storage.StgPath.get_is_file(gpu_file_path) is False:
                # to world
                transform_path_copy = qsm_mya_core.DagNode.copy_to_world(transform_path)
                transform_new_name = '{}_mesh'.format(transform_name)
                transform_path_new = qsm_mya_core.DagNode.rename(transform_path_copy, transform_new_name)
                qsm_mya_core.Transform.zero_transformations(transform_path_new)
                # gpu
                qsm_mya_core.GpuCache.export_frame(
                    gpu_file_path, transform_path_new
                )
                # mesh
                qsm_mya_core.SceneFile.export_file(
                    mesh_file_path, transform_path_new
                )
                # lod
                shape_path_new = qsm_mya_core.Transform.get_shape(transform_path_new)
                bsc_log.Log.trace_method_result(
                    self.LOG_KEY, 'create lod for: "{}", face count is {}'.format(
                        shape_path_new, face_count
                    )
                )
                # memory error when face more than 25000000
                if face_count <= 25000000:
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
                        i_gpu_key = _core.Assembly.Keys.GPU_LOD.format(i_level)
                        i_gpu_file_path_lod = '{}/{}.abc'.format(
                            unit_directory_path, i_gpu_key
                        )
                        qsm_mya_core.GpuCache.export_frame(
                            i_gpu_file_path_lod, transform_path_new
                        )
                        # mesh
                        i_mesh_key = _core.Assembly.Keys.Mesh_LOD.format(i_level)
                        i_mesh_file_path_lod = '{}/{}.ma'.format(
                            unit_directory_path, i_mesh_key
                        )
                        qsm_mya_core.SceneFile.export_file(
                            i_mesh_file_path_lod, transform_path_new
                        )

                qsm_mya_core.Node.delete(transform_path_new)
            #
            # if qsm_mya_core.Shape.is_instanced(shape_path):
            #     instanced_transform_paths = qsm_mya_core.Shape.get_instanced_transforms(shape_path)
            #     for i_transform_path in instanced_transform_paths:
            #         i_shape_path = qsm_mya_core.Transform.get_shape(i_transform_path)
            #         qsm_mya_core.Shape.remove_instanced(i_shape_path)
            #         qsm_mya_core.Transform.delete_all_shapes(i_transform_path)
            #
            #     gpu_shape_path = qsm_mya_core.GpuCache.create(
            #         gpu_file_path, gpu_transform_path
            #     )
            #     self._hash_key_dict[hash_key] = gpu_shape_path
            #     for i_transform_path in instanced_transform_paths:
            #         if i_transform_path != transform_path:
            #             i_gpu_transform_path = self.create_gpu_transform(
            #                 i_transform_path, hash_key
            #             )
            #             qsm_mya_core.Shape.instance_to(
            #                 gpu_shape_path, i_gpu_transform_path
            #             )
            # else:
            qsm_mya_core.Transform.delete_all_shapes(transform_path)
            # create gpu shape
            gpu_shape_path = qsm_mya_core.GpuCache.create(
                gpu_file_path, gpu_transform_path
            )
            self._hash_key_dict[hash_key] = gpu_shape_path
        else:
            qsm_mya_core.Transform.delete_all_shapes(transform_path)
            # instance gpu shape
            gpu_shape_path_src = self._hash_key_dict[hash_key]
            qsm_mya_core.Shape.instance_to(
                gpu_shape_path_src, gpu_transform_path
            )

    def execute(self):
        self._hash_key_dict = {}

        qsm_mya_core.SceneFile.new()

        container = '|{}'.format(GpuInstanceOpt.CACHE_NAME)

        qsm_mya_core.Container.create_as_default(container)
        qsm_mya_core.NodeAttribute.create_as_string(
            container, 'qsm_file', self._file_path
        )
        qsm_mya_core.NodeAttribute.create_as_string(
            container, 'qsm_cache', self._cache_file_path
        )

        bsc_log.Log.trace_method_result(
            self.LOG_KEY, 'import scene: {}'.format(self._file_path)
        )

        import_paths = qsm_mya_core.SceneFile.import_file(
            self._file_path
        )
        qsm_mya_core.Scene.clear_unknown_nodes()
        all_roots = qsm_mya_core.DagNode.find_roots(import_paths)
        # find lost reference first
        _core.GpuImport.find_all_gpu_caches(self._directory_path)
        qsm_mya_core.FileReferences.search_all_from(
            [self._directory_path], ignore_exists=True
        )
        # repair all instanced
        qsm_mya_core.Scene.remove_all_instanced(type_includes=['mesh', 'gpuCache'])
        # import all gpu
        _core.GpuImport().execute()
        # process
        mesh_paths = qsm_mya_core.Scene.find_all_dag_nodes(type_includes=['mesh'])
        with bsc_log.LogProcessContext.create(maximum=len(mesh_paths), label='gpu instance process') as g_p:
            for i_path in mesh_paths:
                self.mesh_prc(i_path)
                g_p.do_update()
        #
        grid_paths = self.grid_mesh_prc()
        if grid_paths:
            qsm_mya_core.Container.add_dag_nodes(container, grid_paths)
        # instance all mesh
        # _core.MeshInstance().execute()
        # remove unused groups
        qsm_mya_core.Scene.remove_all_empty_groups()
        # collection roots
        exists_roots = [x for x in all_roots if qsm_mya_core.Node.is_exists(x)]
        qsm_mya_core.Container.add_dag_nodes(container, exists_roots)

        qsm_mya_core.SceneFile.export_file(
            self._cache_file_path, container
        )
