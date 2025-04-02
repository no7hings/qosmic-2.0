# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

import qsm_maya.core as qsm_mya_core

from ....core import task_parse as _task_parse

from .. import dcc_core as _task_dcc_core


class AssetCfxRigReleaseProcess(object):
    LOG_KEY = 'cfx_rig release'

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def execute(self):
        scene_src_path = self._kwargs['scene_src']
        rig_variant = self._kwargs['rig_variant']

        task_session = _task_parse.TaskParse.generate_task_session_by_asset_release_scene_src(
            scene_src_path
        )
        if not task_session:
            raise RuntimeError()

        with bsc_log.LogProcessContext.create(maximum=6) as l_p:

            # step 1
            qsm_mya_core.SceneFile.new()
            l_p.do_update()

            # step 2
            bsc_log.Log.trace_method_result(
                self.LOG_KEY, 'import scene_src: {}'.format(scene_src_path)
            )
            qsm_mya_core.SceneFile.open(scene_src_path)
            l_p.do_update()

            # step 3, save blend_map
            if rig_variant == 'default':
                connect_map_json_path = task_session.get_file_for(
                    'asset-release-connect_map-json-file'
                )
            else:
                connect_map_json_path = task_session.get_file_for(
                    'asset-release-connect_map-json-var-file', var=rig_variant
                )

            data = _task_dcc_core.AssetCfxRigSceneOpt().generate_connect_map()
            bsc_storage.StgFileOpt(connect_map_json_path).set_write(data)
            l_p.do_update()

            # step 4, remove rig
            _task_dcc_core.AssetCfxRigSceneOpt().remove_rig()
            l_p.do_update()

            # step 5
            if rig_variant == 'default':
                scene_path = task_session.get_file_for(
                    'asset-release-maya-scene-file'
                )
            else:
                scene_path = task_session.get_file_for(
                    'asset-release-maya-scene-var-file', var=rig_variant
                )

            # reset rig preset to default
            _task_dcc_core.AssetCfxRigHandle.load_rig_preset('default')
            
            # create enable aux
            _task_dcc_core.AssetCfxRigHandle.create_nclothes_enable_aux()

            # export scene
            location = _task_dcc_core.AssetCfxRigHandle.LOCATION
            qsm_mya_core.SceneFile.export_file(
                scene_path, location, locations_extend=['QSM_SET']
            )
            bsc_log.Log.trace_method_result(
                self.LOG_KEY, 'export scene: {}.'.format(scene_path)
            )
            l_p.do_update()

            # step 6, link to no version directory
            import qsm_lazy_sync.client as c

            version_path = task_session.get_file_for(
                'asset-release-version-dir'
            )
            no_version_path = task_session.get_file_for(
                'asset-release-no_version-dir'
            )
            
            # fixme: cannot use for production, server not support.
            # c.TaskClient.new_task('symlink', source=version_path, target=no_version_path, replace=True)
            l_p.do_update()
            
            # sync to other studio
            studio = qsm_gnl_core.Sync().studio.get_current()
            
            symlink_kwargs = qsm_gnl_core.Sync().generate_sync_kwargs(
                studio, version_path
            )
            if symlink_kwargs:
                c.TaskClient.new_task(
                    'sync', **symlink_kwargs
                )
