# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.resource as bsc_resource

import lxbasic.storage as bsc_storage

from ... import core as _mya_core

from ...asset import core as _ast_core

from ...assembly import core as _asb_core


class UnitAssemblyGenerate(object):
    CACHE_NAME = 'unit_assembly_dgc'

    def __init__(self, namespace):
        self._namespace = namespace


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

    def mesh_prc(self, shape_path):
        mesh_opt = _mya_core.MeshOpt(shape_path)
        hash_key = mesh_opt.to_hash()
        transform_path = mesh_opt.transform_path
        transform_name = mesh_opt.transform_name

        unit_directory_path = '{}/unit/{}'.format(
            self._cache_directory_path, hash_key
        )
        ad_file_path = '{}/unit.AD.ma'.format(
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
            gpu_file_path = '{}/gpu.abc'.format(
                unit_directory_path
            )
            _mya_core.GpuCache.export_frame(
                gpu_file_path, transform_path_new
            )
            file_dict[_asb_core.UnitAssemblyQuery.Keys.GPU] = gpu_file_path
            # mesh
            mesh_file_path = '{}/mesh.ma'.format(
                unit_directory_path
            )
            _mya_core.SceneFile.export_file(
                mesh_file_path, transform_path_new
            )
            file_dict[_asb_core.UnitAssemblyQuery.Keys.Mesh] = mesh_file_path

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
                i_gpu_file_path_lod = '{}/gpu.lod{}.abc'.format(
                    unit_directory_path, i_level
                )
                _mya_core.GpuCache.export_frame(
                    i_gpu_file_path_lod, transform_path_new
                )
                file_dict[_asb_core.UnitAssemblyQuery.Keys.GPU_LOD.format(i_level)] = i_gpu_file_path_lod
                # mesh
                i_mesh_file_path_lod = '{}/mesh.lod{}.ma'.format(
                    unit_directory_path, i_level
                )
                _mya_core.SceneFile.export_file(
                    i_mesh_file_path_lod, transform_path_new
                )
                file_dict[_asb_core.UnitAssemblyQuery.Keys.Mesh_LOD.format(i_level)] = i_mesh_file_path_lod

            for i_key in _asb_core.UnitAssemblyQuery.Keys.All:
                if i_key in file_dict:
                    i_file_path = file_dict[i_key]
                    if i_key.startswith(_asb_core.UnitAssemblyQuery.Keys.Mesh):
                        _mya_core.AssemblyDefinition.add_scene(
                            ad_path, i_file_path, i_key
                        )
                    elif i_key.startswith(_asb_core.UnitAssemblyQuery.Keys.GPU):
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

        _mya_core.AssemblyReference.create(
            ad_file_path, ar_path
        )

    def gpu_prc(self, shape_path):
        gpu_file_path = _mya_core.Attribute.get_as_string(
            shape_path, 'cacheFileName'
        )
        shape_opt = _mya_core.ShapeOpt(shape_path)
        transform_path = shape_opt.transform_path
        if bsc_storage.StgPathMtd.get_is_file(gpu_file_path):
            paths = _mya_core.SceneFile.import_file(
                gpu_file_path
            )

            roots = _mya_core.DagNode.find_roots(paths)

            _mya_core.Transform.delete_all_shapes(transform_path)

            if roots:
                for i_path in roots:
                    if _mya_core.Node.is_transform(i_path):
                        _mya_core.DagNode.parent_to(i_path, transform_path)

        mesh_paths = _mya_core.DagNode.find_siblings(
            transform_path, ['mesh']
        )
        for i_path in mesh_paths:
            self.mesh_prc(i_path)

    def execute(self):
        _mya_core.SceneFile.new()

        container = '|{}'.format(UnitAssemblyGenerate.CACHE_NAME)

        _mya_core.Container.create_as_default(container)
        cmds.setAttr(container+'.blackBox', 1, lock=1)
        _mya_core.Attribute.create_as_string(
            container, 'qsm_file', self._file_path
        )
        _mya_core.Attribute.create_as_string(
            container, 'qsm_cache', self._cache_file_path
        )

        paths = _mya_core.SceneFile.import_file(
            self._file_path
        )
        # assembly
        roots = _mya_core.DagNode.find_roots(paths)
        # find lost reference first
        _mya_core.FileReferences.search_all_from(
            [self._directory_path]
        )
        # create assembly
        with bsc_log.LogProcessContext.create(maximum=len(paths), label='unit assembly process') as g_p:
            for i_path in paths:
                if _mya_core.Node.is_mesh(i_path) is True:
                    self.mesh_prc(i_path)
                elif _mya_core.Node.is_gpu(i_path) is True:
                    if self._gpu_unpack is True:
                        self.gpu_prc(i_path)

                g_p.do_update()
        # export assembly
        exists_roots = [i for i in roots if _mya_core.Node.is_exists(i)]

        for i_root in exists_roots:
            _mya_core.DagNode.parent_to(
                i_root, container
            )

        _mya_core.SceneFile.export_file(
            self._cache_file_path, container
        )


class GpuInstanceGenerate(object):
    CACHE_NAME = 'gpu_instance_dgc'

    def __init__(self, namespace):
        self._namespace = namespace


class GpuInstanceProcess(object):
    def __init__(self, file_path, cache_file_path=None, gpu_unpack=True, auto_instance=True):
        self._file_path = file_path

        self._directory_path = bsc_storage.StgFileOpt(
            self._file_path
        ).directory_path

        if cache_file_path is None:
            self._cache_file_path = _ast_core.AssetCache.generate_gpu_instance_file(
                self._file_path
            )
        else:
            self._cache_file_path = cache_file_path

        self._cache_directory_path = bsc_storage.StgFileOpt(
            self._cache_file_path
        ).directory_path

        self._hash_dict = {}

        self._gpu_unpack = gpu_unpack
        self._auto_instance = auto_instance

    def mesh_prc(self, shape_path):
        mesh_opt = _mya_core.MeshOpt(shape_path)

        transform_path = mesh_opt.transform_path
        transform_name = mesh_opt.transform_name

        hash_key = mesh_opt.to_hash()
        unit_directory_path = '{}/unit/{}'.format(
            self._cache_directory_path, hash_key
        )
        gpu_file_path = '{}/gpu.abc'.format(
            unit_directory_path
        )
        mesh_file_path = '{}/mesh.ma'.format(
            unit_directory_path
        )
        #
        _mya_core.Attribute.create_as_string(
            transform_path, 'qsm_gpu', gpu_file_path
        )
        _mya_core.Attribute.create_as_string(
            transform_path, 'qsm_mesh', mesh_file_path
        )
        if hash_key not in self._hash_dict:
            # export gpu
            if bsc_storage.StgPathMtd.get_is_file(gpu_file_path) is False:
                transform_path_copy = _mya_core.DagNode.copy_to_world(transform_path)
                transform_new_name = '{}_mesh'.format(transform_name)
                transform_path_new = _mya_core.DagNode.rename(transform_path_copy, transform_new_name)
                _mya_core.Transform.zero_transformations(transform_path_new)
                # gpu
                _mya_core.GpuCache.export_frame(
                    gpu_file_path, transform_path_new
                )
                # mesh
                _mya_core.SceneFile.export_file(
                    mesh_file_path, transform_path_new
                )
                _mya_core.Node.delete(transform_path_new)
            #
            if _mya_core.Shape.is_instanced(shape_path):
                instanced_transform_paths = _mya_core.Shape.get_instanced_transforms(shape_path)
                for i_transform_path in instanced_transform_paths:
                    i_shape_path = _mya_core.Transform.get_shape_path(i_transform_path)
                    _mya_core.Shape.remove_instanced(i_shape_path)
                    _mya_core.Transform.delete_all_shapes(i_transform_path)
                #
                gpu_path = _mya_core.GpuCache.create(
                    gpu_file_path, transform_path
                )
                self._hash_dict[hash_key] = gpu_path
                for i_transform_path in instanced_transform_paths:
                    if i_transform_path != transform_path:
                        _mya_core.Shape.instance_to(
                            gpu_path, i_transform_path
                        )
            else:
                _mya_core.Transform.delete_all_shapes(transform_path)
                # create gpu shape
                gpu_path = _mya_core.GpuCache.create(
                    gpu_file_path, transform_path
                )
                self._hash_dict[hash_key] = gpu_path
        else:
            _mya_core.Transform.delete_all_shapes(transform_path)
            # instance gpu shape
            gpu_path = self._hash_dict[hash_key]
            _mya_core.Shape.instance_to(
                gpu_path, transform_path
            )

    def gpu_prc(self, shape_path):
        gpu_file_path = _mya_core.Attribute.get_as_string(
            shape_path, 'cacheFileName'
        )
        shape_opt = _mya_core.ShapeOpt(shape_path)
        transform_path = shape_opt.transform_path
        _mya_core.Attribute.create_as_boolean(
            transform_path, 'qsm_gpu_expand', False
        )
        expand_group_path = '{}|gpu_expand_grp'.format(transform_path)
        _mya_core.Group.create(expand_group_path)
        if bsc_storage.StgPathMtd.get_is_file(gpu_file_path):
            paths = _mya_core.SceneFile.import_file(
                gpu_file_path
            )

            roots = _mya_core.DagNode.find_roots(paths)

            _mya_core.Transform.hide_all_shapes(transform_path)

            if roots:
                for i_path in roots:
                    if _mya_core.Node.is_transform(i_path):
                        # _mya_core.Connection.create(
                        #    transform_path+'.qsm_gpu_expand', i_path+'.overrideVisibility'
                        # )
                        # _mya_core.NodeDrawOverride.set_enable(i_path, True)
                        #
                        meshes = _mya_core.Group.find_siblings(i_path, ['mesh'])
                        for j_shape_path in meshes:
                            j_transform_path = _mya_core.Shape.get_transform(j_shape_path)
                            _mya_core.DagNode.parent_to(j_transform_path, expand_group_path)

                        if _mya_core.Node.is_exists(i_path):
                            _mya_core.Node.delete(i_path)

        mesh_paths = _mya_core.DagNode.find_siblings(
            transform_path, ['mesh']
        )
        for i_path in mesh_paths:
            self.mesh_prc(i_path)

    def execute(self):
        self._hash_dict = {}

        _mya_core.SceneFile.new()

        container = '|{}'.format(GpuInstanceGenerate.CACHE_NAME)

        _mya_core.Container.create_as_default(container)
        # cmds.setAttr(container+'.blackBox', 1, lock=1)
        _mya_core.Attribute.create_as_string(
            container, 'qsm_file', self._file_path
        )
        _mya_core.Attribute.create_as_string(
            container, 'qsm_cache', self._cache_file_path
        )

        paths = _mya_core.SceneFile.import_file(
            self._file_path
        )
        # assembly
        roots = _mya_core.DagNode.find_roots(paths)
        # find lost reference first
        _mya_core.FileReferences.search_all_from(
            [self._directory_path]
        )
        # create assembly
        with bsc_log.LogProcessContext.create(maximum=len(paths), label='gpu instance process') as g_p:
            for i_path in paths:
                if _mya_core.Node.is_mesh(i_path) is True:
                    self.mesh_prc(i_path)
                elif _mya_core.Node.is_gpu(i_path) is True:
                    if self._gpu_unpack is True:
                        self.gpu_prc(i_path)

                g_p.do_update()
        # export assembly
        exists_roots = [i for i in roots if _mya_core.Node.is_exists(i)]

        for i_root in exists_roots:
            _mya_core.DagNode.parent_to(
                i_root, container
            )

        _mya_core.SceneFile.export_file(
            self._cache_file_path, container
        )


class DynamicCameraMask(object):
    CONTAINER_NAME = 'camera_mask_dgc'

    CAMERA_FRUSTUM = '|__CAMERA_FRUSTUM__'

    def __init__(self, camera=None, frame=None):
        if camera is None:
            self._camera_path = _mya_core.Camera.get_active()
        else:
            self._camera_path = _mya_core.DagNode.to_path(camera)

        if not self._camera_path:
            raise RuntimeError()

        self._frame = frame

        self._unit_cache = {}

        self._node_cache = {}

    def create_camera_frustum(self, container):
        _mya_core.SceneFile.import_file(
            bsc_resource.ExtendResource.get('rig/camera_frustum.ma')
        )
        transform_path = _mya_core.Shape.get_transform(self._camera_path)
        name = self._camera_path.split('|')[-1]
        frustum_name = '{}_fst'.format(name)
        eps_name = '{}_eps'.format(name)
        frustum_transform_path = _mya_core.DagNode.rename(
            self.CAMERA_FRUSTUM, frustum_name
        )
        eps_script = (
            '$f = {camera}.focalLength;\n'
            '$fbw = {camera}.horizontalFilmAperture*25.4;\n'
            '$w = defaultResolution.width;\n'
            '$h = defaultResolution.height;\n'
            '{box}.scaleZ = {camera}.farClipPlane*.1;\n'
            '{box}.scaleX = $fbw/$f*{box}.scaleZ;\n'
            '{box}.scaleY = $fbw/$f*{box}.scaleZ*(($h*1.0)/($w*1.0));'
        ).format(
            camera=self._camera_path, box=frustum_transform_path
        )
        _mya_core.ParentConstraint.create(transform_path, frustum_transform_path)
        _mya_core.Expression.create(
            eps_name, eps_script, frustum_transform_path
        )
        material = _mya_core.Material.create(
            'test_mtl'
        )
        shader = _mya_core.Shader.create(
            'test_sdr', 'surfaceShader'
        )
        _mya_core.Material.assign_surface_shader(
            material, shader
        )
        _mya_core.Material.assign_to(
            material, frustum_transform_path
        )

        _mya_core.Attribute.set_as_tuple(
            shader, 'outTransparency', (.975, .975, .975)
        )
        _mya_core.Attribute.set_as_tuple(
            shader, 'outColor', (1, 0.25, 0)
        )

        _mya_core.Connection.create(
            container+'.qsm_camera_frustum_enable', frustum_transform_path+'.visibility'
        )

        _mya_core.Container.add_dag_nodes(container, [frustum_transform_path])
        _mya_core.Container.add_nodes(container, [eps_name])

    def find_units_at_frame(self, frame):
        _mya_core.Frame.set_current(frame)

        results = _mya_core.Camera.generate_mask_nodes(
            self._camera_path
        )

        mask_units = []
        for i_path in results:
            if i_path in self._unit_cache:
                i_unit_path = self._unit_cache[i_path]
            else:
                i_unit_path = _asb_core.UnitAssemblyQuery.find_unit(i_path)
                self._unit_cache[i_path] = i_unit_path

            if i_unit_path is None:
                continue

            mask_units.append(i_unit_path)

        return mask_units

    def create_container(self, namespace=None):
        if namespace is not None:
            path = '|{}:{}'.format(namespace, self.CONTAINER_NAME)
        else:
            path = '|{}'.format(self.CONTAINER_NAME)
        _mya_core.Container.create_as_expression(
            path
        )
        _mya_core.Attribute.create_as_boolean(
            path, 'qsm_camera_mask_enable'
        )
        _mya_core.Attribute.create_as_boolean(
            path, 'qsm_camera_frustum_enable'
        )
        cmds.setAttr(path+'.blackBox', 1, lock=1)
        return path

    @classmethod
    def pre_execute(cls, all_unit_paths, container):
        nodes = []
        for i_idx, i_unit_path in enumerate(all_unit_paths):
            _mya_core.Connection.create(
                container+'.qsm_camera_mask_enable', i_unit_path+'.overrideEnabled'
            )
            i_name = i_unit_path.split('|')[-1].replace(':', '__')
            i_sum_name = '{}_sum'.format(i_name)
            _mya_core.Node.create(
                i_sum_name, 'plusMinusAverage'
            )
            nodes.append(i_sum_name)

        _mya_core.Container.add_nodes(container, nodes)

    @classmethod
    def post_execute(cls, all_units, container):
        for i_unit_path in all_units:
            i_name = i_unit_path.split('|')[-1].replace(':', '__')
            i_sum_name = '{}_sum'.format(i_name)
            _mya_core.Connection.create(
                i_sum_name+'.output1D', i_unit_path+'.overrideVisibility'
            )

        _mya_core.Attribute.set_value(
            container, 'qsm_camera_mask_enable', True
        )

    def execute(self):
        self._unit_cache = {}

        container = self.create_container()

        all_units = _asb_core.UnitAssemblyQuery.get_all_units()
        self.pre_execute(all_units, container)

        start_frame, end_frame = _mya_core.Frame.auto_range(self._frame)
        frames = range(start_frame, end_frame+1)

        nodes = []

        tuc = _mya_core.Node.create(
            'camera_mask_tuc', 'timeToUnitConversion'
        )
        _mya_core.Attribute.set_value(
            tuc, 'conversionFactor', 0.004
        )
        _mya_core.Connection.create(
            'time1.outTime', tuc+'.input'
        )
        nodes.append(tuc)

        for i_seq, i_frame in enumerate(frames):
            i_units = self.find_units_at_frame(i_frame)

            i_cdt_name = 'camera_mask_cdt_{}'.format(i_frame)
            _mya_core.Node.create(
                i_cdt_name, 'condition'
            )
            cmds.setAttr('{}.firstTerm'.format(i_cdt_name), i_frame)
            cmds.connectAttr(tuc+'.output', i_cdt_name+'.secondTerm')
            cmds.setAttr('{}.colorIfTrueR'.format(i_cdt_name), 1.0)
            cmds.setAttr('{}.colorIfFalseR'.format(i_cdt_name), 0.0)
            nodes.append(i_cdt_name)
            for j_unit_path in i_units:
                j_name = j_unit_path.split('|')[-1].replace(':', '__')
                j_sum_name = '{}_sum'.format(j_name)
                _mya_core.Connection.create(
                    i_cdt_name+'.outColor.outColorR', j_sum_name+'.input1D[{}]'.format(i_seq)
                )
        _mya_core.Container.add_nodes(container, nodes)

        self.post_execute(all_units, container)
        self.create_camera_frustum(container)

    def find_nodes_at_frame(self, frame):
        _mya_core.Frame.set_current(frame)

        results = _mya_core.Camera.generate_mask_nodes(
            self._camera_path
        )
        return results

    def nodes_pre_prc(self, all_shapes, namespace):
        for i_index, i_shape_path in enumerate(all_shapes):
            i_sum_name = '{}:camera_mask_{}_sum'.format(namespace, i_index)
            _mya_core.Node.create(
                i_sum_name, 'plusMinusAverage'
            )
            self._node_cache[i_shape_path] = i_sum_name

    def nodes_post_prc(self, container):
        for i_shape_path, v in self._node_cache.items():

            if _mya_core.Reference.get_is_from_reference(i_shape_path) is True:
                _mya_core.Connection.create(
                    v+'.output1D', i_shape_path+'.visibility'
                )
            else:
                i_transform_path = _mya_core.Shape.get_transform(i_shape_path)
                _mya_core.NodeDrawOverride.set_enable(
                    i_transform_path, True
                )
                _mya_core.Connection.create(
                    v+'.output1D', i_transform_path+'.overrideVisibility'
                )
                _mya_core.Connection.create(
                    container+'.qsm_camera_mask_enable', i_transform_path+'.overrideEnabled'
                )

        _mya_core.Attribute.set_value(
            container, 'qsm_camera_mask_enable', True
        )

    def execute_for(self, namespace):
        container = self.create_container(namespace)

        start_frame, end_frame = _mya_core.Frame.auto_range(self._frame)
        frames = range(start_frame, end_frame+1)

        self._node_cache = {}

        all_shapes = _mya_core.Namespace.find_all_dag_nodes(namespace, type_includes=['mesh', 'gpuCache'])
        self.nodes_pre_prc(all_shapes, namespace)

        nodes = []

        tuc = _mya_core.Node.create(
            'camera_mask_tuc', 'timeToUnitConversion'
        )
        _mya_core.Attribute.set_value(
            tuc, 'conversionFactor', 0.004
        )
        _mya_core.Connection.create(
            'time1.outTime', tuc+'.input'
        )
        nodes.append(tuc)
        
        for i_seq, i_frame in enumerate(frames):
            i_cdt_name = '{}:camera_mask_{}_cdt'.format(namespace, i_frame)
            _mya_core.Node.create(
                i_cdt_name, 'condition'
            )
            cmds.setAttr('{}.firstTerm'.format(i_cdt_name), i_frame)
            cmds.connectAttr(tuc+'.output', i_cdt_name+'.secondTerm')
            cmds.setAttr('{}.colorIfTrueR'.format(i_cdt_name), 1.0)
            cmds.setAttr('{}.colorIfFalseR'.format(i_cdt_name), 0.0)
            nodes.append(i_cdt_name)

            i_nodes = self.find_nodes_at_frame(i_frame)
            for j_path in i_nodes:
                if j_path in self._node_cache:
                    j_sum_name = self._node_cache[j_path]
                    nodes.append(j_sum_name)
                    _mya_core.Connection.create(
                        i_cdt_name+'.outColor.outColorR', j_sum_name+'.input1D[{}]'.format(i_seq)
                    )

        _mya_core.Container.add_nodes(container, list(set(nodes)))

        self.nodes_post_prc(container)
        self.create_camera_frustum(container)


class CameraMask(object):
    LAYER_NAME = 'camera_mask_hide'

    def __init__(self, camera=None, frame=None):
        if camera is None:
            self._camera_path = _mya_core.Camera.get_active()
        else:
            self._camera_path = _mya_core.DagNode.to_path(camera)

        self._frame = frame

    def find_units_at_frame(self, frame):
        _mya_core.Frame.set_current(frame)

        results = _mya_core.Camera.generate_mask_nodes(
            self._camera_path
        )

        mask_unit_paths = []
        for i_path in results:
            i_unit_path = _asb_core.UnitAssemblyQuery.find_unit(i_path)
            if i_unit_path is None:
                continue
            mask_unit_paths.append(i_unit_path)

        return mask_unit_paths

    def restore(self):
        if _mya_core.Node.is_exists(self.LAYER_NAME):
            _mya_core.Node.delete(
                self.LAYER_NAME
            )

    def execute(self):
        self.restore()

        mask_unit_paths = set()
        start_frame, end_frame = _mya_core.Frame.auto_range(self._frame)
        frames = range(start_frame, end_frame+1)
        all_units = _asb_core.UnitAssemblyQuery.get_all_units()

        for i_frame in frames:
            i_units = self.find_units_at_frame(i_frame)
            mask_unit_paths.update(set(i_units))

        hide_unit_paths = list(set(all_units) - set(mask_unit_paths))

        if hide_unit_paths:
            layer = _mya_core.DisplayLayer.create(
                self.LAYER_NAME
            )
            _mya_core.DisplayLayer.add_nodes(layer, hide_unit_paths)
            _mya_core.DisplayLayer.set_visible(layer, False)

    def restore_for(self, namespace):
        pass

    def find_nodes_at_frame(self, frame):
        _mya_core.Frame.set_current(frame)

        return _mya_core.Camera.generate_mask_nodes(
            self._camera_path, type_includes=['mesh', 'gpuCache']
        )

    def create_layer(self, namespace=None):
        if namespace is not None:
            layer_name = '{}:{}'.format(namespace, self.LAYER_NAME)
        else:
            layer_name = self.LAYER_NAME
        layer = _mya_core.DisplayLayer.create(
            layer_name
        )
        return layer

    def execute_for(self, namespace):
        layer = self.create_layer(namespace)

        mask_nodes = set()
        start_frame, end_frame = _mya_core.Frame.auto_range(self._frame)
        frames = range(start_frame, end_frame+1)
        all_nodes = _mya_core.Namespace.find_all_dag_nodes(namespace, type_includes=['mesh', 'gpuCache'])

        for i_frame in frames:
            i_nodes = self.find_nodes_at_frame(i_frame)
            mask_nodes.update(set(i_nodes))

        hide_nodes = list(set(all_nodes)-set(mask_nodes))

        if hide_nodes:
            _mya_core.DisplayLayer.add_nodes(layer, [_mya_core.Shape.get_transform(x) for x in hide_nodes])
            _mya_core.DisplayLayer.set_visible(layer, False)
