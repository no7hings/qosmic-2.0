# coding:utf-8
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.resource as bsc_resource

import lxbasic.storage as bsc_storage

from ... import core as _mya_core

from ...asset import core as _ast_core

from .. import core as _scn_core

from ...resource import core as _rsc_core

from ...assembly import core as _asb_core


class UnitAssemblyOpt(_rsc_core.ResourceScriptOpt):
    CACHE_NAME = 'unit_assembly_dgc'

    CACHE_ROOT = '|__UNIT_ASSEMBLY__'

    def __init__(self, resource):
        super(UnitAssemblyOpt, self).__init__(resource)

    def load_cache(self, cache_file_path):
        self.create_cache_root_auto()

        namespace = self._namespace
        cache_location_new = '{}|{}:{}'.format(self.CACHE_ROOT, namespace, self.CACHE_NAME)
        cache_location = '|{}:{}'.format(namespace, self.CACHE_NAME)
        if cmds.objExists(cache_location) is False and cmds.objExists(cache_location_new) is False:
            if os.path.isfile(cache_file_path) is True:
                _mya_core.SceneFile.import_container_file(
                    cache_file_path, namespace=namespace
                )
                cmds.parent(cache_location, self.CACHE_ROOT)

                self.hide_resource_auto()

    def hide_resource_auto(self):
        self._resource.reference_opt.do_unload()

    def generate_args(self):
        file_path = self._resource.file
        cache_file_path = _ast_core.AssetCache.generate_unit_assembly_file(
            file_path
        )
        if os.path.isfile(cache_file_path) is False:
            cmd_script = _ast_core.MayaCacheProcess.generate_command(
                'method=unit-assembly-cache-generate&file={}&cache_file={}'.format(
                    file_path,
                    cache_file_path,
                )
            )
            return cmd_script, cache_file_path
        return None, cache_file_path


