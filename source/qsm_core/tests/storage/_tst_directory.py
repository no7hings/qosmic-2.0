# coding:utf-8
import lxbasic.storage as bsc_storage

d = bsc_storage.StgDirectoryOpt(
    'X:/videos/测试/MoCap'
)

print(d.get_file_paths(ext_includes=['.fbx']))