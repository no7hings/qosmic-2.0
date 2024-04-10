# coding:utf-8
import lxbasic.fnc.abstracts as bsc_fnc_abstracts
# maya dcc
from ...dcc import objects as mya_dcc_objects

from ...dcc import operators as mya_dcc_operators
# maya fnc
from . import base as mya_fnc_obj_base


class FncMatcherForDccMesh(bsc_fnc_abstracts.AbsFncMatcherForDccMesh):
    FNC_DCC_MESH_CLS = mya_fnc_obj_base.FncDccMesh

    def __init__(self, *args, **kwargs):
        super(FncMatcherForDccMesh, self).__init__(*args, **kwargs)


class FncRepairerForUsdMesh(bsc_fnc_abstracts.AbsFncRepairerForUsdMesh):
    FNC_USD_MESH_CLS = mya_fnc_obj_base.FncNodeForUsdMesh

    def __init__(self, *args, **kwargs):
        super(FncRepairerForUsdMesh, self).__init__(*args, **kwargs)


class FncComparerForGeometry(bsc_fnc_abstracts.AbsFncComparerForDccGeometry):
    DCC_SCENE_CLS = mya_dcc_objects.Scene
    DCC_SCENE_OPT_CLS = mya_dcc_operators.SceneOpt

    FNC_MATCHER_FOR_DCC_MESH_CLS = FncMatcherForDccMesh
    FNC_REPAIRER_FOR_USD_MESH_CLS = FncRepairerForUsdMesh

    RSV_KEYWORD = 'asset-geometry-usd-payload-file'
    DCC_NAMESPACE = 'maya'

    def __init__(self, *args, **kwargs):
        super(FncComparerForGeometry, self).__init__(*args, **kwargs)
