# coding:utf-8
import lxbasic.storage as bsc_storage

f = 'Z:/temporaries/montage_test/test_1.jz'

bsc_storage.StgGzipFileOpt(
    f, '.json'
).set_write(dict(test=0))

print bsc_storage.StgGzipFileOpt(
    f, '.json'
).set_read()
