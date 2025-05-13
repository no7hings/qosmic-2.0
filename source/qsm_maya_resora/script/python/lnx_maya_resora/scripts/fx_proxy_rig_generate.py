# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import qsm_maya.core as qsm_mya_core

from .. import core as _core


class FxProxyRigGenerateProcess(object):
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def execute(self):
        video_path = self._kwargs['video_path']
        image_sequence_path = self._kwargs['image_sequence_path']
        rig_path = self._kwargs['rig_path']
        video_path = bsc_core.ensure_string(video_path)

        with bsc_log.LogProcessContext.create(maximum=3) as l_p:

            # step 1
            frame_args = bsc_core.BscFfmpegVideo.get_frame_args(video_path)
            if not frame_args:
                raise RuntimeError()

            size_args = bsc_core.BscFfmpegVideo.get_size_args(video_path)
            if not size_args:
                raise RuntimeError()
            width, height = size_args

            bsc_core.BscFfmpegVideo.extract_image_sequence(
                video_path, image_sequence_path, width_maximum=1024
            )
            l_p.do_update()

            # step 2
            qsm_mya_core.SceneFile.new()
            start_frame, end_frame = frame_args
            image_sequence_path = image_sequence_path.replace('%04d', '<f>')

            _core.FxProxyRigGraph().create_all(
                image_sequence_path, start_frame, end_frame, width, height
            )
            l_p.do_update()

            # step 3
            qsm_mya_core.SceneFile.save_to(rig_path)
            l_p.do_update()
