# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_lazy_resource.resource_types.audio.scripts as lzy_rsc_etd_ado_scripts

file_paths = bsc_storage.StgDirectoryOpt('X:/audios/测试').get_all_file_paths(ext_includes=['.wav', '.mp3'])

lzy_rsc_etd_ado_scripts.AudioBatchRegister('audio_test', file_paths, ).execute()
