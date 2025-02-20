# coding:utf-8
import lxbasic.storage as bsc_storage

import lnx_resora.resource_types.video.scripts as s

file_paths = bsc_storage.StgDirectoryOpt('X:/videos/测试/video').get_all_file_paths(ext_includes=['.mov', '.mp4', '.avi'])

s.VideoRegisterBatch('resource_video_14', file_paths).execute()
