# coding:utf-8
import lxbasic.fnc.abstracts as bsc_fnc_abstracts
# katana
from ... import core as ktn_core
# katana dcc
from ...dcc import operators as ktn_dcc_operators


class FncMatcherForDccMesh(bsc_fnc_abstracts.AbsFncMatcherForDccMesh):
    FNC_DCC_MESH_CLS = None

    def __init__(self, *args, **kwargs):
        super(FncMatcherForDccMesh, self).__init__(*args, **kwargs)


class FncComparerForGeometry(bsc_fnc_abstracts.AbsFncComparerForDccGeometry):
    DCC_SCENE_CLS = None
    DCC_SCENE_OPT_CLS = None
    #
    FNC_MATCHER_FOR_DCC_MESH_CLS = FncMatcherForDccMesh
    FNC_REPAIRER_FOR_USD_MESH_CLS = None
    #
    RSV_KEYWORD = 'asset-geometry-usd-payload-file'
    DCC_NAMESPACE = 'usd'

    def __init__(self, *args):
        super(FncComparerForGeometry, self).__init__(*args)

    def _update_target_fnc(self):
        import lxbasic.core as bsc_core

        import lxusd.dcc.objects as usd_dcc_objects

        import lxusd.dcc.operators as usd_dcc_operators

        w_s = ktn_core.WorkspaceSetting()
        opt = w_s.get_current_look_output_opt_force()
        if opt is None:
            return False

        s = ktn_dcc_operators.LookOutputOpt(opt)

        usd_file_path = s.get_geometry_uv_map_usd_source_file()
        if usd_file_path is not None:
            location = self._location

            hash_key = bsc_core.UuidMtd.generate_by_file(usd_file_path)
            self._dcc_scene_tgt = usd_dcc_objects.Scene()
            if hash_key in bsc_fnc_abstracts.AbsFncComparerForDccGeometry.CACHE:
                self._dcc_scene_tgt = bsc_fnc_abstracts.AbsFncComparerForDccGeometry.CACHE[hash_key]
                self._dcc_universe_tgt = self._dcc_scene_tgt.universe
            else:
                self._dcc_scene_tgt.load_from_dot_usd(usd_file_path, location)
                bsc_fnc_abstracts.AbsFncComparerForDccGeometry.CACHE[hash_key] = self._dcc_scene_tgt
                self._dcc_universe_tgt = self._dcc_scene_tgt.universe

            self._scene_usd_scene_opt = usd_dcc_operators.SceneOpt(self._dcc_scene_tgt.usd_stage, self.DCC_NAMESPACE)
            self._dcc_comparer_data_tgt = self._scene_usd_scene_opt.get_mesh_comparer_data(usd_file_path)
            self._dcc_geometries_tgt = []
            mesh_type = self._dcc_universe_tgt.get_obj_type('Mesh')
            if mesh_type is not None:
                self._dcc_geometries_tgt = mesh_type.get_objs()
