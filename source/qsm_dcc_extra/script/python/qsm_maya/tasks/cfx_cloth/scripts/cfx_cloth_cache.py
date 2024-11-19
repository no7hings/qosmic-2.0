# coding:utf-8
import copy
import os.path

# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_general.process as qsm_gnl_process

import qsm_maya.core as qsm_mya_core

import qsm_maya.general.core as qsm_mya_gnl_core

import qsm_maya.resource.core as qsm_mya_rsc_core

from ...general import core as _tsk_gnl_core

from ...animation import core as _tsk_anm_core

from .. import core as _core


class CfxRigsOpt(object):
    def __init__(self):
        pass

    def load_all(self):
        import qsm_maya_wsp_task as qsm_mya_wsp_task

        self._resources_query = _tsk_anm_core.AdvRigAssetsQuery()
        self._resources_query.do_update()
        task_parse = qsm_mya_wsp_task.TaskParse()
        for i_resource in self._resources_query.get_all():
            i_rig_namespace = i_resource.namespace

            i_opt = _core.CfxClothAssetOpt(i_rig_namespace)
            if i_opt.get_cfx_rig_is_loaded() is True:
                continue

            i_scene_path = qsm_mya_core.ReferencesCache().get_file(i_rig_namespace)
            if i_scene_path is None:
                continue

            i_rig_scene_ptn_opt = task_parse.generate_pattern_opt_for(
                'asset-disorder-rig_scene-maya-file'
            )
            i_variants = i_rig_scene_ptn_opt.get_variants(i_scene_path, extract=True)
            if i_variants:
                i_task_variants = copy.copy(i_variants)
                i_task_variants['step'] = 'cfx'
                i_task_variants['task'] = 'cfx_rig'
                i_cfx_rig_scene_ptn_opt = task_parse.generate_pattern_opt_for(
                    'asset-release-maya-scene-file', **i_task_variants
                )
                i_matches = i_cfx_rig_scene_ptn_opt.find_matches(sort=True)
                if i_matches:
                    i_cfx_fig_scene_path = i_matches[-1]['result']
                    i_opt.load_cfx_rig_from(i_cfx_fig_scene_path)

    def apply_solver_start_frame(self, frame):
        import qsm_maya_wsp_task as qsm_mya_wsp_task

        self._resources_query = _tsk_anm_core.AdvRigAssetsQuery()
        self._resources_query.do_update()

        for i_resource in self._resources_query.get_all():
            i_rig_namespace = i_resource.namespace
            i_opt = _core.CfxClothAssetOpt(i_rig_namespace)
            i_opt.apply_all_solver_start_frame(frame)


class CfxClothCacheOpt(qsm_mya_rsc_core.AssetCacheOpt):
    CACHE_ROOT = qsm_mya_gnl_core.ResourceCacheNodes.CfxClothRoot
    CACHE_NAME = qsm_mya_gnl_core.ResourceCacheNodes.CfxClothName

    @classmethod
    def test(cls):
        cls(
            _core.CfxRigAsset(
                'lily_Skin:cfx_rig'
            )
        ).do_export(
            directory_path='Z:/projects/QSM_TST/source/shots/A001_001/A001_001_001/user.shared/cfx.cfx_cloth/main/maya/cfx_caches/A001_001_001.cfx.cfx_cloth.main.v005.v001',
            frame_range=(0, 32),
            frame_step=1,
            frame_offset=0,
        )

    def __init__(self, *args, **kwargs):
        super(CfxClothCacheOpt, self).__init__(*args, **kwargs)

    @classmethod
    def create_cache_root_auto(cls):
        if cmds.objExists(cls.CACHE_ROOT) is False:
            cmds.createNode(
                'dagContainer', name=cls.CACHE_ROOT.split('|')[-1], shared=1, skipSelect=1
            )
            cmds.setAttr(cls.CACHE_ROOT+'.iconName', 'folder-closed.png', type='string')

    def load_cache(self, cache_path):
        self.create_cache_root_auto()
        cache_location_new = '{}|{}:{}'.format(self.CACHE_ROOT, self._namespace, self.CACHE_NAME)
        cache_location = '|{}:{}'.format(self._namespace, self.CACHE_NAME)
        if cmds.objExists(cache_location) is False and cmds.objExists(cache_location_new) is False:
            cache_location = qsm_mya_core.Container.create_as_default(cache_location)
            nodes = qsm_mya_core.SceneFile.import_file(
                cache_path, self._namespace
            )
            dags = []
            non_dags = []
            for i in nodes:
                if qsm_mya_core.DagNode.check_is_dag(i):
                    dags.append(i)
                else:
                    non_dags.append(i)

            mesh_transforms = [x for x in dags if qsm_mya_core.Node.is_mesh_type(x)]

            geometry_location = self._resource.find_geometry_location()
            if geometry_location is None:
                return

            data = self._resource.pull_geometry_topology_data()
            if not data:
                return

            query_dict = {v: k for k, v in data.items()}
            for i_mesh_path in mesh_transforms:
                i_mesh_opt = qsm_mya_core.MeshShapeOpt(i_mesh_path)
                i_uuid = i_mesh_opt.get_face_vertices_as_uuid()
                if i_uuid in query_dict:
                    i_key = query_dict[i_uuid]
                    i_path_tgt = self._resource.key_to_path(self._namespace, geometry_location, i_key, '|')
                    if i_path_tgt is None:
                        continue

                    i_path_src = qsm_mya_core.Shape.get_transform(i_mesh_path)
                    i_results = qsm_mya_core.BlendShape.create(i_path_src, i_path_tgt)
                    non_dags.extend(i_results)

            dag_roots = qsm_mya_core.DagNode.find_roots(dags)
            qsm_mya_core.Container.add_dag_nodes(cache_location, dag_roots)
            qsm_mya_core.Container.add_nodes(cache_location, non_dags)

            qsm_mya_core.NodeDisplay.set_visible(cache_location, False)
            qsm_mya_core.DagNode.parent_to(cache_location, self.CACHE_ROOT)

    def do_export(
        self, directory_path, frame_range, frame_step, frame_offset
    ):
        mesh_transforms = self._resource.generate_cfx_cloth_export_args()
        if mesh_transforms:
            name = self._resource.rig_namespace
            # fix mult layer namespace
            name = name.replace(':', '__')
            options = dict(
                directory=directory_path,
                namespace=name
            )

            abc_path = _tsk_gnl_core.FilePatterns.CfxClothAbcFile.format(**options)
            json_path = _tsk_gnl_core.FilePatterns.CfxClothJsonFile.format(**options)

            data = dict(
                scene_file=qsm_mya_core.SceneFile.get_current(),
                scene_fps=qsm_mya_core.Frame.get_fps_tag(),
                user=bsc_core.BscSystem.get_user_name(),
                host=bsc_core.BscSystem.get_host(),
                time=bsc_core.BscSystem.get_time(),

                frame_range=frame_range,
                frame_step=frame_step,
                frame_offset=frame_offset,
            )

            bsc_storage.StgFileOpt(json_path).set_write(data)

            qsm_mya_core.AlembicCacheExport(
                file_path=abc_path,
                location=mesh_transforms,
                frame_range=frame_range,
                frame_step=frame_step
            ).execute()

    def execute_auto(self, **kwargs):
        pass


