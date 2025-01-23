# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_lazy_resource.extra.video.scripts as s

file_paths = bsc_storage.StgDirectoryOpt('X:/videos/测试').get_all_file_paths(ext_includes=['.mov', '.mp4', '.avi'])

s.VideoBatchRegister('video_test', file_paths).execute()
