# coding:utf-8
import lxbasic.storage as bsc_storage

video_path = 'Z:/libraries/lazy-resource/all/maya_cfx/bo_lang_A/video/bo_lang_A.mov'

thumbnail_path = 'Z:/libraries/lazy-resource/all/maya_cfx/bo_lang_A/thumbnail/bo_lang_A.jpg'

bsc_storage.VdoFileOpt(video_path).create_thumbnail(
    thumbnail_path
)
