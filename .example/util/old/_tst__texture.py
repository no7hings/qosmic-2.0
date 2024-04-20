# coding:utf-8
import lxbasic.dcc.objects as bsc_dcc_objects

# t_0 = bsc_dcc_objects.StgTexture(
#     '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/v001/bl_xiz_f.diff_clr.<udim>.exr'
# )
#
# print t_0._get_path_args_as_ext_tgt_(
#     t_0.path, '.tx'
# )
#
# t_1 = bsc_dcc_objects.StgTexture(
#     '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/v001/bl_xiz_f.diff_clr.<udim>.tx'
# )
#
# print t_1._get_path_args_as_ext_tgt_(
#     t_1.path, '.tx'
# )

# print bsc_dcc_objects.StgTexture(
#     '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/v001/bl_xiz_f.diff_clr.<udim>.exr'
# ).get_args_as_ext_tgt(
#     '.tx'
# )
#
# print bsc_dcc_objects.StgTexture(
#     '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/v001/bl_xiz_f.diff_clr.<udim>.tx'
# ).get_args_as_ext_tgt(
#     '.tx'
# )
#
#
# print bsc_dcc_objects.StgTexture(
#     '/l/temp/td/dongchangbao/tx_convert_test/exr/jiguang_cloth_mask.1001.1001.exr'
# ).get_args_as_ext_tgt(
#     '.tx'
# )
#
# print bsc_dcc_objects.StgTexture(
#     '/l/temp/td/dongchangbao/tx_convert_test/exr/jiguang_cloth_mask.<udim>.####.exr'
# ).get_args_as_ext_tgt(
#     '.tx'
# )
#
# print bsc_dcc_objects.StgTexture(
#     '/l/temp/td/dongchangbao/tx_convert_test/tx_1/jiguang_cloth_mask.1001.1002.tx'
# ).get_args_as_ext_tgt(
#     '.tx'
# )
#
#
# print bsc_dcc_objects.StgTexture(
#     '/l/temp/td/dongchangbao/tx_convert_test/tx_1/jiguang_cloth_mask.<udim>.####.tx'
# ).get_args_as_ext_tgt(
#     '.tx'
# )
#
#
# bsc_dcc_objects.StgTexture(
#     '/l/temp/td/dongchangbao/texture_base_test/exr/jiguang_cloth_mask.<udim>.####.exr'
# ).copy_as_base_link(
#     directory_path_bsc='/l/temp/td/dongchangbao/texture_base_test/base',
#     directory_path_dst='/l/temp/td/dongchangbao/texture_base_test/tgt'
# )

# bsc_dcc_objects.StgTexture(
#     '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/src/bl_xiz_f.diff_clr.<udim>.exr'
# ).get_args_as_ext_tgt_by_directory_args(
#     '.tx',
#     (
#         '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/src',
#         '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/tx'
#     )
# )
#
# bsc_dcc_objects.StgTexture(
#     '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/tx/bl_xiz_f.diff_clr.<udim>.tx'
# ).get_args_as_ext_tgt_by_directory_args(
#     '.tx',
#     (
#         '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/src',
#         '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/tx'
#     )
# )

# print bsc_dcc_objects.StgTexture(
#     '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/tx/bl_xiz_f.metal.<udim>.tx'
# ).get_args_as_ext_tgt_by_directory_args(
#     '.tx',
#     (
#         '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/src',
#         '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/tx'
#     )
# )

print bsc_dcc_objects.StgTexture(
    '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/src/nn4y_eye.normal.1001.exr'
).get_args_as_tx_by_directory_args(
    ('/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/src', '/l/prod/cgm/work/assets/chr/bl_xiz_f/srf/surfacing/texture/main/v001/tx')
)



