# coding:utf-8
import lxbasic.core as bsc_core

cmd_script = bsc_core.BscFfmpegVideo.concat_by_image_sequence(
    image_sequence='C:/Users/nothings/.qosmic/temporary/2024_1128/8037769E-AD42-11EF-81E2-4074E0DA267B/image.####.jpg',
    video_path='C:/Users/nothings/.qosmic/temporary/2024_1128/8037769E-AD42-11EF-81E2-4074E0DA267B/movie.h264.mov',
    start_frame=0,
    end_frame=32,
    frame_step=1,
    fps=24,
    coding=bsc_core.BscFfmpegVideo.Coding.H264,
    replace=True,
)
