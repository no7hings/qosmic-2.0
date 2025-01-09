# coding:utf-8
import os

src_file_path = '/l/prod/shl/publish/assets/chr/nn_gongshifu/srf/surfacing/texture/Tomoco_Studio.tx/V1595447302.Tomoco_Studio.tx'
tgt_file_path = '/l/prod/shl/publish/assets/chr/nn_gongshifu/srf/surfacing/nn_gongshifu.srf.surfacing.v005/texture/Tomoco_Studio.test.tx'

tgt_dir_path = os.path.dirname(tgt_file_path)

src_rel_file_path = os.path.relpath(src_file_path, tgt_dir_path)

# os.symlink(src_rel_file_path, tgt_file_path)
print src_rel_file_path, tgt_file_path


# if os.path.islink(tgt_file_path):
#     src_file_path = os.readlink(tgt_file_path)
#     print src_file_path
#     src_dir_path = os.path.dirname(tgt_file_path)
#     rel_file_path = os.path.relpath(tgt_file_path, src_dir_path)

    # os.symlink(rel_file_path, tgt_file_path)
