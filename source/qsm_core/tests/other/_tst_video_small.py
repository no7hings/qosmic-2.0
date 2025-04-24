# coding:utf-8
import lxbasic.core as bsc_core

# bsc_core.BscFfmpegVideo.create_compress(
#     'X:/videos/test.mp4', 'X:/videos/test_128.mp4', replace=True
# )

print(
    bsc_core.BscFfmpegVideo.get_codec(
        'C:/Users/nothings/.qosmic/temporary/2024_1128/8037769E-AD42-11EF-81E2-4074E0DA267B/movie.h264.mov'
    )
)
