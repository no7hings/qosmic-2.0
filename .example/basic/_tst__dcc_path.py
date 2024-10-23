# coding:utf-8
import lxbasic.core as bsc_core

o = bsc_core.BscPortPathOpt('array.array')

print bsc_core.BscPortPathOpt('array').get_parent_path()
print bsc_core.BscPortPathOpt('array.array').get_parent_path()

print bsc_core.BscPortPathOpt('array.array').get_component_paths()
