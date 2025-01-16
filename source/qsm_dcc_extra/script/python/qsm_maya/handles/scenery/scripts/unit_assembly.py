# coding:utf-8
import functools

import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

import qsm_general.process as qsm_gnl_process

import qsm_maya.core as qsm_mya_core

import qsm_maya.general.core as qsm_mya_gnl_core

import qsm_maya.resource.core as qsm_mya_rsc_core

import qsm_maya.assembly.core as qsm_mya_asb_core

from .. import core as _core


class UnitAssemblyOpt(qsm_mya_rsc_core.AssetCacheOpt):
    TASK_KEY = 'unit_assembly_generate'
    API_VERSION = 1.0

    CACHE_ROOT = qsm_mya_gnl_core.ResourceCacheNodes.UnitAssemblyRoot
    CACHE_NAME = qsm_mya_gnl_core.ResourceCacheNodes.UnitAssemblyName

    def __init__(self, resource):
        super(UnitAssemblyOpt, self).__init__(resource)

        cmds.loadPlugin('sceneAssembly', quiet=1)
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

        statistics = bsc_storage.Statistics.generate()
        statistics.update_at_time(
            dict(
                method='unit_assembly_cache_load',
                cache=cache_file_path
            )
        )

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

        task_name = '[{}][{}]'.format(
            self.TASK_KEY, bsc_storage.StgFileOpt(file_path).name
        )

        cache_path = qsm_gnl_core.DccCache.generate_asset_unit_assembly_file_new(file_path)
        if bsc_storage.StgFileOpt(cache_path).get_is_file() is False:
            cmd_script = qsm_gnl_process.MayaCacheSubprocess.generate_cmd_script_by_option_dict(
                self.TASK_KEY,
                dict(
                    file_path=file_path,
                    cache_path=cache_path,
                )
            )
            return task_name, cmd_script, cache_path
        return task_name, None, cache_path

    @classmethod
    def _load_delay_fnc(cls, task_window, task_args_dict):
        with task_window.gui_progressing(maximum=len(task_args_dict.keys())) as g_p:
            for i_k, i_v in task_args_dict.items():
                i_task_name, i_cmd_script, i_cache_path = i_k

                task_window.submit(
                    'unit_assembly_generate',
                    i_task_name,
                    i_cmd_script,
                    completed_fnc=[
                        functools.partial(cls(x).load_cache, i_cache_path, True) for x in i_v
                    ]
                )
                g_p.do_update()

    @classmethod
    def execute_auto(cls, **kwargs):
        scheme = kwargs['scheme']
        if scheme == 'default':
            resources = []
            namespaces = qsm_mya_core.Namespaces.extract_from_selection()
            if namespaces:
                resources_query = _core.SceneryAssetQuery()
                resources_query.do_update()
                for i_namespace in namespaces:
                    i_resource = resources_query.get(i_namespace)
                    if i_resource:
                        if i_resource.is_unit_assembly_exists() is False:
                            resources.append(i_resource)

            if not resources:
                gui_core.GuiDialog.create(
                    '元素组装加载',
                    content='选择一个或多个可用的场景（如果选中的场景已经加载了元素组装，会被忽略），可以选择场景的任意部件。',
                    status=gui_core.GuiDialog.ValidationStatus.Warning,
                    no_label='Close',
                    ok_visible=False, no_visible=True, cancel_visible=False,
                )
                return

            task_args_dict = {}
            for i_resource in resources:
                i_resource_opt = cls(i_resource)
                i_task_name, i_cmd_script, i_cache_path = i_resource_opt.generate_args()
                if i_cmd_script is not None:
                    task_args_dict.setdefault(
                        (i_task_name, i_cmd_script, i_cache_path),
                        []
                    ).append(
                        i_resource
                    )
                else:
                    i_resource_opt.load_cache(i_cache_path, True)

            if task_args_dict:
                import lxgui.proxy.widgets as gui_prx_widgets

                task_window = gui_prx_widgets.PrxSprcTaskWindow()
                if task_window._language == 'chs':
                    task_window.set_window_title('元素组装加载')
                    task_window.set_tip(
                        '元素组装会在后台生成，生成成功后会自动加载到场景中，请耐心等待；\n'
                        '这个过程可能会让MAYA前台操作产生些许卡顿；\n'
                        '如需要终止任务，请点击“关闭”'
                    )
                else:
                    task_window.set_window_title('Unit Assembly Load')

                task_window.show_window_auto(exclusive=False)
                task_window.run_fnc_delay(
                    functools.partial(cls._load_delay_fnc, task_window, task_args_dict), 500
                )

    @classmethod
    def find_gpu_cache(cls, **kwargs):
        pass

    @classmethod
    def remove_auto(cls, **kwargs):
        resources = []
        namespaces = qsm_mya_core.Namespaces.extract_from_selection()
        if namespaces:
            resources_query = _core.SceneryAssetQuery()
            resources_query.do_update()
            for i_namespace in namespaces:
                i_resource = resources_query.get(i_namespace)
                if i_resource:
                    if i_resource.is_unit_assembly_exists() is True:
                        resources.append(i_resource)

        if not resources:
            gui_core.GuiDialog.create(
                '元素组装移除',
                content='选择一个或多个可用的场景（已经加载了元素组装），可以选择场景的任意部件。',
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                no_label='Close',
                ok_visible=False, no_visible=True, cancel_visible=False,
            )
            return

        for i_resource in resources:
            cls(i_resource).remove_cache()


