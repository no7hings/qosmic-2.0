# coding:utf-8
import lxbasic.core as bsc_core


print bsc_core.PtnFileTilesMtd.get_is_valid(
    'test.<udim>.jpg'
)

print bsc_core.PtnFileTilesMtd.get_is_valid(
    'test.<f>.jpg'
)

print bsc_core.PtnFileTilesMtd.get_is_valid(
    'test.jpg'
)