class CfxClothCacheProcess(object):
    @classmethod
    def test(cls):

        import qsm_general.prc_task as p

        directory_path = 'Z:/projects/QSM_TST/source/shots/A001_001/A001_001_001/user.shared/cfx.cfx_cloth/main/maya/cfx_caches/A001_001_001.cfx.cfx_cloth.main.v006.v002'

        task_name, scene_src_path, cmd_script = cls.generate_subprocess_args(
            ['lily_Skin:cfx_rig'],
            directory_path,
            frame_range=(0, 32),
            frame_step=1,
            frame_offset=0,
        )

        p.SubprocessTaskSubmit.execute_one(
            task_name, cmd_script, completed_fnc=None,
            window_title='CFX Cloth Cache Export', window_title_chs='解算布料缓存导出',
        )

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    @classmethod
    def generate_subprocess_args(
        cls,
        namespaces,
        directory_path,
        frame_range, frame_step=1, frame_offset=0,
    ):
        options = dict(
            directory=directory_path,
        )
        scene_src_path = _tsk_gnl_core.FilePatterns.SceneSrcFile.format(**options)
        qsm_mya_core.SceneFile.export_file(scene_src_path)

        task_name = '[cfx-cloth-cache][{}][{}]'.format(
            bsc_storage.StgDirectoryOpt(directory_path).get_name(), '{}-{}'.format(*frame_range)
        )

        cmd_script = qsm_gnl_process.MayaCacheProcess.generate_cmd_script_by_option_dict(
            'cfx_cloth_cache_export',
            dict(
                directory_path=directory_path,
                namespaces=namespaces,
                frame_range=frame_range,
                frame_step=frame_step,
                frame_offset=frame_offset,
            )
        )

        return task_name, scene_src_path, cmd_script

    @classmethod
    def generate_farm_hook_option(
        cls,
        namespaces,
        directory_path,
        frame_range, frame_step=1, frame_offset=0,
    ):
        options = dict(
            directory=directory_path,
        )
        scene_src_path = _tsk_gnl_core.FilePatterns.SceneSrcFile.format(**options)
        qsm_mya_core.SceneFile.export_file(scene_src_path)

        task_name = '[cfx-cloth-cache][{}][{}]'.format(
            bsc_storage.StgDirectoryOpt(directory_path).get_name(), '{}-{}'.format(*frame_range)
        )

        hook_option = qsm_gnl_process.MayaCacheProcess.generate_hook_option_fnc(
            'cfx_cloth_cache_export',
            dict(
                directory_path=directory_path,
                namespaces=namespaces,
                frame_range=frame_range,
                frame_step=frame_step,
                frame_offset=frame_offset,
            ),
            job_name=task_name,
            output_directory=directory_path
        )

        return hook_option

    def execute(self):
        directory_path = self._kwargs['directory_path']
        namespaces = self._kwargs['namespaces']
        frame_range = self._kwargs['frame_range']
        frame_step = self._kwargs['frame_step']
        frame_offset = self._kwargs['frame_offset']

        options = dict(
            directory=directory_path,
        )
        scene_src_path = _tsk_gnl_core.FilePatterns.SceneSrcFile.format(**options)
        with bsc_log.LogProcessContext.create(maximum=len(namespaces)+2, label='cfx cloth cache export') as l_p:
            # step 1
            qsm_mya_core.SceneFile.new()
            l_p.do_update()
            # step 2
            if os.path.isfile(scene_src_path) is False:
                raise RuntimeError()
            qsm_mya_core.SceneFile.open(scene_src_path)
            l_p.do_update()
            # step 3
            for i_namespace in namespaces:
                i_resource = _core.CfxRigAsset(
                    i_namespace
                )

                CfxClothCacheOpt(i_resource).do_export(
                    directory_path,
                    frame_range, frame_step, frame_offset
                )

                l_p.do_update()