class UnitAssemblyProcess(object):
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

    def __init__(self, file_path, cache_file_path=None, gpu_unpack=True):
        self._load_plugs()

        self._file_path = file_path

        self._directory_path = bsc_storage.StgFileOpt(
            self._file_path
        ).directory_path

        if cache_file_path is None:
            self._cache_file_path = qsm_gnl_core.DccCache.generate_asset_unit_assembly_file_new(self._file_path)
        else:
            self._cache_file_path = cache_file_path

        self._cache_directory_path = bsc_storage.StgFileOpt(
            self._cache_file_path
        ).directory_path

        self._gpu_unpack = gpu_unpack

    def grid_mesh_prc(self, grid_size):
        mesh_paths = qsm_mya_core.Scene.find_all_dag_nodes(['mesh'])
        nodes = []
        list_for_grid = []
        with bsc_log.LogProcessContext.create(maximum=len(mesh_paths), label='mesh process') as l_p:
            for i_shape_path in mesh_paths:
                if qsm_mya_core.Node.is_mesh_type(i_shape_path) is True:
                    i_mesh_opt = qsm_mya_core.MeshShapeOpt(i_shape_path)
                    i_w, i_h, i_d = i_mesh_opt.get_dimension()
                    i_s = max(i_w, i_h, i_d)
                    if i_s < grid_size:
                        list_for_grid.append(i_shape_path)
                    else:
                        self.mesh_prc(i_shape_path, check_face_count=False)

                l_p.do_update()

        if list_for_grid:
            mapper = qsm_mya_asb_core.GridSpace(list_for_grid, grid_size).generate()
            keys = mapper.keys()
            keys.sort()
            with bsc_log.LogProcessContext.create(maximum=len(keys), label='grid process') as l_p:
                for i_seq, i_key in enumerate(keys):
                    i_hash_key = bsc_core.BscHash.to_hash_key(i_key)
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
                        i_mesh_file_path = '{}/mesh.mb'.format(
                            i_directory_path
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
                        # export to gpu and mesh
                        qsm_mya_core.GpuCache.export_frame_(
                            i_gpu_file_path, i_group_path_new
                        )
                        qsm_mya_core.SceneFile.export_file(
                            i_mesh_file_path, i_group_path_new
                        )
                        qsm_mya_core.Node.delete(i_group_path_new)
                        # create AD
                        i_ad_path = '|region_{}_AD'.format(i_seq)
                        # ad
                        qsm_mya_core.AssemblyDefinition.create(
                            i_ad_path
                        )
                        qsm_mya_core.AssemblyDefinition.add_cache(
                            i_ad_path, i_gpu_file_path, 'gpu'
                        )
                        qsm_mya_core.AssemblyDefinition.add_scene(
                            i_ad_path, i_mesh_file_path, 'mesh'
                        )
                        qsm_mya_core.SceneFile.export_file(
                            i_ad_file_path, i_ad_path
                        )
                        qsm_mya_core.Node.delete(i_ad_path)
                    else:
                        i_shape_paths = mapper[i_key]
                        for j_shape_path in i_shape_paths:
                            # fixme: mesh parent mesh
                            if qsm_mya_core.DagNode.is_exists(j_shape_path) is False:
                                continue

                            j_transform_path = qsm_mya_core.Shape.get_transform(j_shape_path)
                            qsm_mya_core.Node.delete(j_transform_path)

                    i_ar_path = '|region_{}_AR'.format(i_seq)
                    i_ar_path_new = qsm_mya_core.AssemblyReference.create(
                        i_ad_file_path, i_ar_path
                    )
                    qsm_mya_core.NodeAttribute.create_as_string(
                        i_ar_path_new, 'qsm_type', 'unit_assembly'
                    )
                    qsm_mya_core.NodeAttribute.create_as_string(
                        i_ar_path_new, 'qsm_hash_key', i_hash_key
                    )
                    qsm_mya_core.NodeDrawOverride.set_enable(
                        i_ar_path_new, True
                    )
                    qsm_mya_core.NodeDrawOverride.set_color(
                        i_ar_path_new, (1.0, .5, .25)
                    )
                    nodes.append(i_ar_path_new)

                    l_p.do_update()

        return nodes

    def mesh_prc(self, shape_path, check_face_count=True):
        mesh_opt = qsm_mya_core.MeshShapeOpt(shape_path)
        face_count = qsm_mya_core.Mesh.get_face_number(shape_path)
        if check_face_count is True:
            if face_count == 0:
                return

            if face_count < _core.Assembly.FACE_COUNT_MAXIMUM:
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
            gpu_key = _core.Assembly.Keys.GPU
            gpu_file_path = '{}/{}.abc'.format(
                unit_directory_path, gpu_key
            )
            qsm_mya_core.GpuCache.export_frame(
                gpu_file_path, transform_path_new
            )
            file_dict[gpu_key] = gpu_file_path
            # mesh
            mesh_key = _core.Assembly.Keys.Mesh
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
                    i_gpu_key = _core.Assembly.Keys.GPU_LOD.format(i_level)
                    i_gpu_file_path_lod = '{}/{}.abc'.format(
                        unit_directory_path, i_gpu_key
                    )
                    qsm_mya_core.GpuCache.export_frame(
                        i_gpu_file_path_lod, transform_path_new
                    )
                    file_dict[i_gpu_key] = i_gpu_file_path_lod
                    # mesh
                    i_mesh_key = _core.Assembly.Keys.Mesh_LOD.format(i_level)
                    i_mesh_file_path_lod = '{}/{}.ma'.format(
                        unit_directory_path, i_mesh_key
                    )
                    qsm_mya_core.SceneFile.export_file(
                        i_mesh_file_path_lod, transform_path_new
                    )
                    file_dict[i_mesh_key] = i_mesh_file_path_lod

            # add attribute
            for i_key in _core.Assembly.Keys.All:
                if i_key in file_dict:
                    i_file_path = file_dict[i_key]
                    if i_key.startswith(_core.Assembly.Keys.Mesh):
                        qsm_mya_core.AssemblyDefinition.add_scene(
                            ad_path, i_file_path, i_key
                        )
                    elif i_key.startswith(_core.Assembly.Keys.GPU):
                        qsm_mya_core.AssemblyDefinition.add_cache(
                            ad_path, i_file_path, i_key
                        )

            qsm_mya_core.Node.delete(transform_path_new)

            qsm_mya_core.SceneFile.export_file(
                ad_file_path, ad_path
            )

            qsm_mya_core.Node.delete(ad_path)

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

    def execute(self):
        qsm_mya_core.SceneFile.new()

        container = '|{}'.format(UnitAssemblyOpt.CACHE_NAME)

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
        _core.GpuImport.find_all_gpu_caches(self._directory_path)
        # find lost reference first
        qsm_mya_core.FileReferences.search_all_from(
            [self._directory_path], ignore_exists=True
        )
        # repair all instanced
        qsm_mya_core.Scene.remove_all_instanced(type_includes=['mesh', 'gpuCache'])
        # import all gpu
        _core.GpuImport().execute()
        # process
        mesh_paths = qsm_mya_core.Scene.find_all_dag_nodes(type_includes=['mesh'])
        mesh_count_data = qsm_mya_core.MeshShapes.get_evaluate(mesh_paths)
        width, height = mesh_count_data['width'], mesh_count_data['height']
        size = max(width, height)
        d = 100
        if size <= d*10000:
            grid_size = d*10
        elif size <= d*100000:
            grid_size = d*100
        elif size <= d*1000000:
            grid_size = d*1000
        elif size <= d*10000000:
            grid_size = d*10000
        else:
            grid_size = d*50000

        with bsc_log.LogProcessContext.create(maximum=len(mesh_paths), label='mesh process') as l_p:
            for i_path in mesh_paths:
                self.mesh_prc(i_path)
                l_p.do_update()
        #
        grid_paths = self.grid_mesh_prc(grid_size)
        if grid_paths:
            qsm_mya_core.Container.add_dag_nodes(container, grid_paths)
        # instance all mesh
        # _core.MeshInstance(material=True).execute()
        # remove unused groups
        qsm_mya_core.Scene.remove_all_empty_groups()
        # collection roots
        exists_roots = [i for i in all_roots if qsm_mya_core.Node.is_exists(i)]
        qsm_mya_core.Container.add_dag_nodes(container, exists_roots)

        qsm_mya_core.SceneFile.export_file(
            self._cache_file_path, container
        )

