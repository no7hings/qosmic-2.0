# coding:utf-8
import lxtool.comparer.gui.abstracts as cpr_gui_abstracts

import lxmaya.dcc.objects as mya_dcc_objects

import lxmaya.fnc.objects as mya_fnc_objects


class PnlComparerForAssetGeometryDcc(cpr_gui_abstracts.AbsPnlComparerForAssetGeometryDcc):
    DCC_NODE_CLS = mya_dcc_objects.Node

    FNC_COMPARER_FOR_DCC_GEOMETRY = mya_fnc_objects.FncComparerForGeometry

    DCC_SELECTION_CLS = mya_dcc_objects.Selection
    DCC_NAMESPACE = 'usd'
    DCC_PATHSEP = '|'

    DCC_LOCATION = '/master/mod/hi'
    DCC_LOCATION_SOURCE = '/master/hi'

    DCC_LOCATION_FOR_GEOMETRY = None

    def __init__(self, session, *args, **kwargs):
        super(PnlComparerForAssetGeometryDcc, self).__init__(session, *args, **kwargs)

    def post_setup_fnc(self):
        scene_src_file_path = mya_dcc_objects.Scene.get_current_file_path()
        self._options_prx_node.set(
            'scene.file', scene_src_file_path
        )
