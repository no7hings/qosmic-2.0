# coding:utf-8
import lxbasic.core as bsc_core

o = bsc_core.PthPortOpt('array.array')

print bsc_core.PthPortOpt('array').get_parent_path()
print bsc_core.PthPortOpt('array.array').get_parent_path()

print bsc_core.PthPortOpt('array.array').get_component_paths()
