# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

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

    def __init__(self, file_path, cache_file_path=None):
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

            transform_path_copy = _mya_core.NodeDag.copy_to_world(transform_path)

            transform_new_name = '{}_mesh'.format(transform_name)
            transform_path_new = _mya_core.NodeDag.rename(transform_path_copy, transform_new_name)

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
                shape_path_copy = _mya_core.Transform.get_shape_path(transform_path_new)
                _mya_core.MeshReduce.reduce_off(shape_path_copy, 50)
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

        location = '|{}'.format(UnitAssemblyGenerate.CACHE_NAME)

        _mya_core.Container.create_as_default(location)

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
        exists_roots = [i for i in roots if _mya_core.Node.is_exists(i)]

        for i_root in exists_roots:
            _mya_core.NodeDag.parent_to(
                i_root, location
            )

        _mya_core.SceneFile.export_file(
            self._cache_file_path, location
        )


class UnitAssemblyCameraMask(object):
    CONTAINER_NAME = 'camera_mask_dgc'

    CAMERA_FRUSTUM = '|__CAMERA_FRUSTUM__'

    def __init__(self, camera=None):
        if camera is None:
            self._camera_path = _mya_core.Camera.get_active()
        else:
            self._camera_path = _mya_core.NodeDag.to_path(camera)

    def get_units_at_frame(self, frame):
        _mya_core.Frame.set_current(frame)

        mask_nodes = _mya_core.Camera.generate_mask_nodes(
            self._camera_path
        )

        mask_unit_paths = []
        for i_path in mask_nodes:
            i_unit_path = _asb_core.UnitAssemblyQuery.find_unit(i_path)
            if i_unit_path is None:
                continue
            mask_unit_paths.append(i_unit_path)

        return mask_unit_paths

    def create_container(self):
        path = '|{}'.format(self.CONTAINER_NAME)
        _mya_core.Container.create_as_expression(
            path
        )
        _mya_core.Attribute.add_as_boolean(
            path, 'qsm_camera_mask_enable'
        )
        _mya_core.Attribute.add_as_boolean(
            path, 'qsm_camera_frustum_enable'
        )
        return path

    def pre_execute(self, unit_paths):
        for i_unit_path in unit_paths:
            _mya_core.NodeDrawOverride.set_enable(
                i_unit_path, True
            )
            i_eps_name = self.to_expression_name(i_unit_path)
            if _mya_core.Node.is_exists(i_eps_name) is False:
                i_eps = _mya_core.Expression.create(
                    i_eps_name, '', i_unit_path
                )
                _mya_core.Attribute.add_as_string(
                    i_eps, 'qsm_camera_mask_frames', ''
                )

    def to_expression_name(self, unit_path):
        unit_name = unit_path.split('|')[-1]
        return '{}_eps'.format(unit_name.replace(':', '__'))

    def post_execute(self, unit_paths, container):
        nodes = []
        for i_unit_path in unit_paths:
            i_eps_name = self.to_expression_name(i_unit_path)
            i_eps_script = (
                '$enable = {container}.qsm_camera_mask_enable;\n'
                'string $str1 = `getAttr("{expression}.qsm_camera_mask_frames")`;\n'
                'string $str2 = frame;\n'
                'if ($enable ==1) {{\n'
                '    if (`gmatch $str1 ("*(" + $str2 + ")*")`) {{\n'
                '        {node}.overrideVisibility=1;\n'
                '    }} else {{\n'
                '        {node}.overrideVisibility=0;\n'
                '    }};\n'
                '}} else {{\n'
                '    {node}.overrideVisibility=1;\n'
                '}};'
            ).format(
                container=container,
                expression=i_eps_name,
                node=i_unit_path
            )
            _mya_core.Expression.set_script(i_eps_name, i_eps_script)
            nodes.append(i_eps_name)

        _mya_core.Attribute.set_value(
            container, 'qsm_camera_mask_enable', True
        )
        _mya_core.Container.add_nodes(container, nodes)

    def create_camera_frustum(self, container):
        _mya_core.SceneFile.import_file(
            bsc_resource.ExtendResource.get('rig/camera_frustum.ma')
        )
        transform_path = _mya_core.Shape.get_transform(self._camera_path)
        name = self._camera_path.split('|')[-1]
        frustum_name = '{}_fst'.format(name)
        eps_name = '{}_eps'.format(name)
        frustum_transform_path = _mya_core.NodeDag.rename(
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

    def execute(self):
        container = self.create_container()
        start_frame, end_frame = _mya_core.Frame.get_frame_range()
        unit_paths = _asb_core.UnitAssemblyQuery.get_all_units()
        self.pre_execute(unit_paths)

        frames = range(start_frame, end_frame+1)

        for i_frame in frames:
            i_unit_paths = self.get_units_at_frame(i_frame)
            for j_unit_path in i_unit_paths:
                j_eps_name = self.to_expression_name(j_unit_path)
                j_value_pre = _mya_core.Attribute.get_as_string(
                    j_eps_name, 'qsm_camera_mask_frames'
                )
                if not j_value_pre:
                    j_value = '({})'.format(i_frame)
                else:
                    j_value = j_value_pre+','+'({})'.format(i_frame)

                _mya_core.Attribute.set_as_string(
                    j_eps_name, 'qsm_camera_mask_frames', j_value
                )

        self.post_execute(unit_paths, container)
        self.create_camera_frustum(container)


