# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

from .... import core as _mya_core

from .... import wsp_task as _maya_wsp_task

from .. import core as _core


class CfxRigReleaseOpt(object):
    @classmethod
    def test(cls):
        task_session = _maya_wsp_task.TaskParse.generate_task_session_by_asset_release_scene_src(
            'X:/QSM_TST/QSM/release/assets/chr/lily/cfx.cfx_rig/lily.cfx.cfx_rig.v002/source/lily.ma'
        )
        print task_session.get_file_for(
            'asset-release-scene-maya-file'
        )

    def __init__(self):
        pass
    

class CfxRigReleaseProcess(object):
    LOG_KEY = 'cfx_rig release'

    def __init__(self, **kwargs):
        self._options = kwargs
    
    def execute(self):
        scene_src_path = self._options['scene_src']
        task_session = _maya_wsp_task.TaskParse.generate_task_session_by_asset_release_scene_src(
            scene_src_path
        )
        if not task_session:
            raise RuntimeError()

        with bsc_log.LogProcessContext.create(maximum=5) as l_p:
            # step 1
            _mya_core.SceneFile.new()
            l_p.do_update()
            # step 2
            bsc_log.Log.trace_method_result(
                self.LOG_KEY, 'import scene_src: {}'.format(scene_src_path)
            )
            _mya_core.SceneFile.open(scene_src_path)
            l_p.do_update()
            # step 3, save blend_map
            connect_map_json_path = task_session.get_file_for(
                'asset-release-connect_map-json-file'
            )
            data = _core.AssetRigOpt().generate_connect_map()
            bsc_storage.StgFileOpt(connect_map_json_path).set_write(data)
            l_p.do_update()
            # step 4, remove rig
            _core.AssetRigOpt().remove_rig()
            l_p.do_update()
            # step 5
            scene_path = task_session.get_file_for(
                'asset-release-scene-maya-file'
            )
            bsc_log.Log.trace_method_result(
                self.LOG_KEY, 'export scene: {}'.format(scene_path)
            )
            _mya_core.SceneFile.export_file(
                scene_path, '|master|cfx'
            )
            l_p.do_update()
