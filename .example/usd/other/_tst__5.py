# coding:utf-8
import lxusd.core as usd_core

f = '/l/prod/cgm/publish/assets/chr/td_test/mod/modeling/td_test.mod.modeling.v056/set/usd/td_test.usda'

s = usd_core.UsdStageOpt(f)

s.set_active_at('/master/shape', True)

print s.get_radius((0, 0, 0))
