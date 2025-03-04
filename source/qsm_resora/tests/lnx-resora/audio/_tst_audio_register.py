# coding:utf-8
import lxbasic.storage as bsc_storage

import lnx_resora_extra.media.audio.scripts as s

file_paths = bsc_storage.StgDirectoryOpt('X:/audios/测试/sfx').get_all_file_paths(ext_includes=['.wav', '.mp3'])

s.AudioRegisterBatch('resource_audio_11', file_paths, ).execute()
