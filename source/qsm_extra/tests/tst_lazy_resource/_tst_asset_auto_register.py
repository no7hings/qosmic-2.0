# coding:utf-8
import lnx_resora.resource_types.asset.scripts as s

s.AssetBatchRegisterOpt(
    'QSM_TST', '测试'
).execute(character=True, prop=True, scenery=True)
