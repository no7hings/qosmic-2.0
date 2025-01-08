# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_lazy_rsc.scripts as qsm_rsc_scripts

file_paths = bsc_storage.StgDirectoryOpt('X:/videos/测试').get_all_file_paths(ext_includes=['.mov', '.mp4', '.avi'])

qsm_rsc_scripts.VideoBatchRegister('video_test', file_paths).execute()
