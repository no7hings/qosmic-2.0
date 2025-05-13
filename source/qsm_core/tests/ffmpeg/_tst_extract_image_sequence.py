# coding:utf-8
import lxbasic.core as bsc_core

print(
    bsc_core.BscFfmpegVideo.get_frame_args(
        'X:/videos/测试/video/mesh_wrap_based_on_affine-invariant_coordinates (1080p) (1).mp4'
    )
)

# print(
#     bsc_core.BscFfmpegVideo.get_size_args(
#         'X:/videos/测试/video/mesh_wrap_based_on_affine-invariant_coordinates (1080p) (1).mp4'
#     )
# )

# bsc_core.BscFfmpegVideo.extract_image_sequence(
#     'X:/videos/测试/video/mesh_wrap_based_on_affine-invariant_coordinates (1080p) (1).mp4',
#     'Z:/libraries/lazy-resource/all/resource_video_14/mesh_wrap_based_on_affine_invariant_coordinates_1080p_1_mp4_15/preview/images/image.%04d.jpg'
# )
