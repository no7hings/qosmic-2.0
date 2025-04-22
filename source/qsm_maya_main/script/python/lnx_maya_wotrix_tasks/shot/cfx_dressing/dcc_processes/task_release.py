# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from lnx_maya_wotrix.core import task_parse as _task_parse


class ShotCfxDressingReleaseProcess(object):
    LOG_KEY = 'cfx_dressing release'

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def execute(self):
        scene_src_path = self._kwargs['scene_src']
        task_session = _task_parse.TaskParse.generate_task_session_by_shot_release_scene_src(
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

            # step 3
            cache_directory_path = task_session.get_file_or_dir_for(
                'shot-release-cache-abc-dir'
            )
            qsm_mya_core.SceneFile.collection_alembic_caches_to(
                cache_directory_path
            )
            l_p.do_update()

            # step 5
            scene_path = task_session.get_file_or_dir_for(
                'shot-release-maya-scene-file'
            )
            qsm_mya_core.SceneFile.save_to(scene_path)
            bsc_log.Log.trace_method_result(
                self.LOG_KEY, 'export scene: {}'.format(scene_path)
            )
            l_p.do_update()

            # step 6
            pack_scene_path = task_session.get_file_or_dir_for(
                'shot-release-pack-maya-scene-file'
            )
            qsm_mya_core.SceneFile.save_to(pack_scene_path)
            qsm_mya_core.SceneFile.collection_alembic_caches_auto()
            preview_path = task_session.get_file_or_dir_for(
                'shot-release-preview-mov-file'
            )
            if preview_path:
                if bsc_storage.StgPath.get_is_file(preview_path):
                    pack_preview_path = task_session.get_file_or_dir_for(
                        'shot-release-pack-preview-mov-file'
                    )
                    bsc_storage.StgFileOpt(preview_path).copy_to_file(
                        pack_preview_path
                    )
            l_p.do_update()
