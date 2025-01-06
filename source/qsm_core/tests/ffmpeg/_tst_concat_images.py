# coding:utf-8
import lxbasic.core as bsc_core

# bsc_core.BscFfmpegVideo.concat_by_images(
#     'X:/QSM_TST/QSM/release/assets/chr/cfx.cfx_rig/lily.cfx.cfx_rig.v001/source/lily.mov',
#     [
#         'C:/Users/nothings/screenshot/untitled-SMEUX4.png',
#         'C:/Users/nothings/screenshot/untitled-SMF3Y7.png'
#     ],
#     replace=True
# )


bsc_core.BscFfmpegVideo.concat_by_videos(
    'Z:/temporaries/video_concat/concat_1.mov',
    [
        'Z:/temporaries/video_concat/QSM_TST.gnl.gnl_testing.montage_test_3.v003.mov',
        'Z:/temporaries/video_concat/QSM_TST.gnl.gnl_testing.montage_test_3.v005.mov'
    ],
    replace=True
)
