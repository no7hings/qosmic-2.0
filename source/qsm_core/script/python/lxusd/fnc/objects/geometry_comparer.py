# coding:utf-8
import lxbasic.fnc.abstracts as bsc_fnc_abstracts


class FncMatcherForDccMesh(bsc_fnc_abstracts.AbsFncMatcherForDccMesh):
    FNC_DCC_MESH_CLS = None

    def __init__(self, *args, **kwargs):
        super(FncMatcherForDccMesh, self).__init__(*args, **kwargs)


class FncComparerForGeometry(bsc_fnc_abstracts.AbsFncComparerForUsdGeometry):
    FNC_MATCHER_FOR_DCC_MESH_CLS = FncMatcherForDccMesh

    def __init__(self, *args, **kwargs):
        super(FncComparerForGeometry, self).__init__(*args, **kwargs)
