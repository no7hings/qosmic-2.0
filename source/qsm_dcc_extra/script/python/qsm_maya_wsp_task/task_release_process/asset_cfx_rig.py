# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

import qsm_maya.tasks.cfx_rig as qsm_mya_task_cfx_rig_core

from .. import task_parse as _task_parse


class AssetCfxRigReleaseProcess(object):
    LOG_KEY = 'cfx_rig release'

    def __init__(self, **kwargs):
        self._options = kwargs

    def execute(self):
        scene_src_path = self._options['scene_src']
        task_session = _task_parse.TaskParse.generate_task_session_by_asset_release_scene_src(
            scene_src_path
        )
        if not task_session:
            raise RuntimeError()

        with bsc_log.LogProcessContext.create(maximum=5) as l_p:
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
            connect_map_json_path = task_session.get_file_for(
                'asset-release-connect_map-json-file'
            )
            data = qsm_mya_task_cfx_rig_core.CfxRigAssetOpt().generate_connect_map()
            bsc_storage.StgFileOpt(connect_map_json_path).set_write(data)
            l_p.do_update()
            # step 4, remove rig
            qsm_mya_task_cfx_rig_core.CfxRigAssetOpt().remove_rig()
            l_p.do_update()
            # step 5
            scene_path = task_session.get_file_for(
                'asset-release-maya-scene-file'
            )
            bsc_log.Log.trace_method_result(
                self.LOG_KEY, 'export scene: {}'.format(scene_path)
            )
            qsm_mya_core.SceneFile.export_file(
                scene_path, '|master|cfx_rig', locations_extend=['QSM_SET']
            )
            l_p.do_update()
