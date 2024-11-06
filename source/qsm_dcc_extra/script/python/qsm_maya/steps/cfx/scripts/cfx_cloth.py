# coding:utf-8
import os.path

# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_general.process as qsm_gnl_process

from .... import core as _mya_core

from ....general import core as _gnl_core

from ....resource import core as _rsc_core

from .. import core as _core


class CfxNClothCacheOpt(_rsc_core.AssetCacheOpt):
    CACHE_ROOT = _gnl_core.ResourceCacheNodes.CfxClothRoot
    CACHE_NAME = _gnl_core.ResourceCacheNodes.CfxClothName

    def __init__(self, *args, **kwargs):
        super(CfxNClothCacheOpt, self).__init__(*args, **kwargs)

    @classmethod
    def create_cache_root_auto(cls):
        if cmds.objExists(cls.CACHE_ROOT) is False:
            cmds.createNode(
                'dagContainer', name=cls.CACHE_ROOT.split('|')[-1], shared=1, skipSelect=1
            )
            cmds.setAttr(cls.CACHE_ROOT+'.iconName', 'folder-closed.png', type='string')

    def do_export(
        self, directory_path, frame_range, frame_step, frame_offset,
        with_alembic_cache=True, with_geometry_cache=True
    ):
        mesh_transforms = self._resource.generate_cfx_cloth_export_args()
        if mesh_transforms:
            options = dict(
                directory=directory_path,
                namespace=self._namespace
            )

            mcx_path = _gnl_core.FilePatterns.CfxClothMcxFile.format(**options)
            abc_path = _gnl_core.FilePatterns.CfxClothAbcFile.format(**options)
            json_path = _gnl_core.FilePatterns.CfxClothJsonFile.format(**options)

            data = dict(
                scene_file=_mya_core.SceneFile.get_current(),
                scene_fps=_mya_core.Frame.get_fps_tag(),
                user=bsc_core.BscSystem.get_user_name(),
                host=bsc_core.BscSystem.get_host(),
                time=bsc_core.BscSystem.get_time(),

                frame_range=frame_range,
                frame_step=frame_step,
                frame_offset=frame_offset,
            )

            bsc_storage.StgFileOpt(json_path).set_write(data)
            if with_geometry_cache is True:
                _mya_core.GeometryCacheOpt(
                    file_path=mcx_path,
                    location=mesh_transforms,
                    frame_range=frame_range,
                    frame_step=frame_step
                ).create_and_assign()

            if with_alembic_cache is True:
                _mya_core.AlembicCacheExport(
                    file_path=abc_path,
                    location=mesh_transforms,
                    frame_range=frame_range,
                    frame_step=frame_step
                ).execute()

    def load_cache(self, cache_path):
        self.create_cache_root_auto()
        cache_location_new = '{}|{}:{}'.format(self.CACHE_ROOT, self._namespace, self.CACHE_NAME)
        cache_location = '|{}:{}'.format(self._namespace, self.CACHE_NAME)
        if cmds.objExists(cache_location) is False and cmds.objExists(cache_location_new) is False:
            cache_location = _mya_core.Container.create_as_default(cache_location)
            nodes = _mya_core.SceneFile.import_file(
                cache_path, self._namespace
            )
            dags = []
            non_dags = []
            for i in nodes:
                if _mya_core.DagNode.check_is_dag(i):
                    dags.append(i)
                else:
                    non_dags.append(i)

            mesh_transforms = [x for x in dags if _mya_core.Node.is_mesh_type(x)]

            geometry_location = self._resource.find_geometry_location()
            if geometry_location is None:
                return

            data = self._resource.pull_geometry_topology_data()
            if not data:
                return

            query_dict = {v: k for k, v in data.items()}
            for i_mesh_path in mesh_transforms:
                i_mesh_opt = _mya_core.MeshShapeOpt(i_mesh_path)
                i_uuid = i_mesh_opt.get_face_vertices_as_uuid()
                if i_uuid in query_dict:
                    i_key = query_dict[i_uuid]
                    i_path_tgt = self._resource.key_to_path(self._namespace, geometry_location, i_key, '|')
                    if i_path_tgt is None:
                        continue

                    i_path_src = _mya_core.Shape.get_transform(i_mesh_path)
                    i_results = _mya_core.BlendShape.create(i_path_src, i_path_tgt)
                    non_dags.extend(i_results)

            dag_roots = _mya_core.DagNode.find_roots(dags)
            _mya_core.Container.add_dag_nodes(cache_location, dag_roots)
            _mya_core.Container.add_nodes(cache_location, non_dags)

            _mya_core.NodeDisplay.set_visible(cache_location, False)
            _mya_core.DagNode.parent_to(cache_location, self.CACHE_ROOT)


