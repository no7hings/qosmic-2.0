# coding:utf-8
import lxbasic.log as bsc_log

import qsm_maya.core as qsm_mya_core

from lnx_maya_wotrix.core import task_parse as _task_parse


class ShotAnimationReleaseProcess(object):
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
