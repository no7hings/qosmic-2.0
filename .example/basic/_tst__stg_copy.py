# coding:utf-8
import lxbasic.storage as bsc_storage

d = bsc_storage.StgDirectoryOpt(
    '/l/prod/xkt/publish/assets/chr/jiguang/srf/surfacing/jiguang.srf.surfacing.v096/texture'
)


d.copy_to_directory(
    '/l/temp/temporary/builder/2023_1121-dongchangbao/jiguang/texture'
)
