# coding:utf-8
import lxbasic.dcc.core as bsc_dcc_core

import lxusd.fnc.objects as usd_fnc_objects

print usd_fnc_objects.FncComparerForGeometry(
    option=dict(
        file_src='/l/prod/cgm/publish/assets/flg/xiangzhang_tree_g/mod/modeling/xiangzhang_tree_g.mod.modeling.v003/cache/usd/geo/hi.usd',
        file_tgt='/l/prod/cgm/publish/assets/flg/xiangzhang_tree_g/mod/mod_dynamic/xiangzhang_tree_g.mod.mod_dynamic.v001/cache/usd/geo/hi.usd',
        location='/master/hi'
    )
).generate_results(
    check_status_includes=[
        bsc_dcc_core.DccMeshCheckStatus.Addition,
        bsc_dcc_core.DccMeshCheckStatus.Deletion,
        #
        bsc_dcc_core.DccMeshCheckStatus.PathChanged,
        bsc_dcc_core.DccMeshCheckStatus.PathExchanged,
        #
        bsc_dcc_core.DccMeshCheckStatus.FaceVerticesChanged
    ]
)
