# coding:utf-8
import qsm_lazy_resource.extra.asset.scripts as s

s.AssetBatchRegisterOpt(
    'QSM_TST', '测试'
).execute(character=True, prop=True, scenery=True)