class UnitAssemblyProcess(object):

    def __init__(self, file_path, cache_file_path=None, gpu_unpack=True):
        self._file_path = file_path

        self._directory_path = bsc_storage.StgFileOpt(
            self._file_path
        ).directory_path

        if cache_file_path is None:
            self._cache_file_path = _ast_core.AssetCache.generate_unit_assembly_file(
                self._file_path
            )
        else:
            self._cache_file_path = cache_file_path

        self._cache_directory_path = bsc_storage.StgFileOpt(
            self._cache_file_path
        ).directory_path

        self._gpu_unpack = gpu_unpack

    def grid_mesh_prc(self):
        paths = _mya_core.Scene.find_all_dag_nodes(['mesh'])
        nodes = []
        list_for_grid = []
        for i_shape_path in paths:
            if _mya_core.Node.is_mesh(i_shape_path) is True:
                i_mesh_opt = _mya_core.MeshOpt(i_shape_path)
                i_w, i_h, i_d = i_mesh_opt.get_dimension()
                i_s = max(i_w, i_h, i_d)
                if i_s < _scn_core.Assembly.DIMENSION_MINIMUM:
                    list_for_grid.append(i_shape_path)

        if list_for_grid:
            mapper = _asb_core.GridSpace(list_for_grid, _scn_core.Assembly.DIMENSION_MINIMUM).generate()
            keys = mapper.keys()
            keys.sort()
            for i_seq, i_key in enumerate(keys):
                i_hash_key = bsc_core.HashMtd.to_hash_key(i_key)
                i_directory_path = '{}/region/{}'.format(
                    self._cache_directory_path, i_hash_key
                )
                i_ad_file_path = '{}/AD.ma'.format(
                    i_directory_path
                )
                if bsc_storage.StgFileOpt(i_ad_file_path).get_is_file() is False:
                    i_gpu_file_path = '{}/gpu.abc'.format(
                        i_directory_path
                    )
                    i_mesh_file_path = '{}/mesh.ma'.format(
                        i_directory_path
                    )

                    i_group_path = '|region_{}_GRP'.format(i_seq)
                    i_group_path_new = _mya_core.Group.create(i_group_path)
                    i_shape_paths = mapper[i_key]
                    for j_shape_path in i_shape_paths:
                        j_transform_path = _mya_core.Shape.get_transform(j_shape_path)
                        _mya_core.Group.add(i_group_path_new, j_transform_path)
                    # export to gpu and mesh
                    i_children = _mya_core.Group.get_children(i_group_path_new)
                    _mya_core.GpuCache.export_frame_(
                        i_gpu_file_path, i_children
                    )
                    _mya_core.SceneFile.export_file(
                        i_mesh_file_path, i_children
                    )
                    _mya_core.Node.delete(i_group_path_new)
                    # create AD
                    i_ad_path = '|region_{}_AD'.format(i_seq)
                    # ad
                    _mya_core.AssemblyDefinition.create(
                        i_ad_path
                    )
                    _mya_core.AssemblyDefinition.add_cache(
                        i_ad_path, i_gpu_file_path, 'gpu'
                    )
                    _mya_core.AssemblyDefinition.add_scene(
                        i_ad_path, i_mesh_file_path, 'mesh'
                    )
                    _mya_core.SceneFile.export_file(
                        i_ad_file_path, i_ad_path
                    )
                    _mya_core.Node.delete(i_ad_path)

                i_ar_path = '|region_{}_AR'.format(i_seq)
                i_ar_path_new = _mya_core.AssemblyReference.create(
                    i_ad_file_path, i_ar_path
                )
                _mya_core.NodeAttribute.create_as_string(
                    i_ar_path_new, 'qsm_type', 'unit_assembly'
                )
                _mya_core.NodeAttribute.create_as_string(
                    i_ar_path_new, 'qsm_hash_key', i_hash_key
                )
                _mya_core.NodeDrawOverride.set_enable(
                    i_ar_path_new, True
                )
                _mya_core.NodeDrawOverride.set_color(
                    i_ar_path_new, (1.0, .5, .25)
                )
                nodes.append(i_ar_path_new)

        return nodes

    def mesh_prc(self, shape_path):
        mesh_opt = _mya_core.MeshOpt(shape_path)
        face_count = mesh_opt.get_face_number()
        if face_count < _scn_core.Assembly.FACE_COUNT_MAXIMUM:
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

        if bsc_storage.StgPathMtd.get_is_file(ad_file_path) is False:
            file_dict = {}

            transform_path_copy = _mya_core.DagNode.copy_to_world(transform_path)

            transform_new_name = '{}_mesh'.format(transform_name)
            transform_path_new = _mya_core.DagNode.rename(transform_path_copy, transform_new_name)

            ad_path = '|{}_AD'.format(transform_name)

            _mya_core.Transform.zero_transformations(transform_path_new)
            # gpu
            gpu_key = _scn_core.Assembly.Keys.GPU
            gpu_file_path = '{}/{}.abc'.format(
                unit_directory_path, gpu_key
            )
            _mya_core.GpuCache.export_frame(
                gpu_file_path, transform_path_new
            )
            file_dict[gpu_key] = gpu_file_path
            # mesh
            mesh_key = _scn_core.Assembly.Keys.Mesh
            mesh_file_path = '{}/{}.ma'.format(
                unit_directory_path, mesh_key
            )
            _mya_core.SceneFile.export_file(
                mesh_file_path, transform_path_new
            )
            file_dict[mesh_key] = mesh_file_path

            _mya_core.AssemblyDefinition.create(
                ad_path
            )

            for i_seq in range(2):
                i_level = i_seq+1
                shape_path_new = _mya_core.Transform.get_shape_path(transform_path_new)
                # todo: may be mesh had lamina or non-manifold
                # noinspection PyBroadException
                try:
                    _mya_core.MeshReduce.reduce_off(shape_path_new, 50)
                except Exception:
                    bsc_log.Log.trace_method_error(
                        'mesh reduce', 'mesh "{}" had lamina or non-manifold faces or vertices'.format(
                            shape_path_new
                        )
                    )
                # gpu
                i_gpu_key = _scn_core.Assembly.Keys.GPU_LOD.format(i_level)
                i_gpu_file_path_lod = '{}/{}.abc'.format(
                    unit_directory_path, i_gpu_key
                )
                _mya_core.GpuCache.export_frame(
                    i_gpu_file_path_lod, transform_path_new
                )
                file_dict[i_gpu_key] = i_gpu_file_path_lod
                # mesh
                i_mesh_key = _scn_core.Assembly.Keys.Mesh_LOD.format(i_level)
                i_mesh_file_path_lod = '{}/{}.ma'.format(
                    unit_directory_path, i_mesh_key
                )
                _mya_core.SceneFile.export_file(
                    i_mesh_file_path_lod, transform_path_new
                )
                file_dict[i_mesh_key] = i_mesh_file_path_lod
            # add attribute
            for i_key in _scn_core.Assembly.Keys.All:
                if i_key in file_dict:
                    i_file_path = file_dict[i_key]
                    if i_key.startswith(_scn_core.Assembly.Keys.Mesh):
                        _mya_core.AssemblyDefinition.add_scene(
                            ad_path, i_file_path, i_key
                        )
                    elif i_key.startswith(_scn_core.Assembly.Keys.GPU):
                        _mya_core.AssemblyDefinition.add_cache(
                            ad_path, i_file_path, i_key
                        )

            _mya_core.Node.delete(transform_path_new)

            _mya_core.SceneFile.export_file(
                ad_file_path, ad_path
            )

            _mya_core.Node.delete(ad_path)

        _mya_core.Transform.delete_all_shapes(transform_path)

        ar_path = '{}|{}_AR'.format(transform_path, transform_name)

        ar_path_new = _mya_core.AssemblyReference.create(
            ad_file_path, ar_path
        )
        _mya_core.NodeAttribute.create_as_string(
            ar_path_new, 'qsm_type', 'unit_assembly'
        )
        _mya_core.NodeAttribute.create_as_string(
            ar_path_new, 'qsm_hash_key', hash_key
        )
        _mya_core.NodeDrawOverride.set_enable(
            ar_path_new, True
        )
        _mya_core.NodeDrawOverride.set_color(
            ar_path_new, (1.0, .5, .25)
        )

    def execute(self):
        _mya_core.SceneFile.new()

        container = '|{}'.format(UnitAssemblyOpt.CACHE_NAME)

        _mya_core.Container.create_as_default(container)
        _mya_core.NodeAttribute.create_as_string(
            container, 'qsm_file', self._file_path
        )
        _mya_core.NodeAttribute.create_as_string(
            container, 'qsm_cache', self._cache_file_path
        )

        import_paths = _mya_core.SceneFile.import_file(
            self._file_path
        )
        _mya_core.Scene.clear_unknown_nodes()
        all_roots = _mya_core.DagNode.find_roots(import_paths)
        # find lost reference first
        _mya_core.FileReferences.search_all_from(
            [self._directory_path]
        )
        # repair all instanced
        _mya_core.Scene.remove_all_instanced(type_includes=['mesh', 'gpuCache'])
        # import all gpu
        _scn_core.GpuImport().execute()
        # process
        mesh_paths = _mya_core.Scene.find_all_dag_nodes(type_includes=['mesh'])
        count = len(mesh_paths)
        with bsc_log.LogProcessContext.create(maximum=len(mesh_paths), label='unit assembly process') as g_p:
            for i_path in mesh_paths:
                self.mesh_prc(i_path)
                g_p.do_update()
        #
        grid_paths = self.grid_mesh_prc()
        if grid_paths:
            _mya_core.Container.add_dag_nodes(container, grid_paths)
        # instance all mesh
        # _scn_core.MeshInstance(material=True).execute()
        # remove unused groups
        _mya_core.Scene.remove_all_empty_groups()
        # collection roots
        exists_roots = [i for i in all_roots if _mya_core.Node.is_exists(i)]
        _mya_core.Container.add_dag_nodes(container, exists_roots)

        _mya_core.SceneFile.export_file(
            self._cache_file_path, container
        )

