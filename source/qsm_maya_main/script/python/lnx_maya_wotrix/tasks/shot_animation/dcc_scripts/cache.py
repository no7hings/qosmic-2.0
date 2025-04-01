# coding:utf-8
import copy
import functools

import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

import qsm_general.dotfile as qsm_gnl_dotfile

import qsm_general.process as qsm_gnl_process

import qsm_maya.core as qsm_mya_core

import qsm_maya.handles.general.core as qsm_mya_hdl_gnl_core

import qsm_maya.resource as qsm_mya_resource

from .. import dcc_core as _core


class ShotAnimationCacheOpt(qsm_mya_resource.AssetCacheOpt):
    CACHE_ROOT = qsm_mya_hdl_gnl_core.ResourceCacheNodes.AnimationRoot
    CACHE_NAME = qsm_mya_hdl_gnl_core.ResourceCacheNodes.AnimationName

    @classmethod
    def test(cls):
        cls(
            _core.RigAsset(
                'lily_Skin'
            )
        ).do_export(
            directory_path='Z:/temporaries/animation_cache/v001',
            frame_range=(0, 32),
            frame_step=1,
            frame_offset=0,
        )

    @classmethod
    def test_load(cls):
        cls(
            _core.RigAsset(
                'lily_Skin'
            )
        ).load_cache(
            'Z:/temporaries/animation_cache/v003'
        )

    def __init__(self, *args, **kwargs):
        super(ShotAnimationCacheOpt, self).__init__(*args, **kwargs)

    @classmethod
    def create_cache_root_auto(cls):
        if cmds.objExists(cls.CACHE_ROOT) is False:
            cmds.createNode(
                'dagContainer', name=cls.CACHE_ROOT.split('|')[-1], shared=1, skipSelect=1
            )
            cmds.setAttr(cls.CACHE_ROOT+'.iconName', 'folder-closed.png', type='string')

    def load_cache(self, directory_path):
        self.create_cache_root_auto()

        name = self._namespace
        # fix mult layer namespace
        name = name.replace(':', '__')
        options = dict(
            directory=directory_path,
            namespace=name
        )

        cache_location_new = '{}|{}:{}'.format(self.CACHE_ROOT, self._namespace, self.CACHE_NAME)
        cache_location = '|{}:{}'.format(self._namespace, self.CACHE_NAME)
        if cmds.objExists(cache_location) is False and cmds.objExists(cache_location_new) is False:
            # create namespace auto
            if qsm_mya_core.Namespace.is_exists(self._namespace) is False:
                qsm_mya_core.Namespace.create(self._namespace)

            cache_location = qsm_mya_core.Container.create_as_default(cache_location)
            geo_cache_abc_path = qsm_gnl_core.DccFilePatterns.AniGeoCacheAbcFile.format(**options)
            control_cache_abc_path = qsm_gnl_core.DccFilePatterns.AniCtlCacheAbcFile.format(**options)

            # geometry
            if os.path.isfile(geo_cache_abc_path):
                nodes = qsm_mya_core.SceneFile.import_file(
                    geo_cache_abc_path, self._namespace
                )
                dags = []
                non_dags = []
                for i in nodes:
                    if qsm_mya_core.DagNode.check_is_dag(i):
                        dags.append(i)
                    else:
                        non_dags.append(i)

                dag_roots = qsm_mya_core.DagNode.find_roots(dags)
                qsm_mya_core.Container.add_dag_nodes(cache_location, dag_roots)
                qsm_mya_core.Container.add_nodes(cache_location, non_dags)

            # motion
            if os.path.isfile(control_cache_abc_path):
                nodes = qsm_mya_core.SceneFile.import_file(
                    control_cache_abc_path, self._namespace
                )
                dags = []
                non_dags = []
                for i in nodes:
                    if qsm_mya_core.DagNode.check_is_dag(i):
                        dags.append(i)
                    else:
                        non_dags.append(i)

                dag_roots = qsm_mya_core.DagNode.find_roots(dags)
                qsm_mya_core.Container.add_dag_nodes(cache_location, dag_roots)
                qsm_mya_core.Container.add_nodes(cache_location, non_dags)

            qsm_mya_core.NodeAttribute.create_as_string(
                cache_location, 'qsm_cache_directory', directory_path
            )
            qsm_mya_core.DagNode.parent_to(cache_location, self.CACHE_ROOT)

    def do_export(
        self, directory_path, frame_range, frame_step, frame_offset
    ):
        name = self._namespace

        # fix mult layer namespace
        name = name.replace(':', '__')
        options = dict(
            directory=directory_path,
            namespace=name
        )

        geometry_location = self._resource.find_geometry_location()
        geo_lower_location = self._resource.find_geo_lower_location()
        if geometry_location or geo_lower_location:
            geo_cache_abc_path = qsm_gnl_core.DccFilePatterns.AniGeoCacheAbcFile.format(**options)
            geometry_json_path = qsm_gnl_core.DccFilePatterns.AniGeoJsonFile.format(**options)

            json_data = dict(
                scene_file=qsm_mya_core.SceneFile.get_current(),
                scene_fps=qsm_mya_core.Frame.get_fps_tag(),
                user=bsc_core.BscSystem.get_user_name(),
                host=bsc_core.BscSystem.get_host(),
                time=bsc_core.BscSystem.get_time(),

                frame_range=frame_range,
                frame_step=frame_step,
                frame_offset=frame_offset,
            )

            bsc_storage.StgFileOpt(geometry_json_path).set_write(json_data)

            qsm_mya_core.AlembicCacheExport(
                file_path=geo_cache_abc_path,
                location=filter(None, [geometry_location, geo_lower_location]),
                frame_range=frame_range,
                frame_step=frame_step
            ).execute()

        motion_location = self._resource.find_motion_location()
        if motion_location:
            control_cache_abc_path = qsm_gnl_core.DccFilePatterns.AniCtlCacheAbcFile.format(**options)
            motion_json_path = qsm_gnl_core.DccFilePatterns.AniCtlJsonFile.format(**options)

            json_data = dict(
                scene_file=qsm_mya_core.SceneFile.get_current(),
                scene_fps=qsm_mya_core.Frame.get_fps_tag(),
                user=bsc_core.BscSystem.get_user_name(),
                host=bsc_core.BscSystem.get_host(),
                time=bsc_core.BscSystem.get_time(),

                frame_range=frame_range,
                frame_step=frame_step,
                frame_offset=frame_offset,
            )

            bsc_storage.StgFileOpt(motion_json_path).set_write(json_data)

            qsm_mya_core.AlembicCacheExport(
                file_path=control_cache_abc_path,
                location=motion_location,
                frame_range=frame_range,
                frame_step=frame_step
            ).execute()


