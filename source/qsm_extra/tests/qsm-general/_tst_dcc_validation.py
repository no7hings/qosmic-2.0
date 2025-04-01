# coding:utf-8
import lxbasic.storage as bsc_storage

import lnx_dcc_tool_prc.validation.core as lzy_vld_core

print(
    lzy_vld_core.DccValidationOptions('lazy-validation/option/scenery').to_result_dict_for_mesh_count(
        bsc_storage.StgFileOpt(
            'Z:/caches/temporary/.asset-cache/mesh-count/1MP/4FA75052-080C-3322-8407-850758131841.json'
        ).set_read()
    )
)


print(
    lzy_vld_core.DccValidationOptions('lazy-validation/option/scenery').to_result_dict_for_component_mesh_count(
        bsc_storage.StgFileOpt(
            'Z:/caches/temporary/.asset-cache/mesh-count/1MP/4FA75052-080C-3322-8407-850758131841.json'
        ).set_read()
    )
)
