# coding:utf-8
import lxgeneral.dcc.core as gnl_dcc_core

import lxusd.fnc.objects as usd_fnc_objects

print usd_fnc_objects.FncComparerForGeometry(
    option=dict(
        file_src='/l/prod/cgm/publish/assets/flg/xiangzhang_tree_g/mod/modeling/xiangzhang_tree_g.mod.modeling.v003/cache/usd/geo/hi.usd',
        file_tgt='/l/prod/cgm/publish/assets/flg/xiangzhang_tree_g/mod/mod_dynamic/xiangzhang_tree_g.mod.mod_dynamic.v001/cache/usd/geo/hi.usd',
        location='/master/hi'
    )
).generate_results(
    check_status_includes=[
        gnl_dcc_core.DccMeshCheckStatus.Addition,
        gnl_dcc_core.DccMeshCheckStatus.Deletion,
        #
        gnl_dcc_core.DccMeshCheckStatus.PathChanged,
        gnl_dcc_core.DccMeshCheckStatus.PathExchanged,
        #
        gnl_dcc_core.DccMeshCheckStatus.FaceVerticesChanged
    ]
)