class ShotAnimationCacheProcess:
    TASK_KEY = qsm_gnl_process.MayaTaskSubprocess.TaskKeys.ShotAnimationCacheExport

    @classmethod
    def test(cls):

        import qsm_general.prc_task as p

        directory_path = 'Z:/temporaries/animation_cache/v004'

        task_name, scene_src_path, cmd_script = cls.generate_subprocess_args(
            ['lily_Skin'],
            directory_path,
            frame_range=(0, 32),
            frame_step=1,
            frame_offset=0,
            scene_src_source_override='X:/QSM_TST/A001/A001_001/动画/通过文件/A001_001_001.ma',
            scene_src_target_override='Z:/temporaries/animation_cache/v004/source/A001_001_001.ma',
        )

        p.SubprocessTaskSubmit.execute_one(
            task_name, cmd_script, completed_fnc=None,
            window_title='Animation Cache Export', window_title_chs='动画缓存导出',
        )

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    @classmethod
    def generate_subprocess_args(
        cls,
        namespaces,
        directory_path,
        frame_range, frame_step=1, frame_offset=0,
        scene_src_source_override=None,
        scene_src_target_override=None
    ):
        options = dict(
            directory=directory_path,
        )
        if scene_src_target_override:
            scene_src_path = scene_src_target_override
        else:
            scene_src_path = qsm_gnl_core.DccFilePatterns.SceneSrcFile.format(**options)

        if scene_src_source_override:
            bsc_storage.StgFileOpt(scene_src_source_override).copy_to_file(scene_src_path)
        else:
            qsm_mya_core.SceneFile.export_file(scene_src_path)

        task_name = '[{}][{}][{}]'.format(
            cls.TASK_KEY, bsc_storage.StgDirectoryOpt(directory_path).get_name(), '{}-{}'.format(*frame_range)
        )

        cmd_script = qsm_gnl_process.MayaTaskSubprocess.generate_cmd_script_by_option_dict(
            cls.TASK_KEY,
            dict(
                scene_src_path=scene_src_path,
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
        scene_src_source_override=None,
        scene_src_target_override=None
    ):
        options = dict(
            directory=directory_path,
        )
        if scene_src_target_override:
            scene_src_path = scene_src_target_override
        else:
            scene_src_path = qsm_gnl_core.DccFilePatterns.SceneSrcFile.format(**options)

        if scene_src_source_override:
            bsc_storage.StgFileOpt(scene_src_source_override).copy_to_file(scene_src_path)
        else:
            qsm_mya_core.SceneFile.export_file(scene_src_path)

        task_name = '[{}][{}][{}]'.format(
            cls.TASK_KEY, bsc_storage.StgDirectoryOpt(directory_path).get_name(), '{}-{}'.format(*frame_range)
        )

        hook_option = qsm_gnl_process.MayaTaskSubprocess.generate_hook_option_fnc(
            cls.TASK_KEY,
            dict(
                scene_src_path=scene_src_path,
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
        scene_src_path = self._kwargs['scene_src_path']
        directory_path = self._kwargs['directory_path']
        namespaces = self._kwargs['namespaces']
        frame_range = self._kwargs['frame_range']
        frame_step = self._kwargs['frame_step']
        frame_offset = self._kwargs['frame_offset']

        with bsc_log.LogProcessContext.create(maximum=len(namespaces)+2, label='cfx cloth cache export') as l_p:
            # step 1
            qsm_mya_core.SceneFile.new()
            l_p.do_update()
            # step 2
            if os.path.isfile(scene_src_path) is False:
                raise RuntimeError()

            qsm_mya_core.SceneFile.open(scene_src_path)
            l_p.do_update()
            # step 2++
            for i_namespace in namespaces:
                i_resource = _core.RigAsset(
                    i_namespace
                )

                ShotAnimationCacheOpt(i_resource).do_export(
                    directory_path,
                    frame_range, frame_step, frame_offset
                )

                l_p.do_update()


class ShotAnimationCacheSync:
    @classmethod
    def test(cls):
        # 'X:/QSM_TST/A001/A001_001/动画/通过文件/A001_001_003.ma'

        cls.execute_for(
            namespaces=[
                'lily_Skin',
                'lily_Skin1',
                'A001_001_001:lily_Skin'
            ],
            resource_properties=dict(
                project='QSM_TST',
                episode='A001',
                sequence='A001_001',
                shot='A001_001_003',
            ),
            resource_fnc=cls.cfx_load_ani_cache_auto_fnc
        )

    def __init__(self, **kwargs):
        pass

    @classmethod
    def cfx_load_ani_cache_auto_fnc(cls, directory_path, rig_namespace):
        import lnx_maya_wotrix.tasks.shot_cfx_cloth.dcc_core as c
        c.ShotCfxClothAssetHandle(rig_namespace).sync_ani_cache_auto(directory_path)

    @classmethod
    def generate_export_kwargs(cls, namespaces, resource_properties, scene_path_override=None):
        import lnx_maya_wotrix.core as c

        task_parse = c.TaskParse()

        variants = copy.copy(resource_properties)

        if scene_path_override is None:
            dso_scene_pth_opt = task_parse.generate_pattern_opt_for(
                'shot-disorder-animation-scene-file', **variants
            )

            dso_scene_matches = dso_scene_pth_opt.find_matches()
            if not dso_scene_matches:
                raise RuntimeError()

            dod_scene_path = dso_scene_matches[-1]['result']
        else:
            dod_scene_path = scene_path_override

        variants['step'] = task_parse.Steps.animation
        variants['task'] = task_parse.Tasks.animation

        tmp_scene_src_pth_opt = task_parse.generate_pattern_opt_for(
            'shot-temporary-maya-scene_src-file', **variants
        )

        # auto update scene-src file version
        matches = tmp_scene_src_pth_opt.find_matches(sort=True)
        if matches:
            tmp_scene_path_latest = matches[-1]['result']
            if bsc_storage.StgFileOpt(tmp_scene_path_latest).get_timestamp_is_same_to(dod_scene_path) is True:
                tmp_version = matches[-1]['version']
                tmp_scene_src_path = tmp_scene_path_latest
            else:
                tmp_version = str(int(matches[-1]['version'])+1).zfill(3)
                tmp_scene_pth_opt_new = tmp_scene_src_pth_opt.update_variants_to(version=tmp_version)
                if tmp_scene_pth_opt_new.get_keys():
                    raise RuntimeError()

                tmp_scene_src_path = tmp_scene_pth_opt_new.get_value()
                bsc_storage.StgFileOpt(dod_scene_path).copy_to_file(tmp_scene_src_path)
        else:
            tmp_version = '001'
            tmp_scene_pth_opt_new = tmp_scene_src_pth_opt.update_variants_to(version=tmp_version)
            if tmp_scene_pth_opt_new.get_keys():
                raise RuntimeError()

            tmp_scene_src_path = tmp_scene_pth_opt_new.get_value()
            bsc_storage.StgFileOpt(dod_scene_path).copy_to_file(tmp_scene_src_path)

        variants_new = copy.copy(variants)
        variants_new['version'] = tmp_version
        tmp_version_dir_opt = task_parse.generate_pattern_opt_for(
            'shot-temporary-version-dir', **variants_new
        )
        tmp_version_dir_path = tmp_version_dir_opt.get_value()

        namespaces_valid = []

        for i_namespace in namespaces:
            i_name = i_namespace.replace(':', '__')
            i_options = dict(
                directory=tmp_version_dir_path,
                namespace=i_name
            )
            i_geometry_abc_path = qsm_gnl_core.DccFilePatterns.AniGeoCacheAbcFile.format(**i_options)
            if os.path.isfile(i_geometry_abc_path) is False:
                namespaces_valid.append(i_namespace)

        if namespaces_valid:
            frame_range = qsm_gnl_dotfile.MayaAscii(dod_scene_path).get_frame_range()
            start_frame, end_frame = frame_range
            return True, dict(
                scene_src_path=tmp_scene_src_path,
                directory_path=tmp_version_dir_path,
                namespaces=namespaces_valid,
                frame_range=(1, end_frame),
                frame_step=1,
                frame_offset=0,
            )
        return False, dict(
            directory_path=tmp_version_dir_path,
        )

    @classmethod
    def generate_subprocess_args(cls, namespaces, resource_properties, scene_path_override=None):
        flag, kwargs = cls.generate_export_kwargs(namespaces, resource_properties, scene_path_override)
        if flag is True:
            directory_path = kwargs['directory_path']
            frame_range = kwargs['frame_range']

            task_name = '[{}][{}][{}]'.format(
                ShotAnimationCacheProcess.TASK_KEY,
                bsc_storage.StgDirectoryOpt(directory_path).get_name(),
                '{}-{}'.format(*frame_range)
            )

            cmd_script = qsm_gnl_process.MayaTaskSubprocess.generate_cmd_script_by_option_dict(
                ShotAnimationCacheProcess.TASK_KEY,
                kwargs
            )
            return True, (task_name, directory_path, cmd_script)
        return False, (kwargs['directory_path'], )

    @classmethod
    def execute_for(cls, namespaces, resource_properties, resource_fnc=None, scene_path_override=None):
        def completed_fnc_(directory_path_):
            if resource_fnc is not None:
                for _i_namespace in namespaces:
                    resource_fnc(directory_path_, _i_namespace)

        import qsm_general.prc_task as p

        flag, args = cls.generate_subprocess_args(
            namespaces,
            resource_properties,
            scene_path_override
        )
        if flag is True:
            task_name, directory_path, cmd_script = args
            p.SubprocessTaskSubmit.execute_one(
                task_name, cmd_script, completed_fnc=functools.partial(completed_fnc_, directory_path),
                window_title='Animation Cache Export', window_title_chs='动画缓存导出',
            )
        else:
            directory_path = args[0]
            completed_fnc_(directory_path)
