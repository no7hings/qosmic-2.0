# coding:utf-8
import lxbasic.pinyin as bsc_pinyin

print bsc_pinyin.Text.cleanup(
    'A001_002 测试'
)

print bsc_pinyin.Text.cleanup(
    'A001_002_测试'
)
