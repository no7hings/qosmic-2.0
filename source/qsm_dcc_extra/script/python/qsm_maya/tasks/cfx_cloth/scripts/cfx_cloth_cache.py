# coding:utf-8
import os.path

# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_general.process as qsm_gnl_process

from .... import core as _mya_core

from ....general import core as _gnl_core

from ...general import core as _tsk_gnl_core

from ....resource import core as _rsc_core

from .. import core as _core


class CfxNClothCacheOpt(_rsc_core.AssetCacheOpt):
    CACHE_ROOT = _gnl_core.ResourceCacheNodes.CfxClothRoot
    CACHE_NAME = _gnl_core.ResourceCacheNodes.CfxClothName

    @classmethod
    def test(cls):
        cls(
            _core.CfxRigAsset(
                'lily_Skin:cfx_rig'
            )
        ).do_export(
            directory_path='Z:/projects/QSM_TST/source/shots/A001_001/A001_001_001/user.shared/cfx.cfx_cloth/main/maya/cloth_caches/A001_001_001.cfx.cfx_cloth.main.v005.v001',
            frame_range=(0, 32),
            frame_step=1,
            frame_offset=0,
        )

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
        self, directory_path, frame_range, frame_step, frame_offset
    ):
        mesh_transforms = self._resource.generate_cfx_cloth_export_args()
        if mesh_transforms:
            name = self._resource.rig_namespace
            name = name.replace(':', '__')
            options = dict(
                directory=directory_path,
                namespace=name
            )

            abc_path = _tsk_gnl_core.FilePatterns.CfxClothAbcFile.format(**options)
            json_path = _tsk_gnl_core.FilePatterns.CfxClothJsonFile.format(**options)

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

            _mya_core.AlembicCacheExport(
                file_path=abc_path,
                location=mesh_transforms,
                frame_range=frame_range,
                frame_step=frame_step
            ).execute()


class CfxClothCacheProcess(object):
    def __init__(self, **kwargs):
        self._options = kwargs

    @classmethod
    def generate_subprocess_args(
        cls,
        namespaces,
        directory_path,
        frame_range, frame_step, frame_offset,
        with_alembic_cache, with_geometry_cache
    ):
        options = dict(
            directory=directory_path,
        )
        scene_src_path = _tsk_gnl_core.FilePatterns.SceneSrcFile.format(**options)
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

    def execute(self):
        directory_path = self._options['directory_path']
        namespaces = self._options['namespaces']
        frame_range = self._options['frame_range']
        frame_step = self._options['frame_step']
        frame_offset = self._options['frame_offset']

        options = dict(
            directory=directory_path,
        )
        scene_src_path = _tsk_gnl_core.FilePatterns.SceneSrcFile.format(**options)

        _mya_core.SceneFile.new()
        if os.path.isfile(scene_src_path) is False:
            raise RuntimeError()

        _mya_core.SceneFile.open(scene_src_path)

        for i_namespace in namespaces:
            i_resource = _core.CfxRigAsset(
                i_namespace
            )

            CfxNClothCacheOpt(i_resource).do_export(
                directory_path,
                frame_range, frame_step, frame_offset
            )
