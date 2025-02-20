# coding:utf-8
import os.path

import lxbasic.storage as bsc_storage

import lxbasic.core as bsc_core

file_paths = bsc_storage.StgDirectory.get_all_file_paths(
    'Z:/temporaries/rig_images', ext_includes=['.webp']
)

for i in file_paths:
    bsc_core.BscFfmpegVideo.convert_webp(
        i, '{}.png'.format(os.path.splitext(i)[0])
    )
