# coding:utf-8
import lxusd.core as usd_core

print usd_core.UsdStageOpt(
    '/l/prod/cjd/publish/shots/e10/e10110/set/registry/e10110.set.registry/manifest/usd/e10110.usda'
).get_objs(
    '/assets/chr/qunzhongnan_c*'
)
