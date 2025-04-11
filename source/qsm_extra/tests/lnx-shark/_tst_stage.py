# coding:utf-8
import lnx_parsor.parse as c

stage_default = c.Stage(scheme='default')

print(stage_default.Roots.disorder)

stage_test = c.Stage(scheme='test')

print(stage_test.Roots.disorder)
