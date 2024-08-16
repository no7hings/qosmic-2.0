# coding:utf-8
import lxbasic.core as bsc_core

video_path = 'Z:/libraries/lazy-resource/all/maya_cfx/bo_lang_A/video/bo_lang_A.mov'

bsc_core.BscFfmpeg.extract_all_frames(
    video_path, 'png'
)

