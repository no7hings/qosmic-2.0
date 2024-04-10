# coding:utf-8
import lxtool.comparer.gui.abstracts as cpr_gui_abstracts

import lxkatana.core as ktn_core

import lxkatana.dcc.objects as ktn_dcc_objects

import lxkatana.fnc.objects as ktn_fnc_objects


class PnlComparerForAssetGeometryDcc(cpr_gui_abstracts.AbsPnlComparerForAssetGeometryDcc):
    DCC_NODE_CLS = ktn_dcc_objects.Node
    #
    FNC_COMPARER_FOR_DCC_GEOMETRY = ktn_fnc_objects.FncComparerForGeometry
    #
    DCC_SELECTION_CLS = ktn_core.KtnSGSelectionOpt
    #
    DCC_NAMESPACE = 'usd'
    DCC_PATHSEP = None
    #
    DCC_LOCATION = '/master/hi'
    #
    DCC_LOCATION_FOR_GEOMETRY = '/root/world/geo'

    def __init__(self, session, *args, **kwargs):
        super(PnlComparerForAssetGeometryDcc, self).__init__(session, *args, **kwargs)

    def post_setup_fnc(self):
        scene_src_file_path = ktn_dcc_objects.Scene.get_current_file_path()
        self._options_prx_node.set(
            'scene.file', scene_src_file_path
        )
