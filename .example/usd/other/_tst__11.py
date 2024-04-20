# coding:utf-8
import lxbasic.storage as bsc_storage


print bsc_storage.StgFileMtdForMultiply.convert_to(
    '/l/temp/td/dongchangbao/tx_convert_1/nngongshifu_cloth_mask/nngongshifu_cloth_mask.1001.1012.exr',
    ['*.<udim>.####.{format}', '*.####.{format}']
)

print bsc_storage.StgFileMtdForMultiply.convert_to(
    '/l/temp/td/dongchangbao/tx_convert_1/nngongshifu_cloth_mask/nngongshifu_cloth_mask.1001.exr',
    ['*.<udim>.####.{format}', '*.####.{format}']
)