class CfxNClothCacheProcess(object):
    def __init__(
        self,
        directory_path, namespaces, frame_range, frame_step, frame_offset,
        with_alembic_cache=True, with_geometry_cache=True
    ):
        self._directory_path = directory_path
        self._namespaces = namespaces
        self._frame_range = frame_range
        self._frame_step = frame_step
        self._frame_offset = frame_offset
        self._with_alembic_cache = with_alembic_cache
        self._with_geometry_cache = with_geometry_cache

    @classmethod
    def generate_task_args(
        cls,
        namespaces, 
        directory_path,
        frame_range, frame_step, frame_offset, 
        with_alembic_cache, with_geometry_cache
    ):
        options = dict(
            directory=directory_path,
        )
        scene_src_path = _gnl_core.FilePatterns.SceneSrcFile.format(**options)
        _mya_core.SceneFile.export_file(scene_src_path)

        task_name = '[cfx-cloth-cache][{}][{}]'.format(
            bsc_storage.StgDirectoryOpt(directory_path).get_name(), '{}-{}'.format(*frame_range)
        )

        cmd_script = qsm_gnl_process.MayaCacheProcess.generate_cmd_script_by_option_dict(
            'cfx-cloth-cache-generate',
            dict(
                directory_path=directory_path,
                namespaces=namespaces,
                frame_range=frame_range,
                frame_step=frame_step,
                frame_offset=frame_offset,
                with_alembic_cache=with_alembic_cache, with_geometry_cache=with_geometry_cache
            )
        )

        return task_name, scene_src_path, cmd_script

    @classmethod
    def generate_deadline_job_args(
        cls,
        namespaces,
        directory_path,
        frame_range, frame_step, frame_offset,
        with_alembic_cache, with_geometry_cache
    ):
        options = dict(
            directory=directory_path,
        )
        scene_src_path = _gnl_core.FilePatterns.SceneSrcFile.format(**options)
        _mya_core.SceneFile.export_file(scene_src_path)

        job_name = '[cfx-cloth-cache][{}][{}]'.format(
            bsc_storage.StgDirectoryOpt(directory_path).get_name(), '{}-{}'.format(*frame_range)
        )

        hook_option = qsm_gnl_process.MayaCacheProcess.generate_hook_option_by_option_dict(
            'cfx-cloth-cache-generate',
            dict(
                directory_path=directory_path,
                namespaces=namespaces,
                frame_range=frame_range,
                frame_step=frame_step,
                frame_offset=frame_offset,
                with_alembic_cache=with_alembic_cache, with_geometry_cache=with_geometry_cache
            ),
            job_name=job_name,
            output_directory=directory_path
        )

        return hook_option

    def execute(self):
        options = dict(
            directory=self._directory_path,
        )
        scene_src_path = _gnl_core.FilePatterns.SceneSrcFile.format(**options)

        _mya_core.SceneFile.new()
        if os.path.isfile(scene_src_path) is False:
            raise RuntimeError()

        _mya_core.SceneFile.open(scene_src_path)

        for i_namespace in self._namespaces:
        
            i_resource = _core.CfxAdvRigAsset(i_namespace)

            CfxNClothCacheOpt(i_resource).do_export(
                self._directory_path,
                self._frame_range, self._frame_step, self._frame_offset,
                self._with_alembic_cache, self._with_geometry_cache
            )
