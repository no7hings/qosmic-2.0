# coding:utf-8
import lxbasic.storage as bsc_storage

print bsc_storage.StgFileOpt(
    'Z:/resources/mixamo/Free Test/gangnam style.fbx'
).to_hash_uuid()

print bsc_storage.StgFileOpt(
    'Z:/resources/mixamo/gangnam style.fbx'
).to_hash_uuid()
