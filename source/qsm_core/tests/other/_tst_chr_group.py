# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.pinyin as bsc_pinyin

g = bsc_core.BscChrGroup()

g_0 = bsc_core.BscChrGroup()


print g is g_0

print g_0.groups()

print g_0.get_group('A')

print g_0.get_group(bsc_pinyin.Text.find_first_chr('测试'))
