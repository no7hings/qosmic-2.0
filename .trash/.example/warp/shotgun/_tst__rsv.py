# coding:utf-8
import lxresolver.core as rsv_core

import lxshotgun.rsv.scripts as stg_rsv_scripts

import lxbasic.extra.methods as bsc_etr_methods

resolver = rsv_core.RsvBase.generate_root()

rsv_task = resolver.get_rsv_task(
    project='nsa_dev',
    asset='td_test',
    task='srf_anishading'
)

print rsv_task


# print stg_rsv_scripts.RsvShotgunHookOpt.get_new_registry_file_data_fnc(
#     rsv_task, version='v018'
# )

data = stg_rsv_scripts.RsvShotgunHookOpt.get_new_dependency_file_data_fnc(
    rsv_task, version='v018'
)

stg_version = stg_rsv_scripts._stg_rsv_obj_utility.RsvStgTaskOpt(rsv_task).get_stg_version(version='v018')

print stg_version['id']

for i in data:
    i_keyword, i_result = i
    bsc_etr_methods.EtrBase.register_version_file_dependency(
        version_id=stg_version['id'],
        keyword=i_keyword,
        result=i_result
    )
