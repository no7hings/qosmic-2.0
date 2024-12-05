# coding:utf-8
import lxbasic.core as bsc_core

video_path = 'Z:/temporaries/playblast_test/test_a.mov'

print bsc_core.BscFfmpegVideo.extract_all_frames(
    video_path, 'jpg', width_maximum=512
)

