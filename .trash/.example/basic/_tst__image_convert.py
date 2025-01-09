# coding:utf-8
import lxbasic.storage as bsc_storage

t = bsc_storage.ImgOiioOptForTexture(
    'E:/myworkspace/lynxi-root-2.0/packages/qsm_resource/resources/assets/library/hdri/srgb/StinsonBeach.exr'
)

t.convert_to(
    'E:/myworkspace/lynxi-root-2.0/packages/qsm_resource/resources/assets/library/hdri/srgb/StinsonBeach.png'
)
