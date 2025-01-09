# coding:utf-8
import lxbasic.storage as bsc_storage

raw = bsc_storage.StgFileOpt(
    '/job/CFG/SHOW-CFG/NSA_DEV/presets/global.storage.json'
).set_read()

bsc_storage.StgFileOpt(
    '/data/f/json-temp/global.storage.yml'
).set_write(raw)
